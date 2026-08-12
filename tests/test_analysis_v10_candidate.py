import pytest

from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v10 import (
    ENGLISH_PROMPT_VERSION,
    _persisted_analysis_v10,
    validate_v10_candidate_structured,
)


def _fields():
    return {
        "description": (
            "Skills in content creation with AI, website design, ability to produce visual "
            "content. Ethics and work commitment are important."
        ),
        "skills": ["Artificial Intelligence", "Video content production", "social networks"],
    }


def _requirement(evidence: str, concept: str | None = None):
    return {
        "concept": concept or evidence,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Explicit structured required skill.",
    }


def test_v10_has_distinct_artifact_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v10"


def test_v10_rejects_missing_structured_skill() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="social networks"):
        validate_v10_candidate_structured(structured, _fields())


def test_v10_rejects_structured_skill_strength_drift() -> None:
    social = _requirement("social networks")
    social["requirement_type"] = "contextual"
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
            social,
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="obligation"):
        validate_v10_candidate_structured(structured, _fields())


def test_v10_rejects_ability_qualification_as_responsibility() -> None:
    evidence = "ability to produce visual content"
    structured = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "produce visual content",
                "evidence": evidence,
                "confidence": "high",
            }
        ],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
            _requirement("social networks"),
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="ability to"):
        validate_v10_candidate_structured(structured, _fields())


def test_v10_rejects_responsibility_reusing_requirement_evidence() -> None:
    shared = "Artificial Intelligence"
    structured = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Use artificial intelligence",
                "evidence": shared,
                "confidence": "high",
            }
        ],
        "requirements": [
            _requirement(shared),
            _requirement("Video content production"),
            _requirement("social networks"),
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="qualification evidence"):
        validate_v10_candidate_structured(structured, _fields())


def test_v10_persistence_adds_structured_skill_coverage() -> None:
    fields = {
        "description": "Short source text without a recognized requirement heading.",
        "skills": ["Artificial Intelligence", "social networks"],
    }
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("social networks"),
        ],
        "coverage_exclusions": [],
    }

    analysis = _persisted_analysis_v10(structured, fields)

    coverage = {
        item["evidence"]: item["disposition"]
        for item in analysis["coverage"]
    }
    assert coverage == {
        "Artificial Intelligence": "extracted_requirement",
        "social networks": "extracted_requirement",
    }


def test_v10_accepts_conservative_sparse_shape() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
            _requirement("social networks"),
            _requirement(
                "website design",
                concept="Website design",
            ),
        ],
        "coverage_exclusions": [],
    }

    validate_v10_candidate_structured(structured, _fields())
