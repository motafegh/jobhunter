"""Browser surface for the human-facing Role Capability Blueprint."""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.role_blueprint_service import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
    RoleBlueprintError,
    build_role_blueprint_service,
    format_role_blueprint,
)
from jobhunter.role_blueprint_store import RoleBlueprintStore
from jobhunter.storage import JobHunterStore
from jobhunter.web.operations import OperationBusyError, WebOperationResult

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _csrf(request: Request, submitted: str) -> None:
    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _operation_redirect(operation_id: str, source_job_id: str) -> RedirectResponse:
    return_to = f"/jobs/{source_job_id}/role-blueprint"
    query = urlencode({"return_to": return_to, "auto_return": "1"})
    return RedirectResponse(url=f"/operations/{operation_id}?{query}", status_code=303)


def register_blueprint_routes(app: FastAPI, settings: Settings) -> None:
    @app.get(
        "/jobs/{source_job_id}/role-blueprint",
        response_class=HTMLResponse,
        name="role_blueprint_page",
    )
    def blueprint_page(request: Request, source_job_id: str):
        source_store = JobHunterStore(settings.database_path)
        source_store.initialize()
        posting = source_store.get_job(source_job_id)
        if posting is None:
            raise HTTPException(status_code=404, detail="Job not found in the local catalog")
        detail = source_store.get_latest_job_detail(source_job_id)
        model = settings.effective_analysis_lm_studio_model()
        capability_artifact = CapabilityIntelligenceStore(
            settings.database_path
        ).latest_current(
            source_job_id,
            model=model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        blueprint_artifact = RoleBlueprintStore(settings.database_path).latest_current(
            source_job_id,
            model=model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        blueprint_current = (
            blueprint_artifact is not None
            and capability_artifact is not None
            and blueprint_artifact.capability_artifact_id == capability_artifact.id
            and blueprint_artifact.analysis_artifact_id == capability_artifact.analysis_artifact_id
            and blueprint_artifact.translation_artifact_id
            == capability_artifact.translation_artifact_id
        )
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="role_blueprint.html",
            context={
                "request": request,
                "page": "jobs",
                "csrf_token": request.app.state.csrf_token,
                "active_operation": request.app.state.operations.active(),
                "source_job_id": source_job_id,
                "posting": posting,
                "detail": detail,
                "capability_artifact": capability_artifact,
                "blueprint_artifact": blueprint_artifact,
                "blueprint_current": blueprint_current,
                "analysis_model": model,
            },
        )

    @app.post("/jobs/{source_job_id}/role-blueprint")
    def build_blueprint(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            try:
                service = build_role_blueprint_service(settings)
                result = service.build(source_job_id)
            except RoleBlueprintError as exc:
                raise RuntimeError(f"Role Capability Blueprint is not ready: {exc}") from exc

            artifact = RoleBlueprintStore(settings.database_path).latest_current(
                source_job_id,
                model=result.model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
            )
            if artifact is None:
                raise RuntimeError(
                    "Role Capability Blueprint is unavailable after successful build"
                )
            summary = (
                f"Role Capability Blueprint: {source_job_id}\n"
                f"Outcome: {result.outcome}\n"
                f"Capability areas: {result.capability_areas}\n\n"
                f"{format_role_blueprint(artifact)}"
            )
            return WebOperationResult(summary=summary, status="completed")

        try:
            operation = request.app.state.operations.start(
                f"Role Capability Blueprint: {source_job_id}",
                action,
            )
        except OperationBusyError as exc:
            return RedirectResponse(
                url=f"/jobs/{source_job_id}/role-blueprint?notice={exc}",
                status_code=303,
            )
        return _operation_redirect(operation.id, source_job_id)
