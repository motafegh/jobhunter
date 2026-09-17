"""I5 deterministic aggregate profile over one immutable I4 snapshot.

All numeric facts are application-owned. The service reads only identities frozen by the
snapshot and persists one immutable profile through ``MarketStore``. It performs no model
calls, source refresh, membership inference, repost collapse, trend analysis, or reporting.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter, defaultdict
from contextlib import closing
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.canonical_registry import normalize_registry_text
from jobhunter.config import Settings
from jobhunter.market_models import (
    MARKET_AGGREGATE_CONTRACT_VERSION,
    MarketAggregateProfile,
    MarketCorpusSnapshotMember,
)
from jobhunter.market_store import MarketStore

_SMALL_SAMPLE = 20
_CONCENTRATION_MIN_SAMPLE = 5
_CONCENTRATION_SHARE = 0.50
_STRENGTHS = ("required", "preferred", "contextual", "inferred")
_CONTEXT_FIELDS = (
    "location",
    "employment_type",
    "minimum_experience",
    "education",
    "job_category",
)


class MarketAggregateError(ValueError):
    """Raised when an immutable snapshot cannot support a deterministic profile."""


@dataclass(frozen=True, slots=True)
class MarketAggregateBuildResult:
    artifact: MarketAggregateProfile
    profile: dict[str, Any]


@dataclass(frozen=True, slots=True)
class _SourceEvidence:
    source_job_id: str
    fields: dict[str, Any]
    employer_key: str | None
    employer_label: str | None


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _share(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 6)


def _text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = " ".join(value.split())
    return normalized or None


class MarketAggregateService:
    """Build and persist the deterministic I5 profile for one immutable snapshot."""

    def __init__(
        self,
        *,
        database_path: Path,
        market_store: MarketStore,
        analysis_store: AnalysisStore,
        clock=_utc_now,
    ) -> None:
        self._database_path = database_path
        self._market = market_store
        self._analyses = analysis_store
        self._clock = clock

    def build_profile(self, snapshot_id: int) -> MarketAggregateBuildResult:
        snapshot = self._market.get_snapshot(snapshot_id)
        if snapshot is None:
            raise LookupError(f"Unknown Market snapshot {snapshot_id}")
        members = self._market.list_snapshot_members(snapshot_id)
        definition = self._market.get_definition_version(
            snapshot.target_definition_version_id
        )
        if definition is None:
            raise RuntimeError("Market snapshot lost its target-definition dependency")
        target = self._market.get_target(definition.target_market_id)
        run = self._market.get_run(snapshot.run_id)
        if target is None or run is None:
            raise RuntimeError("Market snapshot lost target/run identity")

        source_by_member = {
            member.id: self._source_evidence(member) for member in members
        }
        core = tuple(item for item in members if item.included_in_primary_corpus)
        if any(item.disposition != "core_match" for item in core):
            raise MarketAggregateError(
                "Snapshot primary corpus contains a non-core membership"
            )
        accepted_core = tuple(
            item
            for item in core
            if item.semantic_coverage_status == "accepted"
            and item.analysis_artifact_id is not None
        )

        disposition_counts = Counter(item.disposition for item in members)
        coverage_counts = Counter(item.semantic_coverage_status for item in core)
        employer = self._employer_profile(core, source_by_member)
        source_context = self._source_context(core, source_by_member)
        requirements = self._requirement_profile(
            accepted_core,
            source_by_member,
            snapshot_created_at=snapshot.created_at,
        )
        responsibilities = self._responsibility_profile(
            accepted_core,
            source_by_member,
            snapshot_created_at=snapshot.created_at,
        )
        warnings = self._warnings(
            core=core,
            accepted_core=accepted_core,
            employer=employer,
        )

        profile: dict[str, Any] = {
            "aggregate_contract_version": MARKET_AGGREGATE_CONTRACT_VERSION,
            "target": {
                "target_market_id": target.id,
                "target_slug": target.slug,
                "target_definition_version_id": definition.id,
                "target_definition_version_number": definition.version_number,
                "target_definition_fingerprint": definition.definition_fingerprint,
                "membership_intent": definition.spec.membership_intent,
            },
            "snapshot": {
                "snapshot_id": snapshot.id,
                "snapshot_contract_version": snapshot.snapshot_contract_version,
                "created_at": snapshot.created_at,
                "run_id": snapshot.run_id,
                "run_status": run.status,
                "run_completed_at": run.completed_at,
                "freshness_rule": snapshot.freshness_rule,
                "source_scope": snapshot.source_scope,
            },
            "corpus": {
                "raw_snapshot_members": len(members),
                "dispositions": {
                    value: disposition_counts.get(value, 0)
                    for value in (
                        "core_match",
                        "adjacent_match",
                        "uncertain",
                        "excluded",
                    )
                },
                "primary_core_postings": len(core),
                "semantic_coverage_core": {
                    value: coverage_counts.get(value, 0)
                    for value in (
                        "accepted",
                        "pending",
                        "missing",
                        "failed",
                        "rejected",
                    )
                },
                "accepted_semantic_core_postings": len(accepted_core),
                "accepted_semantic_coverage": {
                    "numerator": len(accepted_core),
                    "denominator": len(core),
                    "share": _share(len(accepted_core), len(core)),
                },
                "denominator_language": "qualified source postings",
                "repost_adjustment": "not_implemented",
            },
            "employers": employer,
            "source_context": source_context,
            "requirements": requirements,
            "responsibilities": responsibilities,
            "warnings": warnings,
            "limitations": [
                "No automatic repost/new-ID or cross-source duplicate adjustment is applied.",
                (
                    "Semantic requirement/responsibility statistics use accepted-P1.6 core "
                    "postings only."
                ),
                "Registry enrichment uses only reviewed mappings dated no later than the snapshot.",
                (
                    "No role-subfamily, trend, forecast, personal-fit, or model-authored numeric "
                    "score is present."
                ),
            ],
        }
        artifact = self._market.record_aggregate_profile(
            snapshot_id=snapshot.id,
            profile=profile,
            created_at=self._clock(),
        )
        return MarketAggregateBuildResult(artifact=artifact, profile=profile)

    def _source_evidence(self, member: MarketCorpusSnapshotMember) -> _SourceEvidence:
        with closing(self._connect_readonly()) as connection:
            row = connection.execute(
                """
                SELECT v.fields_json
                FROM job_detail_versions AS v
                WHERE v.id = ?
                """,
                (member.job_detail_version_id,),
            ).fetchone()
        if row is None:
            raise MarketAggregateError(
                f"Snapshot lost source detail version {member.job_detail_version_id}"
            )
        fields = json.loads(str(row["fields_json"]))
        if not isinstance(fields, dict):
            raise MarketAggregateError("Source detail fields are not a JSON object")
        employer_label = _text(fields.get("company"))
        employer_key = normalize_registry_text(employer_label) if employer_label else None
        return _SourceEvidence(
            source_job_id=member.source_job_id,
            fields=fields,
            employer_key=employer_key,
            employer_label=employer_label,
        )

    def _employer_profile(
        self,
        core: tuple[MarketCorpusSnapshotMember, ...],
        source_by_member: dict[int, _SourceEvidence],
    ) -> dict[str, Any]:
        postings_by_employer: Counter[str] = Counter()
        labels: dict[str, str] = {}
        unknown_jobs: list[str] = []
        for member in core:
            source = source_by_member[member.id]
            if source.employer_key is None:
                unknown_jobs.append(member.source_job_id)
                continue
            postings_by_employer[source.employer_key] += 1
            labels.setdefault(source.employer_key, source.employer_label or source.employer_key)
        largest = max(postings_by_employer.values(), default=0)
        rows = [
            {
                "employer_key": key,
                "employer": labels[key],
                "postings": count,
                "share_of_core": _share(count, len(core)),
            }
            for key, count in postings_by_employer.items()
        ]
        rows.sort(key=lambda row: (-row["postings"], row["employer"].casefold()))
        return {
            "known_employer_postings": sum(postings_by_employer.values()),
            "unknown_employer_postings": len(unknown_jobs),
            "unknown_employer_job_ids": sorted(unknown_jobs),
            "distinct_known_employers": len(postings_by_employer),
            "largest_employer_postings": largest,
            "largest_employer_share_of_core": _share(largest, len(core)),
            "rows": rows,
        }

    def _source_context(
        self,
        core: tuple[MarketCorpusSnapshotMember, ...],
        source_by_member: dict[int, _SourceEvidence],
    ) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {}
        for field_name in _CONTEXT_FIELDS:
            counts: Counter[str] = Counter()
            labels: dict[str, str] = {}
            for member in core:
                value = _text(source_by_member[member.id].fields.get(field_name))
                if value is None:
                    continue
                key = normalize_registry_text(value)
                counts[key] += 1
                labels.setdefault(key, value)
            denominator = sum(counts.values())
            rows = [
                {
                    "value": labels[key],
                    "postings": count,
                    "denominator": denominator,
                    "share": _share(count, denominator),
                }
                for key, count in counts.items()
            ]
            rows.sort(key=lambda row: (-row["postings"], row["value"].casefold()))
            result[field_name] = rows
        return result

    def _requirement_profile(
        self,
        accepted_core: tuple[MarketCorpusSnapshotMember, ...],
        source_by_member: dict[int, _SourceEvidence],
        *,
        snapshot_created_at: str,
    ) -> list[dict[str, Any]]:
        groups: dict[str, dict[str, Any]] = {}
        for member in accepted_core:
            artifact = self._accepted_artifact(member)
            per_job: dict[str, dict[str, Any]] = {}
            for index, claim in enumerate(artifact.analysis.get("requirements", [])):
                concept = _text(claim.get("concept"))
                concept_type = _text(claim.get("concept_type")) or "other"
                if concept is None:
                    continue
                mapping = self._claim_mapping(
                    artifact.id,
                    "requirement",
                    index,
                    snapshot_created_at=snapshot_created_at,
                )
                key, label, canonical_id, state, mapping_id = self._normalized_claim(
                    kind="requirement",
                    raw_text=concept,
                    raw_type=concept_type,
                    mapping=mapping,
                )
                support = per_job.setdefault(
                    key,
                    {
                        "label": label,
                        "canonical_concept_id": canonical_id,
                        "normalization_states": set(),
                        "mapping_ids": set(),
                        "concept_types": set(),
                        "strengths": set(),
                        "depth_signals": set(),
                        "claim_indexes": [],
                        "evidence": [],
                    },
                )
                support["normalization_states"].add(state)
                if mapping_id is not None:
                    support["mapping_ids"].add(mapping_id)
                support["concept_types"].add(concept_type)
                strength = _text(claim.get("strength"))
                if strength in _STRENGTHS:
                    support["strengths"].add(strength)
                depth = _text(claim.get("depth_signal"))
                if depth:
                    support["depth_signals"].add(depth)
                support["claim_indexes"].append(index)
                evidence = _text(claim.get("evidence"))
                if evidence is not None:
                    support["evidence"].append(evidence)

            source = source_by_member[member.id]
            for key, support in per_job.items():
                group = groups.setdefault(
                    key,
                    {
                        "key": key,
                        "label_candidates": set(),
                        "canonical_concept_id": support["canonical_concept_id"],
                        "normalization_states": set(),
                        "mapping_ids": set(),
                        "concept_types": set(),
                        "postings": set(),
                        "strength_postings": {strength: set() for strength in _STRENGTHS},
                        "depth_signal_postings": defaultdict(set),
                        "employers": set(),
                        "unknown_employer_postings": set(),
                        "evidence": [],
                    },
                )
                group["label_candidates"].add(support["label"])
                group["normalization_states"].update(support["normalization_states"])
                group["mapping_ids"].update(support["mapping_ids"])
                group["concept_types"].update(support["concept_types"])
                group["postings"].add(member.source_job_id)
                for strength in support["strengths"]:
                    group["strength_postings"][strength].add(member.source_job_id)
                for depth in support["depth_signals"]:
                    group["depth_signal_postings"][depth].add(member.source_job_id)
                if source.employer_key is None:
                    group["unknown_employer_postings"].add(member.source_job_id)
                else:
                    group["employers"].add(source.employer_key)
                group["evidence"].append(
                    {
                        "source_job_id": member.source_job_id,
                        "analysis_artifact_id": artifact.id,
                        "claim_indexes": sorted(support["claim_indexes"]),
                        "evidence": sorted(set(support["evidence"])),
                    }
                )

        rows: list[dict[str, Any]] = []
        for group in groups.values():
            label = min(group["label_candidates"], key=lambda value: value.casefold())
            rows.append(
                {
                    "key": group["key"],
                    "label": label,
                    "canonical_concept_id": group["canonical_concept_id"],
                    "normalization_states": sorted(group["normalization_states"]),
                    "mapping_ids": sorted(group["mapping_ids"]),
                    "concept_types": sorted(group["concept_types"]),
                    "postings": len(group["postings"]),
                    "share_of_accepted_semantic_core": _share(
                        len(group["postings"]), len(accepted_core)
                    ),
                    "strength_postings": {
                        strength: len(group["strength_postings"][strength])
                        for strength in _STRENGTHS
                    },
                    "depth_signal_postings": {
                        depth: len(postings)
                        for depth, postings in sorted(group["depth_signal_postings"].items())
                    },
                    "distinct_known_employers": len(group["employers"]),
                    "unknown_employer_postings": len(group["unknown_employer_postings"]),
                    "evidence": sorted(
                        group["evidence"], key=lambda item: item["source_job_id"]
                    ),
                }
            )
        rows.sort(key=lambda row: (-row["postings"], row["label"].casefold(), row["key"]))
        return rows

    def _responsibility_profile(
        self,
        accepted_core: tuple[MarketCorpusSnapshotMember, ...],
        source_by_member: dict[int, _SourceEvidence],
        *,
        snapshot_created_at: str,
    ) -> list[dict[str, Any]]:
        groups: dict[str, dict[str, Any]] = {}
        for member in accepted_core:
            artifact = self._accepted_artifact(member)
            per_job: dict[str, dict[str, Any]] = {}
            for index, claim in enumerate(artifact.analysis.get("responsibilities", [])):
                statement = _text(claim.get("statement"))
                if statement is None:
                    continue
                mapping = self._claim_mapping(
                    artifact.id,
                    "responsibility",
                    index,
                    snapshot_created_at=snapshot_created_at,
                )
                key, label, canonical_id, state, mapping_id = self._normalized_claim(
                    kind="responsibility",
                    raw_text=statement,
                    raw_type="responsibility",
                    mapping=mapping,
                )
                support = per_job.setdefault(
                    key,
                    {
                        "label": label,
                        "canonical_concept_id": canonical_id,
                        "normalization_states": set(),
                        "mapping_ids": set(),
                        "claim_indexes": [],
                        "statements": [],
                        "evidence": [],
                    },
                )
                support["normalization_states"].add(state)
                if mapping_id is not None:
                    support["mapping_ids"].add(mapping_id)
                support["claim_indexes"].append(index)
                support["statements"].append(statement)
                evidence = _text(claim.get("evidence"))
                if evidence is not None:
                    support["evidence"].append(evidence)

            source = source_by_member[member.id]
            for key, support in per_job.items():
                group = groups.setdefault(
                    key,
                    {
                        "key": key,
                        "label_candidates": set(),
                        "canonical_concept_id": support["canonical_concept_id"],
                        "normalization_states": set(),
                        "mapping_ids": set(),
                        "postings": set(),
                        "employers": set(),
                        "unknown_employer_postings": set(),
                        "evidence": [],
                    },
                )
                group["label_candidates"].add(support["label"])
                group["normalization_states"].update(support["normalization_states"])
                group["mapping_ids"].update(support["mapping_ids"])
                group["postings"].add(member.source_job_id)
                if source.employer_key is None:
                    group["unknown_employer_postings"].add(member.source_job_id)
                else:
                    group["employers"].add(source.employer_key)
                group["evidence"].append(
                    {
                        "source_job_id": member.source_job_id,
                        "analysis_artifact_id": artifact.id,
                        "claim_indexes": sorted(support["claim_indexes"]),
                        "statements": sorted(set(support["statements"])),
                        "evidence": sorted(set(support["evidence"])),
                    }
                )

        rows = []
        for group in groups.values():
            label = min(group["label_candidates"], key=lambda value: value.casefold())
            rows.append(
                {
                    "key": group["key"],
                    "label": label,
                    "canonical_concept_id": group["canonical_concept_id"],
                    "normalization_states": sorted(group["normalization_states"]),
                    "mapping_ids": sorted(group["mapping_ids"]),
                    "postings": len(group["postings"]),
                    "share_of_accepted_semantic_core": _share(
                        len(group["postings"]), len(accepted_core)
                    ),
                    "distinct_known_employers": len(group["employers"]),
                    "unknown_employer_postings": len(
                        group["unknown_employer_postings"]
                    ),
                    "evidence": sorted(
                        group["evidence"], key=lambda item: item["source_job_id"]
                    ),
                }
            )
        rows.sort(
            key=lambda row: (-row["postings"], row["label"].casefold(), row["key"])
        )
        return rows

    def _accepted_artifact(self, member: MarketCorpusSnapshotMember) -> AnalysisArtifact:
        if member.semantic_coverage_status != "accepted" or member.analysis_artifact_id is None:
            raise MarketAggregateError("Semantic aggregation requires accepted snapshot P1.6")
        artifact = self._analyses.artifact_by_id(member.analysis_artifact_id)
        if artifact is None:
            raise MarketAggregateError(
                f"Snapshot lost accepted P1.6 artifact {member.analysis_artifact_id}"
            )
        if artifact.job_detail_version_id != member.job_detail_version_id:
            raise MarketAggregateError("Snapshot P1.6/source dependency mismatch")
        if artifact.translation_artifact_id != member.translation_artifact_id:
            raise MarketAggregateError("Snapshot P1.6/translation dependency mismatch")
        return artifact

    def _normalized_claim(
        self,
        *,
        kind: str,
        raw_text: str,
        raw_type: str,
        mapping: sqlite3.Row | None,
    ) -> tuple[str, str, str | None, str, int | None]:
        if mapping is not None and str(mapping["disposition"]) == "mapped":
            concept_id = str(mapping["canonical_concept_id"])
            label = str(mapping["preferred_label"])
            return (
                f"canonical:{concept_id}",
                label,
                concept_id,
                "canonical_mapped",
                int(mapping["mapping_id"]),
            )
        normalized = normalize_registry_text(raw_text)
        key = f"raw:{kind}:{normalize_registry_text(raw_type)}:{normalized}"
        if mapping is None:
            return key, raw_text, None, "raw_unreviewed", None
        disposition = str(mapping["disposition"])
        state = (
            "reviewed_unmapped"
            if disposition == "unmapped"
            else "reviewed_rejected_mapping"
        )
        return key, raw_text, None, state, int(mapping["mapping_id"])

    def _claim_mapping(
        self,
        analysis_artifact_id: int,
        claim_kind: str,
        claim_index: int,
        *,
        snapshot_created_at: str,
    ) -> sqlite3.Row | None:
        with closing(self._connect_readonly()) as connection:
            exists = connection.execute(
                """
                SELECT 1 FROM sqlite_master
                WHERE type = 'table' AND name = 'job_claim_canonical_mappings'
                """
            ).fetchone()
            if exists is None:
                return None
            return connection.execute(
                """
                SELECT
                    m.id AS mapping_id,
                    m.disposition,
                    m.canonical_concept_id,
                    m.reviewed_at,
                    c.preferred_label
                FROM job_claim_canonical_mappings AS m
                LEFT JOIN canonical_concepts AS c
                  ON c.concept_id = m.canonical_concept_id
                WHERE m.analysis_artifact_id = ?
                  AND m.claim_kind = ?
                  AND m.claim_index = ?
                  AND m.reviewed_at <= ?
                LIMIT 1
                """,
                (
                    analysis_artifact_id,
                    claim_kind,
                    claim_index,
                    snapshot_created_at,
                ),
            ).fetchone()

    def _warnings(
        self,
        *,
        core: tuple[MarketCorpusSnapshotMember, ...],
        accepted_core: tuple[MarketCorpusSnapshotMember, ...],
        employer: dict[str, Any],
    ) -> list[dict[str, str]]:
        warnings: list[dict[str, str]] = [
            {
                "code": "repost_adjustment_missing",
                "message": (
                    "Repost/new-ID duplicate adjustment is not implemented; counts are qualified "
                    "source postings, not unique demand units."
                ),
            }
        ]
        if 0 < len(core) < _SMALL_SAMPLE:
            warnings.append(
                {
                    "code": "small_core_sample",
                    "message": (
                        f"Only {len(core)} core postings are in this snapshot; broad market "
                        "conclusions require caution."
                    ),
                }
            )
        if 0 < len(accepted_core) < _SMALL_SAMPLE:
            warnings.append(
                {
                    "code": "small_semantic_sample",
                    "message": (
                        f"Only {len(accepted_core)} core postings have accepted P1.6 evidence; "
                        "semantic prevalence is a limited sample."
                    ),
                }
            )
        if len(accepted_core) < len(core):
            warnings.append(
                {
                    "code": "incomplete_semantic_coverage",
                    "message": (
                        f"Accepted P1.6 covers {len(accepted_core)} of {len(core)} core postings; "
                        "missing/pending/failed/rejected postings are not zero demand."
                    ),
                }
            )
        largest = int(employer["largest_employer_postings"])
        if (
            len(core) >= _CONCENTRATION_MIN_SAMPLE
            and largest / len(core) >= _CONCENTRATION_SHARE
        ):
            warnings.append(
                {
                    "code": "employer_concentration",
                    "message": (
                        f"One employer contributes {largest} of {len(core)} core postings; "
                        "employer concentration can distort apparent prevalence."
                    ),
                }
            )
        unknown = int(employer["unknown_employer_postings"])
        if unknown:
            warnings.append(
                {
                    "code": "unknown_employer_evidence",
                    "message": (
                        f"{unknown} core postings lack an immutable source-detail employer field; "
                        "employer breadth excludes those postings."
                    ),
                }
            )
        return warnings

    def _connect_readonly(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            f"file:{self._database_path.resolve()}?mode=ro",
            uri=True,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection


def build_market_aggregate_service(settings: Settings) -> MarketAggregateService:
    """Compose I5 from the accepted Market store and P1.6 analysis owner."""

    return MarketAggregateService(
        database_path=settings.database_path,
        market_store=MarketStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
    )
