"""P2.3B fact-versus-proposal boundary acceptance for bounded capability briefs."""

from __future__ import annotations

import pytest
from test_job_comparison import _rows, _seed

from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.capability_expectations import (
    ProposedInterpretation,
    build_capability_expectation_brief,
    compose_expectation_brief,
    decode_candidate_json,
    format_expectation_brief,
    validate_interpretation_proposals,
)
from jobhunter.config import Settings
from jobhunter.job_comparison import ComparisonJob, ComparisonOption


@pytest.fixture
def settings(tmp_path):
    return Settings(
        data_dir=tmp_path, evidence_dir=tmp_path / "evidence",
        database_path=tmp_path / "test.sqlite3", translation_enabled=False,
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
    )


def _claim(
    kind: str, index: int, statement: str, strength: str | None = None,
    depth: str | None = None,
) -> CanonicalClaimReviewItem:
    return CanonicalClaimReviewItem(
        analysis_artifact_id=50,
        source_job_id="example",
        job_detail_version_id=3,
        translation_artifact_id=4,
        claim_kind=kind,
        claim_index=index,
        source_text=statement,
        evidence=statement,
        concept_type="tool" if kind == "requirement" else None,
        strength=strength,
        depth_signal=depth,
        mapping=None,
    )


def _job(*claims: CanonicalClaimReviewItem) -> ComparisonJob:
    return ComparisonJob(
        option=ComparisonOption("example", "Engineer", "Example"),
        claims=claims,
        matching_claims=claims,
        groups=(),
        grouping_notice="No Capability v9 overlay.",
        capability_artifact_id=None,
    )


def test_brief_keeps_disjunctive_requirement_scope_and_direct_work_separate() -> None:
    req = _claim(
        "requirement", 4, "LLM Application, RAG, or AI Agent project", "required"
    )
    duty = _claim("responsibility", 6, "Developing RAG systems")
    result = compose_expectation_brief(_job(req, duty), "RAG")
    assert result.contract == "job-capability-expectation-candidate-v0"
    assert result.matched_claim_count == 2
    assert result.source_requirements[0].strength == "required"
    assert result.source_requirements[0].potential_alternatives is True
    assert result.source_responsibilities[0].strength is None
    assert result.source_responsibilities[0].statement == duty.source_text
    assert any(q.kind == "alternative_scope" for q in result.questions)
    assert any(q.kind == "direct_work_demonstration" for q in result.questions)
    text = format_expectation_brief(result)
    assert "Potential alternatives: review required" in text
    assert "Claim strength" in text
    assert "entire statement" in text


def test_requirement_only_case_cannot_become_a_work_duty() -> None:
    req = _claim(
        "requirement", 0,
        "Practical experience designing and implementing RAG systems", "required",
    )
    result = compose_expectation_brief(_job(req), "RAG")
    assert result.source_responsibilities == ()
    assert any(q.kind == "missing_work_scope" for q in result.questions)
    assert "No matching direct duty" in format_expectation_brief(result)
    implied = ProposedInterpretation(
        "You must deploy RAG in production", "strongly_implied_by_work", "high",
        (result.source_requirements[0].ref,), "Required RAG experience",
    )
    with pytest.raises(ValueError, match="requires directly supported work"):
        validate_interpretation_proposals(result, (implied,))


def test_prerequisites_need_non_alternative_required_evidence() -> None:
    preferred = compose_expectation_brief(
        _job(_claim("requirement", 1, "RAG exposure preferred", "preferred")), "RAG"
    )
    proposal = ProposedInterpretation(
        "Retrieval knowledge could be a prerequisite", "model_inferred_prerequisite",
        "low", (preferred.source_requirements[0].ref,), "Candidate reasoning",
    )
    with pytest.raises(ValueError, match="non-alternative required"):
        validate_interpretation_proposals(preferred, (proposal,))
    alternative = compose_expectation_brief(
        _job(_claim("requirement", 1, "RAG or LLM Application", "required")), "RAG"
    )
    with pytest.raises(ValueError, match="non-alternative required"):
        validate_interpretation_proposals(
            alternative,
            (ProposedInterpretation(
                proposal.text, proposal.status, proposal.confidence,
                (alternative.source_requirements[0].ref,), proposal.rationale,
            ),),
        )


def test_candidate_invalid_references_fail_without_rewriting_source() -> None:
    result = compose_expectation_brief(
        _job(_claim("responsibility", 2, "Develop RAG systems")), "RAG"
    )
    with pytest.raises(ValueError, match="unselected or stale"):
        validate_interpretation_proposals(result, (
            ProposedInterpretation(
                "Investigate retrieval architecture", "strongly_implied_by_work",
                "medium", ("999:responsibility:1",), "Unsupported reference",
            ),
        ))
    valid = ProposedInterpretation(
        "A candidate work implication to inspect", "strongly_implied_by_work",
        "low", (result.source_responsibilities[0].ref,), "Tied to explicit duty",
    )
    assert validate_interpretation_proposals(result, (valid,)) == (valid,)
    assert result.source_responsibilities[0].statement == "Develop RAG systems"


def test_real_reader_composes_read_only_without_running_models(settings) -> None:
    _seed(settings, "direct")
    _seed(settings, "no-duty", responsibilities=False)
    initial = build_capability_expectation_brief(settings, "direct", "Python")
    before = _rows(settings)
    direct = build_capability_expectation_brief(settings, "direct", "Python")
    none = build_capability_expectation_brief(settings, "no-duty", "Python")
    assert direct.source_responsibilities
    assert none.source_responsibilities == ()
    assert direct.source_requirements[0].explicit_depth == "proficiency"
    assert direct.source_requirements[0].strength == "required"
    assert direct.accepted_claim_count == 3
    assert initial == direct
    assert _rows(settings) == before


def test_invalid_or_unavailable_selection_has_no_fact_fabrication(settings) -> None:
    _seed(settings, "rejected", status="rejected")
    with pytest.raises(ValueError, match="No accepted/current"):
        build_capability_expectation_brief(settings, "rejected", "Python")
    with pytest.raises(ValueError, match="nonempty capability"):
        compose_expectation_brief(
            _job(_claim("requirement", 0, "Python required")), ""
        )


def test_local_model_decoder_accepts_one_fenced_json_object_only() -> None:
    assert decode_candidate_json('{"proposals": []}') == {"proposals": []}
    assert decode_candidate_json(
        "```json\n{\"proposals\": []}\n```"
    ) == {"proposals": []}
    with pytest.raises(ValueError):
        decode_candidate_json('here is advice: {"proposals": []}')
    with pytest.raises(ValueError):
        decode_candidate_json("[]")


def test_fact_links_point_to_exact_compare_claim_anchors() -> None:
    result = compose_expectation_brief(
        _job(_claim("responsibility", 6, "Developing RAG systems")), "RAG"
    )
    ref = result.source_responsibilities[0]
    assert ref.exact_claim_url == "/compare?job=example#claim-50-responsibility-6"
    assert ref.job_source_url == "/jobs/example#english-analysis"
    assert ref.exact_claim_url in format_expectation_brief(result)
