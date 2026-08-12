from jobhunter.analysis_runtime_v12 import _candidate_evidence_view
from jobhunter.analysis_service_v12 import (
    ENGLISH_PROMPT_VERSION,
    validate_v12_candidate_structured,
)
from jobhunter.evidence_refs import build_field_evidence_catalog


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


def test_v12_has_distinct_artifact_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v12"


def test_v12_candidate_spans_become_normal_evidence_references() -> None:
    fields = _fields()
    effective_fields, references = _candidate_evidence_view(fields)
    catalog = build_field_evidence_catalog(effective_fields)

    assert fields == _fields()
    assert references == [
        "field:__candidate_qualification_evidence:0",
        "field:__candidate_qualification_evidence:1",
        "field:__candidate_qualification_evidence:2",
        "field:__candidate_qualification_evidence:3",
    ]
    assert [catalog[reference] for reference in references] == [
        "Skills in content creation with AI",
        "creativity in creating visual and video content",
        "website design",
        "ability to produce visual content full-time and part-time",
    ]


def test_v12_evidence_aliases_add_no_new_source_text() -> None:
    fields = _fields()
    effective_fields, references = _candidate_evidence_view(fields)
    catalog = build_field_evidence_catalog(effective_fields)
    description = fields["description"]

    assert all(catalog[reference] in description for reference in references)


def test_v12_semantics_accept_exact_canonicalized_evidence() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement("Artificial Intelligence"),
            _requirement("Video content production"),
            _requirement("social networks"),
            _requirement("Skills in content creation with AI"),
            _requirement("creativity in creating visual and video content"),
            _requirement("website design"),
            _requirement("ability to produce visual content full-time and part-time"),
        ],
        "coverage_exclusions": [],
    }

    validate_v12_candidate_structured(structured, _fields())
