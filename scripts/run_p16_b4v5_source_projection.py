"""Read-only B4v5 source-qualified projection over immutable B4v4c local evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.source_qualified_b4v5 import (
    project_source_qualified_case,
    render_source_qualified_briefs,
)

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c"
DEFAULT_CORRECTION = ROOT / (
    "data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json"
)
DEFAULT_OUT = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, content: Any) -> None:
    path.write_text(
        json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(*, output: Path = DEFAULT_OUT, correction: Path = DEFAULT_CORRECTION) -> dict:
    if not output.resolve().is_relative_to((ROOT / "data/local-acceptance").resolve()):
        raise ValueError("B4v5 raw/source text must stay in ignored local acceptance data")
    if output.exists():
        raise ValueError("B4v5 evidence directory exists; do not overwrite sealed output")
    prior_verification = runpy.run_path(str(ROOT / "scripts/verify_p16_b4_milestone.py"))[
        "verify"
    ]()
    if prior_verification["status"] != "PASS_ENGINEERING_BOUNDARIES_SEMANTIC_GATE_OPEN":
        raise ValueError("Frozen B4v4c baseline failed its evidence verification")
    prior = json.loads((PRIOR / "PRIVATE_B4_CANDIDATES.json").read_text(encoding="utf-8"))
    reviewed = json.loads(correction.read_text(encoding="utf-8"))
    if reviewed.get("contract") != "b4v5-source-exact-reviewed-terminology-overlay-v1":
        raise ValueError("Missing recognized terminology overlay review contract")
    overlays = reviewed.get("corrections")
    if not isinstance(overlays, list) or len(overlays) != 1:
        raise ValueError(
            "This bounded review allows exactly one source-specific terminology correction"
        )
    correction_by_job = {item["source_job_id"]: item for item in overlays}
    if set(correction_by_job) != {"tNDx"}:
        raise ValueError("Unexpected reviewed source job")
    if len(prior["cases"]) != 4:
        raise ValueError("Frozen B4v4c source cohort changed")

    projections = []
    for case in prior["cases"]:
        correction_item = correction_by_job.get(case["source_job_id"])
        projections.append(project_source_qualified_case(case, correction=correction_item))
    if tuple(p["source_job_id"] for p in projections) != ("tNhZ", "tMps", "tNDx", "tMjm"):
        raise ValueError("B4v5 case ordering differs from frozen B0")
    total_items = sum(p["source_item_count"] for p in projections)
    source_bound = sum(len(p["source_qualified_items"]) for p in projections)
    if (total_items, source_bound) != (78, 64):
        raise ValueError("B4v5 source completeness changed from frozen B4v4c")
    tMps = projections[1]
    tNDx = projections[2]
    tMjm = projections[3]
    if (
        len(tMps["eligibility_alternative_candidates"]) != 1
        or tMps["eligibility_alternative_candidates"][0]["root"]["kind"] != "any_of"
        or len(tMps["eligibility_alternative_candidates"][0]["root"]["children"]) != 2
    ):
        raise ValueError("Middle/Senior alternative-path structure not retained")
    if len(tNDx["eligibility_alternative_candidates"]) != 1:
        raise ValueError("Certificate-or-equivalent source path not retained")
    if tNDx["corrected_translation_item_ids"] != ["s_ae62e5aa14da3bfe232413c7ca6d01907c2878b1"]:
        raise ValueError("Reviewed Fadak translation was not linked to exact source")
    if (
        tMjm["groups"].get("work_duty")
        or tMjm["v4_model_candidates"] is not None
        or tMjm["b4_analysis_outcome"] != "source_only_candidate"
    ):
        raise ValueError("Qualification-only case must not invent work duties")

    output.mkdir(parents=True)
    write_json(
        output / "PRIVATE_SOURCE_PROJECTIONS.json",
        {
            "contract": "jobhunter-p16-b4-source-qualified-projection-v5",
            "authority": "candidate_only_no_downstream_reuse",
            "frozen_b4v4c_private_sha256": file_sha(PRIOR / "PRIVATE_B4_CANDIDATES.json"),
            "reviewed_terminology_correction_sha256": file_sha(correction),
            "cases": projections,
        },
    )
    (output / "SOURCE_QUALIFIED_BRIEFS.md").write_text(
        render_source_qualified_briefs(projections), encoding="utf-8"
    )
    counts = {
        "contract": "jobhunter-p16-b4v5-safe-source-projection-v1",
        "status": "PASS_SOURCE_PRESENTATION_EXPOSED_COHORT_SEMANTIC_GATE_SEPARATE",
        "authority": "candidate_only_no_downstream_reuse",
        "case_count": 4,
        "source_item_count": 78,
        "source_qualified_item_count": source_bound,
        "excluded_item_count": total_items - source_bound,
        "source_qualification_candidate_count": sum(
            len(p["groups"].get("candidate_qualification", [])) for p in projections
        ),
        "source_behavioral_expectation_candidate_count": sum(
            len(p["groups"].get("behavioral_expectation", [])) for p in projections
        ),
        "application_condition_candidate_count": sum(
            len(p["groups"].get("application_instruction", [])) for p in projections
        ),
        "distinct_eligibility_graph_count": sum(
            len(p["eligibility_alternative_candidates"]) for p in projections
        ),
        "eligibility_graph_root_operators": dict(
            sorted(
                Counter(
                    g["root"]["kind"]
                    for p in projections
                    for g in p["eligibility_alternative_candidates"]
                ).items()
            )
        ),
        "corrected_reviewed_terminology_items": sum(
            len(p["corrected_translation_item_ids"]) for p in projections
        ),
        "suppressed_v4_model_claims_due_to_translation_repair": sum(
            len(p["v4_model_claims_suppressed_due_to_translation_review"]) for p in projections
        ),
        "llm_requests": 0,
        "raw_original_unchanged": True,
        "b3_selected_translation_artifacts_unchanged": True,
        "prior_b4v4c_evidence_unchanged": True,
        "assistant_exposed_source_review": True,
        "independent_blind_human_review": False,
        "semantically_accepted_employer_facts": 0,
        "unseen_generalization_established": False,
        "production_database_written": False,
        "downstream_authority": "none",
        "owner_time_savings_measured": False,
        "per_case": {
            p["source_job_id"]: {
                "total_source_items": p["source_item_count"],
                "displayed_source_qualified_items": len(p["source_qualified_items"]),
                "alternate_eligibility_graphs": len(p["eligibility_alternative_candidates"]),
                "visible_model_source": p["b4_analysis_outcome"],
            }
            for p in projections
        },
    }
    safe_text = json.dumps(counts, ensure_ascii=False)
    if any("\u0600" <= ch <= "\u06ff" for ch in safe_text):
        raise ValueError("B4v5 safe metrics contain original-language vacancy text")
    write_json(output / "SAFE_COUNTS.json", counts)
    audit = {
        "contract": "jobhunter-p16-b4v5-source-projection-audit-v1",
        "status": "PASS_SOURCE_ONLY_EXPOSED_EVIDENCE_WITH_UNPROMOTED_SEMANTIC_CANDIDATES",
        "created_at": datetime.now(UTC).isoformat(),
        "prior_b4v4c_private_sha256": file_sha(PRIOR / "PRIVATE_B4_CANDIDATES.json"),
        "prior_b4v4c_final_audit_sha256": file_sha(PRIOR / "B4_FINAL_AUDIT.json"),
        "reviewed_correction_sha256": file_sha(correction),
        "source_projector_module_sha256": file_sha(ROOT / "src/jobhunter/source_qualified_b4v5.py"),
        "runner_sha256": file_sha(Path(__file__)),
        "private_projection_sha256": file_sha(output / "PRIVATE_SOURCE_PROJECTIONS.json"),
        "markdown_sha256": file_sha(output / "SOURCE_QUALIFIED_BRIEFS.md"),
        "safe_counts_sha256": file_sha(output / "SAFE_COUNTS.json"),
        "b4v4c_preserved": True,
        "raw_source_preserved": True,
        "model_request_count": 0,
        "production_promotion": 0,
    }
    write_json(output / "FINAL_AUDIT.json", audit)
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--correction", type=Path, default=DEFAULT_CORRECTION)
    args = parser.parse_args()
    print(json.dumps(run(output=args.out, correction=args.correction), indent=2))


if __name__ == "__main__":
    main()
