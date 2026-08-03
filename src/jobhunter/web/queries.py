"""Read models used by the local JobHunter web interface."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.job_workflow import JobWorkflowStore
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


@dataclass(frozen=True, slots=True)
class DashboardStats:
    discovered_jobs: int
    detailed_jobs: int
    parsed_jobs: int
    translated_jobs: int
    analyzed_jobs: int
    missing_details: int
    missing_translations: int
    missing_analyses: int
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
    triage_state: str
    detail_status: str
    semantic_versions: int
    translated: bool
    analyzed: bool
    discovery_matches: int
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


def _humanize_company_slug(value: str) -> str:
    words = value.replace("_", "-").split("-")
    return " ".join(word[:1].upper() + word[1:] for word in words if word) or value


class WebRepository:
    """Focused read-only queries for browser views."""

    def __init__(
        self,
        database_path: Path,
        *,
        translation_schema_version: str = TRANSLATION_SCHEMA_VERSION,
        analysis_model: str | None = None,
        analysis_prompt_version: str = PROMPT_VERSION,
        analysis_schema_version: str = ANALYSIS_SCHEMA_VERSION,
    ) -> None:
        self._database_path = database_path
        self._translation_schema_version = translation_schema_version
        self._analysis_model = analysis_model
        self._analysis_prompt_version = analysis_prompt_version
        self._analysis_schema_version = analysis_schema_version

    def _initialize(self) -> None:
        JobHunterStore(self._database_path).initialize()
        JobDetailObservationStore(self._database_path).initialize()
        TranslationStore(self._database_path).initialize()
        JobWorkflowStore(self._database_path).initialize()
        AnalysisStore(self._database_path).initialize()

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
                    (SELECT COUNT(*) FROM job_postings WHERE source = 'jobinja') AS discovered_jobs,
                    (
                        SELECT COUNT(*) FROM job_postings AS p
                        WHERE p.source = 'jobinja'
                          AND EXISTS (
                              SELECT 1 FROM job_detail_versions AS v WHERE v.job_posting_id = p.id
                          )
                    ) AS detailed_jobs,
                    (
                        SELECT COUNT(*) FROM job_postings AS p
                        JOIN job_detail_versions AS v ON v.id = (
                            SELECT MAX(v2.id) FROM job_detail_versions AS v2
                            WHERE v2.job_posting_id = p.id
                        )
                        WHERE p.source = 'jobinja' AND v.parse_status = 'parsed'
                    ) AS parsed_jobs,
                    (
                        SELECT COUNT(*) FROM job_postings AS p
                        JOIN job_detail_versions AS v ON v.id = (
                            SELECT MAX(v2.id) FROM job_detail_versions AS v2
                            WHERE v2.job_posting_id = p.id
                        )
                        WHERE p.source = 'jobinja' AND v.parse_status = 'parsed'
                          AND EXISTS (
                              SELECT 1 FROM job_translation_artifacts AS a
                              WHERE a.job_detail_version_id = v.id
                                AND a.target_language = 'en'
                                AND a.translation_schema_version = ?
                          )
                    ) AS translated_jobs,
                    (
                        SELECT COUNT(*) FROM job_postings AS p
                        JOIN job_detail_versions AS v ON v.id = (
                            SELECT MAX(v2.id) FROM job_detail_versions AS v2
                            WHERE v2.job_posting_id = p.id
                        )
                        WHERE p.source = 'jobinja'
                          AND EXISTS (
                              SELECT 1 FROM job_analysis_artifacts AS a
                              WHERE a.job_detail_version_id = v.id
                                AND a.prompt_version = ?
                                AND a.schema_version = ?
                                AND (? IS NULL OR a.model = ?)
                          )
                    ) AS analyzed_jobs,
                    (SELECT COUNT(*) FROM job_detail_fetch_observations) AS detail_checks,
                    (SELECT COUNT(*) FROM acquisition_runs) AS acquisition_runs
                """,
                (
                    self._translation_schema_version,
                    self._analysis_prompt_version,
                    self._analysis_schema_version,
                    self._analysis_model,
                    self._analysis_model,
                ),
            ).fetchone()
        discovered = int(row["discovered_jobs"])
        detailed = int(row["detailed_jobs"])
        parsed = int(row["parsed_jobs"])
        translated = int(row["translated_jobs"])
        analyzed = int(row["analyzed_jobs"])
        return DashboardStats(
            discovered_jobs=discovered,
            detailed_jobs=detailed,
            parsed_jobs=parsed,
            translated_jobs=translated,
            analyzed_jobs=analyzed,
            missing_details=max(discovered - detailed, 0),
            missing_translations=max(parsed - translated, 0),
            missing_analyses=max(translated - analyzed, 0),
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
        triage: str = "all",
        analysis: str = "all",
        limit: int = 500,
    ) -> tuple[WebJobRow, ...]:
        if detail not in {"all", "available", "missing"}:
            raise ValueError("detail must be all, available, or missing")
        if translation not in {"all", "available", "missing"}:
            raise ValueError("translation must be all, available, or missing")
        if analysis not in {"all", "available", "missing"}:
            raise ValueError("analysis must be all, available, or missing")
        triage_states = {
            "all",
            "unreviewed",
            "interested",
            "review_later",
            "not_relevant",
            "reviewed",
        }
        if triage not in triage_states:
            raise ValueError("unsupported triage filter")
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")

        self._initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.id AS posting_id, p.source_job_id, p.company_slug, p.title_observed,
                    p.lifecycle_state, p.last_seen_at,
                    COALESCE(w.triage_state, 'unreviewed') AS triage_state,
                    v.id AS detail_version_id, v.fetched_at AS latest_detail_at,
                    v.parse_status, v.fields_json,
                    (
                        SELECT COUNT(DISTINCT COALESCE(v3.semantic_sha256, v3.content_sha256))
                        FROM job_detail_versions AS v3 WHERE v3.job_posting_id = p.id
                    ) AS semantic_versions,
                    (
                        SELECT MAX(o.checked_at) FROM job_detail_fetch_observations AS o
                        WHERE o.job_posting_id = p.id
                    ) AS latest_check_at,
                    (
                        SELECT COUNT(DISTINCT d.search_name) FROM job_discoveries AS d
                        WHERE d.job_posting_id = p.id
                    ) AS discovery_matches,
                    EXISTS (
                        SELECT 1 FROM job_translation_artifacts AS a
                        WHERE a.job_detail_version_id = v.id
                          AND a.target_language = 'en'
                          AND a.translation_schema_version = ?
                    ) AS translated,
                    EXISTS (
                        SELECT 1 FROM job_analysis_artifacts AS aa
                        WHERE aa.job_detail_version_id = v.id
                          AND aa.prompt_version = ?
                          AND aa.schema_version = ?
                          AND (? IS NULL OR aa.model = ?)
                    ) AS analyzed
                FROM job_postings AS p
                LEFT JOIN job_user_workflow AS w ON w.job_posting_id = p.id
                LEFT JOIN job_detail_versions AS v ON v.id = (
                    SELECT MAX(v2.id) FROM job_detail_versions AS v2
                    WHERE v2.job_posting_id = p.id
                )
                WHERE p.source = 'jobinja'
                ORDER BY p.last_seen_at DESC, p.id DESC
                """,
                (
                    self._translation_schema_version,
                    self._analysis_prompt_version,
                    self._analysis_schema_version,
                    self._analysis_model,
                    self._analysis_model,
                ),
            ).fetchall()

        needle = " ".join(query.casefold().split())
        result: list[WebJobRow] = []
        for row in rows:
            fields: dict[str, Any] = {}
            if row["fields_json"]:
                fields = json.loads(str(row["fields_json"]))
            has_detail = row["detail_version_id"] is not None
            translated = bool(row["translated"])
            analyzed = bool(row["analyzed"])
            lifecycle_state = str(row["lifecycle_state"])
            triage_state = str(row["triage_state"])
            if detail == "available" and not has_detail:
                continue
            if detail == "missing" and has_detail:
                continue
            if translation == "available" and not translated:
                continue
            if translation == "missing" and translated:
                continue
            if analysis == "available" and not analyzed:
                continue
            if analysis == "missing" and analyzed:
                continue
            if lifecycle != "all" and lifecycle_state != lifecycle:
                continue
            if triage != "all" and triage_state != triage:
                continue

            title = str(fields.get("title") or row["title_observed"] or "Title unavailable")
            raw_company = str(fields.get("company") or "").strip()
            company_slug = str(row["company_slug"])
            company = raw_company or _humanize_company_slug(company_slug)
            location = str(fields.get("location") or "—")
            employment_type = str(fields.get("employment_type") or "—")
            source_language = str(fields.get("language") or "unknown")
            haystack = " ".join(
                (
                    str(row["source_job_id"]),
                    title,
                    company,
                    company_slug,
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
                    company_slug=company_slug,
                    location=location,
                    employment_type=employment_type,
                    source_language=source_language,
                    lifecycle_state=lifecycle_state,
                    triage_state=triage_state,
                    detail_status=str(row["parse_status"] or "missing"),
                    semantic_versions=int(row["semantic_versions"] or 0),
                    translated=translated,
                    analyzed=analyzed,
                    discovery_matches=int(row["discovery_matches"] or 0),
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
                SELECT id, started_at, completed_at, status, searches_attempted,
                       pages_fetched, jobs_discovered, new_jobs, known_jobs, failures
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
