import pytest
from pydantic import ValidationError

from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio import JobAnalysisResponse


def _rich_fields() -> dict:
    return {
        "description": (
            "What you'll do ● Build and validate ML/AI models on semiconductor data. "
            "● Design rigorous validation and monitoring for industrial models. "
            "What we're looking for ● Strong experience applying AI/ML to manufacturing data."
        ),
        "skills": ["Artificial Intelligence", "Python", "Machine learning"],
    }


def test_analysis_evidence_reference_resolves_to_exact_source_text() -> None:
    fields = _rich_fields()
    catalog = build_field_evidence_catalog(fields)
    payload = {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Build and validate industrial ML models",
                "evidence": "field:description:segment:0",
                "confidence": "high",
            }
        ],
        "requirements": [
            {
                "concept": "Python",
                "requirement_type": "required",
                "concept_type": "skill",
                "evidence": "field:skills:1",
                "confidence": "high",
                "rationale": "",
            }
        ],
    }

    result = JobAnalysisResponse.model_validate(
        payload,
        context={"analysis_fields": fields, "evidence_catalog": catalog},
    )

    assert result.responsibilities[0].evidence == (
        "Build and validate ML/AI models on semiconductor data."
    )
    assert result.requirements[0].evidence == "Python"


def test_information_rich_source_cannot_validate_as_empty_analysis() -> None:
    fields = _rich_fields()
    catalog = build_field_evidence_catalog(fields)

    with pytest.raises(ValidationError, match="Information-rich job fields"):
        JobAnalysisResponse.model_validate(
            {"role_purpose": [], "responsibilities": [], "requirements": []},
            context={"analysis_fields": fields, "evidence_catalog": catalog},
        )


def test_sparse_source_may_still_validate_empty_analysis() -> None:
    fields = {"title": "General Assistant", "description": "Short unclear posting."}
    result = JobAnalysisResponse.model_validate(
        {"role_purpose": [], "responsibilities": [], "requirements": []},
        context={"analysis_fields": fields, "evidence_catalog": {}},
    )

    assert result.responsibilities == []
    assert result.requirements == []
