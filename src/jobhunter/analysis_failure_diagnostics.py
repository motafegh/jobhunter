"""Private, non-authoritative diagnostics for unsuccessful P1.6 generation.

Completions and model-valid partition fragments are never P1.6 artifacts.
Do not persist arbitrary SDK exception strings, requests, headers or kwargs.
Expired private payloads are removed during diagnostic store operations.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError

_MAX_CAPTURE_BYTES = 128 * 1024
_MAX_RETRY_CAPTURES = 4
_MAX_PARTITION_CAPTURES = 8
_MAX_DIAGNOSTIC_ROWS = 500
_RETENTION_DAYS = 14
_ALLOWED_STAGES = {
    "unclassified",
    "provider",
    "partition",
    "whole_analysis",
    "partition_inference",
    "before_partition",
    "after_partition",
    "preceding_partition",
}


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
    """Best-effort Instructor 1.x capture without relying on exception __str__."""
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
    partition_index: int | None = None
    partition_total: int | None = None
    payload_kind: str = "failed_completion"
    created_at: str | None = None


class AnalysisFailureDiagnosticStore:
    """Local attempt-linked capture, bounded by record count, payload size and age."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA secure_delete=ON")
        return connection

    def initialize(self) -> None:
        # The caller already created the attempt through AnalysisStore. The
        # private diagnostic schema is not part of accepted/current selectors.
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
            columns = {
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA table_info(job_analysis_failure_diagnostics)"
                )
            }
            for name, definition in (
                ("partition_index", "INTEGER"),
                ("partition_total", "INTEGER"),
                ("payload_kind", "TEXT NOT NULL DEFAULT 'failed_completion'"),
                ("created_at", "TEXT"),
            ):
                if name not in columns:
                    connection.execute(
                        "ALTER TABLE job_analysis_failure_diagnostics "
                        f"ADD COLUMN {name} {definition}"
                    )
            # Older A1 records have no time identity. Start their finite
            # retention period at migration rather than claiming an invented age.
            connection.execute(
                "UPDATE job_analysis_failure_diagnostics SET created_at = ? "
                "WHERE created_at IS NULL",
                (datetime.now(UTC).isoformat(),),
            )
            self._prune(connection)

    @staticmethod
    def _prune(connection: sqlite3.Connection) -> None:
        cutoff = (datetime.now(UTC) - timedelta(days=_RETENTION_DAYS)).isoformat()
        connection.execute(
            "DELETE FROM job_analysis_failure_diagnostics WHERE created_at < ?",
            (cutoff,),
        )
        connection.execute(
            """DELETE FROM job_analysis_failure_diagnostics
               WHERE id NOT IN (
                   SELECT id FROM job_analysis_failure_diagnostics
                   ORDER BY id DESC LIMIT ?
               )""",
            (_MAX_DIAGNOSTIC_ROWS,),
        )

    def record_failure(
        self,
        *,
        attempt_id: int,
        error: Exception,
        failure_stage: str = "unclassified",
    ) -> tuple[int, ...]:
        """Retain only observed data; a failed attempt never creates a P1.6 artifact."""
        if attempt_id < 1:
            raise ValueError("attempt_id must reference a persisted failed attempt")
        if failure_stage == "unclassified":
            failure_stage = getattr(error, "_r05_failure_stage", failure_stage)
        if failure_stage not in _ALLOWED_STAGES:
            raise ValueError("Unknown diagnostic failure stage")
        self.initialize()
        description = describe_failure(error)
        index = getattr(error, "_r05_partition_index", None)
        total = getattr(error, "_r05_partition_total", None)
        index = index if type(index) is int and index > 0 else None
        total = total if type(total) is int and total > 0 else None
        if index is None or total is None or index > total:
            index, total = None, None
        available = _available_completions(error)
        # (retry, text, partition_index, partition_total, kind, stage)
        captures: list[tuple[int | None, str | None, int | None, int | None, str, str]] = [
            (retry, text, index, total, "failed_completion", failure_stage)
            for retry, text in available
        ]
        if not captures:
            captures.append((None, None, index, total, "failed_completion", failure_stage))
        prior = getattr(error, "_r05_prior_partitions", ())
        if isinstance(prior, (list, tuple)):
            for part in prior[-_MAX_PARTITION_CAPTURES:]:
                if (
                    isinstance(part, (list, tuple))
                    and len(part) == 3
                    and type(part[0]) is int
                    and type(part[1]) is int
                    and 0 < part[0] <= part[1]
                    and isinstance(part[2], str)
                ):
                    captures.append(
                        (None, part[2], part[0], part[1],
                         "model_validated_partition_structured", "preceding_partition")
                    )
        ids: list[int] = []
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            for retry, text, part_index, part_total, kind, stage in captures:
                if text is None:
                    state, stored = "unavailable", None
                elif len(text.encode("utf-8")) > _MAX_CAPTURE_BYTES:
                    state, stored = "oversize", None
                else:
                    state, stored = "available", text
                cursor = connection.execute(
                    """
                    INSERT INTO job_analysis_failure_diagnostics(
                        attempt_id, failure_code, failure_stage, retry_number,
                        response_state, completion_text, partition_index,
                        partition_total, payload_kind, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        attempt_id, description.code, stage, retry, state,
                        stored, part_index, part_total, kind, now,
                    ),
                )
                ids.append(int(cursor.lastrowid))
            self._prune(connection)
        return tuple(ids)

    def list_for_attempt(self, attempt_id: int) -> tuple[FailureDiagnostic, ...]:
        """Private inspection API; never use in public corpus or candidate readers."""
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM job_analysis_failure_diagnostics "
                "WHERE attempt_id = ? ORDER BY id",
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
                partition_index=(
                    int(row["partition_index"])
                    if row["partition_index"] is not None else None
                ),
                partition_total=(
                    int(row["partition_total"])
                    if row["partition_total"] is not None else None
                ),
                payload_kind=str(row["payload_kind"]),
                created_at=str(row["created_at"]),
            )
            for row in rows
        )
