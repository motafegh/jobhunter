"""Offline runtime boundary for the isolated P1.6 v21 scoped-evidence candidate."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v20 import (
    V20CandidateAnalysisProvider,
    _v20_requirement_partitions,
)
from jobhunter.evidence_refs_v21 import (
    build_requirement_coverage_plan_v21,
    build_responsibility_coverage_plan_v21,
)
from jobhunter.inference.instructor_lm_studio_v21 import (
    complete_analysis_partition_with_instructor_v21,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


def _v21_requirement_partitions(
    plan: dict[str, dict[str, Any]],
) -> list[dict[str, dict[str, Any]]]:
    """Keep explicit headingless candidate experience out of dense section partitions."""

    section_plan = {
        reference: candidate
        for reference, candidate in plan.items()
        if candidate.get("source_kind") != "candidate_experience"
    }
    candidate_experience_plan = {
        reference: candidate
        for reference, candidate in plan.items()
        if candidate.get("source_kind") == "candidate_experience"
    }
    partitions: list[dict[str, dict[str, Any]]] = []
    if section_plan:
        partitions.extend(_v20_requirement_partitions(section_plan))
    if candidate_experience_plan:
        partitions.extend(_v20_requirement_partitions(candidate_experience_plan))
    return partitions


class V21CandidateAnalysisProvider(V20CandidateAnalysisProvider):
    """Use v21 validation while returning the unchanged v5 persistable shape."""

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        return complete_analysis_partition_with_instructor_v21(**kwargs)

    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return build_requirement_coverage_plan_v21(model_fields)

    def _responsibility_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, str]:
        return build_responsibility_coverage_plan_v21(model_fields)

    def _requirement_partitions(
        self, plan: dict[str, dict[str, Any]]
    ) -> list[dict[str, dict[str, Any]]]:
        return _v21_requirement_partitions(plan)

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        persisted = persisted_v20_shape(structured)
        return {str(key): value for key, value in persisted.items()}


__all__ = ["V21CandidateAnalysisProvider", "_v21_requirement_partitions"]
