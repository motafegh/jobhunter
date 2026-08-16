"""CLI for exporting and verifying the repository-safe public JobHunter corpus."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.public_corpus import (
    DEFAULT_PUBLIC_CORPUS_DIR,
    PublicCorpusError,
    export_public_corpus,
    verify_public_corpus,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter-corpus",
        description=(
            "Project durable public JobHunter SQLite state into deterministic UTF-8 JSON "
            "that can be versioned in Git."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser(
        "export",
        help="Backfill or refresh the complete public corpus from SQLite",
    )
    export_parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PUBLIC_CORPUS_DIR,
        help="Repository corpus directory (default: ./corpus)",
    )
    export_parser.add_argument(
        "--no-prune",
        action="store_true",
        help="Do not remove job directories that no longer exist in SQLite",
    )

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify repository corpus JSON exactly matches current SQLite public state",
    )
    verify_parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PUBLIC_CORPUS_DIR,
        help="Repository corpus directory (default: ./corpus)",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Read the repository manifest without querying SQLite",
    )
    status_parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PUBLIC_CORPUS_DIR,
        help="Repository corpus directory (default: ./corpus)",
    )
    return parser


def _settings(path: Path | None) -> Settings:
    return Settings.load(path)


def _analysis_model(settings: Settings) -> str | None:
    return settings.analysis_lm_studio_model or settings.lm_studio_model


def _capability_model(settings: Settings) -> str | None:
    return settings.capability_lm_studio_model or settings.lm_studio_model


def _fetched_detail_count(manifest: dict[str, object]) -> int:
    jobs = manifest.get("jobs", [])
    if not isinstance(jobs, list):
        return 0
    return sum(
        1
        for item in jobs
        if isinstance(item, dict) and item.get("job_detail_version_id") is not None
    )


def _load_manifest(output_dir: Path) -> dict[str, object]:
    manifest_path = output_dir / "manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _print_export(summary) -> None:
    manifest = _load_manifest(summary.output_dir)
    print(f"Public corpus: {summary.output_dir.as_posix()}")
    print(f"Known/discovered jobs: {summary.jobs}")
    print(f"Fetched/parsed job details: {_fetched_detail_count(manifest)}")
    print(f"English projections: {summary.english_projections}")
    print(f"English P1.6: {summary.english_analyses}")
    print(f"Original P1.6: {summary.original_analyses}")
    print(f"Capabilities: {summary.capabilities}")


def _status(output_dir: Path) -> int:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Public corpus manifest is missing: {manifest_path}", file=sys.stderr)
        return 1
    try:
        manifest = _load_manifest(output_dir)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Public corpus manifest is unreadable: {exc}", file=sys.stderr)
        return 1
    counts = manifest.get("counts", {})
    if not isinstance(counts, dict):
        counts = {}
    print(f"Schema: {manifest.get('schema_version', 'unknown')}")
    print(f"Known/discovered jobs: {counts.get('jobs', 0)}")
    print(f"Fetched/parsed job details: {_fetched_detail_count(manifest)}")
    print(f"English projections: {counts.get('english_projections', 0)}")
    print(f"English P1.6: {counts.get('p16_english', 0)}")
    print(f"Original P1.6: {counts.get('p16_original', 0)}")
    print(f"Capabilities: {counts.get('capabilities', 0)}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parsed = _parser().parse_args(list(argv) if argv is not None else None)
    if parsed.command == "status":
        return _status(parsed.output_dir)

    try:
        settings = _settings(parsed.config)
        if parsed.command == "export":
            summary = export_public_corpus(
                settings.database_path,
                output_dir=parsed.output_dir,
                analysis_model=_analysis_model(settings),
                capability_model=_capability_model(settings),
                prune=not parsed.no_prune,
            )
            _print_export(summary)
            return 0

        verification = verify_public_corpus(
            settings.database_path,
            output_dir=parsed.output_dir,
            analysis_model=_analysis_model(settings),
            capability_model=_capability_model(settings),
        )
    except (ConfigLoadError, ValidationError, PublicCorpusError, OSError, ValueError) as exc:
        print(f"Public corpus command failed: {exc}", file=sys.stderr)
        return 1

    if verification.ok:
        print(f"Public corpus verification PASS ({verification.jobs} known jobs)")
        return 0
    print(f"Public corpus verification FAIL ({len(verification.errors)} issue(s))", file=sys.stderr)
    for error in verification.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
