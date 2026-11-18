"""Source-safe bounded B2 milestone scorecard and local reproducibility."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SAFE = ROOT / "docs/working-memory/2026-11-17_p16_b2/SAFE_B2_CANDIDATE_MILESTONE.json"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"


def _report() -> dict:
    return json.loads(SAFE.read_text(encoding="utf-8"))


def test_b2_candidate_milestone_is_bounded_and_non_promoting() -> None:
    report = _report()
    assert report["contract"] == "jobhunter-p16-b2-bounded-candidate-milestone-v1"
    assert report["candidate_milestone"] == "PASS_BOUNDED_EXPOSED_COHORT"
    assert report["b2_full_semantic_generalization"] == "NOT_ESTABLISHED"
    assert report["candidate_semantic_review"] == "candidate_unreviewed"
    assert report["model_generated_source_reference_route"] == "RESEARCH_ONLY_NO_PROMOTION"
    assert (
        report["source_cohort"]
        == "four frozen, previously exposed A1 development ads; not a holdout"
    )
    assert report["independent_accuracy_claim"] is False
    assert report["production_route_changed"] is False
    assert report["accepted_employer_facts_promoted"] == 0
    assert report["downstream_authority"] == "none"
    assert report["next_stage"] == "B3_SOURCE_BOUND_ITEM_TRANSLATION_CANDIDATE"


def test_b2_milestone_aggregate_and_board_conflict_types_are_explicit() -> None:
    report = _report()
    assert report["aggregate"] == {
        "source_item_count": 78,
        "board_value_count": 53,
        "work_duty_candidate_count": 22,
        "work_capability_hint_count": 10,
        "candidate_alternative_group_count": 3,
        "candidate_eligibility_graph_count": 2,
        "candidate_eligibility_leaf_count": 11,
        "board_conflict_count": 4,
    }
    assert report["board_conflict_type_counts"] == {
        "board_vs_employer_arrangement": 1,
        "board_vs_employer_compensation": 1,
        "board_vs_employer_experience": 1,
        "board_vs_employer_strength": 1,
    }
    assert report["per_case"]["tMjm"]["work_duty_candidate_count"] == 0
    assert report["per_case"]["tMps"]["candidate_eligibility_leaf_count"] == 9
    assert report["per_case"]["tNDx"]["board_conflict_types"] == ["board_vs_employer_compensation"]
    assert set(report["per_case"]["tNhZ"]["board_conflict_types"]) == {
        "board_vs_employer_strength",
        "board_vs_employer_arrangement",
    }


def test_safe_milestone_contains_no_raw_source_or_model_text() -> None:
    serialized = json.dumps(_report(), ensure_ascii=False)
    for forbidden in ("original_text", "exact_text", "raw_response", "PRIVATE_B2_CANDIDATES"):
        assert forbidden not in serialized
    for required in (
        "source_database_sha256",
        "private_candidate_sha256",
        "safe_diagnostic_metrics_sha256",
        "schema_sha256",
    ):
        assert len(_report()[required]) == 64


def test_local_private_candidate_reconciliation_reproduces_safe_scorecard() -> None:
    if not B0.is_file() or not (PRIVATE / "PRIVATE_B2_CANDIDATES.json").is_file():
        pytest.skip("Private frozen B0/candidate outputs are intentionally absent in CI")
    sys.path.insert(0, str(ROOT / "scripts"))
    from reconcile_b2_candidate_milestone import reconcile

    assert reconcile(B0, PRIVATE) == _report()
