import pytest
from pydantic import ValidationError

from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft,
    partition_source_requirements,
    reconcile_capability_intelligence,
)


def _expectation(statement: str, status: str, evidence: list[str]) -> dict:
    return {
        "statement": statement,
        "evidence_status": status,
        "evidence": evidence,
        "rationale": "Supported by accepted P1.6 evidence.",
        "confidence": "high",
    }


def _requirements(count: int = 12) -> list[dict]:
    items = []
    for index in range(count):
        items.append(
            {
                "concept": f"Capability requirement {index}",
                "concept_type": "knowledge",
                "requirement_type": "required" if index < 2 else "contextual",
                "depth_signal": "Expert" if index == 0 else None,
                "evidence": f"Requirement evidence {index}",
                "confidence": "high",
                "rationale": "Accepted fact.",
            }
        )
    items[-2] = {
        "concept": "Master's degree",
        "concept_type": "education",
        "requirement_type": "required",
        "depth_signal": None,
        "evidence": "Master's degree",
        "confidence": "high",
        "rationale": "Accepted fact.",
    }
    items[-1] = {
        "concept": "Professional experience",
        "concept_type": "experience",
        "requirement_type": "required",
        "depth_signal": "three to six years",
        "evidence": "three to six years",
        "confidence": "high",
        "rationale": "Accepted fact.",
    }
    return items


def _extraction(*, requirement_count: int = 12, responsibility_count: int = 5) -> dict:
    return {
        "role_purpose": [
            {
                "statement": "Operate and improve the supported technical system.",
                "evidence": "Operate and improve the supported technical system.",
                "confidence": "high",
            }
        ],
        "requirements": _requirements(requirement_count),
        "responsibilities": [
            {
                "statement": f"Responsibility {index} for supported operations",
                "evidence": f"Responsibility evidence {index}",
                "confidence": "high",
            }
            for index in range(responsibility_count)
        ],
    }


def _fields(extraction: dict) -> dict:
    return {
        "description": " ".join(
            [
                *(item["evidence"] for item in extraction["requirements"]),
                *(item["evidence"] for item in extraction["responsibilities"]),
                *(item["evidence"] for item in extraction["role_purpose"]),
            ]
        )
    }


def _catalog(extraction: dict) -> dict[str, str]:
    catalog = {}
    for index, item in enumerate(extraction["requirements"]):
        catalog[f"p1:requirements:{index}"] = item["evidence"]
    for index, item in enumerate(extraction["responsibilities"]):
        catalog[f"p1:responsibilities:{index}"] = item["evidence"]
    return catalog


def _profile(
    *,
    label: str,
    requirement_indices: list[int],
    responsibility_indices: list[int],
    derived: bool = True,
) -> dict:
    evidence = (
        [f"p1:requirements:{requirement_indices[0]}"]
        if requirement_indices
        else [f"p1:responsibilities:{responsibility_indices[0]}"]
    )
    return {
        "capability_label": label,
        "summary": "A coherent capability grouping backed by accepted P1.6 facts.",
        "source_requirement_indices": requirement_indices,
        "source_responsibility_indices": responsibility_indices,
        "requirement_strength": "unspecified",
        "depth_signals": [],
        "work_activities": [],
        "sub_capabilities": (
            [
                _expectation(
                    "Apply the linked facts together during supported technical work.",
                    "strongly_implied_by_work",
                    evidence,
                )
            ]
            if derived
            else []
        ),
        "underlying_knowledge": [],
        "operational_practices": [],
        "independence_expectation": None,
        "operational_context": [],
        "unknown_scope": (
            []
            if derived
            else [
                _expectation(
                    "Narrower implementation detail is not established.",
                    "unknown_or_unsupported",
                    [],
                )
            ]
        ),
        "overall_confidence": "high",
    }


