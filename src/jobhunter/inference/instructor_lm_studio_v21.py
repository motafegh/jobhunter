"""Isolated P1.6 candidate contract for item-scoped source evidence.

This response model is not wired to a provider or a persisted artifact contract.
It tests whether broad coverage and exact item scope can remain separate before
changing the accepted v20/v5 path.
"""

from __future__ import annotations

from typing import Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.evidence_refs import (
    evidence_mixes_english_optionality,
    has_english_optionality_signal,
)
from jobhunter.inference.instructor_lm_studio_v20 import (
    AnalysisRequirementV20,
    JobAnalysisResponseV20,
    _depth_matches,
    _validate_depth_fields_v20,
)


class AnalysisRequirementV21(AnalysisRequirementV20):
    """Retain parent coverage while validating depth against one exact item excerpt."""

    item_excerpt: str = Field(min_length=2)

    @model_validator(mode="after")
    def validate_requirement_semantics(self, info: ValidationInfo) -> Self:
        if self.item_excerpt not in self.evidence:
            raise ValueError("item_excerpt must be an exact contiguous source subspan of evidence")

        if self.requirement_type == "inferred" and not self.rationale.strip():
            raise ValueError("Inferred requirements require a concise non-empty rationale")

        if (info.context or {}).get("analysis_mode") != "english":
            return self

        if evidence_mixes_english_optionality(self.item_excerpt):
            raise ValueError("One item excerpt cannot mix core and optional wording")

        plan = (info.context or {}).get("requirement_coverage_plan") or {}
        parent_hints = {
            str(candidate.get("obligation_hint") or "")
            for candidate in plan.values()
            if isinstance(candidate, dict) and candidate.get("text") == self.evidence
        }
        if "preferred" in parent_hints and self.requirement_type != "preferred":
            raise ValueError("Preferred parent coverage requires preferred item strength")
        if self.requirement_type == "preferred" and not (
            has_english_optionality_signal(self.item_excerpt)
            or ("preferred" in parent_hints and has_english_optionality_signal(self.evidence))
        ):
            raise ValueError("Preferred item needs exact source preference in item or parent")

        if self.depth_signal is None and _depth_matches(self.item_excerpt):
            raise ValueError("Explicit item depth must be supplied, not borrowed or omitted")
        self.depth_signal = _validate_depth_fields_v20(
            self.concept, self.depth_signal, self.item_excerpt
        )
        return self


class JobAnalysisResponseV21(JobAnalysisResponseV20):
    """Candidate response retaining v20 aggregate coverage with scoped requirements."""

    requirements: list[AnalysisRequirementV21] = Field()


def persisted_v20_shape(structured: dict[str, object]) -> dict[str, object]:
    """Remove candidate-only scope fields before any v5 persistence validation."""

    result = dict(structured)
    requirements = result.get("requirements")
    if not isinstance(requirements, list):
        return result
    result["requirements"] = [
        {key: value for key, value in item.items() if key != "item_excerpt"}
        if isinstance(item, dict)
        else item
        for item in requirements
    ]
    return result


__all__ = [
    "AnalysisRequirementV21",
    "JobAnalysisResponseV21",
    "persisted_v20_shape",
]
