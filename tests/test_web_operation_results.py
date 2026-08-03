import time

import pytest

from jobhunter.web.operations import WebOperationManager, WebOperationResult


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
        ),
    )

    finished = _wait(manager, operation.id)

    assert finished is not None
    assert finished.status == "completed_with_failures"
    assert finished.summary == "8 completed, 2 failed"
    assert finished.error is None
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
