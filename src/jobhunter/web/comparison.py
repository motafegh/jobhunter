"""Read-only browser comparison over the same current SQLite evidence owners."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from jobhunter.config import Settings
from jobhunter.job_comparison import build_job_comparison, claim_anchor
from jobhunter.web.common import TEMPLATES, template_context
from jobhunter.web.intelligence_navigation import request_origin


def register_comparison_routes(app: FastAPI, settings: Settings) -> None:
    @app.get("/compare", response_class=HTMLResponse, name="job_comparison")
    def compare_jobs(request: Request):
        job_ids = tuple(request.query_params.getlist("job"))
        query = request.query_params.get("q", "")
        origin_job = request.query_params.get("origin_job", "")
        has_origin = any(key in request.query_params for key in ("from_snapshot", "from_report"))
        if has_origin and not origin_job:
            raise HTTPException(400, "Market context requires the originating job")
        origin = request_origin(settings, origin_job, request) if origin_job else None
        try:
            comparison = build_job_comparison(settings, job_ids, query)
        except LookupError as exc:
            raise HTTPException(404, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        return TEMPLATES.TemplateResponse(
            request=request,
            name="job_comparison.html",
            context=template_context(
                request, page="compare", comparison=comparison, claim_anchor=claim_anchor,
                selected_ids=[job.option.source_job_id for job in comparison.jobs],
                origin=origin, origin_job=origin_job,
            ),
        )
