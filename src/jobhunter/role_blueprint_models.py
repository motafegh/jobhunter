"""Typed contract and deterministic grounding for Role Capability Blueprint v3."""

from __future__ import annotations

import re
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

InterpretationStrength = Literal["highly_likely", "plausible", "speculative"]
ToolRelationship = Literal["source_named", "likely_example", "possible_example"]
SourceRequirementStrength = Literal[
    "required",
    "preferred",
    "contextual",
    "inferred",
    "mixed",
    "unspecified",
]
ScenarioBasis = Literal["source_stated_workflow", "professional_example"]

_CERTAINTY_RE = re.compile(r"\b(?:mandatory|required|must|necessary|non-negotiable)\b", re.I)
_NEGATED_CERTAINTY_RE = re.compile(
    r"\b(?:not|isn't|is not|unlikely to be)\s+"
    r"(?:mandatory|required|necessary|non-negotiable)\b",
    re.I,
)
_EXPERT_DEPTH_RE = re.compile(r"\b(?:mastery|expert(?:-level)?)\b", re.I)


def _uses_absolute_requirement_language(value: str) -> bool:
    cleaned = _NEGATED_CERTAINTY_RE.sub("", value)
    return bool(_CERTAINTY_RE.search(cleaned))


def _dedupe_indices(values: list[int]) -> list[int]:
    result: list[int] = []
    seen: set[int] = set()
    for value in values:
        if value < 0:
            raise ValueError("Source indices cannot be negative")
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _derived_strength(
    indices: list[int],
    requirements: list[dict[str, Any]],
) -> SourceRequirementStrength:
    strengths = {
        str(requirements[index].get("requirement_type") or "").strip()
        for index in indices
        if str(requirements[index].get("requirement_type") or "").strip()
    }
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        value = next(iter(strengths))
        if value in {"required", "preferred", "contextual", "inferred"}:
            return cast(SourceRequirementStrength, value)
        return "unspecified"
    return "mixed"


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BlueprintSourceConstraint(_StrictModel):
    """Role-level employer fact deterministically copied from accepted P1.6."""

    requirement_index: int
    concept: str
    requirement_type: str
    depth_signal: str | None = None
    evidence: list[str] = Field(max_length=8)


class BlueprintToolExample(_StrictModel):
    """A source-named or analyst-suggested implementation example."""

    name: str
    relationship: ToolRelationship
    why_relevant: str
    source_requirement_indices: list[int] = Field(default_factory=list, max_length=8)
    source_responsibility_indices: list[int] = Field(default_factory=list, max_length=8)
    source_requirement_strength: SourceRequirementStrength = "unspecified"
    source_depth_signals: list[str] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    def relationship_matches_source_links(self) -> BlueprintToolExample:
        self.source_requirement_indices = _dedupe_indices(self.source_requirement_indices)
        self.source_responsibility_indices = _dedupe_indices(self.source_responsibility_indices)
        if self.relationship == "source_named":
            if not self.source_requirement_indices and not self.source_responsibility_indices:
                raise ValueError("source_named tools must link at least one accepted P1.6 fact")
        else:
            if self.source_requirement_indices or self.source_responsibility_indices:
                raise ValueError("Inferred tool examples cannot claim accepted P1.6 source links")
            if self.source_requirement_strength != "unspecified" or self.source_depth_signals:
                raise ValueError(
                    "Inferred tool examples cannot carry deterministic source strength/depth"
                )
            if _uses_absolute_requirement_language(self.why_relevant):
                raise ValueError(
                    "Suggested tool examples cannot be described as mandatory/required/necessary"
                )
        return self


