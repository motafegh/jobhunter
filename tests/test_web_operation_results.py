import time

import pytest

from jobhunter.web.operations import (
    WebOperationLink,
    WebOperationManager,
    WebOperationResult,
)


def _wait(manager: WebOperationManager, operation_id: str):
    operation = None
    for _ in range(100):
        operation = manager.get(operation_id)
        if operation is not None and operation.status in {
            "completed",
            "completed_with_failures",
            "failed",
        }:
            return operation
        time.sleep(0.01)
    return operation


def test_operation_manager_preserves_explicit_partial_success() -> None:
    manager = WebOperationManager()
    operation = manager.start(
        "Partial workflow",
        lambda: WebOperationResult(
            summary="8 completed, 2 failed",
            status="completed_with_failures",
            links=(WebOperationLink(label="Open report", url="/report"),),
        ),
    )

    finished = _wait(manager, operation.id)

    assert finished is not None
    assert finished.status == "completed_with_failures"
    assert finished.summary == "8 completed, 2 failed"
    assert finished.error is None
    assert finished.links == (WebOperationLink(label="Open report", url="/report"),)
    assert finished.to_dict()["links"] == (
        {"label": "Open report", "url": "/report"},
    )
    assert manager.active() is None


def test_plain_string_operation_remains_completed() -> None:
    manager = WebOperationManager()
    operation = manager.start("Simple workflow", lambda: "done")

    finished = _wait(manager, operation.id)

    assert finished is not None
    assert finished.status == "completed"
    assert finished.summary == "done"


def test_invalid_non_exception_terminal_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="completed or completed_with_failures"):
        WebOperationResult(summary="bad", status="failed")


@pytest.mark.parametrize("url", ("https://example.com", "//example.com", "jobs/one"))
def test_operation_links_reject_non_local_targets(url: str) -> None:
    with pytest.raises(ValueError, match="local absolute path"):
        WebOperationLink(label="Unsafe", url=url)
