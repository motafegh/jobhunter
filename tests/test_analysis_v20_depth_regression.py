from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v20 import AnalysisRequirementV20


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
