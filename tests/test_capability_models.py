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
                "employer_stated_depth": [
                    _expectation(
                        (
                            "The employer explicitly asks for mastery of VPN and network "
                            "infrastructure."
                        ),
                        "source_explicit",
                        ["Mastery of VPN and network infrastructure"],
                    )
                ],
                "work_activities": [
                    _expectation(
                        "Diagnose connectivity and security incidents.",
                        "source_explicit",
                        ["Troubleshoot connectivity and security incidents"],
                    )
                ],
                "sub_capabilities": [
                    _expectation(
                        (
                            "Troubleshoot VPN/connectivity failures rather than only configure "
                            "static settings."
                        ),
                        "strongly_implied_by_work",
                        [
                            "Mastery of VPN and network infrastructure",
                            "Troubleshoot connectivity and security incidents",
                        ],
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
                        [
                            "Mastery of VPN and network infrastructure",
                            "Troubleshoot connectivity and security incidents",
                        ],
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
                        ["enterprise infrastructure security services"],
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


def test_capability_model_allows_synthesized_analysis_with_exact_evidence() -> None:
    result = JobCapabilityIntelligence.model_validate(
        _payload(),
        context={"analysis_fields": _fields()},
    )

    profile = result.capabilities[0]
    assert "TCP/IP" in profile.underlying_knowledge[0].statement
    assert profile.underlying_knowledge[0].statement not in _fields()["description"]
    assert profile.underlying_knowledge[0].evidence_status == "model_inferred_prerequisite"


def test_capability_provider_schema_omits_large_string_length_constraints() -> None:
    schema = JobCapabilityIntelligence.model_json_schema()
    serialized = json.dumps(schema, sort_keys=True)

    # LM Studio turns JSON Schema string length bounds into llama.cpp grammar repetitions.
    # Large values such as {3,1200}/{20,2400} exceeded the engine's sane repetition limit.
    assert '"minLength"' not in serialized
    assert '"maxLength"' not in serialized
    # Structural collection bounds remain provider-visible; only prose bounds moved to runtime.
    assert '"maxItems"' in serialized


def test_capability_text_bounds_remain_runtime_enforced() -> None:
    payload = _payload()
    payload["role_interpretation"] = "too short"

    with pytest.raises(ValidationError, match="at least 20 characters"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_capability_model_rejects_paraphrased_evidence_but_not_synthesized_statement() -> None:
    payload = _payload()
    payload["capabilities"][0]["sub_capabilities"][0]["evidence"] = [
        "The person must troubleshoot VPN problems"
    ]

    with pytest.raises(ValidationError, match="Evidence must be an exact excerpt"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_composite_evidence_is_split_into_exact_source_excerpts() -> None:
    payload = _payload()
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


def test_composite_evidence_rejects_any_unproven_fragment() -> None:
    payload = _payload()
    payload["capabilities"][0]["underlying_knowledge"][0]["evidence"] = [
        (
            "Mastery of VPN and network infrastructure, invented unsupported phrase, "
            "Troubleshoot connectivity and security incidents"
        )
    ]

    with pytest.raises(ValidationError, match="Evidence must be an exact excerpt"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_supported_expectation_requires_evidence() -> None:
    payload = _payload()
    payload["capabilities"][0]["underlying_knowledge"][0]["evidence"] = []

    with pytest.raises(ValidationError, match="require at least one evidence excerpt"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_unknown_scope_must_be_labeled_unknown() -> None:
    payload = _payload()
    unknown = payload["capabilities"][0]["unknown_scope"][0]
    unknown["evidence_status"] = "model_inferred_prerequisite"
    unknown["evidence"] = ["Mastery of VPN and network infrastructure"]

    with pytest.raises(ValidationError, match="unknown_scope items"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_employer_stated_depth_must_be_source_explicit() -> None:
    payload = _payload()
    depth = payload["capabilities"][0]["employer_stated_depth"][0]
    depth["evidence_status"] = "strongly_implied_by_work"

    with pytest.raises(ValidationError, match="employer_stated_depth items"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_duplicate_capability_labels_are_rejected() -> None:
    payload = _payload()
    payload["capabilities"].append(dict(payload["capabilities"][0]))

    with pytest.raises(ValidationError, match="duplicate capability_label"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_capability_profile_cannot_be_only_restatement_of_employer_facts() -> None:
    payload = _payload()
    profile = payload["capabilities"][0]
    profile["sub_capabilities"] = []
    profile["underlying_knowledge"] = []
    profile["operational_practices"] = []
    profile["independence_expectation"] = None
    profile["operational_context"] = []
    profile["unknown_scope"] = []

    with pytest.raises(ValidationError, match="must add derived reasoning"):
        JobCapabilityIntelligence.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )
