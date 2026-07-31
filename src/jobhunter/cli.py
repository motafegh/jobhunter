"""Command-line interface for JobHunter."""

from __future__ import annotations

import argparse
import hashlib
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter import __version__
from jobhunter.config import ConfigLoadError, JobinjaSearchDefinition, Settings
from jobhunter.doctor import format_report, run_doctor
from jobhunter.evidence import EvidenceStore
from jobhunter.inference import LMStudioProvider
from jobhunter.job_audit import JobDetailAuditor, format_job_audit
from jobhunter.job_catalog import JobCatalog, format_job_list
from jobhunter.jobinja_batch import (
    JobinjaBatchFetchService,
    format_batch_fetch_summary,
)
from jobhunter.jobinja_detail_service import (
    JobinjaDetailService,
    JobNotFoundError,
    format_job_detail,
)
from jobhunter.jobinja_discovery import (
    DiscoverySearch,
    JobinjaDiscoveryService,
    format_discovery_summary,
)
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore

DEFAULT_CONFIG = """# JobHunter local configuration
[jobhunter]
data_dir = "data"
evidence_dir = "data/evidence"
database_path = "data/jobhunter.sqlite3"

# LM Studio normally exposes its OpenAI-compatible API on this local URL.
lm_studio_base_url = "http://127.0.0.1:1234/v1"
# Set this to an exact identifier returned by the LM Studio models endpoint.
# lm_studio_model = "your-model-identifier"
# Keep tokens in an environment variable rather than this file when enabled.
# lm_studio_api_token = ""

inference_timeout_seconds = 30.0
inference_max_retries = 1

# Public Jobinja acquisition settings.
jobinja_user_agent = "JobHunter/0.1 (local personal career research)"
jobinja_request_timeout_seconds = 30.0
jobinja_request_delay_seconds = 1.0

# Configure each search once. JobHunter discovers individual job URLs automatically.
# [[jobhunter.jobinja_searches]]
# name = "Artificial intelligence roles"
# url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
# enabled = true
# max_pages = 3

log_level = "INFO"
"""


def _bounded_page_count(value: str) -> int:
    try:
        page_count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("page count must be an integer") from exc
    if not 1 <= page_count <= 50:
        raise argparse.ArgumentTypeError("page count must be between 1 and 50")
    return page_count


def _bounded_batch_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("batch limit must be an integer") from exc
    if not 1 <= count <= 50:
        raise argparse.ArgumentTypeError("batch limit must be between 1 and 50")
    return count


def _bounded_list_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("list limit must be an integer") from exc
    if not 1 <= count <= 500:
        raise argparse.ArgumentTypeError("list limit must be between 1 and 500")
    return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter",
        description="Local-first personal career-intelligence application",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a local configuration file")
    init_parser.add_argument(
        "--path",
        type=Path,
        default=Path("jobhunter.toml"),
        help="Configuration file to create",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing configuration file",
    )

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check local storage, SQLite, and LM Studio connectivity",
    )
    doctor_parser.add_argument(
        "--smoke",
        action="store_true",
        help="Also request a small schema-conforming response from a local model",
    )

    jobinja_parser = subparsers.add_parser(
        "jobinja",
        help="Acquire and process approved public Jobinja pages",
    )
    jobinja_subparsers = jobinja_parser.add_subparsers(
        dest="jobinja_command",
        required=True,
    )
    discover_parser = jobinja_subparsers.add_parser(
        "discover",
        help="Discover and persist jobs from Jobinja search pages",
    )
    discover_parser.add_argument(
        "--url",
        action="append",
        default=[],
        help=(
            "One-off Jobinja search URL; repeat for multiple searches. "
            "When supplied, configured searches are not used."
        ),
    )
    discover_parser.add_argument(
        "--pages",
        type=_bounded_page_count,
        default=None,
        help="Override the configured maximum pages for this run (1-50)",
    )
    discover_parser.add_argument(
        "--show-jobs",
        action="store_true",
        help="Print canonical URLs for newly discovered jobs",
    )

    fetch_parser = jobinja_subparsers.add_parser(
        "fetch",
        help="Fetch and preserve complete pages for discovered Jobinja jobs",
    )
    fetch_parser.add_argument(
        "job_ids",
        nargs="*",
        help="Stable Jobinja job IDs already present in the local database",
    )
    fetch_parser.add_argument(
        "--missing",
        action="store_true",
        help="Fetch discovered jobs that do not yet have local detail content",
    )
    fetch_parser.add_argument(
        "--limit",
        type=_bounded_batch_count,
        default=None,
        help="Maximum jobs selected by --missing (default: 5, maximum: 50)",
    )

    jobs_parser = subparsers.add_parser(
        "jobs",
        help="Inspect locally stored job records",
    )
    jobs_subparsers = jobs_parser.add_subparsers(dest="jobs_command", required=True)
    list_parser = jobs_subparsers.add_parser(
        "list",
        help="List discovered jobs and their local detail status",
    )
    list_parser.add_argument(
        "--details",
        choices=("all", "missing", "available"),
        default="all",
        help="Filter by local detail availability",
    )
    list_parser.add_argument(
        "--limit",
        type=_bounded_list_count,
        default=50,
        help="Maximum jobs to display (default: 50, maximum: 500)",
    )

    audit_parser = jobs_subparsers.add_parser(
        "audit",
        help="Audit latest local detail parsing without network or LM Studio",
    )
    audit_parser.add_argument(
        "job_ids",
        nargs="*",
        help="Optional Jobinja job IDs; defaults to all jobs with local details",
    )
    audit_parser.add_argument(
        "--limit",
        type=_bounded_list_count,
        default=50,
        help="Maximum jobs to audit (default: 50, maximum: 500)",
    )
    audit_parser.add_argument(
        "--only-issues",
        action="store_true",
        help="Show only jobs with structural audit findings",
    )

    show_parser = jobs_subparsers.add_parser(
        "show",
        help="Show the latest locally stored complete job detail",
    )
    show_parser.add_argument("job_id", help="Stable Jobinja job ID, for example tpLF")

    return parser


