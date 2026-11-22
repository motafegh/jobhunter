"""B5 opt-in local translation transport budget, independent of B3/v2 provider.

One session bounds every attempted HTTP dispatch, including automatic 5xx
retries and truncation recovery; the local OS monotonic alarm interrupts
a stalled response. Every translation remains candidate-only. Source/model
payloads are never logged by this guard.

Only use this on Linux/macOS in the process main thread with SIGALRM. If a
process-wide deadline cannot be enforced, refuse to enter the session.
"""

from __future__ import annotations

import signal
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

from jobhunter.translation.base import TranslationError

B5_PHYSICAL_BUDGET_CONTRACT = "jobhunter-p16-b5-local-translation-physical-budget-v1"
LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
MAX_SESSION_ATTEMPTS = 8
MAX_SESSION_WALL_SECONDS = 900.0


class B5AttemptBudgetExceeded(TranslationError):
    """The next model POST was rejected before transport dispatch."""


class B5WallBudgetExceeded(TranslationError):
    """The monotonic wall-clock deadline ended the bounded model session."""


@dataclass(frozen=True, slots=True)
class B5PhysicalBudget:
    max_http_attempts: int
    wall_seconds: float

    def __post_init__(self) -> None:
        if not 1 <= self.max_http_attempts <= MAX_SESSION_ATTEMPTS:
            raise ValueError("B5 translation pilot requires 1..8 physical HTTP attempts")
        if not 0 < self.wall_seconds <= MAX_SESSION_WALL_SECONDS:
            raise ValueError("B5 translation pilot wall limit must be 0..900 seconds")


@dataclass(frozen=True, slots=True)
class B5AttemptReceipt:
    ordinal: int
    status_code: int | None
    error_type: str | None
    duration_seconds: float


class B5PhysicalBudgetTransport(httpx.BaseTransport):
    """Count *attempted dispatches*, not logical source items or responses.

    No request/response content is retained. HTTP 5xx, connection retries and
    length recovery consume the same capped budget as successful completions.
    """

    def __init__(
        self,
        *,
        budget: B5PhysicalBudget,
        inner: httpx.BaseTransport | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.budget = budget
        self._inner = inner or httpx.HTTPTransport(trust_env=False, retries=0)
        self._clock = clock
        self._entered = False
        self._context_depth = 0
        self._finished = False
        self._deadline: float | None = None
        self._previous_handler: Any = None
        self.attempts: list[B5AttemptReceipt] = []
        self.rejected_before_dispatch = 0
        self.wall_deadline_hit = False

    @property
    def attempted_http_dispatches(self) -> int:
        return len(self.attempts)

    @property
    def completed_http_responses(self) -> int:
        return sum(x.status_code is not None for x in self.attempts)

    def _alarm(self, _signum: int, _frame: Any) -> None:
        self.wall_deadline_hit = True
        raise B5WallBudgetExceeded("B5 translation model session wall deadline reached")

    def __enter__(self) -> B5PhysicalBudgetTransport:
        # httpx.Client enters the provided transport for each physical call.
        # Keep the explicit outer session alive while nested clients enter/exit.
        if self._entered:
            self._context_depth += 1
            return self
        if self._finished:
            raise ValueError("B5 physical budget is single-use")
        if (
            not hasattr(signal, "SIGALRM")
            or not hasattr(signal, "setitimer")
            or threading.current_thread() is not threading.main_thread()
        ):
            raise RuntimeError("B5 hard wall deadline requires POSIX main-thread SIGALRM")
        if signal.getitimer(signal.ITIMER_REAL)[0] > 0:
            raise RuntimeError("Another live OS alarm exists; cannot enforce isolated B5 budget")
        self._previous_handler = signal.getsignal(signal.SIGALRM)
        self._deadline = self._clock() + self.budget.wall_seconds
        signal.signal(signal.SIGALRM, self._alarm)
        signal.setitimer(signal.ITIMER_REAL, self.budget.wall_seconds)
        self._entered = True
        self._context_depth = 1
        return self

    def __exit__(self, _type: Any, _value: Any, _tb: Any) -> None:
        if self._context_depth > 1:
            self._context_depth -= 1
            return
        if not self._entered:
            raise RuntimeError("B5 budget transport was not in an active session")
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self._previous_handler)
        self._entered = False
        self._context_depth = 0
        self._finished = True
        self._inner.close()

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if not self._entered or self._deadline is None:
            raise RuntimeError("B5 model requests require active hard-deadline session")
        if (
            request.method != "POST"
            or request.url.scheme != "http"
            or request.url.host not in LOCAL_HOSTS
            or request.url.port != 18080
            or request.url.path != "/v1/chat/completions"
            or bool(request.url.username)
            or bool(request.url.password)
        ):
            self.rejected_before_dispatch += 1
            raise TranslationError("B5 guard permits only local LM Studio translation POST")
        if self._clock() >= self._deadline:
            self.wall_deadline_hit = True
            self.rejected_before_dispatch += 1
            raise B5WallBudgetExceeded("B5 model deadline exhausted before HTTP dispatch")
        if self.attempted_http_dispatches >= self.budget.max_http_attempts:
            self.rejected_before_dispatch += 1
            raise B5AttemptBudgetExceeded("B5 physical model HTTP attempt ceiling reached")

        ordinal = self.attempted_http_dispatches + 1
        started = self._clock()
        status: int | None = None
        error: str | None = None
        try:
            response = self._inner.handle_request(request)
            # This read is guarded by the session-wide OS alarm.
            response.read()
            status = response.status_code
            return response
        except Exception as exc:
            error = type(exc).__name__
            raise
        finally:
            # Append exactly once even when the model call/response is interrupted.
            self.attempts.append(
                B5AttemptReceipt(
                    ordinal=ordinal,
                    status_code=status,
                    error_type=error,
                    duration_seconds=round(max(0.0, self._clock() - started), 3),
                )
            )

    def close(self) -> None:
        # httpx provider uses one short-lived client for each attempt;
        # session owns and closes the shared transport on __exit__.
        return None

    def safe_summary(self) -> dict[str, Any]:
        return {
            "contract": B5_PHYSICAL_BUDGET_CONTRACT,
            "max_http_attempts": self.budget.max_http_attempts,
            "wall_seconds": self.budget.wall_seconds,
            "attempted_http_dispatches": self.attempted_http_dispatches,
            "completed_http_responses": self.completed_http_responses,
            "rejected_before_dispatch": self.rejected_before_dispatch,
            "wall_deadline_hit": self.wall_deadline_hit,
            "attempts": [
                {
                    "ordinal": x.ordinal,
                    "status_code": x.status_code,
                    "error_type": x.error_type,
                    "duration_seconds": x.duration_seconds,
                }
                for x in self.attempts
            ],
            "no_payload_retained": True,
            "not_a_translation_quality_claim": True,
        }
