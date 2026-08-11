from jobhunter.role_blueprint_models import RoleCapabilityBlueprint, reconcile_role_blueprint


def test_role_constraint_normalizes_p1_string_evidence() -> None:
    accepted = {
        "responsibilities": [],
        "requirements": [
            {
                "concept": "Professional experience",
                "requirement_type": "required",
                "depth_signal": "three to six years",
                "evidence": "three to six years",
            }
        ],
    }
    capability = {
        "capabilities": [{"capability_label": "Applied ML"}],
        "source_truth": {"role_level_requirement_indices": [0]},
    }
    draft = RoleCapabilityBlueprint.model_validate(
        {
            "role_read": "Applied ML role.",
            "likely_role_shape": "Applied ML Engineer",
            "capability_areas": [
                {
                    "name": "Applied ML",
                    "source_capability_indices": [0],
                    "interpretation_strength": "highly_likely",
                    "likely_depth": "Practical applied ML work.",
                    "why_this_matters": "This is the accepted capability area.",
                    "likely_subskills": [],
                    "likely_tools_or_examples": [],
                    "likely_work_products": [],
                    "likely_failure_modes_or_operational_concerns": [],
                    "probably_not_required": [],
                }
            ],
            "hidden_requirements": [],
            "likely_end_to_end_scenarios": [],
            "what_probably_does_not_matter": [],
            "important_unknowns": [],
            "bottom_line": "Applied ML work.",
        }
    )

    result = reconcile_role_blueprint(
        draft,
        accepted_extraction=accepted,
        capability_intelligence=capability,
    )

    assert result.source_role_constraints[0].evidence == ["three to six years"]
