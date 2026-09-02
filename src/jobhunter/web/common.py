"""Shared browser-layer security, template, and redirect primitives.

The local web application has several independently registered route modules.  Keep the small
cross-cutting rules that must behave identically across those modules here rather than duplicating
security or navigation logic in each feature surface.
"""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

_WEB_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(_WEB_DIR / "templates"))


def require_csrf(request: Request, submitted: str) -> None:
    """Reject a mutating local form whose token does not match the app-local token."""

    if not secrets.compare_digest(submitted, request.app.state.csrf_token):
        raise HTTPException(status_code=403, detail="Invalid local form token")


def template_context(
    request: Request,
    *,
    page: str,
    **extra: Any,
) -> dict[str, Any]:
    """Build the common context every server-rendered JobHunter page requires."""

    context: dict[str, Any] = {
        "request": request,
        "page": page,
        "csrf_token": request.app.state.csrf_token,
        "active_operation": request.app.state.operations.active(),
    }
    context.update(extra)
    return context


def _local_path(value: str) -> str:
    path = value.strip()
    if path.startswith("/") and not path.startswith("//"):
        return path
    raise ValueError("Web redirects must use a local absolute path")


def redirect_with_notice(path: str, notice: str) -> RedirectResponse:
    """Redirect to a local page with one URL-encoded human-readable notice."""

    target = _local_path(path)
    separator = "&" if "?" in target else "?"
    return RedirectResponse(
        url=f"{target}{separator}{urlencode({'notice': notice})}",
        status_code=303,
    )


def operation_redirect(
    operation_id: str,
    *,
    return_to: str,
    auto_return: bool = False,
) -> RedirectResponse:
    """Redirect to an operation page while preserving a validated local return target."""

    params = {"return_to": _local_path(return_to)}
    if auto_return:
        params["auto_return"] = "1"
    return RedirectResponse(
        url=f"/operations/{operation_id}?{urlencode(params)}",
        status_code=303,
    )
