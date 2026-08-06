import json

import pytest
from pydantic import ValidationError

from jobhunter.capability_models import JobCapabilityIntelligence


def _fields() -> dict:
    return {
        "title": "Infrastructure Security Specialist",
        "minimum_experience": "three to six years",
        "description": (
            "Mastery of VPN and network infrastructure. "
            "Troubleshoot connectivity and security incidents. "
            "Maintain secure remote access for employees."
        ),
        "company_description": "We provide enterprise infrastructure security services.",
    }


def _catalog() -> dict[str, str]:
    return {
        "p1:requirements:0": "Mastery of VPN and network infrastructure",
        "p1:responsibilities:0": "Troubleshoot connectivity and security incidents",
        "field:company_description": "We provide enterprise infrastructure security services.",
    }


def _context() -> dict:
    return {"analysis_fields": _fields(), "evidence_catalog": _catalog()}


def _expectation(
    statement: str,
    status: str,
    evidence: list[str],
    rationale: str = "Supported by the listed work.",
) -> dict:
    return {
        "statement": statement,
        "evidence_status": status,
        "evidence": evidence,
        "rationale": rationale,
        "confidence": "medium",
    }


def _payload() -> dict:
    return {
        "role_interpretation": (
            "The role operates and troubleshoots secure network connectivity rather than "
            "merely recognizing VPN terminology."
        ),
        "capabilities": [
            {
                "capability_label": "Secure network connectivity and VPN operations",
                "summary": (
                    "The employee is expected to maintain and diagnose secure connectivity, "
                    "with VPN knowledge applied in operational troubleshooting."
                ),
                "requirement_strength": "required",
                "depth_signals": [
                    _expectation(
                        (
                            "The employer explicitly asks for mastery of VPN and network "
                            "infrastructure."
                        ),
                        "source_explicit",
                        ["p1:requirements:0"],
                    )
                ],
                "work_activities": [
                    _expectation(
                        "Diagnose connectivity and security incidents.",
                        "source_explicit",
                        ["p1:responsibilities:0"],
                    )
                ],
                "sub_capabilities": [
                    _expectation(
                        (
                            "Troubleshoot VPN/connectivity failures rather than only configure "
                            "static settings."
                        ),
                        "strongly_implied_by_work",
                        ["p1:requirements:0", "p1:responsibilities:0"],
                        (
                            "VPN mastery combined with incident troubleshooting implies "
                            "operational fault diagnosis."
                        ),
                    )
                ],
                "underlying_knowledge": [
                    _expectation(
                        (
                            "Use TCP/IP and routing fundamentals when reasoning about tunnel "
                            "traffic flow."
                        ),
                        "model_inferred_prerequisite",
                        ["p1:requirements:0", "p1:responsibilities:0"],
                        (
                            "Operational VPN troubleshooting normally requires understanding "
                            "how traffic is routed before, through, and after a tunnel."
                        ),
                    )
                ],
                "operational_practices": [],
                "independence_expectation": None,
                "operational_context": [
                    _expectation(
                        "Work in an enterprise infrastructure-security context.",
                        "source_explicit",
                        ["field:company_description"],
                    )
                ],
                "unknown_scope": [
                    _expectation(
                        (
                            "The exact VPN vendor and advanced HA architecture are not "
                            "supported by the posting."
                        ),
                        "unknown_or_unsupported",
                        [],
                        "No vendor, topology, or high-availability details are provided.",
                    )
                ],
                "overall_confidence": "high",
            }
        ],
        "cross_capability_observations": [],
        "uncertainties": ["Exact VPN vendor and topology are not stated."],
    }


def _historical_exact_text_payload() -> dict:
    """Materialize v2 evidence references so legacy no-catalog validation is tested honestly."""

    payload = _payload()
    catalog = _catalog()
    for profile in payload["capabilities"]:
        for section_name in (
            "depth_signals",
            "work_activities",
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
            "unknown_scope",
        ):
            for item in profile[section_name]:
                item["evidence"] = [catalog.get(value, value) for value in item["evidence"]]
        independence = profile["independence_expectation"]
        if independence is not None:
            independence["evidence"] = [
                catalog.get(value, value) for value in independence["evidence"]
            ]
    for item in payload["cross_capability_observations"]:
        item["evidence"] = [catalog.get(value, value) for value in item["evidence"]]
    return payload


def test_capability_model_resolves_evidence_references_to_exact_source_text() -> None:
    result = JobCapabilityIntelligence.model_validate(_payload(), context=_context())

    profile = result.capabilities[0]
    assert profile.depth_signals[0].evidence == ["Mastery of VPN and network infrastructure"]
    assert profile.underlying_knowledge[0].evidence == [
        "Mastery of VPN and network infrastructure",
        "Troubleshoot connectivity and security incidents",
    ]
    assert "TCP/IP" in profile.underlying_knowledge[0].statement


