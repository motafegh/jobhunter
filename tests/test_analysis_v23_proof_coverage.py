"""Offline evidence gates for an isolated proof-of-ability P1.6 candidate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_runtime_v15 import _v15_candidate_evidence_view
from jobhunter.analysis_runtime_v23 import (
    V23CandidateAnalysisProvider,
    _remove_duplicate_residual_ownership,
    _scoped_preferred_qualification_plan,
)
from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.analysis_service_v23 import (
    _ENGLISH_SYSTEM_PROMPT_V23,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs import requirement_coverage_payload
from jobhunter.evidence_refs_v21 import build_requirement_coverage_plan_v21
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio_v23 import (
    AnalysisRequirementV23,
    AnalysisResponsibilityV23,
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


def test_v23_scopes_preferred_list_strength_to_exact_source_sentence() -> None:
    fields = _fields("t7ck")
    _effective, refs, _residuals, additional = _v15_candidate_evidence_view(fields)
    scoped = _scoped_preferred_qualification_plan(fields, additional)
    by_text = {item["text"]: item for ref, item in scoped.items() if ref in refs}

    assert by_text["Proficiency in Python"]["obligation_hint"] == "required"
    for text in ("Experience in Streaming Audio", "Real-Time Voice", "VAD", "Voice Cloning"):
        assert by_text[text]["obligation_hint"] == "preferred"
        assert by_text[text]["obligation_context"].endswith("an important asset.")
    assert any(
        entry.get("obligation_context", "").endswith("an important asset.")
        for entry in requirement_coverage_payload(scoped)
    )

    item = by_text["Real-Time Voice"]
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": fields["description"]},
        "evidence_catalog": {},
        "requirement_coverage_plan": {"item": item},
    }
    requirement = {
        "concept": "Real-Time Voice",
        "depth_signal": None,
        "requirement_type": "preferred",
        "concept_type": "skill",
        "evidence": "Real-Time Voice",
        "item_excerpt": "Real-Time Voice",
        "confidence": "high",
        "rationale": "Exact qualification in a preferred source sentence.",
    }
    assert AnalysisRequirementV23.model_validate(
        requirement, context=context
    ).requirement_type == "preferred"
    with pytest.raises(ValidationError, match="Preferred parent coverage"):
        AnalysisRequirementV23.model_validate(
            {**requirement, "requirement_type": "required"}, context=context
        )


def test_v23_keeps_preferred_heading_context_for_separate_bullets() -> None:
    fields = _fields("tjgi")
    plan = build_requirement_coverage_plan_v23(fields)
    candidate = next(
        item for item in plan.values()
        if item["text"] == "Experience building AI Agents or LLM-based tools"
    )
    assert candidate["obligation_hint"] == "preferred"
    assert candidate["obligation_context"] == "Score is given for"
    requirement = {
        "concept": "Building AI Agents or LLM-based tools",
        "depth_signal": None,
        "requirement_type": "preferred",
        "concept_type": "experience",
        "evidence": candidate["text"],
        "item_excerpt": candidate["text"],
        "confidence": "high",
        "rationale": "Source heading gives this item preference strength.",
    }
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": fields["description"]},
        "evidence_catalog": {},
        "requirement_coverage_plan": {"preferred_item": candidate},
    }
    assert AnalysisRequirementV23.model_validate(
        requirement, context=context
    ).requirement_type == "preferred"


def test_v23_exact_candidate_fact_owns_identical_residual_sentence() -> None:
    fields = _fields("t7ck")
    effective, _quals, residuals, additional = _v15_candidate_evidence_view(fields)
    base = build_requirement_coverage_plan_v23(effective)
    filtered = _remove_duplicate_residual_ownership(additional, base)

    assert len(residuals) == 4
    assert len([ref for ref in residuals if ref in filtered]) == 3
    removed = next(ref for ref in residuals if ref not in filtered)
    assert "ability to research, test" in additional[removed]["text"]
    assert any(
        item["text"] == additional[removed]["text"]
        and item["allow_exclusion"] is False
        for item in base.values()
    )


def test_v23_separates_required_criteria_from_hiring_priority() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("t7Ay"))
    relevant = [
        item for item in plan.values()
        if "most important criteria" in item["text"].lower()
        or "prioritized in the recruitment process" in item["text"]
    ]

    assert len(relevant) == 2
    assert {item["obligation_hint"] for item in relevant} == {"required", "preferred"}
    assert all(
        not (
            "most important criteria" in item["text"].lower()
            and "prioritized in the recruitment process" in item["text"]
        )
        for item in relevant
    )
    assert any(
        "Submitting samples of work" in item["text"]
        and item["obligation_hint"] == "preferred"
        for item in plan.values()
    )


def test_v23_preferred_heading_is_context_not_a_qualification() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tjgi"))
    assert not any(item["text"] == "Score is given for" for item in plan.values())
    preferred = [
        item for item in plan.values()
        if item.get("obligation_context") == "Score is given for"
    ]
    assert len(preferred) == 5
    assert all(item["obligation_hint"] == "preferred" for item in preferred)


def test_v23_dense_lists_require_every_exact_qualification_item() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tNVe"))
    essential = next(
        item for item in plan.values()
        if item["text"].startswith("practical mastery of TypeScript")
    )
    preferred = next(
        item for item in plan.values()
        if item["text"].startswith("Points are also awarded for")
    )

    assert [item["text"] for item in essential["required_item_excerpts"]] == [
        "practical mastery of TypeScript and Node.js",
        "experience working with NestJS, Express, or similar frameworks",
        "a good understanding of Backend, APIs, and service architecture",
        "practical experience working with LLM APIs such as OpenAI, Anthropic, or similar services",
        "real-world experience in at least one LLM Application, RAG, or AI Agent project",
        "practical familiarity with Tool / Function Calling and Structured Output",
        "understanding of Embedding, Retrieval, Chunking, and Context Management",
        "familiarity with SQL or NoSQL databases",
        "familiarity with Git",
        "and the ability to debug and solve problems independently are considered points",
    ]
    assert [item["text"] for item in preferred["required_item_excerpts"]] == [
        "experience developing AI systems in a Production environment",
        "experience with OpenAI Agents SDK, LangGraph, LangChain, or similar tools",
        "experience with Multi-Agent Systems and LLM Evaluation",
        "familiarity with Vector Search, Redis, and Queue",
        "experience integrating with ERP, CRM, Email, or Ticketing Systems",
        "familiarity with Docker, CI/CD, WebSocket, or Python",
        "and a relevant educational background in Computer Science or Software Engineering",
    ]
    for parent in (essential, preferred):
        assert all(item["text"] in parent["text"] for item in parent["required_item_excerpts"])
        for item in parent["required_item_excerpts"]:
            expected_type = "experience" if item["text"].startswith((
                "experience ", "practical experience ", "real-world experience "
            )) else None
            assert item["required_concept_type"] == expected_type


def test_v23_points_preference_applies_only_to_its_exact_item() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tNVe"))
    parent = next(
        item for item in plan.values()
        if item["text"].startswith("practical mastery of TypeScript")
    )
    assert parent["obligation_hint"] == "required"
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": _fields("tNVe")["description"]},
        "evidence_catalog": {},
        "requirement_coverage_plan": {"parent": parent},
    }
    requirement = {
        "concept": "independent debugging",
        "depth_signal": None,
        "requirement_type": "preferred",
        "concept_type": "skill",
        "evidence": parent["text"],
        "item_excerpt": parent["required_item_excerpts"][-1]["text"],
        "confidence": "high",
        "rationale": "The exact item says it is considered points.",
    }
    assert AnalysisRequirementV23.model_validate(
        requirement, context=context
    ).requirement_type == "preferred"
    with pytest.raises(ValidationError, match="Preferred item needs exact source preference"):
        AnalysisRequirementV23.model_validate(
            {**requirement, "item_excerpt": parent["required_item_excerpts"][0]["text"]},
            context=context,
        )


def test_v23_keeps_at_least_one_language_alternative() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tjgi"))
    parent = next(
        item for item in plan.values()
        if item["text"].startswith("Programming experience with at least one of")
    )
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": _fields("tjgi")["description"]},
        "evidence_catalog": {},
        "requirement_coverage_plan": {"parent": parent},
    }
    requirement = {
        "concept": "Programming experience with Python or JavaScript/TypeScript",
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "experience",
        "evidence": parent["text"],
        "item_excerpt": parent["text"],
        "confidence": "high",
        "rationale": "At least one of the source languages is required.",
    }
    assert AnalysisRequirementV23.model_validate(
        requirement, context=context
    ).requirement_type == "required"
    normalized = AnalysisRequirementV23.model_validate(
        {**requirement, "concept": "Programming experience with Python"},
        context=context,
    )
    assert normalized.concept == parent["text"]


def test_v23_source_alternative_fallback_keeps_preferred_choices() -> None:
    plan = build_requirement_coverage_plan_v23(_fields("tjgi"))
    cases = (
        ("Familiarity with Docker, Linux, or cloud services", "Docker, Linux, and cloud services",
         "Docker, Linux, or cloud services"),
        ("Experience deploying projects and having GitHub or an online demo",
         "Deploying projects", "Experience deploying projects and having GitHub or an online demo"),
    )
    for source, model_concept, expected in cases:
        parent = next(item for item in plan.values() if item["text"] == source)
        context = {
            "analysis_mode": "english",
            "analysis_fields": {"description": _fields("tjgi")["description"]},
            "evidence_catalog": {},
            "requirement_coverage_plan": {"parent": parent},
        }
        requirement = {
            "concept": model_concept,
            "depth_signal": "Familiarity" if source.startswith("Familiarity") else None,
            "requirement_type": "preferred",
            "concept_type": "tool" if source.startswith("Familiarity") else "experience",
            "evidence": source,
            "item_excerpt": source,
            "confidence": "high",
            "rationale": "Exact preferred source item.",
        }
        normalized = AnalysisRequirementV23.model_validate(requirement, context=context)
        assert normalized.concept == expected


def test_v23_preserves_explicit_condition_on_employer_work() -> None:
    evidence = (
        "developing multi-step workflows, and if necessary, Multi-Agent Integration "
        "with Email, Ticketing, and other system modules"
    )
    context = {
        "analysis_mode": "english",
        "analysis_fields": {"description": _fields("tNVe")["description"]},
        "evidence_catalog": {},
        "responsibility_coverage_plan": {"duty": evidence},
    }
    claim = {
        "statement": (
            "Develop multi-step workflows and Multi-Agent Integration "
            "with Email and Ticketing"
        ),
        "evidence": evidence,
        "confidence": "high",
    }
    with pytest.raises(ValidationError, match="preserve explicit source condition"):
        AnalysisResponsibilityV23.model_validate(claim, context=context)
    accepted = AnalysisResponsibilityV23.model_validate(
        {
            **claim,
            "statement": (
                "Develop multi-step workflows and, if necessary, Multi-Agent "
                "Integration with Email and Ticketing"
            ),
        },
        context=context,
    )
    assert "if necessary" in accepted.statement
    AnalysisResponsibilityV23.model_validate(
        {**claim, "evidence": "developing multi-step workflows"},
        context={
            **context,
            "responsibility_coverage_plan": {"duty": "developing multi-step workflows"},
        },
    )


def test_v23_discards_extra_work_claim_outside_partition(monkeypatch) -> None:
    assigned = {"statement": "Build AI agents", "evidence": "Build AI agents", "confidence": "high"}
    extra = {
        "statement": "Make useful products",
        "evidence": "We build useful products",
        "confidence": "high",
    }
    result = StructuredInferenceResult(
        model="test",
        structured={
            "role_purpose": [extra],
            "responsibilities": [assigned, extra],
            "requirements": [],
            "coverage_exclusions": [],
        },
        request_body={"runtime": {"contract": "v23"}},
        raw_response={"original": "retained"},
        finish_reason="stop",
    )
    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v23.complete_analysis_partition_with_instructor_v23",
        lambda **_kwargs: result,
    )
    provider = object.__new__(V23CandidateAnalysisProvider)
    filtered = provider._complete_partition(
        responsibility_coverage_plan={"duty": "Build AI agents"}
    )
    assert filtered.structured["role_purpose"] == []
    assert filtered.structured["responsibilities"] == [assigned]
    assert filtered.structured["requirements"] == []
    assert filtered.raw_response == result.raw_response
    assert filtered.request_body["runtime"]["p16_v23_dropped_unassigned_work_claims"] == 2


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
