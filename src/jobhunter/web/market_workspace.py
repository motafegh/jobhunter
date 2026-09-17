"""Thin browser routes for the shared I6 Market workspace."""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from jobhunter.config import Settings
from jobhunter.market_workspace import (
    MarketRunControls,
    MarketWorkspaceService,
    market_run_summary,
)
from jobhunter.web.operations import (
    OperationBusyError,
    WebOperationLink,
    WebOperationResult,
)

_WEB_DIR = Path(__file__).resolve().parent
_TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def _csrf(request: Request, submitted: str) -> None:
    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def _context(request: Request, **extra):
    context = {
        "request": request,
        "csrf_token": request.app.state.csrf_token,
        "active_operation": request.app.state.operations.active(),
    }
    context.update(extra)
    return context


def _redirect_operation(request: Request, name: str, action) -> RedirectResponse:
    try:
        operation = request.app.state.operations.start(name, action)
    except OperationBusyError as exc:
        query = urlencode({"notice": str(exc)})
        return RedirectResponse(url=f"/market/targets?{query}", status_code=303)
    query = urlencode({"return_to": "/market/targets", "auto_return": "1"})
    return RedirectResponse(url=f"/operations/{operation.id}?{query}", status_code=303)


def _split_values(value: str) -> tuple[str, ...]:
    normalized = value.replace("\n", ",")
    return tuple(
        dict.fromkeys(part.strip() for part in normalized.split(",") if part.strip())
    )


def _controls(
    *,
    request_budget: int,
    search_limit: int,
    default_max_pages: int,
    missing_limit: int,
    refresh_limit: int,
    refresh_after_hours: float,
    translation_limit: int,
    analysis_limit: int,
    membership_limit: int,
) -> MarketRunControls:
    return MarketRunControls(
        request_budget=request_budget,
        search_limit=search_limit,
        default_max_pages=default_max_pages,
        missing_limit=missing_limit,
        refresh_limit=refresh_limit,
        refresh_after_hours=refresh_after_hours,
        translation_limit=translation_limit,
        analysis_limit=analysis_limit,
        membership_limit=membership_limit,
    ).validate()


