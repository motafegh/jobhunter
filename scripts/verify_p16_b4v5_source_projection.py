"""Replay the B4v5 private source-qualified projection audit without model calls."""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

from jobhunter.source_qualified_b4v5 import project_source_qualified_case

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c"
CORRECTION = ROOT / (
    "data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json"
)
OUT = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Review artifact must contain JSON object")
    return value


def verify() -> dict:
    old = runpy.run_path(str(ROOT / "scripts/verify_p16_b4_milestone.py"))["verify"]()
    if old["status"] != "PASS_ENGINEERING_BOUNDARIES_SEMANTIC_GATE_OPEN":
        raise ValueError("Prior B4v4c verification is not complete")

    audit = load(OUT / "FINAL_AUDIT.json")
    metrics = load(OUT / "SAFE_COUNTS.json")
    projected = load(OUT / "PRIVATE_SOURCE_PROJECTIONS.json")
    reviewed = load(CORRECTION)
    prior = load(PRIOR / "PRIVATE_B4_CANDIDATES.json")
    values = {
        "prior_b4v4c_private_sha256": sha(PRIOR / "PRIVATE_B4_CANDIDATES.json"),
        "prior_b4v4c_final_audit_sha256": sha(PRIOR / "B4_FINAL_AUDIT.json"),
        "reviewed_correction_sha256": sha(CORRECTION),
        "source_projector_module_sha256": sha(ROOT / "src/jobhunter/source_qualified_b4v5.py"),
        "runner_sha256": sha(ROOT / "scripts/run_p16_b4v5_source_projection.py"),
        "private_projection_sha256": sha(OUT / "PRIVATE_SOURCE_PROJECTIONS.json"),
        "markdown_sha256": sha(OUT / "SOURCE_QUALIFIED_BRIEFS.md"),
        "safe_counts_sha256": sha(OUT / "SAFE_COUNTS.json"),
    }
    for key, digest in values.items():
        if audit.get(key) != digest:
            raise ValueError(f"B4v5 source-projection audit SHA mismatch: {key}")
    if projected["frozen_b4v4c_private_sha256"] != values["prior_b4v4c_private_sha256"]:
        raise ValueError("B4v5 source projection not tied to frozen B4v4c")
    if projected["reviewed_terminology_correction_sha256"] != values["reviewed_correction_sha256"]:
        raise ValueError("B4v5 selected correction SHA mismatch")
    if not (
        metrics["llm_requests"] == 0
        and metrics["case_count"] == 4
        and metrics["source_item_count"] == 78
        and metrics["source_qualified_item_count"] == 64
        and metrics["excluded_item_count"] == 14
        and metrics["source_qualification_candidate_count"] == 23
        and metrics["source_behavioral_expectation_candidate_count"] == 7
        and metrics["application_condition_candidate_count"] == 1
        and metrics["distinct_eligibility_graph_count"] == 2
        and metrics["corrected_reviewed_terminology_items"] == 1
        and metrics["suppressed_v4_model_claims_due_to_translation_repair"] == 2
        and metrics["semantically_accepted_employer_facts"] == 0
        and metrics["production_database_written"] is False
        and metrics["unseen_generalization_established"] is False
        and metrics["independent_blind_human_review"] is False
    ):
        raise ValueError("B4v5 expected counts or authority boundary changed")
    cases = projected["cases"]
    if tuple(c["source_job_id"] for c in cases) != ("tNhZ", "tMps", "tNDx", "tMjm"):
        raise ValueError("B4v5 four-case source identity changed")
    correction = reviewed["corrections"][0]
    for index, old_case in enumerate(prior["cases"]):
        job = old_case["source_job_id"]
        rebuilt = project_source_qualified_case(
            old_case, correction=correction if job == "tNDx" else None
        )
        if rebuilt != cases[index]:
            raise ValueError(f"B4v5 projection replay differs from frozen source: {job}")
        all_source = {
            item["item_id"]
            for item in old_case["candidate"]["items"]
            if item["translation"] is not None
        }
        displayed = {item["source_item_id"] for item in rebuilt["source_qualified_items"]}
        if displayed != all_source:
            raise ValueError(f"B4v5 dropped a selected source item: {job}")
        for group_items in rebuilt["groups"].values():
            if any(
                item["authority"] != "B2_B3_source_qualified_candidate_not_accepted_fact"
                for item in group_items
            ):
                raise ValueError("B4v5 assigned accepted authority to candidate evidence")

    middle = cases[1]["eligibility_alternative_candidates"][0]["root"]
    if middle["kind"] != "any_of" or len(middle["children"]) != 2:
        raise ValueError("Middle/Senior root OR was lost")
    if any(branch["kind"] != "all_of" for branch in middle["children"]):
        raise ValueError("Middle/Senior branch requirements were flattened")
    cert = cases[2]["eligibility_alternative_candidates"][0]["root"]
    if cert["kind"] != "any_of" or len(cert["children"]) != 2:
        raise ValueError("Certificate / knowledge OR was lost")
    if cases[3]["groups"].get("work_duty") or cases[3]["v4_model_candidates"] is not None:
        raise ValueError("Qualification-only source case fabricated duties")
    named_item = next(
        item
        for item in cases[2]["source_qualified_items"]
        if item["source_item_id"] == correction["source_item_id"]
    )
    if (
        "Fadak" not in named_item["target_text_candidate"]
        or "FDC" in named_item["target_text_candidate"]
        or named_item["b4_reviewed_terminology_overlay"] is None
        or "فدک" not in named_item["original_text"]
    ):
        raise ValueError("Reviewed source-owned named entity was lost")
    if any("\u0600" <= char <= "\u06ff" for char in json.dumps(metrics)):
        raise ValueError("Private original-language text leaked into safe metrics")
    return {
        "status": "PASS_EXPOSED_SOURCE_QUALIFIED_PRESENTATION_NO_SEMANTIC_PROMOTION",
        "jobs": len(cases),
        "preserved_source_items": metrics["source_item_count"],
        "visible_source_qualified_items": metrics["source_qualified_item_count"],
        "alternative_eligibility_graphs": metrics["distinct_eligibility_graph_count"],
        "reviewed_name_corrections": metrics["corrected_reviewed_terminology_items"],
        "removed_stale_model_claims": metrics[
            "suppressed_v4_model_claims_due_to_translation_repair"
        ],
        "model_calls": 0,
        "accepted_facts": 0,
        "unseen_verified": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