class BlueprintCapabilityArea(_StrictModel):
    """One professionally interpreted area grounded in accepted Capability profiles."""

    name: str
    source_capability_indices: list[int] = Field(min_length=1, max_length=8)
    interpretation_strength: InterpretationStrength
    likely_depth: str
    why_this_matters: str
    likely_subskills: list[str] = Field(max_length=20)
    likely_tools_or_examples: list[BlueprintToolExample] = Field(max_length=16)
    likely_work_products: list[str] = Field(max_length=16)
    likely_failure_modes_or_operational_concerns: list[str] = Field(max_length=16)
    probably_not_required: list[str] = Field(max_length=12)

    @model_validator(mode="after")
    def validate_area(self) -> BlueprintCapabilityArea:
        self.source_capability_indices = _dedupe_indices(self.source_capability_indices)
        if (
            self.interpretation_strength != "highly_likely"
            and _uses_absolute_requirement_language(self.likely_depth)
        ):
            raise ValueError(
                "Plausible/speculative capability depth cannot use mandatory/required/must language"
            )
        return self


class BlueprintInsight(_StrictModel):
    title: str
    explanation: str
    interpretation_strength: InterpretationStrength
    source_capability_indices: list[int] = Field(default_factory=list, max_length=8)
    source_responsibility_indices: list[int] = Field(default_factory=list, max_length=16)

    @model_validator(mode="after")
    def highly_likely_requires_grounding(self) -> BlueprintInsight:
        self.source_capability_indices = _dedupe_indices(self.source_capability_indices)
        self.source_responsibility_indices = _dedupe_indices(self.source_responsibility_indices)
        if (
            self.interpretation_strength == "highly_likely"
            and not self.source_capability_indices
            and not self.source_responsibility_indices
        ):
            raise ValueError("Highly likely hidden requirements must link accepted upstream work")
        return self


class BlueprintScenario(_StrictModel):
    name: str
    why_likely: str
    flow_steps: list[str] = Field(min_length=2, max_length=16)
    engineering_concerns: list[str] = Field(max_length=16)
    interpretation_strength: InterpretationStrength
    scenario_basis: ScenarioBasis
    source_capability_indices: list[int] = Field(default_factory=list, max_length=8)
    source_responsibility_indices: list[int] = Field(default_factory=list, max_length=16)
    assumptions: list[str] = Field(default_factory=list, max_length=12)

    @model_validator(mode="after")
    def scenario_certainty_matches_basis(self) -> BlueprintScenario:
        self.source_capability_indices = _dedupe_indices(self.source_capability_indices)
        self.source_responsibility_indices = _dedupe_indices(self.source_responsibility_indices)
        if (
            self.scenario_basis == "professional_example"
            and self.interpretation_strength == "highly_likely"
        ):
            raise ValueError("Professional example scenarios cannot be highly_likely")
        if self.scenario_basis == "source_stated_workflow" and not self.source_responsibility_indices:
            raise ValueError("source_stated_workflow scenarios must link an accepted responsibility")
        if self.interpretation_strength == "highly_likely" and self.assumptions:
            raise ValueError("Highly likely scenarios cannot depend on unresolved assumptions")
        return self


class RoleCapabilityBlueprint(_StrictModel):
    """Human-facing expert explanation built above JobHunter's accepted analytical layers."""

    role_read: str
    likely_role_shape: str
    source_capability_coverage: list[int] = Field(default_factory=list, max_length=24)
    source_role_constraints: list[BlueprintSourceConstraint] = Field(default_factory=list, max_length=16)
    capability_areas: list[BlueprintCapabilityArea] = Field(min_length=1, max_length=12)
    hidden_requirements: list[BlueprintInsight] = Field(max_length=16)
    likely_end_to_end_scenarios: list[BlueprintScenario] = Field(max_length=8)
    what_probably_does_not_matter: list[str] = Field(max_length=16)
    important_unknowns: list[str] = Field(max_length=16)
    bottom_line: str


