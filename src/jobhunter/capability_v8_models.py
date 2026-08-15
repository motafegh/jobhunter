"""Bounded planning and per-profile reasoning contracts for Capability v8."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, model_validator

from jobhunter.capability_models import CapabilityExpectation

_DERIVED_STATUSES = {"strongly_implied_by_work", "model_inferred_prerequisite"}


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CapabilityGroupSeedV8(_StrictModel):
    group_id: int = Field(ge=0, le=7)
    capability_label: str = Field(min_length=2, max_length=160)
    summary: str = Field(min_length=12, max_length=1200)


class CapabilityGroupPlanV8(_StrictModel):
    """Small semantic plan; it deliberately owns no source-index coverage bookkeeping."""

    role_interpretation: str = Field(min_length=12, max_length=1600)
    groups: list[CapabilityGroupSeedV8] = Field(min_length=1, max_length=6)
    uncertainties: list[str] = Field(default_factory=list, max_length=12)

    @model_validator(mode="after")
    def validate_group_plan(self, info: ValidationInfo) -> CapabilityGroupPlanV8:
        group_ids = [group.group_id for group in self.groups]
        if len(group_ids) != len(set(group_ids)):
            raise ValueError("Capability group IDs must be unique")
        normalized_labels = [" ".join(group.capability_label.split()).casefold() for group in self.groups]
        if len(normalized_labels) != len(set(normalized_labels)):
            raise ValueError("Capability group labels must be distinct")

        context = info.context or {}
        requirement_count = int(context.get("capability_requirement_count") or 0)
        responsibility_count = int(context.get("responsibility_count") or 0)
        if requirement_count >= 12 and responsibility_count >= 5 and len(self.groups) < 2:
            raise ValueError("Dense jobs require at least two capability groups")
        return self


class CapabilityFactAssignmentV8(_StrictModel):
    index: int = Field(ge=0)
    group_ids: list[int] = Field(min_length=1, max_length=2)

    @model_validator(mode="after")
    def unique_groups(self) -> CapabilityFactAssignmentV8:
        if len(self.group_ids) != len(set(self.group_ids)):
            raise ValueError("Assignment group_ids must be unique")
        return self


class CapabilityAssignmentPartitionV8(_StrictModel):
    """Exact assignment of one bounded partition of known source facts."""

    requirement_assignments: list[CapabilityFactAssignmentV8]
    responsibility_assignments: list[CapabilityFactAssignmentV8]

    @model_validator(mode="after")
    def validate_partition(self, info: ValidationInfo) -> CapabilityAssignmentPartitionV8:
        context = info.context or {}
        owned_requirements = set(context.get("owned_requirement_indices") or [])
        owned_responsibilities = set(context.get("owned_responsibility_indices") or [])
        valid_group_ids = set(context.get("valid_group_ids") or [])

        requirement_indices = [item.index for item in self.requirement_assignments]
        responsibility_indices = [item.index for item in self.responsibility_assignments]
        if len(requirement_indices) != len(set(requirement_indices)):
            raise ValueError("Requirement assignment indices must be unique")
        if len(responsibility_indices) != len(set(responsibility_indices)):
            raise ValueError("Responsibility assignment indices must be unique")
        if set(requirement_indices) != owned_requirements:
            raise ValueError(
                "Assignment partition must cover exactly its owned requirement indices: "
                f"expected={sorted(owned_requirements)} actual={sorted(requirement_indices)}"
            )
        if set(responsibility_indices) != owned_responsibilities:
            raise ValueError(
                "Assignment partition must cover exactly its owned responsibility indices: "
                f"expected={sorted(owned_responsibilities)} actual={sorted(responsibility_indices)}"
            )

        for item in [*self.requirement_assignments, *self.responsibility_assignments]:
            invalid = sorted(set(item.group_ids) - valid_group_ids)
            if invalid:
                raise ValueError(f"Assignment references unknown capability groups: {invalid}")
        return self


def _expectation_statuses(items: list[CapabilityExpectation]) -> set[str]:
    return {item.evidence_status for item in items}


class CapabilityProfileReasoningV8(_StrictModel):
    """Model-owned reasoning for one already-linked capability group.

    Source links, source-explicit strength, depth, and responsibilities are intentionally absent.
    JobHunter adds those deterministically after the group has been reasoned about.
    """

    summary: str = Field(min_length=12, max_length=1600)
    depth_signals: list[CapabilityExpectation] = Field(default_factory=list, max_length=8)
    work_activities: list[CapabilityExpectation] = Field(default_factory=list, max_length=8)
    sub_capabilities: list[CapabilityExpectation] = Field(default_factory=list, max_length=12)
    underlying_knowledge: list[CapabilityExpectation] = Field(default_factory=list, max_length=10)
    operational_practices: list[CapabilityExpectation] = Field(default_factory=list, max_length=10)
    operational_context: list[CapabilityExpectation] = Field(default_factory=list, max_length=8)
    unknown_scope: list[CapabilityExpectation] = Field(default_factory=list, max_length=10)
    overall_confidence: str
    uncertainties: list[str] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    def validate_reasoning_boundary(self) -> CapabilityProfileReasoningV8:
        for field_name in (
            "depth_signals",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            invalid = _expectation_statuses(getattr(self, field_name)) - _DERIVED_STATUSES
            if invalid:
                raise ValueError(
                    f"{field_name} may contain only derived reasoning statuses in Capability v8: "
                    f"{sorted(invalid)}"
                )
        if any(item.evidence_status != "unknown_or_unsupported" for item in self.unknown_scope):
            raise ValueError("unknown_scope items must use unknown_or_unsupported")
        if self.overall_confidence not in {"high", "medium", "low"}:
            raise ValueError("overall_confidence must be high, medium, or low")

        derived = [
            *self.depth_signals,
            *self.work_activities,
            *self.sub_capabilities,
            *self.underlying_knowledge,
            *self.operational_practices,
            *self.operational_context,
        ]
        if not derived and not self.unknown_scope:
            raise ValueError(
                "Capability profile reasoning must add derived reasoning or an explicit unknown "
                "boundary"
            )
        return self


def assignment_partitions(
    capability_requirement_indices: list[int],
    responsibility_count: int,
    *,
    requirement_chunk_size: int = 8,
) -> list[tuple[list[int], list[int]]]:
    """Create deterministic bounded assignment partitions without dropping any source fact."""

    if requirement_chunk_size < 1:
        raise ValueError("requirement_chunk_size must be positive")
    requirement_chunks = [
        capability_requirement_indices[index : index + requirement_chunk_size]
        for index in range(0, len(capability_requirement_indices), requirement_chunk_size)
    ]
    if not requirement_chunks:
        requirement_chunks = [[]]

    responsibility_indices = list(range(responsibility_count))
    responsibility_buckets = [[] for _ in requirement_chunks]
    for offset, responsibility_index in enumerate(responsibility_indices):
        responsibility_buckets[offset % len(responsibility_buckets)].append(responsibility_index)

    return [
        (requirements, responsibility_buckets[index])
        for index, requirements in enumerate(requirement_chunks)
    ]


__all__ = [
    "CapabilityAssignmentPartitionV8",
    "CapabilityFactAssignmentV8",
    "CapabilityGroupPlanV8",
    "CapabilityGroupSeedV8",
    "CapabilityProfileReasoningV8",
    "assignment_partitions",
]
