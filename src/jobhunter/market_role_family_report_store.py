"""Persistence for durable Market role-family intelligence reports.

The persisted report is an immutable analytical artifact over one exact Market
snapshot. Persistence and human review do not promote generated role families
or subfamilies into canonical taxonomy.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.market_models import (
    ROLE_FAMILY_REPORT_CONTRACT_VERSION,
    ROLE_FAMILY_REPORT_REVIEW_CONTRACT_VERSION,
    MarketRoleFamilyIntelligenceReport,
    MarketRoleFamilyReportAttempt,
    MarketRoleFamilyReportAttemptOutcome,
    MarketRoleFamilyReportReview,
    MarketRoleFamilyReportReviewDisposition,
)
from jobhunter.market_store import MarketStore


class MarketRoleFamilyReportStoreError(ValueError):
    """Raised when a role-family report persistence invariant is violated."""


def canonical_json(value: Any) -> str:
    """Return the stable JSON representation used for report fingerprints."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def role_family_input_fingerprint(candidate_input: dict[str, Any]) -> str:
    return canonical_json_sha256(candidate_input)


def role_family_generation_fingerprint(
    *,
    input_fingerprint: str,
    report_contract_version: str,
    candidate_contract_version: str,
    prompt_version: str,
    model: str,
    generation_identity: dict[str, Any],
) -> str:
    return canonical_json_sha256(
        {
            "input_fingerprint": _required_text(
                input_fingerprint,
                name="input_fingerprint",
            ),
            "report_contract_version": _required_text(
                report_contract_version,
                name="report_contract_version",
            ),
            "candidate_contract_version": _required_text(
                candidate_contract_version,
                name="candidate_contract_version",
            ),
            "prompt_version": _required_text(
                prompt_version,
                name="prompt_version",
            ),
            "model": _required_text(model, name="model"),
            "generation_identity": _normalized_generation_identity(
                generation_identity,
                model=model,
            ),
        }
    )


def role_family_report_sha256(report: dict[str, Any]) -> str:
    return canonical_json_sha256(report)


