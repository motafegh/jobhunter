"""Candidate-only typed response model for P1.6 v14.

v14 keeps the shared P1.6 depth validator strict, but normalizes work-arrangement phrases such as
``full-time`` / ``part-time`` out of ``depth_signal`` before that validator runs. These phrases are
schedule/employment context, not employer-stated capability depth. Genuine accepted depth or
experience-extent signals remain untouched.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, model_validator

from jobhunter.inference.instructor_lm_studio import (
    AnalysisRequirement,
    JobAnalysisResponse,
    _DEPTH_SIGNAL_PATTERNS,
)

_WORK_SCHEDULE_RE = re.compile(r"\b(?:full[ -]?time|part[ -]?time)\b", re.I)


def _schedule_only_depth_signal(value: str) -> bool:
    """Return true only when schedule wording is present without an accepted depth signal."""

    if _WORK_SCHEDULE_RE.search(value) is None:
        return False
    return not any(pattern.search(value) for pattern in _DEPTH_SIGNAL_PATTERNS.values())


class AnalysisRequirementV14(AnalysisRequirement):
    """Apply v14 schedule/depth normalization before shared requirement validation."""

    @model_validator(mode="before")
    @classmethod
    def normalize_schedule_only_depth(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        signal = value.get("depth_signal")
        if not isinstance(signal, str) or not signal.strip():
            return value
        if not _schedule_only_depth_signal(signal):
            return value
        normalized = dict(value)
        normalized["depth_signal"] = None
        return normalized


class JobAnalysisResponseV14(JobAnalysisResponse):
    """v14 typed response with schedule-only depth normalization."""

    requirements: list[AnalysisRequirementV14] = Field(max_length=32)


__all__ = [
    "AnalysisRequirementV14",
    "JobAnalysisResponseV14",
    "_schedule_only_depth_signal",
]
