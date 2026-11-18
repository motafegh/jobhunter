#!/usr/bin/env python3
"""Verify tracked B3 safe milestone hashes against ignored local evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
B2 = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"
SCORECARD = ROOT / "docs/working-memory/2026-11-18_p16_b3/SAFE_B3_MILESTONE.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    safe = json.loads(SCORECARD.read_text(encoding="utf-8"))
    manifest = json.loads((OUT / "run_manifest.json").read_text(encoding="utf-8"))
    flags = json.loads((OUT / "B3_REVIEW_FLAG_REASSESSMENT.json").read_text(encoding="utf-8"))
    checks = {
        "source_database_sha256": sha(B0),
        "b2_private_candidate_sha256": sha(B2 / "PRIVATE_B2_CANDIDATES.json"),
        "run_manifest_sha256": sha(OUT / "run_manifest.json"),
        "private_candidate_output_sha256": sha(OUT / "PRIVATE_B3_CANDIDATES.json"),
        "corrective_candidate_sha256": sha(OUT / "B3_CORRECTIVE_CANDIDATE.json"),
        "selected_b1_drafts_sha256": sha(OUT / "B1_COMPATIBLE_DRAFTS.json"),
        "safe_metrics_sha256": sha(OUT / "SAFE_B3_METRICS.json"),
        "semantic_review_sha256": sha(OUT / "B3_SEMANTIC_REVIEW.json"),
        "review_flag_reassessment_sha256": sha(OUT / "B3_REVIEW_FLAG_REASSESSMENT.json"),
        "mechanical_audit_sha256": sha(OUT / "B3_MECHANICAL_AUDIT.json"),
        "final_audit_sha256": sha(OUT / "B3_FINAL_AUDIT.json"),
        "raw_capture_index_sha256": sha(OUT / "RAW_CAPTURE_INDEX.json"),
        "checkpoint_sha256": sha(OUT / "checkpoint.jsonl"),
    }
    for key, actual in checks.items():
        if safe["hashes"][key] != actual:
            raise ValueError(f"Safe milestone hash mismatch: {key}")

    code = safe["code_fingerprints"]
    assert code["run_time_b3_runner_sha256"] == manifest["b3_code_fingerprints"]["runner_sha256"]
    assert (
        code["run_time_b3_support_module_sha256"]
        == manifest["b3_code_fingerprints"]["support_module_sha256"]
    )
    assert code["reassessment_support_module_sha256"] == flags["reassessment_support_module_sha256"]
    assert code["corrective_runner_sha256"] == sha(
        ROOT / "scripts/run_p16_b3_single_corrective_candidate.py"
    )
    assert code["reconciliation_script_sha256"] == sha(
        ROOT / "scripts/reconcile_p16_b3_corrective_selection.py"
    )
    assert code["validator_script_sha256"] == sha(
        ROOT / "scripts/validate_p16_b3_translation_run.py"
    )
    assert code["semantic_review_finalizer_sha256"] == sha(
        ROOT / "scripts/finalize_p16_b3_semantic_review.py"
    )
    assert code["safe_milestone_verifier_sha256"] == sha(
        ROOT / "scripts/verify_p16_b3_safe_milestone.py"
    )

    assert safe["status"] == "PASS_BOUNDED_EXPOSED_COHORT"
    assert safe["execution"]["total_generation_requests"] == 64
    assert safe["semantic_review"]["selected_translation_unresolved_count"] == 0
    assert safe["authority"]["accepted_employer_facts_promoted"] == 0
    assert (
        ROOT / "docs/working-memory/2026-11-18_P16_B3_SOURCE_BOUND_TRANSLATION_MILESTONE.md"
    ).is_file()
    print(
        json.dumps(
            {"status": "PASS", "verified_hashes": len(checks), "next_gate": safe["next_gate"]},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
