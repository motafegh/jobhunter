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
_TOKEN_RE = re.compile(r"[^\s\u200c]+")
_COMPOSITE_SEPARATOR_RE = re.compile(r",\s+|;\s+|\n+|\s+\|\s+")
_DERIVED_STATUSES = {"strongly_implied_by_work", "model_inferred_prerequisite"}


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


def _bounded_text(
    value: str,
    *,
    field_name: str,
    minimum: int,
    maximum: int,
) -> str:
    """Validate prose bounds at runtime without emitting grammar-heavy JSON Schema limits."""

    length = len(value)
    if length < minimum:
        raise ValueError(f"{field_name} must contain at least {minimum} characters")
    if length > maximum:
        raise ValueError(f"{field_name} may contain at most {maximum} characters")
    return value


def _equivalent_source_excerpt(evidence: str, source_text: str) -> str | None:
    """Return exact source span when only whitespace/ZWNJ/case tokenization differs."""

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


def _try_canonicalize_evidence(value: str, fields: dict[str, Any]) -> str | None:
    evidence = value.strip()
    if len(evidence) < 2:
        return None

    for source_text in _iter_strings(fields):
        canonical = _equivalent_source_excerpt(evidence, source_text)
        if canonical is not None:
            return canonical

    return _field_value_for_prefixed_evidence(evidence, fields)


def canonicalize_evidence(value: str, fields: dict[str, Any]) -> str:
    """Map one mechanically equivalent evidence item back to exact English projection text."""

    canonical = _try_canonicalize_evidence(value, fields)
    if canonical is not None:
        return canonical

    raise ValueError(
        "Evidence must be an exact excerpt from an analysis_fields value. "
        "Analytical statements may be synthesized, but supporting evidence may not be "
        "paraphrased, translated, or invented. Non-contiguous support must be represented "
        "as separate exact evidence excerpts."
    )


def _partition_composite_evidence(
    value: str,
    fields: dict[str, Any],
    *,
    max_parts: int,
) -> list[str] | None:
    """Recover a model-concatenated quote only when every fragment is exact source evidence.

    The model occasionally joins two real but non-contiguous source clauses into one evidence
    string. This helper is deliberately mechanical: it may split only at punctuation/newline
    separators, every resulting fragment must independently canonicalize to an exact source span,
    and the smallest successful number of fragments wins. It never repairs paraphrased content.
    """

    candidate = value.strip()
    if max_parts < 2 or len(candidate) < 4:
        return None

    split_matches = list(_COMPOSITE_SEPARATOR_RE.finditer(candidate))
    if not split_matches:
        return None

    def search(text: str, parts: int) -> list[str] | None:
        if parts == 1:
            canonical = _try_canonicalize_evidence(text, fields)
            return [canonical] if canonical is not None else None

        for match in _COMPOSITE_SEPARATOR_RE.finditer(text):
            left = text[: match.start()].strip(" \t\r\n,;|")
            right = text[match.end() :].strip(" \t\r\n,;|")
            if len(left) < 2 or len(right) < 2:
                continue
            canonical_left = _try_canonicalize_evidence(left, fields)
            if canonical_left is None:
                continue
            remainder = search(right, parts - 1)
            if remainder is not None:
                return [canonical_left, *remainder]
        return None

    for part_count in range(2, max_parts + 1):
        result = search(candidate, part_count)
        if result is not None:
            return result
    return None


