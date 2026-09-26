"""Isolated v23 provider using the v22 fail-closed source-fact response model."""

from __future__ import annotations

from typing import Any

from jobhunter.inference import instructor_lm_studio_v20 as v20
from jobhunter.inference.instructor_lm_studio_v22 import (
    JobAnalysisResponseV22,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


def complete_analysis_partition_with_instructor_v23(
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
        contract_version="v23",
        validation_retries=validation_retries,
        additional_evidence_catalog=additional_evidence_catalog,
    )
    request_body = dict(result.request_body)
    runtime = dict(request_body.get("runtime") or {})
    runtime["p16_v21_item_scoped_evidence"] = True
    runtime["p16_v22_ontology_abstention"] = True
    runtime["p16_v23_candidate_proof_coverage"] = True
    request_body["runtime"] = runtime
    return StructuredInferenceResult(
        model=result.model,
        structured=result.structured,
        request_body=request_body,
        raw_response=result.raw_response,
        finish_reason=result.finish_reason,
    )


__all__ = [
    "complete_analysis_partition_with_instructor_v23",
    "persisted_v20_shape",
]
