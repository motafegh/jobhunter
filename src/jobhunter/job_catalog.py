"""Read-only local catalog queries for discovered and acquired jobs."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class LocalJobSummary:
    """Compact local state for one discovered Jobinja posting."""

    source_job_id: str
    title: str | None
    company_slug: str
    lifecycle_state: str
    first_seen_at: str
    last_seen_at: str
    detail_status: str
    semantic_versions: int
    latest_detail_at: str | None


class JobCatalog:
    """Provide bounded read-only views over the local JobHunter database."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def list_jobs(
        self,
        *,
        detail_filter: str = "all",
        limit: int = 50,
    ) -> tuple[LocalJobSummary, ...]:
        """List discovered jobs with their latest local detail status."""

        if detail_filter not in {"all", "missing", "available"}:
            raise ValueError("detail_filter must be all, missing, or available")
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")

        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.source_job_id,
                    p.title_observed,
                    p.company_slug,
                    p.lifecycle_state,
                    p.first_seen_at,
                    p.last_seen_at,
                    COUNT(
                        DISTINCT COALESCE(v.semantic_sha256, v.content_sha256)
                    ) AS semantic_versions,
                    (
                        SELECT latest.parse_status
                        FROM job_detail_versions AS latest
                        WHERE latest.job_posting_id = p.id
                        ORDER BY latest.id DESC
                        LIMIT 1
                    ) AS detail_status,
                    (
                        SELECT latest.fetched_at
                        FROM job_detail_versions AS latest
                        WHERE latest.job_posting_id = p.id
                        ORDER BY latest.id DESC
                        LIMIT 1
                    ) AS latest_detail_at
                FROM job_postings AS p
                LEFT JOIN job_detail_versions AS v ON v.job_posting_id = p.id
                WHERE p.source = 'jobinja'
                GROUP BY p.id
                ORDER BY p.id ASC
                """
            ).fetchall()

        entries: list[LocalJobSummary] = []
        for row in rows:
            semantic_versions = int(row["semantic_versions"])
            if detail_filter == "missing" and semantic_versions:
                continue
            if detail_filter == "available" and not semantic_versions:
                continue
            entries.append(
                LocalJobSummary(
                    source_job_id=str(row["source_job_id"]),
                    title=row["title_observed"],
                    company_slug=str(row["company_slug"]),
                    lifecycle_state=str(row["lifecycle_state"]),
                    first_seen_at=str(row["first_seen_at"]),
                    last_seen_at=str(row["last_seen_at"]),
                    detail_status=str(row["detail_status"] or "missing"),
                    semantic_versions=semantic_versions,
                    latest_detail_at=(
                        str(row["latest_detail_at"])
                        if row["latest_detail_at"] is not None
                        else None
                    ),
                )
            )
            if len(entries) >= limit:
                break
        return tuple(entries)

    def missing_job_ids(
        self,
        *,
        limit: int,
        preferred_ids: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        """Return missing-detail jobs, prioritizing supplied source IDs."""

        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")

        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT p.source_job_id
                FROM job_postings AS p
                WHERE p.source = 'jobinja'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM job_detail_versions AS v
                      WHERE v.job_posting_id = p.id
                  )
                ORDER BY p.id ASC
                """
            ).fetchall()

        available = tuple(str(row["source_job_id"]) for row in rows)
        available_set = set(available)
        preferred = tuple(
            dict.fromkeys(
                source_job_id.strip()
                for source_job_id in preferred_ids
                if source_job_id.strip()
            )
        )
        prioritized = [
            source_job_id
            for source_job_id in preferred
            if source_job_id in available_set
        ]
        prioritized_set = set(prioritized)
        prioritized.extend(
            source_job_id
            for source_job_id in available
            if source_job_id not in prioritized_set
        )
        return tuple(prioritized[:limit])


def format_job_list(entries: tuple[LocalJobSummary, ...]) -> str:
    """Format an inspectable terminal list of local jobs."""

    available = sum(1 for entry in entries if entry.semantic_versions)
    missing = len(entries) - available
    lines = [
        f"Local jobs shown: {len(entries)}",
        f"Details available: {available}",
        f"Details missing: {missing}",
    ]
    if not entries:
        lines.append("No matching jobs.")
        return "\n".join(lines)

    lines.append("Jobs:")
    for entry in entries:
        if entry.semantic_versions:
            version_word = "version" if entry.semantic_versions == 1 else "versions"
            status = (
                f"{entry.detail_status}, "
                f"{entry.semantic_versions} semantic {version_word}"
            )
        else:
            status = "missing"
        title = entry.title or "(title unavailable)"
        lines.append(f"- {entry.source_job_id} [{status}] {title}")
    return "\n".join(lines)