def _load_settings(config_path: Path | None) -> Settings:
    try:
        return Settings.load(config_path)
    except (ConfigLoadError, ValidationError) as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc


def _initialize(path: Path, *, force: bool) -> int:
    path = path.expanduser()
    if path.exists() and not force:
        print(f"Configuration already exists: {path}", file=sys.stderr)
        print("Use --force only when replacement is intentional.", file=sys.stderr)
        return 1

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DEFAULT_CONFIG, encoding="utf-8")
        settings = Settings.load(path)
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        settings.evidence_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, ConfigLoadError, ValidationError) as exc:
        print(f"Initialization failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created configuration: {path.resolve()}")
    print(f"Created data directory: {settings.data_dir.resolve()}")
    print("Run a Jobinja search with: jobhunter jobinja discover --url '<search-url>'")
    return 0


def _discovery_searches(
    settings: Settings,
    *,
    command_urls: Sequence[str],
    page_override: int | None,
) -> list[DiscoverySearch]:
    if command_urls:
        searches: list[DiscoverySearch] = []
        for url in command_urls:
            digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
            definition = JobinjaSearchDefinition(
                name=f"adhoc-{digest}",
                url=url,
                max_pages=page_override or 1,
            )
            searches.append(
                DiscoverySearch(
                    name=definition.name,
                    url=definition.url,
                    max_pages=definition.max_pages,
                )
            )
        return searches

    return [
        DiscoverySearch(
            name=definition.name,
            url=definition.url,
            max_pages=page_override or definition.max_pages,
        )
        for definition in settings.jobinja_searches
        if definition.enabled
    ]


def _jobinja_client(settings: Settings) -> JobinjaClient:
    return JobinjaClient(
        user_agent=settings.jobinja_user_agent,
        timeout_seconds=settings.jobinja_request_timeout_seconds,
    )


def _detail_service(settings: Settings) -> JobinjaDetailService:
    return JobinjaDetailService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
    )


def _run_jobinja_discovery(settings: Settings, arguments: argparse.Namespace) -> int:
    try:
        searches = _discovery_searches(
            settings,
            command_urls=arguments.url,
            page_override=arguments.pages,
        )
    except ValidationError as exc:
        print(f"Jobinja search configuration error: {exc}", file=sys.stderr)
        return 2

    if not searches:
        print(
            "No enabled Jobinja searches are configured. Add one to jobhunter.toml "
            "or pass --url.",
            file=sys.stderr,
        )
        return 2

    service = JobinjaDiscoveryService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )
    summary = service.run(searches)
    print(format_discovery_summary(summary, show_jobs=arguments.show_jobs))
    return 0 if summary.succeeded else 1


def _run_jobinja_fetch(settings: Settings, arguments: argparse.Namespace) -> int:
    if arguments.missing and arguments.job_ids:
        print("Pass explicit job IDs or --missing, not both.", file=sys.stderr)
        return 2
    if not arguments.missing and arguments.limit is not None:
        print("--limit is only valid with --missing.", file=sys.stderr)
        return 2

    if arguments.missing:
        limit = arguments.limit or 5
        job_ids = JobCatalog(settings.database_path).missing_job_ids(limit=limit)
        if not job_ids:
            print("No discovered jobs are missing local detail content.")
            return 0
    else:
        job_ids = tuple(arguments.job_ids)
        if not job_ids:
            print("Pass one or more job IDs, or use --missing.", file=sys.stderr)
            return 2

    service = JobinjaBatchFetchService(
        detail_service=_detail_service(settings),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )
    summary = service.run(job_ids)
    print(format_batch_fetch_summary(summary))
    return 1 if summary.failures else 0


def _list_jobs(settings: Settings, arguments: argparse.Namespace) -> int:
    entries = JobCatalog(settings.database_path).list_jobs(
        detail_filter=arguments.details,
        limit=arguments.limit,
    )
    print(format_job_list(entries))
    return 0


def _audit_jobs(settings: Settings, arguments: argparse.Namespace) -> int:
    report = JobDetailAuditor(settings.database_path).audit(
        source_job_ids=tuple(arguments.job_ids),
        limit=arguments.limit,
    )
    print(format_job_audit(report, only_issues=arguments.only_issues))
    return 1 if report.needs_review else 0


def _show_job(settings: Settings, job_id: str) -> int:
    try:
        detail = _detail_service(settings).show(job_id)
    except JobNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(format_job_detail(detail))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "init":
        return _initialize(arguments.path, force=arguments.force)

    settings = _load_settings(arguments.config)
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    if arguments.command == "doctor":
        provider = LMStudioProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.lm_studio_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        )
        report = run_doctor(
            settings,
            provider,
            perform_smoke_test=arguments.smoke,
        )
        print(format_report(report))
        return 1 if report.has_failures else 0

    if arguments.command == "jobinja" and arguments.jobinja_command == "discover":
        return _run_jobinja_discovery(settings, arguments)
    if arguments.command == "jobinja" and arguments.jobinja_command == "fetch":
        return _run_jobinja_fetch(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "list":
        return _list_jobs(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "audit":
        return _audit_jobs(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "show":
        return _show_job(settings, arguments.job_id)

    parser.error(f"Unsupported command: {arguments.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
