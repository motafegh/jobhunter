from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.work_intelligence_models import DeliverableCandidate, JobWorkIntelligence, WorkTheme


def test_work_theme_json_schema_requires_structured_direct_work_references() -> None:
    schema = JobWorkIntelligence.model_json_schema()
    required = set(schema["$defs"]["WorkTheme"]["required"])

    assert {"responsibility_indices", "role_purpose_indices"} <= required


def test_deliverable_json_schema_requires_structured_direct_work_references() -> None:
    schema = JobWorkIntelligence.model_json_schema()
    required = set(schema["$defs"]["DeliverableCandidate"]["required"])

    assert {"responsibility_indices", "role_purpose_indices"} <= required


def test_work_theme_cannot_hide_source_references_only_in_rationale() -> None:
    with pytest.raises(ValidationError, match="responsibility_indices"):
        WorkTheme.model_validate(
            {
                "theme_id": "theme-1",
                "label": "Security architecture",
                "summary": "Design and implement network security architecture.",
                "emphasis": "primary",
                "confidence": "high",
                "rationale": "Covers responsibilities 0, 3, and 8.",
            }
        )


def test_deliverable_cannot_hide_source_references_only_in_rationale() -> None:
    with pytest.raises(ValidationError, match="responsibility_indices"):
        DeliverableCandidate.model_validate(
            {
                "label": "Security documentation",
                "summary": "Technical documentation for deployed security systems.",
                "status": "source_explicit",
                "confidence": "high",
                "rationale": "Supported by responsibility 9.",
            }
        )
