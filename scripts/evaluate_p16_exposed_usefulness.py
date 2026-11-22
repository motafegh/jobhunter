"""Offline, source-bound B4v5 usefulness inspection of four already exposed ads.

A finite, assistant-reviewed diagnostic task matrix is frozen here. The script
checks exact original spans and prior frozen B4/v30/v9 evidence, but does NOT
certify model semantics, publish original employer text, or use providers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from collections import Counter
from pathlib import Path
from typing import Any

from jobhunter.source_qualified_b4v5 import digest_text

ROOT = Path(__file__).resolve().parents[1]
B4 = Path("data/local-acceptance/p16-stage-b4-2026-11-19")
PROJECTION = B4 / "source-projection-v5c/PRIVATE_SOURCE_PROJECTIONS.json"
BASELINE = B4 / "primary-v4c/B4_BASELINE_COMPARISON.json"
PRIVATE_OUT = ROOT / "data/local-acceptance/p16-exposed-usefulness-2026-11-22/v1"
PUBLIC_OUT = (
    ROOT
    / "docs/working-memory/2026-11-22_p16_utility"
    / "SAFE_EXPOSED_JOB_UNDERSTANDING_USEFULNESS.json"
)
INPUT_DIGESTS = {
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/B4_BASELINE_COMPARISON.json"
    ): "e7d6b37235136bd98df568240ae36e1a05deb79c2ccf5ed58ac9e9eda22a279d",
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/PRIVATE_B4_CANDIDATES.json"
    ): "8d7155448f0311ad0fff4e3d739c4fd3fb57dca33d08e46815e2618686837bc3",
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/"
        "primary-v4c/B4_EXPOSED_ASSISTANT_SEMANTIC_REVIEW.json"
    ): "a3a61f5cc35fa460102d0c0960c7ff3a9c58536d3ed74dcb1448315e92087d26",
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/"
        "source-projection-v5c/PRIVATE_SOURCE_PROJECTIONS.json"
    ): "a9ea424cfa497620799600947d31ee3906f8b351a959d8325c983dc5abc63a27",
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c/FINAL_AUDIT.json"
    ): "16078e2c8e894289cb3a5174f76d4d1fb985bba3fd76fffcf8877982d86ee6ee",
    (
        "data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json"
    ): "054c1065c54e0a1abdf27e93803dbf3feedac25859f01e2778a3e464594450f4",
    "data/jobhunter.sqlite3": "d9068fcb503860638cb2187b537e57151bea0192ff69ab7dbe381c84fb2353d8",
    "corpus/manifest.json": "7a65485c813a855d144160f1009559decaf0383dba06a089760d2101726fda4a",
}
CASES = ("tNhZ", "tMps", "tNDx", "tMjm")
BASELINE_STATES = {
    "tNhZ": ("failed_no_artifact", "no_v9_artifact"),
    "tMps": ("failed_no_artifact", "no_v9_artifact"),
    "tNDx": ("failed_no_artifact", "artifact_present_accepted"),
    "tMjm": ("rejected_candidate_no_valid_artifact", "no_v9_artifact"),
}
# Source-exposed assistant judgments. Never count these as blinded or whole-ad scores.
TASKS = (
    {
        "id": "tNhZ-work",
        "case": "tNhZ",
        "kind": "duties",
        "expected_count": 6,
        "verdict": "source_supported_visible",
        "note": "Six source-anchored task statements, not employer-required prior experience.",
    },
    {
        "id": "tNhZ-optional",
        "case": "tNhZ",
        "kind": "items",
        "anchors": {
            "s_17bb3fbd433884ce343a06b8a95c2908049a1554": ("candidate_qualification", "preferred")
        },
        "verdict": "source_supported_visible",
        "note": (
            "Original explicit advantage without mandatory prior financial/LLM "
            "familiarity. B4 model summary omitted this expectation."
        ),
    },
    {
        "id": "tMps-work",
        "case": "tMps",
        "kind": "duties",
        "expected_count": 11,
        "verdict": "partially_visible_or_uncertain",
        "note": (
            "Eleven candidate work passages displayed, including broad role-purpose "
            "phrasing; categorical completeness is not independently certified."
        ),
    },
    {
        "id": "tMps-path",
        "case": "tMps",
        "kind": "graph",
        "graph_id": "candidate_middle_or_senior",
        "parents": (
            "s_822b03f21c2da70f9e5982288a08e00a1a8ac5ef",
            "s_5c59034ad7457f23463b2a18bc255ed2b5eb9014",
        ),
        "verdict": "partially_visible_or_uncertain",
        "note": (
            "Middle/Senior OR with nested AND/OR original subspans; child English "
            "alignments not established and eligibility graph unreviewed."
        ),
    },
    {
        "id": "tNDx-work",
        "case": "tNDx",
        "kind": "duties",
        "expected_count": 5,
        "verdict": "source_supported_visible",
        "note": (
            "Five original EDR actions displayed; earlier generated model claims "
            "depending on a mistranslated name are separately withheld."
        ),
    },
    {
        "id": "tNDx-certificate-preference",
        "case": "tNDx",
        "kind": "items_and_graph",
        "anchors": {
            "s_1c2d341438db101875c5dd6548ed330f89065d03": ("behavioral_expectation", "preferred")
        },
        "graph_id": "candidate_certificate_or_knowledge",
        "parents": ("s_895ee592688fc24ae54c071319382a6123fe6c94",),
        "verdict": "partially_visible_or_uncertain",
        "note": (
            "Teamwork advantage shown; certificate OR equivalent knowledge source path "
            "preserved but not accepted as verified eligibility."
        ),
    },
    {
        "id": "tNDx-name-exam",
        "case": "tNDx",
        "kind": "items",
        "anchors": {
            "s_ae62e5aa14da3bfe232413c7ca6d01907c2878b1": ("work_duty", "not_applicable"),
            "s_580d9b8a4ccb7f042da732b483e97ee953f9272e": (
                "application_instruction",
                "not_applicable",
            ),
        },
        "requires_overlay": "s_ae62e5aa14da3bfe232413c7ca6d01907c2878b1",
        "requires_condition": "s_580d9b8a4ccb7f042da732b483e97ee953f9272e",
        "verdict": "source_supported_visible",
        "note": (
            "Exact-original-source ticket name corrected only in B4v5 and technical "
            "entrance-exam condition is visible."
        ),
    },
    {
        "id": "tMjm-work",
        "case": "tMjm",
        "kind": "duties",
        "expected_count": 0,
        "verdict": "partially_visible_or_uncertain",
        "note": (
            "Source-only view correctly does not invent distinct assigned duties; this "
            "does not assert that the real job has no duties."
        ),
    },
    {
        "id": "tMjm-remote",
        "case": "tMjm",
        "kind": "items",
        "anchors": {
            "s_cd4e80643c050912473e70566245481358d225c1": ("work_arrangement", "not_applicable")
        },
        "verdict": "source_supported_visible",
        "note": (
            "Original wording offers a remote-work possibility; it is not an applicant requirement."
        ),
    },
)
ALLOWED_VERDICTS = {
    "source_supported_visible",
    "partially_visible_or_uncertain",
    "potentially_misleading",
    "not_visible",
    "not_evaluable",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path.name}")
    return value


def frozen_inputs() -> None:
    for path, expected in INPUT_DIGESTS.items():
        if sha(ROOT / path) != expected:
            raise ValueError(f"Frozen input/production identity changed: {path}")


def original_item_integrity(item: dict[str, Any]) -> None:
    if digest_text(item["original_text"]) != item["source_span_sha256"]:
        raise ValueError("Original source-span SHA mismatch")
    if item["authority"] != "B2_B3_source_qualified_candidate_not_accepted_fact":
        raise ValueError("Candidate item has unexpected employer authority")
    if not item["source_item_id"] or not item["target_text_candidate"]:
        raise ValueError("Selected source item is not inspectable")


def graph_evidence(
    case: dict[str, Any], task: dict[str, Any], items: dict[str, Any]
) -> dict[str, Any]:
    graphs = [
        g for g in case["eligibility_alternative_candidates"] if g["graph_id"] == task["graph_id"]
    ]
    if len(graphs) != 1 or graphs[0]["root"]["kind"] != "any_of":
        raise ValueError("Required source-backed alternative graph unavailable")
    root = graphs[0]["root"]
    if len(root["children"]) != 2:
        raise ValueError("Expected two alternative eligibility branches")
    for parent in task["parents"]:
        if parent not in items or items[parent]["category_candidate"] != "candidate_qualification":
            raise ValueError("Alternative parent item was lost")
    nested: list[dict[str, Any]] = []

    def visit(node: dict[str, Any]) -> None:
        if node["kind"] in {"any_of", "all_of"}:
            for child in node["children"]:
                visit(child)
        elif node["kind"] == "original_subspan":
            if node["child_english_alignment"] != "not_established":
                raise ValueError("Invented independent English child alignment")
            nested.append(node)
        elif node["kind"] == "whole_item":
            if node["source_item_id"] not in items:
                raise ValueError("Graph leaf missing from source items")
        else:
            raise ValueError("Unknown eligibility graph node")

    visit(root)
    if not nested:
        raise ValueError("Unaligned source graph lacks original subspans")
    return {
        "graph_id": task["graph_id"],
        "root_operator": "any_of",
        "branch_count": len(root["children"]),
        "source_subspan_count": len(nested),
        "child_english_alignment": "not_established",
        "graph_authority": graphs[0]["authority"],
    }


def task_evidence(case: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    available = {x["source_item_id"]: x for x in case["source_qualified_items"]}
    if len(available) != len(case["source_qualified_items"]):
        raise ValueError("Duplicate source-qualified source ID")
    if task["kind"] not in {"duties", "items", "graph", "items_and_graph"}:
        raise ValueError("Unsupported task")
    selected: list[dict[str, Any]] = []
    if task["kind"] == "duties":
        selected = list(case["groups"].get("work_duty", []))
        if len(selected) != task["expected_count"]:
            raise ValueError("Frozen explicit-work candidate count drift")
    for source_id, (category, strength) in task.get("anchors", {}).items():
        item = available.get(source_id)
        if not item or (item["category_candidate"], item["strength_candidate"]) != (
            category,
            strength,
        ):
            raise ValueError("Task original source/category/strength evidence drift")
        selected.append(item)
    for item in selected:
        original_item_integrity(item)
    overlay_id = task.get("requires_overlay")
    if overlay_id:
        item = available[overlay_id]
        if (
            item["b4_reviewed_terminology_overlay"] is None
            or item["translation_review_state"]
            != "assistant_reviewed_original_source_terminology_overlay"
            or "Fadak" not in item["target_text_candidate"]
            or "FDC" in item["target_text_candidate"]
        ):
            raise ValueError("Reviewed source-terminology correction was lost")
    condition_id = task.get("requires_condition")
    if condition_id and not available[condition_id]["is_conditional_application_statement"]:
        raise ValueError("Explicit acceptance condition not shown")
    graph = None
    if "graph_id" in task:
        graph = graph_evidence(case, task, available)
    return {
        "source_anchors": [
            {
                "source_item_id": x["source_item_id"],
                "source_sha256": x["source_span_sha256"],
                "category_candidate": x["category_candidate"],
                "strength_candidate": x["strength_candidate"],
                "original_text": x["original_text"],
                "english_reading_aid": x["target_text_candidate"],
                "translation_review_state": x["translation_review_state"],
            }
            for x in selected
        ],
        "alternative_graph": graph,
    }


def baseline_state(baseline: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    job = case["source_job_id"]
    entry = baseline[job]
    if (
        entry["source_job_id"] != job
        or entry["job_detail_version_id"] != case["source_version"]["job_detail_version_id"]
        or entry["source_snapshot_same_as_b4"] is not True
        or (entry["v30"]["status"], entry["v9"]["status"]) != BASELINE_STATES[job]
        or entry["v30"]["valid_artifact_ids"]
    ):
        raise ValueError("No longer the frozen same-source, no-valid-v30 baseline")
    if job == "tNDx":
        if entry["v9"]["artifacts"] != [{"id": 2, "semantic_review_status": "accepted"}]:
            raise ValueError("Original-language v9 evidence status drift")
    elif entry["v9"]["artifacts"]:
        raise ValueError("Unexpected historical original-language v9 artifact")
    return {
        "same_source_snapshot": True,
        "english_v30_status": entry["v30"]["status"],
        "english_v30_valid_artifact_count": 0,
        "original_v9_status": entry["v9"]["status"],
        "original_v9_accepted_artifact_count": len(entry["v9"]["artifacts"]),
        "baseline_output_semantic_pair_comparable": False,
    }


def evaluate() -> tuple[dict[str, Any], dict[str, Any]]:
    frozen_inputs()
    result = runpy.run_path(str(ROOT / "scripts/verify_p16_b4v5_source_projection.py"))["verify"]()
    if result["status"] != "PASS_EXPOSED_SOURCE_QUALIFIED_PRESENTATION_NO_SEMANTIC_PROMOTION":
        raise ValueError("B4v5 frozen projection did not replay")
    baseline = read_json(ROOT / BASELINE)
    projections = read_json(ROOT / PROJECTION)
    cases = projections["cases"]
    if tuple(x["source_job_id"] for x in cases) != CASES:
        raise ValueError("Exposed cohort identities/order changed")
    if set(baseline) != set(CASES):
        raise ValueError("Different baseline cohort")
    if len(TASKS) != 9 or len({x["id"] for x in TASKS}) != 9:
        raise ValueError("Diagnostic tasks changed from frozen selection")
    private = {
        "contract": "jobhunter-p16-exposed-usefulness-task-review-v1",
        "reviewer": "assistant_exposed_nonblind_selection_not_independent",
        "prior_commit_frozen_protocol": "1abd1e0",
        "original_source_authority": "source_quote_only_not_verified_employer_semantics",
        "comparisons": [],
    }
    per_case = {}
    verdicts = Counter()
    for case in cases:
        job = case["source_job_id"]
        if case["accepted_employer_facts"] != 0 or case["downstream_authority"] != "none":
            raise ValueError("Unreviewed model/source content was promoted")
        current = baseline_state(baseline, case)
        tasks = []
        for task in TASKS:
            if task["case"] != job:
                continue
            if task["verdict"] not in ALLOWED_VERDICTS:
                raise ValueError("Unknown task verdict")
            evidence = task_evidence(case, task)
            tasks.append({"task_id": task["id"], "verdict": task["verdict"]})
            verdicts[task["verdict"]] += 1
            private["comparisons"].append(
                {
                    "task_id": task["id"],
                    "case_id": job,
                    "selected_exposed_source_assertion": True,
                    "judgment": task["verdict"],
                    "assistant_reasoning_summary": task["note"],
                    "evidence": evidence,
                }
            )
        per_case[job] = {
            **current,
            "b4v5_source_item_count": case["source_item_count"],
            "b4v5_visible_source_qualified_item_count": len(case["source_qualified_items"]),
            "b4v5_alternative_graph_count": len(case["eligibility_alternative_candidates"]),
            "b4_model_candidate_state": case["b4_analysis_outcome"],
            "b4v5_reviewed_translation_overlays": len(case["corrected_translation_item_ids"]),
            "b4v5_withheld_old_model_claims": len(
                case["v4_model_claims_suppressed_due_to_translation_review"]
            ),
            "task_results": tasks,
        }
    if sum(verdicts.values()) != 9:
        raise ValueError("Some selected tasks were omitted")
    safe = {
        "contract": "jobhunter-p16-exposed-usefulness-scorecard-v1",
        "status": "PASS_OFFLINE_EXPOSED_TASK_EVIDENCE_NOT_USER_VALUE_OR_B5",
        "evaluation_scope": "four_previously_exposed_jobs_nine_selected_diagnostic_questions",
        "frozen_protocol_commit": "1abd1e0",
        "frozen_input_sha256": INPUT_DIGESTS,
        "evaluator_sha256": sha(Path(__file__)),
        "candidate_version": "B4v5_existing_source_qualified_projection_only",
        "baseline_identity": "same_frozen_job_detail_source",
        "case_count": 4,
        "preselected_task_count": 9,
        "assistant_exposed_review_counts": dict(sorted(verdicts.items())),
        "source_item_count": sum(x["b4v5_source_item_count"] for x in per_case.values()),
        "visible_source_qualified_items": sum(
            x["b4v5_visible_source_qualified_item_count"] for x in per_case.values()
        ),
        "v30_valid_same_source_artifact_count": 0,
        "v30_failed_case_count": sum(
            x["english_v30_status"] == "failed_no_artifact" for x in per_case.values()
        ),
        "v30_rejected_only_case_count": sum(
            x["english_v30_status"] == "rejected_candidate_no_valid_artifact"
            for x in per_case.values()
        ),
        "v9_accepted_artifact_count": sum(
            x["original_v9_accepted_artifact_count"] for x in per_case.values()
        ),
        "same_source_model_semantic_pair_count": 0,
        "b4v5_alternative_graphs": sum(
            x["b4v5_alternative_graph_count"] for x in per_case.values()
        ),
        "b4v5_reviewed_terminology_overlays": sum(
            x["b4v5_reviewed_translation_overlays"] for x in per_case.values()
        ),
        "b4v5_withheld_old_model_claims": sum(
            x["b4v5_withheld_old_model_claims"] for x in per_case.values()
        ),
        "new_LLM_or_source_network_requests": 0,
        "accepted_employer_facts_promoted": 0,
        "production_database_modified": False,
        "public_corpus_modified": False,
        "measured_owner_time_savings": False,
        "blind_independent_human_review": False,
        "candidate_source_categories_semantically_certified": False,
        "v30_accuracy_superiority_established": False,
        "user_usefulness_advantage_established": False,
        "B5_independent_generalization_pass": False,
        "B6_promotion_authorized": False,
        "per_case": per_case,
        "limitations": [
            (
                "Same assistant, previously exposed source cohort; nine high-risk questions "
                "selected from prior failures, not a representative denominator"
            ),
            (
                "B4v5 source-role/strength/eligibility semantics remain candidate-only; "
                "original quotes are authoritative but English translations may be incomplete"
            ),
            (
                "No valid same-source v30 English output for qualitative semantic comparison; "
                "historical v9 accepted artifact is not a calibrated human assessment"
            ),
            (
                "No independently observed user decision, time saved, comprehension, reading "
                "effort, or A/B comparison"
            ),
            (
                "More displayed source items may increase reading burden; comparison measures "
                "presence and caution, not validated usability"
            ),
        ],
    }
    if any("\u0600" <= ch <= "\u06ff" for ch in json.dumps(safe, ensure_ascii=False)):
        raise ValueError("Public safe report leaked original Persian text")
    return safe, private


def serialized(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def write_once() -> None:
    if PRIVATE_OUT.exists() or PUBLIC_OUT.exists():
        raise ValueError("Immutable usefulness output exists; verification only")
    safe, private = evaluate()
    PRIVATE_OUT.mkdir(parents=True, exist_ok=False)
    private_file = PRIVATE_OUT / "PRIVATE_EXPOSED_TASK_REVIEW.json"
    private_file.write_bytes(serialized(private))
    safe["private_exposed_task_review_sha256"] = sha(private_file)
    PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT.write_bytes(serialized(safe))
    print(
        json.dumps(
            {
                "status": safe["status"],
                "case_count": safe["case_count"],
                "diagnostic_task_count": safe["preselected_task_count"],
                "task_review_states": safe["assistant_exposed_review_counts"],
                "valid_v30_artifacts": safe["v30_valid_same_source_artifact_count"],
                "new_model_requests": 0,
            },
            sort_keys=True,
        )
    )


def verify() -> dict[str, Any]:
    safe, private = evaluate()
    private_file = PRIVATE_OUT / "PRIVATE_EXPOSED_TASK_REVIEW.json"
    if not private_file.is_file() or private_file.read_bytes() != serialized(private):
        raise ValueError("Private frozen source/task review drift")
    safe["private_exposed_task_review_sha256"] = sha(private_file)
    if PUBLIC_OUT.read_bytes() != serialized(safe):
        raise ValueError("Public safe task scorecard does not replay")
    return {
        "status": "PASS_REPLAY_EXPOSED_USEFULNESS_EVIDENCE_NO_SEMANTIC_PROMOTION",
        "tasks": safe["preselected_task_count"],
        "cases": safe["case_count"],
        "valid_v30_artifacts": 0,
        "B5_pass": False,
        "B6_authorized": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-once", action="store_true")
    args = parser.parse_args()
    if args.write_once:
        write_once()
    else:
        print(json.dumps(verify(), sort_keys=True))
