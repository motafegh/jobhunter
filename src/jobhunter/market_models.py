"""Typed records for the first target-scoped Market Intelligence slice."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


MARKET_SNAPSHOT_CONTRACT_VERSION = "market-corpus-snapshot-v1"
MARKET_AGGREGATE_CONTRACT_VERSION = "market-aggregate-profile-v1"


class MarketRunStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    COMPLETED_WITH_FAILURES = "completed_with_failures"
    FAILED = "failed"


class MarketMembershipDisposition(StrEnum):
    CORE_MATCH = "core_match"
    ADJACENT_MATCH = "adjacent_match"
    UNCERTAIN = "uncertain"
    EXCLUDED = "excluded"


class P16CoverageStatus(StrEnum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    MISSING = "missing"
    FAILED = "failed"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class MarketDefinitionSpec:
    membership_intent: str
    search_catalog_version: str
    source: str = "jobinja"
    search_profiles: tuple[str, ...] = ()
    search_packs: tuple[str, ...] = ()
    extra_search_terms: tuple[str, ...] = ()
    raw_searches: tuple[dict[str, Any], ...] = ()
    include_hints: tuple[str, ...] = ()
    exclude_hints: tuple[str, ...] = ()
    geography_scope: str | None = None
    work_arrangement_scope: str | None = None
    seniority_scope: str | None = None
    employment_type_scope: str | None = None
    freshness_rule: str = "current-active"


@dataclass(frozen=True, slots=True)
class TargetMarket:
    id: int
    slug: str
    name: str
    description: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class TargetMarketDefinitionVersion:
    id: int
    target_market_id: int
    version_number: int
    definition_fingerprint: str
    spec: MarketDefinitionSpec
    created_at: str


@dataclass(frozen=True, slots=True)
class MarketResearchRun:
    id: int
    target_definition_version_id: int
    status: str
    controls: dict[str, Any]
    ledger: dict[str, Any]
    started_at: str
    completed_at: str | None
    error_summary: str | None


@dataclass(frozen=True, slots=True)
class MarketJobMembership:
    id: int
    target_definition_version_id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int | None
    analysis_artifact_id: int | None
    classifier_contract_version: str
    classifier_method: str
    classifier_identity: dict[str, Any]
    dependency_fingerprint: str
    disposition: str
    reason: str
    evidence_refs: tuple[str, ...]
    confidence: str | None
    supersedes_membership_id: int | None
    created_at: str


@dataclass(frozen=True, slots=True)
class MarketSnapshotMemberInput:
    membership_id: int
    semantic_coverage_status: str
    translation_artifact_id: int | None = None
    analysis_artifact_id: int | None = None
    state: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class MarketCorpusSnapshot:
    id: int
    target_definition_version_id: int
    run_id: int
    snapshot_contract_version: str
    freshness_rule: str
    source_scope: dict[str, Any]
    metadata: dict[str, Any]
    created_at: str


@dataclass(frozen=True, slots=True)
class MarketCorpusSnapshotMember:
    id: int
    snapshot_id: int
    membership_id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int | None
    analysis_artifact_id: int | None
    disposition: str
    semantic_coverage_status: str
    included_in_primary_corpus: bool
    state: dict[str, Any]


@dataclass(frozen=True, slots=True)
class MarketAggregateProfile:
    id: int
    snapshot_id: int
    aggregate_contract_version: str
    profile_sha256: str
    profile: dict[str, Any]
    created_at: str
