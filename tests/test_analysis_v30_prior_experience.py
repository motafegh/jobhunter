"""Preserve source-explicit prior experience without broad type coercion."""

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_service_v30 import ENGLISH_PROMPT_VERSION
from jobhunter.inference.instructor_lm_studio_v30 import AnalysisRequirementV30


def _parse(evidence: str, kind: str) -> AnalysisRequirementV30:
    return AnalysisRequirementV30.model_validate(
        {
            "concept": evidence,
            "depth_signal": None,
            "requirement_type": "required",
            "concept_type": kind,
            "evidence": evidence,
            "confidence": "high",
            "rationale": "Exact source requirement.",
            "item_excerpt": evidence,
        },
        context={"analysis_mode": "english", "analysis_fields": {"description": evidence}},
    )


def test_practical_design_experience_is_prior_experience() -> None:
    text = "practical experience in designing and implementing RAG systems"
    assert _parse(text, "skill").concept_type == "experience"


def test_activity_without_prior_experience_stays_untyped() -> None:
    text = "designing and implementing RAG systems"
    assert _parse(text, "other").concept_type == "other"


def test_v30_isolated_from_public_v23() -> None:
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v30"
