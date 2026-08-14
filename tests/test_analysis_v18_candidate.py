from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.analysis_runtime_v18 import (
    _materialize_v18_deterministic_requirements,
    _v18_structured_partition,
    _v18_structured_skill_coverage_plan,
)
from jobhunter.analysis_service_v14 import _persisted_analysis_v14
from jobhunter.analysis_service_v17 import _validate_evidence_v17, validate_v17_candidate_structured
from jobhunter.analysis_service_v18 import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    _ANALYSIS_SCHEMA_V18,
    _ENGLISH_SYSTEM_PROMPT_V18,
)
from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v17 import JobAnalysisResponseV17


def _fields() -> dict:
    return {
        "title": "Dense role",
        "skills": ["Python", "Linux", "Git"],
        "minimum_experience": "three to six years",
        "education": "Master's degree",
    }


def _skill_requirement(skill: str) -> dict:
    return {
        "concept": skill,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": skill,
        "confidence": "high",
        "rationale": "Structured skill requirement.",
    }


def test_v18_has_new_prompt_identity_without_changing_v5_shape() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v18"
    assert ANALYSIS_SCHEMA_VERSION == "job-analysis-v5"
    assert "DETERMINISTIC STRUCTURED-FACT OWNERSHIP" in _ENGLISH_SYSTEM_PROMPT_V18
    assert "maxItems" not in _ANALYSIS_SCHEMA_V18["properties"]["requirements"]


def test_v18_partition_moves_parseable_experience_and_education_out_of_model_view() -> None:
    fields = _fields()
    model_fields, deterministic, references = _v18_structured_partition(fields, fields)

    assert "minimum_experience" not in model_fields
    assert "education" not in model_fields
    assert model_fields["skills"] == ["Python", "Linux", "Git"]
    assert references == ["field:minimum_experience", "field:education"]

    experience = deterministic[0]
    assert experience["concept"] == "Professional experience"
    assert experience["depth_signal"] == "three to six years"
    assert experience["concept_type"] == "experience"
    assert experience["evidence"] == "three to six years"

    education = deterministic[1]
    assert education["concept"] == "Master's degree"
    assert education["depth_signal"] is None
    assert education["concept_type"] == "education"
    assert education["evidence"] == "Master's degree"


def test_v18_unrecognized_experience_wording_remains_model_owned() -> None:
    fields = {
        **_fields(),
        "minimum_experience": "Several years of professional experience",
    }
    model_fields, deterministic, references = _v18_structured_partition(fields, fields)

    assert model_fields["minimum_experience"] == "Several years of professional experience"
    assert "education" not in model_fields
    assert references == ["field:education"]
    assert [item["concept_type"] for item in deterministic] == ["education"]


def test_v18_structured_skills_get_explicit_non_excludable_coverage() -> None:
    plan = _v18_structured_skill_coverage_plan(_fields())

    assert sorted(plan) == ["field:skills:0", "field:skills:1", "field:skills:2"]
    assert all(item["obligation_hint"] == "required" for item in plan.values())
    assert all(item["allow_exclusion"] is False for item in plan.values())


def test_v18_typed_retry_feedback_reports_all_missing_structured_skills() -> None:
    fields = _fields()
    model_fields, _deterministic, _references = _v18_structured_partition(fields, fields)
    skill_plan = _v18_structured_skill_coverage_plan(model_fields)
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [_skill_requirement("Python")],
        "coverage_exclusions": [],
    }
    context = {
        "analysis_fields": model_fields,
        "evidence_catalog": build_field_evidence_catalog(model_fields),
        "analysis_mode": "english",
        "requirement_coverage_plan": skill_plan,
        "responsibility_coverage_plan": {},
    }

    with pytest.raises(ValidationError) as exc_info:
        JobAnalysisResponseV17.model_validate(payload, context=context)

    error = str(exc_info.value)
    assert "field:skills:1" in error
    assert "field:skills:2" in error
    assert "field:minimum_experience" not in error
    assert "field:education" not in error


def test_v18_materialized_structured_facts_pass_existing_strict_validation() -> None:
    fields = _fields()
    _model_fields, deterministic, _references = _v18_structured_partition(fields, fields)
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [_skill_requirement(skill) for skill in fields["skills"]],
        "coverage_exclusions": [],
    }
    structured = _materialize_v18_deterministic_requirements(structured, deterministic)

    validate_v17_candidate_structured(structured, fields)
    analysis = _persisted_analysis_v14(structured, fields)
    _validate_evidence_v17(analysis, fields)

    by_evidence = {
        item["evidence"]: item
        for item in analysis["requirements"]
    }
    assert by_evidence["three to six years"]["concept"] == "Professional experience"
    assert by_evidence["three to six years"]["depth_signal"] == "three to six years"
    assert by_evidence["Master's degree"]["concept_type"] == "education"


def test_v18_materializer_is_idempotent_for_identical_deterministic_records() -> None:
    fields = _fields()
    _model_fields, deterministic, _references = _v18_structured_partition(fields, fields)
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [*deterministic],
        "coverage_exclusions": [],
    }

    once = _materialize_v18_deterministic_requirements(structured, deterministic)
    twice = _materialize_v18_deterministic_requirements(once, deterministic)

    assert len(once["requirements"]) == 2
    assert twice == once
