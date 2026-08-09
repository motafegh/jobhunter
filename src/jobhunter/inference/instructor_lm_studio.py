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

from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
    evidence_mixes_english_optionality,
    evidence_reference_payload,
    has_english_optionality_signal,
    requirement_coverage_payload,
    responsibility_coverage_payload,
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
_DEPTH_SIGNAL_PATTERNS = {
    "expert": re.compile(r"\bexpert(?:ise)?\b", re.I),
    "proficient": re.compile(r"\bproficien(?:t|cy)\b", re.I),
    "mastery": re.compile(r"\bmastery\b", re.I),
    "familiarity": re.compile(r"\bfamili(?:ar|arity)\b", re.I),
    "strong": re.compile(r"\bstrong\b", re.I),
    "solid": re.compile(r"\bsolid\b", re.I),
    "hands_on": re.compile(r"\bhands?[ -]on\b", re.I),
    "comfort": re.compile(r"\bcomfort(?:able)?\b", re.I),
    "years": re.compile(
        r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
        r"(?:\s*(?:-|–|to)\s*(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten))?"
        r"\s+years?\b",
        re.I,
    ),
}


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
    context = info.context or {}
    fields = context.get("analysis_fields")
    if not isinstance(fields, dict):
        raise ValueError("analysis validation context is missing analysis_fields")
    catalog = context.get("evidence_catalog") or {}
    if not isinstance(catalog, dict):
        raise ValueError("analysis validation context contains invalid evidence_catalog")

    referenced = catalog.get(value)
    if isinstance(referenced, str) and referenced.strip():
        return referenced

    for source_text in _iter_strings(fields):
        canonical = _equivalent_source_excerpt(value, source_text)
        if canonical is not None:
            return canonical

    canonical = _field_value_for_prefixed_evidence(value, fields)
    if canonical is not None:
        return canonical

    raise ValueError(
        "Evidence must be one known JobHunter evidence reference or a verbatim excerpt from an "
        "analysis_fields value. Do not invent reference IDs, prepend field names, paraphrase, "
        "translate, concatenate, or reconstruct evidence."
    )


def _source_is_information_rich(fields: dict[str, Any]) -> bool:
    """Conservatively detect sources where completely empty extraction is implausible."""

    skills = fields.get("skills")
    if isinstance(skills, list) and any(
        isinstance(item, str) and item.strip() for item in skills
    ):
        return True
    description = fields.get("description")
    if isinstance(description, str) and len(description.strip()) >= 160:
        return True
    minimum_experience = fields.get("minimum_experience")
    if isinstance(minimum_experience, str):
        normalized = _normalize(minimum_experience)
        if normalized and normalized not in {
            "it doesn't matter",
            "doesn't matter",
            "not important",
            "unspecified",
        }:
            return True
    return False


def _leaf_evidence_catalog(catalog: dict[str, str]) -> dict[str, str]:
    """Avoid repeating parent text when more precise child references contain it."""

    references = tuple(catalog)
    return {
        reference: text
        for reference, text in catalog.items()
        if not any(
            other != reference and other.startswith(f"{reference}:")
            for other in references
        )
    }


def _validate_depth_fields(
    concept: str, depth_signal: str | None, evidence: str
) -> str | None:
    """Keep normalized subject, explicit depth, and employer obligation independent."""

    for label, pattern in _DEPTH_SIGNAL_PATTERNS.items():
        if pattern.search(concept):
            raise ValueError(
                f"Requirement concept contains {label} depth wording; keep concept depth-neutral "
                "and copy the exact source depth phrase into depth_signal."
            )

    normalized_concept = _normalize(concept)
    if normalized_concept in {"experience", "skill", "knowledge", "practice"}:
        raise ValueError(
            "Requirement concept is too generic for review and aggregation; use a standalone "
            "depth-neutral noun phrase such as professional experience or experience with the "
            "source-supported subject."
        )
    if re.match(r"^(?:with|in|of|for|to)\b", normalized_concept):
        raise ValueError(
            "Requirement concept must be a standalone noun phrase, not a prepositional fragment"
        )

    matched_source_signal: str | None = None
    for pattern in _DEPTH_SIGNAL_PATTERNS.values():
        match = pattern.search(evidence)
        if match is not None:
            matched_source_signal = evidence[match.start() : match.end()]
            break

    if depth_signal is None:
        return matched_source_signal
    normalized_signal = depth_signal.strip()
    if not normalized_signal:
        raise ValueError("depth_signal must be null or a non-empty exact source phrase")
    if _equivalent_source_excerpt(normalized_signal, evidence) is None:
        raise ValueError(
            "depth_signal must be an exact contiguous excerpt of the cited evidence; include "
            "the subject in that excerpt when needed to preserve scope."
        )
    if not any(
        pattern.search(normalized_signal) for pattern in _DEPTH_SIGNAL_PATTERNS.values()
    ):
        raise ValueError(
            "depth_signal must contain an explicit employer depth or experience-extent signal"
        )
    if matched_source_signal is None:
        raise ValueError(
            "depth_signal must contain an explicit employer depth or experience-extent signal"
        )
    return matched_source_signal


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
    depth_signal: str | None
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
    def validate_requirement_semantics(self, info: ValidationInfo) -> AnalysisRequirement:
        if self.requirement_type == "inferred" and not self.rationale.strip():
            raise ValueError("Inferred requirements require a concise non-empty rationale")

        if (info.context or {}).get("analysis_mode") == "english":
            if evidence_mixes_english_optionality(self.evidence):
                raise ValueError(
                    "A requirement cannot use mixed-strength evidence; split core and optional "
                    "clauses into atomic requirements using specific evidence references."
                )
            if self.requirement_type == "preferred" and not has_english_optionality_signal(
                self.evidence
            ):
                raise ValueError(
                    "English preferred requirements require explicit preference/plus/helpful/"
                    "advantage wording in their cited evidence; otherwise use contextual or "
                    "preserve the source's actual strength."
                )
            self.depth_signal = _validate_depth_fields(
                self.concept, self.depth_signal, self.evidence
            )
        return self


