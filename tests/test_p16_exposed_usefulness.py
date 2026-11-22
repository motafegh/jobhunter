"""Exposed-source usefulness audit invariants (private real-case replay is optional)."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = runpy.run_path(str(ROOT / "scripts/evaluate_p16_exposed_usefulness.py"))
SAFE = SCRIPT["PUBLIC_OUT"]


def test_safe_scorecard_refuses_semantic_or_product_promotion():
    record = json.loads(SAFE.read_text(encoding="utf-8"))
    assert record["contract"] == "jobhunter-p16-exposed-usefulness-scorecard-v1"
    assert record["status"] == "PASS_OFFLINE_EXPOSED_TASK_EVIDENCE_NOT_USER_VALUE_OR_B5"
    assert record["case_count"] == 4
    assert record["preselected_task_count"] == 9
    assert record["assistant_exposed_review_counts"] == {
        "partially_visible_or_uncertain": 4,
        "source_supported_visible": 5,
    }
    assert record["v30_valid_same_source_artifact_count"] == 0
    assert record["v30_failed_case_count"] == 3
    assert record["v30_rejected_only_case_count"] == 1
    assert record["v9_accepted_artifact_count"] == 1
    assert record["same_source_model_semantic_pair_count"] == 0
    assert record["new_LLM_or_source_network_requests"] == 0
    assert record["accepted_employer_facts_promoted"] == 0
    assert record["B5_independent_generalization_pass"] is False
    assert record["B6_promotion_authorized"] is False
    assert record["measured_owner_time_savings"] is False
    assert record["user_usefulness_advantage_established"] is False
    assert record["blind_independent_human_review"] is False
    assert record["candidate_source_categories_semantically_certified"] is False
    assert record["production_database_modified"] is False
    assert record["public_corpus_modified"] is False


def test_public_safe_scorecard_has_no_original_language_employer_text():
    text = SAFE.read_text(encoding="utf-8")
    assert not any("\u0600" <= character <= "\u06ff" for character in text)
    assert "original_text" not in text
    assert "english_reading_aid" not in text
    assert "assistant_reasoning_summary" not in text
    assert "https://jobinja" not in text
    assert "/home/motafeq" not in text


def test_synthetic_source_anchor_changed_quote_is_rejected():
    item = {
        "original_text": "Build secure APIs",
        "source_span_sha256": SCRIPT["digest_text"]("Build secure APIs"),
        "authority": "B2_B3_source_qualified_candidate_not_accepted_fact",
        "source_item_id": "s_synthetic",
        "target_text_candidate": "Build secure APIs",
    }
    SCRIPT["original_item_integrity"](item)
    item["original_text"] = "Build unrelated systems"
    with pytest.raises(ValueError, match="source-span SHA mismatch"):
        SCRIPT["original_item_integrity"](item)


def test_synthetic_accepted_v30_artifact_is_not_treated_as_failed_baseline():
    case = {"source_job_id": "tNhZ", "source_version": {"job_detail_version_id": 1}}
    baseline = {
        "tNhZ": {
            "source_job_id": "tNhZ",
            "job_detail_version_id": 1,
            "source_snapshot_same_as_b4": True,
            "v30": {"status": "failed_no_artifact", "valid_artifact_ids": [77]},
            "v9": {"status": "no_v9_artifact", "artifacts": []},
        }
    }
    with pytest.raises(ValueError, match="no-valid-v30 baseline"):
        SCRIPT["baseline_state"](baseline, case)


def test_synthetic_graph_does_not_invent_translated_child_alignment():
    graph = {
        "graph_id": "synthetic",
        "authority": "B2_candidate_structure_not_accepted_employer_eligibility",
        "root": {
            "kind": "any_of",
            "children": [
                {
                    "kind": "original_subspan",
                    "source_item_id": "x",
                    "child_english_alignment": "established",
                },
                {
                    "kind": "original_subspan",
                    "source_item_id": "y",
                    "child_english_alignment": "not_established",
                },
            ],
        },
    }
    case = {"eligibility_alternative_candidates": [graph]}
    item = {"category_candidate": "candidate_qualification"}
    task = {"graph_id": "synthetic", "parents": ("parent",)}
    with pytest.raises(ValueError, match="Invented independent English"):
        SCRIPT["graph_evidence"](case, task, {"parent": item})


def test_task_selection_keeps_qualified_abstentions_and_source_only_case():
    record = json.loads(SAFE.read_text(encoding="utf-8"))
    cases = record["per_case"]
    assert tuple(cases) == ("tMjm", "tMps", "tNDx", "tNhZ") or set(cases) == {
        "tNhZ",
        "tMps",
        "tNDx",
        "tMjm",
    }
    assert cases["tMjm"]["b4_model_candidate_state"] == "source_only_candidate"
    assert cases["tMjm"]["b4v5_alternative_graph_count"] == 0
    assert cases["tMps"]["b4_model_candidate_state"] == "failed"
    assert cases["tNDx"]["b4v5_reviewed_translation_overlays"] == 1
    assert cases["tNDx"]["b4v5_withheld_old_model_claims"] == 2
    assert cases["tNhZ"]["b4_model_candidate_state"] == "partial_candidate"


def test_private_source_task_replay_when_local_evidence_is_available():
    private = SCRIPT["PRIVATE_OUT"] / "PRIVATE_EXPOSED_TASK_REVIEW.json"
    if not private.exists():
        pytest.skip("Private original-source evidence not available in CI")
    status = SCRIPT["verify"]()
    assert status["status"] == "PASS_REPLAY_EXPOSED_USEFULNESS_EVIDENCE_NO_SEMANTIC_PROMOTION"
    assert status["tasks"] == 9
    assert status["valid_v30_artifacts"] == 0
    assert status["B5_pass"] is False
