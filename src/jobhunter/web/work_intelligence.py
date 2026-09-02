"""Browser-first P2.2A Job Work Intelligence surface.

Work Intelligence persistence is intentionally outside ``WebOperationManager`` in P2.2A because a
successful operation-manager mutation refreshes the public corpus and publication of this candidate
analytical layer has not been authorized.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from jobhunter.config import Settings
from jobhunter.storage import JobHunterStore
from jobhunter.web.common import TEMPLATES, redirect_with_notice, require_csrf, template_context
from jobhunter.work_intelligence_models import JobWorkIntelligence
from jobhunter.work_intelligence_service import (
    WorkIntelligenceError,
    build_work_intelligence_service,
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

        return TEMPLATES.TemplateResponse(
            request=request,
            name="work_intelligence.html",
            context=template_context(
                request,
                page="jobs",
                source_job_id=source_job_id,
                posting=posting,
                detail=detail,
                artifact=artifact,
                document=document,
                notice=notice,
                readiness_error=readiness_error,
            ),
        )

    @app.post("/jobs/{source_job_id}/work-intelligence")
    def generate_work_intelligence(
        request: Request,
        source_job_id: str,
        csrf_token: Annotated[str, Form()],
    ):
        require_csrf(request, csrf_token)
        target = f"/jobs/{source_job_id}/work-intelligence"
        try:
            result = build_work_intelligence_service(settings).analyze_job(source_job_id)
        except (ValueError, WorkIntelligenceError) as exc:
            return redirect_with_notice(target, f"Work Intelligence not ready: {exc}")
        return redirect_with_notice(
            target,
            (
                f"Work Intelligence {result.outcome}: artifact {result.artifact_id}, "
                f"themes {result.work_theme_count}. Candidate interpretation only."
            ),
        )