def _required_text(value: str, *, name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise MarketRoleFamilyReportStoreError(f"{name} must not be empty")
    return cleaned


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _positive_int(value: Any, *, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise MarketRoleFamilyReportStoreError(
            f"generation_identity.{name} must be a positive integer"
        )
    return value


def _normalized_generation_identity(
    value: dict[str, Any],
    *,
    model: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MarketRoleFamilyReportStoreError(
            "generation_identity must be an object"
        )
    normalized = json.loads(canonical_json(value))
    provider = normalized.get("provider")
    identity_model = normalized.get("model")
    structured_schema = normalized.get("structured_schema")
    seed = normalized.get("seed")

    if not isinstance(provider, str) or not provider.strip():
        raise MarketRoleFamilyReportStoreError(
            "generation_identity.provider must not be empty"
        )
    if not isinstance(identity_model, str) or identity_model.strip() != model.strip():
        raise MarketRoleFamilyReportStoreError(
            "generation_identity.model must match model"
        )
    if not isinstance(structured_schema, str) or not structured_schema.strip():
        raise MarketRoleFamilyReportStoreError(
            "generation_identity.structured_schema must not be empty"
        )
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise MarketRoleFamilyReportStoreError(
            "generation_identity.seed must be an integer"
        )
    _positive_int(normalized.get("context_length"), name="context_length")
    _positive_int(normalized.get("max_tokens"), name="max_tokens")
    return normalized


def _generation_payload(
    *,
    candidate_input: dict[str, Any],
    report_contract_version: str,
    candidate_contract_version: str,
    prompt_version: str,
    model: str,
    generation_identity: dict[str, Any],
) -> tuple[str, str, dict[str, Any]]:
    if not isinstance(candidate_input, dict):
        raise MarketRoleFamilyReportStoreError("candidate_input must be an object")
    contract = _required_text(
        report_contract_version,
        name="report_contract_version",
    )
    candidate_contract = _required_text(
        candidate_contract_version,
        name="candidate_contract_version",
    )
    prompt = _required_text(prompt_version, name="prompt_version")
    model_name = _required_text(model, name="model")
    identity = _normalized_generation_identity(
        generation_identity,
        model=model_name,
    )
    input_fingerprint = role_family_input_fingerprint(candidate_input)
    generation_fingerprint = role_family_generation_fingerprint(
        input_fingerprint=input_fingerprint,
        report_contract_version=contract,
        candidate_contract_version=candidate_contract,
        prompt_version=prompt,
        model=model_name,
        generation_identity=identity,
    )
    return input_fingerprint, generation_fingerprint, identity


class MarketRoleFamilyReportStore:
    """Own durable local history for bounded role-family report artifacts."""

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
        MarketStore(self._database_path).initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS market_role_family_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    report_contract_version TEXT NOT NULL,
                    candidate_contract_version TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    model TEXT NOT NULL,
                    generation_identity_json TEXT NOT NULL,
                    input_fingerprint TEXT NOT NULL,
                    generation_fingerprint TEXT NOT NULL,
                    report_sha256 TEXT NOT NULL,
                    report_json TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    raw_response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(snapshot_id) REFERENCES market_corpus_snapshots(id)
                );

                CREATE INDEX IF NOT EXISTS idx_role_family_reports_snapshot
                ON market_role_family_reports(snapshot_id, id DESC);

                CREATE INDEX IF NOT EXISTS idx_role_family_reports_generation
                ON market_role_family_reports(
                    snapshot_id,
                    generation_fingerprint,
                    id DESC
                );

                CREATE TABLE IF NOT EXISTS market_role_family_report_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    attempted_at TEXT NOT NULL,
                    report_contract_version TEXT NOT NULL,
                    candidate_contract_version TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    model TEXT NOT NULL,
                    generation_identity_json TEXT NOT NULL,
                    input_fingerprint TEXT NOT NULL,
                    generation_fingerprint TEXT NOT NULL,
                    outcome TEXT NOT NULL CHECK(
                        outcome IN ('completed', 'failed', 'reused')
                    ),
                    artifact_id INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    FOREIGN KEY(snapshot_id) REFERENCES market_corpus_snapshots(id),
                    FOREIGN KEY(artifact_id) REFERENCES market_role_family_reports(id),
                    CHECK(
                        (outcome IN ('completed', 'reused') AND artifact_id IS NOT NULL)
                        OR
                        (outcome = 'failed' AND artifact_id IS NULL)
                    )
                );

                CREATE INDEX IF NOT EXISTS idx_role_family_attempts_snapshot
                ON market_role_family_report_attempts(
                    snapshot_id,
                    attempted_at DESC,
                    id DESC
                );

                CREATE TABLE IF NOT EXISTS market_role_family_report_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_artifact_id INTEGER NOT NULL,
                    review_contract_version TEXT NOT NULL,
                    disposition TEXT NOT NULL CHECK(
                        disposition IN ('accepted_for_bounded_use', 'rejected')
                    ),
                    note TEXT,
                    reviewed_at TEXT NOT NULL,
                    FOREIGN KEY(report_artifact_id)
                        REFERENCES market_role_family_reports(id)
                );

                CREATE INDEX IF NOT EXISTS idx_role_family_reviews_report
                ON market_role_family_report_reviews(
                    report_artifact_id,
                    id DESC
                );

                CREATE TRIGGER IF NOT EXISTS market_role_family_reports_immutable_update
                BEFORE UPDATE ON market_role_family_reports
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family reports are immutable'
                    );
                END;

                CREATE TRIGGER IF NOT EXISTS market_role_family_reports_immutable_delete
                BEFORE DELETE ON market_role_family_reports
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family reports are immutable'
                    );
                END;

                CREATE TRIGGER IF NOT EXISTS market_role_family_attempts_immutable_update
                BEFORE UPDATE ON market_role_family_report_attempts
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family report attempts are immutable'
                    );
                END;

                CREATE TRIGGER IF NOT EXISTS market_role_family_attempts_immutable_delete
                BEFORE DELETE ON market_role_family_report_attempts
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family report attempts are immutable'
                    );
                END;

                CREATE TRIGGER IF NOT EXISTS market_role_family_reviews_immutable_update
                BEFORE UPDATE ON market_role_family_report_reviews
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family report reviews are immutable'
                    );
                END;

                CREATE TRIGGER IF NOT EXISTS market_role_family_reviews_immutable_delete
                BEFORE DELETE ON market_role_family_report_reviews
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Market role-family report reviews are immutable'
                    );
                END;
                """
            )

    def record_report(
        self,
        *,
        snapshot_id: int,
        candidate_contract_version: str,
        prompt_version: str,
        model: str,
        generation_identity: dict[str, Any],
        candidate_input: dict[str, Any],
        report: dict[str, Any],
        request_body: dict[str, Any],
        raw_response: dict[str, Any],
        created_at: datetime,
        report_contract_version: str = ROLE_FAMILY_REPORT_CONTRACT_VERSION,
    ) -> MarketRoleFamilyIntelligenceReport:
        self._require_snapshot(snapshot_id)
        if not isinstance(report, dict):
            raise MarketRoleFamilyReportStoreError("report must be an object")
        if not isinstance(request_body, dict):
            raise MarketRoleFamilyReportStoreError("request_body must be an object")
        if not isinstance(raw_response, dict):
            raise MarketRoleFamilyReportStoreError("raw_response must be an object")

        input_fingerprint, generation_fingerprint, identity = _generation_payload(
            candidate_input=candidate_input,
            report_contract_version=report_contract_version,
            candidate_contract_version=candidate_contract_version,
            prompt_version=prompt_version,
            model=model,
            generation_identity=generation_identity,
        )
        report_json = canonical_json(report)
        report_hash = hashlib.sha256(report_json.encode("utf-8")).hexdigest()

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO market_role_family_reports(
                    snapshot_id,
                    report_contract_version,
                    candidate_contract_version,
                    prompt_version,
                    model,
                    generation_identity_json,
                    input_fingerprint,
                    generation_fingerprint,
                    report_sha256,
                    report_json,
                    request_json,
                    raw_response_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    _required_text(
                        report_contract_version,
                        name="report_contract_version",
                    ),
                    _required_text(
                        candidate_contract_version,
                        name="candidate_contract_version",
                    ),
                    _required_text(prompt_version, name="prompt_version"),
                    _required_text(model, name="model"),
                    canonical_json(identity),
                    input_fingerprint,
                    generation_fingerprint,
                    report_hash,
                    report_json,
                    canonical_json(request_body),
                    canonical_json(raw_response),
                    created_at.isoformat(),
                ),
            )
            artifact_id = int(cursor.lastrowid)
        return self._require_report(artifact_id)

    def find_reusable_report(
        self,
        *,
        snapshot_id: int,
        candidate_contract_version: str,
        prompt_version: str,
        model: str,
        generation_identity: dict[str, Any],
        candidate_input: dict[str, Any],
        report_contract_version: str = ROLE_FAMILY_REPORT_CONTRACT_VERSION,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        self._require_snapshot(snapshot_id)
        _input, generation_fingerprint, _identity = _generation_payload(
            candidate_input=candidate_input,
            report_contract_version=report_contract_version,
            candidate_contract_version=candidate_contract_version,
            prompt_version=prompt_version,
            model=model,
            generation_identity=generation_identity,
        )
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM market_role_family_reports
                WHERE snapshot_id = ? AND generation_fingerprint = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (snapshot_id, generation_fingerprint),
            ).fetchone()
        return _report(row) if row else None

    def get_report(
        self,
        artifact_id: int,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_role_family_reports WHERE id = ?",
                (artifact_id,),
            ).fetchone()
        return _report(row) if row else None

    def list_reports(
        self,
        snapshot_id: int,
    ) -> tuple[MarketRoleFamilyIntelligenceReport, ...]:
        self._require_snapshot(snapshot_id)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM market_role_family_reports
                WHERE snapshot_id = ?
                ORDER BY id DESC
                """,
                (snapshot_id,),
            ).fetchall()
        return tuple(_report(row) for row in rows)

    def record_attempt(
        self,
        *,
        snapshot_id: int,
        attempted_at: datetime,
        candidate_contract_version: str,
        prompt_version: str,
        model: str,
        generation_identity: dict[str, Any],
        candidate_input: dict[str, Any],
        outcome: MarketRoleFamilyReportAttemptOutcome | str,
        artifact_id: int | None = None,
        error: Exception | None = None,
        report_contract_version: str = ROLE_FAMILY_REPORT_CONTRACT_VERSION,
    ) -> MarketRoleFamilyReportAttempt:
        self._require_snapshot(snapshot_id)
        outcome = MarketRoleFamilyReportAttemptOutcome(outcome)
        input_fingerprint, generation_fingerprint, identity = _generation_payload(
            candidate_input=candidate_input,
            report_contract_version=report_contract_version,
            candidate_contract_version=candidate_contract_version,
            prompt_version=prompt_version,
            model=model,
            generation_identity=generation_identity,
        )

        if outcome in {
            MarketRoleFamilyReportAttemptOutcome.COMPLETED,
            MarketRoleFamilyReportAttemptOutcome.REUSED,
        }:
            if artifact_id is None:
                raise MarketRoleFamilyReportStoreError(
                    f"{outcome.value} attempt requires an artifact"
                )
            artifact = self._require_report(artifact_id)
            if artifact.snapshot_id != snapshot_id:
                raise MarketRoleFamilyReportStoreError(
                    "Attempt artifact belongs to a different snapshot"
                )
            if artifact.generation_fingerprint != generation_fingerprint:
                raise MarketRoleFamilyReportStoreError(
                    "Attempt artifact generation identity does not match the attempt"
                )
            if error is not None:
                raise MarketRoleFamilyReportStoreError(
                    f"{outcome.value} attempt must not include an error"
                )
        else:
            if artifact_id is not None:
                raise MarketRoleFamilyReportStoreError(
                    "failed attempt must not reference an artifact"
                )

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO market_role_family_report_attempts(
                    snapshot_id,
                    attempted_at,
                    report_contract_version,
                    candidate_contract_version,
                    prompt_version,
                    model,
                    generation_identity_json,
                    input_fingerprint,
                    generation_fingerprint,
                    outcome,
                    artifact_id,
                    error_type,
                    error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    attempted_at.isoformat(),
                    _required_text(
                        report_contract_version,
                        name="report_contract_version",
                    ),
                    _required_text(
                        candidate_contract_version,
                        name="candidate_contract_version",
                    ),
                    _required_text(prompt_version, name="prompt_version"),
                    _required_text(model, name="model"),
                    canonical_json(identity),
                    input_fingerprint,
                    generation_fingerprint,
                    outcome.value,
                    artifact_id,
                    type(error).__name__ if error is not None else None,
                    str(error) if error is not None else None,
                ),
            )
            attempt_id = int(cursor.lastrowid)
        return self._require_attempt(attempt_id)

    def list_attempts(
        self,
        snapshot_id: int,
    ) -> tuple[MarketRoleFamilyReportAttempt, ...]:
        self._require_snapshot(snapshot_id)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM market_role_family_report_attempts
                WHERE snapshot_id = ?
                ORDER BY id ASC
                """,
                (snapshot_id,),
            ).fetchall()
        return tuple(_attempt(row) for row in rows)

    def record_review(
        self,
        *,
        report_artifact_id: int,
        disposition: MarketRoleFamilyReportReviewDisposition | str,
        reviewed_at: datetime,
        note: str | None = None,
        review_contract_version: str = ROLE_FAMILY_REPORT_REVIEW_CONTRACT_VERSION,
    ) -> MarketRoleFamilyReportReview:
        self._require_report(report_artifact_id)
        disposition = MarketRoleFamilyReportReviewDisposition(disposition)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO market_role_family_report_reviews(
                    report_artifact_id,
                    review_contract_version,
                    disposition,
                    note,
                    reviewed_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    report_artifact_id,
                    _required_text(
                        review_contract_version,
                        name="review_contract_version",
                    ),
                    disposition.value,
                    _optional_text(note),
                    reviewed_at.isoformat(),
                ),
            )
            review_id = int(cursor.lastrowid)
        return self._require_review(review_id)

    def list_reviews(
        self,
        report_artifact_id: int,
    ) -> tuple[MarketRoleFamilyReportReview, ...]:
        self._require_report(report_artifact_id)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM market_role_family_report_reviews
                WHERE report_artifact_id = ?
                ORDER BY id ASC
                """,
                (report_artifact_id,),
            ).fetchall()
        return tuple(_review(row) for row in rows)

    def effective_review(
        self,
        report_artifact_id: int,
    ) -> MarketRoleFamilyReportReview | None:
        self._require_report(report_artifact_id)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM market_role_family_report_reviews
                WHERE report_artifact_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (report_artifact_id,),
            ).fetchone()
        return _review(row) if row else None

    def effective_review_state(self, report_artifact_id: int) -> str:
        review = self.effective_review(report_artifact_id)
        return review.disposition if review is not None else "pending"

    def latest_accepted_for_snapshot(
        self,
        snapshot_id: int,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        self._require_snapshot(snapshot_id)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT r.*
                FROM market_role_family_reports AS r
                WHERE r.snapshot_id = ?
                  AND (
                      SELECT disposition
                      FROM market_role_family_report_reviews AS rv
                      WHERE rv.report_artifact_id = r.id
                      ORDER BY rv.id DESC
                      LIMIT 1
                  ) = 'accepted_for_bounded_use'
                ORDER BY r.id DESC
                LIMIT 1
                """,
                (snapshot_id,),
            ).fetchone()
        return _report(row) if row else None

    def _require_snapshot(self, snapshot_id: int) -> None:
        if snapshot_id <= 0:
            raise LookupError(f"Unknown Market snapshot {snapshot_id}")
        snapshot = MarketStore(self._database_path).get_snapshot(snapshot_id)
        if snapshot is None:
            raise LookupError(f"Unknown Market snapshot {snapshot_id}")
        self.initialize()

    def _require_report(
        self,
        artifact_id: int,
    ) -> MarketRoleFamilyIntelligenceReport:
        report = self.get_report(artifact_id)
        if report is None:
            raise LookupError(f"Unknown Market role-family report {artifact_id}")
        return report

    def _require_attempt(self, attempt_id: int) -> MarketRoleFamilyReportAttempt:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_role_family_report_attempts WHERE id = ?",
                (attempt_id,),
            ).fetchone()
        if row is None:
            raise LookupError(f"Unknown Market role-family report attempt {attempt_id}")
        return _attempt(row)

    def _require_review(self, review_id: int) -> MarketRoleFamilyReportReview:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_role_family_report_reviews WHERE id = ?",
                (review_id,),
            ).fetchone()
        if row is None:
            raise LookupError(f"Unknown Market role-family report review {review_id}")
        return _review(row)


def _report(row: sqlite3.Row) -> MarketRoleFamilyIntelligenceReport:
    identity = json.loads(str(row["generation_identity_json"]))
    report = json.loads(str(row["report_json"]))
    expected_generation = role_family_generation_fingerprint(
        input_fingerprint=str(row["input_fingerprint"]),
        report_contract_version=str(row["report_contract_version"]),
        candidate_contract_version=str(row["candidate_contract_version"]),
        prompt_version=str(row["prompt_version"]),
        model=str(row["model"]),
        generation_identity=identity,
    )
    if expected_generation != str(row["generation_fingerprint"]):
        raise MarketRoleFamilyReportStoreError(
            "Persisted role-family generation fingerprint is corrupt"
        )
    if role_family_report_sha256(report) != str(row["report_sha256"]):
        raise MarketRoleFamilyReportStoreError(
            "Persisted role-family report fingerprint is corrupt"
        )
    return MarketRoleFamilyIntelligenceReport(
        id=int(row["id"]),
        snapshot_id=int(row["snapshot_id"]),
        report_contract_version=str(row["report_contract_version"]),
        candidate_contract_version=str(row["candidate_contract_version"]),
        prompt_version=str(row["prompt_version"]),
        model=str(row["model"]),
        generation_identity=identity,
        input_fingerprint=str(row["input_fingerprint"]),
        generation_fingerprint=str(row["generation_fingerprint"]),
        report_sha256=str(row["report_sha256"]),
        report=report,
        request_body=json.loads(str(row["request_json"])),
        raw_response=json.loads(str(row["raw_response_json"])),
        created_at=str(row["created_at"]),
    )


def _attempt(row: sqlite3.Row) -> MarketRoleFamilyReportAttempt:
    artifact_id = row["artifact_id"]
    return MarketRoleFamilyReportAttempt(
        id=int(row["id"]),
        snapshot_id=int(row["snapshot_id"]),
        attempted_at=str(row["attempted_at"]),
        report_contract_version=str(row["report_contract_version"]),
        candidate_contract_version=str(row["candidate_contract_version"]),
        prompt_version=str(row["prompt_version"]),
        model=str(row["model"]),
        generation_identity=json.loads(str(row["generation_identity_json"])),
        input_fingerprint=str(row["input_fingerprint"]),
        generation_fingerprint=str(row["generation_fingerprint"]),
        outcome=str(row["outcome"]),
        artifact_id=int(artifact_id) if artifact_id is not None else None,
        error_type=str(row["error_type"]) if row["error_type"] is not None else None,
        error_message=(
            str(row["error_message"]) if row["error_message"] is not None else None
        ),
    )


def _review(row: sqlite3.Row) -> MarketRoleFamilyReportReview:
    return MarketRoleFamilyReportReview(
        id=int(row["id"]),
        report_artifact_id=int(row["report_artifact_id"]),
        review_contract_version=str(row["review_contract_version"]),
        disposition=str(row["disposition"]),
        note=str(row["note"]) if row["note"] is not None else None,
        reviewed_at=str(row["reviewed_at"]),
    )


__all__ = [
    "MarketRoleFamilyReportStore",
    "MarketRoleFamilyReportStoreError",
    "canonical_json",
    "canonical_json_sha256",
    "role_family_generation_fingerprint",
    "role_family_input_fingerprint",
    "role_family_report_sha256",
]
