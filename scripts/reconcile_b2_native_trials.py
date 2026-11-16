"""Offline, source-safe reconciliation of two B2 original-context LLM trials.

This is an evidence and acceptance-boundary auditor, not a semantic judge.
Existing review findings are assistant diagnostic observations, never an
independent human review or authorization for downstream facts.

Run from JobHunter root with frozen, ignored, local raw trial records:
python scripts/reconcile_b2_native_trials.py --v2 ... --v3 ... \
  --review docs/working-memory/2026-11-16_p16_b2/SAFE_ASSISTANT_SOURCE_SEMANTIC_CHECKS.json \
  --out docs/working-memory/2026-11-16_p16_b2/SAFE_RECONCILED_B2_GATE.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

CASES = ("tNhZ", "tMps", "tNDx", "tMjm")
SEVEN_FIELDS = (
    "duties",
    "requirements",
    "preferences",
    "alternatives",
    "arrangements",
    "uncertainties",
    "work_implied_capabilities",
)
SOURCE_B0_SHA = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
ALLOWED_OUTCOMES = {"pass", "partial", "fail", "unresolved"}


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_bytes())
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object for B2 evidence")
    return data


def _parse_model_json(text: str) -> dict[str, Any]:
    content = text.strip()
    fence = chr(96) * 3
    if content.startswith(fence):
        lines = content.splitlines()
        if len(lines) < 3 or lines[-1].strip() != fence:
            raise ValueError("Unclosed model JSON fence")
        content = "\n".join(lines[1:-1])
    parsed = json.loads(content)
    if not isinstance(parsed, dict):
        raise ValueError("Model output is not a JSON object")
    if not all(isinstance(parsed.get(field), list) for field in SEVEN_FIELDS):
        raise ValueError("Missing one or more of the seven model output arrays")
    return parsed


def reconcile(v2: dict[str, Any], v3: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    """Reconcile source/prompt/runtime provenance without granting semantic truth."""
    if (
        v2.get("contract") != "jobhunter-b2-original-context-native-reasoning-off-v2"
        or v3.get("contract") != "jobhunter-b2-original-context-native-corrective-v3"
        or v2.get("source_database_sha256") != SOURCE_B0_SHA
        or v3.get("source_database_sha256") != SOURCE_B0_SHA
        or review.get("source_sha256") != SOURCE_B0_SHA
    ):
        raise ValueError("Inconsistent B2 source snapshot or model trial version")
    if (
        v2.get("reasoning") != "off"
        or v3.get("reasoning") != "off"
        or v2.get("model") != v3.get("model")
        or v2.get("authority") != "research_only_no_downstream_reuse"
        or v3.get("authority") != "research_only_no_downstream_reuse"
    ):
        raise ValueError("Unexpected model setting, model identity or authority")
    if (
        review.get("review_authority")
        != "assistant_prior_context_exposed_not_independent_human_or_blind"
        or review.get("semantic_acceptance") is not False
        or review.get("one_corrective_trial_only") is not True
        or review.get("not_generalization_accuracy") is not True
        or review.get("prompt_versions")
        != {
            "native_v2": v2.get("prompt_sha256"),
            "corrective_v3": v3.get("prompt_sha256"),
        }
        or v2.get("prompt_sha256") == v3.get("prompt_sha256")
    ):
        raise ValueError("Assistant review authority or prompt provenance is inconsistent")
    if set(v2.get("cases", {})) != set(CASES) or set(v3.get("cases", {})) != set(CASES):
        raise ValueError("B2 model case coverage changed")
    if len(review.get("reviewed_checks", [])) != 12:
        raise ValueError("Source diagnostic check count changed")
    seen_checks: set[tuple[str, str]] = set()
    outcome_counts: dict[str, Counter[str]] = {
        "native_v2": Counter(),
        "corrective_v3": Counter(),
    }
    durations: dict[str, dict[str, float]] = {"native_v2": {}, "corrective_v3": {}}
    item_counts: dict[str, dict[str, dict[str, int]]] = {
        "native_v2": {},
        "corrective_v3": {},
    }
    semantic_versions = {"native_v2": v2, "corrective_v3": v3}
    for label, trial in semantic_versions.items():
        for job in CASES:
            case = trial["cases"][job]
            if (
                case.get("source_job_id") != job
                or case.get("outcome") != "response"
                or case.get("stats", {}).get("reasoning_output_tokens") != 0
                or not isinstance(case.get("content"), str)
                or not case.get("content")
                or case.get("content_sha256") != _sha(case["content"].encode("utf-8"))
            ):
                raise ValueError("B2 model output missing, altered, or reasoning not off")
            parsed = _parse_model_json(case["content"])
            durations[label][job] = case["elapsed_seconds"]
            item_counts[label][job] = {field: len(parsed[field]) for field in SEVEN_FIELDS}
    for check in review["reviewed_checks"]:
        job = check.get("source_job_id")
        cid = check.get("check")
        if job not in CASES or not isinstance(cid, str) or not cid:
            raise ValueError("Unexpected assistant review check identifier")
        pair = (job, cid)
        if pair in seen_checks:
            raise ValueError("Duplicated assistant review check")
        seen_checks.add(pair)
        if (
            check.get("authority") != "assistant_diagnostic_not_employer_or_independent"
            or check.get("v2_source_semantic_sha256") != v2["cases"][job]["source_semantic_sha256"]
            or check.get("v3_source_semantic_sha256") != v3["cases"][job]["source_semantic_sha256"]
            or not isinstance(check.get("rationale"), str)
            or not check.get("rationale")
        ):
            raise ValueError("Unproven review authority or source version")
        for label, version in (("native_v2", "v2"), ("corrective_v3", "v3")):
            status = check.get(version + "_outcome")
            if status not in ALLOWED_OUTCOMES:
                raise ValueError("Invalid assistant review verdict")
            outcome_counts[label][status] += 1
    blockers = {
        "semantics_not_independently_adjudicated": True,
        "exposed_development_cohort_only": True,
        "source_item_alignment_not_proven_for_model_text": True,
        "material_source_interpretation_failures": (
            outcome_counts["native_v2"]["fail"] > 0 or outcome_counts["corrective_v3"]["fail"] > 0
        ),
        "nested_eligibility_from_model_not_accepted": True,
    }
    return {
        "contract": "jobhunter-b2-native-reconciliation-gate-v1",
        "source_snapshot_sha256": SOURCE_B0_SHA,
        "source_cohort": "four_frozen_exposed_jobs_not_holdout",
        "prompt_change_count": 1,
        "model_identity": v2["model"],
        "model_reasoning": "off",
        "model_output_format_valid_in_both_trials": True,
        "trial_seconds": durations,
        "model_generated_item_counts": item_counts,
        "assistant_checks": {
            label: {
                key: outcome_counts[label][key] for key in ("pass", "partial", "fail", "unresolved")
            }
            for label in semantic_versions
        },
        "review_authority": "assistant_prior_context_exposed",
        "b2_semantic_gate": "OPEN_NO_PROMOTION",
        "blockers": blockers,
        "accepted_employer_facts_from_model": 0,
        "downstream_authority": "none",
        "notes": (
            "Neither JSON validity nor a better assistant-reviewed diagnostic count "
            "establishes semantic accuracy or authorizes product acceptance."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v2", required=True, type=Path)
    parser.add_argument("--v3", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    public_dir = root / "docs/working-memory/2026-11-16_p16_b2"
    if not args.out.resolve().is_relative_to(public_dir):
        raise ValueError("Diagnostic summary must stay in its source-safe review folder")
    if args.out.exists():
        raise FileExistsError("Existing B2 diagnostic summary must not be overwritten")
    for private in (args.v2, args.v3):
        if not private.resolve().is_relative_to(root / "data/local-acceptance"):
            raise ValueError("Raw B2 model evidence must be read from ignored local data")
    result = reconcile(_load(args.v2), _load(args.v3), _load(args.review))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print("B2_RECONCILED", result["b2_semantic_gate"], "checks", result["assistant_checks"])


if __name__ == "__main__":
    main()
