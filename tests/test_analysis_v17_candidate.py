from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.analysis_service import AnalysisValidationError, _ANALYSIS_SCHEMA
from jobhunter.analysis_service_v17 import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    _ANALYSIS_SCHEMA_V17,
    _ENGLISH_SYSTEM_PROMPT_V17,
    _validate_evidence_v17,
)
from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v14 import JobAnalysisResponseV14
from jobhunter.inference.instructor_lm_studio_v17 import JobAnalysisResponseV17


def _fields(count: int = 33) -> dict:
    return {
        "title": "Dense role",
        "skills": [f"Skill {index}" for index in range(count)],
    }


def _requirements(count: int = 33) -> list[dict]:
    return [
        {
            "concept": f"Skill {index}",
            "depth_signal": None,
            "requirement_type": "required",
            "concept_type": "skill",
            "evidence": f"Skill {index}",
            "confidence": "high",
            "rationale": "Structured source skill.",
        }
        for index in range(count)
    ]


def _typed_payload(count: int = 33) -> dict:
    return {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": _requirements(count),
        "coverage_exclusions": [],
    }


def _persisted_payload(count: int = 33) -> dict:
    return {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": _requirements(count),
        "coverage": [],
        "responsibility_coverage": [],
    }


def test_v17_has_new_prompt_and_schema_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v17"
    assert ANALYSIS_SCHEMA_VERSION == "job-analysis-v5"
    assert "no fixed 32-item semantic ceiling" in _ENGLISH_SYSTEM_PROMPT_V17


def test_v17_schema_removes_requirement_cap_without_mutating_v4() -> None:
    assert _ANALYSIS_SCHEMA["properties"]["requirements"]["maxItems"] == 32
    assert "maxItems" not in _ANALYSIS_SCHEMA_V17["properties"]["requirements"]


def test_v17_typed_model_accepts_33_requirements_while_v14_stays_bounded() -> None:
    fields = _fields()
    context = {
        "analysis_fields": fields,
        "evidence_catalog": build_field_evidence_catalog(fields),
    }
    payload = _typed_payload()

    with pytest.raises(ValidationError):
        JobAnalysisResponseV14.model_validate(payload, context=context)

    result = JobAnalysisResponseV17.model_validate(payload, context=context)
    assert len(result.requirements) == 33


def test_v17_final_guard_accepts_33_grounded_unique_requirements() -> None:
    _validate_evidence_v17(_persisted_payload(), _fields())


def test_v17_final_guard_rejects_duplicate_across_legacy_batch_boundary() -> None:
    payload = _persisted_payload()
    payload["requirements"][32] = dict(payload["requirements"][0])

    with pytest.raises(AnalysisValidationError, match="duplicates an earlier requirement"):
        _validate_evidence_v17(payload, _fields())


def test_v17_final_guard_still_rejects_ungrounded_evidence_after_item_32() -> None:
    payload = _persisted_payload()
    payload["requirements"][32] = {
        **payload["requirements"][32],
        "evidence": "Invented skill that is not in the source",
    }

    with pytest.raises(AnalysisValidationError, match="not an exact excerpt"):
        _validate_evidence_v17(payload, _fields())
