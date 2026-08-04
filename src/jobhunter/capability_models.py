"""Typed contracts and deterministic validation for per-job capability intelligence."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

EvidenceStatus = Literal[
    "source_explicit",
    "strongly_implied_by_work",
    "model_inferred_prerequisite",
    "unknown_or_unsupported",
]
Confidence = Literal["high", "medium", "low"]
RequirementStrength = Literal[
    "required",
    "preferred",
    "contextual",
    "inferred",
    "mixed",
    "unspecified",
]


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


def _normalized_span(source: str, generated: str) -> str | None:
    """Return the exact source span when only whitespace/ZWNJ/case differs."""

    target = _normalize(generated)
    if not target:
        return None
    tokens = [match.span() for match in re.finditer(r"\S+", source)]
    for start_index in range(len(tokens)):
        for end_index in range(start_index, len(tokens)):
            start = tokens[start_index][0]
            end = tokens[end_index][1]
            candidate = source[start:end]
            normalized = _normalize(candidate)
            if normalized == target:
                return candidate
            if len(normalized) > len(target) + 32:
                break
    return None


def _field_value_for_prefixed_evidence(
    evidence: str,
    fields: dict[str, Any],
) -> str | None:
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


def canonicalize_evidence(value: str, fields: dict[str, Any]) -> str:
    """Map mechanically equivalent evidence back to exact English projection text."""

    evidence = value.strip()
    if len(evidence) < 2:
        raise ValueError("evidence must contain at least two characters")

    for source_text in _iter_strings(fields):
        if evidence in source_text:
            return evidence

    prefixed = _field_value_for_prefixed_evidence(evidence, fields)
    if prefixed is not None:
        return prefixed

    for source_text in _iter_strings(fields):
        span = _normalized_span(source_text, evidence)
        if span is not None:
            return span

    raise ValueError(
        "Evidence must be an exact excerpt from an analysis_fields value. "
        "Analytical statements may be synthesized, but supporting evidence may not be "
        "paraphrased, translated, concatenated, or invented."
    )


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CapabilityExpectation(_StrictModel):
    """One evidence-qualified analytical conclusion about a job capability."""

    statement: str = Field(min_length=3, max_length=600)
    evidence_status: EvidenceStatus
    evidence: list[str] = Field(max_length=6)
    rationale: str = Field(min_length=3, max_length=1200)
    confidence: Confidence

    @field_validator("evidence")
    @classmethod
    def evidence_must_be_grounded(
        cls,
        values: list[str],
        info: ValidationInfo,
    ) -> list[str]:
        context = info.context or {}
        fields = context.get("analysis_fields")
        if not isinstance(fields, dict):
            raise ValueError("capability validation context is missing analysis_fields")
        return [canonicalize_evidence(value, fields) for value in values]

    @model_validator(mode="after")
    def status_contract(self) -> CapabilityExpectation:
        if self.evidence_status == "unknown_or_unsupported":
            return self
        if not self.evidence:
            raise ValueError(
                f"{self.evidence_status} expectations require at least one evidence excerpt"
            )
        return self


class CapabilityProfile(_StrictModel):
    """Multidimensional job-local capability profile; not yet a canonical taxonomy entry."""

    capability_label: str = Field(min_length=2, max_length=160)
    summary: str = Field(min_length=12, max_length=1600)
    requirement_strength: RequirementStrength
    employer_stated_depth: list[CapabilityExpectation] = Field(max_length=6)
    work_activities: list[CapabilityExpectation] = Field(max_length=12)
    sub_capabilities: list[CapabilityExpectation] = Field(max_length=16)
    underlying_knowledge: list[CapabilityExpectation] = Field(max_length=12)
    operational_practices: list[CapabilityExpectation] = Field(max_length=12)
    independence_expectation: CapabilityExpectation | None
    operational_context: list[CapabilityExpectation] = Field(max_length=10)
    unknown_scope: list[CapabilityExpectation] = Field(max_length=12)
    overall_confidence: Confidence

    @model_validator(mode="after")
    def normalize_sections(self) -> CapabilityProfile:
        for field_name in (
            "employer_stated_depth",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
            "unknown_scope",
        ):
            items: list[CapabilityExpectation] = getattr(self, field_name)
            seen: set[tuple[str, str]] = set()
            unique: list[CapabilityExpectation] = []
            for item in items:
                key = (_normalize(item.statement), item.evidence_status)
                if key in seen:
                    continue
                seen.add(key)
                unique.append(item)
            setattr(self, field_name, unique)

        if any(
            item.evidence_status != "unknown_or_unsupported"
            for item in self.unknown_scope
        ):
            raise ValueError(
                "unknown_scope items must use evidence_status='unknown_or_unsupported'"
            )

        analytical_dimensions = (
            bool(self.sub_capabilities),
            bool(self.underlying_knowledge),
            bool(self.operational_practices),
            self.independence_expectation is not None,
            bool(self.operational_context),
            bool(self.unknown_scope),
        )
        if not any(analytical_dimensions):
            raise ValueError(
                "Capability profile must add at least one analytical dimension beyond "
                "restated employer facts (sub-capability, underlying knowledge, operational "
                "practice/context, independence, or explicit unknown scope)."
            )
        return self


class CrossCapabilityObservation(_StrictModel):
    statement: str = Field(min_length=8, max_length=1000)
    evidence_status: EvidenceStatus
    evidence: list[str] = Field(max_length=8)
    rationale: str = Field(min_length=3, max_length=1200)
    confidence: Confidence

    @field_validator("evidence")
    @classmethod
    def evidence_must_be_grounded(
        cls,
        values: list[str],
        info: ValidationInfo,
    ) -> list[str]:
        context = info.context or {}
        fields = context.get("analysis_fields")
        if not isinstance(fields, dict):
            raise ValueError("capability validation context is missing analysis_fields")
        return [canonicalize_evidence(value, fields) for value in values]

    @model_validator(mode="after")
    def status_contract(self) -> CrossCapabilityObservation:
        if self.evidence_status != "unknown_or_unsupported" and not self.evidence:
            raise ValueError("supported observations require at least one evidence excerpt")
        return self


class JobCapabilityIntelligence(_StrictModel):
    """Whole-job reasoning artifact built above strict P1.6 extraction."""

    role_interpretation: str = Field(min_length=20, max_length=2400)
    capabilities: list[CapabilityProfile] = Field(min_length=1, max_length=12)
    cross_capability_observations: list[CrossCapabilityObservation] = Field(max_length=8)
    uncertainties: list[str] = Field(max_length=16)

    @model_validator(mode="after")
    def capability_labels_must_be_unique(self) -> JobCapabilityIntelligence:
        seen: set[str] = set()
        for profile in self.capabilities:
            key = _normalize(profile.capability_label)
            if key in seen:
                raise ValueError(
                    f"duplicate capability_label after normalization: {profile.capability_label!r}"
                )
            seen.add(key)
        return self
