import pytest

from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import (
    ENGLISH_PROMPT_VERSION,
    _persisted_analysis_v13,
    _validate_evidence_v13,
    decomposed_requirement_references,
    inject_decomposition_exclusions,
    qualification_list_spans,
    validate_v13_candidate_structured,
)
from jobhunter.inference.base import InferenceResponseError
from jobhunter.inference.instructor_lm_studio_v13 import filtered_requirement_coverage_plan


def _fields():
    return {
        "description": (
            "Skills in content creation with AI, creativity in creating visual and video content, "
            "website design, ability to produce visual content full-time and part-time, "
            "the work is teachable. Ethics and work commitment are important."
        ),
        "skills": ["Artificial Intelligence", "Video content production", "social networks"],
    }


def _requirement(evidence: str, concept: str | None = None):
    return {
        "concept": concept or evidence,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Explicit source qualification.",
    }


def _valid_structured():
    fields = _fields()
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
            _requirement("social networks"),
            *[_requirement(span) for span in qualification_list_spans(fields)],
        ],
        "coverage_exclusions": [],
    }
    return inject_decomposition_exclusions(structured, fields)


def test_v13_has_distinct_artifact_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v13"


def test_v13_detects_only_coarse_excludable_requirement_span() -> None:
    assert decomposed_requirement_references(_fields()) == [
        "field:description:segment:0"
    ]


def test_v13_injects_decomposition_bookkeeping_deterministically() -> None:
    structured = inject_decomposition_exclusions(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [],
            "coverage_exclusions": [],
        },
        _fields(),
    )
    assert structured["coverage_exclusions"] == [
        {
            "evidence_reference": "field:description:segment:0",
            "rationale": (
                "JobHunter deterministically decomposed this coarse requirement span into "
                "exact item-level qualification requirements."
            ),
        }
    ]


def test_v13_candidate_instructor_filters_decomposed_coarse_coverage() -> None:
    filtered = filtered_requirement_coverage_plan(
        _fields(), decomposed_requirement_references(_fields())
    )
    assert "field:description:segment:0" not in filtered


def test_v13_candidate_instructor_refuses_non_excludable_suppression() -> None:
    fields = {**_fields(), "education": "Master's degree"}
    with pytest.raises(InferenceResponseError, match="non-excludable"):
        filtered_requirement_coverage_plan(fields, ["field:education"])


def test_v13_validates_after_deterministic_bookkeeping_injection() -> None:
    validate_v13_candidate_structured(_valid_structured(), _fields())


def test_v13_persistence_marks_coarse_span_as_decomposed_requirement() -> None:
    analysis = _persisted_analysis_v13(_valid_structured(), _fields())
    decomposed = [
        item
        for item in analysis["coverage"]
        if item["disposition"] == "decomposed_requirement"
    ]
    assert len(decomposed) == 1
    assert "creativity in creating visual and video content" in decomposed[0]["evidence"]
    extracted = {
        item["evidence"]
        for item in analysis["coverage"]
        if item["disposition"] == "extracted_requirement"
    }
    assert set(qualification_list_spans(_fields())).issubset(extracted)
    assert {"Artificial Intelligence", "Video content production", "social networks"}.issubset(
        extracted
    )


def test_v13_final_evidence_guard_accepts_deterministic_decomposition() -> None:
    analysis = _persisted_analysis_v13(_valid_structured(), _fields())
    _validate_evidence_v13(analysis, _fields())


def test_v13_final_evidence_guard_rejects_fake_decomposition() -> None:
    analysis = _persisted_analysis_v13(_valid_structured(), _fields())
    decomposed = next(
        item for item in analysis["coverage"] if item["disposition"] == "decomposed_requirement"
    )
    decomposed["evidence"] = "Ethics and work commitment are important."
    with pytest.raises(AnalysisValidationError, match="non-deterministic"):
        _validate_evidence_v13(analysis, _fields())
