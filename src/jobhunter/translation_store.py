"""SQLite persistence for derived English translation artifacts."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class TranslationSourceVersion:
    source_job_id: str
    job_detail_version_id: int
    semantic_sha256: str
    source_language: str
    fields: dict[str, Any]


@dataclass(frozen=True, slots=True)
class TranslationArtifact:
    id: int
    source_job_id: str
    job_detail_version_id: int
    source_semantic_sha256: str
    source_language: str
    target_language: str
    provider_name: str
    provider_model: str
    translation_schema_version: str
    fields: dict[str, Any]
    english_document: str
    segment_provenance: dict[str, str]
    translated_segment_count: int
    native_segment_count: int
    translation_sha256: str
    created_at: str


class TranslationStore:
    """Keep derived translations separate from source job versions."""

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
        JobHunterStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS job_translation_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    target_language TEXT NOT NULL,
                    provider_name TEXT NOT NULL,
                    provider_model TEXT NOT NULL,
                    translation_schema_version TEXT NOT NULL,
                    source_semantic_sha256 TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    translated_fields_json TEXT NOT NULL,
                    english_document TEXT NOT NULL,
                    segment_provenance_json TEXT NOT NULL,
                    translated_segment_count INTEGER NOT NULL,
                    native_segment_count INTEGER NOT NULL,
                    translation_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    UNIQUE(
                        job_detail_version_id,
                        target_language,
                        provider_name,
                        provider_model,
                        translation_schema_version
                    )
                );

                CREATE TABLE IF NOT EXISTS job_translation_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_detail_version_id INTEGER NOT NULL,
                    attempted_at TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    provider_name TEXT NOT NULL,
                    provider_model TEXT NOT NULL,
                    translation_schema_version TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK (
                        outcome IN ('completed', 'failed', 'reused')
                    ),
                    artifact_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(artifact_id) REFERENCES job_translation_artifacts(id)
                );

                CREATE INDEX IF NOT EXISTS idx_translation_artifacts_version
                ON job_translation_artifacts(job_detail_version_id, id DESC);

                CREATE INDEX IF NOT EXISTS idx_translation_attempts_version_time
                ON job_translation_attempts(job_detail_version_id, attempted_at DESC, id DESC);
                """
            )

    def latest_source_version(
        self,
        source_job_id: str,
    ) -> TranslationSourceVersion | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    p.source_job_id,
                    v.id AS job_detail_version_id,
                    v.semantic_sha256,
                    v.fields_json
                FROM job_postings AS p
                JOIN job_detail_versions AS v ON v.job_posting_id = p.id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                ORDER BY v.id DESC
                LIMIT 1
                """,
                (source_job_id,),
            ).fetchone()
        if row is None:
            return None
        fields = json.loads(str(row["fields_json"]))
        return TranslationSourceVersion(
            source_job_id=str(row["source_job_id"]),
            job_detail_version_id=int(row["job_detail_version_id"]),
            semantic_sha256=str(row["semantic_sha256"]),
            source_language=str(fields.get("language") or "unknown"),
            fields=fields,
        )

    def latest_source_versions(
        self,
        *,
        limit: int = 500,
    ) -> tuple[TranslationSourceVersion, ...]:
        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.source_job_id,
                    v.id AS job_detail_version_id,
                    v.semantic_sha256,
                    v.fields_json
                FROM job_postings AS p
                JOIN job_detail_versions AS v ON v.job_posting_id = p.id
                WHERE p.source = 'jobinja'
                  AND v.id = (
                      SELECT MAX(latest.id)
                      FROM job_detail_versions AS latest
                      WHERE latest.job_posting_id = p.id
                  )
                ORDER BY p.id ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        result: list[TranslationSourceVersion] = []
        for row in rows:
            fields = json.loads(str(row["fields_json"]))
            result.append(
                TranslationSourceVersion(
                    source_job_id=str(row["source_job_id"]),
                    job_detail_version_id=int(row["job_detail_version_id"]),
                    semantic_sha256=str(row["semantic_sha256"]),
                    source_language=str(fields.get("language") or "unknown"),
                    fields=fields,
                )
            )
        return tuple(result)

    def find_artifact(
        self,
        *,
        job_detail_version_id: int,
        target_language: str,
        provider_name: str,
        provider_model: str,
        translation_schema_version: str,
    ) -> TranslationArtifact | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    a.*,
                    p.source_job_id
                FROM job_translation_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE a.job_detail_version_id = ?
                  AND a.target_language = ?
                  AND a.provider_name = ?
                  AND a.provider_model = ?
                  AND a.translation_schema_version = ?
                LIMIT 1
                """,
                (
                    job_detail_version_id,
                    target_language,
                    provider_name,
                    provider_model,
                    translation_schema_version,
                ),
            ).fetchone()
        return _artifact_from_row(row) if row is not None else None

    def latest_artifact(
        self,
        source_job_id: str,
        *,
        target_language: str = "en",
    ) -> TranslationArtifact | None:
        """Return an artifact only when it belongs to the latest source version."""

        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_translation_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja'
                  AND p.source_job_id = ?
                  AND a.target_language = ?
                  AND v.id = (
                      SELECT MAX(latest.id)
                      FROM job_detail_versions AS latest
                      WHERE latest.job_posting_id = p.id
                  )
                ORDER BY a.id DESC
                LIMIT 1
                """,
                (source_job_id, target_language),
            ).fetchone()
        return _artifact_from_row(row) if row is not None else None

    def list_latest_artifacts(
        self,
        *,
        target_language: str = "en",
        limit: int = 500,
    ) -> tuple[TranslationArtifact, ...]:
        """Return current artifacts only; stale source versions are excluded."""

        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_translation_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE p.source = 'jobinja'
                  AND a.target_language = ?
                  AND v.id = (
                      SELECT MAX(latest.id)
                      FROM job_detail_versions AS latest
                      WHERE latest.job_posting_id = p.id
                  )
                  AND a.id = (
                      SELECT MAX(a2.id)
                      FROM job_translation_artifacts AS a2
                      WHERE a2.job_detail_version_id = v.id
                        AND a2.target_language = ?
                  )
                ORDER BY p.id ASC
                LIMIT ?
                """,
                (target_language, target_language, limit),
            ).fetchall()
        return tuple(_artifact_from_row(row) for row in rows)

    def record_artifact(
        self,
        *,
        source: TranslationSourceVersion,
        target_language: str,
        provider_name: str,
        provider_model: str,
        translation_schema_version: str,
        fields: dict[str, Any],
        english_document: str,
        segment_provenance: dict[str, str],
        translated_segment_count: int,
        native_segment_count: int,
        translation_sha256: str,
        created_at: datetime,
    ) -> int:
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_translation_artifacts(
                    job_detail_version_id,
                    target_language,
                    provider_name,
                    provider_model,
                    translation_schema_version,
                    source_semantic_sha256,
                    source_language,
                    translated_fields_json,
                    english_document,
                    segment_provenance_json,
                    translated_segment_count,
                    native_segment_count,
                    translation_sha256,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source.job_detail_version_id,
                    target_language,
                    provider_name,
                    provider_model,
                    translation_schema_version,
                    source.semantic_sha256,
                    source.source_language,
                    json.dumps(fields, ensure_ascii=False, sort_keys=True),
                    english_document,
                    json.dumps(segment_provenance, ensure_ascii=False, sort_keys=True),
                    translated_segment_count,
                    native_segment_count,
                    translation_sha256,
                    created_at.isoformat(),
                ),
            )
            return int(cursor.lastrowid)

    def record_attempt(
        self,
        *,
        source: TranslationSourceVersion,
        attempted_at: datetime,
        target_language: str,
        provider_name: str,
        provider_model: str,
        translation_schema_version: str,
        outcome: str,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> int:
        if outcome not in {"completed", "failed", "reused"}:
            raise ValueError("Unsupported translation attempt outcome")
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_translation_attempts(
                    job_detail_version_id,
                    attempted_at,
                    target_language,
                    provider_name,
                    provider_model,
                    translation_schema_version,
                    outcome,
                    artifact_id,
                    error_type,
                    error_message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source.job_detail_version_id,
                    attempted_at.isoformat(),
                    target_language,
                    provider_name,
                    provider_model,
                    translation_schema_version,
                    outcome,
                    artifact_id,
                    type(error).__name__ if error is not None else None,
                    str(error) if error is not None else None,
                ),
            )
            return int(cursor.lastrowid)


def _artifact_from_row(row: sqlite3.Row) -> TranslationArtifact:
    return TranslationArtifact(
        id=int(row["id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        source_semantic_sha256=str(row["source_semantic_sha256"]),
        source_language=str(row["source_language"]),
        target_language=str(row["target_language"]),
        provider_name=str(row["provider_name"]),
        provider_model=str(row["provider_model"]),
        translation_schema_version=str(row["translation_schema_version"]),
        fields=json.loads(str(row["translated_fields_json"])),
        english_document=str(row["english_document"]),
        segment_provenance=json.loads(str(row["segment_provenance_json"])),
        translated_segment_count=int(row["translated_segment_count"]),
        native_segment_count=int(row["native_segment_count"]),
        translation_sha256=str(row["translation_sha256"]),
        created_at=str(row["created_at"]),
    )
