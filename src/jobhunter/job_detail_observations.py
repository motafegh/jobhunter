"""Operational history for every Jobinja detail-page fetch attempt."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class JobDetailFetchObservation:
    """One successful or failed attempt to check a Jobinja detail page."""

    id: int
    source_job_id: str
    checked_at: str
    outcome: str
    requested_url: str
    final_url: str | None
    status_code: int | None
    content_sha256: str | None
    semantic_sha256: str | None
    evidence_path: str | None
    metadata_path: str | None
    parser_version: str | None
    parse_status: str | None
    job_detail_version_id: int | None
    error_type: str | None
    error_message: str | None


class JobDetailObservationStore:
    """Persist and query detail-fetch observations independently from versions."""

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
        """Create the observation table after the core JobHunter schema exists."""

        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_detail_fetch_observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_posting_id INTEGER NOT NULL,
                    checked_at TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK (
                        outcome IN ('new_version', 'unchanged', 'failed')
                    ),
                    requested_url TEXT NOT NULL,
                    final_url TEXT,
                    status_code INTEGER,
                    content_sha256 TEXT,
                    semantic_sha256 TEXT,
                    evidence_path TEXT,
                    metadata_path TEXT,
                    parser_version TEXT,
                    parse_status TEXT,
                    job_detail_version_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(job_posting_id) REFERENCES job_postings(id),
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id)
                );

                CREATE INDEX IF NOT EXISTS idx_detail_fetch_observations_job_time
                ON job_detail_fetch_observations(job_posting_id, checked_at DESC, id DESC);
                """
            )

    def record_success(
        self,
        *,
        job_posting_id: int,
        checked_at: datetime,
        requested_url: str,
        final_url: str,
        status_code: int,
        content_sha256: str,
        semantic_sha256: str,
        evidence_path: Path,
        metadata_path: Path,
        parser_version: str,
        parse_status: str,
        job_detail_version_id: int,
        is_new_version: bool,
    ) -> int:
        """Record a successful check whether content changed or not."""

        self.initialize()
        outcome = "new_version" if is_new_version else "unchanged"
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_detail_fetch_observations(
                    job_posting_id,
                    checked_at,
                    outcome,
                    requested_url,
                    final_url,
                    status_code,
                    content_sha256,
                    semantic_sha256,
                    evidence_path,
                    metadata_path,
                    parser_version,
                    parse_status,
                    job_detail_version_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_posting_id,
                    checked_at.isoformat(),
                    outcome,
                    requested_url,
                    final_url,
                    status_code,
                    content_sha256,
                    semantic_sha256,
                    str(evidence_path),
                    str(metadata_path),
                    parser_version,
                    parse_status,
                    job_detail_version_id,
                ),
            )
            return int(cursor.lastrowid)

    def record_failure(
        self,
        *,
        job_posting_id: int,
        checked_at: datetime,
        requested_url: str,
        error: Exception,
    ) -> int:
        """Record a retryable failed check without changing semantic history."""

        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_detail_fetch_observations(
                    job_posting_id,
                    checked_at,
                    outcome,
                    requested_url,
                    error_type,
                    error_message
                )
                VALUES (?, ?, 'failed', ?, ?, ?)
                """,
                (
                    job_posting_id,
                    checked_at.isoformat(),
                    requested_url,
                    type(error).__name__,
                    str(error),
                ),
            )
            return int(cursor.lastrowid)

    def list_for_job(
        self,
        source_job_id: str,
        *,
        limit: int = 20,
    ) -> tuple[JobDetailFetchObservation, ...]:
        """Return newest observations for one stable Jobinja job ID."""

        if not 1 <= limit <= 200:
            raise ValueError("limit must be between 1 and 200")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    o.id,
                    p.source_job_id,
                    o.checked_at,
                    o.outcome,
                    o.requested_url,
                    o.final_url,
                    o.status_code,
                    o.content_sha256,
                    o.semantic_sha256,
                    o.evidence_path,
                    o.metadata_path,
                    o.parser_version,
                    o.parse_status,
                    o.job_detail_version_id,
                    o.error_type,
                    o.error_message
                FROM job_detail_fetch_observations AS o
                JOIN job_postings AS p ON p.id = o.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                ORDER BY o.checked_at DESC, o.id DESC
                LIMIT ?
                """,
                (source_job_id, limit),
            ).fetchall()
        return tuple(_observation_from_row(row) for row in rows)

    def refresh_due_job_ids(
        self,
        *,
        as_of: datetime,
        older_than_hours: float,
        limit: int,
    ) -> tuple[str, ...]:
        """Select acquired jobs whose most recent check is older than a threshold."""

        if older_than_hours <= 0:
            raise ValueError("older_than_hours must be greater than zero")
        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        self.initialize()
        cutoff = as_of.astimezone(UTC) - timedelta(hours=older_than_hours)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.source_job_id,
                    COALESCE(
                        (
                            SELECT MAX(o.checked_at)
                            FROM job_detail_fetch_observations AS o
                            WHERE o.job_posting_id = p.id
                        ),
                        (
                            SELECT MAX(v.fetched_at)
                            FROM job_detail_versions AS v
                            WHERE v.job_posting_id = p.id
                        )
                    ) AS last_checked_at
                FROM job_postings AS p
                WHERE p.source = 'jobinja'
                  AND EXISTS (
                      SELECT 1
                      FROM job_detail_versions AS v
                      WHERE v.job_posting_id = p.id
                  )
                ORDER BY last_checked_at ASC, p.id ASC
                """
            ).fetchall()

        selected: list[str] = []
        for row in rows:
            raw_timestamp = row["last_checked_at"]
            if raw_timestamp is None:
                continue
            checked_at = datetime.fromisoformat(str(raw_timestamp))
            if checked_at.tzinfo is None:
                checked_at = checked_at.replace(tzinfo=UTC)
            if checked_at.astimezone(UTC) > cutoff:
                continue
            selected.append(str(row["source_job_id"]))
            if len(selected) >= limit:
                break
        return tuple(selected)

    def count_for_job(self, source_job_id: str) -> int:
        """Return the number of recorded checks for one Jobinja job."""

        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM job_detail_fetch_observations AS o
                JOIN job_postings AS p ON p.id = o.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                """,
                (source_job_id,),
            ).fetchone()
        return int(row["count"])


