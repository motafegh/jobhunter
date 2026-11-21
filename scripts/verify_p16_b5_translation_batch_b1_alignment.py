#!/usr/bin/env python3
"""Freeze/replay the B1 alignment of two exposed batched model outputs.

The original source and HTTP pilot were sealed before this connector was
implemented. It does not rerun inference or promote any employer facts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.source_bound_translation_b1_alignment_b5 import (
    align_batch_result_to_b1,
)
from jobhunter.source_item_candidate_b2_v2 import (
    interpret_original_source_candidate_v2,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
PILOT = PRIVATE / "batch-pilot-v1"
RECEIPT = PILOT / "PRIVATE_B1_ALIGNMENT_RECEIPT.json"
SAFE = (
    ROOT / "docs/working-memory/2026-11-21_p16_b5_translation_batch/"
    "SAFE_EXPOSED_TRANSLATION_BATCH_PILOT.json"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def replay() -> dict:
    checked = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_translation_batch_pilot.py"))[
        "verify"
    ]()
    if checked["status"] != ("PASS_EXPOSED_BATCH_ASSOCIATION_PILOT_NO_SEMANTIC_GENERALIZATION"):
        raise ValueError("Frozen model pilot cannot be verified")
    scope = read(PILOT / "FROZEN_SCOPE.json")
    output = read(PILOT / "PRIVATE_RESULT.json")
    chosen = runpy.run_path(str(ROOT / "scripts/pilot_p16_b5_translation_batch.py"))[
        "chosen_batch"
    ]()
    if chosen.batch_id != scope["batch_id"]:
        raise ValueError("B1 alignment source batch changed")
    source = TranslationStore(PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3").latest_source_version(
        chosen.source_job_id
    )
    if source is None:
        raise ValueError("Frozen original job source not found")
    candidate = interpret_original_source_candidate_v2(source)
    b1 = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"](
        candidate, source
    )
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validate(b1, source=source)
    translated = output["source_bound_candidate_outputs"][0]["result"]
    alignments = align_batch_result_to_b1(b1, chosen, translated)
    if len(alignments) != 2:
        raise ValueError("Expected exactly two original-to-English B1 relations")
    b1["alignments"] = list(alignments)
    validate(b1, source=source)
    if (
        b1["authority"] != "candidate_only_no_downstream_reuse"
        or b1["brief"]["downstream_authority"] != "none"
        or b1["review_events"] != []
        or not all(
            a["state"] == "source_bound_translation_candidate"
            and a["meaning_review"] == "unreviewed"
            for a in alignments
        )
    ):
        raise ValueError("B1 batched output was improperly promoted")
    return {
        "contract": "jobhunter-p16-b5-exposed-batch-B1-alignment-candidate-v1",
        "source_cohort": "previously_exposed_development_only",
        "pilot_scope_sha256": sha(PILOT / "FROZEN_SCOPE.json"),
        "pilot_result_sha256": sha(PILOT / "PRIVATE_RESULT.json"),
        "private_assistant_review_sha256": sha(PILOT / "PRIVATE_ASSISTANT_TRANSLATION_REVIEW.json"),
        "B1_bridge_module_sha256": sha(
            ROOT / "src/jobhunter/source_bound_translation_b1_alignment_b5.py"
        ),
        "B1_source_contract_authority": b1["authority"],
        "B1_downstream_authority": b1["brief"]["downstream_authority"],
        "source_semantic_sha256": source.semantic_sha256,
        "source_exact_original_anchor_ids": [i.source_anchor_id for i in chosen.items],
        "candidate_alignments": list(alignments),
        "exact_B1_contract_validation_pass": True,
        "paired_translation_model_calls_added": 0,
        "accepted_facts": 0,
        "new_B5_unseen_verification": False,
        "production_modified": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seal", action="store_true")
    args = p.parse_args()
    regenerated = replay()
    if args.seal:
        if RECEIPT.exists():
            raise ValueError("B1 pilot evidence already sealed")
        regenerated["sealed_at_utc"] = datetime.now(UTC).isoformat()
        RECEIPT.write_text(
            json.dumps(regenerated, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )
        RECEIPT.chmod(0o600)
        public = read(SAFE)
        public["B1_item_translation_alignment_count"] = 2
        public["B1_candidate_alignment_contract_validated"] = True
        public["B1_source_item_strength_and_field_sha_verification"] = "pass"
        public["B1_translation_alignment_source_unreviewed"] = True
        public["B1_connector_uses_no_additional_model_calls"] = True
        public["evidence_sha256"]["candidate_B1_alignment_connector"] = sha(
            ROOT / "src/jobhunter/source_bound_translation_b1_alignment_b5.py"
        )
        public["evidence_sha256"]["private_B1_alignment_receipt"] = sha(RECEIPT)
        public["pilot_latency_interpretation"] = (
            "batch_request_was_first_then_two_single_controls;"
            "warming_and_order_not_controlled;no_inferred_latency_savings"
        )
        SAFE.write_text(json.dumps(public, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        original = read(RECEIPT)
        checked = {k: v for k, v in original.items() if k != "sealed_at_utc"}
        if checked != regenerated:
            raise ValueError("Sealed B1 alignment replay no longer matches original")
        public = read(SAFE)
        if public["evidence_sha256"]["private_B1_alignment_receipt"] != sha(RECEIPT):
            raise ValueError("Public safe receipt SHA changed")
    print(
        json.dumps(
            {
                "status": "PASS_EXPOSED_B1_ALIGNMENT_CANDIDATE_ONLY",
                "source_items": len(regenerated["candidate_alignments"]),
                "B1_contract_valid": regenerated["exact_B1_contract_validation_pass"],
                "model_calls_added": 0,
                "new_B5_unseen": False,
                "accepted_facts": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