def register_market_workspace_routes(app: FastAPI, settings: Settings) -> None:
    """Register target-scoped Market workflow routes on the local app."""

    @app.get("/market/targets", response_class=HTMLResponse)
    def market_targets(
        request: Request,
        target_id: int | None = None,
        definition_id: int | None = None,
        snapshot_id: int | None = None,
        notice: str = "",
    ):
        workspace = MarketWorkspaceService(settings)
        try:
            state = workspace.state(
                target_id=target_id,
                definition_id=definition_id,
                snapshot_id=snapshot_id,
            )
            preview = (
                workspace.preview(
                    state.selected_definition.id,
                    controls=MarketRunControls(
                        request_budget=settings.jobinja_search_request_budget,
                        search_limit=settings.jobinja_max_expanded_searches,
                        default_max_pages=settings.jobinja_default_keyword_max_pages,
                        missing_limit=settings.jobinja_sync_missing_limit,
                        refresh_limit=settings.jobinja_sync_refresh_limit,
                        refresh_after_hours=settings.jobinja_refresh_after_hours,
                        translation_limit=settings.translation_batch_limit,
                        analysis_limit=settings.analysis_batch_limit,
                        membership_limit=20,
                    ),
                )
                if state.selected_definition is not None
                else None
            )
        except (LookupError, RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="market_workspace.html",
            context=_context(
                request,
                page="market",
                state=state,
                preview=preview,
                catalog=settings.search_catalog(),
                notice=notice,
                settings=settings,
            ),
        )

    @app.get("/market/runs/{run_id}", response_class=HTMLResponse)
    def market_run_detail(request: Request, run_id: int):
        workspace = MarketWorkspaceService(settings)
        try:
            run = workspace.run_by_id(run_id)
            state = workspace.state(definition_id=run.target_definition_version_id)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        snapshot = next((item for item in state.snapshots if item.run_id == run.id), None)
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="market_run.html",
            context=_context(
                request,
                page="market",
                run=run,
                snapshot=snapshot,
            ),
        )

    @app.get("/market/snapshots/{snapshot_id}", response_class=HTMLResponse)
    def market_snapshot_detail(request: Request, snapshot_id: int):
        workspace = MarketWorkspaceService(settings)
        try:
            snapshot, members, profile = workspace.snapshot_by_id(snapshot_id)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return _TEMPLATES.TemplateResponse(
            request=request,
            name="market_snapshot.html",
            context=_context(
                request,
                page="market",
                snapshot=snapshot,
                members=members,
                profile=profile,
            ),
        )

    @app.post("/market/actions/target")
    def create_market_target(
        request: Request,
        csrf_token: Annotated[str, Form()],
        slug: Annotated[str, Form()],
        name: Annotated[str, Form()],
        description: Annotated[str, Form()] = "",
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            target = MarketWorkspaceService(settings).create_target(
                slug=slug,
                name=name,
                description=description or None,
            )
            return WebOperationResult(
                summary=f"Created Market target {target.id}: {target.name}",
                links=(
                    WebOperationLink(
                        label="Open target",
                        url=f"/market/targets?target_id={target.id}",
                    ),
                ),
            )

        return _redirect_operation(request, "Create Market target", action)

    @app.post("/market/actions/definition")
    def create_market_definition(
        request: Request,
        csrf_token: Annotated[str, Form()],
        target_id: Annotated[int, Form()],
        membership_intent: Annotated[str, Form()],
        profiles: Annotated[str, Form()] = "",
        packs: Annotated[str, Form()] = "",
        terms: Annotated[str, Form()] = "",
        include_hints: Annotated[str, Form()] = "",
        exclude_hints: Annotated[str, Form()] = "",
        geography_scope: Annotated[str, Form()] = "",
        work_arrangement_scope: Annotated[str, Form()] = "",
        seniority_scope: Annotated[str, Form()] = "",
        employment_type_scope: Annotated[str, Form()] = "",
    ):
        _csrf(request, csrf_token)

        def action() -> WebOperationResult:
            definition = MarketWorkspaceService(settings).create_definition(
                target_id,
                membership_intent=membership_intent,
                search_profiles=_split_values(profiles),
                search_packs=_split_values(packs),
                extra_search_terms=_split_values(terms),
                include_hints=_split_values(include_hints),
                exclude_hints=_split_values(exclude_hints),
                geography_scope=geography_scope,
                work_arrangement_scope=work_arrangement_scope,
                seniority_scope=seniority_scope,
                employment_type_scope=employment_type_scope,
            )
            return WebOperationResult(
                summary=(
                    f"Market target {target_id}: definition version "
                    f"{definition.version_number} ({definition.id})"
                ),
                links=(
                    WebOperationLink(
                        label="Open definition",
                        url=f"/market/targets?definition_id={definition.id}",
                    ),
                ),
            )

        return _redirect_operation(request, "Create Market definition", action)

    @app.post("/market/actions/run")
    def run_market_target(
        request: Request,
        csrf_token: Annotated[str, Form()],
        definition_id: Annotated[int, Form()],
        request_budget: Annotated[int, Form()],
        search_limit: Annotated[int, Form()],
        default_max_pages: Annotated[int, Form()],
        missing_limit: Annotated[int, Form()],
        refresh_limit: Annotated[int, Form()],
        refresh_after_hours: Annotated[float, Form()],
        translation_limit: Annotated[int, Form()],
        analysis_limit: Annotated[int, Form()],
        membership_limit: Annotated[int, Form()],
    ):
        _csrf(request, csrf_token)
        controls = _controls(
            request_budget=request_budget,
            search_limit=search_limit,
            default_max_pages=default_max_pages,
            missing_limit=missing_limit,
            refresh_limit=refresh_limit,
            refresh_after_hours=refresh_after_hours,
            translation_limit=translation_limit,
            analysis_limit=analysis_limit,
            membership_limit=membership_limit,
        )

        def action() -> WebOperationResult:
            result = MarketWorkspaceService(settings).run(
                definition_id,
                controls=controls,
            )
            links = [
                WebOperationLink(
                    label="Open Market run",
                    url=f"/market/runs/{result.run.id}",
                )
            ]
            if result.snapshot is not None:
                links.append(
                    WebOperationLink(
                        label="Open frozen snapshot",
                        url=f"/market/snapshots/{result.snapshot.id}",
                    )
                )
            return WebOperationResult(
                summary=market_run_summary(result),
                status="completed_with_failures" if result.has_failures else "completed",
                links=tuple(links),
            )

        return _redirect_operation(request, "Run target-scoped Market update", action)
