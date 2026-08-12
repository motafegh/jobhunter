import pytest

from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v11 import (
    ENGLISH_PROMPT_VERSION,
    _persisted_analysis_v11,
    qualification_list_spans,
    validate_v11_candidate_structured,
)


def _fields():
    return {
        "description": (
            "Skills in content creation with AI, creativity in creating visual and video content, "
            "website design, ability to produce visual content full-time and part-time, "
            "the work is teachable. Ethics and work commitment are important. "
            "Benefits include insurance, parking, bonus."
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
        "rationale": "Explicit source qualification.",
    }


def _valid_requirements():
    fields = _fields()
    return [
        _requirement("Artificial Intelligence"),
        _requirement("Video content production"),
        _requirement("social networks"),
        *[_requirement(span) for span in qualification_list_spans(fields)],
    ]


def _coarse_coverage_exclusion():
    return {
        "evidence_reference": "field:description:segment:0",
        "rationale": "Superseded by exact qualification-list item requirements.",
    }


def test_v11_has_distinct_artifact_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v11"


def test_v11_extracts_only_explicit_qualification_list_items() -> None:
    assert qualification_list_spans(_fields()) == [
        "Skills in content creation with AI",
        "creativity in creating visual and video content",
        "website design",
        "ability to produce visual content full-time and part-time",
    ]


def test_v11_does_not_treat_arbitrary_comma_sentence_as_qualification_list() -> None:
    fields = {
        "description": "Benefits include insurance, parking, commission, annual bonus.",
        "skills": [],
    }
    assert qualification_list_spans(fields) == []


def test_v11_accepts_common_technical_qualification_list() -> None:
    fields = {
        "description": "Skills in Python, SQL, Docker. The team builds internal tools.",
        "skills": [],
    }
    assert qualification_list_spans(fields) == ["Skills in Python", "SQL", "Docker"]


def test_v11_rejects_missing_qualification_item() -> None:
    requirements = _valid_requirements()
    requirements = [
        item
        for item in requirements
        if item["evidence"] != "creativity in creating visual and video content"
    ]
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": requirements,
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="creativity"):
        validate_v11_candidate_structured(structured, _fields())


def test_v11_rejects_coarse_requirement_evidence_after_decomposition() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            *_valid_requirements(),
            _requirement(_fields()["description"], concept="General content qualifications"),
        ],
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="coarse evidence"):
        validate_v11_candidate_structured(structured, _fields())


def test_v11_rejects_qualification_list_item_as_responsibility() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Design websites",
                "evidence": "website design",
                "confidence": "high",
            }
        ],
        "requirements": _valid_requirements(),
        "coverage_exclusions": [],
    }

    with pytest.raises(AnalysisValidationError, match="qualification"):
        validate_v11_candidate_structured(structured, _fields())


def test_v11_persistence_accounts_for_structured_and_list_coverage() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": _valid_requirements(),
        "coverage_exclusions": [_coarse_coverage_exclusion()],
    }

    analysis = _persisted_analysis_v11(structured, _fields())
    coverage = {
        item["evidence"]: item["disposition"]
        for item in analysis["coverage"]
    }

    for evidence in [
        "Artificial Intelligence",
        "Video content production",
        "social networks",
        "Skills in content creation with AI",
        "creativity in creating visual and video content",
        "website design",
        "ability to produce visual content full-time and part-time",
    ]:
        assert coverage[evidence] == "extracted_requirement"

    assert any(
        item["disposition"] == "decomposed_requirement"
        and "content creation with AI" in item["evidence"]
        for item in analysis["coverage"]
    )
