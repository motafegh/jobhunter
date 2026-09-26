"""Current P1.6 v23 provider and service wiring."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v20 import _v20_requirement_partitions
from jobhunter.analysis_runtime_v21 import V21CandidateAnalysisProvider
from jobhunter.analysis_service_v23 import JobAnalysisServiceV23
from jobhunter.config import Settings
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio_v23 import (
    complete_analysis_partition_with_instructor_v23,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V23CandidateAnalysisProvider(V21CandidateAnalysisProvider):
    """Keep proof preferences in their own bounded model partition."""

    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return build_requirement_coverage_plan_v23(model_fields)

    def _requirement_partitions(
        self, plan: dict[str, dict[str, Any]]
    ) -> list[dict[str, dict[str, Any]]]:
        partitions: list[dict[str, dict[str, Any]]] = []
        for source_kind in ("standard", "candidate_experience", "candidate_proof"):
            subset = {
                ref: candidate
                for ref, candidate in plan.items()
                if (
                    (source_kind == "standard" and candidate.get("source_kind") not in
                     {"candidate_experience", "candidate_proof"})
                    or candidate.get("source_kind") == source_kind
                )
            }
            if subset:
                partitions.extend(_v20_requirement_partitions(subset))
        return partitions

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        return complete_analysis_partition_with_instructor_v23(**kwargs)

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        return dict(persisted_v20_shape(structured))


def build_v23_analysis_service(settings: Settings) -> JobAnalysisServiceV23:
    """Build the shared current English service with local failure diagnostics."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV23(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V23CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V23CandidateAnalysisProvider", "build_v23_analysis_service"]
