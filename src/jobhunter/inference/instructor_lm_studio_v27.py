"""V27 source-exact depth modifiers and explicit prior-work ontology."""

from __future__ import annotations

import re
from typing import Any, Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference.instructor_lm_studio_v25 import (
    AnalysisRequirementV25,
    JobAnalysisResponseV25,
)

_QUALIFIED_DEPTH_RE = re.compile(
    r"\b(?:relative|initial|basic|general|advanced)\s+"
    r"(?:mastery|familiarity|proficiency)\b",
    re.I,
)
_EXPLICIT_WORK_RE = re.compile(r"\bexperience\s+working\s+with\b", re.I)


class AnalysisRequirementV27(AnalysisRequirementV25):
    @model_validator(mode="before")
    @classmethod
    def retain_explicit_prior_work_type(cls, value: Any) -> Any:
        if (
            isinstance(value, dict)
            and value.get("concept_type") == "tool"
            and _EXPLICIT_WORK_RE.search(str(value.get("item_excerpt") or ""))
            and _EXPLICIT_WORK_RE.search(str(value.get("concept") or ""))
        ):
            return {**value, "concept_type": "experience"}
        return value

    @model_validator(mode="after")
    def retain_exact_depth_modifier(self, info: ValidationInfo) -> Self:
        if (info.context or {}).get("analysis_mode") != "english":
            return self
        match = _QUALIFIED_DEPTH_RE.search(self.item_excerpt)
        if (
            match is not None
            and self.depth_signal is not None
            and self.depth_signal.casefold() in match.group().casefold()
        ):
            self.depth_signal = match.group()
        return self


class JobAnalysisResponseV27(JobAnalysisResponseV25):
    requirements: list[AnalysisRequirementV27] = Field()


__all__ = ["AnalysisRequirementV27", "JobAnalysisResponseV27"]
