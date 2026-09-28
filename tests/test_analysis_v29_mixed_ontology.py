"""Exact source ontology abstention for mixed P1.6 items."""

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_service_v29 import ENGLISH_PROMPT_VERSION
from jobhunter.inference.instructor_lm_studio_v29 import AnalysisRequirementV29


def _claim(concept: str, evidence: str, kind: str) -> dict:
    return {
        "concept": concept,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": kind,
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Exact source claim.",
        "item_excerpt": evidence,
    }


def _parse(claim: dict) -> AnalysisRequirementV29:
    return AnalysisRequirementV29.model_validate(
        claim,
        context={
            "analysis_mode": "english",
            "analysis_fields": {"description": claim["evidence"]},
        },
    )


def test_mixed_knowledge_and_experience_abstains_from_single_type() -> None:
    evidence = "specialized knowledge and practical experience in Model Context Protocol"
    assert _parse(_claim(evidence, evidence, "knowledge")).concept_type == "other"


def test_mixed_education_and_experience_abstains_from_single_type() -> None:
    evidence = "specialized education in AI, along with practical experience in LLM"
    assert _parse(_claim(evidence, evidence, "education")).concept_type == "other"


def test_source_explicit_knowledge_is_not_just_the_named_tool() -> None:
    evidence = "proficient knowledge of the Python programming language"
    claim = _claim("knowledge of the Python programming language", evidence, "tool")
    claim["depth_signal"] = "proficient"
    assert _parse(claim).concept_type == "knowledge"


def test_v29_does_not_change_public_current_contract() -> None:
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v29"
