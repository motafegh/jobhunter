"""Local environment and LM Studio health checks."""

from __future__ import annotations

import os
import sqlite3
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from jobhunter.config import Settings
from jobhunter.inference import InferenceProvider, InferenceProviderError


class CheckStatus(StrEnum):
    PASS = "PASS"
    WARNING = "WARN"
    FAILURE = "FAIL"


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True, slots=True)
class DoctorReport:
    checks: tuple[CheckResult, ...]

    @property
    def has_failures(self) -> bool:
        return any(check.status is CheckStatus.FAILURE for check in self.checks)


def _check_writable_directory(name: str, directory: Path) -> CheckResult:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".jobhunter-check-", delete=True):
            pass
    except OSError as exc:
        return CheckResult(name, CheckStatus.FAILURE, f"{directory}: {exc}")
    return CheckResult(name, CheckStatus.PASS, str(directory.resolve()))


def _check_database(database_path: Path) -> CheckResult:
    try:
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(database_path) as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("SELECT 1")
    except (OSError, sqlite3.Error) as exc:
        return CheckResult("SQLite", CheckStatus.FAILURE, f"{database_path}: {exc}")
    return CheckResult("SQLite", CheckStatus.PASS, str(database_path.resolve()))


def run_doctor(
    settings: Settings,
    provider: InferenceProvider,
    *,
    perform_smoke_test: bool = False,
) -> DoctorReport:
    """Run deterministic local checks followed by LM Studio checks."""

    checks: list[CheckResult] = [
        CheckResult("Configuration", CheckStatus.PASS, "Settings loaded and validated"),
        _check_writable_directory("Data directory", settings.data_dir),
        _check_writable_directory("Evidence directory", settings.evidence_dir),
        _check_database(settings.database_path),
    ]

    try:
        models = provider.list_models()
    except InferenceProviderError as exc:
        checks.append(CheckResult("LM Studio", CheckStatus.FAILURE, str(exc)))
        return DoctorReport(tuple(checks))

    if models:
        checks.append(
            CheckResult(
                "LM Studio",
                CheckStatus.PASS,
                f"Reachable; {len(models)} model(s) visible",
            )
        )
    else:
        checks.append(
            CheckResult(
                "LM Studio",
                CheckStatus.WARNING,
                "Reachable, but no models are visible to the server",
            )
        )

    analysis_model = settings.effective_analysis_lm_studio_model()
    if analysis_model:
        if analysis_model in models:
            checks.append(
                CheckResult(
                    "Analysis model",
                    CheckStatus.PASS,
                    analysis_model,
                )
            )
        else:
            checks.append(
                CheckResult(
                    "Analysis model",
                    CheckStatus.WARNING,
                    f"{analysis_model!r} is not in the visible model list",
                )
            )
    else:
        checks.append(
            CheckResult(
                "Analysis model",
                CheckStatus.WARNING,
                "No analysis model resolves from analysis_lm_studio_model, "
                "lm_studio_model, or translation_lm_studio_model",
            )
        )

    if perform_smoke_test:
        try:
            model_used = provider.structured_smoke_test(analysis_model)
        except InferenceProviderError as exc:
            checks.append(
                CheckResult("Structured inference", CheckStatus.FAILURE, str(exc))
            )
        else:
            checks.append(
                CheckResult(
                    "Structured inference",
                    CheckStatus.PASS,
                    f"Schema-conforming response received from {model_used}",
                )
            )

    return DoctorReport(tuple(checks))


def format_report(report: DoctorReport) -> str:
    """Format a report for terminal display without external UI dependencies."""

    width = max(len(check.name) for check in report.checks)
    lines = [
        f"[{check.status.value:<4}] {check.name:<{width}}  {check.detail}"
        for check in report.checks
    ]
    return os.linesep.join(lines)
