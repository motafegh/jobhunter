"""Persistence for human-facing Role Capability Blueprint artifacts."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.capability_store import CapabilityIntelligenceStore


@dataclass(frozen=True, slots=True)
class RoleBlueprintArtifact:
    id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int
    analysis_artifact_id: int
    capability_artifact_id: int
    model: str
    prompt_version: str
    schema_version: str
    blueprint: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    created_at: str


class RoleBlueprintStore:
    """Keep expert human-facing interpretation separate from machine-facing reasoning."""

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
        CapabilityIntelligenceStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_role_blueprint_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER NOT NULL,
                    analysis_artifact_id INTEGER NOT NULL,
                    capability_artifact_id INTEGER NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    blueprint_json TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    raw_response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id) REFERENCES job_translation_artifacts(id),
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    FOREIGN KEY(capability_artifact_id)
                        REFERENCES job_capability_intelligence_artifacts(id),
                    UNIQUE(
                        job_detail_version_id,
                        translation_artifact_id,
                        analysis_artifact_id,
                        capability_artifact_id,
                        model,
                        prompt_version,
                        schema_version
                    )
                );

                CREATE TABLE IF NOT EXISTS job_role_blueprint_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    attempted_at TEXT NOT NULL,
                    translation_artifact_id INTEGER,
                    analysis_artifact_id INTEGER,
                    capability_artifact_id INTEGER,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK(outcome IN ('completed', 'failed', 'reused')),
                    artifact_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id) REFERENCES job_translation_artifacts(id),
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    FOREIGN KEY(capability_artifact_id)
                        REFERENCES job_capability_intelligence_artifacts(id),
                    FOREIGN KEY(artifact_id) REFERENCES job_role_blueprint_artifacts(id)
                );

                CREATE INDEX IF NOT EXISTS idx_role_blueprint_artifacts_version
                ON job_role_blueprint_artifacts(job_detail_version_id, id DESC);

                CREATE INDEX IF NOT EXISTS idx_role_blueprint_attempts_version_time
                ON job_role_blueprint_attempts(job_detail_version_id, attempted_at DESC, id DESC);
                """
            )

    def find_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int,
        analysis_artifact_id: int,
        capability_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
    ) -> RoleBlueprintArtifact | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT b.*, p.source_job_id
                FROM job_role_blueprint_artifacts AS b
                JOIN job_detail_versions AS v ON v.id = b.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE b.job_detail_version_id = ?
                  AND b.translation_artifact_id = ?
                  AND b.analysis_artifact_id = ?
                  AND b.capability_artifact_id = ?
                  AND b.model = ?
                  AND b.prompt_version = ?
                  AND b.schema_version = ?
                LIMIT 1
                """,
                (
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    capability_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                ),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def latest_current(
        self,
        source_job_id: str,
        *,
        model: str | None = None,
        prompt_version: str | None = None,
        schema_version: str | None = None,
    ) -> RoleBlueprintArtifact | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT b.*, p.source_job_id
                FROM job_role_blueprint_artifacts AS b
                JOIN job_detail_versions AS v ON v.id = b.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja'
                  AND p.source_job_id = ?
                  AND v.id = (
                      SELECT MAX(v2.id)
                      FROM job_detail_versions AS v2
                      WHERE v2.job_posting_id = p.id
                  )
                  AND (? IS NULL OR b.model = ?)
                  AND (? IS NULL OR b.prompt_version = ?)
                  AND (? IS NULL OR b.schema_version = ?)
                ORDER BY b.id DESC
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

    def record_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int,
        analysis_artifact_id: int,
        capability_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
        blueprint: dict[str, Any],
        request_body: dict[str, Any],
        raw_response: dict[str, Any],
        created_at: datetime,
    ) -> int:
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_role_blueprint_artifacts(
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    capability_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                    blueprint_json,
                    request_json,
                    raw_response_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    capability_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                    json.dumps(blueprint, ensure_ascii=False, sort_keys=True),
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
        translation_artifact_id: int | None = None,
        analysis_artifact_id: int | None = None,
        capability_artifact_id: int | None = None,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> int:
        if outcome not in {"completed", "failed", "reused"}:
            raise ValueError("Unsupported role-blueprint attempt outcome")
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_role_blueprint_attempts(
                    job_detail_version_id,
                    attempted_at,
                    translation_artifact_id,
                    analysis_artifact_id,
                    capability_artifact_id,
                    model,
                    prompt_version,
                    schema_version,
                    outcome,
                    artifact_id,
                    error_type,
                    error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_detail_version_id,
                    attempted_at.isoformat(),
                    translation_artifact_id,
                    analysis_artifact_id,
                    capability_artifact_id,
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


def _artifact(row: sqlite3.Row) -> RoleBlueprintArtifact:
    return RoleBlueprintArtifact(
        id=int(row["id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=int(row["translation_artifact_id"]),
        analysis_artifact_id=int(row["analysis_artifact_id"]),
        capability_artifact_id=int(row["capability_artifact_id"]),
        model=str(row["model"]),
        prompt_version=str(row["prompt_version"]),
        schema_version=str(row["schema_version"]),
        blueprint=json.loads(str(row["blueprint_json"])),
        request_body=json.loads(str(row["request_json"])),
        raw_response=json.loads(str(row["raw_response_json"])),
        created_at=str(row["created_at"]),
    )
