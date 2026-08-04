"""Bounded browser review surface for per-job capability intelligence."""

from __future__ import annotations

import secrets
from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing_extensions import Annotated

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
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
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.operations import OperationBusyError, WebOperationResult

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _translation_service(settings: Settings) -> TranslationService:
    """Read current effective translation through the main capability service when needed."""

    # Capability service owns provider-aware dependency validation. The page itself only needs
    # latest persisted English fields for display, so this helper is intentionally not used for
    # readiness decisions.
    return TranslationService(store=TranslationStore(settings.database_path), provider=None)


def _csrf(request: Request, submitted: str) -> None:
    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _operation_redirect(operation_id: str, source_job_id: str) -> RedirectResponse:
    return_to = f"/jobs/{source_job_id}/capability-intelligence"
    query = urlencode({"return_to": return_to, "auto_return": "1"})
    return RedirectResponse(url=f"/operations/{operation_id}?{query}", status_code=303)


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
        model = settings.effective_analysis_lm_studio_model()
        english_analysis = AnalysisStore(settings.database_path).latest_current(
            source_job_id,
            model=model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        capability_artifact = CapabilityIntelligenceStore(
            settings.database_path
        ).latest_current(
            source_job_id,
            model=model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        latest_translation = TranslationStore(settings.database_path).latest_artifact(
            source_job_id,
            target_language="en",
        )
        current_dependency = (
            capability_artifact is not None
            and english_analysis is not None
            and capability_artifact.analysis_artifact_id == english_analysis.id
            and latest_translation is not None
            and capability_artifact.translation_artifact_id == latest_translation.id
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="capability_intelligence.html",
            context={
                "request": request,
                "csrf_token": request.app.state.csrf_token,
                "active_operation": request.app.state.operations.active(),
                "source_job_id": source_job_id,
                "posting": posting,
                "detail": detail,
                "english_analysis": english_analysis,
                "capability_artifact": capability_artifact,
                "capability_current": current_dependency,
                "analysis_model": model,
            },
        )

    @app.post("/jobs/{source_job_id}/capability-intelligence")
    def build_capability(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            try:
                service = build_capability_intelligence_service(settings)
                result = service.analyze_job(source_job_id)
                artifact = CapabilityIntelligenceStore(settings.database_path).latest_current(
                    source_job_id,
                    model=result.model,
                    prompt_version=CAPABILITY_PROMPT_VERSION,
                    schema_version=CAPABILITY_SCHEMA_VERSION,
                )
                if artifact is None:
                    raise RuntimeError(
                        "Capability artifact is unavailable after successful analysis"
                    )
                summary = (
                    f"Capability intelligence: {source_job_id}\n"
                    f"Outcome: {result.outcome}\n"
                    f"Capabilities: {result.capabilities}\n\n"
                    f"{format_capability_intelligence(artifact)}"
                )
                return WebOperationResult(summary=summary, status="completed")
            except CapabilityIntelligenceError as exc:
                return WebOperationResult(
                    summary=f"Capability intelligence is not ready: {exc}",
                    status="failed",
                )
            except Exception as exc:
                return WebOperationResult(
                    summary=f"Capability intelligence failed: {exc}",
                    status="failed",
                )

        try:
            operation = request.app.state.operations.start(
                f"Capability intelligence: {source_job_id}",
                action,
            )
        except OperationBusyError as exc:
            return RedirectResponse(
                url=f"/jobs/{source_job_id}/capability-intelligence?notice={exc}",
                status_code=303,
            )
        return _operation_redirect(operation.id, source_job_id)
