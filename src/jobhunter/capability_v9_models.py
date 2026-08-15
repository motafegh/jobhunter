"""Capability v9 semantic guardrails and corrected source-truth accounting."""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator

from jobhunter.capability_models import CapabilityExpectation
from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft,
    CapabilitySourcePurpose,
    CapabilitySourceRequirement,
    CapabilitySourceResponsibility,
)
from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityFactAssignmentV8,
    CapabilityGroupPlanV8,
    CapabilityGroupSeedV8,
    CapabilityProfileReasoningV8,
    assignment_partitions,
)

_DEPTH_INFLATION_RE = re.compile(
    r"\b(?:advanced|expert(?:ise)?|proficien(?:t|cy)|mastery|strong|solid|hands-on)\b",
    re.IGNORECASE,
)
_OBLIGATION_RE = re.compile(
    r"\b(?:requires?|required|must|mandatory|mandates?|mandated|necessar(?:y|ily)|"
    r"necessitates?|prerequisite)\b",
    re.IGNORECASE,
)
_SCOPE_INFLATION_RE = re.compile(
    r"\b(?:end[- ]to[- ]end|full lifecycle|ownership|owning|owns|leadership|leading|"
    r"autonomy|autonomous|architecting|architecture)\b",
    re.IGNORECASE,
)
_DEEP_RE = re.compile(r"\bdeep\b", re.IGNORECASE)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _without_deep_learning(value: str) -> str:
    return re.sub(r"\bdeep\s+learning\b", "learning", value, flags=re.IGNORECASE)


def _guard_model_owned_text(
    value: str,
    *,
    field_name: str,
    allow_depth_language: bool = False,
) -> None:
    if _OBLIGATION_RE.search(value):
        raise ValueError(
            f"{field_name} may not restate requirement obligation; JobHunter owns strength"
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
    """Bounded profile reasoning that cannot override deterministic source semantics."""

    @model_validator(mode="after")
    def guard_profile_semantics(self, info: ValidationInfo) -> CapabilityProfileReasoningV9:
        _guard_model_owned_text(self.summary, field_name="profile.summary")

        for field_name in (
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            for item in getattr(self, field_name):
                _guard_model_owned_text(
                    item.statement,
                    field_name=f"{field_name}.statement",
                )
                _guard_model_owned_text(
                    item.rationale,
                    field_name=f"{field_name}.rationale",
                )
                _validate_prerequisite_optionality(item, info, field_name=field_name)

        for item in self.depth_signals:
            _guard_model_owned_text(
                item.statement,
                field_name="depth_signals.statement",
                allow_depth_language=True,
            )
            _guard_model_owned_text(
                item.rationale,
                field_name="depth_signals.rationale",
                allow_depth_language=True,
            )
            _validate_prerequisite_optionality(item, info, field_name="depth_signals")
        return self


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


class JobCapabilityIntelligenceV9(CapabilityReasoningDraft):
    source_truth: CapabilitySourceTruthV9


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
    payload["source_truth"] = transformed
    return JobCapabilityIntelligenceV9.model_validate(payload).model_dump(mode="json")


__all__ = [
    "CapabilityAssignmentPartitionV9",
    "CapabilityFactAssignmentV9",
    "CapabilityGroupPlanV9",
    "CapabilityGroupSeedV8",
    "CapabilityProfileReasoningV9",
    "CapabilitySourceTruthV9",
    "JobCapabilityIntelligenceV9",
    "assignment_partitions",
    "build_v9_intelligence",
]
