"""SQLite persistence for the first target-scoped Market Intelligence slice."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.market_models import (
    MARKET_AGGREGATE_CONTRACT_VERSION,
    MARKET_SNAPSHOT_CONTRACT_VERSION,
    MarketAggregateProfile,
    MarketCorpusSnapshot,
    MarketCorpusSnapshotMember,
    MarketDefinitionSpec,
    MarketJobMembership,
    MarketMembershipDisposition,
    MarketResearchRun,
    MarketRunStatus,
    MarketSnapshotMemberInput,
    P16CoverageStatus,
    TargetMarket,
    TargetMarketDefinitionVersion,
)

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TERMINAL_RUN_STATUSES = {
    MarketRunStatus.COMPLETED,
    MarketRunStatus.COMPLETED_WITH_FAILURES,
    MarketRunStatus.FAILED,
}


class MarketStoreError(ValueError):
    """Raised when a Market persistence invariant would be violated."""


def _json_text(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _json_sha256(value: Any) -> str:
    return hashlib.sha256(_json_text(value).encode("utf-8")).hexdigest()


def _required_text(value: str, *, name: str) -> str:
    value = value.strip()
    if not value:
        raise MarketStoreError(f"{name} must not be empty")
    return value


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _normalized_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    cleaned = {
        value.strip()
        for value in values
        if isinstance(value, str) and value.strip()
    }
    return tuple(sorted(cleaned, key=str.casefold))


def _definition_payload(spec: MarketDefinitionSpec) -> dict[str, Any]:
    source = _required_text(spec.source, name="source")
    if source != "jobinja":
        raise MarketStoreError("The first Market slice supports only Jobinja")
    raw_searches = []
    for item in spec.raw_searches:
        if not isinstance(item, dict):
            raise MarketStoreError("raw_searches entries must be objects")
        raw_searches.append(json.loads(_json_text(item)))
    raw_searches.sort(key=_json_text)
    return {
        "membership_intent": _required_text(
            spec.membership_intent,
            name="membership_intent",
        ),
        "search_catalog_version": _required_text(
            spec.search_catalog_version,
            name="search_catalog_version",
        ),
        "source": source,
        "search_profiles": _normalized_strings(spec.search_profiles),
        "search_packs": _normalized_strings(spec.search_packs),
        "extra_search_terms": _normalized_strings(spec.extra_search_terms),
        "raw_searches": raw_searches,
        "include_hints": _normalized_strings(spec.include_hints),
        "exclude_hints": _normalized_strings(spec.exclude_hints),
        "geography_scope": _optional_text(spec.geography_scope),
        "work_arrangement_scope": _optional_text(spec.work_arrangement_scope),
        "seniority_scope": _optional_text(spec.seniority_scope),
        "employment_type_scope": _optional_text(spec.employment_type_scope),
        "freshness_rule": _required_text(spec.freshness_rule, name="freshness_rule"),
    }


def _spec_from_payload(payload: dict[str, Any]) -> MarketDefinitionSpec:
    return MarketDefinitionSpec(
        membership_intent=str(payload["membership_intent"]),
        search_catalog_version=str(payload["search_catalog_version"]),
        source=str(payload["source"]),
        search_profiles=tuple(payload.get("search_profiles", ())),
        search_packs=tuple(payload.get("search_packs", ())),
        extra_search_terms=tuple(payload.get("extra_search_terms", ())),
        raw_searches=tuple(payload.get("raw_searches", ())),
        include_hints=tuple(payload.get("include_hints", ())),
        exclude_hints=tuple(payload.get("exclude_hints", ())),
        geography_scope=payload.get("geography_scope"),
        work_arrangement_scope=payload.get("work_arrangement_scope"),
        seniority_scope=payload.get("seniority_scope"),
        employment_type_scope=payload.get("employment_type_scope"),
        freshness_rule=str(payload["freshness_rule"]),
    )


class MarketStore:
    """Own the local/history persistence boundary for Market I1."""

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
                CREATE TABLE IF NOT EXISTS market_targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS market_target_definition_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_market_id INTEGER NOT NULL,
                    version_number INTEGER NOT NULL CHECK(version_number >= 1),
                    definition_fingerprint TEXT NOT NULL,
                    definition_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(target_market_id) REFERENCES market_targets(id),
                    UNIQUE(target_market_id, version_number),
                    UNIQUE(target_market_id, definition_fingerprint)
                );

                CREATE TABLE IF NOT EXISTS market_research_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_definition_version_id INTEGER NOT NULL,
                    status TEXT NOT NULL CHECK(
                        status IN (
                            'running',
                            'completed',
                            'completed_with_failures',
                            'failed'
                        )
                    ),
                    controls_json TEXT NOT NULL,
                    ledger_json TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    error_summary TEXT,
                    FOREIGN KEY(target_definition_version_id)
                        REFERENCES market_target_definition_versions(id)
                );

                CREATE TABLE IF NOT EXISTS market_job_memberships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_definition_version_id INTEGER NOT NULL,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER,
                    analysis_artifact_id INTEGER,
                    classifier_contract_version TEXT NOT NULL,
                    classifier_method TEXT NOT NULL,
                    classifier_identity_json TEXT NOT NULL,
                    dependency_fingerprint TEXT NOT NULL,
                    membership_fingerprint TEXT NOT NULL UNIQUE,
                    disposition TEXT NOT NULL CHECK(
                        disposition IN (
                            'core_match',
                            'adjacent_match',
                            'uncertain',
                            'excluded'
                        )
                    ),
                    reason TEXT NOT NULL,
                    evidence_refs_json TEXT NOT NULL,
                    confidence TEXT,
                    supersedes_membership_id INTEGER,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(target_definition_version_id)
                        REFERENCES market_target_definition_versions(id),
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id)
                        REFERENCES job_translation_artifacts(id),
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    FOREIGN KEY(supersedes_membership_id)
                        REFERENCES market_job_memberships(id)
                );

                CREATE INDEX IF NOT EXISTS idx_market_membership_dependency
                ON market_job_memberships(
                    target_definition_version_id,
                    job_detail_version_id,
                    dependency_fingerprint,
                    id DESC
                );

                CREATE TABLE IF NOT EXISTS market_corpus_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_definition_version_id INTEGER NOT NULL,
                    run_id INTEGER NOT NULL,
                    snapshot_contract_version TEXT NOT NULL,
                    freshness_rule TEXT NOT NULL,
                    source_scope_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(target_definition_version_id)
                        REFERENCES market_target_definition_versions(id),
                    FOREIGN KEY(run_id) REFERENCES market_research_runs(id),
                    UNIQUE(run_id, snapshot_contract_version)
                );

                CREATE TABLE IF NOT EXISTS market_corpus_snapshot_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    membership_id INTEGER NOT NULL,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER,
                    analysis_artifact_id INTEGER,
                    disposition TEXT NOT NULL CHECK(
                        disposition IN (
                            'core_match',
                            'adjacent_match',
                            'uncertain',
                            'excluded'
                        )
                    ),
                    semantic_coverage_status TEXT NOT NULL CHECK(
                        semantic_coverage_status IN (
                            'accepted',
                            'pending',
                            'missing',
                            'failed',
                            'rejected'
                        )
                    ),
                    included_in_primary_corpus INTEGER NOT NULL CHECK(
                        included_in_primary_corpus IN (0, 1)
                    ),
                    state_json TEXT NOT NULL,
                    FOREIGN KEY(snapshot_id) REFERENCES market_corpus_snapshots(id),
                    FOREIGN KEY(membership_id) REFERENCES market_job_memberships(id),
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id)
                        REFERENCES job_translation_artifacts(id),
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    UNIQUE(snapshot_id, job_detail_version_id),
                    UNIQUE(snapshot_id, membership_id)
                );

                CREATE INDEX IF NOT EXISTS idx_market_snapshot_members
                ON market_corpus_snapshot_members(snapshot_id, disposition, id);

                CREATE TABLE IF NOT EXISTS market_aggregate_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    aggregate_contract_version TEXT NOT NULL,
                    profile_sha256 TEXT NOT NULL,
                    profile_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(snapshot_id) REFERENCES market_corpus_snapshots(id),
                    UNIQUE(snapshot_id, aggregate_contract_version)
                );
                """
            )
            for table, label in (
                ("market_target_definition_versions", "target definitions"),
                ("market_job_memberships", "job memberships"),
                ("market_corpus_snapshots", "corpus snapshots"),
                ("market_corpus_snapshot_members", "snapshot members"),
                ("market_aggregate_profiles", "aggregate profiles"),
            ):
                connection.executescript(
                    f"""
                    CREATE TRIGGER IF NOT EXISTS {table}_immutable_update
                    BEFORE UPDATE ON {table}
                    BEGIN
                        SELECT RAISE(ABORT, 'Market {label} are immutable');
                    END;

                    CREATE TRIGGER IF NOT EXISTS {table}_immutable_delete
                    BEFORE DELETE ON {table}
                    BEGIN
                        SELECT RAISE(ABORT, 'Market {label} are immutable');
                    END;
                    """
                )

    def create_target(
        self,
        *,
        slug: str,
        name: str,
        description: str | None,
        created_at: datetime,
    ) -> TargetMarket:
        slug = slug.strip()
        if not _SLUG_RE.fullmatch(slug):
            raise MarketStoreError("slug must be lowercase kebab-case")
        name = _required_text(name, name="name")
        description = _optional_text(description)
        self.initialize()
        existing = self.get_target_by_slug(slug)
        if existing is not None:
            if existing.name == name and existing.description == description:
                return existing
            raise MarketStoreError(
                "Target slug already exists; use update_target for display changes"
            )
        stamp = created_at.isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO market_targets(
                    slug, name, description, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (slug, name, description, stamp, stamp),
            )
            target_id = int(cursor.lastrowid)
        return self._require_target(target_id)

    def update_target(
        self,
        target_id: int,
        *,
        name: str,
        description: str | None,
        updated_at: datetime,
    ) -> TargetMarket:
        self._require_target(target_id)
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE market_targets
                SET name = ?, description = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    _required_text(name, name="name"),
                    _optional_text(description),
                    updated_at.isoformat(),
                    target_id,
                ),
            )
        return self._require_target(target_id)

    def get_target(self, target_id: int) -> TargetMarket | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_targets WHERE id = ?",
                (target_id,),
            ).fetchone()
        return _target(row) if row else None

    def get_target_by_slug(self, slug: str) -> TargetMarket | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_targets WHERE slug = ?",
                (slug.strip(),),
            ).fetchone()
        return _target(row) if row else None

    def create_definition_version(
        self,
        target_market_id: int,
        *,
        spec: MarketDefinitionSpec,
        created_at: datetime,
    ) -> TargetMarketDefinitionVersion:
        self._require_target(target_market_id)
        payload = _definition_payload(spec)
        fingerprint = _json_sha256(payload)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM market_target_definition_versions
                WHERE target_market_id = ? AND definition_fingerprint = ?
                """,
                (target_market_id, fingerprint),
            ).fetchone()
            if row:
                return _definition(row)
            version = int(
                connection.execute(
                    """
                    SELECT COALESCE(MAX(version_number), 0) + 1 AS value
                    FROM market_target_definition_versions
                    WHERE target_market_id = ?
                    """,
                    (target_market_id,),
                ).fetchone()["value"]
            )
            cursor = connection.execute(
                """
                INSERT INTO market_target_definition_versions(
                    target_market_id,
                    version_number,
                    definition_fingerprint,
                    definition_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    target_market_id,
                    version,
                    fingerprint,
                    _json_text(payload),
                    created_at.isoformat(),
                ),
            )
            definition_id = int(cursor.lastrowid)
        return self._require_definition(definition_id)

    def get_definition_version(
        self,
        definition_version_id: int,
    ) -> TargetMarketDefinitionVersion | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_target_definition_versions WHERE id = ?",
                (definition_version_id,),
            ).fetchone()
        return _definition(row) if row else None

    def start_run(
        self,
        target_definition_version_id: int,
        *,
        controls: dict[str, Any],
        started_at: datetime,
    ) -> MarketResearchRun:
        self._require_definition(target_definition_version_id)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO market_research_runs(
                    target_definition_version_id,
                    status,
                    controls_json,
                    ledger_json,
                    started_at
                ) VALUES (?, 'running', ?, '{}', ?)
                """,
                (
                    target_definition_version_id,
                    _json_text(controls),
                    started_at.isoformat(),
                ),
            )
            run_id = int(cursor.lastrowid)
        return self._require_run(run_id)

    def update_run_ledger(
        self,
        run_id: int,
        *,
        ledger: dict[str, Any],
    ) -> MarketResearchRun:
        run = self._require_run(run_id)
        if run.status != MarketRunStatus.RUNNING:
            raise MarketStoreError("Only a running Market run may change its ledger")
        with self._connect() as connection:
            connection.execute(
                "UPDATE market_research_runs SET ledger_json = ? WHERE id = ?",
                (_json_text(ledger), run_id),
            )
        return self._require_run(run_id)

    def finish_run(
        self,
        run_id: int,
        *,
        status: MarketRunStatus | str,
        ledger: dict[str, Any],
        completed_at: datetime,
        error_summary: str | None = None,
    ) -> MarketResearchRun:
        run = self._require_run(run_id)
        status = MarketRunStatus(status)
        if status not in _TERMINAL_RUN_STATUSES:
            raise MarketStoreError("finish_run requires a terminal status")
        if run.status != MarketRunStatus.RUNNING:
            raise MarketStoreError("A terminal Market run is immutable")
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE market_research_runs
                SET status = ?, ledger_json = ?, completed_at = ?, error_summary = ?
                WHERE id = ?
                """,
                (
                    status.value,
                    _json_text(ledger),
                    completed_at.isoformat(),
                    _optional_text(error_summary),
                    run_id,
                ),
            )
        return self._require_run(run_id)

    def get_run(self, run_id: int) -> MarketResearchRun | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_research_runs WHERE id = ?",
                (run_id,),
            ).fetchone()
        return _run(row) if row else None

    def record_membership(
        self,
        *,
        target_definition_version_id: int,
        job_detail_version_id: int,
        classifier_contract_version: str,
        classifier_method: str,
        classifier_identity: dict[str, Any],
        disposition: MarketMembershipDisposition | str,
        reason: str,
        evidence_refs: tuple[str, ...],
        created_at: datetime,
        translation_artifact_id: int | None = None,
        analysis_artifact_id: int | None = None,
        confidence: str | None = None,
        supersedes_membership_id: int | None = None,
    ) -> MarketJobMembership:
        self._require_definition(target_definition_version_id)
        disposition = MarketMembershipDisposition(disposition)
        contract = _required_text(
            classifier_contract_version,
            name="classifier_contract_version",
        )
        method = _required_text(classifier_method, name="classifier_method")
        identity = json.loads(_json_text(classifier_identity))
        dependency = {
            "target_definition_version_id": target_definition_version_id,
            "job_detail_version_id": job_detail_version_id,
            "translation_artifact_id": translation_artifact_id,
            "analysis_artifact_id": analysis_artifact_id,
            "classifier_contract_version": contract,
            "classifier_method": method,
            "classifier_identity": identity,
        }
        dependency_fingerprint = _json_sha256(dependency)
        result = {
            "dependency_fingerprint": dependency_fingerprint,
            "disposition": disposition.value,
            "reason": _required_text(reason, name="reason"),
            "evidence_refs": _normalized_strings(evidence_refs),
            "confidence": _optional_text(confidence),
            "supersedes_membership_id": supersedes_membership_id,
        }
        membership_fingerprint = _json_sha256(result)

        with self._connect() as connection:
            source_job_id = self._validate_dependency_chain(
                connection,
                job_detail_version_id=job_detail_version_id,
                translation_artifact_id=translation_artifact_id,
                analysis_artifact_id=analysis_artifact_id,
                require_accepted_analysis=analysis_artifact_id is not None,
            )
            exact = connection.execute(
                """
                SELECT m.*, p.source_job_id
                FROM market_job_memberships AS m
                JOIN job_detail_versions AS v ON v.id = m.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE m.membership_fingerprint = ?
                """,
                (membership_fingerprint,),
            ).fetchone()
            if exact:
                return _membership(exact)

            same_dependencies = connection.execute(
                """
                SELECT id
                FROM market_job_memberships
                WHERE dependency_fingerprint = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (dependency_fingerprint,),
            ).fetchone()
            if same_dependencies and supersedes_membership_id is None:
                raise MarketStoreError(
                    "Exact membership dependencies already have an immutable decision; "
                    "record a superseding correction instead"
                )
            if supersedes_membership_id is not None:
                previous = connection.execute(
                    """
                    SELECT target_definition_version_id, job_detail_version_id
                    FROM market_job_memberships
                    WHERE id = ?
                    """,
                    (supersedes_membership_id,),
                ).fetchone()
                if previous is None:
                    raise LookupError(
                        f"Unknown superseded membership {supersedes_membership_id}"
                    )
                if (
                    int(previous["target_definition_version_id"])
                    != target_definition_version_id
                    or int(previous["job_detail_version_id"])
                    != job_detail_version_id
                ):
                    raise MarketStoreError(
                        "A correction must preserve target definition and source version"
                    )

            cursor = connection.execute(
                """
                INSERT INTO market_job_memberships(
                    target_definition_version_id,
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    classifier_contract_version,
                    classifier_method,
                    classifier_identity_json,
                    dependency_fingerprint,
                    membership_fingerprint,
                    disposition,
                    reason,
                    evidence_refs_json,
                    confidence,
                    supersedes_membership_id,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    target_definition_version_id,
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    contract,
                    method,
                    _json_text(identity),
                    dependency_fingerprint,
                    membership_fingerprint,
                    disposition.value,
                    result["reason"],
                    _json_text(result["evidence_refs"]),
                    result["confidence"],
                    supersedes_membership_id,
                    created_at.isoformat(),
                ),
            )
            membership_id = int(cursor.lastrowid)
        membership = self._require_membership(membership_id)
        if membership.source_job_id != source_job_id:
            raise RuntimeError("Market membership source identity changed unexpectedly")
        return membership

    def find_reusable_membership(
        self,
        *,
        target_definition_version_id: int,
        job_detail_version_id: int,
        classifier_contract_version: str,
        classifier_method: str,
        classifier_identity: dict[str, Any],
        translation_artifact_id: int | None = None,
        analysis_artifact_id: int | None = None,
    ) -> MarketJobMembership | None:
        dependency = {
            "target_definition_version_id": target_definition_version_id,
            "job_detail_version_id": job_detail_version_id,
            "translation_artifact_id": translation_artifact_id,
            "analysis_artifact_id": analysis_artifact_id,
            "classifier_contract_version": _required_text(
                classifier_contract_version,
                name="classifier_contract_version",
            ),
            "classifier_method": _required_text(
                classifier_method,
                name="classifier_method",
            ),
            "classifier_identity": json.loads(_json_text(classifier_identity)),
        }
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT m.*, p.source_job_id
                FROM market_job_memberships AS m
                JOIN job_detail_versions AS v ON v.id = m.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE m.dependency_fingerprint = ?
                ORDER BY m.id DESC
                LIMIT 1
                """,
                (_json_sha256(dependency),),
            ).fetchone()
        return _membership(row) if row else None

    def get_membership(self, membership_id: int) -> MarketJobMembership | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT m.*, p.source_job_id
                FROM market_job_memberships AS m
                JOIN job_detail_versions AS v ON v.id = m.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE m.id = ?
                """,
                (membership_id,),
            ).fetchone()
        return _membership(row) if row else None

    def record_snapshot(
        self,
        *,
        target_definition_version_id: int,
        run_id: int,
        freshness_rule: str,
        source_scope: dict[str, Any],
        metadata: dict[str, Any],
        members: tuple[MarketSnapshotMemberInput, ...],
        created_at: datetime,
        snapshot_contract_version: str = MARKET_SNAPSHOT_CONTRACT_VERSION,
    ) -> MarketCorpusSnapshot:
        self._require_definition(target_definition_version_id)
        run = self._require_run(run_id)
        if run.target_definition_version_id != target_definition_version_id:
            raise MarketStoreError("Snapshot target definition must match its run")
        contract = _required_text(
            snapshot_contract_version,
            name="snapshot_contract_version",
        )
        with self._connect() as connection:
            if connection.execute(
                """
                SELECT 1
                FROM market_corpus_snapshots
                WHERE run_id = ? AND snapshot_contract_version = ?
                """,
                (run_id, contract),
            ).fetchone():
                raise MarketStoreError(
                    "This run already has an immutable snapshot for the contract"
                )
            prepared = [
                self._prepare_snapshot_member(
                    connection,
                    target_definition_version_id=target_definition_version_id,
                    item=item,
                )
                for item in members
            ]
            detail_ids = [item["job_detail_version_id"] for item in prepared]
            if len(detail_ids) != len(set(detail_ids)):
                raise MarketStoreError(
                    "A snapshot may contain a source detail version at most once"
                )
            cursor = connection.execute(
                """
                INSERT INTO market_corpus_snapshots(
                    target_definition_version_id,
                    run_id,
                    snapshot_contract_version,
                    freshness_rule,
                    source_scope_json,
                    metadata_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    target_definition_version_id,
                    run_id,
                    contract,
                    _required_text(freshness_rule, name="freshness_rule"),
                    _json_text(source_scope),
                    _json_text(metadata),
                    created_at.isoformat(),
                ),
            )
            snapshot_id = int(cursor.lastrowid)
            connection.executemany(
                """
                INSERT INTO market_corpus_snapshot_members(
                    snapshot_id,
                    membership_id,
                    job_detail_version_id,
                    translation_artifact_id,
                    analysis_artifact_id,
                    disposition,
                    semantic_coverage_status,
                    included_in_primary_corpus,
                    state_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        snapshot_id,
                        item["membership_id"],
                        item["job_detail_version_id"],
                        item["translation_artifact_id"],
                        item["analysis_artifact_id"],
                        item["disposition"],
                        item["semantic_coverage_status"],
                        item["included_in_primary_corpus"],
                        item["state_json"],
                    )
                    for item in prepared
                ],
            )
        return self._require_snapshot(snapshot_id)

    def get_snapshot(self, snapshot_id: int) -> MarketCorpusSnapshot | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_corpus_snapshots WHERE id = ?",
                (snapshot_id,),
            ).fetchone()
        return _snapshot(row) if row else None

    def list_snapshot_members(
        self,
        snapshot_id: int,
    ) -> tuple[MarketCorpusSnapshotMember, ...]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT sm.*, p.source_job_id
                FROM market_corpus_snapshot_members AS sm
                JOIN job_detail_versions AS v ON v.id = sm.job_detail_version_id
                JOIN job_postings AS p ON p.id = v.job_posting_id
                WHERE sm.snapshot_id = ?
                ORDER BY sm.id ASC
                """,
                (snapshot_id,),
            ).fetchall()
        return tuple(_snapshot_member(row) for row in rows)

    def record_aggregate_profile(
        self,
        *,
        snapshot_id: int,
        profile: dict[str, Any],
        created_at: datetime,
        aggregate_contract_version: str = MARKET_AGGREGATE_CONTRACT_VERSION,
    ) -> MarketAggregateProfile:
        self._require_snapshot(snapshot_id)
        contract = _required_text(
            aggregate_contract_version,
            name="aggregate_contract_version",
        )
        profile_json = _json_text(profile)
        profile_hash = hashlib.sha256(profile_json.encode("utf-8")).hexdigest()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM market_aggregate_profiles
                WHERE snapshot_id = ? AND aggregate_contract_version = ?
                """,
                (snapshot_id, contract),
            ).fetchone()
            if row:
                current = _profile(row)
                if current.profile_sha256 == profile_hash:
                    return current
                raise MarketStoreError(
                    "The same deterministic aggregate contract produced a different "
                    "profile for an immutable snapshot"
                )
            cursor = connection.execute(
                """
                INSERT INTO market_aggregate_profiles(
                    snapshot_id,
                    aggregate_contract_version,
                    profile_sha256,
                    profile_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    contract,
                    profile_hash,
                    profile_json,
                    created_at.isoformat(),
                ),
            )
            profile_id = int(cursor.lastrowid)
        return self._require_profile(profile_id)

    def get_aggregate_profile(
        self,
        profile_id: int,
    ) -> MarketAggregateProfile | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM market_aggregate_profiles WHERE id = ?",
                (profile_id,),
            ).fetchone()
        return _profile(row) if row else None

    def _validate_dependency_chain(
        self,
        connection: sqlite3.Connection,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int | None,
        analysis_artifact_id: int | None,
        require_accepted_analysis: bool,
    ) -> str:
        source = connection.execute(
            """
            SELECT p.source_job_id
            FROM job_detail_versions AS v
            JOIN job_postings AS p ON p.id = v.job_posting_id
            WHERE v.id = ?
            """,
            (job_detail_version_id,),
        ).fetchone()
        if source is None:
            raise LookupError(f"Unknown job detail version {job_detail_version_id}")

        if translation_artifact_id is not None:
            translation = connection.execute(
                """
                SELECT job_detail_version_id
                FROM job_translation_artifacts
                WHERE id = ?
                """,
                (translation_artifact_id,),
            ).fetchone()
            if translation is None:
                raise LookupError(
                    f"Unknown translation artifact {translation_artifact_id}"
                )
            if int(translation["job_detail_version_id"]) != job_detail_version_id:
                raise MarketStoreError(
                    "Translation artifact does not match the source version"
                )

        if analysis_artifact_id is not None:
            analysis = connection.execute(
                """
                SELECT job_detail_version_id,
                       translation_artifact_id,
                       semantic_review_status
                FROM job_analysis_artifacts
                WHERE id = ?
                """,
                (analysis_artifact_id,),
            ).fetchone()
            if analysis is None:
                raise LookupError(f"Unknown P1.6 artifact {analysis_artifact_id}")
            if int(analysis["job_detail_version_id"]) != job_detail_version_id:
                raise MarketStoreError("P1.6 artifact does not match the source version")
            analysis_translation = analysis["translation_artifact_id"]
            analysis_translation = (
                int(analysis_translation)
                if analysis_translation is not None
                else None
            )
            if analysis_translation != translation_artifact_id:
                raise MarketStoreError(
                    "Translation and P1.6 dependencies do not form one exact chain"
                )
            if (
                require_accepted_analysis
                and str(analysis["semantic_review_status"]) != "accepted"
            ):
                raise MarketStoreError(
                    "Market membership may consume only accepted P1.6 evidence"
                )
        return str(source["source_job_id"])

    def _prepare_snapshot_member(
        self,
        connection: sqlite3.Connection,
        *,
        target_definition_version_id: int,
        item: MarketSnapshotMemberInput,
    ) -> dict[str, Any]:
        coverage = P16CoverageStatus(item.semantic_coverage_status)
        membership = connection.execute(
            "SELECT * FROM market_job_memberships WHERE id = ?",
            (item.membership_id,),
        ).fetchone()
        if membership is None:
            raise LookupError(f"Unknown Market membership {item.membership_id}")
        if (
            int(membership["target_definition_version_id"])
            != target_definition_version_id
        ):
            raise MarketStoreError(
                "Snapshot membership belongs to a different target definition"
            )
        detail_id = int(membership["job_detail_version_id"])
        self._validate_dependency_chain(
            connection,
            job_detail_version_id=detail_id,
            translation_artifact_id=item.translation_artifact_id,
            analysis_artifact_id=item.analysis_artifact_id,
            require_accepted_analysis=coverage == P16CoverageStatus.ACCEPTED,
        )

        if coverage in {P16CoverageStatus.ACCEPTED, P16CoverageStatus.PENDING}:
            if item.analysis_artifact_id is None:
                raise MarketStoreError(
                    f"{coverage.value} coverage requires a P1.6 artifact"
                )
            row = connection.execute(
                """
                SELECT semantic_review_status
                FROM job_analysis_artifacts
                WHERE id = ?
                """,
                (item.analysis_artifact_id,),
            ).fetchone()
            if row is None or str(row["semantic_review_status"]) != coverage.value:
                raise MarketStoreError(
                    "Snapshot coverage status does not match P1.6 review state"
                )
        elif item.analysis_artifact_id is not None:
            raise MarketStoreError(
                f"{coverage.value} coverage must not reference a live P1.6 artifact"
            )

        disposition = MarketMembershipDisposition(str(membership["disposition"]))
        return {
            "membership_id": item.membership_id,
            "job_detail_version_id": detail_id,
            "translation_artifact_id": item.translation_artifact_id,
            "analysis_artifact_id": item.analysis_artifact_id,
            "disposition": disposition.value,
            "semantic_coverage_status": coverage.value,
            "included_in_primary_corpus": int(
                disposition == MarketMembershipDisposition.CORE_MATCH
            ),
            "state_json": _json_text(item.state or {}),
        }

    def _require_target(self, target_id: int) -> TargetMarket:
        target = self.get_target(target_id)
        if target is None:
            raise LookupError(f"Unknown Market target {target_id}")
        return target

    def _require_definition(
        self,
        definition_id: int,
    ) -> TargetMarketDefinitionVersion:
        definition = self.get_definition_version(definition_id)
        if definition is None:
            raise LookupError(f"Unknown Market target definition {definition_id}")
        return definition

    def _require_run(self, run_id: int) -> MarketResearchRun:
        run = self.get_run(run_id)
        if run is None:
            raise LookupError(f"Unknown Market run {run_id}")
        return run

    def _require_membership(self, membership_id: int) -> MarketJobMembership:
        membership = self.get_membership(membership_id)
        if membership is None:
            raise LookupError(f"Unknown Market membership {membership_id}")
        return membership

    def _require_snapshot(self, snapshot_id: int) -> MarketCorpusSnapshot:
        snapshot = self.get_snapshot(snapshot_id)
        if snapshot is None:
            raise LookupError(f"Unknown Market snapshot {snapshot_id}")
        return snapshot

    def _require_profile(self, profile_id: int) -> MarketAggregateProfile:
        profile = self.get_aggregate_profile(profile_id)
        if profile is None:
            raise LookupError(f"Unknown Market aggregate profile {profile_id}")
        return profile


def _target(row: sqlite3.Row) -> TargetMarket:
    return TargetMarket(
        id=int(row["id"]),
        slug=str(row["slug"]),
        name=str(row["name"]),
        description=_optional_text(row["description"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _definition(row: sqlite3.Row) -> TargetMarketDefinitionVersion:
    payload = json.loads(str(row["definition_json"]))
    return TargetMarketDefinitionVersion(
        id=int(row["id"]),
        target_market_id=int(row["target_market_id"]),
        version_number=int(row["version_number"]),
        definition_fingerprint=str(row["definition_fingerprint"]),
        spec=_spec_from_payload(payload),
        created_at=str(row["created_at"]),
    )


def _run(row: sqlite3.Row) -> MarketResearchRun:
    return MarketResearchRun(
        id=int(row["id"]),
        target_definition_version_id=int(row["target_definition_version_id"]),
        status=str(row["status"]),
        controls=json.loads(str(row["controls_json"])),
        ledger=json.loads(str(row["ledger_json"])),
        started_at=str(row["started_at"]),
        completed_at=_optional_text(row["completed_at"]),
        error_summary=_optional_text(row["error_summary"]),
    )


def _membership(row: sqlite3.Row) -> MarketJobMembership:
    return MarketJobMembership(
        id=int(row["id"]),
        target_definition_version_id=int(row["target_definition_version_id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=(
            int(row["translation_artifact_id"])
            if row["translation_artifact_id"] is not None
            else None
        ),
        analysis_artifact_id=(
            int(row["analysis_artifact_id"])
            if row["analysis_artifact_id"] is not None
            else None
        ),
        classifier_contract_version=str(row["classifier_contract_version"]),
        classifier_method=str(row["classifier_method"]),
        classifier_identity=json.loads(str(row["classifier_identity_json"])),
        dependency_fingerprint=str(row["dependency_fingerprint"]),
        disposition=str(row["disposition"]),
        reason=str(row["reason"]),
        evidence_refs=tuple(json.loads(str(row["evidence_refs_json"]))),
        confidence=_optional_text(row["confidence"]),
        supersedes_membership_id=(
            int(row["supersedes_membership_id"])
            if row["supersedes_membership_id"] is not None
            else None
        ),
        created_at=str(row["created_at"]),
    )


def _snapshot(row: sqlite3.Row) -> MarketCorpusSnapshot:
    return MarketCorpusSnapshot(
        id=int(row["id"]),
        target_definition_version_id=int(row["target_definition_version_id"]),
        run_id=int(row["run_id"]),
        snapshot_contract_version=str(row["snapshot_contract_version"]),
        freshness_rule=str(row["freshness_rule"]),
        source_scope=json.loads(str(row["source_scope_json"])),
        metadata=json.loads(str(row["metadata_json"])),
        created_at=str(row["created_at"]),
    )


def _snapshot_member(row: sqlite3.Row) -> MarketCorpusSnapshotMember:
    return MarketCorpusSnapshotMember(
        id=int(row["id"]),
        snapshot_id=int(row["snapshot_id"]),
        membership_id=int(row["membership_id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=(
            int(row["translation_artifact_id"])
            if row["translation_artifact_id"] is not None
            else None
        ),
        analysis_artifact_id=(
            int(row["analysis_artifact_id"])
            if row["analysis_artifact_id"] is not None
            else None
        ),
        disposition=str(row["disposition"]),
        semantic_coverage_status=str(row["semantic_coverage_status"]),
        included_in_primary_corpus=bool(row["included_in_primary_corpus"]),
        state=json.loads(str(row["state_json"])),
    )


def _profile(row: sqlite3.Row) -> MarketAggregateProfile:
    return MarketAggregateProfile(
        id=int(row["id"]),
        snapshot_id=int(row["snapshot_id"]),
        aggregate_contract_version=str(row["aggregate_contract_version"]),
        profile_sha256=str(row["profile_sha256"]),
        profile=json.loads(str(row["profile_json"])),
        created_at=str(row["created_at"]),
    )
