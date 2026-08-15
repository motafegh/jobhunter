"""Capability v9 semantic guardrails and corrected source-truth accounting."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator

from jobhunter.capability_models import CapabilityExpectation, CapabilityProfile
from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft,
    CapabilitySourcePurpose,
    CapabilitySourceRequirement,
    CapabilitySourceResponsibility,
    reconcile_capability_intelligence,
)
from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityFactAssignmentV8,
    CapabilityGroupPlanV8,
    CapabilityGroupSeedV8,
    CapabilityProfileReasoningV8,
    assignment_partitions,
)

_DERIVED_STATUSES = {"strongly_implied_by_work", "model_inferred_prerequisite"}
_DEPTH_INFLATION_RE = re.compile(
    r"\b(?:advanced|expert(?:ise)?|proficien(?:t|cy)|mastery|strong|solid|hands-on)\b",
    re.IGNORECASE,
)
_SOURCE_OBLIGATION_RE = re.compile(
    r"\b(?:requires?|required|must|mandatory|mandates?|mandated)\b",
    re.IGNORECASE,
)
_PREREQUISITE_LANGUAGE_RE = re.compile(
    r"\b(?:necessar(?:y|ily)|necessitates?|prerequisite)\b",
    re.IGNORECASE,
)
_SCOPE_INFLATION_RE = re.compile(
    r"\b(?:end[- ]to[- ]end|full lifecycle|ownership|owning|owns|leadership|leading|"
    r"autonomy|autonomous|architecting|architecture)\b",
    re.IGNORECASE,
)
_DEEP_RE = re.compile(r"\bdeep\b", re.IGNORECASE)
_RECONCILIATION_BRIDGE_STATEMENT = (
    "No additional model-derived claim is required for this bounded capability profile."
)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _without_deep_learning(value: str) -> str:
    return re.sub(r"\bdeep\s+learning\b", "learning", value, flags=re.IGNORECASE)


def _guard_model_owned_text(
    value: str,
    *,
    field_name: str,
    allow_depth_language: bool = False,
    allow_prerequisite_language: bool = False,
    allow_source_obligation_language: bool = False,
) -> None:
    if not allow_source_obligation_language and _SOURCE_OBLIGATION_RE.search(value):
        raise ValueError(
            f"{field_name} may not restate source requirement obligation; "
            "JobHunter owns source strength"
        )
    if not allow_prerequisite_language and _PREREQUISITE_LANGUAGE_RE.search(value):
        raise ValueError(
            f"{field_name} may not introduce necessity/prerequisite language outside an "
            "explicit model_inferred_prerequisite"
        )
    if _SCOPE_INFLATION_RE.search(value):
        raise ValueError(
            f"{field_name} may not infer ownership, lifecycle breadth, autonomy, or architecture"
        )
    if allow_depth_language:
        return
    depth_text = _without_deep_learning(value)
    if _DEPTH_INFLATION_RE.search(depth_text) or _DEEP_RE.search(depth_text):
        raise ValueError(
            f"{field_name} may not add technical depth; JobHunter owns source-explicit depth"
        )


def _requirement_evidence_map(
    info: ValidationInfo,
) -> tuple[dict[str, list[dict[str, Any]]], set[str]]:
    context = info.context or {}
    raw_requirements = context.get("assigned_requirements") or []
    if not isinstance(raw_requirements, list):
        raise ValueError("Capability v9 context assigned_requirements must be a list")

    evidence_map: dict[str, list[dict[str, Any]]] = {}
    required_concepts: set[str] = set()
    for item in raw_requirements:
        if not isinstance(item, dict):
            continue
        concept = item.get("concept")
        if isinstance(concept, str) and item.get("requirement_type") == "required":
            required_concepts.add(_normalize(concept))
        raw_evidence = item.get("evidence")
        values = raw_evidence if isinstance(raw_evidence, list) else [raw_evidence]
        for evidence in values:
            if isinstance(evidence, str) and evidence.strip():
                evidence_map.setdefault(_normalize(evidence), []).append(item)
    return evidence_map, required_concepts


def _validate_prerequisite_optionality(
    item: CapabilityExpectation,
    info: ValidationInfo,
    *,
    field_name: str,
) -> None:
    if item.evidence_status != "model_inferred_prerequisite":
        return
    evidence_map, required_concepts = _requirement_evidence_map(info)
    for evidence in item.evidence:
        for requirement in evidence_map.get(_normalize(evidence), []):
            strength = requirement.get("requirement_type")
            concept = requirement.get("concept")
            normalized_concept = _normalize(concept) if isinstance(concept, str) else ""
            optional_only = (
                strength in {"preferred", "contextual"}
                and normalized_concept not in required_concepts
            )
            if optional_only:
                raise ValueError(
                    f"{field_name} may not infer a prerequisite from preferred/contextual-only "
                    f"source fact {concept!r}"
                )


def _safe_derived_expectation(
    item: CapabilityExpectation,
    info: ValidationInfo,
    *,
    field_name: str,
    allow_depth_language: bool = False,
) -> bool:
    """Fail closed on one optional model inference without discarding its whole profile."""

    inferred_prerequisite = item.evidence_status == "model_inferred_prerequisite"
    try:
        _guard_model_owned_text(
            item.statement,
            field_name=f"{field_name}.statement",
            allow_depth_language=allow_depth_language,
            allow_prerequisite_language=inferred_prerequisite,
        )
        _guard_model_owned_text(
            item.rationale,
            field_name=f"{field_name}.rationale",
            allow_depth_language=allow_depth_language,
            allow_prerequisite_language=inferred_prerequisite,
            allow_source_obligation_language=inferred_prerequisite,
        )
        _validate_prerequisite_optionality(item, info, field_name=field_name)
    except ValueError:
        return False
    return True


def _has_derived_reasoning(profile: dict[str, Any]) -> bool:
    for field_name in (
        "depth_signals",
        "work_activities",
        "sub_capabilities",
        "underlying_knowledge",
        "operational_practices",
        "operational_context",
    ):
        for item in profile.get(field_name) or []:
            if isinstance(item, dict) and item.get("evidence_status") in _DERIVED_STATUSES:
                return True
    return False


class CapabilityGroupPlanV9(CapabilityGroupPlanV8):
    """V8 group shape with v9 separation of semantics from strength/depth/scope."""

    @model_validator(mode="after")
    def guard_group_prose(self) -> CapabilityGroupPlanV9:
        _guard_model_owned_text(
            self.role_interpretation,
            field_name="role_interpretation",
        )
        for group in self.groups:
            _guard_model_owned_text(
                group.capability_label,
                field_name=f"group[{group.group_id}].capability_label",
            )
            _guard_model_owned_text(
                group.summary,
                field_name=f"group[{group.group_id}].summary",
            )
        return self


class CapabilityFactAssignmentV9(CapabilityFactAssignmentV8):
    """Versioned name for unchanged exact source-fact assignment semantics."""


class CapabilityAssignmentPartitionV9(CapabilityAssignmentPartitionV8):
    requirement_assignments: list[CapabilityFactAssignmentV9]
    responsibility_assignments: list[CapabilityFactAssignmentV9]


class CapabilityProfileReasoningV9(CapabilityProfileReasoningV8):
    """Optional bounded enrichment above deterministic source-owned capability facts."""

    @model_validator(mode="after")
    def validate_reasoning_boundary(self) -> CapabilityProfileReasoningV9:
        """Override v8's forced-enrichment invariant while preserving section contracts."""

        for field_name in (
            "depth_signals",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            invalid = {
                item.evidence_status for item in getattr(self, field_name)
            } - _DERIVED_STATUSES
            if invalid:
                raise ValueError(
                    f"{field_name} may contain only optional derived reasoning statuses in "
                    f"Capability v9: {sorted(invalid)}"
                )
        if any(item.evidence_status != "unknown_or_unsupported" for item in self.unknown_scope):
            raise ValueError("unknown_scope items must use unknown_or_unsupported")
        if self.overall_confidence not in {"high", "medium", "low"}:
            raise ValueError("overall_confidence must be high, medium, or low")
        return self

    @model_validator(mode="after")
    def guard_profile_semantics(self, info: ValidationInfo) -> CapabilityProfileReasoningV9:
        context = info.context or {}
        try:
            _guard_model_owned_text(self.summary, field_name="profile.summary")
        except ValueError:
            fallback = context.get("group_summary")
            if not isinstance(fallback, str) or not fallback.strip():
                raise
            _guard_model_owned_text(fallback, field_name="group_summary")
            self.summary = fallback.strip()
            note = (
                "JobHunter replaced model-expanded profile summary with the already-validated "
                "neutral capability-group summary."
            )
            if note not in self.uncertainties:
                self.uncertainties.append(note)

        discarded = 0
        for field_name in (
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            items: list[CapabilityExpectation] = getattr(self, field_name)
            kept = [
                item
                for item in items
                if _safe_derived_expectation(item, info, field_name=field_name)
            ]
            discarded += len(items) - len(kept)
            setattr(self, field_name, kept)

        depth_kept = [
            item
            for item in self.depth_signals
            if _safe_derived_expectation(
                item,
                info,
                field_name="depth_signals",
                allow_depth_language=True,
            )
        ]
        discarded += len(self.depth_signals) - len(depth_kept)
        self.depth_signals = depth_kept

        if discarded:
            note = (
                "JobHunter discarded "
                f"{discarded} optional model-derived expectation(s) that crossed v9 semantic "
                "guardrails; deterministic P1.6 source truth remains authoritative."
            )
            if note not in self.uncertainties:
                self.uncertainties.append(note)
        return self


class CapabilityProfileV9(CapabilityProfile):
    """Final v9 profile: source linkage is mandatory; extra model enrichment is not."""

    @model_validator(mode="after")
    def normalize_sections(self) -> CapabilityProfileV9:
        """Override the historical requirement to invent derived reasoning or unknown scope."""

        if not self.source_requirement_indices and not self.source_responsibility_indices:
            raise ValueError(
                "Capability profile must link at least one accepted P1.6 requirement or "
                "responsibility"
            )

        for field_name in (
            "depth_signals",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
            "unknown_scope",
        ):
            items: list[CapabilityExpectation] = getattr(self, field_name)
            seen: set[tuple[str, str]] = set()
            unique: list[CapabilityExpectation] = []
            for item in items:
                key = (_normalize(item.statement), item.evidence_status)
                if key in seen:
                    continue
                seen.add(key)
                unique.append(item)
            setattr(self, field_name, unique)

        if any(
            item.evidence_status != "unknown_or_unsupported" for item in self.unknown_scope
        ):
            raise ValueError(
                "unknown_scope items must use evidence_status='unknown_or_unsupported'"
            )
        return self


class CapabilityReasoningDraftV9(CapabilityReasoningDraft):
    """V9 draft retaining strict source coverage while allowing zero optional enrichment."""

    capabilities: list[CapabilityProfileV9]


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CapabilitySourceTruthV9(_StrictModel):
    """Source truth with capability-depth and role-level-depth accounting separated."""

    role_purpose: list[CapabilitySourcePurpose]
    requirements: list[CapabilitySourceRequirement]
    responsibilities: list[CapabilitySourceResponsibility]
    capability_requirement_indices: list[int]
    role_level_requirement_indices: list[int]
    linked_requirement_indices: list[int]
    unlinked_capability_requirement_indices: list[int]
    linked_responsibility_indices: list[int]
    unlinked_responsibility_indices: list[int]
    all_explicit_depth_requirement_indices: list[int]
    capability_explicit_depth_requirement_indices: list[int]
    linked_capability_explicit_depth_requirement_indices: list[int]
    unlinked_capability_explicit_depth_requirement_indices: list[int]
    role_level_explicit_depth_requirement_indices: list[int]


class JobCapabilityIntelligenceV9(CapabilityReasoningDraftV9):
    """Persisted v9 artifact with optional enrichment and strict deterministic source truth."""

    source_truth: CapabilitySourceTruthV9 | None = None


def build_v9_intelligence(intelligence: dict[str, Any]) -> dict[str, Any]:
    """Replace v7 depth-link accounting with capability-vs-role-level accounting."""

    payload = deepcopy(intelligence)
    source_truth = payload.get("source_truth")
    if not isinstance(source_truth, dict):
        raise ValueError("Capability v9 requires deterministic source_truth")

    requirements = source_truth.get("requirements") or []
    if not isinstance(requirements, list):
        raise ValueError("Capability v9 source_truth requirements must be a list")
    capability_indices = set(source_truth.get("capability_requirement_indices") or [])
    role_level_indices = set(source_truth.get("role_level_requirement_indices") or [])
    linked_indices = set(source_truth.get("linked_requirement_indices") or [])

    all_depth = sorted(
        int(item["index"])
        for item in requirements
        if isinstance(item, dict)
        and isinstance(item.get("index"), int)
        and isinstance(item.get("depth_signal"), str)
        and item["depth_signal"].strip()
    )
    capability_depth = sorted(set(all_depth) & capability_indices)
    role_level_depth = sorted(set(all_depth) & role_level_indices)
    linked_capability_depth = sorted(set(capability_depth) & linked_indices)

    transformed = dict(source_truth)
    transformed.pop("explicit_depth_requirement_indices", None)
    transformed.pop("linked_explicit_depth_requirement_indices", None)
    transformed.pop("unlinked_explicit_depth_requirement_indices", None)
    transformed.update(
        {
            "all_explicit_depth_requirement_indices": all_depth,
            "capability_explicit_depth_requirement_indices": capability_depth,
            "linked_capability_explicit_depth_requirement_indices": linked_capability_depth,
            "unlinked_capability_explicit_depth_requirement_indices": sorted(
                set(capability_depth) - linked_indices
            ),
            "role_level_explicit_depth_requirement_indices": role_level_depth,
        }
    )
    validated = CapabilitySourceTruthV9.model_validate(transformed)
    payload["source_truth"] = validated.model_dump(mode="json")
    return payload


def reconcile_capability_intelligence_v9(
    intelligence: CapabilityReasoningDraftV9,
    *,
    accepted_extraction: dict[str, Any],
    analysis_fields: dict[str, Any],
    evidence_catalog: dict[str, str] | None = None,
) -> JobCapabilityIntelligenceV9:
    """Reuse deterministic v7 reconciliation without inheriting its forced-enrichment contract."""

    bridge_payload = intelligence.model_dump(mode="json")
    bridged_profile_indices: list[int] = []
    for index, profile in enumerate(bridge_payload.get("capabilities") or []):
        if not isinstance(profile, dict):
            continue
        if _has_derived_reasoning(profile) or profile.get("unknown_scope"):
            continue
        profile["unknown_scope"] = [
            {
                "statement": _RECONCILIATION_BRIDGE_STATEMENT,
                "evidence_status": "unknown_or_unsupported",
                "evidence": [],
                "rationale": (
                    "Internal compatibility bridge for historical reconciliation; removed before "
                    "Capability v9 persistence."
                ),
                "confidence": "high",
            }
        ]
        bridged_profile_indices.append(index)

    legacy_draft = CapabilityReasoningDraft.model_validate(
        bridge_payload,
        context={
            "analysis_fields": analysis_fields,
            "evidence_catalog": evidence_catalog or {},
            "accepted_extraction": accepted_extraction,
        },
    )
    legacy_reconciled = reconcile_capability_intelligence(
        legacy_draft,
        accepted_extraction=accepted_extraction,
        analysis_fields=analysis_fields,
        evidence_catalog=evidence_catalog,
    )
    payload = legacy_reconciled.model_dump(mode="json")
    for index in bridged_profile_indices:
        profile = payload["capabilities"][index]
        profile["unknown_scope"] = [
            item
            for item in profile.get("unknown_scope") or []
            if item.get("statement") != _RECONCILIATION_BRIDGE_STATEMENT
        ]

    payload = build_v9_intelligence(payload)
    return JobCapabilityIntelligenceV9.model_validate(
        payload,
        context={
            "analysis_fields": analysis_fields,
            "evidence_catalog": evidence_catalog or {},
            "accepted_extraction": accepted_extraction,
        },
    )


__all__ = [
    "CapabilityAssignmentPartitionV9",
    "CapabilityFactAssignmentV9",
    "CapabilityGroupPlanV9",
    "CapabilityGroupSeedV8",
    "CapabilityProfileReasoningV9",
    "CapabilityProfileV9",
    "CapabilityReasoningDraftV9",
    "CapabilitySourceTruthV9",
    "JobCapabilityIntelligenceV9",
    "assignment_partitions",
    "build_v9_intelligence",
    "reconcile_capability_intelligence_v9",
]
