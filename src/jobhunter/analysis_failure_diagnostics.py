"""Private, non-authoritative diagnostics for unsuccessful P1.6 generation.

This store is deliberately separate from job_analysis_artifacts. A captured
completion is diagnostic text, never a valid requirement or a pending analysis.
No exception string, model request, authorization header, or SDK create_kwargs
is persisted by this module.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError

_MAX_CAPTURE_BYTES = 128 * 1024
_MAX_RETRY_CAPTURES = 4


@dataclass(frozen=True, slots=True)
class FailureDescription:
    code: str
    message: str


def describe_failure(error: Exception) -> FailureDescription:
    """Produce only application-authored strings safe for an ordinary attempt row."""
    if isinstance(error, InferenceConnectionError):
        return FailureDescription(
            "inference_connection_failed", "Local inference connection failed"
        )
    if isinstance(error, InferenceResponseError):
        return FailureDescription(
            "inference_response_failed",
            "Structured inference failed; inspect private diagnostics",
        )
    if isinstance(error, sqlite3.IntegrityError):
        return FailureDescription(
            "storage_integrity_failed", "Analysis storage integrity check failed"
        )
    if isinstance(error, sqlite3.DatabaseError):
        return FailureDescription("storage_failed", "Analysis storage failed")
    if isinstance(error, (ValueError, TypeError)):
        return FailureDescription("analysis_validation_failed", "Analysis validation failed")
    return FailureDescription("analysis_processing_failed", "Analysis processing failed")


class SafeFailure(Exception):
    """Exception proxy for existing attempt storage; never formats its cause."""

    def __init__(self, description: FailureDescription) -> None:
        self.code = description.code
        super().__init__(f"{description.code}: {description.message}")


def _completion_text(completion: Any) -> str | None:
    """Read explicit message content only; never stringify arbitrary SDK objects."""
    if isinstance(completion, str):
        return completion or None
    choices = (
        completion.get("choices")
        if isinstance(completion, dict)
        else getattr(completion, "choices", None)
    )
    if not isinstance(choices, (list, tuple)) or not choices:
        return None
    first = choices[0]
    message = first.get("message") if isinstance(first, dict) else getattr(first, "message", None)
    content = (
        message.get("content")
        if isinstance(message, dict)
        else getattr(message, "content", None)
    )
    return content if isinstance(content, str) and content else None


def _exception_chain(error: Exception) -> list[BaseException]:
    chain: list[BaseException] = []
    current: BaseException | None = error
    while current is not None and len(chain) < 5 and current not in chain:
        chain.append(current)
        current = current.__cause__
    return chain


def _available_completions(error: Exception) -> list[tuple[int | None, str]]:
    """Best-effort Instructor 1.x capture, without relying on exception __str__."""
    result: list[tuple[int | None, str]] = []
    for cause in _exception_chain(error):
        attempts = getattr(cause, "failed_attempts", None)
        if isinstance(attempts, (list, tuple)):
            for attempt in attempts[:_MAX_RETRY_CAPTURES]:
                try:
                    text = _completion_text(getattr(attempt, "completion", None))
                    number = getattr(attempt, "attempt_number", None)
                except (AttributeError, TypeError, ValueError):
                    continue
                if text:
                    retry = number if type(number) is int and number > 0 else None
                    result.append((retry, text))
            if result:
                return result
        for attribute in ("last_completion", "raw_response"):
            try:
                text = _completion_text(getattr(cause, attribute, None))
            except (AttributeError, TypeError, ValueError):
                continue
            if text:
                return [(None, text)]
    return result


@dataclass(frozen=True, slots=True)
class FailureDiagnostic:
    id: int
    attempt_id: int
    failure_code: str
    failure_stage: str
    retry_number: int | None
    response_state: str
    completion_text: str | None


class AnalysisFailureDiagnosticStore:
    """Append-only local capture linked to the existing analysis-attempt ledger."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def initialize(self) -> None:
        # The caller has already created the attempt through AnalysisStore.
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_analysis_failure_diagnostics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id INTEGER NOT NULL,
                    failure_code TEXT NOT NULL,
                    failure_stage TEXT NOT NULL,
                    retry_number INTEGER,
                    response_state TEXT NOT NULL CHECK(response_state IN
                        ('available', 'unavailable', 'oversize')),
                    completion_text TEXT,
                    FOREIGN KEY(attempt_id) REFERENCES job_analysis_attempts(id),
                    CHECK((response_state = 'available' AND completion_text IS NOT NULL)
                       OR (response_state != 'available' AND completion_text IS NULL))
                );
                CREATE INDEX IF NOT EXISTS idx_analysis_failure_diagnostic_attempt
                ON job_analysis_failure_diagnostics(attempt_id, id);
                """
            )

    def record_failure(
        self,
        *,
        attempt_id: int,
        error: Exception,
        failure_stage: str = "unclassified",
    ) -> tuple[int, ...]:
        """Retain available response text; never turn failed output into an artifact."""
        if attempt_id < 1:
            raise ValueError("attempt_id must reference a persisted failed attempt")
        if failure_stage not in {"unclassified", "provider", "partition", "whole_analysis"}:
            raise ValueError("Unknown diagnostic failure stage")
        self.initialize()
        description = describe_failure(error)
        available = _available_completions(error)
        records: list[tuple[int | None, str, str | None]] = []
        if not available:
            records.append((None, "unavailable", None))
        for number, text in available:
            if len(text.encode("utf-8")) > _MAX_CAPTURE_BYTES:
                records.append((number, "oversize", None))
            else:
                records.append((number, "available", text))
        ids: list[int] = []
        with self._connect() as connection:
            for number, state, text in records:
                cursor = connection.execute(
                    """
                    INSERT INTO job_analysis_failure_diagnostics(
                        attempt_id, failure_code, failure_stage,
                        retry_number, response_state, completion_text
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (attempt_id, description.code, failure_stage, number, state, text),
                )
                ids.append(int(cursor.lastrowid))
        return tuple(ids)

    def list_for_attempt(self, attempt_id: int) -> tuple[FailureDiagnostic, ...]:
        """Private inspection API; callers must not expose response text in public exports."""
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM job_analysis_failure_diagnostics
                WHERE attempt_id = ? ORDER BY id
                """,
                (attempt_id,),
            ).fetchall()
        return tuple(
            FailureDiagnostic(
                id=int(row["id"]),
                attempt_id=int(row["attempt_id"]),
                failure_code=str(row["failure_code"]),
                failure_stage=str(row["failure_stage"]),
                retry_number=(
                    int(row["retry_number"]) if row["retry_number"] is not None else None
                ),
                response_state=str(row["response_state"]),
                completion_text=(
                    str(row["completion_text"])
                    if row["completion_text"] is not None
                    else None
                ),
            )
            for row in rows
        )
