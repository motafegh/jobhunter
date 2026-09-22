"""Candidate P1.6 v22 contract with ontology abstention.

V22 keeps every v21 source/evidence/depth/coverage guard. Its only new deterministic
normalization is narrow: when the model labels a requirement as experience but the
exact candidate item does not prove prior applied exposure, preserve the source-backed
requirement and abstain from the unsupported ontology label by using concept_type=other.

This does not infer a replacement semantic type. Explicit source-backed experience
and exact checklist items typed as experience remain experience.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference.instructor_lm_studio_v20 import _PRIOR_APPLIED_EXPOSURE_RE
from jobhunter.inference.instructor_lm_studio_v19 import _raw_evidence_text
from jobhunter.inference.instructor_lm_studio_v21 import (
    AnalysisRequirementV21,
    JobAnalysisResponseV21,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_WORKING_WITH_EXPOSURE_RE = re.compile(r"\bworking\s+with\b", re.I)


def _exact_item_is_source_proven_experience(
    *,
    item_excerpt: str,
    evidence: str,
    plan: dict[str, Any],
) -> bool:
    """Return true only when exact source scope proves prior applied exposure."""

    if _PRIOR_APPLIED_EXPOSURE_RE.search(item_excerpt) is not None:
        return True
    if _WORKING_WITH_EXPOSURE_RE.search(item_excerpt) is not None:
        return True

    normalized_item = " ".join(item_excerpt.split()).casefold()
    for candidate in plan.values():
        if not isinstance(candidate, dict) or str(candidate.get("text") or "") != evidence:
            continue
        for required in candidate.get("required_item_excerpts") or []:
            if not isinstance(required, dict):
                continue
            if str(required.get("required_concept_type") or "") != "experience":
                continue
            required_text = " ".join(str(required.get("text") or "").split()).casefold()
            if required_text == normalized_item:
                return True
    return False


class AnalysisRequirementV22(AnalysisRequirementV21):
    """Preserve factual requirements while abstaining from unproven experience typing."""

    @model_validator(mode="before")
    @classmethod
    def abstain_from_unproven_experience(
        cls,
        value: Any,
        info: ValidationInfo,
    ) -> Any:
        if not isinstance(value, dict) or value.get("concept_type") != "experience":
            return value
        if (info.context or {}).get("analysis_mode") != "english":
            return value

        item_excerpt = str(value.get("item_excerpt") or "")
        evidence = _raw_evidence_text(value, info)
        plan = (info.context or {}).get("requirement_coverage_plan") or {}
        if _exact_item_is_source_proven_experience(
            item_excerpt=item_excerpt,
            evidence=evidence,
            plan=plan if isinstance(plan, dict) else {},
        ):
            return value

        normalized = dict(value)
        normalized["concept_type"] = "other"
        return normalized


class JobAnalysisResponseV22(JobAnalysisResponseV21):
    """V21 response contract plus deterministic ontology abstention."""

    requirements: list[AnalysisRequirementV22] = Field()


def complete_analysis_partition_with_instructor_v22(
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
    """Run v22 through the proven shared v20 transport."""

    from jobhunter.inference import instructor_lm_studio_v20 as v20

    additional_evidence_catalog = {
        reference: str(candidate.get("text") or "")
        for reference, candidate in requirement_coverage_plan.items()
    }
    additional_evidence_catalog.update(responsibility_coverage_plan)
    candidate_payload = dict(user_payload)
    candidate_payload["exact_item_coverage"] = [
        {
            "parent_reference": reference,
            "item_excerpt": required.get("text"),
            "required_concept_type": required.get("required_concept_type"),
        }
        for reference, candidate in requirement_coverage_plan.items()
        for required in candidate.get("required_item_excerpts") or []
        if isinstance(required, dict)
    ]
    result = v20._complete_analysis_partition_with_instructor(
        base_url=base_url,
        api_token=api_token,
        timeout_seconds=timeout_seconds,
        network_retries=network_retries,
        selected_model=selected_model,
        system_prompt=system_prompt,
        user_payload=candidate_payload,
        max_tokens=max_tokens,
        seed=seed,
        requirement_coverage_plan=requirement_coverage_plan,
        responsibility_coverage_plan=responsibility_coverage_plan,
        response_model=JobAnalysisResponseV22,
        contract_version="v22",
        validation_retries=validation_retries,
        additional_evidence_catalog=additional_evidence_catalog,
    )
    request_body = dict(result.request_body)
    runtime = dict(request_body.get("runtime") or {})
    runtime["p16_v21_item_scoped_evidence"] = True
    runtime["p16_v22_ontology_abstention"] = True
    request_body["runtime"] = runtime
    return StructuredInferenceResult(
        model=result.model,
        structured=result.structured,
        request_body=request_body,
        raw_response=result.raw_response,
        finish_reason=result.finish_reason,
    )


__all__ = [
    "AnalysisRequirementV22",
    "JobAnalysisResponseV22",
    "_exact_item_is_source_proven_experience",
    "complete_analysis_partition_with_instructor_v22",
    "persisted_v20_shape",
]
