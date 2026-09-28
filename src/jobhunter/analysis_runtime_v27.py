"""Isolated v27 provider combining source ownership with scoped inference."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v23 import _filter_unassigned_partition_claims
from jobhunter.analysis_runtime_v26 import V26CandidateAnalysisProvider
from jobhunter.analysis_service_v27 import JobAnalysisServiceV27
from jobhunter.config import Settings
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.evidence_refs_v27 import inherit_decomposed_required_residuals
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.instructor_lm_studio_v27 import JobAnalysisResponseV27
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V27CandidateAnalysisProvider(V26CandidateAnalysisProvider):
    def _prepare_inherited_additional_plan(
        self, plan: dict[str, dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        return plan

    def _run_once(self, **kwargs: Any) -> StructuredInferenceResult:
        kwargs = dict(kwargs)
        original_base = build_requirement_coverage_plan_v23(kwargs["effective_fields"])
        current_base = self._requirement_coverage_plan(kwargs["effective_fields"])
        complete_for_ownership = {**current_base, **kwargs["additional_plan"]}
        owned = inherit_decomposed_required_residuals(
            complete_for_ownership, original_base
        )
        kwargs["additional_plan"] = self._prepare_inherited_additional_plan({
            ref: owned[ref] for ref in kwargs["additional_plan"]
        })
        return super()._run_once(**kwargs)

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        refs = list(kwargs["requirement_coverage_plan"])
        refs.extend(kwargs["responsibility_coverage_plan"])
        result = complete_analysis_partition_with_instructor_v24(
            **kwargs,
            contract_version="v27",
            model_evidence_references=refs,
            response_model=JobAnalysisResponseV27,
        )
        return _filter_unassigned_partition_claims(
            result,
            requirement_plan=kwargs["requirement_coverage_plan"],
            responsibility_plan=kwargs["responsibility_coverage_plan"],
        )


def build_v27_analysis_service(settings: Settings) -> JobAnalysisServiceV27:
    """Build isolated candidate service over a private SQLite copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV27(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V27CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V27CandidateAnalysisProvider", "build_v27_analysis_service"]
