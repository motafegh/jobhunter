"""Read-only versioned re-score of the ALREADY EXPOSED fourth B5 cohort.

The original frozen prospective scorer/result remain byte-identical.
No retraining, acquisitions, LLM calls, v30 generation or production writes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from pathlib import Path
from typing import Any

from jobhunter.source_gate_evaluation_v2 import evaluate_calibrated_gate
from jobhunter.source_item_candidate_b2_v4_dom import interpret_original_source_candidate_v4
from jobhunter.source_item_candidate_b2_v5_dom import interpret_original_source_candidate_v5
from jobhunter.source_item_candidate_b2_v6_dom import interpret_original_source_candidate_v6
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/fourth-source-cohort-v1"
PRIVATE_OUT = ROOT / "data/local-acceptance/p16-b5-calibrated-2026-11-22"
PUBLIC_OUT = (
    ROOT / "docs/working-memory/2026-11-22_p16_b5_calibrated/"
    "SAFE_EXPOSED_SOURCE_GATE_CALIBRATION.json"
)
OLD_SAFE = (
    ROOT / "docs/working-memory/2026-11-22_p16_b5_fourth/"
    "SAFE_FOURTH_B5_FAILURE_AND_B2V5_EXPOSED.json"
)
ENGINES = (
    (
        "B2v4_frozen_prospective",
        interpret_original_source_candidate_v4,
        "src/jobhunter/source_item_candidate_b2_v4_dom.py",
    ),
    (
        "B2v5_exposed",
        interpret_original_source_candidate_v5,
        "src/jobhunter/source_item_candidate_b2_v5_dom.py",
    ),
    (
        "B2v6_exposed",
        interpret_original_source_candidate_v6,
        "src/jobhunter/source_item_candidate_b2_v6_dom.py",
    ),
)
CALIBRATION_FILE = "src/jobhunter/source_gate_evaluation_v2.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def serialized(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def evaluate() -> tuple[dict[str, Any], dict[str, Any]]:
    # The historical frozen record verifies the original SHA/DB/source bytes,
    # order, assistant-first review, and exact original B2v4 failed result.
    old_verify = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_fourth_source_gate.py"))["verify"]
    old_result = old_verify()
    if old_result["status"] != ("PASS_REPLAY_FOURTH_UNSEEN_SOURCE_GATE_FAILURE_NOT_B5_ACCEPTANCE"):
        raise ValueError("Original frozen B5 failed record changed")
    old_safe = load(OLD_SAFE)
    if old_safe["B5_pass"] or old_safe["B6_promotion_authorized"]:
        raise ValueError("Original prospective verdict was promoted")
    for key, _engine, path in ENGINES[:2]:
        baseline_key = (
            "B2v4_frozen_candidate" if key.startswith("B2v4") else "B2v5_exposed_candidate"
        )
        if sha(ROOT / path) != old_safe["sha256"][baseline_key]:
            raise ValueError("Historical candidate bytes changed")

    original = load(PRIVATE / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json")
    review = load(PRIVATE / "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    supplement = load(PRIVATE / "SOURCE_FIRST_EXPLICIT_OR_SUPPLEMENT_SEALED.json")
    metadata = load(PRIVATE / "FROZEN_METADATA_SELECTION.json")
    records = {x["source_job_id"]: x for x in original["entries"]}
    versions = {}
    store = TranslationStore(PRIVATE / "isolated-fourth-cohort.sqlite3")
    for item in metadata["primary"]:
        job = item["source_job_id"]
        versions[job] = store.latest_source_version(job)
    # Deep-copy source-first review; NEVER rewrite any private frozen source.
    selected_review = json.loads(json.dumps(review))
    for extra in supplement["alternative_anchors"]:
        entry = next(
            x for x in selected_review["entries"] if x["source_job_id"] == extra["source_job_id"]
        )
        entry["reviewed_original_anchors"].append(
            {k: v for k, v in extra.items() if k != "source_job_id"}
        )
    frozen = {"selected_primary": metadata["primary"]}
    scored = {}
    for name, engine, _path in ENGINES:

        def candidate(src, _engine=engine):
            rec = records[src.source_job_id]
            return _engine(
                src,
                raw_job_page=Path(rec["private_raw_html_path"]).read_bytes(),
                expected_html_sha256=rec["raw_html_sha256"],
            )

        scored[name] = evaluate_calibrated_gate(
            frozen=frozen,
            review=selected_review,
            source_versions=versions,
            engine=candidate,
        )

    # Verify the latest candidate still satisfies the unchanged B1 original
    # evidence contract; this does not certify category semantics.
    b1_bundle = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ]
    b1_validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))[
        "validate_bundle"
    ]
    for src in versions.values():
        rec = records[src.source_job_id]
        v6_candidate = interpret_original_source_candidate_v6(
            src,
            raw_job_page=Path(rec["private_raw_html_path"]).read_bytes(),
            expected_html_sha256=rec["raw_html_sha256"],
        )
        b1_validate(b1_bundle(v6_candidate, src), source=src)

    safe = {
        "contract": "jobhunter-p16-b5-exposed-calibrated-gate-v2",
        "status": "PASS_EXPOSED_METHOD_REPAIR_NO_B5_ACCEPTANCE",
        "original_frozen_evaluation_status": old_result["status"],
        "original_B2v4_source_gate_failed": True,
        "candidate_scope": "all_fourth_sources_now_exposed",
        "source_jobs": old_result["source_jobs"],
        "selected_original_source_assertions": 80,
        "b1_candidate_contract_validations": len(versions),
        "review_blind_to_candidate_at_original_time": True,
        "review_independent_human": False,
        "material_category_errors_still_counted": True,
        "example_lists_do_not_imply_mandatory_eligibility_OR": True,
        "multiple_contiguous_original_duty_bullets_preserve_separate_items": True,
        "candidates": {
            name: {
                "disposition": output["disposition"],
                "counts": output["counts"],
            }
            for name, output in scored.items()
        },
        "code_sha256": {path: sha(ROOT / path) for _, _, path in ENGINES}
        | {CALIBRATION_FILE: sha(ROOT / CALIBRATION_FILE)},
        "frozen_original_record_sha256": sha(
            PRIVATE / "B5_FOURTH_FROZEN_PROSPECTIVE_SOURCE_GATE_RESULT.json"
        ),
        "frozen_source_first_review_sha256": sha(
            PRIVATE / "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"
        ),
        "frozen_source_first_alternatives_sha256": sha(
            PRIVATE / "SOURCE_FIRST_EXPLICIT_OR_SUPPLEMENT_SEALED.json"
        ),
        "production_database_sha256": sha(ROOT / "data/jobhunter.sqlite3"),
        "public_corpus_manifest_sha256": sha(ROOT / "corpus/manifest.json"),
        "new_model_requests": 0,
        "new_source_requests": 0,
        "new_accepted_employer_facts": 0,
        "B5_accepted": False,
        "B6_promotion_authorized": False,
        "independent_generalization_established": False,
        "user_usefulness_measured": False,
        "limitations": [
            "Original fourth cohort is exposed and cannot validate new candidates prospectively",
            "Source-first assertions were assistant selected, not exhaustive or "
            "independent human truth",
            "A source-covered alternative example is not a certified employer eligibility DAG",
            "Corrected segmentation scoring and broad taxonomy compatibility "
            "need independent calibration",
            "No paired bilingual/English v30 or real user decision evidence acquired",
        ],
    }
    private = {
        "contract": "jobhunter-p16-b5-calibrated-private-replay-v2",
        "original_prospective_record_preserved": True,
        "reviewer_status": "assistant_original_first_subsequently_exposed",
        "engines": scored,
    }
    return safe, private


def write_once() -> dict[str, Any]:
    if PUBLIC_OUT.exists() or PRIVATE_OUT.exists():
        raise ValueError("Frozen calibrated outputs already exist; use verification")
    safe, private = evaluate()
    PRIVATE_OUT.mkdir(parents=True)
    f = PRIVATE_OUT / "PRIVATE_EXPOSED_CALIBRATED_DETAILS.json"
    f.write_bytes(serialized(private))
    safe["private_calibrated_details_sha256"] = sha(f)
    PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT.write_bytes(serialized(safe))
    return {
        "status": safe["status"],
        "candidates": safe["candidates"],
        "B5_accepted": False,
    }


def verify() -> dict[str, Any]:
    safe, private = evaluate()
    private_file = PRIVATE_OUT / "PRIVATE_EXPOSED_CALIBRATED_DETAILS.json"
    if not private_file.is_file() or private_file.read_bytes() != serialized(private):
        raise ValueError("Private calibrated source replay changed")
    safe["private_calibrated_details_sha256"] = sha(private_file)
    if not PUBLIC_OUT.is_file() or PUBLIC_OUT.read_bytes() != serialized(safe):
        raise ValueError("Public calibrated source scorecard changed")
    return {
        "status": safe["status"],
        "candidates": safe["candidates"],
        "B5_accepted": False,
        "B6_authorized": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-once", action="store_true")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    if args.preview:
        report, _ = evaluate()
        print(
            json.dumps(
                {"status": report["status"], "candidates": report["candidates"]},
                sort_keys=True,
            )
        )
    elif args.write_once:
        print(json.dumps(write_once(), sort_keys=True))
    else:
        print(json.dumps(verify(), sort_keys=True))
