"""Runtime wiring for P1.6 v21 scoped-evidence analysis."""

from __future__ import annotations

import json
from contextvars import ContextVar
from typing import Any

from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
from jobhunter.analysis_runtime_v20 import (
    V20CandidateAnalysisProvider,
    _v20_requirement_partitions,
)
from jobhunter.analysis_service_v21 import JobAnalysisServiceV21
from jobhunter.config import Settings
from jobhunter.evidence_refs_v21 import (
    build_requirement_coverage_plan_v21,
    build_responsibility_coverage_plan_v21,
)
from jobhunter.inference.instructor_lm_studio_v21 import (
    complete_analysis_partition_with_instructor_v21,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

# Per invocation, never on a shared provider instance. Each value holds only
# structured model-valid partition data, NOT a fully validated P1.6 artifact.
_PARTITION_EVIDENCE: ContextVar[list[tuple[int, int, str]] | None] = ContextVar(
    "v21_failure_partition_evidence", default=None
)


def _v21_requirement_partitions(
    plan: dict[str, dict[str, Any]],
) -> list[dict[str, dict[str, Any]]]:
    """Keep explicit headingless candidate experience out of dense section partitions."""
    section_plan = {
        reference: candidate
        for reference, candidate in plan.items()
        if candidate.get("source_kind") != "candidate_experience"
    }
    candidate_experience_plan = {
        reference: candidate
        for reference, candidate in plan.items()
        if candidate.get("source_kind") == "candidate_experience"
    }
    partitions: list[dict[str, dict[str, Any]]] = []
    if section_plan:
        partitions.extend(_v20_requirement_partitions(section_plan))
    if candidate_experience_plan:
        partitions.extend(_v20_requirement_partitions(candidate_experience_plan))
    return partitions


class V21CandidateAnalysisProvider(V20CandidateAnalysisProvider):
    """Use v21 validation and preserve bounded non-authoritative failure context."""

    def _run_once(self, **kwargs: Any) -> StructuredInferenceResult:
        token = _PARTITION_EVIDENCE.set([])
        try:
            return super()._run_once(**kwargs)
        except Exception as exc:
            # Scope/global checks occur in the parent, after a partition returns.
            # Do not mislabel a model-valid partition as fully source-scope-valid.
            completed = _PARTITION_EVIDENCE.get() or []
            if not hasattr(exc, "_r05_failure_stage"):
                exc._r05_failure_stage = (
                    "after_partition" if completed else "before_partition"
                )
            exc._r05_prior_partitions = tuple(completed)
            raise
        finally:
            _PARTITION_EVIDENCE.reset(token)

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        partition = (kwargs.get("user_payload") or {}).get("analysis_partition") or {}
        index = partition.get("index") if isinstance(partition, dict) else None
        total = partition.get("total") if isinstance(partition, dict) else None
        try:
            result = complete_analysis_partition_with_instructor_v21(**kwargs)
        except Exception as exc:
            exc._r05_failure_stage = "partition_inference"
            if type(index) is int and index > 0:
                exc._r05_partition_index = index
            if type(total) is int and total > 0:
                exc._r05_partition_total = total
            raise
        completed = _PARTITION_EVIDENCE.get()
        if (
            completed is not None
            and type(index) is int
            and type(total) is int
            and 0 < index <= total
        ):
            # This is normalized structured output, NOT the original model bytes,
            # and has not yet passed the parent's partition-scope/global checks.
            completed.append(
                (index, total, json.dumps(result.structured, ensure_ascii=False))
            )
        return result

    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return build_requirement_coverage_plan_v21(model_fields)

    def _responsibility_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, str]:
        return build_responsibility_coverage_plan_v21(model_fields)

    def _requirement_partitions(
        self, plan: dict[str, dict[str, Any]]
    ) -> list[dict[str, dict[str, Any]]]:
        return _v21_requirement_partitions(plan)

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        persisted = persisted_v20_shape(structured)
        return {str(key): value for key, value in persisted.items()}


__all__ = ["V21CandidateAnalysisProvider", "_v21_requirement_partitions"]


def build_v21_analysis_service(settings: Settings) -> JobAnalysisServiceV21:
    """Build the same persisted service for CLI, browser and Market execution."""
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV21(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V21CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )
