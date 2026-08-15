from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.capability_v7_inference_models import CapabilityReasoningDraft


def _accepted_extraction() -> dict:
    return {
        "role_purpose": [],
        "requirements": [
            {
                "concept": "Python",
                "concept_type": "skill",
                "requirement_type": "required",
                "depth_signal": None,
                "evidence": "Python",
                "confidence": "high",
            },
            {
                "concept": "SQL",
                "concept_type": "tool",
                "requirement_type": "contextual",
                "depth_signal": None,
                "evidence": "SQL",
                "confidence": "high",
            },
        ],
        "responsibilities": [
            {
                "statement": "Build models",
                "evidence": "Build models",
                "confidence": "high",
            },
            {
                "statement": "Ensure traceability",
                "evidence": "Ensure traceability",
                "confidence": "high",
            },
        ],
    }


def _context() -> dict:
    return {
        "analysis_fields": {
            "description": "Python SQL Build models Ensure traceability",
        },
        "evidence_catalog": {},
        "accepted_extraction": _accepted_extraction(),
    }


def _profile(*, recover_missing: bool, responsibility_indices: list[int]) -> dict:
    derived_items = [
        {
            "statement": "Python-based model implementation",
            "evidence_status": "strongly_implied_by_work",
            "evidence": ["Python"],
            "rationale": "Python supports implementation work.",
            "confidence": "high",
        }
    ]
    if recover_missing:
        derived_items.extend(
            [
                {
                    "statement": "SQL-backed data access",
                    "evidence_status": "strongly_implied_by_work",
                    "evidence": ["SQL"],
                    "rationale": "SQL supports data access work.",
                    "confidence": "high",
                },
                {
                    "statement": "Traceable model operations",
                    "evidence_status": "strongly_implied_by_work",
                    "evidence": ["Ensure traceability"],
                    "rationale": "Traceability evidence supports this operational expectation.",
                    "confidence": "high",
                },
            ]
        )
    return {
        "capability_label": "Applied model engineering",
        "summary": "Applies programming and operational practices to model delivery.",
        "source_requirement_indices": [0],
        "source_responsibility_indices": responsibility_indices,
        "requirement_strength": "unspecified",
        "depth_signals": [],
        "work_activities": [],
        "sub_capabilities": derived_items,
        "underlying_knowledge": [],
        "operational_practices": [],
        "independence_expectation": None,
        "operational_context": [],
        "unknown_scope": [],
        "overall_confidence": "high",
    }


def _draft(profile: dict) -> dict:
    return {
        "role_interpretation": "Applied model engineering role.",
        "capabilities": [profile],
        "cross_capability_observations": [],
        "uncertainties": [],
    }


def test_inference_repairs_out_of_range_index_from_exact_grounded_evidence() -> None:
    validated = CapabilityReasoningDraft.model_validate(
        _draft(
            _profile(
                recover_missing=True,
                responsibility_indices=[0, 9],
            )
        ),
        context=_context(),
    )

    profile = validated.capabilities[0]
    assert profile.source_requirement_indices == [0, 1]
    assert profile.source_responsibility_indices == [0, 1]


def test_inference_still_fails_when_missing_coverage_has_no_profile_evidence() -> None:
    with pytest.raises(
        ValidationError,
        match="omitted capability-relevant accepted P1.6 requirements",
    ):
        CapabilityReasoningDraft.model_validate(
            _draft(
                _profile(
                    recover_missing=False,
                    responsibility_indices=[0, 9],
                )
            ),
            context=_context(),
        )


def test_inference_does_not_normalize_negative_source_indices() -> None:
    with pytest.raises(ValidationError, match="indices must be zero or positive"):
        CapabilityReasoningDraft.model_validate(
            _draft(
                _profile(
                    recover_missing=True,
                    responsibility_indices=[-1, 0],
                )
            ),
            context=_context(),
        )
