"""Local FastAPI application for operating JobHunter without memorizing CLI commands."""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jobhunter.config import Settings
from jobhunter.evidence import EvidenceStore
from jobhunter.job_audit import JobDetailAuditor, format_job_audit
from jobhunter.job_catalog import JobCatalog
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_batch import JobinjaBatchFetchService, format_batch_fetch_summary
from jobhunter.jobinja_detail_service import JobinjaDetailService, JobNotFoundError
from jobhunter.jobinja_discovery import DiscoverySearch, JobinjaDiscoveryService
from jobhunter.jobinja_sync import JobinjaSyncService, format_sync_summary
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore
from jobhunter.translation import GoogleCloudTranslationProvider, LMStudioTranslationProvider
from jobhunter.translation_export import export_english_corpus
from jobhunter.translation_service import TranslationService, format_translation_batch_summary
from jobhunter.translation_store import TranslationStore
from jobhunter.web.operations import OperationBusyError, WebOperationManager
from jobhunter.web.queries import WebRepository

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _jobinja_client(settings: Settings) -> JobinjaClient:
    return JobinjaClient(
        user_agent=settings.jobinja_user_agent,
        timeout_seconds=settings.jobinja_request_timeout_seconds,
    )


def _observation_store(settings: Settings) -> JobDetailObservationStore:
    return JobDetailObservationStore(settings.database_path)


def _detail_service(settings: Settings) -> JobinjaDetailService:
    return JobinjaDetailService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        observation_store=_observation_store(settings),
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
            "Google translation is enabled but JOBHUNTER_GOOGLE_TRANSLATION_API_KEY "
            "is not configured"
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


