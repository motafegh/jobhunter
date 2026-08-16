"""Partition-scoped Instructor helper for dense P1.6 v20 extraction.

V20 keeps the full evidence catalog available for grounding but gives each model call a bounded,
explicit subset of requirement/responsibility coverage. This prevents a correction for one dense
subset from replacing another already-correct subset.

The first live v20 dense run exposed one further item-normalization edge case: the model copied the
word ``some`` from ``some C / C++ helpful`` into ``depth_signal``. JobHunter does not treat that
vague quantifier as an accepted technical-depth signal. V20 therefore clears it only when the exact
same evidence independently proves a preferred/optional requirement and contains no accepted depth
or experience-extent marker. Exact source evidence is never changed.

The next live partition exposed the adjacent scope/depth boundary: ``industrial / edge deployment``
was placed in ``depth_signal`` even though it names the deployment scope itself. V20 preserves that
exact source-supported scope in the normalized concept, clears the non-depth signal, and separately
rejects ``concept_type=experience`` when preferred evidence does not actually state prior applied
exposure.
"""

from __future__ import annotations

import json
import re
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI
from pydantic import Field, ValidationInfo, model_validator

from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    evidence_reference_payload,
    has_english_optionality_signal,
    requirement_coverage_payload,
    responsibility_coverage_payload,
)
from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError
from jobhunter.inference.instructor_lm_studio import (
    _DEPTH_SIGNAL_PATTERNS,
    _equivalent_source_excerpt,
    _leaf_evidence_catalog,
    _normalize,
)
from jobhunter.inference.instructor_lm_studio_v19 import (
    AnalysisRequirementV19,
    JobAnalysisResponseV19,
    _raw_evidence_text,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_VAGUE_PREFERENCE_EXTENT_RE = re.compile(r"^some$", re.I)
_PRIOR_APPLIED_EXPOSURE_RE = re.compile(
    r"\b(?:experience|experienced|hands?[ -]on|years?|worked|working background|"
    r"prior background|background|practical exposure|applied exposure)\b",
    re.I,
)

# Live heterogeneous review exposed this explicit employer degree phrase. Extend the shared
# validator registry narrowly for v20; plain ``knowledge`` intentionally remains non-depth.
_DEPTH_SIGNAL_PATTERNS.setdefault(
    "sufficient_knowledge",
    re.compile(r"\bsufficient\s+knowledge\b", re.I),
)


def _has_accepted_depth(text: str) -> bool:
    return any(pattern.search(text) for pattern in _DEPTH_SIGNAL_PATTERNS.values())


def _signal_is_scoped_concept(concept: str, signal: str) -> bool:
    """Return whether a non-depth signal is the same concept with source-supported scope added."""

    normalized_concept = _normalize(concept)
    normalized_signal = _normalize(signal)
    if not normalized_concept or not normalized_signal:
        return False
    return normalized_signal == normalized_concept or normalized_signal.endswith(
        f" {normalized_concept}"
    )


class AnalysisRequirementV20(AnalysisRequirementV19):
    """Keep v19 strictness while canonicalizing proven preferred scope/depth boundary mistakes."""

    @model_validator(mode="before")
    @classmethod
    def normalize_preferred_non_depth_signal(
        cls,
        value: Any,
        info: ValidationInfo,
    ) -> Any:
        if not isinstance(value, dict):
            return value

        signal = value.get("depth_signal")
        if (
            value.get("requirement_type") != "preferred"
            or not isinstance(signal, str)
            or not signal.strip()
        ):
            return value

        evidence = _raw_evidence_text(value, info)
        normalized = dict(value)

        if (
            _VAGUE_PREFERENCE_EXTENT_RE.fullmatch(signal.strip()) is not None
            and has_english_optionality_signal(evidence)
            and re.search(r"\bsome\b", evidence, re.I) is not None
            and not _has_accepted_depth(evidence)
        ):
            normalized["depth_signal"] = None
            return normalized

        concept = value.get("concept")
        if (
            isinstance(concept, str)
            and concept.strip()
            and has_english_optionality_signal(evidence)
            and not _has_accepted_depth(evidence)
            and not _has_accepted_depth(signal)
            and _equivalent_source_excerpt(signal.strip(), evidence) is not None
            and _signal_is_scoped_concept(concept.strip(), signal.strip())
        ):
            normalized["concept"] = signal.strip()
            normalized["depth_signal"] = None
        return normalized

    @model_validator(mode="after")
    def reject_unproven_preferred_experience(self) -> AnalysisRequirementV20:
        """Do not turn a preferred subject phrase into prior experience without source support."""

        if (
            self.requirement_type == "preferred"
            and self.concept_type == "experience"
            and has_english_optionality_signal(self.evidence)
            and _PRIOR_APPLIED_EXPOSURE_RE.search(self.evidence) is None
        ):
            raise ValueError(
                "concept_type=experience requires explicit prior applied exposure in the cited "
                "evidence; a preferred subject/scope phrase alone does not prove experience"
            )
        return self


class JobAnalysisResponseV20(JobAnalysisResponseV19):
    """V19 response-level coverage semantics with v20 requirement-item normalization."""

    requirements: list[AnalysisRequirementV20] = Field()


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
            response_model=JobAnalysisResponseV20,
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
            "p16_v20_vague_preference_extent_normalization": True,
            "p16_v20_preferred_scope_depth_normalization": True,
            "p16_v20_preferred_experience_evidence_guard": True,
        },
        "instructor": {
            "mode": "JSON_SCHEMA",
            "response_model": "JobAnalysisResponseV20",
            "validation_retries": validation_retries,
            "schema": JobAnalysisResponseV20.model_json_schema(),
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
    "AnalysisRequirementV20",
    "JobAnalysisResponseV20",
    "_signal_is_scoped_concept",
    "_validated_partition_plan",
    "complete_analysis_partition_with_instructor_v20",
]
