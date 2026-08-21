from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio import (
    AnalysisRequirement as HistoricalAnalysisRequirement,
)
from jobhunter.inference.instructor_lm_studio_v20 import (
    AnalysisRequirementV20,
    JobAnalysisResponseV20,
)


def _context(fields: dict) -> dict:
    return {
        "analysis_fields": fields,
        "analysis_mode": "english",
        "evidence_catalog": build_field_evidence_catalog(fields),
    }


def test_v20_accepts_sufficient_knowledge_as_explicit_employer_depth() -> None:
    evidence = "Sufficient knowledge of Object-Oriented concepts, modular design"
    fields = {"description": evidence}

    result = AnalysisRequirementV20.model_validate(
        {
            "concept": "Object-Oriented concepts, modular design",
            "depth_signal": evidence,
            "requirement_type": "required",
            "concept_type": "knowledge",
            "evidence": evidence,
            "confidence": "high",
            "rationale": "The employer explicitly states a sufficient-knowledge depth requirement.",
        },
        context=_context(fields),
    )

    assert result.concept == "Object-Oriented concepts, modular design"
    assert result.depth_signal == "Sufficient knowledge"
    assert result.evidence == evidence


def test_v20_depth_extension_does_not_mutate_historical_validator_registry() -> None:
    evidence = "Sufficient knowledge of Object-Oriented concepts"
    fields = {"description": evidence}

    with pytest.raises(ValidationError, match="explicit employer depth"):
        HistoricalAnalysisRequirement.model_validate(
            {
                "concept": "Object-Oriented concepts",
                "depth_signal": "Sufficient knowledge",
                "requirement_type": "required",
                "concept_type": "knowledge",
                "evidence": evidence,
                "confidence": "high",
                "rationale": "Historical contracts must not inherit v20 vocabulary by import.",
            },
            context=_context(fields),
        )


def test_v20_does_not_treat_plain_knowledge_as_depth() -> None:
    evidence = "Knowledge of Object-Oriented concepts"
    fields = {"description": evidence}

    with pytest.raises(ValidationError, match="explicit employer depth"):
        AnalysisRequirementV20.model_validate(
            {
                "concept": "Object-Oriented concepts",
                "depth_signal": "Knowledge",
                "requirement_type": "required",
                "concept_type": "knowledge",
                "evidence": evidence,
                "confidence": "high",
                "rationale": "Plain knowledge wording has no explicit degree qualifier.",
            },
            context=_context(fields),
        )


@pytest.mark.parametrize(
    ("concept", "signal", "expected"),
    [
        ("Django Rest Framework and FastAPI", "Mastery of DRF, FastAPI", "Mastery"),
        ("Linux operating system", "Familiarity with Linux operating system", "Familiarity"),
        (
            "SQL and NoSQL databases",
            "Familiarity with SQL and NoSQL databases",
            "Familiarity",
        ),
        (
            "Object-Oriented concepts and modular design",
            "Sufficient knowledge of Object-Oriented concepts, modular design",
            "Sufficient knowledge",
        ),
        (
            "Database locking, concurrency, and transaction management",
            "Familiarity with Database Locking, Concurrency, and Transaction Management",
            "Familiarity",
        ),
    ],
)
def test_v20_preserves_item_specific_depth_inside_multi_signal_evidence(
    concept: str,
    signal: str,
    expected: str,
) -> None:
    evidence = (
        "- Mastery of Python/Django - Mastery of DRF, FastAPI - Familiarity with Git "
        "- Familiarity with Linux operating system - Familiarity with SQL and NoSQL databases "
        "- Sufficient knowledge of Object-Oriented concepts, modular design - Familiarity with "
        "Database Locking, Concurrency, and Transaction Management."
    )
    fields = {"description": evidence}

    result = AnalysisRequirementV20.model_validate(
        {
            "concept": concept,
            "depth_signal": signal,
            "requirement_type": "required",
            "concept_type": "knowledge",
            "evidence": evidence,
            "confidence": "high",
            "rationale": "Exact subject-specific source depth.",
        },
        context=_context(fields),
    )

    assert result.depth_signal == expected
    assert result.evidence == evidence