def _configured_searches(settings: Settings, *, limit: int) -> list[DiscoverySearch]:
    searches = [
        DiscoverySearch(
            name=definition.name,
            url=definition.url,
            max_pages=definition.max_pages,
        )
        for definition in settings.jobinja_searches
        if definition.enabled
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
    expected = request.app.state.csrf_token
    if not secrets.compare_digest(submitted, expected):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _operation_redirect(operation_id: str) -> RedirectResponse:
    return RedirectResponse(url=f"/operations/{operation_id}", status_code=303)


def _start_operation(request: Request, name: str, action) -> RedirectResponse:
    try:
        operation = request.app.state.operations.start(name, action)
    except OperationBusyError as exc:
        return RedirectResponse(url=f"/?notice={str(exc)}", status_code=303)
    return _operation_redirect(operation.id)


def _template_context(request: Request, **extra):
    context = {
        "request": request,
        "csrf_token": request.app.state.csrf_token,
        "active_operation": request.app.state.operations.active(),
    }
    context.update(extra)
    return context


def create_app(
    settings: Settings,
    *,
    operations: WebOperationManager | None = None,
) -> FastAPI:
    """Build the local browser application around an already validated Settings object."""

    app = FastAPI(
        title="JobHunter",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.state.settings = settings
    app.state.operations = operations or WebOperationManager()
    app.state.csrf_token = secrets.token_urlsafe(32)
    app.state.web_repository = WebRepository(settings.database_path)
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
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="dashboard.html",
            context=_template_context(
                request,
                page="dashboard",
                notice=notice,
                stats=repository.dashboard_stats(),
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
    ):
        repository: WebRepository = request.app.state.web_repository
        rows = repository.list_jobs(
            query=q,
            detail=detail,
            translation=translation,
            lifecycle=lifecycle,
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
            ),
        )

    @app.get("/jobs/{source_job_id}", response_class=HTMLResponse)
    def job_detail(request: Request, source_job_id: str):
        detail = None
        error = None
        try:
            detail = _detail_service(settings).show(source_job_id)
        except JobNotFoundError as exc:
            error = str(exc)
        translation = TranslationStore(settings.database_path).latest_artifact(source_job_id)
        observations = _observation_store(settings).list_for_job(source_job_id, limit=20)
        audit = JobDetailAuditor(settings.database_path).audit(
            source_job_ids=(source_job_id,),
            limit=1,
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="job_detail.html",
            context=_template_context(
                request,
                page="jobs",
                source_job_id=source_job_id,
                detail=detail,
                translation=translation,
                observations=observations,
                audit=audit,
                error=error,
                translation_enabled=settings.translation_enabled,
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
                settings=settings,
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
    def operation_detail(request: Request, operation_id: str):
        operation = request.app.state.operations.get(operation_id)
        if operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="operation_detail.html",
            context=_template_context(
                request,
                page="operations",
                operation=operation,
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
        translation_store = TranslationStore(settings.database_path)
        sources = translation_store.latest_source_versions(limit=5000)
        artifacts = translation_store.list_latest_artifacts(limit=5000)
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="system.html",
            context=_template_context(
                request,
                page="system",
                settings=settings,
                parsed_versions=len(sources),
                english_artifacts=len(artifacts),
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
        if not 1 <= search_limit <= 500:
            raise HTTPException(status_code=400, detail="search_limit must be 1-500")
        if not 1 <= request_budget <= 500:
            raise HTTPException(status_code=400, detail="request_budget must be 1-500")
        if not 0 <= missing_limit <= 50 or not 0 <= refresh_limit <= 50:
            raise HTTPException(status_code=400, detail="detail limits must be 0-50")
        if missing_limit + refresh_limit > 50:
            raise HTTPException(status_code=400, detail="combined detail limit may not exceed 50")
        if refresh_after_hours <= 0:
            raise HTTPException(status_code=400, detail="refresh age must be positive")

        def action() -> str:
            selected = _configured_searches(settings, limit=search_limit)
            service = JobinjaSyncService(
                discovery_service=_discovery_service(settings, request_budget=request_budget),
                batch_service=_batch_service(settings),
                catalog=JobCatalog(settings.database_path),
                observations=_observation_store(settings),
                auditor=JobDetailAuditor(settings.database_path),
            )
            summary = service.run(
                selected,
                missing_limit=missing_limit,
                refresh_limit=refresh_limit,
                refresh_after_hours=refresh_after_hours,
            )
            output = format_sync_summary(summary)
            if settings.translation_enabled and settings.translation_auto_after_sync:
                preferred_ids = (
                    tuple(item.source_job_id for item in summary.detail_fetch.results)
                    if summary.detail_fetch is not None
                    else ()
                )
                translated = _translation_service(settings).run(
                    missing=True,
                    limit=settings.translation_batch_limit,
                    preferred_ids=preferred_ids,
                )
                output += "\n\n" + format_translation_batch_summary(translated)
            return output

        return _start_operation(request, "Jobinja sync", action)

    @app.post("/actions/audit")
    def start_audit(request: Request, csrf_token: Annotated[str, Form()]):
        _csrf(request, csrf_token)

        def action() -> str:
            report = JobDetailAuditor(settings.database_path).audit(limit=500)
            return format_job_audit(report)

        return _start_operation(request, "Parser audit", action)

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

        def action() -> str:
            summary = _translation_service(settings).run(missing=True, limit=limit)
            return format_translation_batch_summary(summary)

        return _start_operation(request, "Translate missing jobs", action)

    @app.post("/actions/export")
    def start_export(request: Request, csrf_token: Annotated[str, Form()]):
        _csrf(request, csrf_token)

        def action() -> str:
            output_path = settings.data_dir / "exports/job_english_corpus.jsonl"
            result = export_english_corpus(
                TranslationStore(settings.database_path),
                output_path=output_path,
                limit=5000,
            )
            return f"English corpus exported: {result.records} records\nPath: {result.path}"

        return _start_operation(request, "Export English corpus", action)

    @app.post("/jobs/{source_job_id}/fetch")
    def start_job_fetch(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)

        def action() -> str:
            summary = _batch_service(settings).run((source_job_id,))
            return format_batch_fetch_summary(summary)

        return _start_operation(request, f"Fetch {source_job_id}", action)

    @app.post("/jobs/{source_job_id}/translate")
    def start_job_translation(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)
        if not settings.translation_enabled:
            raise HTTPException(status_code=400, detail="Translation is disabled")

        def action() -> str:
            summary = _translation_service(settings).run(source_job_ids=(source_job_id,))
            return format_translation_batch_summary(summary)

        return _start_operation(request, f"Translate {source_job_id}", action)

    return app
