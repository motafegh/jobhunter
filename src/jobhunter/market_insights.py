"""Deterministic aggregate views over discovery and accepted semantic analysis."""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from jobhunter.analysis_store import AnalysisStore
from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class SearchEffectiveness:
    search_name: str
    distinct_jobs: int
    discovery_events: int
    runs: int
    unique_contributions: int


@dataclass(frozen=True, slots=True)
class RequirementDemand:
    concept: str
    jobs: int
    required: int
    preferred: int
    contextual: int
    inferred: int


@dataclass(frozen=True, slots=True)
class MarketSummary:
    analyzed_jobs: int
    responsibility_claims: int
    requirement_claims: int
    requirements: tuple[RequirementDemand, ...]


class MarketInsights:
    """Read-only aggregate intelligence; no source or model mutation happens here."""

    def __init__(
        self,
        database_path: Path,
        *,
        analysis_model: str | None = None,
        analysis_prompt_version: str | None = None,
        analysis_schema_version: str | None = None,
    ) -> None:
        self._database_path = database_path
        self._analysis_model = analysis_model
        self._analysis_prompt_version = analysis_prompt_version
        self._analysis_schema_version = analysis_schema_version

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def search_effectiveness(self, *, limit: int = 200) -> tuple[SearchEffectiveness, ...]:
        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                WITH distinct_matches AS (
                    SELECT DISTINCT run_id, job_posting_id, search_name
                    FROM job_discoveries
                ),
                per_match AS (
                    SELECT
                        run_id,
                        job_posting_id,
                        search_name,
                        COUNT(*) OVER (
                            PARTITION BY run_id, job_posting_id
                        ) AS searches_for_job
                    FROM distinct_matches
                )
                SELECT
                    search_name,
                    COUNT(DISTINCT job_posting_id) AS distinct_jobs,
                    COUNT(*) AS discovery_events,
                    COUNT(DISTINCT run_id) AS runs,
                    SUM(CASE WHEN searches_for_job = 1 THEN 1 ELSE 0 END) AS unique_contributions
                FROM per_match
                GROUP BY search_name
                ORDER BY unique_contributions DESC, distinct_jobs DESC, search_name ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return tuple(
            SearchEffectiveness(
                search_name=str(row["search_name"]),
                distinct_jobs=int(row["distinct_jobs"]),
                discovery_events=int(row["discovery_events"]),
                runs=int(row["runs"]),
                unique_contributions=int(row["unique_contributions"] or 0),
            )
            for row in rows
        )

    def job_search_provenance(self, source_job_id: str) -> tuple[str, ...]:
        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT d.search_name
                FROM job_discoveries AS d
                JOIN job_postings AS p ON p.id = d.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                ORDER BY d.search_name ASC
                """,
                (source_job_id,),
            ).fetchall()
        return tuple(str(row["search_name"]) for row in rows)

    def market_summary(self, *, top_requirements: int = 50) -> MarketSummary:
        artifacts = AnalysisStore(self._database_path).list_current(
            limit=5000,
            model=self._analysis_model,
            prompt_version=self._analysis_prompt_version,
            schema_version=self._analysis_schema_version,
        )
        job_sets: dict[str, set[str]] = defaultdict(set)
        classification_job_sets: dict[str, dict[str, set[str]]] = defaultdict(
            lambda: {
                "required": set(),
                "preferred": set(),
                "contextual": set(),
                "inferred": set(),
            }
        )
        display_names: dict[str, str] = {}
        responsibility_claims = 0
        requirement_claims = 0
        for artifact in artifacts:
            responsibility_claims += len(artifact.analysis.get("responsibilities") or [])
            for item in artifact.analysis.get("requirements") or []:
                if not isinstance(item, dict):
                    continue
                concept = str(item.get("concept") or "").strip()
                classification = str(item.get("requirement_type") or "")
                if not concept or classification not in {
                    "required",
                    "preferred",
                    "contextual",
                    "inferred",
                }:
                    continue
                key = " ".join(concept.casefold().split())
                display_names.setdefault(key, concept)
                job_sets[key].add(artifact.source_job_id)
                classification_job_sets[key][classification].add(artifact.source_job_id)
                requirement_claims += 1

        requirements = [
            RequirementDemand(
                concept=display_names[key],
                jobs=len(job_sets[key]),
                required=len(classification_job_sets[key]["required"]),
                preferred=len(classification_job_sets[key]["preferred"]),
                contextual=len(classification_job_sets[key]["contextual"]),
                inferred=len(classification_job_sets[key]["inferred"]),
            )
            for key in job_sets
        ]
        requirements.sort(
            key=lambda item: (-item.jobs, -item.required, item.concept.casefold())
        )
        return MarketSummary(
            analyzed_jobs=len(artifacts),
            responsibility_claims=responsibility_claims,
            requirement_claims=requirement_claims,
            requirements=tuple(requirements[:top_requirements]),
        )
