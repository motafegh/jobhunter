"""Capture bounded read-only P2.3B candidate expectation briefs for real cases.

Full exact employer wording is local-only under ignored data/local-acceptance/.
The optional repository-safe summary contains only public IDs and counts.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

from jobhunter.capability_expectations import (
    build_capability_expectation_brief,
    format_expectation_brief,
)
from jobhunter.config import Settings

SCENARIOS = (
    ("tvMm", "RAG"),
    ("tNVe", "RAG"),
    ("t7Ay", "RAG"),
    ("tG9K", "Python"),
)
LOCAL_OUTPUT = Path("data/local-acceptance/p23b-capability-expectations")
PUBLIC_OUTPUT = Path(
    "docs/working-memory/2026-11-11_p23b_capability_expectation/"
    "REAL_CASE_MECHANICAL_AUDIT.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="jobhunter.toml")
    args = parser.parse_args()

    if not Path("AGENTS.md").is_file():
        parser.error("Run from JobHunter repository root")
    settings = Settings.load(args.config)
    if not settings.database_path.is_file():
        parser.error("Configured SQLite database not available")

    LOCAL_OUTPUT.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "contract": "p23b-capability-expectation-mechanical-audit-v0",
        "state": "candidate-only; not a semantic or owner acceptance",
        "source_baseline_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "model_calls": 0,
        "acquisition_calls": 0,
        "live_database_mutated": False,
        "cases": [],
    }
    with tempfile.TemporaryDirectory(prefix="p23b-read-", dir=LOCAL_OUTPUT) as temp:
        copy = Path(temp) / "read-copy.sqlite3"
        uri = "file:" + quote(str(settings.database_path.resolve()), safe="/") + "?mode=ro"
        source = sqlite3.connect(uri, uri=True)
        try:
            with sqlite3.connect(copy) as destination:
                source.backup(destination)
        finally:
            source.close()
        with sqlite3.connect(copy) as audit:
            assert audit.execute("pragma integrity_check").fetchone()[0] == "ok"
            assert not audit.execute("pragma foreign_key_check").fetchall()

        isolated = settings.model_copy(update={"database_path": copy})
        for job_id, phrase in SCENARIOS:
            brief = build_capability_expectation_brief(isolated, job_id, phrase)
            # Raw source-derived wording is intentionally not repository published.
            local_report = LOCAL_OUTPUT / f"{job_id}-{phrase.lower()}-candidate.md"
            local_report.write_text(format_expectation_brief(brief), encoding="utf-8")
            result["cases"].append({
                "source_job_id": job_id,
                "capability_phrase": phrase,
                "accepted_claims": brief.accepted_claim_count,
                "exact_phrase_matches": brief.matched_claim_count,
                "qualifications": len(brief.source_requirements),
                "direct_duties": len(brief.source_responsibilities),
                "qualification_alternative_flags": sum(
                    fact.potential_alternatives for fact in brief.source_requirements
                ),
                "explicit_depth_qualifications": sum(
                    bool(fact.explicit_depth) for fact in brief.source_requirements
                ),
                "current_capability_v9_available": (
                    brief.current_capability_artifact_id is not None
                ),
                "verification_questions": len(brief.questions),
            })
            print(job_id, phrase, "brief saved locally", local_report)

    PUBLIC_OUTPUT.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("Repository-safe aggregate:", PUBLIC_OUTPUT)
    print("No private SQLite or raw employer wording was exported into the repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
