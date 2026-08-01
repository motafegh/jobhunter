"""Read models used by the local JobHunter web interface."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.storage import JobHunterStore
from jobhunter.translation_store import TranslationStore


@dataclass(frozen=True, slots=True)
class DashboardStats:
    discovered_jobs: int
    detailed_jobs: int
    translated_jobs: int
    missing_details: int
    missing_translations: int
    detail_checks: int
    acquisition_runs: int


@dataclass(frozen=True, slots=True)
class WebJobRow:
    source_job_id: str
    title: str
    company: str
    company_slug: str
    location: str
    employment_type: str
    source_language: str
    lifecycle_state: str
    detail_status: str
    semantic_versions: int
    translated: bool
    last_seen_at: str
    latest_detail_at: str | None
    latest_check_at: str | None


@dataclass(frozen=True, slots=True)
class RecentRun:
    id: int
    started_at: str
    completed_at: str | None
    status: str
    searches_attempted: int
    pages_fetched: int
    jobs_discovered: int
    new_jobs: int
    known_jobs: int
    failures: int


class WebRepository:
    """Focused read-only queries for browser views."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _initialize(self) -> None:
        JobHunterStore(self._database_path).initialize()
        JobDetailObservationStore(self._database_path).initialize()
        TranslationStore(self._database_path).initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def dashboard_stats(self) -> DashboardStats:
        self._initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM job_postings WHERE source = 'jobinja')
                        AS discovered_jobs,
                    (
                        SELECT COUNT(*)
                        FROM job_postings AS p
                        WHERE p.source = 'jobinja'
                          AND EXISTS (
                              SELECT 1 FROM job_detail_versions AS v
                              WHERE v.job_posting_id = p.id
                          )
                    ) AS detailed_jobs,
                    (
                        SELECT COUNT(*)
                        FROM job_postings AS p
                        JOIN job_detail_versions AS v ON v.id = (
                            SELECT MAX(v2.id)
                            FROM job_detail_versions AS v2
                            WHERE v2.job_posting_id = p.id
                        )
                        WHERE p.source = 'jobinja'
                          AND v.parse_status = 'parsed'
                          AND EXISTS (
                              SELECT 1
                              FROM job_translation_artifacts AS a
                              WHERE a.job_detail_version_id = v.id
                                AND a.target_language = 'en'
                          )
                    ) AS translated_jobs,
                    (SELECT COUNT(*) FROM job_detail_fetch_observations)
                        AS detail_checks,
                    (SELECT COUNT(*) FROM acquisition_runs) AS acquisition_runs
                """
            ).fetchone()
        discovered = int(row["discovered_jobs"])
        detailed = int(row["detailed_jobs"])
        translated = int(row["translated_jobs"])
        return DashboardStats(
            discovered_jobs=discovered,
            detailed_jobs=detailed,
            translated_jobs=translated,
            missing_details=max(discovered - detailed, 0),
            missing_translations=max(detailed - translated, 0),
            detail_checks=int(row["detail_checks"]),
            acquisition_runs=int(row["acquisition_runs"]),
        )

    def list_jobs(
        self,
        *,
        query: str = "",
        detail: str = "all",
        translation: str = "all",
        lifecycle: str = "all",
        limit: int = 500,
    ) -> tuple[WebJobRow, ...]:
        if detail not in {"all", "available", "missing"}:
            raise ValueError("detail must be all, available, or missing")
        if translation not in {"all", "available", "missing"}:
            raise ValueError("translation must be all, available, or missing")
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")

        self._initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.id AS posting_id,
                    p.source_job_id,
                    p.company_slug,
                    p.title_observed,
                    p.lifecycle_state,
                    p.last_seen_at,
                    v.id AS detail_version_id,
                    v.fetched_at AS latest_detail_at,
                    v.parse_status,
                    v.fields_json,
                    (
                        SELECT COUNT(
                            DISTINCT COALESCE(v3.semantic_sha256, v3.content_sha256)
                        )
                        FROM job_detail_versions AS v3
                        WHERE v3.job_posting_id = p.id
                    ) AS semantic_versions,
                    (
                        SELECT MAX(o.checked_at)
                        FROM job_detail_fetch_observations AS o
                        WHERE o.job_posting_id = p.id
                    ) AS latest_check_at,
                    EXISTS (
                        SELECT 1
                        FROM job_translation_artifacts AS a
                        WHERE a.job_detail_version_id = v.id
                          AND a.target_language = 'en'
                    ) AS translated
                FROM job_postings AS p
                LEFT JOIN job_detail_versions AS v ON v.id = (
                    SELECT MAX(v2.id)
                    FROM job_detail_versions AS v2
                    WHERE v2.job_posting_id = p.id
                )
                WHERE p.source = 'jobinja'
                ORDER BY p.last_seen_at DESC, p.id DESC
                """
            ).fetchall()

        needle = " ".join(query.casefold().split())
        result: list[WebJobRow] = []
        for row in rows:
            fields: dict[str, Any] = {}
            if row["fields_json"]:
                fields = json.loads(str(row["fields_json"]))
            has_detail = row["detail_version_id"] is not None
            translated = bool(row["translated"])
            lifecycle_state = str(row["lifecycle_state"])
            if detail == "available" and not has_detail:
                continue
            if detail == "missing" and has_detail:
                continue
            if translation == "available" and not translated:
                continue
            if translation == "missing" and translated:
                continue
            if lifecycle != "all" and lifecycle_state != lifecycle:
                continue

            title = str(fields.get("title") or row["title_observed"] or "Title unavailable")
            company = str(fields.get("company") or row["company_slug"])
            location = str(fields.get("location") or "—")
            employment_type = str(fields.get("employment_type") or "—")
            source_language = str(fields.get("language") or "unknown")
            haystack = " ".join(
                (
                    str(row["source_job_id"]),
                    title,
                    company,
                    location,
                    employment_type,
                )
            ).casefold()
            if needle and needle not in haystack:
                continue

            result.append(
                WebJobRow(
                    source_job_id=str(row["source_job_id"]),
                    title=title,
                    company=company,
                    company_slug=str(row["company_slug"]),
                    location=location,
                    employment_type=employment_type,
                    source_language=source_language,
                    lifecycle_state=lifecycle_state,
                    detail_status=str(row["parse_status"] or "missing"),
                    semantic_versions=int(row["semantic_versions"] or 0),
                    translated=translated,
                    last_seen_at=str(row["last_seen_at"]),
                    latest_detail_at=(
                        str(row["latest_detail_at"])
                        if row["latest_detail_at"] is not None
                        else None
                    ),
                    latest_check_at=(
                        str(row["latest_check_at"])
                        if row["latest_check_at"] is not None
                        else None
                    ),
                )
            )
            if len(result) >= limit:
                break
        return tuple(result)

    def recent_runs(self, *, limit: int = 8) -> tuple[RecentRun, ...]:
        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")
        self._initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    started_at,
                    completed_at,
                    status,
                    searches_attempted,
                    pages_fetched,
                    jobs_discovered,
                    new_jobs,
                    known_jobs,
                    failures
                FROM acquisition_runs
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return tuple(
            RecentRun(
                id=int(row["id"]),
                started_at=str(row["started_at"]),
                completed_at=(
                    str(row["completed_at"]) if row["completed_at"] is not None else None
                ),
                status=str(row["status"]),
                searches_attempted=int(row["searches_attempted"]),
                pages_fetched=int(row["pages_fetched"]),
                jobs_discovered=int(row["jobs_discovered"]),
                new_jobs=int(row["new_jobs"]),
                known_jobs=int(row["known_jobs"]),
                failures=int(row["failures"]),
            )
            for row in rows
        )
