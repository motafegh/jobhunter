"""V25 exact-source repair for shared list qualifiers and unsupported experience labels."""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference.instructor_lm_studio_v19 import _raw_evidence_text
from jobhunter.inference.instructor_lm_studio_v22 import (
    _exact_item_is_source_proven_experience,
)
from jobhunter.inference.instructor_lm_studio_v23 import (
    AnalysisRequirementV23,
    JobAnalysisResponseV23,
)

_SHARED_QUALIFIER_RE = re.compile(
    r"^(familiarity with|knowledge of|proficiency in)\s+(.+)$", re.I
)
_EXPERIENCE_CONCEPT_RE = re.compile(r"^experience\s+(?:in\s+)?(.+)$", re.I)


class AnalysisRequirementV25(AnalysisRequirementV23):
    """Keep the claim while replacing only demonstrably inaccurate model labels."""

    @model_validator(mode="before")
    @classmethod
    def repair_exact_source_labels(cls, value: Any, info: ValidationInfo) -> Any:
        if not isinstance(value, dict):
            return value
        evidence = _raw_evidence_text(value, info)
        item = str(value.get("item_excerpt") or "")
        normalized = dict(value)
        if item and item not in evidence:
            match = _SHARED_QUALIFIER_RE.fullmatch(item)
            if match:
                qualifier, subject = match.groups()
                prefix_at = evidence.casefold().rfind(
                    qualifier.casefold() + " ", 0, evidence.find(subject)
                )
                intervening = (
                    evidence[prefix_at + len(qualifier) : evidence.index(subject)]
                    if prefix_at >= 0 and subject in evidence else ""
                )
                if (
                    prefix_at >= 0
                    and evidence.count(subject) == 1
                    and "," in intervening
                    and not any(mark in intervening for mark in ".;\n")
                ):
                    normalized["item_excerpt"] = subject
                    item = subject
        if normalized.get("concept_type") == "experience":
            plan = (info.context or {}).get("requirement_coverage_plan") or {}
            proven = _exact_item_is_source_proven_experience(
                item_excerpt=item,
                evidence=evidence,
                plan=plan if isinstance(plan, dict) else {},
            )
            concept_match = _EXPERIENCE_CONCEPT_RE.fullmatch(
                str(normalized.get("concept") or "")
            )
            if (
                not proven
                and concept_match
                and item
                and item in evidence
                and "experience" not in item.casefold()
                and concept_match.group(1).casefold() == item.casefold()
            ):
                normalized["concept"] = item
                normalized["concept_type"] = "other"
        return normalized


class JobAnalysisResponseV25(JobAnalysisResponseV23):
    requirements: list[AnalysisRequirementV25] = Field()


__all__ = ["AnalysisRequirementV25", "JobAnalysisResponseV25"]
