import json

import pytest
from pydantic import ValidationError

from jobhunter.role_blueprint_models import (
    RoleCapabilityBlueprint,
    reconcile_role_blueprint,
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
                "requirement_type": "contextual",
                "depth_signal": "expert",
                "evidence": ["Python (expert)"],
            },
            {
                "concept": "PyTorch or TensorFlow",
                "requirement_type": "contextual",
                "depth_signal": None,
                "evidence": ["PyTorch, TensorFlow"],
            },
            {
                "concept": "Docker",
                "requirement_type": "preferred",
                "depth_signal": None,
                "evidence": ["Docker a plus"],
            },
            {
                "concept": "Professional experience",
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
            {"capability_label": "Model implementation"},
            {"capability_label": "Production operations"},
        ],
        "source_truth": {
            "role_level_requirement_indices": [3],
        },
    }


def _payload() -> dict:
    return {
        "role_read": "This is a production ML engineering role.",
        "likely_role_shape": "Applied ML Engineer",
        "capability_areas": [
            {
                "name": "Model implementation",
                "source_capability_indices": [0],
                "interpretation_strength": "highly_likely",
                "likely_depth": "Strong practical model implementation and debugging.",
                "why_this_matters": "The role explicitly builds production ML services.",
                "likely_subskills": ["model validation"],
                "likely_tools_or_examples": [
                    {
                        "name": "Python",
                        "relationship": "source_named",
                        "why_relevant": "Expert Python depth is explicitly stated.",
                        "source_requirement_indices": [0],
                    },
                    {
                        "name": "httpx",
                        "relationship": "possible_example",
                        "why_relevant": "A possible HTTP client when integrations are needed.",
                    },
                ],
                "likely_work_products": ["Production model service"],
                "likely_failure_modes_or_operational_concerns": ["bad model inputs"],
                "probably_not_required": ["foundation-model pretraining"],
            },
            {
                "name": "Production operations",
                "source_capability_indices": [1],
                "interpretation_strength": "highly_likely",
                "likely_depth": "Reliable operation of pipelines and deployed models.",
                "why_this_matters": "The role explicitly operates reliable data pipelines.",
                "likely_subskills": ["monitoring"],
                "likely_tools_or_examples": [
                    {
                        "name": "Docker",
                        "relationship": "source_named",
                        "why_relevant": "Docker is a source-named optional deployment tool.",
                        "source_requirement_indices": [2],
                    }
                ],
                "likely_work_products": ["Repeatable deployment workflow"],
                "likely_failure_modes_or_operational_concerns": ["deployment drift"],
                "probably_not_required": [],
            },
        ],
        "hidden_requirements": [
            {
                "title": "Operational debugging",
                "explanation": "Production services imply debugging under failure conditions.",
                "interpretation_strength": "highly_likely",
                "source_capability_indices": [1],
                "source_responsibility_indices": [1],
            }
        ],
        "likely_end_to_end_scenarios": [
            {
                "name": "Illustrative deployment flow",
                "why_likely": "A coherent example of how the work may connect.",
                "flow_steps": ["Build model", "Validate", "Deploy", "Monitor"],
                "engineering_concerns": ["rollback", "observability"],
                "interpretation_strength": "plausible",
                "scenario_basis": "professional_example",
                "source_capability_indices": [0, 1],
                "source_responsibility_indices": [0, 1],
                "assumptions": ["The posting does not specify the deployment topology."],
            }
        ],
        "what_probably_does_not_matter": ["Training foundation models from scratch"],
        "important_unknowns": ["Exact deployment topology is not stated."],
        "bottom_line": "Build and operate reliable applied ML systems.",
    }


def test_blueprint_reconciliation_preserves_source_truth_and_coverage() -> None:
    draft = RoleCapabilityBlueprint.model_validate(_payload())
    result = reconcile_role_blueprint(
        draft,
        accepted_extraction=_accepted_extraction(),
        capability_intelligence=_capability_intelligence(),
    )

    assert result.source_capability_coverage == [0, 1]
    assert result.source_role_constraints[0].requirement_index == 3
    assert result.source_role_constraints[0].depth_signal == "three to six years"
    python = result.capability_areas[0].likely_tools_or_examples[0]
    assert python.source_requirement_strength == "contextual"
    assert python.source_depth_signals == ["expert"]
    docker = result.capability_areas[1].likely_tools_or_examples[0]
    assert docker.source_requirement_strength == "preferred"