def reconcile_role_blueprint(
    blueprint: RoleCapabilityBlueprint,
    *,
    accepted_extraction: dict[str, Any],
    capability_intelligence: dict[str, Any],
) -> RoleCapabilityBlueprint:
    """Reconcile mechanically provable Blueprint grounding against accepted upstream truth."""

    payload = blueprint.model_dump(mode="python")
    requirements = list(accepted_extraction.get("requirements") or [])
    responsibilities = list(accepted_extraction.get("responsibilities") or [])
    capability_profiles = list(capability_intelligence.get("capabilities") or [])
    source_truth = capability_intelligence.get("source_truth")
    if not isinstance(source_truth, dict):
        raise ValueError("Blueprint v3 requires accepted Capability v7 source_truth")

    def validate_indices(values: list[int], *, upper: int, label: str) -> list[int]:
        deduped = _dedupe_indices(values)
        missing = [value for value in deduped if value >= upper]
        if missing:
            raise ValueError(f"{label} reference missing accepted upstream items: {missing}")
        return deduped

    covered_capabilities: set[int] = set()
    for area in payload["capability_areas"]:
        area["source_capability_indices"] = validate_indices(
            area["source_capability_indices"],
            upper=len(capability_profiles),
            label="Capability area",
        )
        covered_capabilities.update(area["source_capability_indices"])
        for tool in area["likely_tools_or_examples"]:
            tool["source_requirement_indices"] = validate_indices(
                tool["source_requirement_indices"],
                upper=len(requirements),
                label="Tool requirement",
            )
            tool["source_responsibility_indices"] = validate_indices(
                tool["source_responsibility_indices"],
                upper=len(responsibilities),
                label="Tool responsibility",
            )
            if tool["relationship"] == "source_named":
                tool["source_requirement_strength"] = _derived_strength(
                    tool["source_requirement_indices"], requirements
                )
                tool["source_depth_signals"] = [
                    str(requirements[index].get("depth_signal")).strip()
                    for index in tool["source_requirement_indices"]
                    if requirements[index].get("depth_signal")
                ]
                if (
                    tool["source_requirement_strength"] != "required"
                    and _uses_absolute_requirement_language(tool["why_relevant"])
                ):
                    raise ValueError(
                        "A non-required source-named tool cannot be described as "
                        "mandatory/required/necessary"
                    )
                if _EXPERT_DEPTH_RE.search(tool["why_relevant"]) and not any(
                    re.search(r"\b(?:expert|mastery)\b", signal, re.I)
                    for signal in tool["source_depth_signals"]
                ):
                    raise ValueError(
                        "Source-named tool cannot claim expert/mastery depth without matching "
                        "P1.6 depth"
                    )
            else:
                tool["source_requirement_indices"] = []
                tool["source_responsibility_indices"] = []
                tool["source_requirement_strength"] = "unspecified"
                tool["source_depth_signals"] = []

    expected_capabilities = set(range(len(capability_profiles)))
    if covered_capabilities != expected_capabilities:
        missing = sorted(expected_capabilities - covered_capabilities)
        extra = sorted(covered_capabilities - expected_capabilities)
        raise ValueError(
            "Blueprint capability coverage must match accepted Capability profiles; "
            f"missing={missing}, extra={extra}"
        )
    payload["source_capability_coverage"] = sorted(covered_capabilities)

    for insight in payload["hidden_requirements"]:
        insight["source_capability_indices"] = validate_indices(
            insight["source_capability_indices"],
            upper=len(capability_profiles),
            label="Hidden requirement capability",
        )
        insight["source_responsibility_indices"] = validate_indices(
            insight["source_responsibility_indices"],
            upper=len(responsibilities),
            label="Hidden requirement responsibility",
        )

    for scenario in payload["likely_end_to_end_scenarios"]:
        scenario["source_capability_indices"] = validate_indices(
            scenario["source_capability_indices"],
            upper=len(capability_profiles),
            label="Scenario capability",
        )
        scenario["source_responsibility_indices"] = validate_indices(
            scenario["source_responsibility_indices"],
            upper=len(responsibilities),
            label="Scenario responsibility",
        )

    role_level_indices = validate_indices(
        list(source_truth.get("role_level_requirement_indices") or []),
        upper=len(requirements),
        label="Role-level requirement",
    )
    payload["source_role_constraints"] = [
        {
            "requirement_index": index,
            "concept": str(requirements[index].get("concept") or ""),
            "requirement_type": str(requirements[index].get("requirement_type") or ""),
            "depth_signal": requirements[index].get("depth_signal"),
            "evidence": list(requirements[index].get("evidence") or []),
        }
        for index in role_level_indices
    ]

    return RoleCapabilityBlueprint.model_validate(payload)
