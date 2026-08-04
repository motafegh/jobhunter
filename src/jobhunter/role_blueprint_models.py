"""Lightweight typed contract for human-facing expert role interpretation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

InterpretationStrength = Literal["highly_likely", "plausible", "speculative"]
ToolRelationship = Literal["source_named", "likely_example", "possible_example"]


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BlueprintToolExample(_StrictModel):
    """A source-named or analyst-suggested implementation example."""

    name: str
    relationship: ToolRelationship
    why_relevant: str


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
