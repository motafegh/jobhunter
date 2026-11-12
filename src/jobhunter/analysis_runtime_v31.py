"""Isolated, non-promoted P1.6 v31 candidate over exact source sections."""
from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v23 import _filter_unassigned_partition_claims
from jobhunter.analysis_runtime_v30 import V30CandidateAnalysisProvider
from jobhunter.analysis_service_v31 import JobAnalysisServiceV31
from jobhunter.config import Settings
from jobhunter.evidence_refs_v31 import (
    v31_requirement_plan,
    v31_responsibility_plan,
    v31_scoped_additional_plan,
)
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.instructor_lm_studio_v31 import JobAnalysisResponseV31
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.source_obligation_conflicts import structured_skill_preference_conflicts


class V31CandidateAnalysisProvider(V30CandidateAnalysisProvider):
    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        inherited = super()._requirement_coverage_plan(model_fields)
        return v31_requirement_plan(model_fields, inherited)

    def _responsibility_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, str]:
        inherited = super()._responsibility_coverage_plan(model_fields)
        return v31_responsibility_plan(model_fields, inherited)

    def _run_once(self, **kwargs: Any) -> StructuredInferenceResult:
        updated = dict(kwargs)
        updated["additional_plan"] = v31_scoped_additional_plan(
            kwargs["original_fields"], kwargs["additional_plan"]
        )
        result = super()._run_once(**updated)
        conflicts = structured_skill_preference_conflicts(kwargs["original_fields"])
        if not conflicts:
            return result
        # Runtime metadata is review-only. It neither rewrites structured
        # requirements nor silently declares either source authoritative.
        request_body = dict(result.request_body)
        runtime = dict(request_body.get("runtime") or {})
        runtime["p16_v31_structured_skill_obligation_conflicts"] = [
            {
                "skill": conflict.skill,
                "source_section_start": conflict.source_section_start,
                "source_section_end": conflict.source_section_end,
                "reason": conflict.reason,
            }
            for conflict in conflicts
        ]
        request_body["runtime"] = runtime
        return StructuredInferenceResult(
            model=result.model,
            structured=result.structured,
            request_body=request_body,
            raw_response=result.raw_response,
            finish_reason=result.finish_reason,
        )

    def _source_context_exclusions(
        self, plan: dict[str, dict[str, Any]]
    ) -> tuple[list[str], list[dict[str, str]]]:
        references, exclusions = super()._source_context_exclusions(plan)
        for ref, candidate in plan.items():
            if (
                ref not in references
                and candidate.get("source_kind") == "v31_nonqualification_context"
                and candidate.get("allow_exclusion", False)
            ):
                references.append(ref)
                exclusions.append({
                    "evidence_reference": ref,
                    "rationale": ("Source is application or employment context, "
                                  "not an applicant qualification."),
                })
        return references, exclusions

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        refs = list(kwargs["requirement_coverage_plan"])
        refs.extend(kwargs["responsibility_coverage_plan"])
        result = complete_analysis_partition_with_instructor_v24(
            **kwargs,
            contract_version="v31",
            model_evidence_references=refs,
            response_model=JobAnalysisResponseV31,
        )
        return _filter_unassigned_partition_claims(
            result,
            requirement_plan=kwargs["requirement_coverage_plan"],
            responsibility_plan=kwargs["responsibility_coverage_plan"],
        )


def build_v31_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV31:
    """Use only on a separate evaluation database; do not modify main routing."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV31(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V31CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V31CandidateAnalysisProvider", "build_v31_candidate_analysis_service"]
