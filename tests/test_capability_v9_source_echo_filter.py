from jobhunter.capability_v9_models import CapabilityProfileReasoningV9


def test_v9_filters_source_explicit_echoes_from_model_owned_profile_reasoning() -> None:
    context = {
        "analysis_fields": {
            "description": (
                "Hands-on with process control. Solid statistics fundamentals. "
                "Turn manufacturing problems into well-scoped modeling problems."
            )
        },
        "evidence_catalog": {
            "p1:requirements:1": "Hands-on with process control.",
            "p1:requirements:3": "Solid statistics fundamentals.",
            "p1:responsibilities:4": (
                "Turn manufacturing problems into well-scoped modeling problems."
            ),
        },
        "assigned_requirements": [
            {
                "index": 1,
                "concept": "Process control",
                "concept_type": "experience",
                "requirement_type": "required",
                "depth_signal": "hands-on",
                "evidence": ["Hands-on with process control."],
                "confidence": "high",
            },
            {
                "index": 3,
                "concept": "Statistics fundamentals",
                "concept_type": "knowledge",
                "requirement_type": "required",
                "depth_signal": "solid",
                "evidence": ["Solid statistics fundamentals."],
                "confidence": "high",
            },
        ],
        "assigned_responsibilities": [
            {
                "index": 4,
                "statement": "Turn manufacturing problems into well-scoped modeling problems.",
                "evidence": [
                    "Turn manufacturing problems into well-scoped modeling problems."
                ],
            }
        ],
        "group_summary": "This capability area covers industrial analytics and process control.",
    }
    payload = {
        "summary": "This capability area covers industrial analytics and process control.",
        "overall_confidence": "high",
        "depth_signals": [
            {
                "statement": "Hands-on experience is required in process control.",
                "evidence_status": "source_explicit",
                "evidence": ["p1:requirements:1"],
                "rationale": "The requirement explicitly signals hands-on application.",
                "confidence": "high",
            },
            {
                "statement": "Solid statistics fundamentals are required.",
                "evidence_status": "source_explicit",
                "evidence": ["p1:requirements:3"],
                "rationale": "The requirement explicitly signals solid fundamentals.",
                "confidence": "high",
            },
        ],
        "work_activities": [],
        "sub_capabilities": [],
        "underlying_knowledge": [],
        "operational_practices": [],
        "operational_context": [
            {
                "statement": "The work includes translating manufacturing problems for modeling.",
                "evidence_status": "source_explicit",
                "evidence": ["p1:responsibilities:4"],
                "rationale": "This responsibility is explicit in the accepted source facts.",
                "confidence": "high",
            }
        ],
        "unknown_scope": [],
        "uncertainties": [],
    }

    profile = CapabilityProfileReasoningV9.model_validate(payload, context=context)

    assert profile.depth_signals == []
    assert profile.operational_context == []
    assert any(
        "discarded 3 redundant or misplaced model expectation" in item
        for item in profile.uncertainties
    )
