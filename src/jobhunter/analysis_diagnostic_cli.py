"""Explicit local inspection of non-authoritative P1.6 failure diagnostics.

The default view includes metadata only. Response content is displayed only after
an explicit command-line opt-in; this command never exports to the public corpus.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Sequence
from urllib.parse import quote

from jobhunter.config import Settings


def main(argv: Sequence[str] | None = None, *, config_path: Path | None = None) -> int:
    parser = argparse.ArgumentParser(prog="jobhunter diagnostics")
    commands = parser.add_subparsers(dest="action", required=True)
    recent = commands.add_parser("list", help="List recent failed analysis attempts")
    recent.add_argument("--limit", type=int, default=20)
    detail = commands.add_parser("show", help="Inspect one failed analysis attempt")
    detail.add_argument("attempt_id", type=int)
    detail.add_argument(
        "--include-response",
        action="store_true",
        help="Explicitly display sensitive model output in this local terminal",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.action == "list" and not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.action == "show" and args.attempt_id < 1:
        parser.error("attempt_id must be positive")

    database_path = Settings.load(config_path).database_path
    if not database_path.is_file():
        print("No local JobHunter database exists at the configured path.", file=sys.stderr)
        return 2

    # Read-only SQLite URI; this command never initializes schemas or mutates state.
    database_uri = f"file:{quote(str(database_path.resolve()), safe='/')}?mode=ro"
    try:
        with sqlite3.connect(database_uri, uri=True) as connection:
            connection.row_factory = sqlite3.Row
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            if "job_analysis_attempts" not in tables:
                print("No analysis attempt history is available.")
                return 0
            has_diagnostics = "job_analysis_failure_diagnostics" in tables
            if args.action == "list":
                rows = connection.execute(
                    """
                    SELECT id, job_detail_version_id, attempted_at, model, prompt_version,
                           schema_version, outcome, error_type, error_message
                    FROM job_analysis_attempts WHERE outcome = 'failed'
                    ORDER BY id DESC LIMIT ?
                    """,
                    (args.limit,),
                ).fetchall()
                for row in rows:
                    record = dict(row)
                    # Old attempt messages may contain untrusted SDK text. Never display them.
                    record.pop("error_message", None)
                    record.pop("error_type", None)
                    record["diagnostics_available"] = has_diagnostics and connection.execute(
                        "SELECT 1 FROM job_analysis_failure_diagnostics "
                        "WHERE attempt_id = ? LIMIT 1",
                        (row["id"],),
                    ).fetchone() is not None
                    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
                return 0

            attempt = connection.execute(
                """
                SELECT id, job_detail_version_id, attempted_at, model, prompt_version,
                       schema_version, outcome
                FROM job_analysis_attempts WHERE id = ? AND outcome = 'failed'
                """,
                (args.attempt_id,),
            ).fetchone()
            if attempt is None:
                print("No failed analysis attempt has that ID.", file=sys.stderr)
                return 2
            print(json.dumps(dict(attempt), ensure_ascii=False, sort_keys=True))
            if not has_diagnostics:
                print("No diagnostic capture was recorded for this attempt.")
                return 0
            rows = connection.execute(
                "SELECT * FROM job_analysis_failure_diagnostics "
                "WHERE attempt_id = ? ORDER BY id",
                (args.attempt_id,),
            ).fetchall()
            if not rows:
                print("No diagnostic capture was recorded for this attempt.")
            for row in rows:
                record = dict(row)
                if not args.include_response:
                    record.pop("completion_text", None)
                print(json.dumps(record, ensure_ascii=False, sort_keys=True))
            return 0
    except sqlite3.DatabaseError:
        print("Local analysis diagnostic storage is unavailable.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
