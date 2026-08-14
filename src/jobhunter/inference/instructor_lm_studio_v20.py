"""Partition-scoped Instructor helper for dense P1.6 v20 extraction.

V20 keeps the full evidence catalog available for grounding but gives each model call a bounded,
explicit subset of requirement/responsibility coverage. This prevents a correction for one dense
subset from replacing another already-correct subset.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI

from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    evidence_reference_payload,
    requirement_coverage_payload,
    responsibility_coverage_payload,
)
from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError
from jobhunter.inference.instructor_lm_studio import _leaf_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v19 import JobAnalysisResponseV19
from jobhunter.inference.lm_studio import StructuredInferenceResult


def _validated_partition_plan(
    plan: dict[str, dict[str, Any]],
    catalog: dict[str, str],
    *,
    label: str,
) -> dict[str, dict[str, Any]]:
    validated: dict[str, dict[str, Any]] = {}
    for reference, candidate in plan.items():
        evidence = catalog.get(reference)
        if evidence is None:
            raise InferenceResponseError(
                f"P1.6 v20 {label} partition references unknown evidence: {reference}"
            )
        if str(candidate.get("text") or "") != evidence:
            raise InferenceResponseError(
                f"P1.6 v20 {label} partition text is not exact evidence: {reference}"
            )
        validated[reference] = dict(candidate)
    return validated


def complete_analysis_partition_with_instructor_v20(
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
    """Run one bounded semantic extraction partition with exact JobHunter coverage context."""

    if not 0 <= validation_retries <= 3:
        raise ValueError("validation_retries must be between 0 and 3")
    analysis_fields = user_payload.get("analysis_fields")
    if not isinstance(analysis_fields, dict):
        raise InferenceResponseError(
            "P1.6 v20 Instructor partition requires dictionary analysis_fields"
        )

    evidence_catalog = build_field_evidence_catalog(analysis_fields)
    model_evidence_catalog = _leaf_evidence_catalog(evidence_catalog)
    requirement_plan = _validated_partition_plan(
        requirement_coverage_plan,
        evidence_catalog,
        label="requirement",
    )
    raw_responsibility_plan = {
        reference: {"text": text}
        for reference, text in responsibility_coverage_plan.items()
    }
    _validated_partition_plan(
        raw_responsibility_plan,
        evidence_catalog,
        label="responsibility",
    )
    responsibility_plan = dict(responsibility_coverage_plan)

    enriched_payload = dict(user_payload)
    enriched_payload.pop("analysis_fields", None)
    enriched_payload["analysis_field_names"] = sorted(analysis_fields)
    enriched_payload["evidence_references"] = evidence_reference_payload(
        model_evidence_catalog
    )
    enriched_payload["requirement_coverage"] = requirement_coverage_payload(
        requirement_plan
    )
    enriched_payload["responsibility_coverage"] = responsibility_coverage_payload(
        responsibility_plan
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
            response_model=JobAnalysisResponseV19,
            messages=messages,
            context={
                "analysis_fields": analysis_fields,
                "evidence_catalog": evidence_catalog,
                "analysis_mode": user_payload.get("analysis_mode"),
                "requirement_coverage_plan": requirement_plan,
                "responsibility_coverage_plan": responsibility_plan,
            },
            max_retries=validation_retries,
            temperature=0,
            seed=seed,
            max_tokens=max_tokens,
        )
    except (APIConnectionError, APITimeoutError) as exc:
        raise InferenceConnectionError(
            f"Could not reach LM Studio for P1.6 v20 partition: {exc}"
        ) from exc
    except Exception as exc:
        raise InferenceResponseError(
            "Instructor could not produce a JobHunter-valid P1.6 v20 partition "
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
            "p16_v20_requirement_partition_refs": sorted(requirement_plan),
            "p16_v20_responsibility_partition_refs": sorted(responsibility_plan),
        },
        "instructor": {
            "mode": "JSON_SCHEMA",
            "response_model": "JobAnalysisResponseV19",
            "validation_retries": validation_retries,
            "schema": JobAnalysisResponseV19.model_json_schema(),
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
    "_validated_partition_plan",
    "complete_analysis_partition_with_instructor_v20",
]
