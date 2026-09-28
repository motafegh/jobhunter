"""V29 abstains from single-category labels for explicitly mixed source facts."""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, model_validator

from jobhunter.inference.instructor_lm_studio_v27 import (
    AnalysisRequirementV27,
    JobAnalysisResponseV27,
)

_EXPERIENCE_RE = re.compile(r"\b(?:experience|work\s+history)\b", re.I)
_KNOWLEDGE_RE = re.compile(r"\bknowledge\b", re.I)
_EDUCATION_RE = re.compile(r"\b(?:education|degree)\b", re.I)
_KNOWLEDGE_OF_RE = re.compile(r"\bknowledge\s+of\b", re.I)


class AnalysisRequirementV29(AnalysisRequirementV27):
    @model_validator(mode="before")
    @classmethod
    def retain_mixed_source_ontology(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        concept = str(value.get("concept") or "")
        item = str(value.get("item_excerpt") or "")
        category = value.get("concept_type")
        source_has_experience = bool(
            _EXPERIENCE_RE.search(concept) and _EXPERIENCE_RE.search(item)
        )
        if source_has_experience and (
            (_KNOWLEDGE_RE.search(concept) and _KNOWLEDGE_RE.search(item))
            or (_EDUCATION_RE.search(concept) and _EDUCATION_RE.search(item))
        ) and category in {"knowledge", "education", "experience"}:
            return {**value, "concept_type": "other"}
        if (
            category == "tool"
            and _KNOWLEDGE_OF_RE.search(concept)
            and _KNOWLEDGE_OF_RE.search(item)
        ):
            return {**value, "concept_type": "knowledge"}
        return value


class JobAnalysisResponseV29(JobAnalysisResponseV27):
    requirements: list[AnalysisRequirementV29] = Field()


__all__ = ["AnalysisRequirementV29", "JobAnalysisResponseV29"]
