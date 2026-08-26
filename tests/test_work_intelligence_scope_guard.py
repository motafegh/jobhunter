from __future__ import annotations

import pytest

from jobhunter.work_intelligence_models import JobWorkIntelligence, WorkTheme
from jobhunter.work_intelligence_service import (
    WORK_INTELLIGENCE_PROMPT_VERSION,
    WorkIntelligenceError,
    _validate_scope_language,
)


def _document(summary: str) -> JobWorkIntelligence:
    return JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary=summary,
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Network security design",
                summary="Design and implement network security architecture.",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale="The accepted responsibility directly describes security design work.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )


def test_scope_guard_rejects_unsupported_end_to_end_language() -> None:
    document = _document(
        "This role provides end-to-end network security design and implementation "
        "across the estate."
    )

    with pytest.raises(WorkIntelligenceError, match="unsupported lifecycle/scope intensifier"):
        _validate_scope_language(
            document,
            responsibilities=[
                {"statement": "Designing and implementing network security architecture"}
            ],
            role_purpose=[],
        )


def test_scope_guard_allows_explicit_source_scope_language() -> None:
    document = _document(
        "This role provides end-to-end network security implementation for the stated platform."
    )

    _validate_scope_language(
        document,
        responsibilities=[
            {"statement": "Providing end-to-end network security implementation"}
        ],
        role_purpose=[],
    )


def test_scope_repair_bumps_prompt_identity_without_schema_churn() -> None:
    assert WORK_INTELLIGENCE_PROMPT_VERSION == "job-work-intelligence-v1.1"
