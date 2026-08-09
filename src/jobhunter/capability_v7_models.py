"""Capability v7 source-truth boundary above the accepted P1.6 substrate."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator

from jobhunter.capability_models import (
    CapabilityExpectation,
    CapabilityProfile,
    CrossCapabilityObservation,
    JobCapabilityIntelligence as V6JobCapabilityIntelligence,
    RequirementStrength,
)

SourceRequirementStrength = Literal["required", "preferred", "contextual", "inferred"]
Confidence = Literal["high", "medium", "low"]

_P1_REQUIREMENT_STRENGTHS = {"required", "preferred", "contextual", "inferred"}
_DERIVED_STATUSES = {"strongly_implied_by_work", "model_inferred_prerequisite"}
_MODEL_DERIVED_SECTION_NAMES = (
    "sub_capabilities",
    "underlying_knowledge",
    "operational_practices",
    "operational_context",
)
_DURATION_ONLY_RE = re.compile(
    r"^\s*(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"(?:\s*(?:-|–|—|to)\s*"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten))?"
    r"\s+years?(?:\s+of\s+(?:professional\s+)?experience)?\s*$",
    re.IGNORECASE,
)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _confidence(value: Any) -> Confidence:
    return value if value in {"high", "medium", "low"} else "high"


def _evidence_values(item: dict[str, Any]) -> list[str]:
    raw = item.get("evidence")
    values = raw if isinstance(raw, list) else [raw]
    return [
        value.strip()
        for value in values
        if isinstance(value, str) and value.strip()
    ]


def _accepted_extraction(info: ValidationInfo) -> dict[str, Any] | None:
    extraction = (info.context or {}).get("accepted_extraction")
    if extraction is None:
        return None
    if not isinstance(extraction, dict):
        raise ValueError("capability validation context contains invalid accepted_extraction")
    return extraction


def _is_role_level_requirement(requirement: dict[str, Any]) -> bool:
    """Keep role-entry constraints separate from technical capability grouping."""

    concept_type = str(requirement.get("concept_type") or "").casefold()
    if concept_type == "education":
        return True
    if concept_type != "experience":
        return False

    candidates = [
        requirement.get("depth_signal"),
        requirement.get("evidence"),
        requirement.get("concept"),
    ]
    return any(
        isinstance(value, str) and _DURATION_ONLY_RE.fullmatch(value)
        for value in candidates
    )


def partition_source_requirements(
    accepted_extraction: dict[str, Any],
) -> tuple[list[int], list[int]]:
    """Partition accepted requirements into capability-relevant and role-level constraints."""

    requirements = accepted_extraction.get("requirements") or []
    if not isinstance(requirements, list):
        raise ValueError("accepted_extraction.requirements must be a list")

    capability_indices: list[int] = []
    role_level_indices: list[int] = []
    for index, item in enumerate(requirements):
        if isinstance(item, dict) and _is_role_level_requirement(item):
            role_level_indices.append(index)
        else:
            capability_indices.append(index)
    return capability_indices, role_level_indices


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CapabilitySourcePurpose(_StrictModel):
    index: int
    statement: str
    evidence: list[str]
    confidence: Confidence


class CapabilitySourceRequirement(_StrictModel):
    index: int
    concept: str
    concept_type: str
    requirement_type: SourceRequirementStrength
    depth_signal: str | None
    evidence: list[str]
    confidence: Confidence


class CapabilitySourceResponsibility(_StrictModel):
    index: int
    statement: str
    evidence: list[str]
    confidence: Confidence


class CapabilitySourceTruth(_StrictModel):
    """JobHunter-owned complete projection of accepted P1.6 facts and coverage."""

    role_purpose: list[CapabilitySourcePurpose]
    requirements: list[CapabilitySourceRequirement]
    responsibilities: list[CapabilitySourceResponsibility]
    capability_requirement_indices: list[int]
    role_level_requirement_indices: list[int]
    linked_requirement_indices: list[int]
    unlinked_capability_requirement_indices: list[int]
    linked_responsibility_indices: list[int]
    unlinked_responsibility_indices: list[int]
    explicit_depth_requirement_indices: list[int]
    linked_explicit_depth_requirement_indices: list[int]
    unlinked_explicit_depth_requirement_indices: list[int]


class CapabilityReasoningDraft(V6JobCapabilityIntelligence):
    """LLM-owned grouping and derived reasoning before deterministic v7 reconciliation."""

    @model_validator(mode="after")
    def complete_source_coverage(
        self,
        info: ValidationInfo,
    ) -> "CapabilityReasoningDraft":
        extraction = _accepted_extraction(info)
        if extraction is None:
            return self

        requirements = extraction.get("requirements") or []
        responsibilities = extraction.get("responsibilities") or []
        if not isinstance(requirements, list):
            raise ValueError("accepted_extraction.requirements must be a list")
        if not isinstance(responsibilities, list):
            raise ValueError("accepted_extraction.responsibilities must be a list")

        capability_requirements, _ = partition_source_requirements(extraction)
        linked_requirements = {
            index
            for profile in self.capabilities
            for index in profile.source_requirement_indices
        }
        linked_responsibilities = {
            index
            for profile in self.capabilities
            for index in profile.source_responsibility_indices
        }

        missing_requirements = sorted(set(capability_requirements) - linked_requirements)
        if missing_requirements:
            raise ValueError(
                "Capability grouping omitted capability-relevant accepted P1.6 requirements: "
                f"{missing_requirements}"
            )

        missing_responsibilities = sorted(
            set(range(len(responsibilities))) - linked_responsibilities
        )
        if missing_responsibilities:
            raise ValueError(
                "Capability grouping omitted accepted P1.6 responsibilities: "
                f"{missing_responsibilities}"
            )

        if (
            len(responsibilities) >= 5
            and len(requirements) >= 12
            and len(self.capabilities) < 2
        ):
            raise ValueError(
                "Dense accepted P1.6 evidence requires at least two coherent capability profiles"
            )

        if len(self.capabilities) < 2 and self.cross_capability_observations:
            raise ValueError(
                "cross_capability_observations require at least two capability profiles"
            )
        return self


class JobCapabilityIntelligence(CapabilityReasoningDraft):
    """Persisted v7 artifact: semantic reasoning plus JobHunter-owned source truth."""

    source_truth: CapabilitySourceTruth | None = None


def _deterministic_requirement_strength(
    requirement_indices: list[int],
    requirements: list[Any],
) -> RequirementStrength:
    strengths = {
        item.get("requirement_type")
        for index in requirement_indices
        if 0 <= index < len(requirements)
        and isinstance((item := requirements[index]), dict)
        and item.get("requirement_type") in _P1_REQUIREMENT_STRENGTHS
    }
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        return next(iter(strengths))  # type: ignore[return-value]
    return "mixed"


def _deterministic_depth_expectations(
    requirement_indices: list[int],
    requirements: list[Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str, tuple[str, ...]]] = set()
    for index in requirement_indices:
        if not 0 <= index < len(requirements):
            continue
        requirement = requirements[index]
        if not isinstance(requirement, dict):
            continue
        depth = requirement.get("depth_signal")
        if not isinstance(depth, str) or not depth.strip():
            continue
        concept = requirement.get("concept")
        if not isinstance(concept, str) or not concept.strip():
            concept = "Linked requirement"
        evidence = _evidence_values(requirement)
        if not evidence:
            continue
        key = (_normalize(concept), _normalize(depth), tuple(evidence))
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "statement": f"{concept} — employer-stated depth: {depth}",
                "evidence_status": "source_explicit",
                "evidence": evidence,
                "rationale": (
                    "Deterministically propagated from accepted P1.6 requirement "
                    f"{index}; not model-inferred."
                ),
                "confidence": _confidence(requirement.get("confidence")),
            }
        )
    return items


def _deterministic_work_activities(
    responsibility_indices: list[int],
    responsibilities: list[Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for index in responsibility_indices:
        if not 0 <= index < len(responsibilities):
            continue
        responsibility = responsibilities[index]
        if not isinstance(responsibility, dict):
            continue
        statement = responsibility.get("statement")
        evidence = _evidence_values(responsibility)
        if not isinstance(statement, str) or not statement.strip() or not evidence:
            continue
        key = (_normalize(statement), tuple(evidence))
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "statement": statement.strip(),
                "evidence_status": "source_explicit",
                "evidence": evidence,
                "rationale": (
                    "Deterministically propagated from accepted P1.6 responsibility "
                    f"{index}; not model-inferred."
                ),
                "confidence": _confidence(responsibility.get("confidence")),
            }
        )
    return items


def _build_source_truth(
    *,
    accepted_extraction: dict[str, Any],
    capabilities: list[dict[str, Any]],
) -> dict[str, Any]:
    requirements = accepted_extraction.get("requirements") or []
    responsibilities = accepted_extraction.get("responsibilities") or []
    role_purpose = accepted_extraction.get("role_purpose") or []
    if not isinstance(requirements, list):
        raise ValueError("accepted_extraction.requirements must be a list")
    if not isinstance(responsibilities, list):
        raise ValueError("accepted_extraction.responsibilities must be a list")
    if not isinstance(role_purpose, list):
        raise ValueError("accepted_extraction.role_purpose must be a list")

    capability_indices, role_level_indices = partition_source_requirements(accepted_extraction)
    linked_requirements = sorted(
        {
            index
            for profile in capabilities
            for index in profile.get("source_requirement_indices") or []
        }
    )
    linked_responsibilities = sorted(
        {
            index
            for profile in capabilities
            for index in profile.get("source_responsibility_indices") or []
        }
    )
    depth_indices = [
        index
        for index, item in enumerate(requirements)
        if isinstance(item, dict)
        and isinstance(item.get("depth_signal"), str)
        and item["depth_signal"].strip()
    ]

    purpose_facts = [
        {
            "index": index,
            "statement": item["statement"].strip(),
            "evidence": _evidence_values(item),
            "confidence": _confidence(item.get("confidence")),
        }
        for index, item in enumerate(role_purpose)
        if isinstance(item, dict)
        and isinstance(item.get("statement"), str)
        and item["statement"].strip()
    ]

    requirement_facts = [
        {
            "index": index,
            "concept": item["concept"].strip(),
            "concept_type": str(item.get("concept_type") or "unknown"),
            "requirement_type": item["requirement_type"],
            "depth_signal": (
                item["depth_signal"].strip()
                if isinstance(item.get("depth_signal"), str)
                and item["depth_signal"].strip()
                else None
            ),
            "evidence": _evidence_values(item),
            "confidence": _confidence(item.get("confidence")),
        }
        for index, item in enumerate(requirements)
        if isinstance(item, dict)
        and isinstance(item.get("concept"), str)
        and item["concept"].strip()
        and item.get("requirement_type") in _P1_REQUIREMENT_STRENGTHS
    ]

    responsibility_facts = [
        {
            "index": index,
            "statement": item["statement"].strip(),
            "evidence": _evidence_values(item),
            "confidence": _confidence(item.get("confidence")),
        }
        for index, item in enumerate(responsibilities)
        if isinstance(item, dict)
        and isinstance(item.get("statement"), str)
        and item["statement"].strip()
    ]

    linked_depth = sorted(set(depth_indices) & set(linked_requirements))
    return {
        "role_purpose": purpose_facts,
        "requirements": requirement_facts,
        "responsibilities": responsibility_facts,
        "capability_requirement_indices": capability_indices,
        "role_level_requirement_indices": role_level_indices,
        "linked_requirement_indices": linked_requirements,
        "unlinked_capability_requirement_indices": sorted(
            set(capability_indices) - set(linked_requirements)
        ),
        "linked_responsibility_indices": linked_responsibilities,
        "unlinked_responsibility_indices": sorted(
            set(range(len(responsibilities))) - set(linked_responsibilities)
        ),
        "explicit_depth_requirement_indices": depth_indices,
        "linked_explicit_depth_requirement_indices": linked_depth,
        "unlinked_explicit_depth_requirement_indices": sorted(
            set(depth_indices) - set(linked_requirements)
        ),
    }


def reconcile_capability_intelligence(
    intelligence: CapabilityReasoningDraft | JobCapabilityIntelligence,
    *,
    accepted_extraction: dict[str, Any],
    analysis_fields: dict[str, Any],
    evidence_catalog: dict[str, str] | None = None,
) -> JobCapabilityIntelligence:
    """Reconcile the v7 model draft with complete accepted P1.6 source truth."""

    requirements = accepted_extraction.get("requirements") or []
    responsibilities = accepted_extraction.get("responsibilities") or []
    if not isinstance(requirements, list):
        raise ValueError("accepted_extraction.requirements must be a list")
    if not isinstance(responsibilities, list):
        raise ValueError("accepted_extraction.responsibilities must be a list")

    payload = intelligence.model_dump(mode="json")
    payload.pop("source_truth", None)

    for profile in payload.get("capabilities") or []:
        requirement_indices = profile.get("source_requirement_indices") or []
        responsibility_indices = profile.get("source_responsibility_indices") or []

        profile["requirement_strength"] = _deterministic_requirement_strength(
            requirement_indices,
            requirements,
        )
        profile["depth_signals"] = [
            *_deterministic_depth_expectations(requirement_indices, requirements),
            *[
                item
                for item in profile.get("depth_signals") or []
                if item.get("evidence_status") in _DERIVED_STATUSES
            ],
        ]
        profile["work_activities"] = [
            *_deterministic_work_activities(responsibility_indices, responsibilities),
            *[
                item
                for item in profile.get("work_activities") or []
                if item.get("evidence_status") in _DERIVED_STATUSES
            ],
        ]

        for field_name in _MODEL_DERIVED_SECTION_NAMES:
            profile[field_name] = [
                item
                for item in profile.get(field_name) or []
                if item.get("evidence_status") in _DERIVED_STATUSES
            ]

        if profile.get("independence_expectation") is not None:
            unknown_scope = list(profile.get("unknown_scope") or [])
            unknown_scope.append(
                {
                    "statement": (
                        "Exact independence / ownership scope is not established by accepted "
                        "P1.6 evidence."
                    ),
                    "evidence_status": "unknown_or_unsupported",
                    "evidence": [],
                    "rationale": (
                        "Capability v7 deliberately does not convert collaboration, build, "
                        "pipeline, production, or MLOps language into autonomy or ownership."
                    ),
                    "confidence": "high",
                }
            )
            profile["unknown_scope"] = unknown_scope
        profile["independence_expectation"] = None

    # Two consecutive live Capability reviews showed that this model family uses this surface to
    # synthesize unsupported lifecycle ownership. Keep v7 focused on per-capability reasoning.
    payload["cross_capability_observations"] = []
    payload["source_truth"] = _build_source_truth(
        accepted_extraction=accepted_extraction,
        capabilities=payload.get("capabilities") or [],
    )

    return JobCapabilityIntelligence.model_validate(
        payload,
        context={
            "analysis_fields": analysis_fields,
            "evidence_catalog": evidence_catalog or {},
            "accepted_extraction": accepted_extraction,
        },
    )


__all__ = [
    "CapabilityExpectation",
    "CapabilityProfile",
    "CapabilityReasoningDraft",
    "CapabilitySourceTruth",
    "CrossCapabilityObservation",
    "JobCapabilityIntelligence",
    "partition_source_requirements",
    "reconcile_capability_intelligence",
]