def test_blueprint_rejects_missing_capability_coverage() -> None:
    payload = _payload()
    payload["capability_areas"] = payload["capability_areas"][:1]
    draft = RoleCapabilityBlueprint.model_validate(payload)

    with pytest.raises(ValueError, match="capability coverage"):
        reconcile_role_blueprint(
            draft,
            accepted_extraction=_accepted_extraction(),
            capability_intelligence=_capability_intelligence(),
        )


def test_source_named_tool_requires_upstream_link() -> None:
    payload = _payload()
    tool = payload["capability_areas"][0]["likely_tools_or_examples"][0]
    tool["source_requirement_indices"] = []

    with pytest.raises(ValidationError, match="source_named tools"):
        RoleCapabilityBlueprint.model_validate(payload)


def test_inferred_tool_cannot_claim_source_link_or_requirement_certainty() -> None:
    payload = _payload()
    tool = payload["capability_areas"][0]["likely_tools_or_examples"][1]
    tool["source_requirement_indices"] = [0]

    with pytest.raises(ValidationError, match="cannot claim accepted P1.6 source links"):
        RoleCapabilityBlueprint.model_validate(payload)

    payload = _payload()
    tool = payload["capability_areas"][0]["likely_tools_or_examples"][1]
    tool["why_relevant"] = "httpx is necessary for this role."
    with pytest.raises(ValidationError, match="cannot be described as mandatory"):
        RoleCapabilityBlueprint.model_validate(payload)


def test_non_required_source_tool_cannot_become_required_after_reconciliation() -> None:
    payload = _payload()
    tool = payload["capability_areas"][1]["likely_tools_or_examples"][0]
    tool["why_relevant"] = "Docker is required for production deployment."
    draft = RoleCapabilityBlueprint.model_validate(payload)

    with pytest.raises(ValueError, match="non-required source-named tool"):
        reconcile_role_blueprint(
            draft,
            accepted_extraction=_accepted_extraction(),
            capability_intelligence=_capability_intelligence(),
        )


def test_framework_mastery_requires_matching_explicit_depth() -> None:
    payload = _payload()
    tool = payload["capability_areas"][0]["likely_tools_or_examples"][0]
    tool["name"] = "PyTorch"
    tool["source_requirement_indices"] = [1]
    tool["why_relevant"] = "Expert-level PyTorch is central to this role."
    draft = RoleCapabilityBlueprint.model_validate(payload)

    with pytest.raises(ValueError, match="expert/mastery depth"):
        reconcile_role_blueprint(
            draft,
            accepted_extraction=_accepted_extraction(),
            capability_intelligence=_capability_intelligence(),
        )


def test_professional_example_scenario_cannot_be_highly_likely() -> None:
    payload = _payload()
    payload["likely_end_to_end_scenarios"][0]["interpretation_strength"] = "highly_likely"

    with pytest.raises(ValidationError, match="Professional example scenarios"):
        RoleCapabilityBlueprint.model_validate(payload)


def test_highly_likely_source_workflow_cannot_have_assumptions() -> None:
    payload = _payload()
    scenario = payload["likely_end_to_end_scenarios"][0]
    scenario["scenario_basis"] = "source_stated_workflow"
    scenario["interpretation_strength"] = "highly_likely"

    with pytest.raises(ValidationError, match="unresolved assumptions"):
        RoleCapabilityBlueprint.model_validate(payload)


def test_blueprint_provider_schema_exposes_grounding_contract() -> None:
    schema = RoleCapabilityBlueprint.model_json_schema()
    serialized = json.dumps(schema, sort_keys=True)

    assert "source_capability_indices" in serialized
    assert "source_requirement_indices" in serialized
    assert "scenario_basis" in serialized
    assert "professional_example" in serialized
    assert "source_role_constraints" in serialized
