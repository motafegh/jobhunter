from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.analysis_service_v19 import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    _ANALYSIS_SCHEMA_V19,
    _ENGLISH_SYSTEM_PROMPT_V19,
)
from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v19 import (
    AnalysisRequirementV19,
    JobAnalysisResponseV19,
)


def _context(fields: dict) -> dict:
    return {
        "analysis_fields": fields,
        "analysis_mode": "english",
        "evidence_catalog": build_field_evidence_catalog(fields),
    }


def test_v19_has_new_prompt_identity_without_changing_v5_shape() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v19"
    assert ANALYSIS_SCHEMA_VERSION == "job-analysis-v5"
    assert "DEPTH / OPTIONALITY CANONICALIZATION" in _ENGLISH_SYSTEM_PROMPT_V19
    assert "maxItems" not in _ANALYSIS_SCHEMA_V19["properties"]["requirements"]


def test_v19_clears_preference_wording_from_depth_signal() -> None:
    fields = {"description": "MATLAB a plus"}
    result = AnalysisRequirementV19.model_validate(
        {
            "concept": "MATLAB",
            "depth_signal": "a plus",
            "requirement_type": "preferred",
            "concept_type": "tool",
            "evidence": "MATLAB a plus",
            "confidence": "high",
            "rationale": "Explicit preference.",
        },
        context=_context(fields),
    )

    assert result.requirement_type == "preferred"
    assert result.depth_signal is None
    assert result.evidence == "MATLAB a plus"


def test_v19_clears_helpful_from_depth_signal_without_losing_preference() -> None:
    fields = {"description": "some C / C++ helpful"}
    result = AnalysisRequirementV19.model_validate(
        {
            "concept": "C / C++",
            "depth_signal": "helpful",
            "requirement_type": "preferred",
            "concept_type": "tool",
            "evidence": "some C / C++ helpful",
            "confidence": "high",
            "rationale": "Explicit preference.",
        },
        context=_context(fields),
    )

    assert result.requirement_type == "preferred"
    assert result.depth_signal is None
    assert result.concept == "C / C++"


def test_v19_removes_unsupported_expertise_from_normalized_concept() -> None:
    evidence = (
        "Semiconductor domain: FDC / APC / SPC, virtual metrology, run-to-run control, "
        "yield analysis"
    )
    fields = {"description": evidence}
    result = AnalysisRequirementV19.model_validate(
        {
            "concept": (
                "Semiconductor domain expertise (FDC / APC / SPC, virtual metrology, "
                "run-to-run control, yield analysis)"
            ),
            "depth_signal": None,
            "requirement_type": "contextual",
            "concept_type": "domain",
            "evidence": evidence,
            "confidence": "high",
            "rationale": "Contextual domain knowledge.",
        },
        context=_context(fields),
    )

    assert result.concept == (
        "Semiconductor domain (FDC / APC / SPC, virtual metrology, run-to-run control, "
        "yield analysis)"
    )
    assert result.depth_signal is None
    assert result.evidence == evidence


def test_v19_preserves_genuine_source_depth_for_strict_validator() -> None:
    fields = {"description": "Python (expert)"}
    result = AnalysisRequirementV19.model_validate(
        {
            "concept": "Python",
            "depth_signal": None,
            "requirement_type": "contextual",
            "concept_type": "skill",
            "evidence": "Python (expert)",
            "confidence": "high",
            "rationale": "Explicit source depth.",
        },
        context=_context(fields),
    )

    assert result.concept == "Python"
    assert result.depth_signal == "expert"


def test_v19_still_fails_closed_when_depth_cleanup_would_destroy_concept() -> None:
    fields = {"description": "Semiconductor domain"}

    with pytest.raises(ValidationError, match="concept contains expert depth wording"):
        AnalysisRequirementV19.model_validate(
            {
                "concept": "expertise",
                "depth_signal": None,
                "requirement_type": "contextual",
                "concept_type": "domain",
                "evidence": "Semiconductor domain",
                "confidence": "high",
                "rationale": "Invalid generic concept.",
            },
            context=_context(fields),
        )


def test_v19_exact_live_failure_trio_validates_together() -> None:
    semiconductor = (
        "Semiconductor domain: FDC / APC / SPC, virtual metrology, run-to-run control, "
        "yield analysis"
    )
    fields = {
        "description": "\n".join(
            [
                "MATLAB a plus",
                "some C / C++ helpful",
                semiconductor,
            ]
        )
    }
    payload = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                "concept": "MATLAB",
                "depth_signal": "a plus",
                "requirement_type": "preferred",
                "concept_type": "tool",
                "evidence": "MATLAB a plus",
                "confidence": "high",
                "rationale": "Explicitly preferred tool.",
            },
            {
                "concept": "C / C++",
                "depth_signal": "helpful",
                "requirement_type": "preferred",
                "concept_type": "tool",
                "evidence": "some C / C++ helpful",
                "confidence": "high",
                "rationale": "Explicitly preferred tool.",
            },
            {
                "concept": (
                    "Semiconductor domain expertise (FDC / APC / SPC, virtual metrology, "
                    "run-to-run control, yield analysis)"
                ),
                "depth_signal": None,
                "requirement_type": "contextual",
                "concept_type": "domain",
                "evidence": semiconductor,
                "confidence": "high",
                "rationale": "Contextually mentioned domain knowledge.",
            },
        ],
        "coverage_exclusions": [],
    }

    result = JobAnalysisResponseV19.model_validate(payload, context=_context(fields))

    assert len(result.requirements) == 3
    assert result.requirements[0].depth_signal is None
    assert result.requirements[1].depth_signal is None
    assert "expertise" not in result.requirements[2].concept.casefold()
