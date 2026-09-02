from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from jobhunter.web.common import (
    operation_redirect,
    redirect_with_notice,
    require_csrf,
    template_context,
)


class _Operations:
    def active(self):
        return "active-operation"


def _request():
    state = SimpleNamespace(csrf_token="local-token", operations=_Operations())
    return SimpleNamespace(app=SimpleNamespace(state=state))


def test_shared_template_context_preserves_common_web_state() -> None:
    request = _request()

    context = template_context(request, page="jobs", source_job_id="tG9K")

    assert context["request"] is request
    assert context["page"] == "jobs"
    assert context["csrf_token"] == "local-token"
    assert context["active_operation"] == "active-operation"
    assert context["source_job_id"] == "tG9K"


def test_shared_csrf_guard_accepts_only_the_app_local_token() -> None:
    request = _request()

    require_csrf(request, "local-token")

    with pytest.raises(HTTPException) as captured:
        require_csrf(request, "wrong-token")

    assert captured.value.status_code == 403


def test_notice_redirect_encodes_message_and_preserves_existing_query() -> None:
    response = redirect_with_notice("/registry/claims?state=all", "Mapped A & B")

    assert response.status_code == 303
    assert response.headers["location"] == (
        "/registry/claims?state=all&notice=Mapped+A+%26+B"
    )


def test_operation_redirect_keeps_return_navigation_local() -> None:
    response = operation_redirect(
        "abc123",
        return_to="/jobs/tG9K/capability-intelligence",
        auto_return=True,
    )

    assert response.status_code == 303
    assert response.headers["location"] == (
        "/operations/abc123?return_to=%2Fjobs%2FtG9K%2Fcapability-intelligence&auto_return=1"
    )

    with pytest.raises(ValueError, match="local absolute path"):
        operation_redirect("abc123", return_to="https://example.com")

    with pytest.raises(ValueError, match="local absolute path"):
        redirect_with_notice("//example.com", "unsafe")
