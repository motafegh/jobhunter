"""Blueprint v5 contracts with source truth separated from professional inference."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

InferenceStrength = Literal["plausible", "speculative"]

_ABSOLUTE_REQUIREMENT_RE = re.compile(
    r"\b(?:mandatory|required|must|necessary|non-negotiable|has to|have to|"
    r"needs to|need to|expected to|responsible for)\b",
    re.I,
)
_NEGATED_REQUIREMENT_RE = re.compile(
    r"\b(?:not|isn't|is not|unlikely to be|probably not)\s+"
    r"(?:mandatory|required|necessary|non-negotiable)\b",
    re.I,
)
_END_TO_END_OWNERSHIP_RE = re.compile(
    r"\b(?:own|owns|owning)\s+(?:the\s+)?(?:entire|full|end-to-end)\s+"
    r"(?:lifecycle|stack|pipeline|system)\b",
    re.I,
)


def _uses_absolute_inference_language(value: str) -> bool:
    cleaned = _NEGATED_REQUIREMENT_RE.sub("", value)
    return bool(
        _ABSOLUTE_REQUIREMENT_RE.search(cleaned)
        or _END_TO_END_OWNERSHIP_RE.search(cleaned)
    )


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
# Model-facing draft. Every generated statement is professional inference.
# ---------------------------------------------------------------------------


class BlueprintProfessionalConsiderationDraft(_StrictModel):
    statement: str = Field(min_length=1)
    interpretation_strength: InferenceStrength
    uncertainty: str = Field(min_length=1)

    @model_validator(mode="after")
    def inference_cannot_claim_employer_obligation(
        self,
    ) -> BlueprintProfessionalConsiderationDraft:
        if _uses_absolute_inference_language(self.statement):
            raise ValueError(
                "Professional considerations cannot claim employer obligation or full ownership"
            )
        return self


class BlueprintCapabilityInterpretationDraft(_StrictModel):
    practical_interpretation: str = Field(min_length=1)
    professional_considerations: list[BlueprintProfessionalConsiderationDraft] = Field(
        default_factory=list,
        max_length=8,
    )
    probably_not_required: list[str] = Field(default_factory=list, max_length=8)
    important_unknowns: list[str] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    def interpretation_cannot_claim_employer_obligation(
        self,
    ) -> BlueprintCapabilityInterpretationDraft:
        if _uses_absolute_inference_language(self.practical_interpretation):
            raise ValueError(
                "Practical interpretation cannot claim employer obligation or full ownership"
            )
        for value in self.probably_not_required:
            if _uses_absolute_inference_language(value):
                raise ValueError(
                    "Probable non-requirements cannot contain unqualified obligation language"
                )
        return self


class RoleBlueprintDraft(_StrictModel):
    """LLM-owned v5 interpretation with no source or Capability provenance fields."""

    capability_interpretations: list[BlueprintCapabilityInterpretationDraft] = Field(
        min_length=1,
        max_length=12,
    )
    overall_unknowns: list[str] = Field(default_factory=list, max_length=12)


# ---------------------------------------------------------------------------
# Persisted v5 Blueprint. Source facts are copied by JobHunter, not the model.
# ---------------------------------------------------------------------------


class BlueprintSourceRolePurpose(_StrictModel):
    statement: str
    evidence: list[str] = Field(default_factory=list, max_length=8)


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


class BlueprintProfessionalConsideration(_StrictModel):
    statement: str
    interpretation_strength: InferenceStrength
    uncertainty: str


class BlueprintCapabilityArea(_StrictModel):
    name: str
    source_capability_index: int
    interpretation_strength: Literal["plausible"] = "plausible"
    practical_interpretation: str
    source_requirements: list[BlueprintSourceRequirement] = Field(
        default_factory=list,
        max_length=40,
    )
    source_responsibilities: list[BlueprintSourceResponsibility] = Field(
        default_factory=list,
        max_length=24,
    )
    professional_considerations: list[BlueprintProfessionalConsideration] = Field(
        default_factory=list,
        max_length=8,
    )
    probably_not_required: list[str] = Field(default_factory=list, max_length=8)
    important_unknowns: list[str] = Field(default_factory=list, max_length=8)


class RoleCapabilityBlueprint(_StrictModel):
    """Persisted v5 Blueprint: deterministic employer truth plus bounded interpretation."""

    source_role_purpose: list[BlueprintSourceRolePurpose] = Field(
        default_factory=list,
        max_length=8,
    )
    source_capability_coverage: list[int] = Field(default_factory=list, max_length=24)
    source_role_constraints: list[BlueprintSourceConstraint] = Field(
        default_factory=list,
        max_length=16,
    )
    capability_areas: list[BlueprintCapabilityArea] = Field(min_length=1, max_length=12)
    overall_unknowns: list[str] = Field(default_factory=list, max_length=12)


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


def reconcile_role_blueprint_v5(
    draft: RoleBlueprintDraft,
    *,
    accepted_extraction: dict[str, Any],
    capability_intelligence: dict[str, Any],
) -> RoleCapabilityBlueprint:
    """Attach accepted P1.6 provenance while keeping generated text explicitly inferential."""

    requirements = list(accepted_extraction.get("requirements") or [])
    responsibilities = list(accepted_extraction.get("responsibilities") or [])
    capability_profiles = list(capability_intelligence.get("capabilities") or [])
    source_truth = capability_intelligence.get("source_truth")
    if not isinstance(source_truth, dict):
        raise ValueError("Blueprint v5 requires accepted Capability v7 source_truth")
    if not capability_profiles:
        raise ValueError("Blueprint v5 requires at least one accepted Capability profile")
    if len(draft.capability_interpretations) != len(capability_profiles):
        raise ValueError(
            "Blueprint v5 requires exactly one interpretation per accepted Capability profile "
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
                practical_interpretation=interpretation.practical_interpretation,
                source_requirements=[
                    _source_requirement(requirements[index], requirement_index=index)
                    for index in requirement_indices
                    if isinstance(requirements[index], dict)
                ],
                source_responsibilities=[
                    _source_responsibility(responsibilities[index], responsibility_index=index)
                    for index in responsibility_indices
                    if isinstance(responsibilities[index], dict)
                ],
                professional_considerations=[
                    BlueprintProfessionalConsideration.model_validate(
                        item.model_dump(mode="python")
                    )
                    for item in interpretation.professional_considerations
                ],
                probably_not_required=interpretation.probably_not_required,
                important_unknowns=interpretation.important_unknowns,
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

    role_purpose = [
        BlueprintSourceRolePurpose(
            statement=str(item.get("statement") or ""),
            evidence=_evidence_list(item.get("evidence")),
        )
        for item in accepted_extraction.get("role_purpose") or []
        if isinstance(item, dict) and str(item.get("statement") or "").strip()
    ]

    return RoleCapabilityBlueprint(
        source_role_purpose=role_purpose,
        source_capability_coverage=list(range(len(capability_profiles))),
        source_role_constraints=role_constraints,
        capability_areas=areas,
        overall_unknowns=draft.overall_unknowns,
    )
