"""Command-line interface for JobHunter."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from pydantic import ValidationError

from jobhunter import __version__
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.doctor import format_report, run_doctor
from jobhunter.inference import LMStudioProvider

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
log_level = "INFO"
"""


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
    print("Start LM Studio's local server, then run: jobhunter doctor")
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

    parser.error(f"Unsupported command: {arguments.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
