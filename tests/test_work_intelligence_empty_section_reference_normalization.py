from __future__ import annotations

import pytest

from jobhunter.work_intelligence_models import JobWorkIntelligence, WorkTheme
from jobhunter.work_intelligence_service import WorkIntelligenceError, WorkIntelligenceService


def _document(*, responsibility_indices: list[int], role_purpose_indices: list[int]) -> JobWorkIntelligence:
    return JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary="The role groups accepted direct work into one bounded candidate theme.",
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Candidate work theme",
                summary="Group the accepted direct work without inventing additional source claims.",
                emphasis="primary",
                confidence="high",
                responsibility_indices=responsibility_indices,
                role_purpose_indices=role_purpose_indices,
                supporting_requirement_indices=[],
                rationale="The theme is linked only through structured direct-work references.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )


def test_empty_role_purpose_reference_is_removed_when_responsibility_support_remains() -> None:
    document = _document(responsibility_indices=[0], role_purpose_indices=[1])

    WorkIntelligenceService._validate_references(
        document,
        responsibility_count=1,
        role_purpose_count=0,
        requirement_count=0,
    )

    assert document.work_themes[0].responsibility_indices == [0]
    assert document.work_themes[0].role_purpose_indices == []


def test_empty_section_normalization_does_not_create_unsupported_theme() -> None:
    document = _document(responsibility_indices=[], role_purpose_indices=[1])

    with pytest.raises(WorkIntelligenceError, match="no valid direct work references"):
        WorkIntelligenceService._validate_references(
            document,
            responsibility_count=1,
            role_purpose_count=0,
            requirement_count=0,
        )


def test_nonempty_role_purpose_section_still_rejects_out_of_range_reference() -> None:
    document = _document(responsibility_indices=[0], role_purpose_indices=[1])

    with pytest.raises(WorkIntelligenceError, match="missing role-purpose indices"):
        WorkIntelligenceService._validate_references(
            document,
            responsibility_count=1,
            role_purpose_count=1,
            requirement_count=0,
        )
