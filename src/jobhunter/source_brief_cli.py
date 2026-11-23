"""Local, read-only, original-source job brief when model analysis is unavailable.

Not a v30/v9 replacement. Uses only source-fingerprinted B2v7 candidate
classification and retains original evidence for inspectable drilldown.
No model calls, external requests, inferred employer facts or promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

from jobhunter.config import Settings
from jobhunter.source_item_candidate_b2_v7_dom import (
    B2V7_DOM_CONTRACT,
    interpret_original_source_candidate_v7,
)
from jobhunter.translation_store import TranslationSourceVersion

_MAX_PREVIEW_EACH = 3
_GROUPS = (
    ("work_duty", "Original source: candidate work duties"),
    ("qualification_required", "Original source: explicitly required candidate capabilities"),
    ("qualification_preferred", "Original source: explicitly preferred capabilities"),
    ("qualification_other", "Original source: other / uncertain capabilities"),
    ("behavioral_expectation", "Original source: behavioral expectations"),
    ("work_arrangement", "Original source: working conditions"),
    ("application_instruction", "Original source: application instructions"),
    ("compensation", "Original source: compensation"),
    ("benefit", "Original source: employer benefits"),
    ("context", "Other original context"),
    ("unresolved", "Original source requiring review"),
)


def source_brief(
    database_path: Path,
    source_job_id: str,
    *,
    all_evidence: bool = False,
    preview_per_group: int = _MAX_PREVIEW_EACH,
) -> dict:
    """Create a candidate-only source inventory with an explicit uncertainty boundary."""
    if not 1 <= preview_per_group <= 12:
        raise ValueError("preview_per_group must be between 1 and 12")
    if not source_job_id or len(source_job_id) > 128:
        raise ValueError("Invalid source job ID")
    # Use SQLite read-only from the FIRST operation: TranslationStore's usual
    # initialization opens writable connections and may change journal mode.
    with sqlite3.connect(f"file:{database_path.resolve()}?mode=ro", uri=True) as db:
        rec = db.execute(
            "SELECT p.source_job_id, v.id, v.semantic_sha256, v.fields_json, "
            "v.evidence_path, v.content_sha256 "
            "FROM job_postings AS p JOIN job_detail_versions AS v "
            "ON v.job_posting_id = p.id "
            "WHERE p.source = 'jobinja' AND p.source_job_id = ? "
            "AND v.id = (SELECT MAX(id) FROM job_detail_versions "
            "WHERE job_posting_id = p.id) AND v.parse_status = 'parsed' "
            "LIMIT 1",
            (source_job_id,),
        ).fetchone()
    if rec is None:
        raise ValueError("No currently parsed source exists for this job ID")
    fields = json.loads(rec[3])
    source = TranslationSourceVersion(
        source_job_id=str(rec[0]),
        job_detail_version_id=int(rec[1]),
        semantic_sha256=str(rec[2]),
        source_language=str(fields.get("language") or "unknown"),
        fields=fields,
    )
    expected_sha256 = str(rec[5])
    raw = Path(rec[4]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("Original source HTML integrity mismatch")
    candidate = interpret_original_source_candidate_v7(
        source, raw_job_page=raw, expected_html_sha256=expected_sha256
    )
    grouped = defaultdict(list)
    for item in candidate.items:
        group = item.category
        if group == "candidate_qualification":
            group = (
                "qualification_required"
                if item.employer_strength == "required"
                else "qualification_preferred"
                if item.employer_strength == "preferred"
                else "qualification_other"
            )
        grouped[group].append(
            {
                "source_anchor_id": item.anchor.anchor_id,
                "original_text": item.anchor.exact_text,
                "original_text_sha256": hashlib.sha256(
                    item.anchor.exact_text.encode("utf-8")
                ).hexdigest(),
                "role_candidate": item.category,
                "obligation_candidate": item.employer_strength,
                "evidence_basis": item.evidence_basis,
            }
        )
    groups = []
    for category, heading in _GROUPS:
        evidence = grouped[category]
        visible = evidence if all_evidence else evidence[:preview_per_group]
        groups.append(
            {
                "category": category,
                "label": heading,
                "candidate_count": len(evidence),
                "visible": visible,
                "requires_drilldown": len(evidence) - len(visible),
            }
        )
    if len(groups) != len(_GROUPS):
        raise AssertionError("Unknown source inventory grouping")
    return {
        "contract": "jobhunter-source-brief-opt-in-candidate-v1",
        "source_role_contract": B2V7_DOM_CONTRACT,
        "source_job_id": source.source_job_id,
        "original_source_semantic_sha256": source.semantic_sha256,
        "original_source_html_sha256": expected_sha256,
        "source_version_id": source.job_detail_version_id,
        # Show board/source metadata verbatim rather than silently resolving
        # contradictions with the original narrative description.
        "source_metadata_verbatim": {
            key: value
            for key, value in source.fields.items()
            if key
            in {
                "title",
                "company",
                "minimum_experience",
                "employment_type",
                "job_type",
                "location",
                "seniority",
                "education",
                "workplace_type",
                "salary",
            }
            and isinstance(value, str)
            and len(value) <= 300
        },
        "groups": groups,
        "extracted_source_item_count": len(candidate.items),
        "candidate_eligibility_alternatives_unreviewed": len(candidate.alternatives),
        "no_explicit_work_items_is_not_no_real_duties": True,
        "no_inference_requests": True,
        "source_authority": "exact_source_evidence_only",
        "candidate_only_not_accepted_employer_facts": True,
        "B5_independent_acceptance": False,
        "B6_production_promotion": False,
    }


def format_source_brief(result: dict) -> str:
    lines = [
        "JobHunter — ORIGINAL-SOURCE job brief (candidate-only, NOT accepted analysis)",
        f"Source job: {result['source_job_id']}",
        f"Original evidence SHA-256: {result['original_source_semantic_sha256']}",
        "All labels and strengths are provisional; verify each employer statement.",
        "This view works independently of failed English v30 or original v9.",
        "Structured job-board fields can contradict the narrative; neither wins automatically.",
    ]
    for field, value in result["source_metadata_verbatim"].items():
        lines.append(f"Original board field {field}: {value}")
    for section in result["groups"]:
        if not section["candidate_count"]:
            continue
        lines.append("")
        lines.append(f"{section['label']} ({section['candidate_count']} original-source items)")
        for item in section["visible"]:
            lines.append(
                f"- candidate strength={item['obligation_candidate']}, "
                f"source={item['source_anchor_id']}"
            )
            lines.append("  " + item["original_text"].replace("\n", "\n  "))
        if section["requires_drilldown"]:
            lines.append(
                f"  {section['requires_drilldown']} more source items omitted from "
                "first view; re-run with --all for complete evidence."
            )
    if not any(
        group["candidate_count"] for group in result["groups"] if group["category"] == "work_duty"
    ):
        lines.append(
            "No separate explicit duty items classified. This does NOT "
            "establish that the job has no real responsibilities."
        )
    lines.append(
        "\nUnreviewed options/alternatives: "
        + str(result["candidate_eligibility_alternatives_unreviewed"])
        + " candidate structures, not employer-certified eligibility."
    )
    lines.append("No model, translation, accepted-fact, or production write occurred.")
    return "\n".join(lines)


def main(argv: list[str] | None = None, *, config_path: Path | None = None) -> int:
    parser = argparse.ArgumentParser(prog="jobhunter jobs source-brief")
    parser.add_argument("job_id")
    parser.add_argument("--all", action="store_true", help="Show all exact-source items")
    parser.add_argument("--max-per-section", type=int, default=_MAX_PREVIEW_EACH)
    parser.add_argument("--json", action="store_true", help="Print candidate-only JSON")
    args = parser.parse_args(argv)
    settings = Settings.load(config_path)
    result = source_brief(
        settings.database_path,
        args.job_id,
        all_evidence=args.all,
        preview_per_group=args.max_per_section,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(format_source_brief(result))
    return 0
