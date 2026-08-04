"""Instructor + Pydantic validation for JobHunter semantic-analysis calls.

The existing LMStudioProvider remains the transport and generic structured-output
boundary. Analysis calls opt into this helper lazily, so doctor/smoke and other
structured inference paths keep their established behavior.
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError

RequirementType = Literal["required", "preferred", "contextual", "inferred"]
ConceptType = Literal[
    "tool",
    "skill",
    "knowledge",
    "practice",
    "domain",
    "experience",
    "education",
    "other",
]
Confidence = Literal["high", "medium", "low"]
_TOKEN_RE = re.compile(r"[^\s\u200c]+")


def _iter_strings(value: Any):
    if isinstance(value, str):
        if value.strip():
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from _iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _equivalent_source_excerpt(evidence: str, source_text: str) -> str | None:
    """Return the exact source span when tokens differ only by spacing/ZWNJ/case."""

    exact_start = source_text.find(evidence)
    if exact_start >= 0:
        return source_text[exact_start : exact_start + len(evidence)]

    evidence_tokens = [match.group(0).casefold() for match in _TOKEN_RE.finditer(evidence)]
    if not evidence_tokens:
        return None
    source_matches = list(_TOKEN_RE.finditer(source_text))
    source_tokens = [match.group(0).casefold() for match in source_matches]
    width = len(evidence_tokens)
    for start in range(0, len(source_tokens) - width + 1):
        if source_tokens[start : start + width] != evidence_tokens:
            continue
        first = source_matches[start]
        last = source_matches[start + width - 1]
        return source_text[first.start() : last.end()]
    return None


def _field_value_for_prefixed_evidence(
    evidence: str,
    fields: dict[str, Any],
) -> str | None:
    """Strip an invented ``field_name:`` prefix only when mechanically provable."""

    if ":" not in evidence:
        return None
    raw_key, raw_value = evidence.split(":", 1)
    key = raw_key.strip()
    if key not in fields:
        return None
    candidate = raw_value.strip()
    actual = fields[key]
    if isinstance(actual, str) and _normalize(candidate) == _normalize(actual):
        return actual.strip()
    if isinstance(actual, list):
        for item in actual:
            if isinstance(item, str) and _normalize(candidate) == _normalize(item):
                return item.strip()
    return None


def _canonical_evidence(evidence: str, info: ValidationInfo) -> str:
    value = evidence.strip()
    fields = (info.context or {}).get("analysis_fields")
    if not isinstance(fields, dict):
        raise ValueError("analysis validation context is missing analysis_fields")

    for source_text in _iter_strings(fields):
        canonical = _equivalent_source_excerpt(value, source_text)
        if canonical is not None:
            return canonical

    canonical = _field_value_for_prefixed_evidence(value, fields)
    if canonical is not None:
        return canonical

    raise ValueError(
        "Evidence must be copied verbatim from an analysis_fields VALUE. "
        "Do not prepend field names such as 'education:' or 'minimum_experience:', "
        "and do not paraphrase, translate, concatenate, or reconstruct evidence."
    )


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AnalysisClaim(_StrictModel):
    statement: str = Field(min_length=1)
    evidence: str = Field(min_length=2)
    confidence: Confidence

    @field_validator("evidence")
    @classmethod
    def evidence_must_be_grounded(cls, value: str, info: ValidationInfo) -> str:
        return _canonical_evidence(value, info)


class AnalysisRequirement(_StrictModel):
    concept: str = Field(min_length=1)
    requirement_type: RequirementType
    concept_type: ConceptType
    evidence: str = Field(min_length=2)
    confidence: Confidence
    rationale: str

    @field_validator("evidence")
    @classmethod
    def evidence_must_be_grounded(cls, value: str, info: ValidationInfo) -> str:
        return _canonical_evidence(value, info)

    @model_validator(mode="after")
    def inferred_requires_rationale(self) -> AnalysisRequirement:
        if self.requirement_type == "inferred" and not self.rationale.strip():
            raise ValueError("Inferred requirements require a concise non-empty rationale")
        return self


class JobAnalysisResponse(_StrictModel):
    role_purpose: list[AnalysisClaim] = Field(max_length=1)
    responsibilities: list[AnalysisClaim] = Field(max_length=16)
    requirements: list[AnalysisRequirement] = Field(max_length=32)

    @model_validator(mode="after")
    def remove_exact_duplicate_claims(self) -> JobAnalysisResponse:
        """Collapse exact duplicates deterministically instead of spending another LM call."""

        seen_responsibilities: set[tuple[str, str]] = set()
        responsibilities: list[AnalysisClaim] = []
        for item in self.responsibilities:
            key = (_normalize(item.statement), _normalize(item.evidence))
            if key in seen_responsibilities:
                continue
            seen_responsibilities.add(key)
            responsibilities.append(item)
        self.responsibilities = responsibilities

        seen_requirements: set[tuple[str, str, str]] = set()
        requirements: list[AnalysisRequirement] = []
        for item in self.requirements:
            key = (
                _normalize(item.concept),
                item.requirement_type,
                _normalize(item.evidence),
            )
            if key in seen_requirements:
                continue
            seen_requirements.add(key)
            requirements.append(item)
        self.requirements = requirements
        return self


def complete_analysis_with_instructor(
    *,
    base_url: str,
    api_token: str | None,
    timeout_seconds: float,
    network_retries: int,
    transport: httpx.BaseTransport | None,
    selected_model: str,
    system_prompt: str,
    user_payload: dict[str, Any],
    schema: dict[str, Any],
    max_tokens: int,
    seed: int,
    validation_retries: int = 1,
):
    """Return one analysis result validated by Instructor and JobHunter Pydantic rules."""

    if not 0 <= validation_retries <= 3:
        raise ValueError("validation_retries must be between 0 and 3")
    analysis_fields = user_payload.get("analysis_fields")
    if not isinstance(analysis_fields, dict):
        raise InferenceResponseError(
            "Instructor analysis requires dictionary analysis_fields"
        )

    http_client = httpx.Client(
        timeout=timeout_seconds,
        transport=transport,
        trust_env=False,
    )
    openai_client = OpenAI(
        base_url=base_url,
        api_key=api_token or "lm-studio-local",
        timeout=timeout_seconds,
        max_retries=network_retries,
        http_client=http_client,
    )
    client = instructor.from_openai(openai_client, mode=instructor.Mode.JSON_SCHEMA)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps(user_payload, ensure_ascii=False, sort_keys=True),
        },
    ]

    try:
        result, completion = client.create_with_completion(
            model=selected_model,
            response_model=JobAnalysisResponse,
            messages=messages,
            context={"analysis_fields": analysis_fields},
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
        "instructor": {
            "mode": "JSON_SCHEMA",
            "response_model": "JobAnalysisResponse",
            "validation_retries": validation_retries,
            "schema": JobAnalysisResponse.model_json_schema(),
        },
    }

    # Import lazily to avoid a module cycle while LMStudioProvider itself lazily imports us.
    from jobhunter.inference.lm_studio import StructuredInferenceResult

    return StructuredInferenceResult(
        model=selected_model,
        structured=structured,
        request_body=request_body,
        raw_response=raw_response,
        finish_reason=str(finish_reason) if finish_reason is not None else None,
    )
