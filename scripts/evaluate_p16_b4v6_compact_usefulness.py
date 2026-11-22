"""Read-only exposed-cohort B4v6 question-first presentation experiment.

The preregistered protocol at e830c3c is upstream of this implementation.
Never fetch new postings, call any model, mutate accepted state, or treat
exposed source-navigation measurements as human usefulness/semantic accuracy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from collections import Counter
from pathlib import Path
from typing import Any

from jobhunter.source_qualified_b4v6 import (
    _node_sources,
    build_compact_decision_view,
    render_compact_decision_views,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19"
V5 = BASE / "source-projection-v5c/PRIVATE_SOURCE_PROJECTIONS.json"
V5_MARKDOWN = BASE / "source-projection-v5c/SOURCE_QUALIFIED_BRIEFS.md"
BASELINE = BASE / "primary-v4c/B4_BASELINE_COMPARISON.json"
PRIVATE_OUT = ROOT / "data/local-acceptance/p16-b4v6-compact-2026-11-22/v1"
PUBLIC_OUT = (
    ROOT / "docs/working-memory/2026-11-22_p16_b4v6_compact/"
    "SAFE_EXPOSED_COMPACT_DECISION_NAVIGATION.json"
)
FROZEN_PROTOCOL = (
    ROOT / "docs/working-memory/2026-11-22_P16_B4V6_COMPACT_DECISION_VIEW_FROZEN_PROTOCOL.md"
)
VERSIONED_MODULE = ROOT / "src/jobhunter/source_qualified_b4v6.py"
EXPECTED_CASES = ("tNhZ", "tMps", "tNDx", "tMjm")
EXPECTED_PROTOCOL_COMMIT = "e830c3c"
EXPECTED_BASELINE_SHA = "e7d6b37235136bd98df568240ae36e1a05deb79c2ccf5ed58ac9e9eda22a279d"
EXPECTED_PROJECTIONS_SHA = "a9ea424cfa497620799600947d31ee3906f8b351a959d8325c983dc5abc63a27"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Expected frozen top-level JSON mapping")
    return data


def serialize(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _chars(items: list[dict[str, Any]], *, compact: bool) -> int:
    if compact:
        return sum(len(x["original_text"]) + len(x["english_reading_aid"]) for x in items)
    return sum(len(x["original_text"]) + len(x["target_text_candidate"]) for x in items)


def assess_question(
    *,
    task: dict[str, Any],
    prior_task_evidence: dict[str, Any],
    view: dict[str, Any],
) -> dict[str, Any]:
    # This is only a source-evidence *navigation* metric. It does not
    # re-evaluate human comprehension or the true employer semantics.
    required = {x["source_item_id"] for x in prior_task_evidence["source_anchors"]}
    full = {x["source_item_id"] for x in view["source_drilldown"]}
    visible = set(view["default_visible_source_item_ids"])
    alt = prior_task_evidence["alternative_graph"]
    if alt is not None:
        candidate = next(
            (
                graph
                for graph in view["sections"]["eligibility"]["unreviewed_candidate_graphs"]
                if graph["graph_id"] == alt["graph_id"]
            ),
            None,
        )
        if candidate is None:
            raise ValueError("B4v6 source-backed eligibility path was omitted")
        if candidate["root"]["kind"] != alt["root_operator"]:
            raise ValueError("B4v6 candidate OR/AND meaning changed")
        refs = _node_sources(candidate["root"])
        visible |= refs
        required |= set(task.get("parents", ()))
        if not set(task.get("parents", ())).issubset(refs):
            raise ValueError("B4v6 eligibility graph lost original parent source location")
    if not required and task["kind"] == "duties" and task["expected_count"] == 0:
        visibility = (
            "immediate_no_separate_duties_not_no_real_work"
            if view["sections"]["what_work"]["candidate_count"] == 0
            else "contradicts_source_duty_absence_review"
        )
        hidden: set[str] = set()
    elif not required.issubset(full):
        visibility = "source_evidence_lost"
        hidden = required - full
    else:
        hidden = required - visible
        visibility = "immediate_source_navigation" if not hidden else "source_drilldown_needed"
    return {
        "task_id": task["id"],
        "source_job_id": task["case"],
        "kind": task["kind"],
        "prior_assistant_verdict": task["verdict"],
        "navigation_state": visibility,
        "required_source_item_ids": sorted(required),
        "hidden_required_source_item_ids": sorted(hidden),
        "hidden_required_source_item_count": len(hidden),
        "full_evidence_present": visibility
        not in {"source_evidence_lost", "contradicts_source_duty_absence_review"},
        "answer_semantics_independently_certified": False,
        "human_reading_time_measured": False,
    }


def evaluate() -> tuple[dict[str, Any], dict[str, Any], str]:
    # A previous separate, frozen study owns the nine questions and integrity
    # checks. Do NOT embed the task source IDs in the new display engine.
    prior = runpy.run_path(str(ROOT / "scripts/evaluate_p16_exposed_usefulness.py"))
    prior["frozen_inputs"]()
    if sha(BASELINE) != EXPECTED_BASELINE_SHA or sha(V5) != EXPECTED_PROJECTIONS_SHA:
        raise ValueError("Frozen original baseline/projection drift")
    if not FROZEN_PROTOCOL.is_file():
        raise ValueError("B4v6 frozen protocol missing")
    old_safe, _ = prior["evaluate"]()
    if old_safe["status"] != "PASS_OFFLINE_EXPOSED_TASK_EVIDENCE_NOT_USER_VALUE_OR_B5":
        raise ValueError("Prior source-grounded usefulness audit did not replay")

    projections = read(V5)
    cases = projections["cases"]
    if tuple(case["source_job_id"] for case in cases) != EXPECTED_CASES:
        raise ValueError("Original four exposed B4v5 cases changed")
    views = [build_compact_decision_view(case) for case in cases]
    markdown = render_compact_decision_views(views)
    if not markdown or not V5_MARKDOWN.is_file():
        raise ValueError("Expected existing B4v5 reading surface unavailable")
    verbose = V5_MARKDOWN.read_text(encoding="utf-8")
    if not verbose.strip():
        raise ValueError("Empty frozen B4v5 presentation")
    # B4v5's detailed markdown includes all source-qualified items and all
    # graph branches; count it as a display-size proxy, not a semantic baseline.
    baseline = read(BASELINE)
    results = []
    checks = []
    for case, view in zip(cases, views, strict=True):
        if (
            case["source_job_id"] != view["source_job_id"]
            or case["source_version"] != view["source_version"]
            or view["accepted_employer_facts"] != 0
            or view["source_qualified_item_count"] != len(view["source_drilldown"])
            or len({x["source_item_id"] for x in view["source_drilldown"]})
            != len(view["source_drilldown"])
        ):
            raise ValueError("Compact source identity, authority or drilldown drift")
        prior["baseline_state"](baseline, case)
        original_items = {item["source_item_id"]: item for item in case["source_qualified_items"]}
        for item in view["source_drilldown"]:
            original = original_items[item["source_item_id"]]
            if (
                item["original_text"] != original["original_text"]
                or item["source_span_sha256"] != original["source_span_sha256"]
                or item["english_reading_aid"] != original["target_text_candidate"]
                or item["category_candidate"] != original["category_candidate"]
                or item["strength_candidate"] != original["strength_candidate"]
            ):
                raise ValueError("B4v6 original-source drilldown damaged or strengthened")
        if (
            view["corrected_translation_item_ids"] != case["corrected_translation_item_ids"]
            or view["suppressed_prior_model_claims"]
            != case["v4_model_claims_suppressed_due_to_translation_review"]
            or len(view["sections"]["eligibility"]["unreviewed_candidate_graphs"])
            != len(case["eligibility_alternative_candidates"])
        ):
            raise ValueError("B4v6 dropped reviewed correction, graph or model-suppression guard")
        metrics = {
            "source_item_count": len(case["source_qualified_items"]),
            "default_visible_item_count": view["default_visible_evidence_item_count"],
            "hidden_source_item_count": (
                len(case["source_qualified_items"]) - view["default_visible_evidence_item_count"]
            ),
            "original_english_chars_verbose": _chars(case["source_qualified_items"], compact=False),
            "original_english_chars_default": _chars(
                [
                    item
                    for item in view["source_drilldown"]
                    if item["source_item_id"] in view["default_visible_source_item_ids"]
                ],
                compact=True,
            ),
            "eligibility_graphs": len(case["eligibility_alternative_candidates"]),
            "model_claims_suppressed": len(
                case["v4_model_claims_suppressed_due_to_translation_review"]
            ),
            "reviewed_translation_corrections": len(case["corrected_translation_item_ids"]),
            "excluded_source_items": case["excluded_source_item_count"],
            "b4_model_outcome": case["b4_analysis_outcome"],
        }
        checks.append(metrics)

    for task in prior["TASKS"]:
        case_index = EXPECTED_CASES.index(task["case"])
        evidence = prior["task_evidence"](cases[case_index], task)
        results.append(
            assess_question(task=task, prior_task_evidence=evidence, view=views[case_index])
        )
    if len(results) != 9:
        raise ValueError("B4v6 changed the frozen nine-question set")
    if any(not r["full_evidence_present"] for r in results):
        raise ValueError("B4v6 lost required source evidence or a duty abstention")

    totals = Counter(result["navigation_state"] for result in results)
    full_count = sum(c["source_item_count"] for c in checks)
    default_count = sum(c["default_visible_item_count"] for c in checks)
    plain_full_chars = sum(c["original_english_chars_verbose"] for c in checks)
    plain_default_chars = sum(c["original_english_chars_default"] for c in checks)
    public = {
        "contract": "jobhunter-p16-b4v6-compact-usefulness-exposed-v1",
        "status": "PASS_EXPOSED_COMPACT_PRESENTATION_ENGINEERING_NOT_USER_BENEFIT",
        "frozen_protocol_preimplementation_commit": EXPECTED_PROTOCOL_COMMIT,
        "cohort": "four_previously_exposed_original_source_jobs",
        "case_count": 4,
        "predeclared_task_count": 9,
        "original_B4v5_source_qualified_items": full_count,
        "B4v6_immediately_visible_source_items": default_count,
        "B4v6_full_drilldown_source_items": sum(len(v["source_drilldown"]) for v in views),
        "B4v5_original_plus_english_evidence_chars": plain_full_chars,
        "B4v6_visible_original_plus_english_evidence_chars": plain_default_chars,
        "B4v5_markdown_chars": len(verbose),
        "B4v6_markdown_chars": len(markdown),
        "navigation_state_counts": dict(sorted(totals.items())),
        "task_all_original_evidence_available": all(r["full_evidence_present"] for r in results),
        "tasks_requiring_drilldown": sum(
            r["navigation_state"] == "source_drilldown_needed" for r in results
        ),
        "source_refs_behind_drilldown_for_selected_tasks": sum(
            r["hidden_required_source_item_count"] for r in results
        ),
        "eligibility_candidate_graphs_retained": sum(c["eligibility_graphs"] for c in checks),
        "translation_corrections_retained": sum(
            c["reviewed_translation_corrections"] for c in checks
        ),
        "model_claims_still_suppressed": sum(c["model_claims_suppressed"] for c in checks),
        "existing_v30_valid_same_source_artifact_count": 0,
        "code_sha256": {
            "src/jobhunter/source_qualified_b4v6.py": sha(VERSIONED_MODULE),
        },
        "frozen_inputs_sha256": {
            str(V5.relative_to(ROOT)): sha(V5),
            str(BASELINE.relative_to(ROOT)): sha(BASELINE),
            str(V5_MARKDOWN.relative_to(ROOT)): sha(V5_MARKDOWN),
            str(FROZEN_PROTOCOL.relative_to(ROOT)): sha(FROZEN_PROTOCOL),
        },
        "new_model_http_requests": 0,
        "new_source_requests": 0,
        "new_accepted_employer_facts": 0,
        "production_database_modified": False,
        "public_corpus_modified": False,
        "B5_independent_generalization_accepted": False,
        "B6_production_promotion_authorized": False,
        "blind_independent_human_review": False,
        "user_time_saved_measured": False,
        "semantic_accuracy_superiority_established": False,
        "limitations": [
            "Display-size and evidence-navigation proxies are not measured human reading time",
            "Nine selected high-risk questions across four previously "
            "exposed cases are not representative",
            "Original-first assistant review is not independent applicant comprehension",
            "Source-bound B2 categories and B3 translations remain candidate-only",
            "No valid same-source English v30 semantic-output comparison exists",
            "Full source drilldown remains required for hidden evidence and ambiguous eligibility",
        ],
    }
    private = {
        "contract": "jobhunter-p16-b4v6-private-exposed-navigation-review-v1",
        "candidate_views": views,
        "tasks": results,
        "per_case_metrics": checks,
        "read_only": True,
    }
    return public, private, markdown


def write_once() -> dict[str, Any]:
    if PRIVATE_OUT.exists() or PUBLIC_OUT.exists():
        raise ValueError("B4v6 research outputs already sealed; verify instead")
    public, private, markdown = evaluate()
    PRIVATE_OUT.mkdir(parents=True)
    raw = PRIVATE_OUT / "PRIVATE_B4V6_CANDIDATE_AND_TASK_REVIEW.json"
    demo = PRIVATE_OUT / "B4V6_COMPACT_FIRST_VIEW.md"
    raw.write_bytes(serialize(private))
    demo.write_text(markdown, encoding="utf-8")
    public["private_review_sha256"] = sha(raw)
    public["private_markdown_sha256"] = sha(demo)
    PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT.write_bytes(serialize(public))
    return {
        key: public[key]
        for key in (
            "status",
            "predeclared_task_count",
            "navigation_state_counts",
            "B4v6_immediately_visible_source_items",
            "B4v5_markdown_chars",
            "B4v6_markdown_chars",
            "B5_independent_generalization_accepted",
        )
    }


def verify() -> dict[str, Any]:
    public, private, markdown = evaluate()
    raw = PRIVATE_OUT / "PRIVATE_B4V6_CANDIDATE_AND_TASK_REVIEW.json"
    demo = PRIVATE_OUT / "B4V6_COMPACT_FIRST_VIEW.md"
    if (
        not raw.is_file()
        or raw.read_bytes() != serialize(private)
        or not demo.is_file()
        or demo.read_text(encoding="utf-8") != markdown
    ):
        raise ValueError("B4v6 sealed local research output changed")
    public["private_review_sha256"] = sha(raw)
    public["private_markdown_sha256"] = sha(demo)
    if not PUBLIC_OUT.is_file() or PUBLIC_OUT.read_bytes() != serialize(public):
        raise ValueError("B4v6 public-safe scorecard changed")
    return {
        key: public[key]
        for key in (
            "status",
            "predeclared_task_count",
            "navigation_state_counts",
            "B4v6_immediately_visible_source_items",
            "B4v5_markdown_chars",
            "B4v6_markdown_chars",
            "B5_independent_generalization_accepted",
        )
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-once", action="store_true")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    if args.preview:
        data, _, _ = evaluate()
        print(
            json.dumps(
                {
                    key: data[key]
                    for key in (
                        "status",
                        "navigation_state_counts",
                        "B4v5_markdown_chars",
                        "B4v6_markdown_chars",
                        "B4v6_immediately_visible_source_items",
                    )
                },
                sort_keys=True,
            )
        )
    elif args.write_once:
        print(json.dumps(write_once(), sort_keys=True))
    else:
        print(json.dumps(verify(), sort_keys=True))
