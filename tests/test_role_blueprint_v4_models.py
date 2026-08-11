import json

import pytest
from pydantic import ValidationError

from jobhunter.role_blueprint_v4_models import (
    RoleBlueprintDraft,
    reconcile_role_blueprint_v4,
)


def _accepted_extraction() -> dict:
    return {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Build production ML services",
                "evidence": ["Build production ML services"],
                "confidence": "high",
            },
            {
                "statement": "Operate reliable data pipelines",
                "evidence": ["Operate reliable data pipelines"],
                "confidence": "high",
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
                "concept": "PyTorch or TensorFlow",
                "concept_type": "knowledge",
                "requirement_type": "contextual",
                "depth_signal": None,
                "evidence": ["PyTorch, TensorFlow"],
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
        "role_interpretation": "Production ML engineering role.",
        "capabilities": [
            {
                "capability_label": "Model implementation",
                "source_requirement_indices": [0, 1],
                "source_responsibility_indices": [0],
            },
            {
                "capability_label": "Production operations",
                "source_requirement_indices": [2],
                "source_responsibility_indices": [1],
            },
        ],
        "source_truth": {
            "role_level_requirement_indices": [3],
        },
    }


def _draft_payload() -> dict:
    return {
        "role_read": "This is a production ML engineering role.",
        "likely_role_shape": "Applied ML Engineer",
        "capability_interpretations": [
            {
                "interpretation_strength": "highly_likely",
                "likely_depth": "Strong practical model implementation and debugging.",
                "why_this_matters": "The role explicitly builds production ML services.",
                "likely_subskills": ["model validation"],
                "suggested_tools_or_examples": [
                    {
                        "name": "httpx",
                        "relationship": "possible_example",
                        "why_relevant": (
                            "One possible HTTP client for integration-heavy implementations."
                        ),
                    }
                ],
                "likely_work_products": ["Production model service"],
                "likely_failure_modes_or_operational_concerns": ["bad model inputs"],
                "probably_not_required": ["foundation-model pretraining"],
            },
            {
                "interpretation_strength": "plausible",
                "likely_depth": "Practical operation of repeatable deployment workflows.",
                "why_this_matters": "Reliable pipelines imply operational discipline.",
                "likely_subskills": ["monitoring"],
                "suggested_tools_or_examples": [],
                "likely_work_products": ["Repeatable deployment workflow"],
                "likely_failure_modes_or_operational_concerns": ["deployment drift"],
                "probably_not_required": [],
            },
        ],
        "hidden_requirements": [
            {
                "title": "Operational debugging",
                "explanation": (
                    "Production services plausibly imply debugging under failure conditions."
                ),
                "interpretation_strength": "plausible",
            }
        ],
        "professional_example_scenarios": [
            {
                "name": "Illustrative deployment flow",
                "why_useful": "Shows one coherent way the accepted work could connect.",
                "flow_steps": ["Build model", "Validate", "Deploy", "Monitor"],
                "engineering_concerns": ["rollback", "observability"],
                "interpretation_strength": "plausible",
                "assumptions": ["The source does not specify deployment topology."],
            }
        ],
        "what_probably_does_not_matter": ["Training foundation models from scratch"],
        "important_unknowns": ["Exact deployment topology is not stated."],
        "bottom_line": "Build and operate reliable applied ML systems.",
    }


def test_v4_reconciliation_attaches_complete_upstream_truth_by_position() -> None:
    draft = RoleBlueprintDraft.model_validate(_draft_payload())
    result = reconcile_role_blueprint_v4(
        draft,
        accepted_extraction=_accepted_extraction(),
        capability_intelligence=_capability_intelligence(),
    )

    assert result.source_capability_coverage == [0, 1]
    assert [area.source_capability_index for area in result.capability_areas] == [0, 1]
    assert [area.name for area in result.capability_areas] == [
        "Model implementation",
        "Production operations",
    ]
    python = result.capability_areas[0].source_requirements[0]
    assert python.requirement_index == 0
    assert python.requirement_type == "contextual"
    assert python.depth_signal == "expert"
    docker = result.capability_areas[1].source_requirements[0]
    assert docker.requirement_index == 2
    assert docker.requirement_type == "preferred"
    assert result.source_role_constraints[0].requirement_index == 3
    assert result.source_role_constraints[0].depth_signal == "three to six years"
    assert result.professional_example_scenarios[0].scenario_basis == "professional_example"
    assert result.professional_example_scenarios[0].interpretation_strength == "plausible"


def test_v4_requires_exactly_one_interpretation_per_capability() -> None:
    payload = _draft_payload()
    payload["capability_interpretations"] = payload["capability_interpretations"][:1]
    draft = RoleBlueprintDraft.model_validate(payload)

    with pytest.raises(ValueError, match="exactly one interpretation"):
        reconcile_role_blueprint_v4(
            draft,
            accepted_extraction=_accepted_extraction(),
            capability_intelligence=_capability_intelligence(),
        )


def test_v4_suggested_tool_cannot_claim_requirement_or_expert_depth() -> None:
    payload = _draft_payload()
    tool = payload["capability_interpretations"][0]["suggested_tools_or_examples"][0]
    tool["why_relevant"] = "httpx is required for this role."
    with pytest.raises(ValidationError, match="cannot be described"):
        RoleBlueprintDraft.model_validate(payload)

    payload = _draft_payload()
    tool = payload["capability_interpretations"][0]["suggested_tools_or_examples"][0]
    tool["why_relevant"] = "Expert-level httpx knowledge would matter here."
    with pytest.raises(ValidationError, match="expert/mastery"):
        RoleBlueprintDraft.model_validate(payload)


def test_v4_hidden_requirements_and_scenarios_cannot_be_highly_likely() -> None:
    payload = _draft_payload()
    payload["hidden_requirements"][0]["interpretation_strength"] = "highly_likely"
    with pytest.raises(ValidationError):
        RoleBlueprintDraft.model_validate(payload)

    payload = _draft_payload()
    payload["professional_example_scenarios"][0]["interpretation_strength"] = "highly_likely"
    with pytest.raises(ValidationError):
        RoleBlueprintDraft.model_validate(payload)


def test_model_facing_v4_schema_contains_no_upstream_index_bookkeeping() -> None:
    serialized = json.dumps(RoleBlueprintDraft.model_json_schema(), sort_keys=True)

    assert "source_capability" not in serialized
    assert "source_requirement" not in serialized
    assert "source_responsibility" not in serialized
    assert "source_role_constraints" not in serialized
    assert "scenario_basis" not in serialized
    assert "capability_interpretations" in serialized
    assert "professional_example_scenarios" in serialized
