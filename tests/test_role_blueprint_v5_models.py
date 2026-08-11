import json

import pytest
from pydantic import ValidationError

from jobhunter.role_blueprint_v5_models import (
    RoleBlueprintDraft,
    reconcile_role_blueprint_v5,
)


def _accepted_extraction() -> dict:
    return {
        "role_purpose": [
            {
                "statement": "Build and validate ML models for manufacturing data",
                "evidence": ["Build and validate ML models for manufacturing data"],
            }
        ],
        "responsibilities": [
            {
                "statement": "Build production ML services",
                "evidence": ["Build production ML services"],
            },
            {
                "statement": "Operate reliable data pipelines",
                "evidence": ["Operate reliable data pipelines"],
            },
        ],
        "requirements": [
            {
                "concept": "Python",
                "concept_type": "skill",
                "requirement_type": "contextual",
                "depth_signal": "expert",
                "evidence": ["Python (expert)"],
            },
            {
                "concept": "Docker",
                "concept_type": "knowledge",
                "requirement_type": "preferred",
                "depth_signal": None,
                "evidence": ["Docker a plus"],
            },
            {
                "concept": "Professional experience",
                "concept_type": "experience",
                "requirement_type": "required",
                "depth_signal": "three to six years",
                "evidence": ["three to six years"],
            },
        ],
    }


def _capability_intelligence() -> dict:
    return {
        "capabilities": [
            {
                "capability_label": "Model implementation",
                "source_requirement_indices": [0],
                "source_responsibility_indices": [0],
                "summary": "Aggressive derived prose must not be needed by v5.",
            },
            {
                "capability_label": "Production operations",
                "source_requirement_indices": [1],
                "source_responsibility_indices": [1],
                "summary": "Another derived summary that v5 does not need.",
            },
        ],
        "source_truth": {"role_level_requirement_indices": [2]},
    }


def _draft_payload() -> dict:
    return {
        "capability_interpretations": [
            {
                "practical_interpretation": (
                    "This area is centered on implementing and validating applied ML behavior."
                ),
                "professional_considerations": [
                    {
                        "statement": "Input validation may become operationally important.",
                        "interpretation_strength": "plausible",
                        "uncertainty": "The vacancy does not specify serving boundaries.",
                    }
                ],
                "probably_not_required": ["Foundation-model pretraining is probably not central."],
                "important_unknowns": ["The serving topology is not stated."],
            },
            {
                "practical_interpretation": (
                    "This area connects model work with repeatable production operation."
                ),
                "professional_considerations": [],
                "probably_not_required": [],
                "important_unknowns": ["The deployment platform is not stated."],
            },
        ],
        "overall_unknowns": ["The vacancy does not establish latency requirements."],
    }


def test_v5_reconciliation_keeps_source_truth_separate_from_inference() -> None:
    draft = RoleBlueprintDraft.model_validate(_draft_payload())
    result = reconcile_role_blueprint_v5(
        draft,
        accepted_extraction=_accepted_extraction(),
        capability_intelligence=_capability_intelligence(),
    )

    assert result.source_capability_coverage == [0, 1]
    assert result.source_role_purpose[0].statement.startswith("Build and validate")
    assert result.source_role_constraints[0].requirement_index == 2
    assert result.source_role_constraints[0].depth_signal == "three to six years"
    assert result.capability_areas[0].source_requirements[0].requirement_index == 0
    assert result.capability_areas[0].source_requirements[0].depth_signal == "expert"
    assert result.capability_areas[1].source_requirements[0].requirement_type == "preferred"
    assert result.capability_areas[0].interpretation_strength == "plausible"


def test_v5_requires_one_interpretation_per_accepted_capability() -> None:
    payload = _draft_payload()
    payload["capability_interpretations"] = payload["capability_interpretations"][:1]
    draft = RoleBlueprintDraft.model_validate(payload)

    with pytest.raises(ValueError, match="exactly one interpretation"):
        reconcile_role_blueprint_v5(
            draft,
            accepted_extraction=_accepted_extraction(),
            capability_intelligence=_capability_intelligence(),
        )


def test_v5_rejects_obligation_and_full_lifecycle_ownership_language() -> None:
    payload = _draft_payload()
    payload["capability_interpretations"][0]["practical_interpretation"] = (
        "The practitioner must own the entire lifecycle."
    )
    with pytest.raises(ValidationError, match="cannot claim employer obligation"):
        RoleBlueprintDraft.model_validate(payload)

    payload = _draft_payload()
    consideration = payload["capability_interpretations"][0]["professional_considerations"][0]
    consideration["statement"] = "The engineer is expected to run real-time control loops."
    with pytest.raises(ValidationError, match="cannot claim employer obligation"):
        RoleBlueprintDraft.model_validate(payload)


def test_v5_allows_cautious_negative_scope_language() -> None:
    payload = _draft_payload()
    payload["capability_interpretations"][0]["probably_not_required"] = [
        "Building foundation models is probably not required."
    ]
    RoleBlueprintDraft.model_validate(payload)


def test_model_facing_v5_schema_has_no_legacy_blueprint_expansion_fields() -> None:
    serialized = json.dumps(RoleBlueprintDraft.model_json_schema(), sort_keys=True)

    for forbidden in (
        "source_capability",
        "source_requirement",
        "source_responsibility",
        "likely_role_shape",
        "likely_depth",
        "suggested_tools_or_examples",
        "hidden_requirements",
        "professional_example_scenarios",
        "bottom_line",
    ):
        assert forbidden not in serialized
    assert "professional_considerations" in serialized
    assert "uncertainty" in serialized
