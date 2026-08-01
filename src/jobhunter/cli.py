"""Command-line interface for JobHunter."""

from __future__ import annotations

import argparse
import hashlib
import logging
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from jobhunter import __version__
from jobhunter.config import ConfigLoadError, JobinjaSearchDefinition, Settings
from jobhunter.doctor import format_report, run_doctor
from jobhunter.evidence import EvidenceStore
from jobhunter.inference import LMStudioProvider
from jobhunter.job_audit import JobDetailAuditor, format_job_audit
from jobhunter.job_catalog import JobCatalog, format_job_list
from jobhunter.job_detail_observations import (
    JobDetailObservationStore,
    format_job_detail_observations,
)
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
from jobhunter.jobinja_sync import JobinjaSyncService, format_sync_summary
from jobhunter.search_registry import expand_keyword_searches, format_search_catalog
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore
from jobhunter.translation import (
    GoogleCloudTranslationProvider,
    LMStudioTranslationProvider,
    TranslationError,
)
from jobhunter.translation_export import export_english_corpus
from jobhunter.translation_service import (
    TranslationService,
    format_translation_artifact,
    format_translation_batch_summary,
)
from jobhunter.translation_store import TranslationStore

DEFAULT_CONFIG = """# JobHunter local configuration
[jobhunter]
data_dir = "data"
evidence_dir = "data/evidence"
database_path = "data/jobhunter.sqlite3"

# LM Studio normally exposes its OpenAI-compatible API on this local URL.
lm_studio_base_url = "http://127.0.0.1:1234/v1"
# lm_studio_model = "your-model-identifier"
inference_timeout_seconds = 30.0
inference_max_retries = 1

# Public Jobinja acquisition settings.
jobinja_user_agent = "JobHunter/0.1 (local personal career research)"
jobinja_request_timeout_seconds = 30.0
jobinja_request_delay_seconds = 1.0
jobinja_search_request_budget = 40
jobinja_max_expanded_searches = 40
jobinja_default_keyword_max_pages = 1
# Optional complete replacement vocabulary file using the documented TOML schema.
# jobinja_search_catalog_path = "my-search-catalog.toml"

jobinja_search_profiles = ["ai-security-python"]
jobinja_search_packs = []
jobinja_excluded_terms = []

jobinja_sync_missing_limit = 10
jobinja_sync_refresh_limit = 5
jobinja_refresh_after_hours = 24.0

# Derived English corpus. LM Studio is the local-first default translator.
translation_enabled = false
translation_auto_after_sync = false
translation_provider = "lm-studio"
translation_target_language = "en"
translation_batch_limit = 20
translation_timeout_seconds = 30.0
translation_max_retries = 1
# Optional dedicated translation model. If omitted, lm_studio_model is reused;
# if both are omitted, JobHunter auto-selects only when exactly one model is visible.
# translation_lm_studio_model = "your-translation-model-identifier"
translation_lm_studio_max_tokens = 4096
translation_lm_studio_character_target = 6000

# Google Cloud Translation remains an optional provider.
google_translation_model = "nmt"
# Set JOBHUNTER_GOOGLE_TRANSLATION_API_KEY only when using google-cloud.

# Optional custom bilingual group.
# [[jobhunter.jobinja_keyword_groups]]
# name = "My focused roles"
# terms = ["مهندس امنیت هوش مصنوعی", "AI Security Engineer", "Python Security"]
# enabled = true
# max_pages = 1

# Optional raw Jobinja search URL for filters not represented by keyword groups.
# [[jobhunter.jobinja_searches]]
# name = "Tehran remote AI roles"
# url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
# enabled = true
# max_pages = 2

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


def _optional_batch_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("sync detail limit must be an integer") from exc
    if not 0 <= count <= 50:
        raise argparse.ArgumentTypeError("sync detail limit must be between 0 and 50")
    return count


def _bounded_list_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("list limit must be an integer") from exc
    if not 1 <= count <= 500:
        raise argparse.ArgumentTypeError("list limit must be between 1 and 500")
    return count


def _bounded_observation_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("check-history limit must be an integer") from exc
    if not 1 <= count <= 200:
        raise argparse.ArgumentTypeError(
            "check-history limit must be between 1 and 200"
        )
    return count


def _bounded_request_budget(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("request budget must be an integer") from exc
    if not 1 <= count <= 500:
        raise argparse.ArgumentTypeError("request budget must be between 1 and 500")
    return count


def _nonnegative_offset(value: str) -> int:
    try:
        offset = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("search offset must be an integer") from exc
    if offset < 0:
        raise argparse.ArgumentTypeError("search offset must not be negative")
    return offset


def _positive_hours(value: str) -> float:
    try:
        hours = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("hours must be a number") from exc
    if not 0 < hours <= 8760:
        raise argparse.ArgumentTypeError("hours must be greater than 0 and at most 8760")
    return hours


def _add_search_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="One-off raw Jobinja search URL; repeat for multiple URLs",
    )
    parser.add_argument(
        "--profile",
        action="append",
        default=[],
        help="Bilingual search profile; repeat to combine profiles",
    )
    parser.add_argument(
        "--pack",
        action="append",
        default=[],
        help="Bilingual search pack; repeat to combine packs",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        help="One-off Persian or English keyword term; repeat for multiple terms",
    )
    parser.add_argument(
        "--pages",
        type=_bounded_page_count,
        default=None,
        help="Override maximum pages for every selected search (1-50)",
    )
    parser.add_argument(
        "--request-budget",
        type=_bounded_request_budget,
        default=None,
        help="Maximum Jobinja search-page requests for this run (1-500)",
    )
    parser.add_argument(
        "--search-limit",
        type=_bounded_list_count,
        default=None,
        help="Maximum expanded searches selected for this run (1-500)",
    )
    parser.add_argument(
        "--search-offset",
        type=_nonnegative_offset,
        default=0,
        help="Rotate the expanded plan before applying --search-limit",
    )


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

    catalog_parser = jobinja_subparsers.add_parser(
        "catalog",
        help="List data-driven bilingual search profiles and packs",
    )
    catalog_parser.add_argument(
        "--show-terms",
        action="store_true",
        help="Show every term loaded from the effective search catalog",
    )

    plan_parser = jobinja_subparsers.add_parser(
        "plan",
        help="Expand and inspect the effective search plan without network access",
    )
    _add_search_selection_arguments(plan_parser)
    plan_parser.add_argument(
        "--show-urls",
        action="store_true",
        help="Include canonical Jobinja URLs in the plan",
    )

    discover_parser = jobinja_subparsers.add_parser(
        "discover",
        help="Discover and persist jobs from configured or selected searches",
    )
    _add_search_selection_arguments(discover_parser)
    discover_parser.add_argument(
        "--show-jobs",
        action="store_true",
        help="Print canonical URLs for newly discovered jobs",
    )

    sync_parser = jobinja_subparsers.add_parser(
        "sync",
        help="Run bounded discovery, detail acquisition, audit, and optional translation",
    )
    _add_search_selection_arguments(sync_parser)
    sync_parser.add_argument(
        "--missing-limit",
        type=_optional_batch_count,
        default=None,
        help="Maximum newly discovered jobs to fetch (0-50)",
    )
    sync_parser.add_argument(
        "--refresh-limit",
        type=_optional_batch_count,
        default=None,
        help="Maximum refresh-due jobs to check (0-50)",
    )
    sync_parser.add_argument(
        "--refresh-after-hours",
        type=_positive_hours,
        default=None,
        help="Age threshold used for refresh-due selection",
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
        "--refresh-due",
        action="store_true",
        help="Fetch acquired jobs whose latest recorded check is old enough",
    )
    fetch_parser.add_argument(
        "--older-than-hours",
        type=_positive_hours,
        default=None,
        help="Age threshold for --refresh-due (default from configuration)",
    )
    fetch_parser.add_argument(
        "--limit",
        type=_bounded_batch_count,
        default=None,
        help=(
            "Maximum jobs selected by --missing or --refresh-due "
            "(default: 5, maximum: 50)"
        ),
    )

    jobs_parser = subparsers.add_parser("jobs", help="Inspect locally stored job records")
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

    checks_parser = jobs_subparsers.add_parser(
        "checks",
        help="Show recorded detail-fetch checks for one Jobinja job",
    )
    checks_parser.add_argument("job_id", help="Stable Jobinja job ID")
    checks_parser.add_argument(
        "--limit",
        type=_bounded_observation_count,
        default=20,
        help="Maximum observations to show (default: 20, maximum: 200)",
    )

    show_parser = jobs_subparsers.add_parser(
        "show",
        help="Show the latest locally stored complete job detail",
    )
    show_parser.add_argument("job_id", help="Stable Jobinja job ID, for example tpLF")

    translations_parser = subparsers.add_parser(
        "translations",
        help="Create and inspect the separate English corpus",
    )
    translation_subparsers = translations_parser.add_subparsers(
        dest="translations_command",
        required=True,
    )
    translation_subparsers.add_parser(
        "status",
        help="Show translation configuration and current corpus coverage",
    )
    translation_subparsers.add_parser(
        "models",
        help="List exact model identifiers visible to the local LM Studio server",
    )
    translation_run = translation_subparsers.add_parser(
        "run",
        help="Create English projections for explicit jobs or a missing queue",
    )
    translation_run.add_argument("job_ids", nargs="*", help="Optional Jobinja job IDs")
    translation_run.add_argument(
        "--missing",
        action="store_true",
        help="Translate latest source versions missing a current English artifact",
    )
    translation_run.add_argument(
        "--limit",
        type=_bounded_batch_count,
        default=None,
        help="Maximum missing translations to create (default from configuration)",
    )
    translation_show = translation_subparsers.add_parser(
        "show",
        help="Show the current English projection for one job",
    )
    translation_show.add_argument("job_id", help="Stable Jobinja job ID")
    translation_export = translation_subparsers.add_parser(
        "export",
        help="Export the current English corpus as JSON Lines",
    )
    translation_export.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Output path (default: data/exports/job_english_corpus.jsonl)",
    )
    translation_export.add_argument(
        "--limit",
        type=_bounded_list_count,
        default=500,
        help="Maximum current English artifacts to export",
    )

    return parser


def _load_settings(config_path: Path | None) -> Settings:
    try:
        return Settings.load(config_path)
    except (ConfigLoadError, ValidationError, ValueError) as exc:
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
    except (OSError, ConfigLoadError, ValidationError, ValueError) as exc:
        print(f"Initialization failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created configuration: {path.resolve()}")
    print(f"Created data directory: {settings.data_dir.resolve()}")
    print("Inspect the bilingual plan with: jobhunter jobinja plan")
    return 0


def _explicit_search_selection(arguments: argparse.Namespace) -> bool:
    return bool(arguments.url or arguments.profile or arguments.pack or arguments.term)


def _rotate_and_limit_searches(
    searches: list[DiscoverySearch],
    *,
    offset: int,
    limit: int,
) -> list[DiscoverySearch]:
    if not searches:
        return []
    effective_offset = offset % len(searches)
    rotated = searches[effective_offset:] + searches[:effective_offset]
    return rotated[:limit]


def _discovery_searches(
    settings: Settings,
    *,
    arguments: argparse.Namespace,
) -> list[DiscoverySearch]:
    explicit = _explicit_search_selection(arguments)
    page_override = arguments.pages
    searches: list[DiscoverySearch] = []

    raw_definitions: list[JobinjaSearchDefinition] = []
    if explicit:
        for url in arguments.url:
            digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
            raw_definitions.append(
                JobinjaSearchDefinition(
                    name=f"adhoc-url-{digest}",
                    url=url,
                    max_pages=page_override or 1,
                )
            )
    else:
        raw_definitions.extend(
            definition for definition in settings.jobinja_searches if definition.enabled
        )

    searches.extend(
        DiscoverySearch(
            name=definition.name,
            url=definition.url,
            max_pages=page_override or definition.max_pages,
        )
        for definition in raw_definitions
    )

    if explicit:
        keyword_searches = expand_keyword_searches(
            pack_names=tuple(arguments.pack),
            profile_names=tuple(arguments.profile),
            extra_terms=tuple(arguments.term),
            excluded_terms=tuple(settings.jobinja_excluded_terms),
            default_max_pages=page_override or settings.jobinja_default_keyword_max_pages,
            catalog=settings.search_catalog(),
        )
    else:
        keyword_searches = settings.expanded_keyword_searches()

    searches.extend(
        DiscoverySearch(
            name=search.name,
            url=search.url,
            max_pages=page_override or search.max_pages,
        )
        for search in keyword_searches
    )

    unique_by_url: dict[str, DiscoverySearch] = {}
    for search in searches:
        unique_by_url.setdefault(search.url, search)
    unique_searches = list(unique_by_url.values())
    limit = arguments.search_limit or settings.jobinja_max_expanded_searches
    return _rotate_and_limit_searches(
        unique_searches,
        offset=arguments.search_offset,
        limit=limit,
    )


def _format_effective_search_plan(
    searches: Sequence[DiscoverySearch],
    *,
    request_budget: int,
    show_urls: bool,
) -> str:
    planned_requests = sum(search.max_pages for search in searches)
    lines = [
        "Effective Jobinja search plan",
        f"Searches selected: {len(searches)}",
        f"Planned page requests: {planned_requests}",
        f"Request budget: {request_budget}",
        f"Maximum requests this run: {min(planned_requests, request_budget)}",
    ]
    if planned_requests > request_budget:
        lines.append(
            "The plan exceeds the request budget; remaining searches are retained "
            "in the plan but reported as request_budget_reached."
        )
    if not searches:
        lines.append("No searches are configured or selected.")
        return "\n".join(lines)

    lines.append("Searches:")
    for index, search in enumerate(searches, start=1):
        lines.append(f"- {index}. {search.name} [max_pages={search.max_pages}]")
        if show_urls:
            lines.append(f"  {search.url}")
    return "\n".join(lines)


def _jobinja_client(settings: Settings) -> JobinjaClient:
    return JobinjaClient(
        user_agent=settings.jobinja_user_agent,
        timeout_seconds=settings.jobinja_request_timeout_seconds,
    )


def _observation_store(settings: Settings) -> JobDetailObservationStore:
    return JobDetailObservationStore(settings.database_path)


def _detail_service(settings: Settings) -> JobinjaDetailService:
    return JobinjaDetailService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        observation_store=_observation_store(settings),
    )


def _batch_service(settings: Settings) -> JobinjaBatchFetchService:
    return JobinjaBatchFetchService(
        detail_service=_detail_service(settings),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )


def _discovery_service(
    settings: Settings,
    *,
    request_budget: int,
) -> JobinjaDiscoveryService:
    return JobinjaDiscoveryService(
        client=_jobinja_client(settings),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
        request_budget=request_budget,
    )


def _translation_store(settings: Settings) -> TranslationStore:
    return TranslationStore(settings.database_path)


def _translation_service(settings: Settings) -> TranslationService:
    provider = None
    if (
        settings.translation_enabled
        and settings.translation_provider == "google-cloud"
        and not settings.google_translation_api_key
    ):
        raise ValueError(
            "Google translation is enabled but "
            "JOBHUNTER_GOOGLE_TRANSLATION_API_KEY is not configured"
        )

    if settings.translation_enabled and settings.translation_provider == "lm-studio":
        provider = LMStudioTranslationProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.effective_translation_lm_studio_model(),
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
            max_tokens=settings.translation_lm_studio_max_tokens,
            request_character_target=settings.translation_lm_studio_character_target,
        )
    elif settings.translation_enabled and settings.translation_provider == "google-cloud":
        provider = GoogleCloudTranslationProvider(
            api_key=settings.google_translation_api_key or "",
            model=settings.google_translation_model,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
        )
    return TranslationService(
        store=_translation_store(settings),
        provider=provider,
        target_language=settings.translation_target_language,
    )


def _resolve_searches(
    settings: Settings,
    arguments: argparse.Namespace,
) -> tuple[list[DiscoverySearch], int]:
    searches = _discovery_searches(settings, arguments=arguments)
    request_budget = arguments.request_budget or settings.jobinja_search_request_budget
    return searches, request_budget


def _run_jobinja_plan(settings: Settings, arguments: argparse.Namespace) -> int:
    try:
        searches, request_budget = _resolve_searches(settings, arguments)
    except (ValidationError, ValueError) as exc:
        print(f"Jobinja search plan error: {exc}", file=sys.stderr)
        return 2
    print(
        _format_effective_search_plan(
            searches,
            request_budget=request_budget,
            show_urls=arguments.show_urls,
        )
    )
    return 0 if searches else 1


def _run_jobinja_discovery(settings: Settings, arguments: argparse.Namespace) -> int:
    try:
        searches, request_budget = _resolve_searches(settings, arguments)
    except (ValidationError, ValueError) as exc:
        print(f"Jobinja search configuration error: {exc}", file=sys.stderr)
        return 2

    if not searches:
        print(
            "No enabled Jobinja searches are configured. Add a profile, pack, "
            "custom keyword group, raw URL, or command-line selector.",
            file=sys.stderr,
        )
        return 2

    summary = _discovery_service(
        settings,
        request_budget=request_budget,
    ).run(searches)
    print(format_discovery_summary(summary, show_jobs=arguments.show_jobs))
    return 0 if summary.succeeded else 1


def _run_jobinja_sync(settings: Settings, arguments: argparse.Namespace) -> int:
    try:
        searches, request_budget = _resolve_searches(settings, arguments)
    except (ValidationError, ValueError) as exc:
        print(f"Jobinja sync search configuration error: {exc}", file=sys.stderr)
        return 2
    if not searches:
        print("No enabled Jobinja searches are configured for sync.", file=sys.stderr)
        return 2

    missing_limit = (
        settings.jobinja_sync_missing_limit
        if arguments.missing_limit is None
        else arguments.missing_limit
    )
    refresh_limit = (
        settings.jobinja_sync_refresh_limit
        if arguments.refresh_limit is None
        else arguments.refresh_limit
    )
    if missing_limit + refresh_limit > 50:
        print(
            "Combined --missing-limit and --refresh-limit may not exceed 50.",
            file=sys.stderr,
        )
        return 2
    refresh_after_hours = (
        settings.jobinja_refresh_after_hours
        if arguments.refresh_after_hours is None
        else arguments.refresh_after_hours
    )

    service = JobinjaSyncService(
        discovery_service=_discovery_service(
            settings,
            request_budget=request_budget,
        ),
        batch_service=_batch_service(settings),
        catalog=JobCatalog(settings.database_path),
        observations=_observation_store(settings),
        auditor=JobDetailAuditor(settings.database_path),
    )
    summary = service.run(
        searches,
        missing_limit=missing_limit,
        refresh_limit=refresh_limit,
        refresh_after_hours=refresh_after_hours,
    )
    print(format_sync_summary(summary))

    translation_failed = False
    if settings.translation_enabled and settings.translation_auto_after_sync:
        preferred_ids = (
            tuple(result.source_job_id for result in summary.detail_fetch.results)
            if summary.detail_fetch is not None
            else ()
        )
        try:
            translation_summary = _translation_service(settings).run(
                missing=True,
                limit=settings.translation_batch_limit,
                preferred_ids=preferred_ids,
            )
        except ValueError as exc:
            print(f"Translation configuration error: {exc}", file=sys.stderr)
            return 2
        print("")
        print(format_translation_batch_summary(translation_summary))
        translation_failed = bool(translation_summary.failures)

    return 0 if summary.succeeded and not translation_failed else 1


def _run_jobinja_fetch(settings: Settings, arguments: argparse.Namespace) -> int:
    selection_modes = sum(
        (
            bool(arguments.job_ids),
            arguments.missing,
            arguments.refresh_due,
        )
    )
    if selection_modes != 1:
        print(
            "Choose exactly one: explicit job IDs, --missing, or --refresh-due.",
            file=sys.stderr,
        )
        return 2
    if arguments.older_than_hours is not None and not arguments.refresh_due:
        print("--older-than-hours is only valid with --refresh-due.", file=sys.stderr)
        return 2
    if arguments.limit is not None and arguments.job_ids:
        print("--limit is only valid with --missing or --refresh-due.", file=sys.stderr)
        return 2

    limit = arguments.limit or 5
    if arguments.missing:
        job_ids = JobCatalog(settings.database_path).missing_job_ids(limit=limit)
        if not job_ids:
            print("No discovered jobs are missing local detail content.")
            return 0
    elif arguments.refresh_due:
        older_than_hours = (
            arguments.older_than_hours or settings.jobinja_refresh_after_hours
        )
        job_ids = _observation_store(settings).refresh_due_job_ids(
            as_of=datetime.now(UTC),
            older_than_hours=older_than_hours,
            limit=limit,
        )
        if not job_ids:
            print(
                "No acquired jobs are due for a detail refresh at the requested age."
            )
            return 0
    else:
        job_ids = tuple(arguments.job_ids)

    summary = _batch_service(settings).run(job_ids)
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


def _show_checks(settings: Settings, arguments: argparse.Namespace) -> int:
    observations = _observation_store(settings).list_for_job(
        arguments.job_id,
        limit=arguments.limit,
    )
    print(
        format_job_detail_observations(
            observations,
            source_job_id=arguments.job_id,
        )
    )
    return 0


def _show_job(settings: Settings, job_id: str) -> int:
    try:
        detail = _detail_service(settings).show(job_id)
    except JobNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(format_job_detail(detail))
    return 0


def _translation_status(settings: Settings) -> int:
    store = _translation_store(settings)
    sources = store.latest_source_versions(limit=5000)
    artifacts = store.list_latest_artifacts(target_language="en", limit=5000)
    print("English translation corpus status")
    print(f"Translation enabled: {'yes' if settings.translation_enabled else 'no'}")
    print(f"Automatic after sync: {'yes' if settings.translation_auto_after_sync else 'no'}")
    print(f"Provider: {settings.translation_provider}")
    if settings.translation_provider == "lm-studio":
        selected_model = settings.effective_translation_lm_studio_model()
        print(f"LM Studio base URL: {settings.lm_studio_base_url}")
        print(
            "Model: "
            + (
                selected_model
                if selected_model
                else "(auto-select only when exactly one model is visible)"
            )
        )
        print("External translation service: no")
    else:
        print(f"Model: {settings.google_translation_model}")
        print(
            "Google API key configured: "
            f"{'yes' if settings.google_translation_api_key else 'no'}"
        )
        print("External translation service: yes")
    print(f"Latest parsed source versions: {len(sources)}")
    print(f"Current English artifacts: {len(artifacts)}")
    print(f"Source versions without current English artifact: {len(sources) - len(artifacts)}")
    return 0


def _translation_models(settings: Settings) -> int:
    provider = LMStudioTranslationProvider(
        base_url=settings.lm_studio_base_url,
        configured_model=settings.effective_translation_lm_studio_model(),
        api_token=settings.lm_studio_api_token,
        timeout_seconds=settings.translation_timeout_seconds,
        max_retries=settings.translation_max_retries,
        max_tokens=settings.translation_lm_studio_max_tokens,
        request_character_target=settings.translation_lm_studio_character_target,
    )
    try:
        models = provider.list_models()
    except TranslationError as exc:
        print(f"LM Studio model discovery failed: {exc}", file=sys.stderr)
        return 1
    print("LM Studio models visible to JobHunter")
    if not models:
        print("- (none)")
        return 0
    configured = settings.effective_translation_lm_studio_model()
    for model in models:
        marker = " [configured]" if model == configured else ""
        print(f"- {model}{marker}")
    return 0


def _run_translations(settings: Settings, arguments: argparse.Namespace) -> int:
    if not settings.translation_enabled:
        print(
            "Translation is disabled. Set translation_enabled = true after selecting "
            "the intended translation provider.",
            file=sys.stderr,
        )
        return 2
    if arguments.job_ids and arguments.missing:
        print("Choose explicit job IDs or --missing, not both.", file=sys.stderr)
        return 2
    try:
        service = _translation_service(settings)
    except ValueError as exc:
        print(f"Translation configuration error: {exc}", file=sys.stderr)
        return 2
    summary = service.run(
        source_job_ids=tuple(arguments.job_ids),
        missing=arguments.missing or not arguments.job_ids,
        limit=arguments.limit or settings.translation_batch_limit,
    )
    print(format_translation_batch_summary(summary))
    return 1 if summary.failures else 0


def _show_translation(settings: Settings, job_id: str) -> int:
    artifact = _translation_store(settings).latest_artifact(job_id, target_language="en")
    if artifact is None:
        print(
            f"Job {job_id!r} has no English artifact for its latest semantic version.",
            file=sys.stderr,
        )
        return 1
    print(format_translation_artifact(artifact))
    return 0


def _export_translations(settings: Settings, arguments: argparse.Namespace) -> int:
    output_path = arguments.path or settings.data_dir / "exports/job_english_corpus.jsonl"
    try:
        result = export_english_corpus(
            _translation_store(settings),
            output_path=output_path,
            limit=arguments.limit,
        )
    except OSError as exc:
        print(f"English corpus export failed: {exc}", file=sys.stderr)
        return 1
    print(f"English corpus exported: {result.records} records")
    print(f"Path: {result.path}")
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

    if arguments.command == "jobinja" and arguments.jobinja_command == "catalog":
        print(
            format_search_catalog(
                settings.search_catalog(),
                show_terms=arguments.show_terms,
            )
        )
        return 0
    if arguments.command == "jobinja" and arguments.jobinja_command == "plan":
        return _run_jobinja_plan(settings, arguments)
    if arguments.command == "jobinja" and arguments.jobinja_command == "discover":
        return _run_jobinja_discovery(settings, arguments)
    if arguments.command == "jobinja" and arguments.jobinja_command == "sync":
        return _run_jobinja_sync(settings, arguments)
    if arguments.command == "jobinja" and arguments.jobinja_command == "fetch":
        return _run_jobinja_fetch(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "list":
        return _list_jobs(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "audit":
        return _audit_jobs(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "checks":
        return _show_checks(settings, arguments)
    if arguments.command == "jobs" and arguments.jobs_command == "show":
        return _show_job(settings, arguments.job_id)
    if arguments.command == "translations" and arguments.translations_command == "status":
        return _translation_status(settings)
    if arguments.command == "translations" and arguments.translations_command == "models":
        return _translation_models(settings)
    if arguments.command == "translations" and arguments.translations_command == "run":
        return _run_translations(settings, arguments)
    if arguments.command == "translations" and arguments.translations_command == "show":
        return _show_translation(settings, arguments.job_id)
    if arguments.command == "translations" and arguments.translations_command == "export":
        return _export_translations(settings, arguments)

    parser.error(f"Unsupported command: {arguments.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
