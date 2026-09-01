from __future__ import annotations

import pytest

from jobhunter.work_intelligence_models import CandidateJobWorkIntelligence, CandidateWorkTheme
from jobhunter.work_intelligence_service import (
    WORK_INTELLIGENCE_PROMPT_VERSION,
    WORK_INTELLIGENCE_SCHEMA_VERSION,
    WorkIntelligenceError,
    _validate_scope_language,
)


def _candidate(rationale: str) -> CandidateJobWorkIntelligence:
    return CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Network security design",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale=rationale,
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )


def test_scope_guard_rejects_unsupported_end_to_end_language() -> None:
    candidate = _candidate(
        "This groups the work as end-to-end network security design and implementation."
    )

    with pytest.raises(WorkIntelligenceError, match="unsupported lifecycle/scope intensifier"):
        _validate_scope_language(
            candidate,
            responsibilities=[
                {"statement": "Designing and implementing network security architecture"}
            ],
            role_purpose=[],
        )


def test_scope_guard_allows_explicit_source_scope_language_across_hyphenation() -> None:
    candidate = _candidate(
        "This groups the accepted end-to-end network security implementation work."
    )

    _validate_scope_language(
        candidate,
        responsibilities=[
            {"statement": "Providing end to end network security implementation"}
        ],
        role_purpose=[],
    )


def test_representation_redesign_uses_new_prompt_and_schema_identity() -> None:
    assert WORK_INTELLIGENCE_PROMPT_VERSION == "job-work-intelligence-v2.0"
    assert WORK_INTELLIGENCE_SCHEMA_VERSION == "job-work-intelligence-v2"
