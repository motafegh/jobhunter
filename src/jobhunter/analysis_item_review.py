"""Non-authoritative, source-anchored item review of pending English P1.6.

Original generated claims remain untouched. Review observations and suggested
corrections do not create a revised candidate or authorize factual promotion.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore

_KINDS = {"role_purpose", "responsibilities", "requirements"}
_FINDINGS = {"supported", "needs_clarification", "unsupported"}
_GAP_FINDINGS = {"gap_open", "gap_dismissed"}


def _json(item: Any) -> str:
    return json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _digest(item: Any) -> str:
    return hashlib.sha256(_json(item).encode("utf-8")).hexdigest()


def _note(value: str) -> str:
    note = " ".join(value.split())
    if not 8 <= len(note) <= 2000:
        raise ValueError("Review note must contain 8–2000 characters")
    return note


@dataclass(frozen=True, slots=True)
class ItemReviewEvent:
    id: int
    artifact_id: int
    kind: str
    item_index: int | None
    item_digest: str
    finding: str
    material: bool
    note: str
    source_excerpt: str | None
    proposed_text: str | None
    original_item: dict[str, Any] | None
    created_at: str


class AnalysisItemReviewStore:
    """Append-only item/gap findings with a reviewed-artifact promotion fence."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
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
                CREATE TABLE IF NOT EXISTS job_analysis_item_review_sessions (
                    artifact_id INTEGER PRIMARY KEY,
                    source_job_id TEXT NOT NULL,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    completion_note TEXT
                );
                CREATE TABLE IF NOT EXISTS job_analysis_item_review_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artifact_id INTEGER NOT NULL,
                    kind TEXT NOT NULL CHECK(kind IN (
                        'role_purpose','responsibilities','requirements','coverage_gap')),
                    item_index INTEGER,
                    item_digest TEXT NOT NULL,
                    finding TEXT NOT NULL CHECK(finding IN (
                        'supported','needs_clarification','unsupported',
                        'gap_open','gap_dismissed')),
                    material INTEGER NOT NULL CHECK(material IN (0,1)),
                    note TEXT NOT NULL,
                    source_excerpt TEXT,
                    proposed_text TEXT,
                    original_item_json TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(artifact_id)
                        REFERENCES job_analysis_item_review_sessions(artifact_id)
                );
                CREATE INDEX IF NOT EXISTS idx_item_review_events_artifact
                ON job_analysis_item_review_events(artifact_id, id);
                CREATE TRIGGER IF NOT EXISTS item_review_events_immutable_update
                BEFORE UPDATE ON job_analysis_item_review_events
                BEGIN SELECT RAISE(ABORT, 'Item review history is immutable'); END;
                CREATE TRIGGER IF NOT EXISTS item_review_events_immutable_delete
                BEFORE DELETE ON job_analysis_item_review_events
                BEGIN SELECT RAISE(ABORT, 'Item review history is immutable'); END;
                -- This gate is owned by the shared analysis table. Both CLI and
                -- browser review_current use the same SQL acceptance transition.
                CREATE TRIGGER IF NOT EXISTS item_review_acceptance_fence
                BEFORE UPDATE OF semantic_review_status ON job_analysis_artifacts
                WHEN NEW.semantic_review_status = 'accepted'
                 AND OLD.semantic_review_status = 'pending'
                 AND EXISTS (
                     SELECT 1 FROM job_analysis_item_review_sessions s
                     WHERE s.artifact_id = OLD.id AND s.completed_at IS NULL
                 )
                BEGIN
                    SELECT RAISE(ABORT, 'Finish item review before analysis acceptance');
                END;
                """
            )

    def _pending(self, artifact_id: int) -> AnalysisArtifact:
        artifact = AnalysisStore(self._database_path).artifact_by_id(artifact_id)
        if artifact is None or artifact.semantic_review_status != "pending":
            raise ValueError("Item review requires a persisted pending analysis artifact")
        if artifact.translation_artifact_id is None or (
            artifact.prompt_version not in {"job-analysis-english-v21", "job-analysis-english-v23"}
            or artifact.schema_version != "job-analysis-v5"
        ):
            raise ValueError("Item review supports new English v21/v5 or v23/v5 candidates only")
        current = AnalysisStore(self._database_path).latest_current(
            artifact.source_job_id,
            model=artifact.model,
            prompt_version=artifact.prompt_version,
            schema_version=artifact.schema_version,
            translation_artifact_id=artifact.translation_artifact_id,
            require_translation_dependency=True,
        )
        if current is None or current.id != artifact_id:
            raise ValueError("Item review requires the exact current candidate and projection")
        return artifact

    def _begin(self, connection: sqlite3.Connection, artifact: AnalysisArtifact) -> None:
        connection.execute(
            """INSERT OR IGNORE INTO job_analysis_item_review_sessions(
                   artifact_id, source_job_id, job_detail_version_id,
                   translation_artifact_id, model, prompt_version, schema_version,
                   started_at
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                artifact.id, artifact.source_job_id, artifact.job_detail_version_id,
                artifact.translation_artifact_id, artifact.model, artifact.prompt_version,
                artifact.schema_version, datetime.now(UTC).isoformat(),
            ),
        )

    def begin(self, artifact_id: int) -> None:
        """Start explicit complete-item review; legacy untouched candidates remain unchanged."""
        self.initialize()
        artifact = self._pending(artifact_id)
        with self._connect() as connection:
            self._begin(connection, artifact)

    def _source_excerpt(self, artifact: AnalysisArtifact, excerpt: str) -> str:
        text = excerpt.strip()
        if not 1 <= len(text) <= 2000:
            raise ValueError("Source excerpt must be 1–2000 characters")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT translated_fields_json FROM job_translation_artifacts WHERE id = ?",
                (artifact.translation_artifact_id,),
            ).fetchone()
        if row is None:
            raise ValueError("Current English projection is unavailable")
        fields = json.loads(str(row["translated_fields_json"]))

        def present(value: Any) -> bool:
            if isinstance(value, str):
                return text in value
            if isinstance(value, list):
                return any(present(entry) for entry in value)
            if isinstance(value, dict):
                return any(present(entry) for entry in value.values())
            return False

        if not present(fields):
            raise ValueError("Coverage excerpt must be exact current English source evidence")
        return text

    def review_item(
        self,
        artifact_id: int,
        *,
        kind: str,
        index: int,
        finding: str,
        note: str,
        material: bool = True,
        proposed_text: str | None = None,
    ) -> int:
        if kind not in _KINDS or finding not in _FINDINGS:
            raise ValueError("Unknown item kind or review finding")
        if type(index) is not int or index < 0:
            raise ValueError("Item index must be a nonnegative integer")
        normalized_note = _note(note)
        suggestion = proposed_text.strip() if proposed_text is not None else None
        if suggestion is not None and not 1 <= len(suggestion) <= 1000:
            raise ValueError("Proposed correction must contain 1–1000 characters")
        if suggestion is not None and finding == "supported":
            raise ValueError("A proposed correction is not an accepted original claim")
        if finding == "unsupported" and not material:
            raise ValueError("Unsupported employer-fact claims require material review")
        self.initialize()
        artifact = self._pending(artifact_id)
        items = artifact.analysis.get(kind)
        if not isinstance(items, list) or index >= len(items):
            raise ValueError("Review anchor does not match an original claim")
        item = items[index]
        if not isinstance(item, dict):
            raise ValueError("Review anchor is not a structured original claim")
        with self._connect() as connection:
            self._begin(connection, artifact)
            cursor = connection.execute(
                """INSERT INTO job_analysis_item_review_events(
                       artifact_id, kind, item_index, item_digest, finding, material,
                       note, source_excerpt, proposed_text, original_item_json, created_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    artifact_id, kind, index, _digest(item), finding,
                    int(material and finding != "supported"), normalized_note,
                    str(item.get("evidence") or ""), suggestion, _json(item),
                    datetime.now(UTC).isoformat(),
                ),
            )
            connection.execute(
                "UPDATE job_analysis_item_review_sessions SET completed_at = NULL, "
                "completion_note = NULL WHERE artifact_id = ?",
                (artifact_id,),
            )
            return int(cursor.lastrowid)

    def review_gap(
        self,
        artifact_id: int,
        *,
        source_excerpt: str,
        finding: str,
        note: str,
        material: bool = True,
        proposed_text: str | None = None,
    ) -> int:
        if finding not in _GAP_FINDINGS:
            raise ValueError("Unknown source-coverage finding")
        normalized_note = _note(note)
        if finding == "gap_open" and not material:
            # A trivial omission can be documented, but is not an acceptance blocker.
            pass
        if finding == "gap_dismissed" and proposed_text is not None:
            raise ValueError("Dismissing a gap cannot also add a claim")
        proposal = proposed_text.strip() if proposed_text is not None else None
        if proposal is not None and not 1 <= len(proposal) <= 1000:
            raise ValueError("Proposed addition must contain 1–1000 characters")
        self.initialize()
        artifact = self._pending(artifact_id)
        excerpt = self._source_excerpt(artifact, source_excerpt)
        with self._connect() as connection:
            self._begin(connection, artifact)
            cursor = connection.execute(
                """INSERT INTO job_analysis_item_review_events(
                       artifact_id, kind, item_index, item_digest, finding, material,
                       note, source_excerpt, proposed_text, original_item_json, created_at
                   ) VALUES (?, 'coverage_gap', NULL, ?, ?, ?, ?, ?, ?, NULL, ?)""",
                (
                    artifact_id, _digest(excerpt), finding,
                    int(material and finding == "gap_open"), normalized_note,
                    excerpt, proposal, datetime.now(UTC).isoformat(),
                ),
            )
            connection.execute(
                "UPDATE job_analysis_item_review_sessions SET completed_at = NULL, "
                "completion_note = NULL WHERE artifact_id = ?",
                (artifact_id,),
            )
            return int(cursor.lastrowid)

    def events(self, artifact_id: int) -> tuple[ItemReviewEvent, ...]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM job_analysis_item_review_events "
                "WHERE artifact_id = ? ORDER BY id", (artifact_id,),
            ).fetchall()
        return tuple(
            ItemReviewEvent(
                id=int(row["id"]), artifact_id=int(row["artifact_id"]),
                kind=str(row["kind"]),
                item_index=(int(row["item_index"]) if row["item_index"] is not None else None),
                item_digest=str(row["item_digest"]), finding=str(row["finding"]),
                material=bool(row["material"]), note=str(row["note"]),
                source_excerpt=(str(row["source_excerpt"])
                                if row["source_excerpt"] is not None else None),
                proposed_text=(str(row["proposed_text"])
                               if row["proposed_text"] is not None else None),
                original_item=(json.loads(str(row["original_item_json"]))
                               if row["original_item_json"] is not None else None),
                created_at=str(row["created_at"]),
            )
            for row in rows
        )

    def complete(self, artifact_id: int, *, note: str) -> None:
        """Finish only a fully enumerated review without unresolved material findings."""
        completion_note = _note(note)
        self.initialize()
        artifact = self._pending(artifact_id)
        with self._connect() as connection:
            started = connection.execute(
                "SELECT 1 FROM job_analysis_item_review_sessions WHERE artifact_id = ?",
                (artifact_id,),
            ).fetchone()
            if started is None:
                raise ValueError("Begin the item review before completing it")
            latest = connection.execute(
                """SELECT e.* FROM job_analysis_item_review_events e
                   WHERE e.artifact_id = ? AND e.id = (
                       SELECT MAX(previous.id) FROM job_analysis_item_review_events previous
                       WHERE previous.artifact_id = e.artifact_id
                         AND previous.kind = e.kind
                         AND previous.item_digest = e.item_digest
                         AND previous.item_index IS e.item_index
                   )""",
                (artifact_id,),
            ).fetchall()
            reviewed = {(str(row["kind"]), int(row["item_index"]),
                         str(row["item_digest"]))
                        for row in latest if row["kind"] != "coverage_gap"}
            for kind in ("role_purpose", "responsibilities", "requirements"):
                items = artifact.analysis.get(kind, [])
                if not isinstance(items, list):
                    raise ValueError("Original analysis has malformed reviewable items")
                for index, item in enumerate(items):
                    if (kind, index, _digest(item)) not in reviewed:
                        raise ValueError("Every original claim needs an explicit review finding")
            if any(bool(row["material"]) for row in latest):
                raise ValueError("Material item findings or source-coverage gaps remain unresolved")
            connection.execute(
                """UPDATE job_analysis_item_review_sessions
                   SET completed_at = ?, completion_note = ? WHERE artifact_id = ?""",
                (datetime.now(UTC).isoformat(), completion_note, artifact_id),
            )

    def is_complete(self, artifact_id: int) -> bool:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT completed_at FROM job_analysis_item_review_sessions WHERE artifact_id = ?",
                (artifact_id,),
            ).fetchone()
        return row is not None and row["completed_at"] is not None
