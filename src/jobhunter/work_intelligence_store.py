"""Persistence for versioned candidate Job Work Intelligence artifacts.

Persistence provides reproducibility and reuse. It does *not* promote generated interpretation into
canonical responsibility families or role archetypes.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_store import AnalysisStore


@dataclass(frozen=True, slots=True)
class JobWorkIntelligenceArtifact:
    id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int
    analysis_artifact_id: int
    analysis_model: str
    analysis_prompt_version: str
    analysis_schema_version: str
    model: str
    prompt_version: str
    schema_version: str
    intelligence: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    semantic_state: str
    created_at: str


class WorkIntelligenceStore:
    """Store immutable candidate interpretations above one exact P1.6 artifact."""

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
        AnalysisStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_work_intelligence_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_artifact_id INTEGER NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    intelligence_json TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    raw_response_json TEXT NOT NULL,
                    semantic_state TEXT NOT NULL DEFAULT 'candidate'
                        CHECK(semantic_state = 'candidate'),
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    UNIQUE(analysis_artifact_id, model, prompt_version, schema_version)
                );

                CREATE TABLE IF NOT EXISTS job_work_intelligence_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_artifact_id INTEGER NOT NULL,
                    attempted_at TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK(outcome IN ('completed', 'failed', 'reused')),
                    artifact_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    FOREIGN KEY(artifact_id) REFERENCES job_work_intelligence_artifacts(id)
                );

                CREATE INDEX IF NOT EXISTS idx_work_intelligence_analysis
                ON job_work_intelligence_artifacts(analysis_artifact_id, id DESC);
                CREATE INDEX IF NOT EXISTS idx_work_intelligence_attempts
                ON job_work_intelligence_attempts(
                    analysis_artifact_id,
                    attempted_at DESC,
                    id DESC
                );
                """
            )

    def find_artifact(
        self,
        *,
        analysis_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
    ) -> JobWorkIntelligenceArtifact | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT w.*, a.job_detail_version_id, a.translation_artifact_id,
                       a.model AS analysis_model,
                       a.prompt_version AS analysis_prompt_version,
                       a.schema_version AS analysis_schema_version,
                       p.source_job_id
                FROM job_work_intelligence_artifacts AS w
                JOIN job_analysis_artifacts AS a ON a.id = w.analysis_artifact_id
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE w.analysis_artifact_id = ?
                  AND w.model = ?
                  AND w.prompt_version = ?
                  AND w.schema_version = ?
                LIMIT 1
                """,
                (analysis_artifact_id, model, prompt_version, schema_version),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def artifact_by_id(self, artifact_id: int) -> JobWorkIntelligenceArtifact | None:
        if artifact_id <= 0:
            raise ValueError("artifact_id must be greater than zero")
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT w.*, a.job_detail_version_id, a.translation_artifact_id,
                       a.model AS analysis_model,
                       a.prompt_version AS analysis_prompt_version,
                       a.schema_version AS analysis_schema_version,
                       p.source_job_id
                FROM job_work_intelligence_artifacts AS w
                JOIN job_analysis_artifacts AS a ON a.id = w.analysis_artifact_id
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE w.id = ?
                LIMIT 1
                """,
                (artifact_id,),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def latest_for_job(
        self,
        source_job_id: str,
        *,
        prompt_version: str | None = None,
        schema_version: str | None = None,
    ) -> JobWorkIntelligenceArtifact | None:
        """Return latest persisted candidate; currentness is evaluated by the service."""

        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT w.*, a.job_detail_version_id, a.translation_artifact_id,
                       a.model AS analysis_model,
                       a.prompt_version AS analysis_prompt_version,
                       a.schema_version AS analysis_schema_version,
                       p.source_job_id
                FROM job_work_intelligence_artifacts AS w
                JOIN job_analysis_artifacts AS a ON a.id = w.analysis_artifact_id
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                  AND (? IS NULL OR w.prompt_version = ?)
                  AND (? IS NULL OR w.schema_version = ?)
                ORDER BY w.id DESC
                LIMIT 1
                """,
                (
                    source_job_id,
                    prompt_version,
                    prompt_version,
                    schema_version,
                    schema_version,
                ),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def record_artifact(
        self,
        *,
        analysis_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
        intelligence: dict[str, Any],
        request_body: dict[str, Any],
        raw_response: dict[str, Any],
        created_at: datetime,
    ) -> int:
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_work_intelligence_artifacts(
                    analysis_artifact_id, model, prompt_version, schema_version,
                    intelligence_json, request_json, raw_response_json,
                    semantic_state, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'candidate', ?)
                """,
                (
                    analysis_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                    json.dumps(intelligence, ensure_ascii=False, sort_keys=True),
                    json.dumps(request_body, ensure_ascii=False, sort_keys=True),
                    json.dumps(raw_response, ensure_ascii=False, sort_keys=True),
                    created_at.isoformat(),
                ),
            )
            return int(cursor.lastrowid)

    def record_attempt(
        self,
        *,
        analysis_artifact_id: int,
        attempted_at: datetime,
        model: str,
        prompt_version: str,
        schema_version: str,
        outcome: str,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> int:
        if outcome not in {"completed", "failed", "reused"}:
            raise ValueError("Unsupported Work Intelligence attempt outcome")
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_work_intelligence_attempts(
                    analysis_artifact_id, attempted_at, model, prompt_version,
                    schema_version, outcome, artifact_id, error_type, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    analysis_artifact_id,
                    attempted_at.isoformat(),
                    model,
                    prompt_version,
                    schema_version,
                    outcome,
                    artifact_id,
                    type(error).__name__ if error is not None else None,
                    str(error) if error is not None else None,
                ),
            )
            return int(cursor.lastrowid)


def _artifact(row: sqlite3.Row) -> JobWorkIntelligenceArtifact:
    translation_artifact_id = row["translation_artifact_id"]
    if translation_artifact_id is None:
        raise RuntimeError("P2.2A Work Intelligence requires an English P1.6 dependency")
    return JobWorkIntelligenceArtifact(
        id=int(row["id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=int(translation_artifact_id),
        analysis_artifact_id=int(row["analysis_artifact_id"]),
        analysis_model=str(row["analysis_model"]),
        analysis_prompt_version=str(row["analysis_prompt_version"]),
        analysis_schema_version=str(row["analysis_schema_version"]),
        model=str(row["model"]),
        prompt_version=str(row["prompt_version"]),
        schema_version=str(row["schema_version"]),
        intelligence=json.loads(str(row["intelligence_json"])),
        request_body=json.loads(str(row["request_json"])),
        raw_response=json.loads(str(row["raw_response_json"])),
        semantic_state=str(row["semantic_state"]),
        created_at=str(row["created_at"]),
    )


__all__ = ["JobWorkIntelligenceArtifact", "WorkIntelligenceStore"]
