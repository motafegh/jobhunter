from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.work_intelligence_models import (
    CandidateDeliverable,
    CandidateJobWorkIntelligence,
    CandidateWorkTheme,
)


def test_candidate_work_theme_schema_requires_structured_direct_work_references() -> None:
    schema = CandidateJobWorkIntelligence.model_json_schema()
    required = set(schema["$defs"]["CandidateWorkTheme"]["required"])

    assert {"responsibility_indices", "role_purpose_indices"} <= required


def test_candidate_deliverable_schema_requires_structured_direct_work_references() -> None:
    schema = CandidateJobWorkIntelligence.model_json_schema()
    required = set(schema["$defs"]["CandidateDeliverable"]["required"])

    assert {"responsibility_indices", "role_purpose_indices"} <= required


def test_candidate_work_theme_cannot_hide_source_references_only_in_rationale() -> None:
    with pytest.raises(ValidationError, match="responsibility_indices"):
        CandidateWorkTheme.model_validate(
            {
                "theme_id": "theme-1",
                "label": "Security architecture",
                "emphasis": "primary",
                "confidence": "high",
                "rationale": "Covers responsibilities 0, 3, and 8.",
            }
        )


def test_candidate_deliverable_cannot_hide_source_references_only_in_rationale() -> None:
    with pytest.raises(ValidationError, match="responsibility_indices"):
        CandidateDeliverable.model_validate(
            {
                "label": "Security documentation",
                "status": "source_explicit",
                "confidence": "high",
                "rationale": "Supported by responsibility 9.",
            }
        )
