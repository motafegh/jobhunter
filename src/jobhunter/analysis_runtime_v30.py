"""Isolated v30 provider for source-explicit experience ontology."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v23 import _filter_unassigned_partition_claims
from jobhunter.analysis_runtime_v29 import V29CandidateAnalysisProvider
from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
from jobhunter.config import Settings
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.instructor_lm_studio_v30 import JobAnalysisResponseV30
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V30CandidateAnalysisProvider(V29CandidateAnalysisProvider):
    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        refs = list(kwargs["requirement_coverage_plan"])
        refs.extend(kwargs["responsibility_coverage_plan"])
        result = complete_analysis_partition_with_instructor_v24(
            **kwargs,
            contract_version="v30",
            model_evidence_references=refs,
            response_model=JobAnalysisResponseV30,
        )
        return _filter_unassigned_partition_claims(
            result,
            requirement_plan=kwargs["requirement_coverage_plan"],
            responsibility_plan=kwargs["responsibility_coverage_plan"],
        )


def build_v30_analysis_service(settings: Settings) -> JobAnalysisServiceV30:
    """Build isolated candidate service over a private SQLite copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV30(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V30CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V30CandidateAnalysisProvider", "build_v30_analysis_service"]
