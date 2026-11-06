"""Capture public-safe, read-only evidence for owner review of /compare.

This intentionally exports only fixed public job IDs and aggregate counts, never
source text, titles, company names, model prompts, database paths, or local logs.
It does not run acquisition, translation, or model inference.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode

from jobhunter.config import Settings
from jobhunter.job_comparison import build_job_comparison

OUTPUT_DIR = Path("docs/working-memory/2026-11-06_p23a_compare_owner_usefulness")
LOCAL_TMP_DIR = Path("data/local-acceptance")
CASES = (
    (
        "rag_three_jobs",
        ("tvMm", "tNVe", "t7Ay"),
        "RAG",
        "Find exact RAG qualifications, direct RAG work, and evidence. "
        "Which job has no directly stated RAG responsibility?",
    ),
    (
        "python_two_anchors",
        ("tG9K", "tmBK"),
        "Python",
        "Compare Python wording and optional job-local capability groups. "
        "Can you tell exact facts from interpretation?",
    ),
    (
        "requirement_only",
        ("t7ck", "t7Ay"),
        "",
        "Confirm that requirement-only postings do not acquire invented duties.",
    ),
    (
        "no_match",
        ("tvMm", "tNVe"),
        "zzzz-jh-no-match-2026",
        "Check that a literal no-match is not presented as proof of no demand.",
    ),
)


def _head_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
    ).strip()


def _snapshot(source_path: Path, target_path: Path) -> tuple[bool, int]:
    uri = "file:" + quote(str(source_path.resolve()), safe="/") + "?mode=ro"
    source = sqlite3.connect(uri, uri=True)
    try:
        target = sqlite3.connect(target_path)
        try:
            source.backup(target)
            integrity_ok = target.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            foreign_key_violations = len(target.execute("PRAGMA foreign_key_check").fetchall())
            return integrity_ok, foreign_key_violations
        finally:
            target.close()
    finally:
        source.close()


def _job_summary(job) -> dict[str, object]:
    """Only counts and known public identifiers; no employer/source text."""
    requirements = job.requirements
    return {
        "public_job_id": job.option.source_job_id,
        "accepted_distinct_claims": len(job.claims),
        "matching_distinct_claims": len(job.matching_claims),
        "matching_requirements": len(requirements),
        "matching_direct_responsibilities": len(job.responsibilities),
        "total_direct_responsibilities": job.total_responsibilities,
        "matching_requirements_with_obligation": sum(bool(c.strength) for c in requirements),
        "matching_requirements_with_explicit_depth": sum(
            bool(c.depth_signal) for c in requirements
        ),
        "matching_claims_with_reviewed_concept": sum(
            bool(c.mapping and c.mapping.canonical_concept_id) for c in job.matching_claims
        ),
        "current_capability_overlay_available": job.capability_artifact_id is not None,
        "visible_job_local_groups": len(job.groups),
        "repeated_support_slots_in_visible_groups": sum(
            group.shared_claim_count for group in job.groups
        ),
    }


def _review_template() -> str:
    lines = [
        "# P2.3A comparison — owner repeated-use evaluation",
        "",
        "**State:** OBSERVATIONS PENDING. Not product acceptance.",
        "",
        "Use the local browser app with the same populated configuration used for capture.",
        "For each scenario, answer its question by reading the compare view and opening",
        "the cited source when necessary. No new model runs or source refresh are required.",
        "",
        "Do not paste local paths, credentials, private notes, raw SQLite, full",
        "job advertisements, screenshots containing private state, or model protocol logs.",
        "The separate AUTO_METRICS.json contains only fixed public IDs and aggregate counts.",
        "",
        "## Scenarios and observations",
        "",
        "| Scenario | What to verify | Your outcome (pass / friction / blocked) |",
        "| --- | --- | --- |",
    ]
    for key, ids, query, question in CASES:
        params = [("job", job_id) for job_id in ids] + [("q", query)]
        url = "http://127.0.0.1:8765/compare?" + urlencode(params)
        lines.append(f"| [`{key}`]({url}) | {question} | TODO |")
    lines += [
        "",
        "## Repeated-use assessment (fill in after browser review)",
        "",
        "1. **What concrete comparison question did you answer?** TODO",
        "2. **What was faster or clearer than reading separate job pages?** TODO",
        "3. **What caused repeated reading, extra clicks, or confusion?** TODO",
        "4. **Were factual claims, job-local interpretation, and unknown scope distinct?** TODO",
        "5. **Could you open exact supporting evidence without losing context?** TODO",
        "6. **Was an important capability missing, ambiguous, or falsely implied?** TODO",
        "7. **If you actually timed the workflow, record the method and duration;**",
        "   otherwise write 'not measured': TODO",
        "",
        "## Owner recommendation (select only after use)",
        "",
        "- [ ] Accept the bounded comparison for repeated use (not full P2.3).",
        "- [ ] Improve specific comparison usability defects first.",
        "- [ ] Investigate a specific missing semantic capability before next build.",
        "- [ ] Evidence is insufficient; repeat with a documented additional case.",
        "",
        "**Most important next change and the observed reason:** TODO",
        "",
        "Do not reinterpret a lexical match as canonical equivalence, a missing",
        "responsibility as proof it is unnecessary, or overlapping group memberships",
        "as independent counts of demand.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", default="jobhunter.toml", help="Existing populated local TOML"
    )
    args = parser.parse_args()

    if not Path("AGENTS.md").is_file() or not Path("src/jobhunter/job_comparison.py").is_file():
        parser.error("Run from the JobHunter repository root")
    settings = Settings.load(args.config)
    source_path = settings.database_path
    if not source_path.is_file():
        parser.error("Configured SQLite database does not exist; check --config")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_TMP_DIR.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "contract": "p23a-owner-usefulness-aggregate-evidence-v1",
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "git_head": _head_sha(),
        "evidence_type": "automated_mechanical_counts_only_not_owner_acceptance",
        "database_published": False,
        "cases": [],
    }

    with tempfile.TemporaryDirectory(prefix="p23a-compare-", dir=LOCAL_TMP_DIR) as temp:
        snapshot_path = Path(temp) / "snapshot.sqlite3"
        integrity_ok, fk_violations = _snapshot(source_path, snapshot_path)
        payload["snapshot_integrity_ok"] = integrity_ok
        payload["snapshot_foreign_key_violations"] = fk_violations
        if not integrity_ok or fk_violations:
            parser.error("Snapshot integrity check failed; no report written")
        isolated = settings.model_copy(update={"database_path": snapshot_path})
        for key, job_ids, query, _question in CASES:
            case: dict[str, object] = {
                "scenario": key,
                "public_job_ids": list(job_ids),
                "literal_filter": query,
            }
            try:
                comparison = build_job_comparison(isolated, job_ids, query)
                case["state"] = "evaluated"
                case["jobs"] = [_job_summary(job) for job in comparison.jobs]
            except Exception as exc:
                # Never serialize an exception message: it can include local state.
                case["state"] = "not_evaluable"
                case["error_class_only"] = type(exc).__name__
            payload["cases"].append(case)

    metrics_path = OUTPUT_DIR / "AUTO_METRICS.json"
    review_path = OUTPUT_DIR / "OWNER_REVIEW.md"
    metrics_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not review_path.exists():
        review_path.write_text(_review_template(), encoding="utf-8")
    print("Saved repository-reviewable aggregate metrics:", metrics_path)
    print("Owner notes (existing edits preserved):", review_path)
    for case in payload["cases"]:
        print(case["scenario"], case["state"])
    print("SQLite snapshot was temporary and was not included in the report.")
    print("Owner usefulness and time savings have not been established by this capture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
