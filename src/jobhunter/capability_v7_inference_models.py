"""Inference-time source-link repair for Capability v7.

Capability source indices are provenance bookkeeping over accepted P1.6 facts. The reasoning model
may propose them, but JobHunter can safely repair mechanically invalid positive indices and recover
missing links when the profile's already-grounded evidence exactly matches accepted P1.6 evidence.
Strict whole-artifact coverage validation still runs afterward.
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationInfo, model_validator

from jobhunter.capability_models import CapabilityProfile
from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft as _StrictCapabilityReasoningDraft,
)
from jobhunter.capability_v7_models import partition_source_requirements


def _accepted_extraction(info: ValidationInfo) -> dict[str, Any] | None:
    extraction = (info.context or {}).get("accepted_extraction")
    if extraction is None:
        return None
    if not isinstance(extraction, dict):
        raise ValueError("capability validation context contains invalid accepted_extraction")
    return extraction


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _evidence_values(item: Any) -> list[str]:
    if not isinstance(item, dict):
        return []
    raw = item.get("evidence")
    values = raw if isinstance(raw, list) else [raw]
    return [
        value.strip()
        for value in values
        if isinstance(value, str) and value.strip()
    ]


def _drop_positive_out_of_range(values: Any, *, size: int) -> Any:
    """Remove only mechanically impossible positive integer indices.

    Negative values, wrong types, and other malformed input remain untouched so the strict base
    validators still reject them instead of silently normalizing semantic/type errors.
    """

    if not isinstance(values, list):
        return values
    return [
        value
        for value in values
        if not (type(value) is int and value >= 0 and value >= size)
    ]


def _profile_grounded_evidence(profile: CapabilityProfile) -> set[str]:
    evidence: set[str] = set()
    for field_name in (
        "depth_signals",
        "work_activities",
        "sub_capabilities",
        "underlying_knowledge",
        "operational_practices",
        "operational_context",
        "unknown_scope",
    ):
        for item in getattr(profile, field_name):
            evidence.update(_normalize(value) for value in item.evidence)
    if profile.independence_expectation is not None:
        evidence.update(
            _normalize(value) for value in profile.independence_expectation.evidence
        )
    return evidence


def _indices_supported_by_exact_evidence(
    *,
    items: list[Any],
    allowed_indices: set[int],
    profile_evidence: set[str],
) -> list[int]:
    supported: list[int] = []
    for index, item in enumerate(items):
        if index not in allowed_indices:
            continue
        source_evidence = {_normalize(value) for value in _evidence_values(item)}
        if source_evidence & profile_evidence:
            supported.append(index)
    return supported


class CapabilityProfileInferenceV7(CapabilityProfile):
    """V7 profile with deterministic repair for source-index bookkeeping only."""

    @model_validator(mode="before")
    @classmethod
    def remove_impossible_positive_indices(
        cls,
        data: Any,
        info: ValidationInfo,
    ) -> Any:
        extraction = _accepted_extraction(info)
        if extraction is None or not isinstance(data, dict):
            return data

        requirements = extraction.get("requirements") or []
        responsibilities = extraction.get("responsibilities") or []
        if not isinstance(requirements, list):
            raise ValueError("accepted_extraction.requirements must be a list")
        if not isinstance(responsibilities, list):
            raise ValueError("accepted_extraction.responsibilities must be a list")

        repaired = dict(data)
        repaired["source_requirement_indices"] = _drop_positive_out_of_range(
            repaired.get("source_requirement_indices"),
            size=len(requirements),
        )
        repaired["source_responsibility_indices"] = _drop_positive_out_of_range(
            repaired.get("source_responsibility_indices"),
            size=len(responsibilities),
        )
        return repaired

    @model_validator(mode="after")
    def recover_exact_evidence_links(
        self,
        info: ValidationInfo,
    ) -> CapabilityProfileInferenceV7:
        extraction = _accepted_extraction(info)
        if extraction is None:
            return self

        requirements = extraction.get("requirements") or []
        responsibilities = extraction.get("responsibilities") or []
        if not isinstance(requirements, list):
            raise ValueError("accepted_extraction.requirements must be a list")
        if not isinstance(responsibilities, list):
            raise ValueError("accepted_extraction.responsibilities must be a list")

        profile_evidence = _profile_grounded_evidence(self)
        capability_requirement_indices, _ = partition_source_requirements(extraction)
        recovered_requirements = _indices_supported_by_exact_evidence(
            items=requirements,
            allowed_indices=set(capability_requirement_indices),
            profile_evidence=profile_evidence,
        )
        recovered_responsibilities = _indices_supported_by_exact_evidence(
            items=responsibilities,
            allowed_indices=set(range(len(responsibilities))),
            profile_evidence=profile_evidence,
        )

        self.source_requirement_indices = list(
            dict.fromkeys([*self.source_requirement_indices, *recovered_requirements])
        )
        self.source_responsibility_indices = list(
            dict.fromkeys([*self.source_responsibility_indices, *recovered_responsibilities])
        )
        if len(self.source_requirement_indices) > 32:
            raise ValueError("source_requirement_indices may contain at most 32 items")
        if len(self.source_responsibility_indices) > 16:
            raise ValueError("source_responsibility_indices may contain at most 16 items")
        return self


class CapabilityReasoningDraft(_StrictCapabilityReasoningDraft):
    """Instructor response model with v7-only deterministic provenance repair."""

    capabilities: list[CapabilityProfileInferenceV7]


__all__ = ["CapabilityProfileInferenceV7", "CapabilityReasoningDraft"]
