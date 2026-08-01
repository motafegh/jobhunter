"""Local-only user triage and deterministic acquisition priority for discovered jobs."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.storage import JobHunterStore

_TRIAGE_STATES = {
    "unreviewed",
    "interested",
    "review_later",
    "not_relevant",
    "reviewed",
}

_PACK_WEIGHTS = {
    "ai-security": 8,
    "defensive-security": 6,
    "ai-ml": 5,
    "llm-applications": 5,
    "python-data": 4,
    "network-platform": 3,
}
_TITLE_SIGNALS = {
    "security": 4,
    "امنیت": 4,
    "artificial intelligence": 4,
    "هوش مصنوعی": 4,
    "machine learning": 4,
    "یادگیری ماشین": 4,
    "python": 3,
    "پایتون": 3,
    "soc": 3,
    "detection": 3,
    "llm": 3,
    "rag": 2,
    "linux": 2,
    "لینوکس": 2,
}


@dataclass(frozen=True, slots=True)
class JobWorkflowState:
    source_job_id: str
    triage_state: str
    note: str | None
    updated_at: str | None


@dataclass(frozen=True, slots=True)
class JobPriority:
    source_job_id: str
    score: int
    distinct_searches: int
    distinct_packs: int
    signals: tuple[str, ...]


class JobWorkflowStore:
    """Persist human triage without mutating authoritative employer/source records."""

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
                CREATE TABLE IF NOT EXISTS job_user_workflow (
                    job_posting_id INTEGER PRIMARY KEY,
                    triage_state TEXT NOT NULL DEFAULT 'unreviewed' CHECK (
                        triage_state IN (
                            'unreviewed', 'interested', 'review_later',
                            'not_relevant', 'reviewed'
                        )
                    ),
                    note TEXT,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(job_posting_id) REFERENCES job_postings(id)
                );
                CREATE INDEX IF NOT EXISTS idx_job_user_workflow_state
                ON job_user_workflow(triage_state, updated_at DESC);
                """
            )

    def set_state(
        self,
        source_job_ids: tuple[str, ...],
        *,
        triage_state: str,
        note: str | None = None,
        updated_at: datetime | None = None,
    ) -> int:
        if triage_state not in _TRIAGE_STATES:
            raise ValueError(f"Unsupported triage state: {triage_state}")
        unique_ids = tuple(
            dict.fromkeys(
                job_id.strip() for job_id in source_job_ids if job_id.strip()
            )
        )
        if not unique_ids:
            raise ValueError("At least one job is required")
        if len(unique_ids) > 100:
            raise ValueError("At most 100 jobs may be updated at once")
        self.initialize()
        timestamp = (updated_at or datetime.now(UTC)).isoformat()
        changed = 0
        with self._connect() as connection:
            for source_job_id in unique_ids:
                row = connection.execute(
                    """
                    SELECT id
                    FROM job_postings
                    WHERE source = 'jobinja' AND source_job_id = ?
                    """,
                    (source_job_id,),
                ).fetchone()
                if row is None:
                    continue
                connection.execute(
                    """
                    INSERT INTO job_user_workflow(
                        job_posting_id, triage_state, note, updated_at
                    ) VALUES (?, ?, ?, ?)
                    ON CONFLICT(job_posting_id) DO UPDATE SET
                        triage_state = excluded.triage_state,
                        note = COALESCE(excluded.note, job_user_workflow.note),
                        updated_at = excluded.updated_at
                    """,
                    (int(row["id"]), triage_state, note, timestamp),
                )
                changed += 1
        return changed

    def get_state(self, source_job_id: str) -> JobWorkflowState:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT p.source_job_id, w.triage_state, w.note, w.updated_at
                FROM job_postings AS p
                LEFT JOIN job_user_workflow AS w ON w.job_posting_id = p.id
                WHERE p.source = 'jobinja' AND p.source_job_id = ?
                """,
                (source_job_id,),
            ).fetchone()
        if row is None:
            raise LookupError(f"Unknown Jobinja job {source_job_id!r}")
        return JobWorkflowState(
            source_job_id=str(row["source_job_id"]),
            triage_state=str(row["triage_state"] or "unreviewed"),
            note=str(row["note"]) if row["note"] is not None else None,
            updated_at=(
                str(row["updated_at"]) if row["updated_at"] is not None else None
            ),
        )

    def prioritized_missing_job_ids(self, *, limit: int) -> tuple[JobPriority, ...]:
        """Rank missing-detail postings from existing discovery evidence only."""

        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50")
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.id,
                    p.source_job_id,
                    COALESCE(p.title_observed, '') AS title_observed,
                    COALESCE(w.triage_state, 'unreviewed') AS triage_state,
                    COUNT(DISTINCT d.search_name) AS distinct_searches,
                    GROUP_CONCAT(DISTINCT d.search_name) AS search_names
                FROM job_postings AS p
                LEFT JOIN job_user_workflow AS w ON w.job_posting_id = p.id
                LEFT JOIN job_discoveries AS d ON d.job_posting_id = p.id
                WHERE p.source = 'jobinja'
                  AND COALESCE(w.triage_state, 'unreviewed') != 'not_relevant'
                  AND NOT EXISTS (
                      SELECT 1 FROM job_detail_versions AS v
                      WHERE v.job_posting_id = p.id
                  )
                GROUP BY p.id
                """
            ).fetchall()

        priorities: list[JobPriority] = []
        for row in rows:
            raw_names = str(row["search_names"] or "")
            search_names = tuple(name for name in raw_names.split(",") if name)
            packs: set[str] = set()
            signals: list[str] = []
            score = min(int(row["distinct_searches"] or 0), 10)
            for name in search_names:
                if not name.startswith("pack:"):
                    continue
                prefix = name.split(" :: ", 1)[0]
                pack = prefix.removeprefix("pack:")
                packs.add(pack)
            for pack in sorted(packs):
                weight = _PACK_WEIGHTS.get(pack, 1)
                score += weight
                signals.append(f"{pack} +{weight}")
            title = str(row["title_observed"] or "").casefold()
            for needle, weight in _TITLE_SIGNALS.items():
                if needle.casefold() in title:
                    score += weight
                    signals.append(f"title:{needle} +{weight}")
            priorities.append(
                JobPriority(
                    source_job_id=str(row["source_job_id"]),
                    score=score,
                    distinct_searches=int(row["distinct_searches"] or 0),
                    distinct_packs=len(packs),
                    signals=tuple(signals),
                )
            )
        priorities.sort(
            key=lambda item: (
                -item.score,
                -item.distinct_packs,
                item.source_job_id,
            )
        )
        return tuple(priorities[:limit])
