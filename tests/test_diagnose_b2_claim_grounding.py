"""Offline B2 claim-grounding diagnostic safety and private regression."""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
WORK = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-16"
TRIAL = WORK / "native-corrective-v3/PRIVATE_NATIVE_TRIAL.json"
LINKS = WORK / "source-claim-grounding-v1/PRIVATE_REVIEW_LINKS.json"


@pytest.fixture
def diagnostic(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("diagnose_b2_claim_grounding")


def test_raw_sources_and_full_outputs_cannot_be_marked_public(diagnostic, tmp_path: Path):
    private = ROOT / "data/local-acceptance"
    safe = ROOT / "docs/working-memory/2026-11-16_p16_b2"
    assert diagnostic._inside(private / "case/PRIVATE.json", private)
    assert diagnostic._inside(safe / "SAFE.json", safe)
    assert not diagnostic._inside(ROOT / "docs/WORKING_MEMORY.md", private)
    assert not diagnostic._inside(tmp_path / "PRIVATE.json", safe)
    assert not diagnostic._inside(private / "../somewhere-else/file.json", private)


def test_no_model_network_or_production_router_dependency(diagnostic):
    assert diagnostic.OUT_CONTRACT == "jobhunter-b2-advisory-grounding-diagnostic-v1"
    assert diagnostic.CASES == ("tNhZ", "tMps", "tNDx", "tMjm")
    import jobhunter.analysis_current as public_router

    assert not hasattr(public_router, "build_b2_claim_reconciliation_service")


def test_private_exposed_trial_disagreements_are_only_candidate_signals(diagnostic, tmp_path):
    if not all(path.is_file() for path in (B0, TRIAL, LINKS)):
        pytest.skip("Ignored original B0 and native-model trial unavailable in public CI")
    before = hashlib.sha256(B0.read_bytes()).hexdigest()
    private, safe = diagnostic.evaluate(B0, TRIAL, LINKS)
    assert safe["totals"] == {
        "model_claims": 85,
        "linked": 14,
        "unlinked_unknown": 71,
        "source_candidate_disagreement": 9,
        "promoted": 0,
    }
    assert safe["b2_gate"] == "OPEN_NO_PROMOTION"
    assert safe["accepted_employer_facts"] == 0
    assert private["semantic_approval"] is False
    assert not safe["source_links_are_semantic_proof"]
    assert hashlib.sha256(B0.read_bytes()).hexdigest() == before
    for case in ("tNhZ", "tMps", "tNDx", "tMjm"):
        assert safe["cases"][case]["promoted_claims"] == 0
    public_json = json.dumps(safe, ensure_ascii=False)
    assert "source_anchor_ids" not in public_json
    assert "claim_sha256" not in public_json
    assert "original_source_text" not in public_json

    data = json.loads(LINKS.read_text())
    data["links"]["tNDx"][0]["claim_sha256"] = "0" * 64
    changed = tmp_path / "wrong-claim.json"
    changed.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="stale"):
        diagnostic.evaluate(B0, TRIAL, changed)

    data = json.loads(LINKS.read_text())
    data["links"]["tNDx"][0]["source_anchor_ids"] = ["0" * 64]
    changed.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="Unknown"):
        diagnostic.evaluate(B0, TRIAL, changed)

    data = json.loads(LINKS.read_text())
    data["trial_file_sha256"] = "a" * 64
    changed.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="provenance"):
        diagnostic.evaluate(B0, TRIAL, changed)
