"""Exact qualification ownership for the isolated v24 candidate."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_runtime_v14 import _v14_candidate_evidence_view
from jobhunter.analysis_runtime_v20 import _v20_complete_requirement_plan
from jobhunter.analysis_runtime_v24 import (
    V24CandidateAnalysisProvider,
    _exact_qualification_item_plan,
)
from jobhunter.analysis_service_v24 import ENGLISH_PROMPT_VERSION, JobAnalysisServiceV24
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.evidence_refs_v24 import persisted_qualification_plan
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_ROOT = Path(__file__).resolve().parents[1]


def test_v24_exact_items_own_three_redundant_tmvA_sentences() -> None:
    fields = json.loads(
        (_ROOT / "corpus/jobs/tmvA/english-projection.json").read_text(encoding="utf-8")
    )["fields"]
    effective, qualification_refs, _, additional = _v14_candidate_evidence_view(fields)
    provider = object.__new__(V24CandidateAnalysisProvider)
    plan = provider._requirement_coverage_plan(effective)
    redundant = {
        "field:description:segment:3:sentence:2",
        "field:description:segment:3:sentence:4",
        "field:description:segment:3:sentence:6",
    }
    assert redundant <= build_requirement_coverage_plan_v23(effective).keys()
    assert redundant.isdisjoint(plan)
    persisted = persisted_qualification_plan(fields)
    assert set(plan) <= set(persisted)
    assert "field:__candidate_residual_requirement_evidence:12" in persisted
    assert persisted["field:__candidate_residual_requirement_evidence:12"]["text"] == (
        "Location: Early Yousef Abad (near Fatemi), Tehran."
    )
    complete = _v20_complete_requirement_plan(
        effective,
        additional_plan=additional,
        decomposed_refs=[],
        base_plan=plan,
    )
    assert set(qualification_refs) <= complete.keys()
    assert all(not complete[ref]["allow_exclusion"] for ref in qualification_refs)


def test_v24_does_not_suppress_partial_or_preferred_parent() -> None:
    parent = {
        "source_kind": "requirement_section",
        "text": "Familiarity with API, Webhook, and service connections.",
        "allow_exclusion": True,
        "obligation_hint": "required",
    }
    plan = {"parent": parent}
    assert _exact_qualification_item_plan(
        plan, {"__candidate_qualification_evidence": ["Familiarity with API"]}
    ) == plan
    preferred = {"parent": {**parent, "obligation_hint": "preferred"}}
    assert _exact_qualification_item_plan(
        preferred,
        {
            "__candidate_qualification_evidence": [
                "Familiarity with API",
                "Webhook",
                "and service connections",
            ]
        },
    ) == preferred


def test_v24_is_isolated_from_public_v23_identity() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v24"
    assert JobAnalysisServiceV24.prompt_version == ENGLISH_PROMPT_VERSION
    assert CURRENT_PROMPT == "job-analysis-english-v23"


def test_v24_filters_requirement_claims_from_other_partitions(monkeypatch) -> None:
    result = StructuredInferenceResult(
        model="offline",
        structured={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                {"concept": "Python", "evidence": "Python"},
                {"concept": "RAG", "evidence": "RAG"},
            ],
            "coverage_exclusions": [],
        },
        request_body={"runtime": {}},
        raw_response={},
        finish_reason="stop",
    )
    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v24.complete_analysis_partition_with_instructor_v24",
        lambda **_kwargs: result,
    )
    provider = object.__new__(V24CandidateAnalysisProvider)
    filtered = provider._complete_partition(
        requirement_coverage_plan={"skill": {"text": "Python"}},
        responsibility_coverage_plan={},
    )
    assert filtered.structured["requirements"] == [
        {"concept": "Python", "evidence": "Python"}
    ]


def test_v24_persistence_retains_deterministic_decomposition(monkeypatch) -> None:
    monkeypatch.setattr(
        "jobhunter.analysis_persistence_v23.decomposed_requirement_references",
        lambda _fields: ["parent"],
    )
    monkeypatch.setattr(
        "jobhunter.analysis_persistence_v23.build_requirement_coverage_plan",
        lambda _fields: {
            "parent": {"text": "Exact source paragraph.", "allow_exclusion": True}
        },
    )
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [],
        "coverage_exclusions": [
            {"evidence_reference": "parent", "rationale": "Decomposed into exact items."}
        ],
    }
    persisted = persisted_analysis_v23(structured, {}, requirement_plan={})
    assert persisted["coverage"] == [{
        "evidence": "Exact source paragraph.",
        "disposition": "decomposed_requirement",
        "rationale": "Decomposed into exact items.",
    }]


def test_v24_persistence_uses_the_generation_ownership_plan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fields = json.loads(
        (_ROOT / "corpus/jobs/tmvA/english-projection.json").read_text(encoding="utf-8")
    )["fields"]
    captured = {}

    def fake_persist(structured, analysis_fields, *, requirement_plan):
        captured["plan"] = requirement_plan
        return structured

    monkeypatch.setattr(
        "jobhunter.analysis_service_v24.persisted_analysis_v23", fake_persist
    )
    service = object.__new__(JobAnalysisServiceV24)
    assert service._persist_analysis({}, fields) == {}
    assert captured["plan"] == persisted_qualification_plan(fields)


def test_v24_partition_uses_distinct_contract_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_complete(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            model="offline",
            structured={"requirements": [], "responsibilities": []},
            request_body={"runtime": {}},
            raw_response={},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.inference.instructor_lm_studio_v20._complete_analysis_partition_with_instructor",
        fake_complete,
    )
    result = complete_analysis_partition_with_instructor_v24(
        base_url="http://127.0.0.1:1234/v1",
        api_token=None,
        timeout_seconds=30,
        network_retries=0,
        selected_model="offline",
        system_prompt="v24",
        user_payload={},
        max_tokens=512,
        seed=0,
        requirement_coverage_plan={},
        responsibility_coverage_plan={},
    )
    assert calls[0]["contract_version"] == "v24"
    assert result.request_body["runtime"]["p16_v24_exact_qualification_ownership"] is True
