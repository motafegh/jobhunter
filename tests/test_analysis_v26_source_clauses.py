"""Source-fact ownership for the two remaining Market core postings."""

import json
from pathlib import Path

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_runtime_v26 import V26CandidateAnalysisProvider
from jobhunter.analysis_service_v26 import ENGLISH_PROMPT_VERSION
from jobhunter.evidence_refs_v26 import persisted_qualification_plan_v26

_ROOT = Path(__file__).resolve().parents[1]


def _fields(job: str) -> dict:
    return json.loads(
        (_ROOT / f"corpus/jobs/{job}/english-projection.json").read_text(
            encoding="utf-8"
        )
    )["fields"]


def test_t7Ay_mixed_education_preserves_both_obligations() -> None:
    plan = persisted_qualification_plan_v26(_fields("t7Ay"))
    parent = "field:description:segment:1"
    assert parent not in plan
    required = plan[f"{parent}:required_clause"]
    preferred = plan[f"{parent}:preferred_clause"]
    assert required["obligation_hint"] == "required"
    assert preferred["obligation_hint"] == "preferred"
    assert "Master's or Ph.D." in required["text"]
    assert preferred["text"].startswith("preferably graduates")
    provider = object.__new__(V26CandidateAnalysisProvider)
    refs, claims = provider._source_quoted_requirements(plan)
    assert f"{parent}:required_clause" in refs
    assert f"{parent}:preferred_clause" in refs
    for reference, claim in zip(refs, claims, strict=True):
        if reference.startswith(parent):
            assert claim["concept"] == claim["evidence"] == plan[reference]["text"]
            assert claim["requirement_type"] == plan[reference]["obligation_hint"]


def test_tmvA_negative_and_salary_context_stay_out_of_positive_demand() -> None:
    plan = persisted_qualification_plan_v26(_fields("tmvA"))
    provider = object.__new__(V26CandidateAnalysisProvider)
    refs, exclusions = provider._source_context_exclusions(plan)
    assert "field:description:segment:4:sentence:1" in refs
    assert "field:__candidate_residual_requirement_evidence:14" in refs
    assert "field:description:segment:4:sentence:2" not in refs
    assert all(plan[reference]["allow_exclusion"] for reference in refs)
    assert {item["evidence_reference"] for item in exclusions} == set(refs)
    mixed = persisted_qualification_plan_v26(_fields("tGc5"))
    mixed_refs, _ = provider._source_context_exclusions(mixed)
    assert "field:description:segment:10" not in mixed_refs


def test_v26_is_isolated_from_public_contract() -> None:
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v26"
