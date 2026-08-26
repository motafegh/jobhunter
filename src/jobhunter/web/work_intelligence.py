"""Browser-first P2.2A Job Work Intelligence surface.

Work Intelligence persistence is intentionally outside ``WebOperationManager`` in P2.2A because a
successful operation-manager mutation refreshes the public corpus and publication of this candidate
analytical layer has not been authorized.
"""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from jobhunter.config import Settings
from jobhunter.storage import JobHunterStore
from jobhunter.work_intelligence_models import JobWorkIntelligence
from jobhunter.work_intelligence_service import (
    WorkIntelligenceError,
    build_work_intelligence_service,
)

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _csrf(request: Request, submitted: str) -> None:
    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _redirect(source_job_id: str, *, notice: str) -> RedirectResponse:
    query = urlencode({"notice": notice})
    return RedirectResponse(
        url=f"/jobs/{source_job_id}/work-intelligence?{query}",
        status_code=303,
    )


def register_work_intelligence_routes(app: FastAPI, settings: Settings) -> None:
    """Attach browser-first candidate Work Intelligence routes."""

    @app.get(
        "/jobs/{source_job_id}/work-intelligence",
        response_class=HTMLResponse,
        name="work_intelligence_page",
    )
    def work_intelligence_page(
        request: Request,
        source_job_id: str,
        notice: str = "",
    ):
        source_store = JobHunterStore(settings.database_path)
        source_store.initialize()
        posting = source_store.get_job(source_job_id)
        if posting is None:
            raise HTTPException(status_code=404, detail="Job not found in the local catalog")
        detail = source_store.get_latest_job_detail(source_job_id)

        readiness_error = ""
        artifact = None
        document = None
        try:
            service = build_work_intelligence_service(settings)
            artifact = service.current_artifact(source_job_id)
            if artifact is not None:
                document = JobWorkIntelligence.model_validate(artifact.intelligence)
        except (ValueError, WorkIntelligenceError) as exc:
            readiness_error = str(exc)

        return _TEMPLATES.TemplateResponse(
            request=request,
            name="work_intelligence.html",
            context={
                "request": request,
                "page": "jobs",
                "csrf_token": request.app.state.csrf_token,
                "active_operation": request.app.state.operations.active(),
                "source_job_id": source_job_id,
                "posting": posting,
                "detail": detail,
                "artifact": artifact,
                "document": document,
                "notice": notice,
                "readiness_error": readiness_error,
            },
        )

    @app.post("/jobs/{source_job_id}/work-intelligence")
    def generate_work_intelligence(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        _csrf(request, csrf_token)
        try:
            result = build_work_intelligence_service(settings).analyze_job(source_job_id)
        except (ValueError, WorkIntelligenceError) as exc:
            return _redirect(source_job_id, notice=f"Work Intelligence not ready: {exc}")
        return _redirect(
            source_job_id,
            notice=(
                f"Work Intelligence {result.outcome}: artifact {result.artifact_id}, "
                f"themes {result.work_theme_count}. Candidate interpretation only."
            ),
        )
