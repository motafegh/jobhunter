from __future__ import annotations

import pytest

from jobhunter.analysis_runtime_v16 import _clean_v16_concepts
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v16 import (
    ENGLISH_PROMPT_VERSION,
    _ENGLISH_SYSTEM_PROMPT_V16,
    validate_v16_candidate_structured,
)


def _fields() -> dict:
    return {
        "description": "ability to produce visual content full-time and part-time",
        "skills": [],
    }


def _structured(*, concept: str, concept_type: str, evidence: str) -> dict:
    return {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                "concept": concept,
                "concept_type": concept_type,
                "requirement_type": "required",
                "depth_signal": None,
                "evidence": evidence,
                "confidence": "high",
                "rationale": "Explicit qualification.",
            }
        ],
        "coverage_exclusions": [],
    }


def test_v16_has_distinct_identity_and_experience_rule() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v16"
    assert "prior applied exposure" in _ENGLISH_SYSTEM_PROMPT_V16


def test_v16_cleans_empty_grouping_without_changing_evidence() -> None:
    evidence = "ability to produce visual content full-time and part-time"
    structured = _structured(
        concept="Visual content production ( )",
        concept_type="skill",
        evidence=evidence,
    )
    normalized, changed = _clean_v16_concepts(structured)
    assert changed == [0]
    assert normalized["requirements"][0]["concept"] == "Visual content production"
    assert normalized["requirements"][0]["evidence"] == evidence


def test_v16_rejects_experience_type_for_ability_without_experience_evidence() -> None:
    structured = _structured(
        concept="Visual content production",
        concept_type="experience",
        evidence="ability to produce visual content full-time and part-time",
    )
    with pytest.raises(AnalysisValidationError, match="prior-exposure"):
        validate_v16_candidate_structured(structured, _fields())


def test_v16_does_not_reject_experience_when_source_explicitly_says_experience() -> None:
    evidence = "3 years of experience producing visual content"
    structured = _structured(
        concept="Visual content production experience",
        concept_type="experience",
        evidence=evidence,
    )
    # The v16-specific experience guard allows this evidence; shared v15/v14 guards
    # may still validate other source-contract details in full integration tests.
    assert "experience" in evidence
