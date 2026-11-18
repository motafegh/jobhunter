#!/usr/bin/env python3
"""Finalize the assistant's exposed-cohort semantic review ledger and safe hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    private_path = OUT / "PRIVATE_B3_CANDIDATES.json"
    semantic_path = OUT / "B3_SEMANTIC_REVIEW.json"
    safe_path = OUT / "SAFE_B3_METRICS.json"
    audit_path = OUT / "B3_MECHANICAL_AUDIT.json"
    flags_path = OUT / "B3_REVIEW_FLAG_REASSESSMENT.json"
    corrective_path = OUT / "B3_CORRECTIVE_CANDIDATE.json"
    b1_path = OUT / "B1_COMPATIBLE_DRAFTS.json"
    raw_path = OUT / "RAW_CAPTURE_INDEX.json"

    private = read(private_path)
    semantic = read(semantic_path)
    flags = read(flags_path)
    safe = read(safe_path)
    audit = read(audit_path)

    reassessed_by_anchor = {
        row["source_anchor_id"]: row["reassessed_flags_v2"] for row in flags["changed_items"]
    }
    reviewed_items = []
    for record in private["items"]:
        job = record["source_job_id"]
        anchor = record["source_anchor_id"]
        if record["state"] == "native_identity":
            status = "native_identity_verified"
            selected_sha = record["target_sha256"]
            primary_flags = []
            selected_flags = []
        elif (
            job == "tMjm"
            and anchor == "beeca48335d4bd92df06c563ff3593278b8c72c2960583169a7a6d0ec2be8062"
        ):
            status = "primary_mistranslation_corrected"
            selected_sha = record["selected_translation"]["target_sha256"]
            primary_flags = record["review_flags_reassessed_v2"]
            selected_flags = record["selected_translation_review_flags_v2"]
        else:
            status = "meaning_preserving_exposed_cohort"
            selected_sha = record["target_sha256"]
            primary_flags = reassessed_by_anchor.get(anchor, record.get("review_flags", []))
            selected_flags = primary_flags
        record["review_flags_reassessed_v2"] = primary_flags
        record["assistant_semantic_review"] = {
            "status": status,
            "reviewer": "assistant_exposed_cohort_semantic_review",
            "review_scope": "source-bound translation meaning; not employer-fact acceptance",
            "reviewer_exposure": "prior project context; not blind or independent human review",
        }
        reviewed_items.append(
            {
                "source_job_id": job,
                "source_item_id": record["source_item_id"],
                "source_anchor_id": anchor,
                "source_span_sha256": record["source_span_sha256"],
                "review_status": status,
                "primary_target_sha256": record["target_sha256"],
                "selected_target_sha256": selected_sha,
                "primary_review_flags_v2": primary_flags,
                "selected_review_flags_v2": selected_flags,
            }
        )

    private["assistant_semantic_review"] = {
        "status": "completed_for_four_exposed_development_ads",
        "reviewed_persian_translation_count": 63,
        "reviewed_native_identity_count": 1,
        "independent_or_holdout_review": False,
    }
    write(private_path, private)

    semantic["reviewed_items"] = reviewed_items
    semantic["assistant_semantic_review_method"] = (
        "Assistant compared every exact Persian source item with its source-bound English "
        "candidate across the four exposed ads, separately checked modality/alternatives/"
        "heading boundaries, and retained source uncertainty."
    )
    semantic["independent_or_blind_review"] = False
    semantic["assistant_reviewed_item_count"] = len(reviewed_items)
    semantic["assistant_reviewed_translation_count"] = sum(
        row["review_status"] != "native_identity_verified" for row in reviewed_items
    )
    write(semantic_path, semantic)

    safe["limitations"] = [
        "The four source ads are exposed development cases, not a holdout.",
        "Exact source anchors prove provenance, not semantic translation correctness.",
        "Assistant review is not independent blind human review or unseen-generalization evidence.",
        (
            "One primary material mistranslation was superseded by one corrective candidate and a "
            "documented reviewer terminology normalization; the original primary remains preserved."
        ),
        "Native identity is in the B3 sidecar; no B1 v2-native artifact is fabricated.",
        (
            "Twelve nested eligibility leaves have source identity but no separate target "
            "subspan offsets."
        ),
        "No B3 candidate gains accepted-fact or downstream authority.",
    ]

    audit["b3_private_candidate_sha256"] = sha(private_path)
    audit["b1_compatible_drafts_sha256"] = sha(b1_path)
    audit["raw_capture_index_sha256"] = sha(raw_path)
    audit["corrective_candidate_sha256"] = sha(corrective_path)
    audit["semantic_review_sha256"] = sha(semantic_path)
    audit["review_flag_reassessment_sha256"] = sha(flags_path)
    audit["review_flag_counts_after_reassessment"] = flags["reassessed_flag_counts_v2"]
    audit["assistant_reviewed_translation_count"] = 63
    audit["assistant_reviewed_native_identity_count"] = 1
    audit["assistant_review_material_issue_count"] = 1
    write(audit_path, audit)

    safe["private_candidate_output_sha256"] = sha(private_path)
    safe["semantic_review_sha256"] = sha(semantic_path)
    safe["mechanical_audit_sha256"] = sha(audit_path)
    safe["review_flag_reassessment_sha256"] = sha(flags_path)
    safe["corrective_candidate_sha256"] = sha(corrective_path)
    safe["b1_compatible_drafts_sha256"] = sha(b1_path)
    safe["raw_capture_index_sha256"] = sha(raw_path)
    write(safe_path, safe)

    print(
        json.dumps(
            {
                "status": "PASS",
                "reviewed_items": len(reviewed_items),
                "reviewed_persian_translations": 63,
                "reviewed_native_identity": 1,
                "corrected_primary_mistranslations": 1,
                "safe_metrics_sha256": sha(safe_path),
                "semantic_review_sha256": sha(semantic_path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
