"""Capability v9 public model boundary over the preserved core implementation."""

from __future__ import annotations

from pydantic import model_validator

from jobhunter.capability_models import CapabilityExpectation
from jobhunter.capability_v9_models_core import (
    CapabilityAssignmentPartitionV9,
    CapabilityFactAssignmentV9,
    CapabilityGroupPlanV9,
    CapabilityGroupSeedV8,
    CapabilityProfileReasoningV9 as _CapabilityProfileReasoningV9Core,
    CapabilityProfileV9,
    CapabilityReasoningDraftV9,
    CapabilitySourceTruthV9,
    JobCapabilityIntelligenceV9,
    assignment_partitions,
    build_v9_intelligence,
    reconcile_capability_intelligence_v9,
)

_DERIVED_STATUSES = {"strongly_implied_by_work", "model_inferred_prerequisite"}


class CapabilityProfileReasoningV9(_CapabilityProfileReasoningV9Core):
    """Inference-facing v9 profile that treats source echoes as redundant, not invalid."""

    @model_validator(mode="after")
    def validate_reasoning_boundary(self) -> CapabilityProfileReasoningV9:
        """Keep optional inference only; deterministic reconciliation owns source-explicit truth."""

        discarded_source_or_misplaced = 0
        for field_name in (
            "depth_signals",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            items: list[CapabilityExpectation] = getattr(self, field_name)
            kept = [item for item in items if item.evidence_status in _DERIVED_STATUSES]
            discarded_source_or_misplaced += len(items) - len(kept)
            setattr(self, field_name, kept)

        unknown_kept = [
            item
            for item in self.unknown_scope
            if item.evidence_status == "unknown_or_unsupported"
        ]
        discarded_source_or_misplaced += len(self.unknown_scope) - len(unknown_kept)
        self.unknown_scope = unknown_kept

        if self.overall_confidence not in {"high", "medium", "low"}:
            raise ValueError("overall_confidence must be high, medium, or low")

        if discarded_source_or_misplaced:
            note = (
                "JobHunter discarded "
                f"{discarded_source_or_misplaced} redundant or misplaced model expectation(s) "
                "whose evidence status belongs to deterministic source truth or another section."
            )
            if note not in self.uncertainties:
                self.uncertainties.append(note)
        return self


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
