from __future__ import annotations

import pytest

from jobhunter.analysis_runtime_v14 import _v14_candidate_evidence_view
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import inject_decomposition_exclusions
from jobhunter.analysis_service_v14 import (
    ENGLISH_PROMPT_VERSION,
    _persisted_analysis_v14,
    qualification_list_spans,
    residual_requirement_spans,
    validate_v14_candidate_structured,
)


def _fields():
    return {
        "description": (
            "Skills in content creation with AI, creativity in creating visual and video content, "
            "website design, ability to produce visual content full-time and part-time, "
            "the work is teachable. Ethics and your work commitment are important to us. "
            "Please do not send your resume for remote work. (Location: West Tehran) Benefits "
            "include insurance, parking, rest area, monthly discount, commission, business travel."
        ),
        "skills": ["Artificial Intelligence", "Video content production", "social networks"],
    }


def _requirement(evidence: str, concept: str):
    return {
        "concept": concept,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Explicit source qualification.",
    }


def _valid_structured():
    fields = _fields()
    spans = qualification_list_spans(fields)
    residuals = residual_requirement_spans(fields)
    requirements = [
        _requirement(spans[0], "Content creation with AI"),
        _requirement(spans[1], "Creativity in visual and video content"),
        _requirement(spans[2], "Website design"),
        _requirement(spans[3], "Visual content production"),
        _requirement("Artificial Intelligence", "Artificial Intelligence"),
        _requirement("Video content production", "Video content production"),
        _requirement("social networks", "Social networks"),
        {
            "concept": "Ethics and work commitment",
            "depth_signal": None,
            "requirement_type": "required",
            "concept_type": "other",
            "evidence": residuals[1],
            "confidence": "high",
            "rationale": "Explicit employer expectation.",
        },
    ]
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": requirements,
        "coverage_exclusions": [
            {
                "evidence_reference": f"field:__candidate_residual_requirement_evidence:{index}",
                "rationale": "This residual is logistics or non-qualification context.",
            }
            for index in (0, 2, 3)
        ],
    }
    return inject_decomposition_exclusions(structured, fields)


def test_v14_has_distinct_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v14"


def test_v14_residual_spans_preserve_remaining_exact_sentences() -> None:
    assert residual_requirement_spans(_fields()) == [
        "the work is teachable.",
        "Ethics and your work commitment are important to us.",
        "Please do not send your resume for remote work.",
        "(Location: West Tehran) Benefits include insurance, parking, rest area, monthly discount, commission, business travel.",
    ]


def test_v14_candidate_view_adds_mandatory_and_residual_coverage() -> None:
    effective, qualification_refs, residual_refs, plan = _v14_candidate_evidence_view(_fields())
    assert len(qualification_refs) == 4
    assert len(residual_refs) == 4
    assert len(plan) == 8
    assert all(plan[ref]["allow_exclusion"] is False for ref in qualification_refs)
    assert all(plan[ref]["allow_exclusion"] is True for ref in residual_refs)
    assert effective["__candidate_residual_requirement_evidence"][1] == (
        "Ethics and your work commitment are important to us."
    )


def test_v14_rejects_ability_wrapper_and_schedule_words_in_capability_concept() -> None:
    structured = _valid_structured()
    target = structured["requirements"][3]
    target["concept"] = "Ability to produce visual content full-time and part-time"
    with pytest.raises(AnalysisValidationError, match="Ability to"):
        validate_v14_candidate_structured(structured, _fields())

    target["concept"] = "Visual content production full-time"
    with pytest.raises(AnalysisValidationError, match="schedule"):
        validate_v14_candidate_structured(structured, _fields())


def test_v14_persistence_accounts_for_every_residual_sentence() -> None:
    analysis = _persisted_analysis_v14(_valid_structured(), _fields())
    coverage = {item["evidence"]: item["disposition"] for item in analysis["coverage"]}
    residuals = residual_requirement_spans(_fields())
    assert coverage[residuals[1]] == "extracted_requirement"
    assert coverage[residuals[0]] == "excluded_non_requirement"
    assert coverage[residuals[2]] == "excluded_non_requirement"
    assert coverage[residuals[3]] == "excluded_non_requirement"
    assert any(item["disposition"] == "decomposed_requirement" for item in analysis["coverage"])
