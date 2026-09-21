"""Isolated P1.6 candidate contract for item-scoped source evidence.

This response model is not wired to a provider or a persisted artifact contract.
It tests whether broad coverage and exact item scope can remain separate before
changing the accepted v20/v5 path.
"""

from __future__ import annotations

import re
from typing import Any, Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.evidence_refs import (
    evidence_mixes_english_optionality,
    has_english_optionality_signal,
)
from jobhunter.inference.instructor_lm_studio import _equivalent_source_excerpt
from jobhunter.inference.instructor_lm_studio_v20 import (
    AnalysisRequirementV20,
    JobAnalysisResponseV20,
    _depth_matches,
    _validate_depth_fields_v20,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


def _canonicalize_scoped_leading_depth(
    concept: str,
    depth_signal: str | None,
    item_excerpt: str,
) -> tuple[str, str | None]:
    """Move one source-proven leading marker out of a generated concept."""

    if depth_signal is not None:
        return concept, depth_signal
    matches = _depth_matches(item_excerpt)
    if len(matches) != 1:
        return concept, depth_signal
    marker = matches[0][2]
    prefix = re.compile(
        rf"^\s*{re.escape(marker)}(?:\s+(?:with|in|of))?\s+",
        re.I,
    )
    scoped_concept = prefix.sub("", concept, count=1).strip(" ,;:-/")
    if not scoped_concept or scoped_concept == concept:
        return concept, depth_signal
    return scoped_concept, marker


class AnalysisRequirementV21(AnalysisRequirementV20):
    """Retain parent coverage while validating depth against one exact item excerpt."""

    item_excerpt: str = Field(min_length=2)

    @model_validator(mode="after")
    def validate_requirement_semantics(self, info: ValidationInfo) -> Self:
        canonical_item = _equivalent_source_excerpt(self.item_excerpt, self.evidence)
        if canonical_item is None:
            raise ValueError("item_excerpt must be an exact contiguous source subspan of evidence")
        self.item_excerpt = canonical_item

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

        self.concept, self.depth_signal = _canonicalize_scoped_leading_depth(
            self.concept,
            self.depth_signal,
            self.item_excerpt,
        )
        if self.depth_signal is None and _depth_matches(self.item_excerpt):
            raise ValueError("Explicit item depth must be supplied, not borrowed or omitted")
        self.depth_signal = _validate_depth_fields_v20(
            self.concept, self.depth_signal, self.item_excerpt
        )
        return self


class JobAnalysisResponseV21(JobAnalysisResponseV20):
    """Candidate response retaining v20 aggregate coverage with scoped requirements."""

    requirements: list[AnalysisRequirementV21] = Field()


def complete_analysis_partition_with_instructor_v21(
    *,
    base_url: str,
    api_token: str | None,
    timeout_seconds: float,
    network_retries: int,
    selected_model: str,
    system_prompt: str,
    user_payload: dict[str, Any],
    max_tokens: int,
    seed: int,
    requirement_coverage_plan: dict[str, dict[str, Any]],
    responsibility_coverage_plan: dict[str, str],
    validation_retries: int = 1,
) -> StructuredInferenceResult:
    """Run the isolated v21 response contract through the proven v20 transport."""

    # Import the module so tests and later runtime wiring can replace the shared
    # transport without hiding a second network implementation in this candidate.
    from jobhunter.inference import instructor_lm_studio_v20 as v20

    additional_evidence_catalog = {
        reference: str(candidate.get("text") or "")
        for reference, candidate in requirement_coverage_plan.items()
    }
    additional_evidence_catalog.update(responsibility_coverage_plan)
    return v20._complete_analysis_partition_with_instructor(
        base_url=base_url,
        api_token=api_token,
        timeout_seconds=timeout_seconds,
        network_retries=network_retries,
        selected_model=selected_model,
        system_prompt=system_prompt,
        user_payload=user_payload,
        max_tokens=max_tokens,
        seed=seed,
        requirement_coverage_plan=requirement_coverage_plan,
        responsibility_coverage_plan=responsibility_coverage_plan,
        response_model=JobAnalysisResponseV21,
        contract_version="v21",
        validation_retries=validation_retries,
        additional_evidence_catalog=additional_evidence_catalog,
    )


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
    "_canonicalize_scoped_leading_depth",
    "complete_analysis_partition_with_instructor_v21",
    "persisted_v20_shape",
]