def canonicalize_evidence_list(
    values: list[str],
    fields: dict[str, Any],
    *,
    max_items: int,
) -> list[str]:
    """Canonicalize evidence and safely expand fully provable composite quotes."""

    canonical_values: list[str] = []
    for value in values:
        canonical = _try_canonicalize_evidence(value, fields)
        if canonical is not None:
            fragments = [canonical]
        else:
            remaining_capacity = max_items - len(canonical_values)
            fragments = _partition_composite_evidence(
                value,
                fields,
                max_parts=min(3, remaining_capacity),
            )
            if fragments is None:
                canonicalize_evidence(value, fields)
                raise AssertionError("canonicalize_evidence must raise for unsupported evidence")

        for fragment in fragments:
            if fragment not in canonical_values:
                canonical_values.append(fragment)
        if len(canonical_values) > max_items:
            raise ValueError(f"evidence may contain at most {max_items} exact excerpts")
    return canonical_values


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CapabilityExpectation(_StrictModel):
    """One evidence-qualified analytical conclusion about a job capability."""

    # Prose length bounds intentionally live in runtime validators rather than Field metadata.
    # LM Studio converts JSON Schema string bounds into llama.cpp grammar repetitions; large
    # maxLength values (for example 1200) can exceed the grammar parser's sane repetition limit
    # before the model receives the request.
    statement: str
    evidence_status: EvidenceStatus
    evidence: list[str] = Field(max_length=6)
    rationale: str
    confidence: Confidence

    @field_validator("statement")
    @classmethod
    def statement_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="statement",
            minimum=3,
            maximum=600,
        )

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="rationale",
            minimum=3,
            maximum=1200,
        )

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
        return canonicalize_evidence_list(values, fields, max_items=6)

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

    capability_label: str
    summary: str
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

    @field_validator("capability_label")
    @classmethod
    def capability_label_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="capability_label",
            minimum=2,
            maximum=160,
        )

    @field_validator("summary")
    @classmethod
    def summary_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="summary",
            minimum=12,
            maximum=1600,
        )

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
            item.evidence_status != "source_explicit"
            for item in self.employer_stated_depth
        ):
            raise ValueError("employer_stated_depth items must be source_explicit")
        if any(
            item.evidence_status == "unknown_or_unsupported"
            for item in self.work_activities
        ):
            raise ValueError("unknown work scope belongs under unknown_scope")
        if any(
            item.evidence_status != "unknown_or_unsupported"
            for item in self.unknown_scope
        ):
            raise ValueError(
                "unknown_scope items must use evidence_status='unknown_or_unsupported'"
            )
        for field_name in (
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            if any(
                item.evidence_status == "unknown_or_unsupported"
                for item in getattr(self, field_name)
            ):
                raise ValueError(f"unknown {field_name} scope belongs under unknown_scope")
        if (
            self.independence_expectation is not None
            and self.independence_expectation.evidence_status == "unknown_or_unsupported"
        ):
            raise ValueError("unknown independence scope belongs under unknown_scope")

        analytical_items = [
            *self.sub_capabilities,
            *self.underlying_knowledge,
            *self.operational_practices,
            *self.operational_context,
        ]
        if self.independence_expectation is not None:
            analytical_items.append(self.independence_expectation)
        has_derived_reasoning = any(
            item.evidence_status in _DERIVED_STATUSES for item in analytical_items
        )
        has_unknown_boundary = bool(self.unknown_scope)
        if not has_derived_reasoning and not has_unknown_boundary:
            raise ValueError(
                "Capability profile must add derived reasoning or an explicit unknown-scope "
                "boundary beyond restated employer facts."
            )
        return self


class CrossCapabilityObservation(_StrictModel):
    statement: str
    evidence_status: EvidenceStatus
    evidence: list[str] = Field(max_length=8)
    rationale: str
    confidence: Confidence

    @field_validator("statement")
    @classmethod
    def statement_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="cross-capability statement",
            minimum=8,
            maximum=1000,
        )

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="cross-capability rationale",
            minimum=3,
            maximum=1200,
        )

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
        return canonicalize_evidence_list(values, fields, max_items=8)

    @model_validator(mode="after")
    def status_contract(self) -> CrossCapabilityObservation:
        if self.evidence_status != "unknown_or_unsupported" and not self.evidence:
            raise ValueError("supported observations require at least one evidence excerpt")
        return self


class JobCapabilityIntelligence(_StrictModel):
    """Whole-job reasoning artifact built above strict P1.6 extraction."""

    role_interpretation: str
    capabilities: list[CapabilityProfile] = Field(min_length=1, max_length=12)
    cross_capability_observations: list[CrossCapabilityObservation] = Field(max_length=8)
    uncertainties: list[str] = Field(max_length=16)

    @field_validator("role_interpretation")
    @classmethod
    def role_interpretation_bounds(cls, value: str) -> str:
        return _bounded_text(
            value,
            field_name="role_interpretation",
            minimum=20,
            maximum=2400,
        )

    @model_validator(mode="after")
    def capability_labels_must_be_unique(self) -> JobCapabilityIntelligence:
        seen: set[str] = set()
        for profile in self.capabilities:
            key = _normalize(profile.capability_label)
            if key in seen:
                raise ValueError(
                    "duplicate capability_label after normalization: "
                    f"{profile.capability_label!r}"
                )
            seen.add(key)
        return self
