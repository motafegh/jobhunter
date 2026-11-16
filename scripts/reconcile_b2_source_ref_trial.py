"""Offline, source-safe B2 v3 vs source-referenced v4 diagnostic comparison.

No model calls, source fetches, employer-fact acceptance or production writes.
A source ID proves the reference targets a saved candidate item, not semantic truth.
The 12 assistant review judgments are previously exposed, NOT an accuracy sample.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from probe_b2_model_source_refs import (
    CONTRACT,
    DB_SHA256,
    FIELD_ORDER,
    MODEL,
    normalize_model_output,
)
from reconcile_b2_native_trials import _parse_model_json

REVIEW_CONTRACT = "jobhunter-b2-native-source-reference-exposed-review-v1"
BASELINE_CONTRACT = "jobhunter-b2-original-context-native-corrective-v3"
OUT_CONTRACT = "jobhunter-b2-native-source-reference-comparison-v1"
CASES = ("tNhZ", "tMps", "tNDx", "tMjm")
REVIEW_AUTHORITY = "assistant_prior_context_exposed_not_independent_or_blind"


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read_object(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_bytes())
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object")
    return parsed


def reconcile(
    trial: dict[str, Any],
    baseline: dict[str, Any],
    review: dict[str, Any],
    old_review: dict[str, Any],
    metrics: dict[str, Any],
    raw_trial_sha: str,
) -> dict[str, Any]:
    if (
        trial.get("contract") != CONTRACT
        or trial.get("source_database_sha256") != DB_SHA256
        or trial.get("model") != MODEL
        or trial.get("reasoning") != "off"
        or trial.get("authority") != "research_only_no_downstream_reuse"
        or trial.get("accepted_employer_facts") != 0
        or trial.get("stopped_early") is not False
        or baseline.get("contract") != BASELINE_CONTRACT
        or baseline.get("source_database_sha256") != DB_SHA256
        or baseline.get("model") != MODEL
        or baseline.get("reasoning") != "off"
        or review.get("contract") != REVIEW_CONTRACT
        or review.get("source_snapshot_sha256") != DB_SHA256
        or review.get("private_model_run_sha256") != raw_trial_sha
        or review.get("prompt_sha256") != trial.get("prompt_sha256")
        or review.get("review_authority") != REVIEW_AUTHORITY
        or review.get("semantic_acceptance") is not False
        or review.get("b2_gate") != "OPEN_NO_PROMOTION"
        or old_review.get("source_sha256") != DB_SHA256
        or metrics.get("private_trial_sha256") != raw_trial_sha
        or metrics.get("prompt_sha256") != trial.get("prompt_sha256")
        or metrics.get("b2_semantic_gate") != "OPEN_NO_PROMOTION"
    ):
        raise ValueError("Source/model/review/metric provenance differs")
    if (
        set(trial.get("cases", {})) != set(CASES)
        or set(baseline.get("cases", {})) != set(CASES)
        or set(metrics.get("cases", {})) != set(CASES)
    ):
        raise ValueError("Unexpected cohort identity or coverage")
    prior = {(r["source_job_id"], r["check"]): r for r in old_review["reviewed_checks"]}
    observed = {(r["source_job_id"], r["check"]): r for r in review["reviewed_checks"]}
    if len(prior) != 12 or len(observed) != 12 or set(prior) != set(observed):
        raise ValueError("Selected diagnostic checks changed")
    if any(
        r["v4_outcome"] not in {"pass", "partial", "fail", "unresolved"} or not r.get("rationale")
        for r in observed.values()
    ):
        raise ValueError("Invalid source-referenced assistant check")

    per_case = {}
    states = Counter()
    v3_claims = v4_claims = 0
    v3_elapsed = v4_elapsed = 0.0
    v3_output_tokens = v4_output_tokens = 0
    for job in CASES:
        new_case = trial["cases"][job]
        old_case = baseline["cases"][job]
        safe_case = metrics["cases"][job]
        if (
            new_case.get("outcome") != "response"
            or new_case.get("structured") is not True
            or old_case.get("outcome") != "response"
            or new_case.get("source_semantic_sha256") != old_case.get("source_semantic_sha256")
            or safe_case.get("source_semantic_sha256") != new_case.get("source_semantic_sha256")
            or new_case.get("content_sha256") != sha(new_case["content"].encode("utf-8"))
            or safe_case.get("content_sha256") != new_case["content_sha256"]
        ):
            raise ValueError("Model output/source identity mismatch")
        source_map = {item["number"]: item["anchor_id"] for item in new_case["source_items"]}
        if set(source_map) != set(range(len(new_case["source_items"]))):
            raise ValueError("Invalid or repeated source item numbers")
        claims, diagnostics = normalize_model_output(new_case["content"], source_map)
        if (
            diagnostics["invalid_reference_claims"] != new_case["invalid_ref_claims"]
            or new_case["parsed_claims"]
            != [
                {
                    "field": c.field,
                    "index": c.index,
                    "text": c.text,
                    "source_anchor_ids": list(c.source_anchor_ids),
                    "link_provenance": c.link_provenance,
                }
                for c in claims
            ]
            or new_case["field_counts"] != diagnostics["field_counts"]
        ):
            raise ValueError("New model parsing or source references are not reproducible")
        old_parsed = _parse_model_json(old_case["content"])
        if any(not isinstance(old_parsed[k], list) for k in FIELD_ORDER):
            raise ValueError("Unparseable baseline model response")
        old_count = sum(len(old_parsed[k]) for k in FIELD_ORDER)
        counters = Counter(x["grounding_state"] for x in new_case["reconciled_claims"])
        for state, n in counters.items():
            states[state] += n
        if (
            new_case["model_claim_count"] != len(claims)
            or safe_case["model_claim_count"] != len(claims)
            or safe_case["link_counts"] != dict(counters)
        ):
            raise ValueError("Published source-link counts mismatch")
        per_case[job] = {
            "v3_claims": old_count,
            "source_ref_claims": len(claims),
            "source_ref_claims_with_valid_links": len(claims) - counters["unlinked_unknown"],
            "source_ref_unlinked_unknown": counters["unlinked_unknown"],
            "source_ref_candidate_disagreements": counters["source_candidate_disagreement"],
            "source_ref_invalid_claim_citations": len(diagnostics["invalid_reference_claims"]),
            "v3_elapsed_seconds": old_case["elapsed_seconds"],
            "source_ref_elapsed_seconds": new_case["elapsed_seconds"],
        }
        v3_claims += old_count
        v4_claims += len(claims)
        v3_elapsed += old_case["elapsed_seconds"]
        v4_elapsed += new_case["elapsed_seconds"]
        v3_output_tokens += old_case["stats"]["total_output_tokens"]
        v4_output_tokens += new_case["stats"]["total_output_tokens"]
    return {
        "contract": OUT_CONTRACT,
        "source_snapshot_sha256": DB_SHA256,
        "model": MODEL,
        "source_ref_prompt_sha256": trial["prompt_sha256"],
        "raw_source_ref_trial_sha256": raw_trial_sha,
        "review_authority": REVIEW_AUTHORITY,
        "development_cases_exposed": True,
        "independent_accuracy": False,
        "source_link_equals_semantic_entailment": False,
        "semantic_acceptance": False,
        "b2_semantic_gate": "OPEN_NO_PROMOTION",
        "production_promotions": 0,
        "sample_cases": len(CASES),
        "v3_claim_count": v3_claims,
        "source_ref_claim_count": v4_claims,
        "source_ref_valid_linked_claim_count": (v4_claims - states["unlinked_unknown"]),
        "source_ref_unlinked_unknown": states["unlinked_unknown"],
        "source_ref_candidate_disagreements": states["source_candidate_disagreement"],
        "v3_total_elapsed_seconds": round(v3_elapsed, 3),
        "source_ref_total_elapsed_seconds": round(v4_elapsed, 3),
        "v3_total_output_tokens": v3_output_tokens,
        "source_ref_total_output_tokens": v4_output_tokens,
        "assistant_exposed_selected_checks": {
            "previous_v3": dict(Counter(r["v3_outcome"] for r in prior.values())),
            "source_ref_v4": dict(Counter(r["v4_outcome"] for r in observed.values())),
        },
        "per_case": per_case,
        "decision": (
            "Model source citation feasibility established on exposed examples; "
            "semantics still fail material requirements/duty/alternative checks. "
            "Retain research only, do not promote or prompt-iterate blindly."
        ),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("trial", "baseline", "review", "old-review", "metrics", "out"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    root = Path.cwd().resolve()
    private = root / "data/local-acceptance"
    safe = root / "docs/working-memory/2026-11-16_p16_b2"
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter root")
    if any(not path.resolve().is_relative_to(private) for path in (a.trial, a.baseline)):
        raise ValueError("Raw model records must stay private")
    if any(
        not path.resolve().is_relative_to(safe)
        for path in (a.review, a.old_review, a.metrics, a.out)
    ):
        raise ValueError("Safe review/comparison must remain in dedicated source-safe directory")
    if a.out.exists():
        raise FileExistsError("Comparison must not overwrite previous evidence")
    result = reconcile(
        read_object(a.trial),
        read_object(a.baseline),
        read_object(a.review),
        read_object(a.old_review),
        read_object(a.metrics),
        sha(a.trial.read_bytes()),
    )
    a.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "v3_claims": result["v3_claim_count"],
                "source_ref_claims": result["source_ref_claim_count"],
                "linked": result["source_ref_valid_linked_claim_count"],
                "candidate_disagreements": result["source_ref_candidate_disagreements"],
                "decision": result["b2_semantic_gate"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
