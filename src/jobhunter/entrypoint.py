"""Console entrypoint that adds the final Phase-1 run without destabilizing legacy CLI."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter.cli import build_parser as build_legacy_parser
from jobhunter.cli import main as legacy_main
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.phase1_run import (
    build_phase1_run_service,
    configured_searches,
    format_phase1_run_summary,
)


def _bounded_int(name: str, *, minimum: int, maximum: int):
    def parse(value: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"{name} must be an integer") from exc
        if not minimum <= parsed <= maximum:
            raise argparse.ArgumentTypeError(
                f"{name} must be between {minimum} and {maximum}"
            )
        return parsed

    return parse


def _positive_hours(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("refresh age must be a number") from exc
    if not 0 < parsed <= 8760:
        raise argparse.ArgumentTypeError(
            "refresh age must be greater than 0 and at most 8760"
        )
    return parsed


def _run_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter run",
        description=(
            "Run the bounded Phase-1 pipeline: discovery, detail refresh, parser audit, "
            "English v2, semantic analysis, and current Market summary."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    parser.add_argument(
        "--search-limit",
        type=_bounded_int("search limit", minimum=1, maximum=500),
        default=None,
        help="Maximum configured searches selected for this run",
    )
    parser.add_argument(
        "--request-budget",
        type=_bounded_int("request budget", minimum=1, maximum=500),
        default=None,
        help="Maximum Jobinja search-page requests",
    )
    parser.add_argument(
        "--missing-limit",
        type=_bounded_int("missing detail limit", minimum=0, maximum=50),
        default=None,
        help="Maximum newly discovered jobs whose details may be acquired",
    )
    parser.add_argument(
        "--refresh-limit",
        type=_bounded_int("refresh detail limit", minimum=0, maximum=50),
        default=None,
        help="Maximum refresh-due jobs whose details may be checked",
    )
    parser.add_argument(
        "--refresh-after-hours",
        type=_positive_hours,
        default=None,
        help="Age threshold used for refresh-due selection",
    )
    parser.add_argument(
        "--translation-limit",
        type=_bounded_int("translation limit", minimum=1, maximum=50),
        default=None,
        help="Maximum current source versions translated/repaired in this run",
    )
    parser.add_argument(
        "--analysis-limit",
        type=_bounded_int("analysis limit", minimum=1, maximum=20),
        default=None,
        help="Maximum current English-ready jobs analyzed in this run",
    )
    return parser


def _extract_run_invocation(
    arguments: list[str],
) -> tuple[bool, Path | None, list[str]]:
    if arguments and arguments[0] == "run":
        return True, None, arguments[1:]
    if len(arguments) >= 3 and arguments[0] == "--config" and arguments[2] == "run":
        return True, Path(arguments[1]), arguments[3:]
    if (
        len(arguments) >= 2
        and arguments[0].startswith("--config=")
        and arguments[1] == "run"
    ):
        return True, Path(arguments[0].split("=", 1)[1]), arguments[2:]
    return False, None, arguments


def _load_settings(config_path: Path | None) -> Settings:
    try:
        return Settings.load(config_path)
    except (ConfigLoadError, ValidationError, ValueError) as exc:
        raise ValueError(f"Configuration error: {exc}") from exc


def _run_phase1(arguments: list[str], *, default_config: Path | None) -> int:
    parser = _run_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    search_limit = parsed.search_limit or settings.jobinja_max_expanded_searches
    request_budget = parsed.request_budget or settings.jobinja_search_request_budget
    missing_limit = (
        settings.jobinja_sync_missing_limit
        if parsed.missing_limit is None
        else parsed.missing_limit
    )
    refresh_limit = (
        settings.jobinja_sync_refresh_limit
        if parsed.refresh_limit is None
        else parsed.refresh_limit
    )
    refresh_after_hours = (
        settings.jobinja_refresh_after_hours
        if parsed.refresh_after_hours is None
        else parsed.refresh_after_hours
    )
    translation_limit = parsed.translation_limit or settings.translation_batch_limit
    analysis_limit = parsed.analysis_limit or settings.analysis_batch_limit

    if missing_limit + refresh_limit > 50:
        print(
            "Combined --missing-limit and --refresh-limit may not exceed 50.",
            file=sys.stderr,
        )
        return 2

    try:
        searches = configured_searches(settings, limit=search_limit)
        if not searches:
            print(
                "No enabled Jobinja searches are configured for the complete run.",
                file=sys.stderr,
            )
            return 2
        service = build_phase1_run_service(
            settings,
            request_budget=request_budget,
        )
        summary = service.run(
            searches,
            missing_limit=missing_limit,
            refresh_limit=refresh_limit,
            refresh_after_hours=refresh_after_hours,
            translation_limit=translation_limit,
            analysis_limit=analysis_limit,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Phase-1 run failed before a complete summary was available: {exc}", file=sys.stderr)
        return 1

    print(format_phase1_run_summary(summary))
    return 1 if summary.has_failures else 0


def _print_combined_help() -> None:
    build_legacy_parser().print_help()
    print("")
    print("Additional complete workflow command:")
    print("  run                  Run bounded source -> English -> analysis -> Market pipeline")
    print("  run --help           Show Phase-1 run limits and options")


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch the new complete run while preserving every existing CLI command."""

    arguments = list(argv if argv is not None else sys.argv[1:])
    if arguments in (["-h"], ["--help"]):
        _print_combined_help()
        return 0

    is_run, default_config, run_arguments = _extract_run_invocation(arguments)
    if is_run:
        return _run_phase1(run_arguments, default_config=default_config)
    return legacy_main(arguments)
