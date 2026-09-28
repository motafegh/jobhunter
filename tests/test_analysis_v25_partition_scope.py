"""Regression for cross-partition sentence ownership in the isolated candidate."""

import json
from pathlib import Path

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_runtime_v14 import _v14_candidate_evidence_view
from jobhunter.analysis_runtime_v20 import _v20_complete_requirement_plan
from jobhunter.analysis_runtime_v25 import V25CandidateAnalysisProvider
from jobhunter.analysis_service_v25 import ENGLISH_PROMPT_VERSION
from jobhunter.inference.instructor_lm_studio_v25 import (
    AnalysisRequirementV25,
    JobAnalysisResponseV25,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_ROOT = Path(__file__).resolve().parents[1]


def test_tmvA_source_siblings_share_one_partition() -> None:
    fields = json.loads(
        (_ROOT / "corpus/jobs/tmvA/english-projection.json").read_text(encoding="utf-8")
    )["fields"]
    effective, _, _, additional = _v14_candidate_evidence_view(fields)
    provider = object.__new__(V25CandidateAnalysisProvider)
    plan = _v20_complete_requirement_plan(
        effective,
        additional_plan=additional,
        decomposed_refs=[],
        base_plan=provider._requirement_coverage_plan(effective),
    )
    partitions = provider._requirement_partitions(plan)
    first = "field:description:segment:4:sentence:1"
    second = "field:description:segment:4:sentence:2"
    assert sum(first in part and second in part for part in partitions) == 1
    assert set().union(*(set(part) for part in partitions)) == set(plan)
    assert sum(map(len, partitions)) == len(plan)
    assert max(map(len, partitions)) <= 8


def test_t7Ay_explicit_prior_work_preferences_are_retained_as_source_quotes() -> None:
    fields = json.loads(
        (_ROOT / "corpus/jobs/t7Ay/english-projection.json").read_text(encoding="utf-8")
    )["fields"]
    effective, _, _, additional = _v14_candidate_evidence_view(fields)
    provider = object.__new__(V25CandidateAnalysisProvider)
    plan = _v20_complete_requirement_plan(
        effective,
        additional_plan=additional,
        decomposed_refs=[],
        base_plan=provider._requirement_coverage_plan(effective),
    )
    refs, claims = provider._source_quoted_requirements(plan)
    assert "field:description:segment:3:sentence:1" in refs
    assert len(refs) == len(claims) == 2
    for reference, claim in zip(refs, claims, strict=True):
        assert claim["concept"] == claim["evidence"] == plan[reference]["text"]
        assert claim["requirement_type"] == "preferred"
        assert claim["concept_type"] == "experience"
        assert claim["depth_signal"] is None


def test_source_quote_requires_explicit_preference_and_prior_work() -> None:
    provider = object.__new__(V25CandidateAnalysisProvider)
    plan = {
        "preferred-history": {
            "text": "Prior work experience in AI is an advantage.",
            "source_kind": "requirement_section",
            "obligation_hint": "preferred",
        },
        "required-history": {
            "text": "Prior work experience in AI is required.",
            "source_kind": "requirement_section",
            "obligation_hint": "required",
        },
        "preferred-knowledge": {
            "text": "Knowledge of AI is an advantage.",
            "source_kind": "requirement_section",
            "obligation_hint": "preferred",
        },
    }
    refs, _claims = provider._source_quoted_requirements(plan)
    assert refs == ["preferred-history"]


def test_v25_model_sees_only_assigned_evidence(monkeypatch) -> None:
    captured = {}

    def fake_complete(**kwargs):
        captured.update(kwargs)
        return StructuredInferenceResult(
            model="offline",
            structured={
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [],
                "coverage_exclusions": [],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v25.complete_analysis_partition_with_instructor_v24",
        fake_complete,
    )
    provider = object.__new__(V25CandidateAnalysisProvider)
    provider._complete_partition(
        requirement_coverage_plan={"assigned": {"text": "A"}},
        responsibility_coverage_plan={"work": "B"},
    )
    assert captured["model_evidence_references"] == ["assigned", "work"]
    assert captured["contract_version"] == "v25"
    assert captured["response_model"] is JobAnalysisResponseV25
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v25"


def test_shared_list_qualifier_is_trimmed_only_when_source_proves_it() -> None:
    evidence = "familiarity with Embedding, Vector Database, and Semantic Search"
    claim = {
        "concept": "Working with Vector Database",
        "depth_signal": None,
        "requirement_type": "contextual",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Source list item.",
        "item_excerpt": "familiarity with Vector Database",
    }
    context = {"analysis_mode": "english", "analysis_fields": {"description": evidence}}
    normalized = AnalysisRequirementV25.model_validate(claim, context=context)
    assert normalized.item_excerpt == "Vector Database"


def test_unsupported_experience_wording_abstains_to_exact_activity() -> None:
    evidence = "applying new technologies in the field of AI"
    claim = {
        "concept": "Experience in applying new technologies in the field of AI",
        "depth_signal": None,
        "requirement_type": "contextual",
        "concept_type": "experience",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Source activity.",
        "item_excerpt": evidence,
    }
    context = {"analysis_mode": "english", "analysis_fields": {"description": evidence}}
    normalized = AnalysisRequirementV25.model_validate(claim, context=context)
    assert normalized.concept == evidence
    assert normalized.concept_type == "other"
