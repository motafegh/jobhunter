"""Offline evidence gates for an isolated proof-of-ability P1.6 candidate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_runtime_v23 import V23CandidateAnalysisProvider
from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.analysis_service_v23 import (
    _ENGLISH_SYSTEM_PROMPT_V23,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs_v21 import build_requirement_coverage_plan_v21
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio_v23 import (
    AnalysisRequirementV23,
    JobAnalysisResponseV23,
    complete_analysis_partition_with_instructor_v23,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_ROOT = Path(__file__).resolve().parents[1]
_ANCHORS = ("tG9K", "t4jp", "tmBK", "t4qV", "tmyX")


def _fields(job_id: str):
    data = json.loads(
        (_ROOT / "corpus" / "jobs" / job_id / "english-projection.json").read_text()
    )
    return _analysis_fields_for_english(data["fields"])


def _proof(job_id: str):
    return {
        ref: item
        for ref, item in build_requirement_coverage_plan_v23(_fields(job_id)).items()
        if item.get("source_kind") == "candidate_proof"
    }


def test_explicit_proof_preferences_are_exact_and_preferred() -> None:
    tvmm = _proof("tvMm")
    assert len(tvmm) == 3
    demonstration = next(item["text"] for item in tvmm.values()
                         if "huge plus" in item["text"])
    assert "What problem did the Agent solve?" in demonstration
    assert "How did it make decisions?" in demonstration
    assert "What Tools did it have access to?" in demonstration
    assert "How did you manage Context and Memory?" in demonstration
    assert "How did you measure the quality and cost of the system?" in demonstration
    assert any("repository, sample project, or Demo" in item["text"] for item in tvmm.values())
    assert _proof("tjgi") == {}  # "At least one" is qualification strength, not preference.
    description = _fields("tvMm")["description"]
    for item in tvmm.values():
        assert item["text"] in description
        assert item["obligation_hint"] == "preferred"
        assert item["allow_exclusion"] is False
        assert item["required_item_excerpts"] == [
            {"text": item["text"], "required_concept_type": None}
        ]


def test_submission_only_cases_never_become_proof_requirements() -> None:
    for job_id in ("tI1n", "takb", "tm4I", "tGc5"):
        assert _proof(job_id) == {}
    assert _proof("taOX") == {}  # Already covered by v21 with preferred strength.
    existing = build_requirement_coverage_plan_v21(_fields("taOX"))
    assert any(
        "Submitting samples of work" in item["text"]
        and item["obligation_hint"] == "preferred"
        for item in existing.values()
    )


def test_accepted_anchor_plans_and_all_current_projection_sources_remain_stable() -> None:
    for job_id in _ANCHORS:
        fields = _fields(job_id)
        assert build_requirement_coverage_plan_v23(fields) == (
            build_requirement_coverage_plan_v21(fields)
        )
    projections = sorted((_ROOT / "corpus" / "jobs").glob("*/english-projection.json"))
    assert projections
    for path in projections:
        fields = _fields(path.parent.name)
        plan = build_requirement_coverage_plan_v23(fields)
        description = fields["description"]
        proof = [item for item in plan.values() if item.get("source_kind") == "candidate_proof"]
        assert len({item["text"] for item in proof}) == len(proof)
        assert all(item["text"] in description for item in proof)


def test_v23_proof_partition_is_separate_and_public_contract_is_v23() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tvMm"))
    provider = object.__new__(V23CandidateAnalysisProvider)
    partitions = provider._requirement_partitions(plan)
    proof_refs = {ref for ref, item in plan.items() if item.get("source_kind") == "candidate_proof"}
    assert len(proof_refs) == 3
    assert any(set(partition) == proof_refs for partition in partitions)
    assert all(not (set(partition) & proof_refs) or set(partition) == proof_refs
               for partition in partitions)
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v23"
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert "candidate_proof" in _ENGLISH_SYSTEM_PROMPT_V23


def test_v23_transport_keeps_v22_fact_guard_and_versioned_request(monkeypatch) -> None:
    captured = {}

    def shared_transport(**kwargs):
        captured.update(kwargs)
        return StructuredInferenceResult(
            model="offline", structured={}, request_body={}, raw_response={},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.inference.instructor_lm_studio_v20."
        "_complete_analysis_partition_with_instructor", shared_transport,
    )
    result = complete_analysis_partition_with_instructor_v23(
        base_url="http://127.0.0.1:18080/v1", api_token=None,
        timeout_seconds=10, network_retries=0, selected_model="offline",
        system_prompt=_ENGLISH_SYSTEM_PROMPT_V23,
        user_payload={"analysis_fields": {"description": "A demo is very valuable."}},
        max_tokens=1024, seed=0,
        requirement_coverage_plan={
            "proof": {
                "text": "A demo is very valuable.",
                "source_kind": "candidate_proof", "obligation_hint": "preferred",
                "allow_exclusion": False,
                "required_item_excerpts": [
                    {"text": "A demo is very valuable.", "required_concept_type": None}
                ],
            }
        }, responsibility_coverage_plan={},
    )
    assert captured["response_model"] is JobAnalysisResponseV23
    assert captured["contract_version"] == "v23"
    assert captured["user_payload"]["exact_item_coverage"] == [
        {"parent_reference": "proof", "item_excerpt": "A demo is very valuable.",
         "required_concept_type": None}
    ]
    assert result.request_body["runtime"]["p16_v23_candidate_proof_coverage"] is True


@pytest.mark.parametrize("job_id,needle", [
    ("tvMm", "very valuable"),
    ("tvMm", "more valuable"),
])
def test_v23_accepts_exact_source_preference_only_for_proof_ref(
    job_id: str, needle: str,
) -> None:
    proof = _proof(job_id)
    candidate = next(item for item in proof.values() if needle in item["text"])
    excerpt = candidate["text"]
    requirement = {
        "concept": "Candidate work demonstration",
        "depth_signal": None,
        "requirement_type": "preferred",
        "concept_type": "other",
        "evidence": excerpt,
        "item_excerpt": excerpt,
        "confidence": "high",
        "rationale": "Explicit source preference.",
    }
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": _fields(job_id)["description"]},
        "evidence_catalog": {},
        "requirement_coverage_plan": {"proof": candidate},
    }
    result = AnalysisRequirementV23.model_validate(requirement, context=context)
    assert result.requirement_type == "preferred"

    context["requirement_coverage_plan"] = {
        "ordinary": {**candidate, "source_kind": "requirement_section"}
    }
    with pytest.raises(ValidationError, match="Preferred item needs exact"):
        AnalysisRequirementV23.model_validate(requirement, context=context)


def test_proof_followup_questions_keep_exact_source_whitespace() -> None:
    description = (
        "It would be a plus if you could show a sample project: What did it do?\n"
        "How did you evaluate it? A demo is very valuable."
    )
    proof = build_requirement_coverage_plan_v23({"description": description})
    excerpts = [item["text"] for item in proof.values()
                if item.get("source_kind") == "candidate_proof"]
    assert excerpts[0] == (
        "It would be a plus if you could show a sample project: What did it do?\n"
        "How did you evaluate it?"
    )
    assert all(excerpt in description for excerpt in excerpts)
