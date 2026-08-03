"""Persistence for versioned, model-derived JobHunter semantic analysis."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.translation_store import TranslationStore


@dataclass(frozen=True, slots=True)
class AnalysisArtifact:
    id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int | None
    model: str
    prompt_version: str
    schema_version: str
    analysis: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    created_at: str


class AnalysisStore:
    """Keep model interpretation separate from source and translation artifacts."""

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
        # P1.6 analysis artifacts can reference translation artifacts, so initialize the
        # translation store first. TranslationStore in turn migrates the core source schema.
        # This preserves the dependency order for both fresh and legacy SQLite workspaces:
        # source -> translation -> analysis.
        TranslationStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_analysis_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    analysis_json TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    raw_response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id) REFERENCES job_translation_artifacts(id),
                    UNIQUE(job_detail_version_id, model, prompt_version, schema_version)
                );

                CREATE TABLE IF NOT EXISTS job_analysis_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    attempted_at TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK(outcome IN ('completed', 'failed', 'reused')),
                    artifact_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(artifact_id) REFERENCES job_analysis_artifacts(id)
                );

                CREATE INDEX IF NOT EXISTS idx_analysis_artifacts_version
                ON job_analysis_artifacts(job_detail_version_id, id DESC);
                CREATE INDEX IF NOT EXISTS idx_analysis_attempts_version
                ON job_analysis_attempts(job_detail_version_id, attempted_at DESC, id DESC);
                """
            )

    def find_artifact(
        self,
        *,
        job_detail_version_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
    ) -> AnalysisArtifact | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_analysis_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE a.job_detail_version_id = ? AND a.model = ?
                  AND a.prompt_version = ? AND a.schema_version = ?
                LIMIT 1
                """,
                (job_detail_version_id, model, prompt_version, schema_version),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def record_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int | None,
        model: str,
        prompt_version: str,
        schema_version: str,
        analysis: dict[str, Any],
        request_body: dict[str, Any],
        raw_response: dict[str, Any],
        created_at: datetime,
    ) -> int:
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_analysis_artifacts(
                    job_detail_version_id, translation_artifact_id, model,
                    prompt_version, schema_version, analysis_json, request_json,
                    raw_response_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_detail_version_id,
                    translation_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                    json.dumps(analysis, ensure_ascii=False, sort_keys=True),
                    json.dumps(request_body, ensure_ascii=False, sort_keys=True),
                    json.dumps(raw_response, ensure_ascii=False, sort_keys=True),
                    created_at.isoformat(),
                ),
            )
            return int(cursor.lastrowid)

    def record_attempt(
        self,
        *,
        job_detail_version_id: int,
        attempted_at: datetime,
        model: str,
        prompt_version: str,
        schema_version: str,
        outcome: str,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> int:
        if outcome not in {"completed", "failed", "reused"}:
            raise ValueError("Unsupported analysis attempt outcome")
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_analysis_attempts(
                    job_detail_version_id, attempted_at, model, prompt_version,
                    schema_version, outcome, artifact_id, error_type, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_detail_version_id,
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

    def latest_current(
        self,
        source_job_id: str,
        *,
        model: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
    ) -> AnalysisArtifact | None:
        """Return current-source analysis matching the requested analysis contract."""

        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_analysis_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                  AND v.id = (
                      SELECT MAX(v2.id) FROM job_detail_versions AS v2
                      WHERE v2.job_posting_id = p.id
                  )
                  AND (? IS NULL OR a.model = ?)
                  AND (? IS NULL OR a.prompt_version = ?)
                  AND (? IS NULL OR a.schema_version = ?)
                ORDER BY a.id DESC
                LIMIT 1
                """,
                (
                    source_job_id,
                    model,
                    model,
                    prompt_version,
                    prompt_version,
                    schema_version,
                    schema_version,
                ),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def list_current(
        self,
        *,
        limit: int = 5000,
        model: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
    ) -> tuple[AnalysisArtifact, ...]:
        """List current-source artifacts matching one optional analysis contract."""

        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_analysis_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja'
                  AND v.id = (
                      SELECT MAX(v2.id) FROM job_detail_versions AS v2
                      WHERE v2.job_posting_id = p.id
                  )
                  AND (? IS NULL OR a.model = ?)
                  AND (? IS NULL OR a.prompt_version = ?)
                  AND (? IS NULL OR a.schema_version = ?)
                  AND a.id = (
                      SELECT MAX(a2.id) FROM job_analysis_artifacts AS a2
                      WHERE a2.job_detail_version_id = v.id
                        AND (? IS NULL OR a2.model = ?)
                        AND (? IS NULL OR a2.prompt_version = ?)
                        AND (? IS NULL OR a2.schema_version = ?)
                  )
                ORDER BY p.id ASC
                LIMIT ?
                """,
                (
                    model,
                    model,
                    prompt_version,
                    prompt_version,
                    schema_version,
                    schema_version,
                    model,
                    model,
                    prompt_version,
                    prompt_version,
                    schema_version,
                    schema_version,
                    limit,
                ),
            ).fetchall()
        return tuple(_artifact(row) for row in rows)


def _artifact(row: sqlite3.Row) -> AnalysisArtifact:
    return AnalysisArtifact(
        id=int(row["id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=(
            int(row["translation_artifact_id"])
            if row["translation_artifact_id"] is not None
            else None
        ),
        model=str(row["model"]),
        prompt_version=str(row["prompt_version"]),
        schema_version=str(row["schema_version"]),
        analysis=json.loads(str(row["analysis_json"])),
        request_body=json.loads(str(row["request_json"])),
        raw_response=json.loads(str(row["raw_response_json"])),
        created_at=str(row["created_at"]),
    )
