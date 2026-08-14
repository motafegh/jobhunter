"""Current public P1.6 routing across accepted English and original-language contracts.

Historical analysis implementations remain versioned in ``analysis_service`` and
``analysis_service_v*``. This module is the public-current boundary: English P1.6 uses the
accepted v20/v5 path while original-language P1.6 remains on the independently validated v9/v4
path.
"""

from __future__ import annotations

from collections.abc import Callable

from jobhunter.analysis_runtime import build_job_analysis_service as build_v9_job_analysis_service
from jobhunter.analysis_runtime_v20 import build_v20_candidate_analysis_service
from jobhunter.analysis_service import (
    ANALYSIS_SCHEMA_VERSION as V9_ANALYSIS_SCHEMA_VERSION,
    ORIGINAL_PROMPT_VERSION,
    AnalysisBatchSummary,
    AnalysisFailure,
    AnalysisJobResult,
    AnalysisValidationError,
    JobAnalysisService as JobAnalysisServiceV9,
    format_analysis_batch_summary,
)
from jobhunter.analysis_service_v20 import (
    ANALYSIS_SCHEMA_VERSION as ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    JobAnalysisServiceV20,
)
from jobhunter.config import Settings
from jobhunter.inference import InferenceProviderError

ORIGINAL_ANALYSIS_SCHEMA_VERSION = V9_ANALYSIS_SCHEMA_VERSION
PROMPT_VERSION = ENGLISH_PROMPT_VERSION
ANALYSIS_SCHEMA_VERSION = ENGLISH_ANALYSIS_SCHEMA_VERSION


class JobAnalysisService:
    """Public-current P1.6 service with mode-specific accepted implementations."""

    def __init__(
        self,
        *,
        english_service: JobAnalysisServiceV20,
        original_service: JobAnalysisServiceV9,
    ) -> None:
        self._english_service = english_service
        self._original_service = original_service

    def analyze_english_job(self, source_job_id: str) -> AnalysisJobResult:
        """Build or reuse accepted English P1.6 v20/v5."""

        return self._english_service.analyze_english_job(source_job_id)

    def analyze_original_job(self, source_job_id: str) -> AnalysisJobResult:
        """Build or reuse accepted original-language P1.6 v9/v4."""

        return self._original_service.analyze_original_job(source_job_id)

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        """Canonical public analysis alias: accepted English P1.6."""

        return self.analyze_english_job(source_job_id)

    @staticmethod
    def _run_mode(
        source_job_ids: tuple[str, ...],
        *,
        analyzer: Callable[[str], AnalysisJobResult],
        mode: str,
        limit: int,
    ) -> AnalysisBatchSummary:
        unique = tuple(
            dict.fromkeys(job_id.strip() for job_id in source_job_ids if job_id.strip())
        )
        if not unique:
            raise ValueError("At least one job is required for analysis")
        if not 1 <= limit <= 20:
            raise ValueError("analysis limit must be between 1 and 20")

        results: list[AnalysisJobResult] = []
        failures: list[AnalysisFailure] = []
        for source_job_id in unique[:limit]:
            try:
                results.append(analyzer(source_job_id))
            except (
                AnalysisValidationError,
                InferenceProviderError,
                RuntimeError,
                ValueError,
            ) as exc:
                failures.append(AnalysisFailure(source_job_id=source_job_id, error=str(exc)))
        return AnalysisBatchSummary(
            attempted=min(len(unique), limit),
            results=tuple(results),
            failures=tuple(failures),
            analysis_mode=mode,
        )

    def run_english(
        self,
        source_job_ids: tuple[str, ...],
        *,
        limit: int = 5,
    ) -> AnalysisBatchSummary:
        """Run bounded accepted English P1.6 v20/v5."""

        return self._run_mode(
            source_job_ids,
            analyzer=self.analyze_english_job,
            mode="english",
            limit=limit,
        )

    def run_original(
        self,
        source_job_ids: tuple[str, ...],
        *,
        limit: int = 5,
    ) -> AnalysisBatchSummary:
        """Run bounded original-language P1.6 v9/v4."""

        return self._run_mode(
            source_job_ids,
            analyzer=self.analyze_original_job,
            mode="original",
            limit=limit,
        )

    def run(
        self,
        source_job_ids: tuple[str, ...],
        *,
        limit: int = 5,
    ) -> AnalysisBatchSummary:
        """Canonical public batch alias: accepted English P1.6."""

        return self.run_english(source_job_ids, limit=limit)


def build_job_analysis_service(settings: Settings) -> JobAnalysisService:
    """Build the current public P1.6 service without changing historical implementations."""

    return JobAnalysisService(
        english_service=build_v20_candidate_analysis_service(settings),
        original_service=build_v9_job_analysis_service(settings),
    )


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "ORIGINAL_ANALYSIS_SCHEMA_VERSION",
    "ORIGINAL_PROMPT_VERSION",
    "PROMPT_VERSION",
    "AnalysisBatchSummary",
    "AnalysisFailure",
    "AnalysisJobResult",
    "AnalysisValidationError",
    "JobAnalysisService",
    "build_job_analysis_service",
    "format_analysis_batch_summary",
]
