"""Lightweight typed contract for human-facing expert role interpretation."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

InterpretationStrength = Literal["highly_likely", "plausible", "speculative"]
ToolRelationship = Literal["source_named", "likely_example", "possible_example"]
_CERTAINTY_RE = re.compile(r"\b(?:mandatory|required|must|necessary|non-negotiable)\b", re.I)
_NEGATED_CERTAINTY_RE = re.compile(
    r"\b(?:not|isn't|is not|unlikely to be)\s+"
    r"(?:mandatory|required|necessary|non-negotiable)\b",
    re.I,
)


def _uses_absolute_requirement_language(value: str) -> bool:
    cleaned = _NEGATED_CERTAINTY_RE.sub("", value)
    return bool(_CERTAINTY_RE.search(cleaned))


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BlueprintToolExample(_StrictModel):
    """A source-named or analyst-suggested implementation example."""

    name: str
    relationship: ToolRelationship
    why_relevant: str

    @model_validator(mode="after")
    def inferred_tool_must_not_claim_source_certainty(self) -> BlueprintToolExample:
        if (
            self.relationship != "source_named"
            and _uses_absolute_requirement_language(self.why_relevant)
        ):
            raise ValueError(
                "Suggested tool examples cannot be described as mandatory/required/necessary; "
                "use source_named only for employer-named tools or soften the explanation."
            )
        return self


class BlueprintCapabilityArea(_StrictModel):
    """One professionally interpreted area of capability for the vacancy."""

    name: str
    interpretation_strength: InterpretationStrength
    likely_depth: str
    why_this_matters: str
    likely_subskills: list[str] = Field(max_length=20)
    likely_tools_or_examples: list[BlueprintToolExample] = Field(max_length=16)
    likely_work_products: list[str] = Field(max_length=16)
    likely_failure_modes_or_operational_concerns: list[str] = Field(max_length=16)
    probably_not_required: list[str] = Field(max_length=12)

    @model_validator(mode="after")
    def interpretation_strength_must_match_depth_language(self) -> BlueprintCapabilityArea:
        if (
            self.interpretation_strength != "highly_likely"
            and _uses_absolute_requirement_language(self.likely_depth)
        ):
            raise ValueError(
                "Plausible/speculative capability depth cannot use mandatory/required/must "
                "language; lower the certainty wording or raise the interpretation strength."
            )
        return self


class BlueprintInsight(_StrictModel):
    title: str
    explanation: str
    interpretation_strength: InterpretationStrength


class BlueprintScenario(_StrictModel):
    name: str
    why_likely: str
    flow_steps: list[str] = Field(min_length=2, max_length=16)
    engineering_concerns: list[str] = Field(max_length=16)
    interpretation_strength: InterpretationStrength


class RoleCapabilityBlueprint(_StrictModel):
    """Human-facing expert explanation built above JobHunter's strict analytical layers."""

    role_read: str
    likely_role_shape: str
    capability_areas: list[BlueprintCapabilityArea] = Field(min_length=1, max_length=12)
    hidden_requirements: list[BlueprintInsight] = Field(max_length=16)
    likely_end_to_end_scenarios: list[BlueprintScenario] = Field(max_length=8)
    what_probably_does_not_matter: list[str] = Field(max_length=16)
    important_unknowns: list[str] = Field(max_length=16)
    bottom_line: str