def _payload(extraction: dict) -> dict:
    capability_indices, _ = partition_source_requirements(extraction)
    split = max(1, len(capability_indices) // 2)
    responsibilities = list(range(len(extraction["responsibilities"])))
    rsplit = max(1, len(responsibilities) // 2)
    return {
        "role_interpretation": (
            "The role combines several evidence-backed technical capability areas and "
            "operational responsibilities."
        ),
        "capabilities": [
            _profile(
                label="Capability area A",
                requirement_indices=capability_indices[:split],
                responsibility_indices=responsibilities[:rsplit],
            ),
            _profile(
                label="Capability area B",
                requirement_indices=capability_indices[split:],
                responsibility_indices=responsibilities[rsplit:],
            ),
        ],
        "cross_capability_observations": [],
        "uncertainties": [],
    }


def _context(extraction: dict) -> dict:
    return {
        "analysis_fields": _fields(extraction),
        "evidence_catalog": _catalog(extraction),
        "accepted_extraction": extraction,
    }


def test_partition_keeps_education_and_standalone_duration_role_level() -> None:
    extraction = _extraction()
    capability, role_level = partition_source_requirements(extraction)

    assert role_level == [10, 11]
    assert capability == list(range(10))


def test_draft_rejects_missing_capability_requirement_coverage() -> None:
    extraction = _extraction()
    payload = _payload(extraction)
    payload["capabilities"][1]["source_requirement_indices"].pop()

    with pytest.raises(ValidationError, match="omitted capability-relevant"):
        CapabilityReasoningDraft.model_validate(payload, context=_context(extraction))


def test_draft_rejects_missing_responsibility_coverage() -> None:
    extraction = _extraction()
    payload = _payload(extraction)
    payload["capabilities"][1]["source_responsibility_indices"].pop()

    with pytest.raises(ValidationError, match="omitted accepted P1.6 responsibilities"):
        CapabilityReasoningDraft.model_validate(payload, context=_context(extraction))


def test_dense_source_rejects_one_catch_all_profile() -> None:
    extraction = _extraction()
    capability, _ = partition_source_requirements(extraction)
    payload = {
        "role_interpretation": "A long enough interpretation for the dense source fixture.",
        "capabilities": [
            _profile(
                label="Everything",
                requirement_indices=capability,
                responsibility_indices=list(range(5)),
            )
        ],
        "cross_capability_observations": [],
        "uncertainties": [],
    }

    with pytest.raises(ValidationError, match="at least two coherent capability profiles"):
        CapabilityReasoningDraft.model_validate(payload, context=_context(extraction))


def test_reconciliation_owns_source_truth_depth_work_and_strength() -> None:
    extraction = _extraction()
    context = _context(extraction)
    draft = CapabilityReasoningDraft.model_validate(_payload(extraction), context=context)

    result = reconcile_capability_intelligence(
        draft,
        accepted_extraction=extraction,
        analysis_fields=context["analysis_fields"],
        evidence_catalog=context["evidence_catalog"],
    )

    truth = result.source_truth
    assert truth is not None
    assert truth.role_level_requirement_indices == [10, 11]
    assert truth.capability_requirement_indices == list(range(10))
    assert truth.unlinked_capability_requirement_indices == []
    assert truth.unlinked_responsibility_indices == []
    assert truth.explicit_depth_requirement_indices == [0, 11]
    assert truth.linked_explicit_depth_requirement_indices == [0]
    assert truth.unlinked_explicit_depth_requirement_indices == [11]
    assert len(truth.requirements) == 12
    assert len(truth.responsibilities) == 5

    first = result.capabilities[0]
    assert first.requirement_strength in {"required", "mixed"}
    assert any(
        item.evidence_status == "source_explicit"
        and "employer-stated depth: Expert" in item.statement
        for item in first.depth_signals
    )
    expected_work = {
        extraction["responsibilities"][index]["statement"]
        for index in first.source_responsibility_indices
    }
    actual_work = {
        item.statement
        for item in first.work_activities
        if item.evidence_status == "source_explicit"
    }
    assert actual_work == expected_work


def test_reconciliation_defers_autonomy_cross_synthesis_and_model_source_explicit_items() -> None:
    extraction = _extraction()
    payload = _payload(extraction)
    profile = payload["capabilities"][0]
    profile["independence_expectation"] = _expectation(
        "Own the full lifecycle autonomously.",
        "model_inferred_prerequisite",
        ["p1:responsibilities:0"],
    )
    profile["operational_context"] = [
        _expectation(
            "Model repeated a source-explicit context.",
            "source_explicit",
            ["p1:requirements:0"],
        )
    ]
    payload["cross_capability_observations"] = [
        {
            "statement": "The two capability areas imply end-to-end ownership.",
            "evidence_status": "model_inferred_prerequisite",
            "evidence": ["p1:responsibilities:0"],
            "rationale": "Model inference that v7 deliberately defers.",
            "confidence": "high",
        }
    ]
    context = _context(extraction)
    draft = CapabilityReasoningDraft.model_validate(payload, context=context)

    result = reconcile_capability_intelligence(
        draft,
        accepted_extraction=extraction,
        analysis_fields=context["analysis_fields"],
        evidence_catalog=context["evidence_catalog"],
    )

    first = result.capabilities[0]
    assert first.independence_expectation is None
    assert any("independence / ownership" in item.statement for item in first.unknown_scope)
    assert first.operational_context == []
    assert result.cross_capability_observations == []
