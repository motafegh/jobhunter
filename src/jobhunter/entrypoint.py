"""Console entrypoint for complete Phase-1, source-health, and review commands."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_ANALYSIS_SCHEMA_VERSION,
    ORIGINAL_PROMPT_VERSION,
    AnalysisValidationError,
    build_job_analysis_service,
)
from jobhunter.capability_service import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    build_capability_intelligence_service,
    format_capability_intelligence,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.cli import build_parser as build_legacy_parser
from jobhunter.cli import main as legacy_main
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.inference import InferenceProviderError
from jobhunter.phase1_run import (
    build_phase1_run_service,
    configured_searches,
    format_phase1_run_summary,
)
from jobhunter.review_snapshot import ReviewSnapshotError, write_review_snapshot
from jobhunter.role_blueprint_service import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
    RoleBlueprintError,
    build_role_blueprint_service,
    format_role_blueprint,
)
from jobhunter.role_blueprint_store import RoleBlueprintStore
from jobhunter.source_health import SourceHealthReader, format_source_health


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


def _health_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter jobs health",
        description=(
            "Summarize one Jobinja posting's source/lifecycle health without "
            "re-reading the full check timeline."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID")
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    return parser


def _analysis_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter jobs analyze",
        description=(
            "Build or reuse P1.6 semantic analysis for one explicit current job without "
            "running discovery, refresh, translation, or batch orchestration."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID")
    parser.add_argument(
        "--mode",
        choices=("english", "original"),
        default="english",
        help="Evidence representation to analyze (default: english)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    return parser


def _capability_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter jobs capability",
        description=(
            "Build or reuse richer job capability/depth intelligence above the current "
            "accepted English semantic extraction."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID")
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    return parser


def _blueprint_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter jobs blueprint",
        description=(
            "Build or reuse the human-facing Role Capability Blueprint above current "
            "Capability Intelligence."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID")
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    return parser


def _snapshot_parser(*, default_config: Path | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter jobs snapshot",
        description=(
            "Export the current public job/intelligence chain as repository-reviewable JSON."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID")
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("review-snapshots/jobs"),
        help="Snapshot directory (default: review-snapshots/jobs)",
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


def _extract_jobs_invocation(
    arguments: list[str],
    command: str,
) -> tuple[bool, Path | None, list[str]]:
    target = ["jobs", command]
    if len(arguments) >= 2 and arguments[:2] == target:
        return True, None, arguments[2:]
    if (
        len(arguments) >= 4
        and arguments[0] == "--config"
        and arguments[2:4] == target
    ):
        return True, Path(arguments[1]), arguments[4:]
    if (
        len(arguments) >= 3
        and arguments[0].startswith("--config=")
        and arguments[1:3] == target
    ):
        return True, Path(arguments[0].split("=", 1)[1]), arguments[3:]
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
        print(
            f"Phase-1 run failed before a complete summary was available: {exc}",
            file=sys.stderr,
        )
        return 1

    print(format_phase1_run_summary(summary))
    return 1 if summary.has_failures else 0


def _show_source_health(arguments: list[str], *, default_config: Path | None) -> int:
    parser = _health_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
        summary = SourceHealthReader(settings.database_path).get(parsed.job_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except LookupError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(format_source_health(summary))
    return 0


def _run_job_analysis(
    arguments: list[str],
    *,
    default_config: Path | None,
) -> int:
    parser = _analysis_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
        service = build_job_analysis_service(settings)
        result = (
            service.analyze_english_job(parsed.job_id)
            if parsed.mode == "english"
            else service.analyze_original_job(parsed.job_id)
        )
    except (AnalysisValidationError, ValueError) as exc:
        print(f"P1.6 analysis is not ready: {exc}", file=sys.stderr)
        return 2
    except (InferenceProviderError, OSError, RuntimeError) as exc:
        print(f"P1.6 analysis failed: {exc}", file=sys.stderr)
        return 1

    if parsed.mode == "english":
        prompt_version = ENGLISH_PROMPT_VERSION
        schema_version = ENGLISH_ANALYSIS_SCHEMA_VERSION
        label = "English"
    else:
        prompt_version = ORIGINAL_PROMPT_VERSION
        schema_version = ORIGINAL_ANALYSIS_SCHEMA_VERSION
        label = "Original-language"
    print(f"Outcome: {result.outcome}")
    print(f"{label} P1.6 for {result.source_job_id}")
    print(f"Artifact: {result.artifact_id}")
    print(f"Model: {result.model}")
    print(f"Contract: {prompt_version} / {schema_version}")
    print(f"Responsibilities: {result.responsibilities}")
    print(f"Requirements: {result.requirements}")
    return 0


def _run_capability_intelligence(
    arguments: list[str],
    *,
    default_config: Path | None,
) -> int:
    parser = _capability_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
        service = build_capability_intelligence_service(settings)
        result = service.analyze_job(parsed.job_id)
        artifact = CapabilityIntelligenceStore(settings.database_path).latest_current(
            parsed.job_id,
            model=result.model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Capability artifact is unavailable after successful analysis")
    except CapabilityIntelligenceError as exc:
        print(f"Capability intelligence is not ready: {exc}", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Capability intelligence failed: {exc}", file=sys.stderr)
        return 1

    print(f"Outcome: {result.outcome}")
    print(format_capability_intelligence(artifact))
    return 0


def _run_role_blueprint(
    arguments: list[str],
    *,
    default_config: Path | None,
) -> int:
    parser = _blueprint_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
        service = build_role_blueprint_service(settings)
        result = service.build(parsed.job_id)
        artifact = RoleBlueprintStore(settings.database_path).latest_current(
            parsed.job_id,
            model=result.model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Role Capability Blueprint is unavailable after successful build")
    except RoleBlueprintError as exc:
        print(f"Role Capability Blueprint is not ready: {exc}", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Role Capability Blueprint failed: {exc}", file=sys.stderr)
        return 1

    print(f"Outcome: {result.outcome}")
    print(format_role_blueprint(artifact))
    return 0


def _export_review_snapshot(
    arguments: list[str],
    *,
    default_config: Path | None,
) -> int:
    parser = _snapshot_parser(default_config=default_config)
    parsed = parser.parse_args(arguments)
    try:
        settings = _load_settings(parsed.config)
        destination = write_review_snapshot(
            settings.database_path,
            parsed.job_id,
            output_dir=parsed.output_dir,
            analysis_model=settings.effective_analysis_lm_studio_model(),
            capability_model=settings.effective_capability_lm_studio_model(),
            blueprint_model=settings.effective_blueprint_lm_studio_model(),
        )
    except (ReviewSnapshotError, OSError, ValueError) as exc:
        print(f"Review snapshot failed: {exc}", file=sys.stderr)
        return 1

    print(destination.as_posix())
    return 0


def _print_combined_help() -> None:
    build_legacy_parser().print_help()
    print("")
    print("Additional Phase-1 commands:")
    print("  run                      Run bounded source -> English -> analysis -> Market pipeline")
    print("  run --help               Show Phase-1 run limits and options")
    print("  jobs health <id>         Summarize last success/failures and lifecycle state")
    print("  jobs analyze <id>        Build/reuse targeted P1.6 analysis (English by default)")
    print("")
    print("Capability intelligence commands:")
    print("  jobs capability <id>     Build/reuse per-job capability/depth intelligence")
    print("  jobs blueprint <id>      Build/reuse human-facing expert role interpretation")
    print("  jobs snapshot <id>       Export current reviewable job/intelligence JSON")


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch newer commands while preserving every existing CLI command."""

    arguments = list(argv if argv is not None else sys.argv[1:])
    if arguments in (["-h"], ["--help"]):
        _print_combined_help()
        return 0

    is_run, default_config, run_arguments = _extract_run_invocation(arguments)
    if is_run:
        return _run_phase1(run_arguments, default_config=default_config)

    is_health, default_config, health_arguments = _extract_jobs_invocation(arguments, "health")
    if is_health:
        return _show_source_health(health_arguments, default_config=default_config)

    is_analysis, default_config, analysis_arguments = _extract_jobs_invocation(
        arguments,
        "analyze",
    )
    if is_analysis:
        return _run_job_analysis(
            analysis_arguments,
            default_config=default_config,
        )

    is_capability, default_config, capability_arguments = _extract_jobs_invocation(
        arguments,
        "capability",
    )
    if is_capability:
        return _run_capability_intelligence(
            capability_arguments,
            default_config=default_config,
        )

    is_blueprint, default_config, blueprint_arguments = _extract_jobs_invocation(
        arguments,
        "blueprint",
    )
    if is_blueprint:
        return _run_role_blueprint(
            blueprint_arguments,
            default_config=default_config,
        )

    is_snapshot, default_config, snapshot_arguments = _extract_jobs_invocation(
        arguments,
        "snapshot",
    )
    if is_snapshot:
        return _export_review_snapshot(
            snapshot_arguments,
            default_config=default_config,
        )

    return legacy_main(arguments)
