"""Concise source-health read model over preserved detail/lifecycle history."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.lifecycle import LifecycleStore
from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class SourceHealthSummary:
    """Current operational/source state for one logical Jobinja posting."""

    source_job_id: str
    lifecycle_state: str
    total_checks: int
    last_checked_at: str | None
    last_check_outcome: str | None
    last_successful_check_at: str | None
    consecutive_operational_failures: int
    latest_failure_type: str | None
    latest_failure_message: str | None
    latest_lifecycle_classification: str | None
    latest_lifecycle_checked_at: str | None
    consecutive_lifecycle_failures: int


class SourceHealthReader:
    """Build a compact source-health view without mutating source or lifecycle truth."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def get(self, source_job_id: str) -> SourceHealthSummary:
        source_job_id = source_job_id.strip()
        if not source_job_id:
            raise ValueError("source_job_id must not be empty")

        JobHunterStore(self._database_path).initialize()
        JobDetailObservationStore(self._database_path).initialize()
        LifecycleStore(self._database_path).initialize()

        with self._connect() as connection:
            posting = connection.execute(
                """
                SELECT id, source_job_id, lifecycle_state
                FROM job_postings
                WHERE source = 'jobinja' AND source_job_id = ?
                """,
                (source_job_id,),
            ).fetchone()
            if posting is None:
                raise LookupError(f"Unknown Jobinja job {source_job_id!r}")

            job_posting_id = int(posting["id"])
            checks = connection.execute(
                """
                SELECT id, checked_at, outcome, error_type, error_message
                FROM job_detail_fetch_observations
                WHERE job_posting_id = ?
                ORDER BY id DESC
                """,
                (job_posting_id,),
            ).fetchall()
            lifecycle = connection.execute(
                """
                SELECT checked_at, classification
                FROM job_lifecycle_events
                WHERE job_posting_id = ?
                ORDER BY id DESC
                """,
                (job_posting_id,),
            ).fetchall()

        last_check = checks[0] if checks else None
        last_successful = next(
            (row for row in checks if str(row["outcome"]) != "failed"),
            None,
        )
        latest_failure = next(
            (row for row in checks if str(row["outcome"]) == "failed"),
            None,
        )
        consecutive_operational_failures = 0
        for row in checks:
            if str(row["outcome"]) != "failed":
                break
            consecutive_operational_failures += 1

        latest_lifecycle = lifecycle[0] if lifecycle else None
        consecutive_lifecycle_failures = 0
        for row in lifecycle:
            if str(row["classification"]) == "active":
                break
            consecutive_lifecycle_failures += 1

        return SourceHealthSummary(
            source_job_id=str(posting["source_job_id"]),
            lifecycle_state=str(posting["lifecycle_state"]),
            total_checks=len(checks),
            last_checked_at=(
                str(last_check["checked_at"]) if last_check is not None else None
            ),
            last_check_outcome=(
                str(last_check["outcome"]) if last_check is not None else None
            ),
            last_successful_check_at=(
                str(last_successful["checked_at"])
                if last_successful is not None
                else None
            ),
            consecutive_operational_failures=consecutive_operational_failures,
            latest_failure_type=(
                str(latest_failure["error_type"])
                if latest_failure is not None
                and latest_failure["error_type"] is not None
                else None
            ),
            latest_failure_message=(
                str(latest_failure["error_message"])
                if latest_failure is not None
                and latest_failure["error_message"] is not None
                else None
            ),
            latest_lifecycle_classification=(
                str(latest_lifecycle["classification"])
                if latest_lifecycle is not None
                else None
            ),
            latest_lifecycle_checked_at=(
                str(latest_lifecycle["checked_at"])
                if latest_lifecycle is not None
                else None
            ),
            consecutive_lifecycle_failures=consecutive_lifecycle_failures,
        )


def format_source_health(summary: SourceHealthSummary) -> str:
    """Format source health as a concise complement to the detailed checks timeline."""

    lines = [
        f"Jobinja source health: {summary.source_job_id}",
        f"Lifecycle state: {summary.lifecycle_state}",
        f"Recorded detail checks: {summary.total_checks}",
        f"Last check: {summary.last_checked_at or '(none)'}",
        f"Last check outcome: {summary.last_check_outcome or '(none)'}",
        f"Last successful check: {summary.last_successful_check_at or '(none)'}",
        f"Consecutive operational failures: {summary.consecutive_operational_failures}",
        (
            "Latest lifecycle signal: "
            + (
                f"{summary.latest_lifecycle_classification} at "
                f"{summary.latest_lifecycle_checked_at}"
                if summary.latest_lifecycle_classification
                else "(none)"
            )
        ),
        f"Consecutive lifecycle non-active signals: {summary.consecutive_lifecycle_failures}",
    ]
    if summary.latest_failure_message:
        lines.append(
            "Latest operational failure: "
            f"{summary.latest_failure_type or 'Error'}: {summary.latest_failure_message}"
        )
    return "\n".join(lines)
