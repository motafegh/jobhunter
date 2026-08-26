"""Small CLI for generating and inspecting candidate Job Work Intelligence."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.work_intelligence_service import (
    WorkIntelligenceError,
    build_work_intelligence_service,
    format_work_intelligence,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter-work",
        description=(
            "Generate or inspect P2.2A Job Work Intelligence. Output is candidate analytical "
            "interpretation, not employer wording or promoted taxonomy."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate", help="Generate or reuse Work Intelligence")
    generate.add_argument("job_id")
    show = commands.add_parser("show", help="Show current Work Intelligence when available")
    show.add_argument("job_id")
    return parser


def _load_settings(config_path: Path | None) -> Settings:
    try:
        return Settings.load(config_path)
    except (ConfigLoadError, ValidationError, ValueError) as exc:
        raise ValueError(f"Configuration error: {exc}") from exc


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        settings = _load_settings(args.config)
        service = build_work_intelligence_service(settings)
        if args.command == "generate":
            result = service.analyze_job(args.job_id)
            artifact = service.current_artifact(args.job_id)
            if artifact is None:
                raise RuntimeError("Work Intelligence artifact is unavailable after generation")
            print(
                f"Work Intelligence {result.outcome}: {result.source_job_id} "
                f"artifact={result.artifact_id} themes={result.work_theme_count}"
            )
            print()
            print(format_work_intelligence(artifact))
            return 0

        artifact = service.current_artifact(args.job_id)
        if artifact is None:
            print(
                f"No current Work Intelligence exists for {args.job_id}. "
                "A current accepted English P1.6 dependency is required.",
                file=sys.stderr,
            )
            return 1
        print(format_work_intelligence(artifact))
        return 0
    except (WorkIntelligenceError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
