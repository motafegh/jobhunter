"""B2 source-ref comparative scorecard: exact provenance, no promotion."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-16"
SAFE = ROOT / "docs/working-memory/2026-11-16_p16_b2"


@pytest.fixture
def scorer(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("reconcile_b2_source_ref_trial")


def _load(name: str) -> dict:
    return json.loads((SAFE / name).read_text())


def _private_available() -> bool:
    return all(
        p.is_file()
        for p in (
            PRIVATE / "native-source-refs-v1/PRIVATE_SOURCE_REFERENCED_TRIAL.json",
            PRIVATE / "native-corrective-v3/PRIVATE_NATIVE_TRIAL.json",
        )
    )


def _evidence(scorer):
    new_path = PRIVATE / "native-source-refs-v1/PRIVATE_SOURCE_REFERENCED_TRIAL.json"
    old_path = PRIVATE / "native-corrective-v3/PRIVATE_NATIVE_TRIAL.json"
    trial = scorer.read_object(new_path)
    baseline = scorer.read_object(old_path)
    review = _load("SAFE_NATIVE_SOURCE_REF_ASSISTANT_CHECKS.json")
    old_review = _load("SAFE_ASSISTANT_SOURCE_SEMANTIC_CHECKS.json")
    metrics = _load("SAFE_NATIVE_SOURCE_REF_METRICS.json")
    return (
        trial,
        baseline,
        review,
        old_review,
        metrics,
        hashlib.sha256(new_path.read_bytes()).hexdigest(),
    )


def test_frozen_public_review_is_exposed_and_non_promoting():
    record = _load("SAFE_NATIVE_SOURCE_REF_ASSISTANT_CHECKS.json")
    assert record["review_authority"] == "assistant_prior_context_exposed_not_independent_or_blind"
    assert record["semantic_acceptance"] is False
    assert record["b2_gate"] == "OPEN_NO_PROMOTION"
    assert len(record["reviewed_checks"]) == 12
    assert len({(x["source_job_id"], x["check"]) for x in record["reviewed_checks"]}) == 12
    for row in record["reviewed_checks"]:
        assert row["v4_outcome"] in {"pass", "partial", "fail", "unresolved"}
        assert row["rationale"]


def test_source_referenced_result_is_not_interpreted_as_accuracy():
    report = _load("SAFE_NATIVE_SOURCE_REF_RECONCILIATION.json")
    assert report["b2_semantic_gate"] == "OPEN_NO_PROMOTION"
    assert report["semantic_acceptance"] is False
    assert report["independent_accuracy"] is False
    assert report["source_link_equals_semantic_entailment"] is False
    assert report["production_promotions"] == 0
    assert report["sample_cases"] == 4
    assert report["source_ref_valid_linked_claim_count"] == 73
    assert report["source_ref_candidate_disagreements"] == 25
    assert report["source_ref_unlinked_unknown"] == 2
    serialized = json.dumps(report, ensure_ascii=False)
    assert "source_anchor_ids" not in serialized
    assert "original_text" not in serialized
    assert "raw_response" not in serialized


def test_private_exact_records_generate_same_safe_scorecard_and_reject_tampering(scorer):
    if not _private_available():
        pytest.skip("Frozen source and provider evidence intentionally ignored in CI")
    records = _evidence(scorer)
    fresh = scorer.reconcile(*records)
    assert fresh == _load("SAFE_NATIVE_SOURCE_REF_RECONCILIATION.json")
    for index, attr, value in (
        (0, "prompt_sha256", "b" * 64),
        (0, "source_database_sha256", "b" * 64),
        (1, "source_database_sha256", "b" * 64),
        (2, "private_model_run_sha256", "b" * 64),
        (2, "review_authority", "independent_human"),
    ):
        changed = list(copy.deepcopy(records))
        changed[index][attr] = value
        with pytest.raises(ValueError, match="provenance"):
            scorer.reconcile(*changed)
    changed = list(copy.deepcopy(records))
    changed[0]["cases"]["tNDx"]["source_items"][0]["number"] = 3000
    with pytest.raises(ValueError, match="source item numbers"):
        scorer.reconcile(*changed)
    changed = list(copy.deepcopy(records))
    changed[2]["reviewed_checks"][0]["check"] = "fabricated_check"
    with pytest.raises(ValueError, match="checks"):
        scorer.reconcile(*changed)