def test_capability_provider_schema_omits_large_string_length_constraints() -> None:
    schema = JobCapabilityIntelligence.model_json_schema()
    serialized = json.dumps(schema, sort_keys=True)

    assert '"minLength"' not in serialized
    assert '"maxLength"' not in serialized
    assert '"maxItems"' in serialized
    assert "depth_signals" in serialized
    assert "employer_stated_depth" not in serialized


def test_capability_text_bounds_remain_runtime_enforced() -> None:
    payload = _payload()
    payload["role_interpretation"] = "too short"

    with pytest.raises(ValidationError, match="at least 20 characters"):
        JobCapabilityIntelligence.model_validate(payload, context=_context())


def test_unknown_scope_status_is_normalized_by_section() -> None:
    payload = _payload()
    payload["capabilities"][0]["unknown_scope"][0]["evidence_status"] = (
        "model_inferred_prerequisite"
    )

    result = JobCapabilityIntelligence.model_validate(payload, context=_context())

    assert result.capabilities[0].unknown_scope[0].evidence_status == "unknown_or_unsupported"


def test_unknown_item_in_other_section_is_rehomed_to_unknown_scope() -> None:
    payload = _payload()
    item = _expectation(
        "Exact vendor-specific VPN implementation is unknown.",
        "unknown_or_unsupported",
        [],
    )
    payload["capabilities"][0]["sub_capabilities"].append(item)

    result = JobCapabilityIntelligence.model_validate(payload, context=_context())

    assert all(
        item.evidence_status != "unknown_or_unsupported"
        for item in result.capabilities[0].sub_capabilities
    )
    assert any(
        item.statement == "Exact vendor-specific VPN implementation is unknown."
        for item in result.capabilities[0].unknown_scope
    )


def test_exact_text_fallback_still_supports_historical_callers() -> None:
    payload = _historical_exact_text_payload()
    payload["capabilities"][0]["underlying_knowledge"][0]["evidence"] = [
        "Mastery of VPN and network infrastructure",
        "Troubleshoot connectivity and security incidents",
    ]

    result = JobCapabilityIntelligence.model_validate(
        payload,
        context={"analysis_fields": _fields()},
    )

    assert len(result.capabilities[0].underlying_knowledge[0].evidence) == 2


def test_capability_model_rejects_unknown_evidence_reference() -> None:
    payload = _payload()
    payload["capabilities"][0]["sub_capabilities"][0]["evidence"] = ["missing:reference"]

    with pytest.raises(ValidationError, match="known JobHunter evidence reference"):
        JobCapabilityIntelligence.model_validate(payload, context=_context())


def test_composite_exact_evidence_is_split_for_historical_callers() -> None:
    payload = _historical_exact_text_payload()
    payload["capabilities"][0]["underlying_knowledge"][0]["evidence"] = [
        (
            "Mastery of VPN and network infrastructure, "
            "Troubleshoot connectivity and security incidents"
        )
    ]

    result = JobCapabilityIntelligence.model_validate(
        payload,
        context={"analysis_fields": _fields()},
    )

    assert result.capabilities[0].underlying_knowledge[0].evidence == [
        "Mastery of VPN and network infrastructure",
        "Troubleshoot connectivity and security incidents",
    ]


def test_supported_expectation_requires_evidence() -> None:
    payload = _payload()
    payload["capabilities"][0]["underlying_knowledge"][0]["evidence"] = []

    with pytest.raises(ValidationError, match="require at least one evidence excerpt"):
        JobCapabilityIntelligence.model_validate(payload, context=_context())


def test_duplicate_capability_labels_are_rejected() -> None:
    payload = _payload()
    payload["capabilities"].append(dict(payload["capabilities"][0]))

    with pytest.raises(ValidationError, match="duplicate capability_label"):
        JobCapabilityIntelligence.model_validate(payload, context=_context())


def test_capability_profile_cannot_be_only_restatement_of_employer_facts() -> None:
    payload = _payload()
    profile = payload["capabilities"][0]
    profile["depth_signals"] = [
        _expectation(
            "The employer asks for mastery of VPN and network infrastructure.",
            "source_explicit",
            ["p1:requirements:0"],
        )
    ]
    profile["sub_capabilities"] = []
    profile["underlying_knowledge"] = []
    profile["operational_practices"] = []
    profile["independence_expectation"] = None
    profile["operational_context"] = []
    profile["unknown_scope"] = []

    with pytest.raises(ValidationError, match="must add derived reasoning"):
        JobCapabilityIntelligence.model_validate(payload, context=_context())
