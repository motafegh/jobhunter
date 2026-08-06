from jobhunter.capability_models import JobCapabilityIntelligence


def test_grounded_claim_ignores_invalid_additional_reference() -> None:
    fields = {
        "description": (
            "Build and validate ML models. Work on SPC, DOE, anomaly detection, and yield."
        )
    }
    catalog = {"field:description": fields["description"]}
    payload = {
        "role_interpretation": (
            "The role applies industrial machine learning to manufacturing-process problems."
        ),
        "capabilities": [
            {
                "capability_label": "Industrial ML",
                "summary": (
                    "The employee must apply ML and statistical methods to industrial data."
                ),
                "requirement_strength": "required",
                "depth_signals": [],
                "work_activities": [],
                "sub_capabilities": [
                    {
                        "statement": "Apply industrial statistical methods.",
                        "evidence_status": "strongly_implied_by_work",
                        "evidence": ["field:description", "field:skills:99"],
                        "rationale": (
                            "The posting directly combines model work with SPC and DOE."
                        ),
                        "confidence": "high",
                    }
                ],
                "underlying_knowledge": [],
                "operational_practices": [],
                "independence_expectation": None,
                "operational_context": [],
                "unknown_scope": [],
                "overall_confidence": "high",
            }
        ],
        "cross_capability_observations": [],
        "uncertainties": [],
    }

    result = JobCapabilityIntelligence.model_validate(
        payload,
        context={"analysis_fields": fields, "evidence_catalog": catalog},
    )

    assert result.capabilities[0].sub_capabilities[0].evidence == [
        fields["description"]
    ]
