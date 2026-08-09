import pytest
from pydantic import ValidationError

from jobhunter.evidence_refs import (
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
)
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
        "depth_signal": None,
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
                    "depth_signal": "three to six years",
                    "requirement_type": "required",
                "concept_type": "experience",
                "evidence": "minimum_experience: three to six years",
                "confidence": "high",
                "rationale": "Explicit field.",
            },
                {
                    "concept": "Education",
                    "depth_signal": None,
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
                    "depth_signal": None,
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


def test_english_requirement_rejects_mixed_core_and_optional_evidence() -> None:
    evidence = "Programming: Python (expert) and SQL; MATLAB a plus; some C / C++ helpful"
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [_requirement("Programming proficiency", evidence)],
    }

    with pytest.raises(ValidationError, match="mixed-strength evidence"):
        JobAnalysisResponse.model_validate(
            payload,
            context={
                "analysis_fields": {"description": evidence},
                "analysis_mode": "english",
            },
        )


def test_english_preferred_requires_explicit_optionality_evidence() -> None:
    evidence = "Fab data systems: MES, SECS / GEM, and equipment / metrology / trace data"
    requirement = _requirement("Fab data systems", evidence)
    requirement["requirement_type"] = "preferred"
    payload = {"role_purpose": [], "responsibilities": [], "requirements": [requirement]}

    with pytest.raises(ValidationError, match="preferred requirements require explicit"):
        JobAnalysisResponse.model_validate(
            payload,
            context={
                "analysis_fields": {"description": evidence},
                "analysis_mode": "english",
            },
        )


def test_english_preferred_accepts_explicit_plus_wording() -> None:
    evidence = "MATLAB a plus"
    requirement = _requirement("MATLAB", evidence)
    requirement["requirement_type"] = "preferred"
    payload = {"role_purpose": [], "responsibilities": [], "requirements": [requirement]}

    result = JobAnalysisResponse.model_validate(
        payload,
        context={
            "analysis_fields": {"description": evidence},
            "analysis_mode": "english",
        },
    )

    assert result.requirements[0].requirement_type == "preferred"


def test_analysis_rejects_depth_wording_absent_from_cited_evidence() -> None:
    evidence = "ML & deep learning: scikit-learn, PyTorch, TensorFlow"
    requirement = _requirement("Expert proficiency in ML frameworks", evidence)
    payload = {"role_purpose": [], "responsibilities": [], "requirements": [requirement]}

    with pytest.raises(ValidationError, match="concept contains expert depth wording"):
        JobAnalysisResponse.model_validate(
            payload,
            context={
                "analysis_fields": {"description": evidence},
                "analysis_mode": "english",
            },
        )


def test_english_requirement_preserves_scoped_depth_separately_from_concept() -> None:
    evidence = "Programming: Python (expert) and SQL"
    requirement = _requirement("Programming with Python and SQL", evidence)
    requirement["depth_signal"] = "Python (expert)"

    result = JobAnalysisResponse.model_validate(
        {"role_purpose": [], "responsibilities": [], "requirements": [requirement]},
        context={
            "analysis_fields": {"description": evidence},
            "analysis_mode": "english",
        },
    )

    assert result.requirements[0].concept == "Programming with Python and SQL"
    assert result.requirements[0].depth_signal == "expert"


def test_english_requirement_recovers_explicit_depth_from_atomic_evidence() -> None:
    evidence = "Strong experience applying AI/ML to manufacturing data"
    requirement = _requirement(
        "Experience applying AI/ML to manufacturing data", evidence
    )

    result = JobAnalysisResponse.model_validate(
        {"role_purpose": [], "responsibilities": [], "requirements": [requirement]},
        context={
            "analysis_fields": {"description": evidence},
            "analysis_mode": "english",
        },
    )

    assert result.requirements[0].depth_signal == "Strong"


def test_english_requirement_rejects_depth_signal_outside_cited_evidence() -> None:
    evidence = "ML & deep learning: scikit-learn, PyTorch, TensorFlow"
    requirement = _requirement("ML and deep-learning frameworks", evidence)
    requirement["depth_signal"] = "expert"

    with pytest.raises(ValidationError, match="exact contiguous excerpt"):
        JobAnalysisResponse.model_validate(
            {"role_purpose": [], "responsibilities": [], "requirements": [requirement]},
            context={
                "analysis_fields": {"description": evidence},
                "analysis_mode": "english",
            },
        )


def test_requirement_coverage_rejects_a_missing_structured_field_decision() -> None:
    fields = _fields()
    plan = build_requirement_coverage_plan(fields)
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                **_requirement("Relevant experience", "three to six years"),
                "depth_signal": "three to six years",
                "concept_type": "experience",
            },
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(ValidationError, match="must be cited by a requirement"):
        JobAnalysisResponse.model_validate(
            payload,
            context={
                "analysis_fields": fields,
                "analysis_mode": "english",
                "requirement_coverage_plan": plan,
            },
        )


def test_requirement_coverage_enforces_contextual_and_preferred_obligation() -> None:
    fields = {
        "description": (
            "Technical skill stack We don't expect every single item. "
            "● Programming: Python (expert) and SQL; MATLAB a plus"
        )
    }
    plan = build_requirement_coverage_plan(fields)
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                **_requirement("Python", "Python (expert)"),
                "depth_signal": "Python (expert)",
                "requirement_type": "contextual",
            },
            {
                **_requirement("SQL", "SQL"),
                "requirement_type": "contextual",
            },
            {
                **_requirement("MATLAB", "MATLAB a plus"),
                "requirement_type": "preferred",
                "concept_type": "tool",
            },
        ],
        "coverage_exclusions": [],
    }

    result = JobAnalysisResponse.model_validate(
        payload,
        context={
            "analysis_fields": fields,
            "analysis_mode": "english",
            "requirement_coverage_plan": plan,
        },
    )

    assert [item.requirement_type for item in result.requirements] == [
        "contextual",
        "contextual",
        "preferred",
    ]


def test_responsibility_coverage_rejects_an_omitted_explicit_duty() -> None:
    fields = {
        "description": (
            "What you'll do ● Build models. ● Monitor models. "
            "What we're looking for ● Python"
        )
    }
    plan = build_responsibility_coverage_plan(fields)
    payload = {
        "role_purpose": [
            {
                "statement": "Build models",
                "evidence": "Build models.",
                "confidence": "high",
            }
        ],
        "responsibilities": [],
        "requirements": [],
    }

    with pytest.raises(ValidationError, match="Responsibility coverage"):
        JobAnalysisResponse.model_validate(
            payload,
            context={
                "analysis_fields": fields,
                "analysis_mode": "english",
                "responsibility_coverage_plan": plan,
            },
        )