class AnalysisCoverageExclusion(_StrictModel):
    evidence_reference: str = Field(min_length=2)
    rationale: str = Field(min_length=8)

    @field_validator("evidence_reference")
    @classmethod
    def reference_must_be_in_coverage_plan(cls, value: str, info: ValidationInfo) -> str:
        reference = value.strip()
        plan = (info.context or {}).get("requirement_coverage_plan") or {}
        if plan and reference not in plan:
            raise ValueError(
                "Coverage evidence_reference must be one supplied requirement coverage ID"
            )
        return reference


class JobAnalysisResponse(_StrictModel):
    role_purpose: list[AnalysisClaim] = Field(max_length=1)
    responsibilities: list[AnalysisClaim] = Field(max_length=16)
    requirements: list[AnalysisRequirement] = Field(max_length=32)
    coverage_exclusions: list[AnalysisCoverageExclusion] = Field(
        default_factory=list, max_length=64
    )

    @model_validator(mode="after")
    def normalize_and_validate_quality(self, info: ValidationInfo) -> JobAnalysisResponse:
        """Collapse exact duplicates and reject implausibly empty rich-source extraction."""

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

        context = info.context or {}
        fields = context.get("analysis_fields")
        if (
            isinstance(fields, dict)
            and _source_is_information_rich(fields)
            and not self.responsibilities
            and not self.requirements
        ):
            raise ValueError(
                "Information-rich job fields cannot be accepted with both responsibilities "
                "and requirements empty; extract supported career claims or explicitly narrow "
                "the source interpretation on retry."
            )
        coverage_plan = context.get("requirement_coverage_plan") or {}
        if coverage_plan:
            exclusions = {item.evidence_reference: item for item in self.coverage_exclusions}
            if len(exclusions) != len(self.coverage_exclusions):
                raise ValueError("Requirement coverage exclusions contain duplicate references")

            requirements_by_evidence: dict[str, list[AnalysisRequirement]] = {}
            for item in self.requirements:
                requirements_by_evidence.setdefault(_normalize(item.evidence), []).append(item)

            for reference, candidate in coverage_plan.items():
                evidence = str(candidate["text"])
                matching = requirements_by_evidence.get(_normalize(evidence), [])
                if candidate.get("obligation_hint") == "context_only":
                    if matching or reference in exclusions:
                        raise ValueError(
                            f"Coverage reference {reference} is a context-only modifier and must "
                            "not be extracted or excluded"
                        )
                    continue
                if matching:
                    if reference in exclusions:
                        raise ValueError(
                            f"Coverage reference {reference} cannot be both extracted and excluded"
                        )
                    obligation_hint = candidate.get("obligation_hint")
                    if obligation_hint in {"required", "preferred", "contextual"} and not any(
                        item.requirement_type == obligation_hint for item in matching
                    ):
                        raise ValueError(
                            f"Coverage reference {reference} must preserve the supplied "
                            f"{obligation_hint} obligation hint"
                        )
                    continue
                if reference not in exclusions:
                    raise ValueError(
                        f"Requirement coverage reference {reference} must be cited by a "
                        "requirement or explicitly justified in coverage_exclusions"
                    )
                if not candidate.get("allow_exclusion", False):
                    raise ValueError(
                        f"Coverage reference {reference} is a structured requirement and cannot "
                        "be excluded"
                    )

        responsibility_plan = context.get("responsibility_coverage_plan") or {}
        if responsibility_plan:
            represented_evidence = {
                _normalize(item.evidence)
                for item in [*self.role_purpose, *self.responsibilities]
            }
            missing_responsibilities = [
                reference
                for reference, evidence in responsibility_plan.items()
                if _normalize(evidence) not in represented_evidence
            ]
            if missing_responsibilities:
                raise ValueError(
                    "Responsibility coverage must represent every supplied duty as role purpose "
                    f"or responsibility; missing={missing_responsibilities}"
                )
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

    evidence_catalog = build_field_evidence_catalog(analysis_fields)
    model_evidence_catalog = _leaf_evidence_catalog(evidence_catalog)
    requirement_coverage_plan = build_requirement_coverage_plan(analysis_fields)
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

    # Detailed factual extraction may legitimately emit many claims. Keep connection setup
    # bounded but do not terminate a healthy local generation merely because it exceeds a shared
    # short read timeout. Transport replay is disabled; Instructor owns the one validation retry.
    connect_timeout = min(float(timeout_seconds), 10.0)
    timeout = httpx.Timeout(
        connect=connect_timeout,
        read=None,
        write=30.0,
        pool=30.0,
    )
    http_client = httpx.Client(
        timeout=timeout,
        transport=transport,
        trust_env=False,
    )
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
        },
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