def test_v20_rejects_depth_guessing_for_multi_level_evidence() -> None:
    evidence = (
        "- Mastery of Python/Django - Familiarity with Linux operating system "
        "- Sufficient knowledge of Object-Oriented concepts, modular design"
    )
    fields = {"description": evidence}

    with pytest.raises(ValidationError, match="multiple explicit employer depth signals"):
        AnalysisRequirementV20.model_validate(
            {
                "concept": "Linux operating system",
                "depth_signal": None,
                "requirement_type": "required",
                "concept_type": "tool",
                "evidence": evidence,
                "confidence": "high",
                "rationale": "The validator must not borrow another subject's depth marker.",
            },
            context=_context(fields),
        )


def test_v20_clears_exact_effective_application_phrase_when_evidence_has_no_depth() -> None:
    evidence = (
        "Ability to effectively use (AI) to increase the quality and speed of software "
        "development."
    )
    signal = "effectively use (AI) to increase the quality and speed of software development"
    fields = {"description": evidence}

    result = AnalysisRequirementV20.model_validate(
        {
            "concept": "AI usage in software development",
            "depth_signal": signal,
            "requirement_type": "required",
            "concept_type": "skill",
            "evidence": evidence,
            "confidence": "high",
            "rationale": "Effective application is required, but no proficiency depth is stated.",
        },
        context=_context(fields),
    )

    assert result.depth_signal is None
    assert result.requirement_type == "required"
    assert result.evidence == evidence


@pytest.mark.parametrize(
    ("evidence", "concept"),
    [
        (
            "Ability to analyze vulnerabilities and provide practical solutions",
            "Vulnerability analysis and practical solutions",
        ),
        (
            "Skill in troubleshooting Windows and Active Directory",
            "Windows and Active Directory troubleshooting",
        ),
    ],
)
def test_v20_clears_ability_and_skill_application_phrases_without_real_depth(
    evidence: str,
    concept: str,
) -> None:
    fields = {"description": evidence}

    result = AnalysisRequirementV20.model_validate(
        {
            "concept": concept,
            "depth_signal": evidence,
            "requirement_type": "required",
            "concept_type": "skill",
            "evidence": evidence,
            "confidence": "high",
            "rationale": "The source requires the capability without stating proficiency depth.",
        },
        context=_context(fields),
    )

    assert result.depth_signal is None


def test_v20_does_not_clear_effective_application_when_evidence_also_has_real_depth() -> None:
    evidence = (
        "Mastery of Python and ability to effectively use (AI) to improve software development."
    )
    signal = "effectively use (AI) to improve software development"
    fields = {"description": evidence}

    with pytest.raises(ValidationError, match="explicit employer depth"):
        AnalysisRequirementV20.model_validate(
            {
                "concept": "AI usage in software development",
                "depth_signal": signal,
                "requirement_type": "required",
                "concept_type": "skill",
                "evidence": evidence,
                "confidence": "high",
                "rationale": "A different subject in the same evidence has real depth.",
            },
            context=_context(fields),
        )


def test_v20_drops_only_redundant_exclusion_for_already_extracted_reference() -> None:
    represented_ref = "field:description:segment:1"
    represented_text = "Ability to effectively use AI for software development."
    excluded_ref = "field:description:segment:2"
    excluded_text = "Office location and benefits information."
    fields = {"description": f"{represented_text} {excluded_text}"}
    context = _context(fields)
    context["requirement_coverage_plan"] = {
        represented_ref: {
            "text": represented_text,
            "source_kind": "description",
            "obligation_hint": "required",
            "allow_exclusion": True,
        },
        excluded_ref: {
            "text": excluded_text,
            "source_kind": "description",
            "obligation_hint": "contextual",
            "allow_exclusion": True,
        },
    }
    context["evidence_catalog"] = {
        represented_ref: represented_text,
        excluded_ref: excluded_text,
    }
    context["responsibility_coverage_plan"] = {}

    result = JobAnalysisResponseV20.model_validate(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                {
                    "concept": "AI usage in software development",
                    "depth_signal": None,
                    "requirement_type": "required",
                    "concept_type": "skill",
                    "evidence": represented_ref,
                    "confidence": "high",
                    "rationale": "Explicit source requirement.",
                }
            ],
            "coverage_exclusions": [
                {
                    "evidence_reference": represented_ref,
                    "rationale": "Redundant decomposition bookkeeping entry.",
                },
                {
                    "evidence_reference": excluded_ref,
                    "rationale": "This source text is contextual rather than a qualification.",
                },
            ],
        },
        context=context,
    )

    assert [item.evidence_reference for item in result.coverage_exclusions] == [excluded_ref]
