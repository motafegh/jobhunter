"""V30 preserves explicit prior applied exposure when the model mislabels it."""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, model_validator

from jobhunter.inference.instructor_lm_studio_v29 import (
    AnalysisRequirementV29,
    JobAnalysisResponseV29,
)

_PRIOR_EXPERIENCE_RE = re.compile(
    r"^(?:(?:practical|professional|hands-on)\s+)?experience\s+"
    r"(?:in|with|working|designing|developing)\b",
    re.I,
)


class AnalysisRequirementV30(AnalysisRequirementV29):
    @model_validator(mode="before")
    @classmethod
    def preserve_explicit_prior_experience(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        concept = str(value.get("concept") or "")
        item = str(value.get("item_excerpt") or "")
        if (
            value.get("concept_type") in {"skill", "tool", "knowledge"}
            and _PRIOR_EXPERIENCE_RE.match(concept)
            and _PRIOR_EXPERIENCE_RE.match(item)
        ):
            return {**value, "concept_type": "experience"}
        return value


class JobAnalysisResponseV30(JobAnalysisResponseV29):
    requirements: list[AnalysisRequirementV30] = Field()


__all__ = ["AnalysisRequirementV30", "JobAnalysisResponseV30"]
