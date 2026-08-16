from __future__ import annotations

import time

from jobhunter.web.operations import WebOperationManager


def _wait_for_terminal(manager: WebOperationManager, operation_id: str):
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        operation = manager.get(operation_id)
        assert operation is not None
        if operation.status not in {"queued", "running"}:
            return operation
        time.sleep(0.01)
    raise AssertionError("web operation did not reach a terminal state")


def test_web_operation_runs_public_corpus_hook_after_success() -> None:
    calls: list[str] = []
    manager = WebOperationManager(after_success=lambda: calls.append("synced"))

    started = manager.start("test", lambda: "done")
    completed = _wait_for_terminal(manager, started.id)

    assert completed.status == "completed"
    assert completed.summary == "done"
    assert calls == ["synced"]


def test_web_operation_does_not_run_hook_when_action_raises() -> None:
    calls: list[str] = []
    manager = WebOperationManager(after_success=lambda: calls.append("synced"))

    def fail() -> str:
        raise RuntimeError("action failed")

    started = manager.start("test", fail)
    completed = _wait_for_terminal(manager, started.id)

    assert completed.status == "failed"
    assert completed.error == "RuntimeError: action failed"
    assert calls == []


def test_web_operation_surfaces_projection_failure_after_durable_success() -> None:
    def fail_projection() -> None:
        raise OSError("disk full")

    manager = WebOperationManager(after_success=fail_projection)
    started = manager.start("test", lambda: "durable work completed")
    completed = _wait_for_terminal(manager, started.id)

    assert completed.status == "failed"
    assert completed.error is not None
    assert "Public corpus synchronization failed after the durable web operation" in completed.error
    assert "disk full" in completed.error
