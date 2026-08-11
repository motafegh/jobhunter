"""Blueprint v4 contracts: model interpretation above deterministic upstream provenance."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

InterpretationStrength = Literal["highly_likely", "plausible", "speculative"]
DerivedInterpretationStrength = Literal["plausible", "speculative"]
SuggestedToolRelationship = Literal["likely_example", "possible_example"]
SourceRequirementStrength = Literal[
    "required",
    "preferred",
    "contextual",
    "inferred",
    "mixed",
    "unspecified",
]

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


def _evidence_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        cleaned = value.strip()
        return [cleaned] if cleaned else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    raise ValueError("Accepted P1.6 evidence must be a string or list of strings")


def _validated_indices(values: Any, *, upper: int, label: str) -> list[int]:
    if not isinstance(values, list):
        raise ValueError(f"{label} must be a list")
    result: list[int] = []
    for value in values:
        if not isinstance(value, int) or value < 0 or value >= upper:
            raise ValueError(f"{label} contains invalid upstream index {value!r}")
        if value not in result:
            result.append(value)
    return result


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------------------
# Model-facing draft. The LLM never emits upstream numeric provenance.
# ---------------------------------------------------------------------------


class BlueprintSuggestedToolDraft(_StrictModel):
    name: str = Field(min_length=1)
    relationship: SuggestedToolRelationship
    why_relevant: str = Field(min_length=1)

    @model_validator(mode="after")
    def inferred_examples_cannot_become_requirements(self) -> BlueprintSuggestedToolDraft:
        if _uses_absolute_requirement_language(self.why_relevant):
            raise ValueError(
                "Suggested tools are practitioner examples and cannot be described as "
                "mandatory/required/necessary"
            )
        if _EXPERT_DEPTH_RE.search(self.why_relevant):
            raise ValueError(
                "Suggested tools cannot claim expert/mastery depth without employer source depth"
            )
        return self


class BlueprintCapabilityInterpretationDraft(_StrictModel):
    interpretation_strength: InterpretationStrength
    likely_depth: str = Field(min_length=1)
    why_this_matters: str = Field(min_length=1)
    likely_subskills: list[str] = Field(default_factory=list, max_length=20)
    suggested_tools_or_examples: list[BlueprintSuggestedToolDraft] = Field(
        default_factory=list,
        max_length=12,
    )
    likely_work_products: list[str] = Field(default_factory=list, max_length=16)
    likely_failure_modes_or_operational_concerns: list[str] = Field(
        default_factory=list,
        max_length=16,
    )
    probably_not_required: list[str] = Field(default_factory=list, max_length=12)

    @model_validator(mode="after")
    def uncertain_depth_cannot_use_absolute_language(
        self,
    ) -> BlueprintCapabilityInterpretationDraft:
        if (
            self.interpretation_strength != "highly_likely"
            and _uses_absolute_requirement_language(self.likely_depth)
        ):
            raise ValueError(
                "Plausible/speculative capability depth cannot use mandatory/required/must language"
            )
        return self


class BlueprintHiddenRequirementDraft(_StrictModel):
    """Model-created unstated requirement; deliberately never treated as source fact."""

    title: str = Field(min_length=1)
    explanation: str = Field(min_length=1)
    interpretation_strength: DerivedInterpretationStrength


class BlueprintProfessionalScenarioDraft(_StrictModel):
    """Illustrative practitioner workflow, never an asserted employer architecture."""

    name: str = Field(min_length=1)
    why_useful: str = Field(min_length=1)
    flow_steps: list[str] = Field(min_length=2, max_length=16)
    engineering_concerns: list[str] = Field(default_factory=list, max_length=16)
    interpretation_strength: DerivedInterpretationStrength
    assumptions: list[str] = Field(default_factory=list, max_length=12)


class RoleBlueprintDraft(_StrictModel):
    """LLM-owned semantic interpretation before JobHunter attaches provenance."""

    role_read: str = Field(min_length=1)
    likely_role_shape: str = Field(min_length=1)
    capability_interpretations: list[BlueprintCapabilityInterpretationDraft] = Field(
        min_length=1,
        max_length=12,
    )
    hidden_requirements: list[BlueprintHiddenRequirementDraft] = Field(
        default_factory=list,
        max_length=16,
    )
    professional_example_scenarios: list[BlueprintProfessionalScenarioDraft] = Field(
        default_factory=list,
        max_length=8,
    )
    what_probably_does_not_matter: list[str] = Field(default_factory=list, max_length=16)
    important_unknowns: list[str] = Field(default_factory=list, max_length=16)
    bottom_line: str = Field(min_length=1)


# ---------------------------------------------------------------------------
# Persisted v4 Blueprint. All upstream indices/source facts are JobHunter-owned.
# ---------------------------------------------------------------------------


class BlueprintSourceRequirement(_StrictModel):
    requirement_index: int
    concept: str
    concept_type: str
    requirement_type: str
    depth_signal: str | None = None
    evidence: list[str] = Field(default_factory=list, max_length=8)


class BlueprintSourceResponsibility(_StrictModel):
    responsibility_index: int
    statement: str
    evidence: list[str] = Field(default_factory=list, max_length=8)


class BlueprintSourceConstraint(_StrictModel):
    requirement_index: int
    concept: str
    requirement_type: str
    depth_signal: str | None = None
    evidence: list[str] = Field(default_factory=list, max_length=8)


class BlueprintSuggestedTool(_StrictModel):
    name: str
    relationship: SuggestedToolRelationship
    why_relevant: str


class BlueprintCapabilityArea(_StrictModel):
    name: str
    source_capability_index: int
    interpretation_strength: InterpretationStrength
    likely_depth: str
    why_this_matters: str
    likely_subskills: list[str] = Field(default_factory=list, max_length=20)
    source_requirements: list[BlueprintSourceRequirement] = Field(
        default_factory=list,
        max_length=40,
    )
    source_responsibilities: list[BlueprintSourceResponsibility] = Field(
        default_factory=list,
        max_length=24,
    )
    suggested_tools_or_examples: list[BlueprintSuggestedTool] = Field(
        default_factory=list,
        max_length=12,
    )
    likely_work_products: list[str] = Field(default_factory=list, max_length=16)
    likely_failure_modes_or_operational_concerns: list[str] = Field(
        default_factory=list,
        max_length=16,
    )
    probably_not_required: list[str] = Field(default_factory=list, max_length=12)


class BlueprintHiddenRequirement(_StrictModel):
    title: str
    explanation: str
    interpretation_strength: DerivedInterpretationStrength


class BlueprintProfessionalScenario(_StrictModel):
    name: str
    why_useful: str
    flow_steps: list[str] = Field(min_length=2, max_length=16)
    engineering_concerns: list[str] = Field(default_factory=list, max_length=16)
    interpretation_strength: DerivedInterpretationStrength
    scenario_basis: Literal["professional_example"] = "professional_example"
    assumptions: list[str] = Field(default_factory=list, max_length=12)


class RoleCapabilityBlueprint(_StrictModel):
    """Persisted Blueprint v4: model interpretation plus deterministic source anchors."""

    role_read: str
    likely_role_shape: str
    source_capability_coverage: list[int] = Field(default_factory=list, max_length=24)
    source_role_constraints: list[BlueprintSourceConstraint] = Field(
        default_factory=list,
        max_length=16,
    )
    capability_areas: list[BlueprintCapabilityArea] = Field(min_length=1, max_length=12)
    hidden_requirements: list[BlueprintHiddenRequirement] = Field(
        default_factory=list,
        max_length=16,
    )
    professional_example_scenarios: list[BlueprintProfessionalScenario] = Field(
        default_factory=list,
        max_length=8,
    )
    what_probably_does_not_matter: list[str] = Field(default_factory=list, max_length=16)
    important_unknowns: list[str] = Field(default_factory=list, max_length=16)
    bottom_line: str


def _source_requirement(
    requirement: dict[str, Any],
    *,
    requirement_index: int,
) -> BlueprintSourceRequirement:
    return BlueprintSourceRequirement(
        requirement_index=requirement_index,
        concept=str(requirement.get("concept") or ""),
        concept_type=str(requirement.get("concept_type") or ""),
        requirement_type=str(requirement.get("requirement_type") or ""),
        depth_signal=requirement.get("depth_signal"),
        evidence=_evidence_list(requirement.get("evidence")),
    )


def _source_responsibility(
    responsibility: dict[str, Any],
    *,
    responsibility_index: int,
) -> BlueprintSourceResponsibility:
    return BlueprintSourceResponsibility(
        responsibility_index=responsibility_index,
        statement=str(responsibility.get("statement") or ""),
        evidence=_evidence_list(responsibility.get("evidence")),
    )


def reconcile_role_blueprint_v4(
    draft: RoleBlueprintDraft,
    *,
    accepted_extraction: dict[str, Any],
    capability_intelligence: dict[str, Any],
) -> RoleCapabilityBlueprint:
    """Attach all mechanically known provenance without asking the model to reproduce it."""

    requirements = list(accepted_extraction.get("requirements") or [])
    responsibilities = list(accepted_extraction.get("responsibilities") or [])
    capability_profiles = list(capability_intelligence.get("capabilities") or [])
    source_truth = capability_intelligence.get("source_truth")
    if not isinstance(source_truth, dict):
        raise ValueError("Blueprint v4 requires accepted Capability v7 source_truth")
    if not capability_profiles:
        raise ValueError("Blueprint v4 requires at least one accepted Capability profile")
    if len(draft.capability_interpretations) != len(capability_profiles):
        raise ValueError(
            "Blueprint v4 requires exactly one interpretation per accepted Capability profile "
            f"in source order: expected={len(capability_profiles)}, "
            f"actual={len(draft.capability_interpretations)}"
        )

    areas: list[BlueprintCapabilityArea] = []
    for capability_index, (profile, interpretation) in enumerate(
        zip(capability_profiles, draft.capability_interpretations, strict=True)
    ):
        if not isinstance(profile, dict):
            raise ValueError(f"Capability profile {capability_index} must be an object")
        requirement_indices = _validated_indices(
            profile.get("source_requirement_indices") or [],
            upper=len(requirements),
            label=f"Capability {capability_index} requirement links",
        )
        responsibility_indices = _validated_indices(
            profile.get("source_responsibility_indices") or [],
            upper=len(responsibilities),
            label=f"Capability {capability_index} responsibility links",
        )
        areas.append(
            BlueprintCapabilityArea(
                name=str(profile.get("capability_label") or f"Capability {capability_index + 1}"),
                source_capability_index=capability_index,
                interpretation_strength=interpretation.interpretation_strength,
                likely_depth=interpretation.likely_depth,
                why_this_matters=interpretation.why_this_matters,
                likely_subskills=interpretation.likely_subskills,
                source_requirements=[
                    _source_requirement(
                        requirements[index],
                        requirement_index=index,
                    )
                    for index in requirement_indices
                    if isinstance(requirements[index], dict)
                ],
                source_responsibilities=[
                    _source_responsibility(
                        responsibilities[index],
                        responsibility_index=index,
                    )
                    for index in responsibility_indices
                    if isinstance(responsibilities[index], dict)
                ],
                suggested_tools_or_examples=[
                    BlueprintSuggestedTool.model_validate(item.model_dump(mode="python"))
                    for item in interpretation.suggested_tools_or_examples
                ],
                likely_work_products=interpretation.likely_work_products,
                likely_failure_modes_or_operational_concerns=(
                    interpretation.likely_failure_modes_or_operational_concerns
                ),
                probably_not_required=interpretation.probably_not_required,
            )
        )

    role_level_indices = _validated_indices(
        source_truth.get("role_level_requirement_indices") or [],
        upper=len(requirements),
        label="Role-level requirement links",
    )
    role_constraints = [
        BlueprintSourceConstraint(
            requirement_index=index,
            concept=str(requirements[index].get("concept") or ""),
            requirement_type=str(requirements[index].get("requirement_type") or ""),
            depth_signal=requirements[index].get("depth_signal"),
            evidence=_evidence_list(requirements[index].get("evidence")),
        )
        for index in role_level_indices
        if isinstance(requirements[index], dict)
    ]

    return RoleCapabilityBlueprint(
        role_read=draft.role_read,
        likely_role_shape=draft.likely_role_shape,
        source_capability_coverage=list(range(len(capability_profiles))),
        source_role_constraints=role_constraints,
        capability_areas=areas,
        hidden_requirements=[
            BlueprintHiddenRequirement.model_validate(item.model_dump(mode="python"))
            for item in draft.hidden_requirements
        ],
        professional_example_scenarios=[
            BlueprintProfessionalScenario(
                **item.model_dump(mode="python"),
                scenario_basis="professional_example",
            )
            for item in draft.professional_example_scenarios
        ],
        what_probably_does_not_matter=draft.what_probably_does_not_matter,
        important_unknowns=draft.important_unknowns,
        bottom_line=draft.bottom_line,
    )
