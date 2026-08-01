"""Cautious lifecycle evidence for Jobinja postings."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.storage import JobHunterStore

_NON_DESTRUCTIVE = {
    "active",
    "rate_limited",
    "access_denied",
    "challenge",
    "auth_required",
    "server_error",
    "network_error",
    "unexpected_page",
    "unknown_error",
}


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    id: int
    source_job_id: str
    checked_at: str
    classification: str
    status_code: int | None
    retryable: bool
    detail: str | None


class LifecycleStore:
    """Persist source-availability evidence without overreacting to one weak signal."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        return connection

    def initialize(self) -> None:
        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_lifecycle_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_posting_id INTEGER NOT NULL,
                    checked_at TEXT NOT NULL,
                    classification TEXT NOT NULL,
                    status_code INTEGER,
                    retryable INTEGER NOT NULL,
                    detail TEXT,
                    FOREIGN KEY(job_posting_id) REFERENCES job_postings(id)
                );
                CREATE INDEX IF NOT EXISTS idx_job_lifecycle_events_job_time
                ON job_lifecycle_events(job_posting_id, checked_at DESC, id DESC);
                """
            )

    def record(
        self,
        source_job_id: str,
        *,
        classification: str,
        status_code: int | None = None,
        retryable: bool = False,
        detail: str | None = None,
        checked_at: datetime | None = None,
    ) -> int:
        self.initialize()
        timestamp = (checked_at or datetime.now(UTC)).isoformat()
        with self._connect() as connection:
            posting = connection.execute(
                "SELECT id FROM job_postings WHERE source = 'jobinja' AND source_job_id = ?",
                (source_job_id,),
            ).fetchone()
            if posting is None:
                raise LookupError(f"Unknown Jobinja job {source_job_id!r}")
            job_posting_id = int(posting["id"])
            cursor = connection.execute(
                """
                INSERT INTO job_lifecycle_events(
                    job_posting_id, checked_at, classification, status_code, retryable, detail
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    job_posting_id,
                    timestamp,
                    classification,
                    status_code,
                    int(retryable),
                    detail,
                ),
            )
            self._apply_cautious_state(
                connection,
                job_posting_id=job_posting_id,
                classification=classification,
            )
            return int(cursor.lastrowid)

    @staticmethod
    def _apply_cautious_state(
        connection: sqlite3.Connection,
        *,
        job_posting_id: int,
        classification: str,
    ) -> None:
        if classification == "active":
            connection.execute(
                "UPDATE job_postings SET lifecycle_state = 'active' WHERE id = ?",
                (job_posting_id,),
            )
            return
        if classification == "expired_explicit":
            connection.execute(
                "UPDATE job_postings SET lifecycle_state = 'expired' WHERE id = ?",
                (job_posting_id,),
            )
            return
        if classification not in {"not_found", "gone"}:
            return

        rows = connection.execute(
            """
            SELECT classification
            FROM job_lifecycle_events
            WHERE job_posting_id = ?
            ORDER BY id DESC
            LIMIT 2
            """,
            (job_posting_id,),
        ).fetchall()
        consecutive = len(rows) == 2 and all(
            str(row["classification"]) in {"not_found", "gone"} for row in rows
        )
        state = "removed" if consecutive else "possibly_unavailable"
        connection.execute(
            "UPDATE job_postings SET lifecycle_state = ? WHERE id = ?",
            (state, job_posting_id),
        )

    def list_for_job(self, source_job_id: str, *, limit: int = 20) -> tuple[LifecycleEvent, ...]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT e.*, p.source_job_id
                FROM job_lifecycle_events AS e
                JOIN job_postings AS p ON p.id = e.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                ORDER BY e.id DESC
                LIMIT ?
                """,
                (source_job_id, limit),
            ).fetchall()
        return tuple(
            LifecycleEvent(
                id=int(row["id"]),
                source_job_id=str(row["source_job_id"]),
                checked_at=str(row["checked_at"]),
                classification=str(row["classification"]),
                status_code=int(row["status_code"]) if row["status_code"] is not None else None,
                retryable=bool(row["retryable"]),
                detail=str(row["detail"]) if row["detail"] is not None else None,
            )
            for row in rows
        )

    def consecutive_failures(self, source_job_id: str) -> int:
        """Count recent non-active lifecycle events until the latest active event."""

        events = self.list_for_job(source_job_id, limit=100)
        count = 0
        for event in events:
            if event.classification == "active":
                break
            if event.classification in _NON_DESTRUCTIVE or event.classification in {
                "not_found",
                "gone",
                "expired_explicit",
            }:
                count += 1
        return count
