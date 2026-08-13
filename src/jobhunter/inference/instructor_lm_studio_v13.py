"""Candidate-only Instructor path for P1.6 v13 deterministic decomposition.

The production Instructor path remains unchanged. This helper differs only in one place: callers
may supply a set of requirement-coverage references that JobHunter has already proved are coarse
spans deterministically superseded by finer exact evidence. Those references are removed from the
model/Pydantic coverage obligation while all evidence remains available for grounding.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI

from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
    evidence_reference_payload,
    requirement_coverage_payload,
    responsibility_coverage_payload,
)
from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError
from jobhunter.inference.instructor_lm_studio import (
    JobAnalysisResponse,
    _leaf_evidence_catalog,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


def filtered_requirement_coverage_plan(
    analysis_fields: dict[str, Any],
    suppressed_references: list[str],
) -> dict[str, dict[str, Any]]:
    """Filter only mechanically excludable coverage refs; fail closed on unsafe suppression."""

    plan = build_requirement_coverage_plan(analysis_fields)
    requested = {reference.strip() for reference in suppressed_references if reference.strip()}
    unknown = sorted(requested - set(plan))
    if unknown:
        raise InferenceResponseError(
            "P1.6 v13 requested suppression for unknown coverage references: "
            + ", ".join(unknown)
        )
    unsafe = sorted(
        reference
        for reference in requested
        if not bool(plan[reference].get("allow_exclusion", False))
    )
    if unsafe:
        raise InferenceResponseError(
            "P1.6 v13 cannot suppress non-excludable coverage references: "
            + ", ".join(unsafe)
        )
    return {
        reference: candidate
        for reference, candidate in plan.items()
        if reference not in requested
    }


def complete_analysis_with_instructor_v13(
    *,
    base_url: str,
    api_token: str | None,
    timeout_seconds: float,
    network_retries: int,
    selected_model: str,
    system_prompt: str,
    user_payload: dict[str, Any],
    schema: dict[str, Any],
    max_tokens: int,
    seed: int,
    suppressed_requirement_coverage_references: list[str],
    validation_retries: int = 1,
) -> StructuredInferenceResult:
    """Run the typed analysis path with deterministic coarse coverage removed from model duty."""

    if not 0 <= validation_retries <= 3:
        raise ValueError("validation_retries must be between 0 and 3")
    analysis_fields = user_payload.get("analysis_fields")
    if not isinstance(analysis_fields, dict):
        raise InferenceResponseError(
            "Instructor analysis requires dictionary analysis_fields"
        )

    evidence_catalog = build_field_evidence_catalog(analysis_fields)
    model_evidence_catalog = _leaf_evidence_catalog(evidence_catalog)
    requirement_coverage_plan = filtered_requirement_coverage_plan(
        analysis_fields,
        suppressed_requirement_coverage_references,
    )
    responsibility_coverage_plan = build_responsibility_coverage_plan(analysis_fields)

    enriched_payload = dict(user_payload)
    enriched_payload.pop("analysis_fields", None)
    enriched_payload["analysis_field_names"] = sorted(analysis_fields)
    enriched_payload["evidence_references"] = evidence_reference_payload(
        model_evidence_catalog
    )
    enriched_payload["requirement_coverage"] = requirement_coverage_payload(
        requirement_coverage_plan
    )
    enriched_payload["responsibility_coverage"] = responsibility_coverage_payload(
        responsibility_coverage_plan
    )

    connect_timeout = min(float(timeout_seconds), 10.0)
    timeout = httpx.Timeout(
        connect=connect_timeout,
        read=None,
        write=30.0,
        pool=30.0,
    )
    http_client = httpx.Client(timeout=timeout, trust_env=False)
    openai_client = OpenAI(
        base_url=base_url,
        api_key=api_token or "lm-studio-local",
        timeout=timeout,
        max_retries=0,
        http_client=http_client,
    )
    client = instructor.from_openai(openai_client, mode=instructor.Mode.JSON_SCHEMA)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps(enriched_payload, ensure_ascii=False, sort_keys=True),
        },
    ]

    try:
        result, completion = client.create_with_completion(
            model=selected_model,
            response_model=JobAnalysisResponse,
            messages=messages,
            context={
                "analysis_fields": analysis_fields,
                "evidence_catalog": evidence_catalog,
                "analysis_mode": user_payload.get("analysis_mode"),
                "requirement_coverage_plan": requirement_coverage_plan,
                "responsibility_coverage_plan": responsibility_coverage_plan,
            },
            max_retries=validation_retries,
            temperature=0,
            seed=seed,
            max_tokens=max_tokens,
        )
    except (APIConnectionError, APITimeoutError) as exc:
        raise InferenceConnectionError(
            f"Could not reach LM Studio for Instructor analysis: {exc}"
        ) from exc
    except Exception as exc:
        raise InferenceResponseError(
            "Instructor could not produce a JobHunter-valid structured analysis "
            f"after {validation_retries} bounded validation retries: {exc}"
        ) from exc
    finally:
        http_client.close()

    structured = result.model_dump(mode="json")
    raw_response = completion.model_dump(mode="json")
    finish_reason = completion.choices[0].finish_reason if completion.choices else None
    request_body = {
        "model": selected_model,
        "messages": messages,
        "temperature": 0,
        "seed": seed,
        "max_tokens": max_tokens,
        "stream": False,
        "runtime": {
            "read_timeout_seconds": None,
            "connect_timeout_seconds": connect_timeout,
            "transport_retries": 0,
            "configured_network_retries": network_retries,
            "deterministic_decomposition_suppressed_coverage": sorted(
                suppressed_requirement_coverage_references
            ),
        },
        "instructor": {
            "mode": "JSON_SCHEMA",
            "response_model": "JobAnalysisResponse",
            "validation_retries": validation_retries,
            "schema": JobAnalysisResponse.model_json_schema(),
        },
    }

    return StructuredInferenceResult(
        model=selected_model,
        structured=structured,
        request_body=request_body,
        raw_response=raw_response,
        finish_reason=str(finish_reason) if finish_reason is not None else None,
    )


__all__ = [
    "complete_analysis_with_instructor_v13",
    "filtered_requirement_coverage_plan",
]
