"""Persistence for versioned, model-derived JobHunter semantic analysis."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.translation_store import TranslationStore

SEMANTIC_REVIEW_PENDING = "pending"
SEMANTIC_REVIEW_ACCEPTED = "accepted"
_SEMANTIC_REVIEW_STATUSES = {SEMANTIC_REVIEW_PENDING, SEMANTIC_REVIEW_ACCEPTED}


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
    semantic_review_status: str = SEMANTIC_REVIEW_ACCEPTED
    semantic_reviewed_at: str | None = None
    semantic_review_note: str | None = None


@dataclass(frozen=True, slots=True)
class AnalysisReviewResult:
    source_job_id: str
    artifact_id: int
    disposition: str
    outcome: str


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
                    semantic_review_status TEXT NOT NULL DEFAULT 'accepted'
                        CHECK(semantic_review_status IN ('pending', 'accepted')),
                    semantic_reviewed_at TEXT,
                    semantic_review_note TEXT,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id) REFERENCES job_translation_artifacts(id)
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

                CREATE TABLE IF NOT EXISTS job_analysis_rejected_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_artifact_id INTEGER NOT NULL UNIQUE,
                    source_job_id TEXT NOT NULL,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    analysis_json TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    raw_response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    rejected_at TEXT NOT NULL,
                    rejection_note TEXT NOT NULL,
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id) REFERENCES job_translation_artifacts(id)
                );
                """
            )
            columns = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(job_analysis_artifacts)")
            }
            if "semantic_review_status" not in columns:
                connection.execute(
                    "ALTER TABLE job_analysis_artifacts "
                    "ADD COLUMN semantic_review_status TEXT NOT NULL DEFAULT 'accepted' "
                    "CHECK(semantic_review_status IN ('pending', 'accepted'))"
                )
            if "semantic_reviewed_at" not in columns:
                connection.execute(
                    "ALTER TABLE job_analysis_artifacts ADD COLUMN semantic_reviewed_at TEXT"
                )
            if "semantic_review_note" not in columns:
                connection.execute(
                    "ALTER TABLE job_analysis_artifacts ADD COLUMN semantic_review_note TEXT"
                )
        self._migrate_translation_dependency_identity()

    def _migrate_translation_dependency_identity(self) -> None:
        """Make an English projection artifact part of P1.6 artifact identity.

        The original table-level uniqueness omitted ``translation_artifact_id``. That
        made a new projection for an unchanged source version silently reuse analysis
        derived from the previous projection. Partial unique indexes retain one
        original-language artifact per contract while preserving separately versioned
        English dependencies.
        """

        with self._connect() as connection:
            table_sql_row = connection.execute(
                "SELECT sql FROM sqlite_master "
                "WHERE type = 'table' AND name = 'job_analysis_artifacts'"
            ).fetchone()
            table_sql = str(table_sql_row["sql"] or "") if table_sql_row else ""
            normalized_sql = "".join(table_sql.split()).casefold()
            legacy_unique = (
                "unique(job_detail_version_id,model,prompt_version,schema_version)"
                in normalized_sql
            )

        if legacy_unique:
            with self._connect() as connection:
                connection.execute("PRAGMA foreign_keys=OFF")
                connection.executescript(
                    """
                    BEGIN IMMEDIATE;
                    CREATE TABLE job_analysis_artifacts_dependency_v2 (
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
                        semantic_review_status TEXT NOT NULL DEFAULT 'accepted'
                            CHECK(semantic_review_status IN ('pending', 'accepted')),
                        semantic_reviewed_at TEXT,
                        semantic_review_note TEXT,
                        FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                        FOREIGN KEY(translation_artifact_id)
                            REFERENCES job_translation_artifacts(id)
                    );
                    INSERT INTO job_analysis_artifacts_dependency_v2(
                        id, job_detail_version_id, translation_artifact_id, model,
                        prompt_version, schema_version, analysis_json, request_json,
                        raw_response_json, created_at, semantic_review_status,
                        semantic_reviewed_at, semantic_review_note
                    )
                    SELECT
                        id, job_detail_version_id, translation_artifact_id, model,
                        prompt_version, schema_version, analysis_json, request_json,
                        raw_response_json, created_at, semantic_review_status,
                        semantic_reviewed_at, semantic_review_note
                    FROM job_analysis_artifacts;
                    DROP TABLE job_analysis_artifacts;
                    ALTER TABLE job_analysis_artifacts_dependency_v2
                        RENAME TO job_analysis_artifacts;
                    COMMIT;
                    """
                )

        with self._connect() as connection:
            connection.executescript(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_analysis_original_contract
                ON job_analysis_artifacts(
                    job_detail_version_id, model, prompt_version, schema_version
                )
                WHERE translation_artifact_id IS NULL;

                CREATE UNIQUE INDEX IF NOT EXISTS uq_analysis_english_dependency_contract
                ON job_analysis_artifacts(
                    job_detail_version_id, translation_artifact_id,
                    model, prompt_version, schema_version
                )
                WHERE translation_artifact_id IS NOT NULL;

                CREATE INDEX IF NOT EXISTS idx_analysis_artifacts_version
                ON job_analysis_artifacts(job_detail_version_id, id DESC);
                """
            )

    def find_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int | None = None,
        require_translation_dependency: bool = False,
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
                  AND (? = 0 OR a.translation_artifact_id = ?)
                ORDER BY a.id DESC
                LIMIT 1
                """,
                (
                    job_detail_version_id,
                    model,
                    prompt_version,
                    schema_version,
                    int(require_translation_dependency),
                    translation_artifact_id,
                ),
            ).fetchone()
        return _artifact(row) if row is not None else None

    def artifact_by_id(self, artifact_id: int) -> AnalysisArtifact | None:
        """Return one immutable analysis artifact by ID."""

        if artifact_id <= 0:
            raise ValueError("artifact_id must be greater than zero")
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT a.*, p.source_job_id
                FROM job_analysis_artifacts AS a
                JOIN job_detail_versions AS v ON v.id = a.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE a.id = ?
                LIMIT 1
                """,
                (artifact_id,),
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
        semantic_review_status: str = SEMANTIC_REVIEW_ACCEPTED,
    ) -> int:
        if semantic_review_status not in _SEMANTIC_REVIEW_STATUSES:
            raise ValueError("Unsupported semantic review status")
        self.initialize()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO job_analysis_artifacts(
                    job_detail_version_id, translation_artifact_id, model,
                    prompt_version, schema_version, analysis_json, request_json,
                    raw_response_json, created_at, semantic_review_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    semantic_review_status,
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
        accepted_only: bool = False,
        translation_artifact_id: int | None = None,
        require_translation_dependency: bool = False,
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
                  AND (? = 0 OR a.semantic_review_status = 'accepted')
                  AND (? = 0 OR a.translation_artifact_id = ?)
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
                    int(accepted_only),
                    int(require_translation_dependency),
                    translation_artifact_id,
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
        accepted_only: bool = False,
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
                  AND (? = 0 OR a.semantic_review_status = 'accepted')
                  AND a.id = (
                      SELECT MAX(a2.id) FROM job_analysis_artifacts AS a2
                      WHERE a2.job_detail_version_id = v.id
                        AND (? IS NULL OR a2.model = ?)
                        AND (? IS NULL OR a2.prompt_version = ?)
                        AND (? IS NULL OR a2.schema_version = ?)
                        AND (? = 0 OR a2.semantic_review_status = 'accepted')
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
                    int(accepted_only),
                    model,
                    model,
                    prompt_version,
                    prompt_version,
                    schema_version,
                    schema_version,
                    int(accepted_only),
                    limit,
                ),
            ).fetchall()
        return tuple(_artifact(row) for row in rows)

    def review_current(
        self,
        source_job_id: str,
        *,
        model: str,
        prompt_version: str,
        schema_version: str,
        disposition: str,
        reviewed_at: datetime,
        note: str,
        translation_artifact_id: int | None = None,
        require_translation_dependency: bool = False,
    ) -> AnalysisReviewResult:
        """Accept or archive/reject one current-contract analysis after human review."""

        if disposition not in {SEMANTIC_REVIEW_ACCEPTED, "rejected"}:
            raise ValueError("Semantic review disposition must be accepted or rejected")
        normalized_note = " ".join(note.split())
        if len(normalized_note) < 8:
            raise ValueError("Semantic review note must contain at least 8 characters")

        artifact = self.latest_current(
            source_job_id,
            model=model,
            prompt_version=prompt_version,
            schema_version=schema_version,
            translation_artifact_id=translation_artifact_id,
            require_translation_dependency=require_translation_dependency,
        )
        if artifact is None:
            raise LookupError("Job has no current analysis artifact matching the review contract")
        if disposition == SEMANTIC_REVIEW_ACCEPTED and (
            artifact.semantic_review_status == SEMANTIC_REVIEW_ACCEPTED
        ):
            return AnalysisReviewResult(
                source_job_id=source_job_id,
                artifact_id=artifact.id,
                disposition=SEMANTIC_REVIEW_ACCEPTED,
                outcome="reused",
            )

        self.initialize()
        reviewed_at_text = reviewed_at.isoformat()
        with self._connect() as connection:
            if disposition == SEMANTIC_REVIEW_ACCEPTED:
                connection.execute(
                    """
                    UPDATE job_analysis_artifacts
                    SET semantic_review_status = 'accepted',
                        semantic_reviewed_at = ?, semantic_review_note = ?
                    WHERE id = ?
                    """,
                    (reviewed_at_text, normalized_note, artifact.id),
                )
                return AnalysisReviewResult(
                    source_job_id=source_job_id,
                    artifact_id=artifact.id,
                    disposition=SEMANTIC_REVIEW_ACCEPTED,
                    outcome="completed",
                )

            capability_table = connection.execute(
                """
                SELECT 1 FROM sqlite_master
                WHERE type = 'table' AND name = 'job_capability_intelligence_artifacts'
                """
            ).fetchone()
            if capability_table is not None:
                downstream = connection.execute(
                    """
                    SELECT id FROM job_capability_intelligence_artifacts
                    WHERE analysis_artifact_id = ? LIMIT 1
                    """,
                    (artifact.id,),
                ).fetchone()
                if downstream is not None:
                    raise ValueError(
                        "Cannot reject an analysis artifact with durable Capability downstream"
                    )

            connection.execute(
                """
                INSERT INTO job_analysis_rejected_artifacts(
                    original_artifact_id, source_job_id, job_detail_version_id,
                    translation_artifact_id, model, prompt_version, schema_version,
                    analysis_json, request_json, raw_response_json, created_at,
                    rejected_at, rejection_note
                )
                SELECT id, ?, job_detail_version_id, translation_artifact_id, model,
                       prompt_version, schema_version, analysis_json, request_json,
                       raw_response_json, created_at, ?, ?
                FROM job_analysis_artifacts WHERE id = ?
                """,
                (source_job_id, reviewed_at_text, normalized_note, artifact.id),
            )
            connection.execute(
                "UPDATE job_analysis_attempts SET artifact_id = NULL WHERE artifact_id = ?",
                (artifact.id,),
            )
            connection.execute("DELETE FROM job_analysis_artifacts WHERE id = ?", (artifact.id,))
        return AnalysisReviewResult(
            source_job_id=source_job_id,
            artifact_id=artifact.id,
            disposition="rejected",
            outcome="completed",
        )


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
        semantic_review_status=str(row["semantic_review_status"]),
        semantic_reviewed_at=(
            str(row["semantic_reviewed_at"])
            if row["semantic_reviewed_at"] is not None
            else None
        ),
        semantic_review_note=(
            str(row["semantic_review_note"])
            if row["semantic_review_note"] is not None
            else None
        ),
    )
