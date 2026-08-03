"""Single-user background operation queue for the local web interface."""

from __future__ import annotations

import threading
import uuid
from collections import deque
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

_TERMINAL_SUCCESS_STATUSES = {"completed", "completed_with_failures"}


@dataclass(frozen=True, slots=True)
class WebOperationResult:
    """Typed result for an operation that completed without raising an exception."""

    summary: str
    status: str = "completed"

    def __post_init__(self) -> None:
        if self.status not in _TERMINAL_SUCCESS_STATUSES:
            raise ValueError(
                "WebOperationResult status must be completed or completed_with_failures"
            )


@dataclass(slots=True)
class WebOperation:
    id: str
    name: str
    status: str
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    summary: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


class OperationBusyError(RuntimeError):
    """Raised when another mutable operation is already active."""


class WebOperationManager:
    """Run one mutable JobHunter operation at a time without blocking HTTP responses."""

    def __init__(self, *, history_limit: int = 50) -> None:
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="jobhunter-web")
        self._lock = threading.Lock()
        self._operations: dict[str, WebOperation] = {}
        self._history: deque[str] = deque(maxlen=history_limit)
        self._active_id: str | None = None

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    def start(
        self,
        name: str,
        action: Callable[[], str | WebOperationResult],
    ) -> WebOperation:
        with self._lock:
            if self._active_id is not None:
                active = self._operations[self._active_id]
                if active.status in {"queued", "running"}:
                    raise OperationBusyError(
                        f"{active.name} is already {active.status}. Wait for it to finish."
                    )
            operation = WebOperation(
                id=uuid.uuid4().hex[:12],
                name=name,
                status="queued",
                created_at=self._now(),
            )
            self._operations[operation.id] = operation
            self._history.appendleft(operation.id)
            self._active_id = operation.id
            self._executor.submit(self._run, operation.id, action)
            return operation

    def _run(
        self,
        operation_id: str,
        action: Callable[[], str | WebOperationResult],
    ) -> None:
        with self._lock:
            operation = self._operations[operation_id]
            operation.status = "running"
            operation.started_at = self._now()
        try:
            result = action()
            if isinstance(result, WebOperationResult):
                summary = result.summary
                terminal_status = result.status
            else:
                summary = result
                terminal_status = "completed"
        except Exception as exc:
            with self._lock:
                operation = self._operations[operation_id]
                operation.status = "failed"
                operation.error = f"{type(exc).__name__}: {exc}"
                operation.completed_at = self._now()
                if self._active_id == operation_id:
                    self._active_id = None
            return

        with self._lock:
            operation = self._operations[operation_id]
            operation.status = terminal_status
            operation.summary = summary
            operation.completed_at = self._now()
            if self._active_id == operation_id:
                self._active_id = None

    def get(self, operation_id: str) -> WebOperation | None:
        with self._lock:
            operation = self._operations.get(operation_id)
            if operation is None:
                return None
            return WebOperation(**operation.to_dict())

    def recent(self) -> tuple[WebOperation, ...]:
        with self._lock:
            return tuple(
                WebOperation(**self._operations[operation_id].to_dict())
                for operation_id in self._history
                if operation_id in self._operations
            )

    def active(self) -> WebOperation | None:
        with self._lock:
            if self._active_id is None:
                return None
            operation = self._operations.get(self._active_id)
            if operation is None:
                return None
            return WebOperation(**operation.to_dict())
