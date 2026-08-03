"""Local FastAPI application for operating JobHunter without memorizing CLI commands."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jobhunter.analysis_service import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_PROMPT_VERSION,
    PROMPT_VERSION,
    JobAnalysisService,
    format_analysis_batch_summary,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.evidence import EvidenceStore
from jobhunter.inference import LMStudioProvider
from jobhunter.job_audit import JobDetailAuditor, format_job_audit
from jobhunter.job_catalog import JobCatalog
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.job_workflow import JobWorkflowStore
from jobhunter.jobinja_batch import JobinjaBatchFetchService, format_batch_fetch_summary
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.jobinja_discovery import (
    DiscoverySearch,
    JobinjaDiscoveryService,
    format_discovery_summary,
)
from jobhunter.jobinja_sync import JobinjaSyncService, JobinjaSyncSummary
from jobhunter.lifecycle import LifecycleStore
from jobhunter.market_insights import MarketInsights
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore
from jobhunter.translation import GoogleCloudTranslationProvider, LMStudioTranslationProvider
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_export import export_english_corpus
from jobhunter.translation_service import TranslationService, format_translation_batch_summary
from jobhunter.translation_store import TranslationStore
from jobhunter.web.operations import (
    OperationBusyError,
    WebOperationManager,
    WebOperationResult,
)
from jobhunter.web.presentation import format_web_sync_summary
from jobhunter.web.queries import WebRepository
from jobhunter.web.quick_add import parse_quick_add_input

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _jobinja_client(settings: Settings) -> JobinjaClient:
    return JobinjaClient(
        user_agent=settings.jobinja_user_agent,
        timeout_seconds=settings.jobinja_request_timeout_seconds,
        max_retries=settings.jobinja_max_retries,
    )


def _observation_store(settings: Settings) -> JobDetailObservationStore:
    return JobDetailObservationStore(settings.database_path)


def _detail_service(settings: Settings) -> JobinjaDetailService:
    return JobinjaDetailService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        observation_store=_observation_store(settings),
        lifecycle_store=LifecycleStore(settings.database_path),
    )


def _batch_service(settings: Settings) -> JobinjaBatchFetchService:
    return JobinjaBatchFetchService(
        detail_service=_detail_service(settings),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )


def _discovery_service(settings: Settings, *, request_budget: int) -> JobinjaDiscoveryService:
    return JobinjaDiscoveryService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
        request_budget=request_budget,
    )


def _translation_service(settings: Settings) -> TranslationService:
    provider = None
    if (
        settings.translation_enabled
        and settings.translation_provider == "google-cloud"
        and not settings.google_translation_api_key
    ):
        raise ValueError(
            "Google translation is enabled but "
            "JOBHUNTER_GOOGLE_TRANSLATION_API_KEY is not configured"
        )
    if settings.translation_enabled and settings.translation_provider == "lm-studio":
        provider = LMStudioTranslationProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.effective_translation_lm_studio_model(),
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
            max_tokens=settings.translation_lm_studio_max_tokens,
            request_character_target=settings.translation_lm_studio_character_target,
        )
    elif settings.translation_enabled and settings.translation_provider == "google-cloud":
        provider = GoogleCloudTranslationProvider(
            api_key=settings.google_translation_api_key or "",
            model=settings.google_translation_model,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
        )
    return TranslationService(
        store=TranslationStore(settings.database_path),
        provider=provider,
        target_language=settings.translation_target_language,
    )


def _analysis_service(settings: Settings) -> JobAnalysisService:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisService(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=LMStudioProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


def _market_insights(settings: Settings) -> MarketInsights:
    return MarketInsights(
        settings.database_path,
        analysis_model=settings.effective_analysis_lm_studio_model(),
        analysis_prompt_version=PROMPT_VERSION,
        analysis_schema_version=ANALYSIS_SCHEMA_VERSION,
    )


def _configured_searches(settings: Settings, *, limit: int) -> list[DiscoverySearch]:
    searches = [
        DiscoverySearch(name=item.name, url=item.url, max_pages=item.max_pages)
        for item in settings.jobinja_searches
        if item.enabled
    ]
    searches.extend(
        DiscoverySearch(name=item.name, url=item.url, max_pages=item.max_pages)
        for item in settings.expanded_keyword_searches()
    )
    unique_by_url: dict[str, DiscoverySearch] = {}
    for search in searches:
        unique_by_url.setdefault(search.url, search)
    return list(unique_by_url.values())[:limit]


def _csrf(request: Request, submitted: str) -> None:
    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _safe_return_to(value: str) -> str:
    value = value.strip()
    if value.startswith("/") and not value.startswith("//"):
        return value
    return ""


def _return_label(return_to: str) -> str:
    if return_to == "/":
        return "Back to overview"
    if return_to.startswith("/jobs/"):
        return "Back to job"
    if return_to.startswith("/jobs"):
        return "Back to jobs"
    if return_to.startswith("/market"):
        return "Back to market"
    return "Back"


def _operation_redirect(
    operation_id: str,
    *,
    return_to: str = "",
    auto_return: bool = False,
) -> RedirectResponse:
    params: dict[str, str] = {}
    safe_return = _safe_return_to(return_to)
    if safe_return:
        params["return_to"] = safe_return
    if auto_return:
        params["auto_return"] = "1"
    query = f"?{urlencode(params)}" if params else ""
    return RedirectResponse(url=f"/operations/{operation_id}{query}", status_code=303)


def _start_operation(
    request: Request,
    name: str,
    action,
    *,
    return_to: str = "",
    auto_return: bool = False,
) -> RedirectResponse:
    try:
        operation = request.app.state.operations.start(name, action)
    except OperationBusyError as exc:
        return RedirectResponse(url=f"/?notice={str(exc)}", status_code=303)
    return _operation_redirect(
        operation.id,
        return_to=return_to,
        auto_return=auto_return,
    )


def _operation_result(summary: str, *, has_failures: bool) -> WebOperationResult:
    return WebOperationResult(
        summary=summary,
        status="completed_with_failures" if has_failures else "completed",
    )


def _template_context(request: Request, **extra):
    context = {
        "request": request,
        "csrf_token": request.app.state.csrf_token,
        "active_operation": request.app.state.operations.active(),
    }
    context.update(extra)
    return context


def _validate_sync_inputs(
    *,
    search_limit: int,
    request_budget: int,
    missing_limit: int,
    refresh_limit: int,
    refresh_after_hours: float,
) -> None:
    if not 1 <= search_limit <= 500 or not 1 <= request_budget <= 500:
        raise HTTPException(status_code=400, detail="search limits must be 1-500")
    if not 0 <= missing_limit <= 50 or not 0 <= refresh_limit <= 50:
        raise HTTPException(status_code=400, detail="detail limits must be 0-50")
    if missing_limit + refresh_limit > 50:
        raise HTTPException(status_code=400, detail="combined detail limit may not exceed 50")
    if refresh_after_hours <= 0:
        raise HTTPException(status_code=400, detail="refresh age must be positive")


def _run_sync(
    settings: Settings,
    *,
    search_limit: int,
    request_budget: int,
    missing_limit: int,
    refresh_limit: int,
    refresh_after_hours: float,
) -> JobinjaSyncSummary:
    return JobinjaSyncService(
        discovery_service=_discovery_service(settings, request_budget=request_budget),
        batch_service=_batch_service(settings),
        catalog=JobCatalog(settings.database_path),
        observations=_observation_store(settings),
        auditor=JobDetailAuditor(settings.database_path),
    ).run(
        _configured_searches(settings, limit=search_limit),
        missing_limit=missing_limit,
        refresh_limit=refresh_limit,
        refresh_after_hours=refresh_after_hours,
    )


def _successful_detail_ids(summary: JobinjaSyncSummary) -> tuple[str, ...]:
    if summary.detail_fetch is None:
        return ()
    return tuple(item.source_job_id for item in summary.detail_fetch.results)


def _translation_output(
    settings: Settings,
    job_ids: tuple[str, ...],
    *,
    requested: bool,
) -> str:
    if not requested or not job_ids:
        return ""
    summary = _translation_service(settings).run(source_job_ids=job_ids)
    return "\n\n" + format_translation_batch_summary(summary)


def _complete_processing_output(
    settings: Settings,
    job_ids: tuple[str, ...],
    *,
    requested: bool,
) -> str:
    if not requested or not job_ids:
        return ""
    if not settings.translation_enabled:
        return "\n\nComplete processing skipped: translation is disabled."

    translation = _translation_service(settings).run(source_job_ids=job_ids)
    output = "\n\n" + format_translation_batch_summary(translation)
    ready_ids = tuple(result.source_job_id for result in translation.results)
    if not ready_ids:
        return output + "\n\nEnglish analysis skipped: no fetched jobs have current English v2."
    if not settings.effective_analysis_lm_studio_model():
        return output + "\n\nEnglish analysis skipped: no analysis model is configured."

    analysis = _analysis_service(settings).run_english(
        ready_ids,
        limit=min(len(ready_ids), settings.analysis_batch_limit, 20),
    )
    return output + "\n\n" + format_analysis_batch_summary(analysis)


def _full_workflow_output(
    settings: Settings,
    *,
    search_limit: int,
    request_budget: int,
    missing_limit: int,
    refresh_limit: int,
    refresh_after_hours: float,
    translation_limit: int,
    analysis_limit: int,
) -> WebOperationResult:
    sync = _run_sync(
        settings,
        search_limit=search_limit,
        request_budget=request_budget,
        missing_limit=missing_limit,
        refresh_limit=refresh_limit,
        refresh_after_hours=refresh_after_hours,
    )
    has_failures = not sync.succeeded
    sections = ["Complete JobHunter market update", format_web_sync_summary(sync)]
    preferred_ids = _successful_detail_ids(sync)

    if settings.translation_enabled:
        translated = _translation_service(settings).run(
            missing=True,
            limit=translation_limit,
            preferred_ids=preferred_ids,
        )
        has_failures = has_failures or bool(translated.failures)
        sections.append(format_translation_batch_summary(translated))
    else:
        has_failures = True
        sections.append(
            "English v2 stage\nSkipped because translation is disabled in configuration."
        )

    model = settings.effective_analysis_lm_studio_model()
    if model:
        repository = WebRepository(settings.database_path, analysis_model=model)
        ready_rows = repository.list_jobs(
            detail="available",
            translation="available",
            analysis="missing",
            limit=500,
        )
        ready_set = {
            row.source_job_id
            for row in ready_rows
            if row.triage_state != "not_relevant"
        }
        ordered_ids = tuple(
            job_id
            for job_id in dict.fromkeys(
                (*preferred_ids, *(row.source_job_id for row in ready_rows))
            )
            if job_id in ready_set
        )
        if ordered_ids:
            analyzed = _analysis_service(settings).run_english(
                ordered_ids,
                limit=analysis_limit,
            )
            has_failures = has_failures or bool(analyzed.failures)
            sections.append(format_analysis_batch_summary(analyzed))
        else:
            sections.append(
                "English-projection evidence-backed job analysis\n"
                "No eligible current jobs need English analysis."
            )
    else:
        has_failures = True
        sections.append(
            "English-projection evidence-backed job analysis\n"
            "Skipped because no analysis model is configured."
        )

    market = _market_insights(settings).market_summary()
    sections.append(
        "Market view\n"
        f"Discovered Jobinja identities: {market.discovered_jobs}\n"
        f"Current parsed jobs: {market.current_parsed_jobs}\n"
        f"Current accepted English analyses: {market.analyzed_jobs}\n"
        f"Distinct employers in analyzed sample: {market.distinct_employers}\n"
        f"Responsibility claims: {market.responsibility_claims}\n"
        f"Requirement claims: {market.requirement_claims}\n"
        "Market reads only the normalized English-analysis contract; original-language analyses "
        "remain separate review artifacts."
    )
    if market.sample_warning:
        sections.append(f"Market sampling warning\n{market.sample_warning}")
    if market.concentration_warning:
        sections.append(f"Market concentration warning\n{market.concentration_warning}")
    return _operation_result("\n\n".join(sections), has_failures=has_failures)


def create_app(
    settings: Settings,
    *,
    operations: WebOperationManager | None = None,
) -> FastAPI:
    """Build the local browser application around an already validated Settings object."""

    app = FastAPI(title="JobHunter", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings
    app.state.operations = operations or WebOperationManager()
    app.state.csrf_token = secrets.token_urlsafe(32)
    app.state.web_repository = WebRepository(
        settings.database_path,
        analysis_model=settings.effective_analysis_lm_studio_model(),
    )
    app.mount("/static", StaticFiles(directory=str(_WEB_DIR / "static")), name="static")

    @app.middleware("http")
    async def local_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
        )
        return response

    @app.get("/", response_class=HTMLResponse)
    def dashboard(request: Request, notice: str = ""):
        repository: WebRepository = request.app.state.web_repository
        priorities = JobWorkflowStore(settings.database_path).prioritized_missing_job_ids(limit=5)
        missing_rows = {
            row.source_job_id: row
            for row in repository.list_jobs(detail="missing", limit=500)
        }
        priority_preview = tuple(
            {"priority": item, "job": missing_rows.get(item.source_job_id)}
            for item in priorities
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="dashboard.html",
            context=_template_context(
                request,
                page="dashboard",
                notice=notice,
                stats=repository.dashboard_stats(),
                priority_preview=priority_preview,
                recent_runs=repository.recent_runs(limit=6),
                recent_operations=request.app.state.operations.recent()[:6],
                settings=settings,
            ),
        )

    @app.get("/jobs", response_class=HTMLResponse)
    def jobs(
        request: Request,
        q: str = "",
        detail: str = "all",
        translation: str = "all",
        lifecycle: str = "all",
        triage: str = "all",
        analysis: str = "all",
    ):
        repository: WebRepository = request.app.state.web_repository
        rows = repository.list_jobs(
            query=q,
            detail=detail,
            translation=translation,
            lifecycle=lifecycle,
            triage=triage,
            analysis=analysis,
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="jobs.html",
            context=_template_context(
                request,
                page="jobs",
                jobs=rows,
                q=q,
                detail=detail,
                translation=translation,
                lifecycle=lifecycle,
                triage=triage,
                analysis=analysis,
                translation_enabled=settings.translation_enabled,
            ),
        )

    @app.get("/jobs/{source_job_id}", response_class=HTMLResponse)
    def job_detail(request: Request, source_job_id: str):
        store = JobHunterStore(settings.database_path)
        store.initialize()
        posting = store.get_job(source_job_id)
        if posting is None:
            raise HTTPException(status_code=404, detail="Job not found in the local catalog")
        detail = store.get_latest_job_detail(source_job_id)
        translation_service = _translation_service(settings)
        translation = translation_service.current_artifact(source_job_id)
        latest_any_translation = TranslationStore(settings.database_path).latest_artifact(
            source_job_id
        )
        legacy_translation = (
            latest_any_translation
            if latest_any_translation is not None
            and latest_any_translation.translation_schema_version != TRANSLATION_SCHEMA_VERSION
            else None
        )
        model = settings.effective_analysis_lm_studio_model()
        analysis_store = AnalysisStore(settings.database_path)
        english_analysis_artifact = analysis_store.latest_current(
            source_job_id,
            model=model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        original_analysis_artifact = analysis_store.latest_current(
            source_job_id,
            model=model,
            prompt_version=ORIGINAL_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="job_detail.html",
            context=_template_context(
                request,
                page="jobs",
                source_job_id=source_job_id,
                posting=posting,
                detail=detail,
                translation=translation,
                legacy_translation=legacy_translation,
                english_analysis_artifact=english_analysis_artifact,
                original_analysis_artifact=original_analysis_artifact,
                workflow=JobWorkflowStore(settings.database_path).get_state(source_job_id),
                observations=_observation_store(settings).list_for_job(source_job_id, limit=20),
                lifecycle_events=LifecycleStore(settings.database_path).list_for_job(
                    source_job_id, limit=20
                ),
                search_provenance=_market_insights(settings).job_search_provenance(
                    source_job_id
                ),
                audit=JobDetailAuditor(settings.database_path).audit(
                    source_job_ids=(source_job_id,), limit=1
                ),
                translation_enabled=settings.translation_enabled,
                analysis_model=model,
            ),
        )

    @app.get("/searches", response_class=HTMLResponse)
    def searches(request: Request):
        catalog = settings.search_catalog()
        configured = _configured_searches(
            settings,
            limit=settings.jobinja_max_expanded_searches,
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="searches.html",
            context=_template_context(
                request,
                page="searches",
                catalog=catalog,
                configured_searches=configured,
                effectiveness=_market_insights(settings).search_effectiveness(limit=200),
                settings=settings,
            ),
        )

    @app.get("/market", response_class=HTMLResponse)
    def market(request: Request):
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="market.html",
            context=_template_context(
                request,
                page="market",
                market=_market_insights(settings).market_summary(),
            ),
        )

    @app.get("/operations", response_class=HTMLResponse)
    def operations_page(request: Request):
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="operations.html",
            context=_template_context(
                request,
                page="operations",
                operations=request.app.state.operations.recent(),
                settings=settings,
            ),
        )

    @app.get("/operations/{operation_id}", response_class=HTMLResponse)
    def operation_detail(
        request: Request,
        operation_id: str,
        return_to: str = "",
        auto_return: str = "",
    ):
        operation = request.app.state.operations.get(operation_id)
        if operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        safe_return = _safe_return_to(return_to)
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="operation_detail.html",
            context=_template_context(
                request,
                page="operations",
                operation=operation,
                return_to=safe_return,
                return_label=_return_label(safe_return),
                auto_return=auto_return == "1" and bool(safe_return),
            ),
        )

    @app.get("/api/operations/{operation_id}", response_class=JSONResponse)
    def operation_status(request: Request, operation_id: str):
        operation = request.app.state.operations.get(operation_id)
        if operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        return operation.to_dict()

    @app.get("/system", response_class=HTMLResponse)
    def system_page(request: Request):
        source_store = TranslationStore(settings.database_path)
        sources = source_store.latest_source_versions(limit=5000)
        current_english = sum(
            _translation_service(settings).current_artifact(source.source_job_id) is not None
            for source in sources
        )
        model = settings.effective_analysis_lm_studio_model()
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="system.html",
            context=_template_context(
                request,
                page="system",
                settings=settings,
                parsed_versions=len(sources),
                english_artifacts=current_english,
                analysis_artifacts=len(
                    AnalysisStore(settings.database_path).list_current(
                        limit=5000,
                        model=model,
                        prompt_version=ENGLISH_PROMPT_VERSION,
                        schema_version=ANALYSIS_SCHEMA_VERSION,
                    )
                ),
                translation_schema=TRANSLATION_SCHEMA_VERSION,
            ),
        )

    @app.post("/actions/sync")
    def start_sync(
        request: Request,
        csrf_token: Annotated[str, Form()],
        search_limit: Annotated[int, Form()],
        request_budget: Annotated[int, Form()],
        missing_limit: Annotated[int, Form()],
        refresh_limit: Annotated[int, Form()],
        refresh_after_hours: Annotated[float, Form()],
    ):
        _csrf(request, csrf_token)
        _validate_sync_inputs(
            search_limit=search_limit,
            request_budget=request_budget,
            missing_limit=missing_limit,
            refresh_limit=refresh_limit,
            refresh_after_hours=refresh_after_hours,
        )

        def action() -> WebOperationResult:
            summary = _run_sync(
                settings,
                search_limit=search_limit,
                request_budget=request_budget,
                missing_limit=missing_limit,
                refresh_limit=refresh_limit,
                refresh_after_hours=refresh_after_hours,
            )
            return _operation_result(
                format_web_sync_summary(summary),
                has_failures=not summary.succeeded,
            )

        return _start_operation(
            request,
            "Jobinja source sync",
            action,
            return_to="/",
        )

    @app.post("/actions/full-workflow")
    def start_full_workflow(
        request: Request,
        csrf_token: Annotated[str, Form()],
        search_limit: Annotated[int, Form()],
        request_budget: Annotated[int, Form()],
        missing_limit: Annotated[int, Form()],
        refresh_limit: Annotated[int, Form()],
        refresh_after_hours: Annotated[float, Form()],
        translation_limit: Annotated[int, Form()],
        analysis_limit: Annotated[int, Form()],
    ):
        _csrf(request, csrf_token)
        _validate_sync_inputs(
            search_limit=search_limit,
            request_budget=request_budget,
            missing_limit=missing_limit,
            refresh_limit=refresh_limit,
            refresh_after_hours=refresh_after_hours,
        )
        if not 1 <= translation_limit <= 50:
            raise HTTPException(status_code=400, detail="translation limit must be 1-50")
        if not 1 <= analysis_limit <= 20:
            raise HTTPException(status_code=400, detail="analysis limit must be 1-20")

        return _start_operation(
            request,
            "Complete market update",
            lambda: _full_workflow_output(
                settings,
                search_limit=search_limit,
                request_budget=request_budget,
                missing_limit=missing_limit,
                refresh_limit=refresh_limit,
                refresh_after_hours=refresh_after_hours,
                translation_limit=translation_limit,
                analysis_limit=analysis_limit,
            ),
            return_to="/",
        )

    @app.post("/actions/fetch-missing")
    def start_fetch_missing(
        request: Request,
        csrf_token: Annotated[str, Form()],
        limit: Annotated[int, Form()],
    ):
        _csrf(request, csrf_token)
        if not 1 <= limit <= 50:
            raise HTTPException(status_code=400, detail="missing-detail limit must be 1-50")

        def action() -> str | WebOperationResult:
            priorities = JobWorkflowStore(settings.database_path).prioritized_missing_job_ids(
                limit=limit
            )
            job_ids = tuple(item.source_job_id for item in priorities)
            if not job_ids:
                return (
                    "Priority detail backlog\n"
                    "No eligible discovered jobs need a detail-page fetch."
                )
            summary = _batch_service(settings).run(job_ids)
            lines = [
                "Priority detail backlog",
                f"Selected: {len(job_ids)}",
                "No market-search pages were requested for this operation.",
                "Priority is deterministic discovery evidence, not a career-fit score.",
                "",
            ]
            lines.extend(
                f"- {item.source_job_id}: priority {item.score}, "
                f"{item.distinct_searches} searches / {item.distinct_packs} packs"
                for item in priorities
            )
            lines.extend(["", format_batch_fetch_summary(summary)])
            return _operation_result(
                "\n".join(lines),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            "Fetch priority details",
            action,
            return_to="/",
        )

    @app.post("/actions/quick-add")
    def start_quick_add(
        request: Request,
        csrf_token: Annotated[str, Form()],
        value: Annotated[str, Form()],
        pages: Annotated[int, Form()],
        detail_limit: Annotated[int, Form()],
        translate_after: Annotated[bool, Form()] = False,
    ):
        _csrf(request, csrf_token)
        if not 1 <= pages <= 3:
            raise HTTPException(status_code=400, detail="Quick Add pages must be 1-3")
        if not 0 <= detail_limit <= 20:
            raise HTTPException(status_code=400, detail="Quick Add detail limit must be 0-20")
        if translate_after and not settings.translation_enabled:
            raise HTTPException(status_code=400, detail="Translation is disabled")
        try:
            target = parse_quick_add_input(value)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        def action() -> str:
            if target.kind == "job":
                assert target.job is not None
                store = JobHunterStore(settings.database_path)
                store.initialize()
                upserted = store.upsert_job(job=target.job, observed_at=datetime.now(UTC))
                detail_summary = _batch_service(settings).run((target.job.source_job_id,))
                successful_ids = tuple(item.source_job_id for item in detail_summary.results)
                state = "new local job" if upserted.is_new else "already known locally"
                output = "\n".join(
                    [
                        "Quick Add — direct Jobinja job",
                        f"Jobinja reference: {target.job.source_job_id}",
                        f"Catalog state: {state}",
                        "",
                        format_batch_fetch_summary(detail_summary),
                    ]
                )
                return output + _complete_processing_output(
                    settings,
                    successful_ids,
                    requested=translate_after,
                )

            assert target.search_url is not None
            discovery = _discovery_service(settings, request_budget=pages).run(
                (
                    DiscoverySearch(
                        name=target.search_name(),
                        url=target.search_url,
                        max_pages=pages,
                    ),
                )
            )
            selected_ids = discovery.discovered_job_ids[:detail_limit]
            output = "\n".join(
                [
                    f"Quick Add — {target.kind}",
                    f"Input: {target.display_value}",
                    "",
                    format_discovery_summary(discovery),
                ]
            )
            if not selected_ids:
                return output + "\n\nNo detail pages selected."
            detail_summary = _batch_service(settings).run(selected_ids)
            successful_ids = tuple(item.source_job_id for item in detail_summary.results)
            output += "\n\n" + format_batch_fetch_summary(detail_summary)
            return output + _complete_processing_output(
                settings,
                successful_ids,
                requested=translate_after,
            )

        label = (
            target.display_value
            if len(target.display_value) <= 54
            else target.display_value[:51] + "..."
        )
        return _start_operation(
            request,
            f"Quick Add: {label}",
            action,
            return_to="/jobs",
        )

    @app.post("/actions/audit")
    def start_audit(request: Request, csrf_token: Annotated[str, Form()]):
        _csrf(request, csrf_token)
        return _start_operation(
            request,
            "Parser audit",
            lambda: format_job_audit(JobDetailAuditor(settings.database_path).audit(limit=500)),
            return_to="/",
        )

    @app.post("/actions/translate-missing")
    def start_translate_missing(
        request: Request,
        csrf_token: Annotated[str, Form()],
        limit: Annotated[int, Form()],
    ):
        _csrf(request, csrf_token)
        if not settings.translation_enabled:
            raise HTTPException(status_code=400, detail="Translation is disabled")
        if not 1 <= limit <= 50:
            raise HTTPException(status_code=400, detail="translation limit must be 1-50")

        def action() -> WebOperationResult:
            summary = _translation_service(settings).run(missing=True, limit=limit)
            return _operation_result(
                format_translation_batch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            "Repair / translate English corpus",
            action,
            return_to="/",
        )

    @app.post("/actions/analyze-ready")
    def start_analyze_ready(
        request: Request,
        csrf_token: Annotated[str, Form()],
        limit: Annotated[int, Form()],
    ):
        _csrf(request, csrf_token)
        if not 1 <= limit <= 20:
            raise HTTPException(status_code=400, detail="analysis limit must be 1-20")

        def action() -> str | WebOperationResult:
            rows = request.app.state.web_repository.list_jobs(
                detail="available",
                translation="available",
                analysis="missing",
                limit=500,
            )
            job_ids = tuple(
                row.source_job_id
                for row in rows
                if row.triage_state != "not_relevant"
            )
            if not job_ids:
                return (
                    "English-projection evidence-backed job analysis\n"
                    "No eligible current jobs need English analysis."
                )
            summary = _analysis_service(settings).run_english(job_ids, limit=limit)
            return _operation_result(
                format_analysis_batch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            "Analyze English-ready jobs",
            action,
            return_to="/",
        )

    @app.post("/actions/export")
    def start_export(request: Request, csrf_token: Annotated[str, Form()]):
        _csrf(request, csrf_token)

        def action() -> str:
            result = export_english_corpus(
                TranslationStore(settings.database_path),
                output_path=settings.data_dir / "exports/job_english_corpus.jsonl",
                limit=5000,
            )
            return (
                f"English corpus exported: {result.records} records\n"
                f"Path: {result.path}"
            )

        return _start_operation(
            request,
            "Export hardened English corpus",
            action,
            return_to="/",
        )

    @app.post("/actions/jobs-bulk")
    def jobs_bulk(
        request: Request,
        csrf_token: Annotated[str, Form()],
        bulk_action: Annotated[str, Form()],
        source_job_ids: Annotated[list[str], Form()],
    ):
        _csrf(request, csrf_token)
        job_ids = tuple(dict.fromkeys(item.strip() for item in source_job_ids if item.strip()))
        if not job_ids:
            raise HTTPException(status_code=400, detail="Select at least one job")
        if len(job_ids) > 50:
            raise HTTPException(status_code=400, detail="Select at most 50 jobs per bulk action")
        workflow_states = {
            "interested",
            "review_later",
            "not_relevant",
            "reviewed",
            "unreviewed",
        }
        if bulk_action in workflow_states:
            changed = JobWorkflowStore(settings.database_path).set_state(
                job_ids,
                triage_state=bulk_action,
            )
            return RedirectResponse(
                url=f"/jobs?notice=Updated+{changed}+jobs",
                status_code=303,
            )

        def action() -> WebOperationResult:
            if bulk_action == "fetch":
                summary = _batch_service(settings).run(job_ids)
                return _operation_result(
                    format_batch_fetch_summary(summary),
                    has_failures=bool(summary.failures),
                )
            if bulk_action == "translate":
                summary = _translation_service(settings).run(source_job_ids=job_ids)
                return _operation_result(
                    format_translation_batch_summary(summary),
                    has_failures=bool(summary.failures),
                )
            if bulk_action == "analyze_english":
                summary = _analysis_service(settings).run_english(
                    job_ids,
                    limit=min(len(job_ids), 20),
                )
                return _operation_result(
                    format_analysis_batch_summary(summary),
                    has_failures=bool(summary.failures),
                )
            if bulk_action == "analyze_original":
                summary = _analysis_service(settings).run_original(
                    job_ids,
                    limit=min(len(job_ids), 20),
                )
                return _operation_result(
                    format_analysis_batch_summary(summary),
                    has_failures=bool(summary.failures),
                )
            raise ValueError(f"Unsupported bulk action: {bulk_action}")

        if bulk_action not in {"fetch", "translate", "analyze_english", "analyze_original"}:
            raise HTTPException(status_code=400, detail="Unsupported bulk action")
        return _start_operation(
            request,
            f"Bulk {bulk_action.replace('_', ' ')}: {len(job_ids)} jobs",
            action,
            return_to="/jobs",
        )

    @app.post("/jobs/{source_job_id}/triage")
    def set_job_triage(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
        triage_state: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)
        JobWorkflowStore(settings.database_path).set_state(
            (source_job_id,),
            triage_state=triage_state,
        )
        return RedirectResponse(url=f"/jobs/{source_job_id}", status_code=303)

    @app.post("/jobs/{source_job_id}/fetch")
    def start_job_fetch(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
        return_to: Annotated[str, Form()] = "",
    ):
        _csrf(request, csrf_token)
        target = _safe_return_to(return_to) or f"/jobs/{source_job_id}"

        def action() -> WebOperationResult:
            summary = _batch_service(settings).run((source_job_id,))
            return _operation_result(
                format_batch_fetch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            f"Fetch {source_job_id}",
            action,
            return_to=target,
            auto_return=True,
        )

    @app.post("/jobs/{source_job_id}/translate")
    def start_job_translation(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)
        if not settings.translation_enabled:
            raise HTTPException(status_code=400, detail="Translation is disabled")

        def action() -> WebOperationResult:
            summary = _translation_service(settings).run(source_job_ids=(source_job_id,))
            return _operation_result(
                format_translation_batch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            f"Repair English: {source_job_id}",
            action,
            return_to=f"/jobs/{source_job_id}",
            auto_return=True,
        )

    @app.post("/jobs/{source_job_id}/analyze-english")
    def start_job_english_analysis(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            summary = _analysis_service(settings).run_english((source_job_id,), limit=1)
            return _operation_result(
                format_analysis_batch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            f"Analyze English: {source_job_id}",
            action,
            return_to=f"/jobs/{source_job_id}",
            auto_return=True,
        )

    @app.post("/jobs/{source_job_id}/analyze-original")
    def start_job_original_analysis(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            summary = _analysis_service(settings).run_original((source_job_id,), limit=1)
            return _operation_result(
                format_analysis_batch_summary(summary),
                has_failures=bool(summary.failures),
            )

        return _start_operation(
            request,
            f"Analyze Original: {source_job_id}",
            action,
            return_to=f"/jobs/{source_job_id}",
            auto_return=True,
        )

    return app
