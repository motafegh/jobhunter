"""Browser review of pending P1.6 items without changing original candidate claims."""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_item_review import AnalysisItemReviewStore
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.web.common import TEMPLATES, redirect_with_notice, require_csrf, template_context


def register_item_review_routes(app: FastAPI, settings: Settings) -> None:
    """Use the same review store as the CLI, never a second acceptance path."""

    def current(source_job_id: str):
        model = settings.effective_analysis_lm_studio_model()
        artifact = AnalysisStore(settings.database_path).latest_current(
            source_job_id, model=model, prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        )
        if artifact is None:
            raise HTTPException(status_code=404, detail="No current English analysis candidate")
        return artifact

    @app.get("/jobs/{source_job_id}/item-review", response_class=HTMLResponse)
    def item_review_page(request: Request, source_job_id: str, notice: str = ""):
        artifact = current(source_job_id)
        store = AnalysisItemReviewStore(settings.database_path)
        events = store.events(artifact.id)
        latest = {}
        gaps = {}
        for event in events:
            if event.kind == "coverage_gap":
                gaps[event.item_digest] = event
            else:
                latest[(event.kind, event.item_index)] = event
        return TEMPLATES.TemplateResponse(
            request=request,
            name="item_review.html",
            context=template_context(
                request, page="jobs", source_job_id=source_job_id,
                artifact=artifact, latest=latest, gaps=tuple(gaps.values()),
                review_complete=store.is_complete(artifact.id), notice=notice,
            ),
        )

    @app.post("/jobs/{source_job_id}/item-review")
    def record_item_review(
        request: Request, source_job_id: str,
        csrf_token: Annotated[str, Form()],
        artifact_id: Annotated[int, Form()],
        intent: Annotated[str, Form()],
        note: Annotated[str, Form()] = "",
        kind: Annotated[str, Form()] = "",
        item_index: Annotated[int, Form()] = -1,
        finding: Annotated[str, Form()] = "",
        proposed_text: Annotated[str, Form()] = "",
        source_excerpt: Annotated[str, Form()] = "",
        minor: Annotated[bool, Form()] = False,
    ):
        require_csrf(request, csrf_token)
        artifact = current(source_job_id)
        if artifact.id != artifact_id:
            raise HTTPException(status_code=409, detail="Review identity is stale")
        if artifact.semantic_review_status != "pending":
            raise HTTPException(status_code=409, detail="Analysis is not pending review")
        store = AnalysisItemReviewStore(settings.database_path)
        target = f"/jobs/{source_job_id}/item-review"
        try:
            if intent == "begin":
                store.begin(artifact_id)
                result = "Complete-item review started"
            elif intent == "item":
                store.review_item(
                    artifact_id, kind=kind, index=item_index, finding=finding,
                    note=note, material=not minor,
                    proposed_text=proposed_text or None,
                )
                result = "Item finding recorded; original analysis unchanged"
            elif intent == "gap":
                store.review_gap(
                    artifact_id, source_excerpt=source_excerpt, finding=finding,
                    note=note, material=not minor,
                    proposed_text=proposed_text or None,
                )
                result = "Source-coverage finding recorded; no analysis item added"
            elif intent == "finish":
                store.complete(artifact_id, note=note)
                result = "Complete review recorded; separate whole-artifact acceptance required"
            else:
                raise ValueError("Unknown review action")
        except ValueError as exc:
            return redirect_with_notice(target, f"Review not completed: {exc}")
        return redirect_with_notice(target, result)
