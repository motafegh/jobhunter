"""Inspect a bounded job-specific capability expectation brief, without model calls.

Optional external candidate insights are validated against exact accepted claim
references, but their *semantic correctness remains unreviewed*. No persistence.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from pathlib import Path
from urllib.parse import quote

from jobhunter.capability_expectations import (
    ProposedInterpretation,
    build_capability_expectation_brief,
    format_expectation_brief,
    validate_interpretation_proposals,
)
from jobhunter.config import Settings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="jobhunter.toml")
    parser.add_argument("--job", required=True, help="Exact local public source job ID")
    parser.add_argument("--phrase", required=True, help="Literal capability phrase")
    parser.add_argument(
        "--proposals-file", type=Path, help="Optional local candidate JSON list"
    )
    args = parser.parse_args()
    if not Path("AGENTS.md").is_file():
        parser.error("Run from the JobHunter root")
    settings = Settings.load(args.config)
    if not settings.database_path.exists():
        parser.error("Configured SQLite database is missing")

    local = Path("data/local-acceptance")
    local.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="capability-expectation-", dir=local) as temp:
        copy = Path(temp) / "read-copy.sqlite3"
        uri = "file:" + quote(str(settings.database_path.resolve()), safe="/") + "?mode=ro"
        source = sqlite3.connect(uri, uri=True)
        try:
            with sqlite3.connect(copy) as snapshot:
                source.backup(snapshot)
        finally:
            source.close()
        brief = build_capability_expectation_brief(
            settings.model_copy(update={"database_path": copy}), args.job, args.phrase
        )
        report = format_expectation_brief(brief)
        if args.proposals_file:
            raw = json.loads(args.proposals_file.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                parser.error("Proposals file must contain a JSON list")
            proposals = []
            for item in raw:
                if not isinstance(item, dict):
                    parser.error("Every proposal must be an object")
                try:
                    proposals.append(ProposedInterpretation(
                        text=item["text"], status=item["status"],
                        confidence=item["confidence"],
                        supporting_refs=tuple(item["supporting_refs"]),
                        rationale=item["rationale"],
                    ))
                except (KeyError, TypeError):
                    parser.error("Candidate proposal has invalid required fields")
            proposals = validate_interpretation_proposals(brief, tuple(proposals))
            report += "\n## Unreviewed candidate interpretations\n"
            for item in proposals:
                report += (
                    f"\n- [{item.status} / {item.confidence}] {item.text}\n"
                    f"  - Rationale: {item.rationale}\n"
                    f"  - Selected factual support: {', '.join(item.supporting_refs)}\n"
                )
            report += (
                "\nMechanically validated provenance does not establish semantic truth. "
                "Review every inference before treating it as advice.\n"
            )
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
