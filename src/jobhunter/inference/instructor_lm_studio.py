"""Instructor + Pydantic structured inference for JobHunter semantic analysis.

This adapter keeps LM Studio local and OpenAI-compatible while delegating generic
structured-output parsing, validation feedback, and bounded re-asks to Instructor.
JobHunter-specific evidence and duplicate rules stay deterministic in Pydantic.
"""

from __future__ import annotations

import json
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

from jobhunter.inference.base import (
    InferenceConnectionError,
    InferenceResponseError,
)
from jobhunter.inference.lm_studio import LMStudioProvider, StructuredInferenceResult

AnalysisMode = Literal["english", "original"]
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


def _field_value_for_prefixed_evidence(
    evidence: str,
    fields: dict[str, Any],
) -> str | None:
    """Remove a model-invented ``field_name:`` prefix only when mechanically safe.

    Example: ``minimum_experience: three to six years`` may become
    ``three to six years`` only when that is exactly the value of the real
    ``minimum_experience`` field. Arbitrary prefixes or paraphrases still fail.
    """

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

    # Normal case: the model copied a real contiguous excerpt.
    for source_text in _iter_strings(fields):
        if value in source_text:
            return value

    # Safe recovery for a common structured-data mistake: the model prepended
    # the JSON field name to an otherwise exact scalar/list value.
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
    role_purpose: list[AnalysisClaim] = Field(default_factory=list, max_length=1)
    responsibilities: list[AnalysisClaim] = Field(default_factory=list, max_length=16)
    requirements: list[AnalysisRequirement] = Field(default_factory=list, max_length=32)

    @model_validator(mode="after")
    def remove_exact_duplicate_claims(self) -> JobAnalysisResponse:
        """Deterministically collapse exact duplicates instead of spending another LM call."""

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


class InstructorLMStudioProvider(LMStudioProvider):
    """LM Studio provider with Instructor/Pydantic analysis validation and re-asks.

    Non-analysis structured calls still use the established lightweight provider.
    Analysis schemas are routed through Instructor ``JSON_SCHEMA`` mode so provider
    schema enforcement, Pydantic domain validation, and validation-feedback retries
    form one bounded extraction loop.
    """

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str | None = None,
        api_token: str | None = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
        transport: httpx.BaseTransport | None = None,
        analysis_validation_retries: int = 1,
    ) -> None:
        super().__init__(
            base_url=base_url,
            configured_model=configured_model,
            api_token=api_token,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            transport=transport,
        )
        if not 0 <= analysis_validation_retries <= 3:
            raise ValueError("analysis_validation_retries must be between 0 and 3")
        self._analysis_validation_retries = analysis_validation_retries

        headers: dict[str, str] = {}
        if api_token:
            headers["Authorization"] = f"Bearer {api_token}"
        http_client = httpx.Client(
            timeout=timeout_seconds,
            transport=transport,
            trust_env=False,
            headers=headers or None,
        )
        openai_client = OpenAI(
            base_url=base_url,
            api_key=api_token or "lm-studio-local",
            timeout=timeout_seconds,
            max_retries=max_retries,
            http_client=http_client,
        )
        self._instructor_client = instructor.from_openai(
            openai_client,
            mode=instructor.Mode.JSON_SCHEMA,
        )

    @staticmethod
    def _is_analysis_schema(schema_name: str) -> bool:
        return schema_name.startswith("jobhunter_job_analysis_")

    def complete_structured(
        self,
        *,
        system_prompt: str,
        user_payload: dict[str, Any],
        schema_name: str,
        schema: dict[str, Any],
        model: str | None = None,
        max_tokens: int = 8192,
        max_recovery_tokens: int | None = None,
        seed: int = 0,
    ) -> StructuredInferenceResult:
        if not self._is_analysis_schema(schema_name):
            return super().complete_structured(
                system_prompt=system_prompt,
                user_payload=user_payload,
                schema_name=schema_name,
                schema=schema,
                model=model,
                max_tokens=max_tokens,
                max_recovery_tokens=max_recovery_tokens,
                seed=seed,
            )

        selected_model = self._selected_model(model)
        analysis_fields = user_payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise InferenceResponseError(
                "Instructor analysis requires dictionary analysis_fields"
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(user_payload, ensure_ascii=False, sort_keys=True),
            },
        ]
        try:
            result, completion = self._instructor_client.create_with_completion(
                model=selected_model,
                response_model=JobAnalysisResponse,
                messages=messages,
                context={"analysis_fields": analysis_fields},
                max_retries=self._analysis_validation_retries,
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
                f"after {self._analysis_validation_retries} bounded validation retries: {exc}"
            ) from exc

        structured = result.model_dump(mode="json")
        # Keep the existing JSON-Schema validator as an independent final guard. Instructor
        # validates a stricter Pydantic model; this confirms compatibility with JobHunter's
        # persisted v2 analysis schema before the service performs its own final checks.
        self._validate_structured_result(structured, schema)

        raw_response = completion.model_dump(mode="json")
        finish_reason = None
        if completion.choices:
            finish_reason = completion.choices[0].finish_reason
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
                "validation_retries": self._analysis_validation_retries,
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