def _observation_from_row(row: sqlite3.Row) -> JobDetailFetchObservation:
    return JobDetailFetchObservation(
        id=int(row["id"]),
        source_job_id=str(row["source_job_id"]),
        checked_at=str(row["checked_at"]),
        outcome=str(row["outcome"]),
        requested_url=str(row["requested_url"]),
        final_url=str(row["final_url"]) if row["final_url"] is not None else None,
        status_code=int(row["status_code"]) if row["status_code"] is not None else None,
        content_sha256=(
            str(row["content_sha256"])
            if row["content_sha256"] is not None
            else None
        ),
        semantic_sha256=(
            str(row["semantic_sha256"])
            if row["semantic_sha256"] is not None
            else None
        ),
        evidence_path=(
            str(row["evidence_path"]) if row["evidence_path"] is not None else None
        ),
        metadata_path=(
            str(row["metadata_path"]) if row["metadata_path"] is not None else None
        ),
        parser_version=(
            str(row["parser_version"]) if row["parser_version"] is not None else None
        ),
        parse_status=(
            str(row["parse_status"]) if row["parse_status"] is not None else None
        ),
        job_detail_version_id=(
            int(row["job_detail_version_id"])
            if row["job_detail_version_id"] is not None
            else None
        ),
        error_type=str(row["error_type"]) if row["error_type"] is not None else None,
        error_message=(
            str(row["error_message"]) if row["error_message"] is not None else None
        ),
    )


def format_job_detail_observations(
    observations: tuple[JobDetailFetchObservation, ...],
    *,
    source_job_id: str,
) -> str:
    """Format operational fetch history without dumping raw page contents."""

    lines = [
        f"Jobinja detail checks for {source_job_id}",
        f"Observations shown: {len(observations)}",
    ]
    if not observations:
        lines.append("No recorded detail checks.")
        return "\n".join(lines)

    for observation in observations:
        line = f"- {observation.checked_at}: {observation.outcome}"
        if observation.job_detail_version_id is not None:
            line += f", semantic version {observation.job_detail_version_id}"
        if observation.parse_status:
            line += f", {observation.parse_status}"
        lines.append(line)
        if observation.error_message:
            lines.append(
                f"  error: {observation.error_type or 'Error'}: "
                f"{observation.error_message}"
            )
        elif observation.evidence_path:
            lines.append(f"  raw evidence: {observation.evidence_path}")
    return "\n".join(lines)
