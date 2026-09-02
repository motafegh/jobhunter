"""Bounded browser review surface for per-job capability intelligence."""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    build_capability_intelligence_service,
    format_capability_intelligence,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import build_translation_service
from jobhunter.web.common import (
    TEMPLATES,
    operation_redirect,
    redirect_with_notice,
    require_csrf,
    template_context,
)
from jobhunter.web.operations import OperationBusyError, WebOperationLink, WebOperationResult


def register_capability_routes(app: FastAPI, settings: Settings) -> None:
    """Attach the bounded capability-intelligence review routes to the runtime web app."""

    @app.get(
        "/jobs/{source_job_id}/capability-intelligence",
        response_class=HTMLResponse,
        name="capability_intelligence_page",
    )
    def capability_page(request: Request, source_job_id: str):
        source_store = JobHunterStore(settings.database_path)
        source_store.initialize()
        posting = source_store.get_job(source_job_id)
        if posting is None:
            raise HTTPException(status_code=404, detail="Job not found in the local catalog")
        detail = source_store.get_latest_job_detail(source_job_id)
        analysis_model = settings.effective_analysis_lm_studio_model()
        capability_model = settings.effective_capability_lm_studio_model()
        translation = build_translation_service(settings).current_artifact(source_job_id)
        english_analysis = None
        if translation is not None and analysis_model is not None:
            english_analysis = AnalysisStore(settings.database_path).find_artifact(
                job_detail_version_id=translation.job_detail_version_id,
                translation_artifact_id=translation.id,
                require_translation_dependency=True,
                model=analysis_model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            )
            if (
                english_analysis is not None
                and english_analysis.semantic_review_status != "accepted"
            ):
                english_analysis = None
        capability_artifact = CapabilityIntelligenceStore(
            settings.database_path
        ).latest_current(
            source_job_id,
            model=capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        current_dependency = (
            capability_artifact is not None
            and english_analysis is not None
            and capability_artifact.analysis_artifact_id == english_analysis.id
            and english_analysis.translation_artifact_id is not None
            and capability_artifact.translation_artifact_id
            == english_analysis.translation_artifact_id
        )
        return TEMPLATES.TemplateResponse(
            request=request,
            name="capability_intelligence.html",
            context=template_context(
                request,
                page="jobs",
                source_job_id=source_job_id,
                posting=posting,
                detail=detail,
                english_analysis=english_analysis,
                capability_artifact=capability_artifact,
                capability_current=current_dependency,
                analysis_model=analysis_model,
                capability_model=capability_model,
            ),
        )

    @app.post("/jobs/{source_job_id}/capability-intelligence")
    def build_capability(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        require_csrf(request, csrf_token)

        def action() -> WebOperationResult:
            try:
                service = build_capability_intelligence_service(settings)
                result = service.analyze_job(source_job_id)
            except CapabilityIntelligenceError as exc:
                raise RuntimeError(f"Capability intelligence is not ready: {exc}") from exc

            artifact = CapabilityIntelligenceStore(settings.database_path).latest_current(
                source_job_id,
                model=result.model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
            )
            if artifact is None:
                raise RuntimeError("Capability artifact is unavailable after successful analysis")
            summary = (
                f"Capability intelligence: {source_job_id}\n"
                f"Outcome: {result.outcome}\n"
                f"Capabilities: {result.capabilities}\n\n"
                f"{format_capability_intelligence(artifact)}"
            )
            return WebOperationResult(
                summary=summary,
                status="completed",
                links=(
                    WebOperationLink(
                        label="Open capability",
                        url=f"/jobs/{source_job_id}/capability-intelligence",
                    ),
                    WebOperationLink(label="Open Phase-1 report", url="/report"),
                ),
            )

        try:
            operation = request.app.state.operations.start(
                f"Capability intelligence: {source_job_id}",
                action,
            )
        except OperationBusyError as exc:
            return redirect_with_notice(
                f"/jobs/{source_job_id}/capability-intelligence",
                str(exc),
            )
        return operation_redirect(
            operation.id,
            return_to=f"/jobs/{source_job_id}/capability-intelligence",
            auto_return=True,
        )
