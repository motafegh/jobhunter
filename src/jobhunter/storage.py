"""SQLite persistence for JobHunter acquisition and discovery records."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink


@dataclass(frozen=True, slots=True)
class JobUpsertResult:
    """Result of creating or refreshing one logical source job."""

    job_posting_id: int
    is_new: bool


class JobHunterStore:
    """Small SQLite repository for the active Phase 1 records."""

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
        """Create the minimum repeat-safe Phase 1 discovery schema."""

        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS source_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    name TEXT NOT NULL,
                    canonical_url TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    max_pages INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(source, name)
                );

                CREATE TABLE IF NOT EXISTS acquisition_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    status TEXT NOT NULL,
                    searches_attempted INTEGER NOT NULL DEFAULT 0,
                    pages_fetched INTEGER NOT NULL DEFAULT 0,
                    jobs_discovered INTEGER NOT NULL DEFAULT 0,
                    new_jobs INTEGER NOT NULL DEFAULT 0,
                    known_jobs INTEGER NOT NULL DEFAULT 0,
                    failures INTEGER NOT NULL DEFAULT 0,
                    error_summary TEXT
                );

                CREATE TABLE IF NOT EXISTS search_page_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    search_name TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    requested_url TEXT NOT NULL,
                    final_url TEXT NOT NULL,
                    fetched_at TEXT NOT NULL,
                    status_code INTEGER NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    evidence_path TEXT NOT NULL,
                    metadata_path TEXT NOT NULL,
                    discovered_count INTEGER NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES acquisition_runs(id),
                    UNIQUE(run_id, search_name, page_number)
                );

                CREATE TABLE IF NOT EXISTS job_postings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    source_job_id TEXT NOT NULL,
                    company_slug TEXT NOT NULL,
                    canonical_url TEXT NOT NULL,
                    title_observed TEXT,
                    first_seen_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    lifecycle_state TEXT NOT NULL DEFAULT 'active',
                    UNIQUE(source, source_job_id)
                );

                CREATE TABLE IF NOT EXISTS job_discoveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    job_posting_id INTEGER NOT NULL,
                    search_name TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    discovered_at TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES acquisition_runs(id),
                    FOREIGN KEY(job_posting_id) REFERENCES job_postings(id),
                    UNIQUE(run_id, job_posting_id, search_name, page_number)
                );
                """
            )

    def start_run(self, *, source: str, started_at: datetime) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO acquisition_runs(source, started_at, status)
                VALUES (?, ?, 'running')
                """,
                (source, started_at.isoformat()),
            )
            return int(cursor.lastrowid)

    def upsert_search(
        self,
        *,
        source: str,
        name: str,
        canonical_url: str,
        enabled: bool,
        max_pages: int,
        observed_at: datetime,
    ) -> None:
        timestamp = observed_at.isoformat()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO source_searches(
                    source, name, canonical_url, enabled, max_pages, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source, name) DO UPDATE SET
                    canonical_url = excluded.canonical_url,
                    enabled = excluded.enabled,
                    max_pages = excluded.max_pages,
                    updated_at = excluded.updated_at
                """,
                (
                    source,
                    name,
                    canonical_url,
                    int(enabled),
                    max_pages,
                    timestamp,
                    timestamp,
                ),
            )

    def record_search_page(
        self,
        *,
        run_id: int,
        search_name: str,
        page_number: int,
        requested_url: str,
        final_url: str,
        fetched_at: datetime,
        status_code: int,
        content_sha256: str,
        evidence_path: Path,
        metadata_path: Path,
        discovered_count: int,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO search_page_snapshots(
                    run_id,
                    search_name,
                    page_number,
                    requested_url,
                    final_url,
                    fetched_at,
                    status_code,
                    content_sha256,
                    evidence_path,
                    metadata_path,
                    discovered_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    search_name,
                    page_number,
                    requested_url,
                    final_url,
                    fetched_at.isoformat(),
                    status_code,
                    content_sha256,
                    str(evidence_path),
                    str(metadata_path),
                    discovered_count,
                ),
            )

    def upsert_job(
        self,
        *,
        job: DiscoveredJobLink,
        observed_at: datetime,
    ) -> JobUpsertResult:
        timestamp = observed_at.isoformat()
        with self._connect() as connection:
            existing = connection.execute(
                """
                SELECT id
                FROM job_postings
                WHERE source = 'jobinja' AND source_job_id = ?
                """,
                (job.source_job_id,),
            ).fetchone()

            if existing is not None:
                connection.execute(
                    """
                    UPDATE job_postings
                    SET company_slug = ?,
                        canonical_url = ?,
                        title_observed = COALESCE(?, title_observed),
                        last_seen_at = ?,
                        lifecycle_state = 'active'
                    WHERE id = ?
                    """,
                    (
                        job.company_slug,
                        job.canonical_url,
                        job.observed_text,
                        timestamp,
                        int(existing["id"]),
                    ),
                )
                return JobUpsertResult(int(existing["id"]), False)

            cursor = connection.execute(
                """
                INSERT INTO job_postings(
                    source,
                    source_job_id,
                    company_slug,
                    canonical_url,
                    title_observed,
                    first_seen_at,
                    last_seen_at
                )
                VALUES ('jobinja', ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.source_job_id,
                    job.company_slug,
                    job.canonical_url,
                    job.observed_text,
                    timestamp,
                    timestamp,
                ),
            )
            return JobUpsertResult(int(cursor.lastrowid), True)

    def record_discovery(
        self,
        *,
        run_id: int,
        job_posting_id: int,
        search_name: str,
        page_number: int,
        discovered_at: datetime,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO job_discoveries(
                    run_id,
                    job_posting_id,
                    search_name,
                    page_number,
                    discovered_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    job_posting_id,
                    search_name,
                    page_number,
                    discovered_at.isoformat(),
                ),
            )

    def complete_run(
        self,
        *,
        run_id: int,
        completed_at: datetime,
        status: str,
        searches_attempted: int,
        pages_fetched: int,
        jobs_discovered: int,
        new_jobs: int,
        known_jobs: int,
        failures: int,
        error_summary: str | None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE acquisition_runs
                SET completed_at = ?,
                    status = ?,
                    searches_attempted = ?,
                    pages_fetched = ?,
                    jobs_discovered = ?,
                    new_jobs = ?,
                    known_jobs = ?,
                    failures = ?,
                    error_summary = ?
                WHERE id = ?
                """,
                (
                    completed_at.isoformat(),
                    status,
                    searches_attempted,
                    pages_fetched,
                    jobs_discovered,
                    new_jobs,
                    known_jobs,
                    failures,
                    error_summary,
                    run_id,
                ),
            )

    def count_job_postings(self) -> int:
        """Return the number of logical Jobinja jobs, primarily for tests and diagnostics."""

        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) AS count FROM job_postings").fetchone()
            return int(row["count"])
