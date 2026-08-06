import pytest
from pydantic import ValidationError

from jobhunter.inference.instructor_lm_studio import JobAnalysisResponse


def _fields() -> dict:
    return {
        "title": "Infrastructure Security Specialist",
        "minimum_experience": "three to six years",
        "education": "Bachelor's degree",
        "description": (
            "Key Responsibilities:\n"
            "Investigating vulnerabilities and configuration weaknesses and providing "
            "corrective suggestions\n"
            "Specialized Competencies:\n"
            "Mastery of PowerShell for information gathering, auditing, and security reporting\n"
            "Familiarity with security logs, SIEM, and EDR for evidence analysis"
        ),
    }


def _requirement(concept: str, evidence: str) -> dict:
    return {
        "concept": concept,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Explicitly stated competency.",
    }


def test_analysis_validation_requires_all_root_arrays() -> None:
    with pytest.raises(ValidationError, match="responsibilities"):
        JobAnalysisResponse.model_validate(
            {"role_purpose": [], "requirements": []},
            context={"analysis_fields": _fields()},
        )


def test_analysis_validation_canonicalizes_safe_field_prefixes_and_exact_duplicates() -> None:
    power_shell = _requirement(
        "Mastery of PowerShell for information gathering, auditing, and security reporting",
        "Mastery of PowerShell for information gathering, auditing, and security reporting",
    )
    payload = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Investigate vulnerabilities and configuration weaknesses",
                "evidence": (
                    "Investigating vulnerabilities and configuration weaknesses and providing "
                    "corrective suggestions"
                ),
                "confidence": "high",
            }
        ],
        "requirements": [
            {
                "concept": "Minimum Experience",
                "requirement_type": "required",
                "concept_type": "experience",
                "evidence": "minimum_experience: three to six years",
                "confidence": "high",
                "rationale": "Explicit field.",
            },
            {
                "concept": "Education",
                "requirement_type": "required",
                "concept_type": "education",
                "evidence": "education: Bachelor's degree",
                "confidence": "high",
                "rationale": "Explicit field.",
            },
            power_shell,
            dict(power_shell),
        ],
    }

    result = JobAnalysisResponse.model_validate(
        payload,
        context={"analysis_fields": _fields()},
    )

    assert result.requirements[0].evidence == "three to six years"
    assert result.requirements[1].evidence == "Bachelor's degree"
    assert len(result.requirements) == 3


def test_analysis_validation_returns_exact_source_span_for_zwnj_spacing_difference() -> None:
    source = "تهیه چک‌لیست‌ها، مستندات فنی و گزارش‌های امنیتی"
    generated = "تهیه چک لیست ها، مستندات فنی و گزارش های امنیتی"
    payload = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "تهیه مستندات امنیتی",
                "evidence": generated,
                "confidence": "high",
            }
        ],
        "requirements": [],
    }

    result = JobAnalysisResponse.model_validate(
        payload,
        context={"analysis_fields": {"description": source}},
    )

    assert result.responsibilities[0].evidence == source


def test_analysis_validation_rejects_unprovable_field_prefix_or_paraphrase() -> None:
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Python", "education: Python experience"),
        ],
    }

    with pytest.raises(ValidationError, match="known JobHunter evidence reference"):
        JobAnalysisResponse.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )


def test_analysis_validation_requires_rationale_for_inferred_requirement() -> None:
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                "concept": "Security investigation",
                "requirement_type": "inferred",
                "concept_type": "practice",
                "evidence": (
                    "Investigating vulnerabilities and configuration weaknesses and providing "
                    "corrective suggestions"
                ),
                "confidence": "medium",
                "rationale": "",
            }
        ],
    }

    with pytest.raises(ValidationError, match="Inferred requirements require"):
        JobAnalysisResponse.model_validate(
            payload,
            context={"analysis_fields": _fields()},
        )
