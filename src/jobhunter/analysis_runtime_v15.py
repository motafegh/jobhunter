"""Runtime wiring for isolated English P1.6 v15 candidate."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v14 import (
    V14CandidateAnalysisProvider,
    _v14_candidate_evidence_view,
)
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import decomposed_requirement_references
from jobhunter.analysis_service_v15 import JobAnalysisServiceV15
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.translation_store import TranslationStore


def _v15_candidate_evidence_view(
    analysis_fields: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str], dict[str, dict[str, Any]]]:
    """Reuse v14 exact subcoverage but keep residual employer strength semantically neutral."""

    effective_fields, qualification_refs, residual_refs, plan = _v14_candidate_evidence_view(
        analysis_fields
    )
    neutral_plan = {reference: dict(candidate) for reference, candidate in plan.items()}
    for reference in residual_refs:
        neutral_plan[reference]["obligation_hint"] = None
    return effective_fields, qualification_refs, residual_refs, neutral_plan


def _mark_v15_runtime(
    result: StructuredInferenceResult,
    *,
    qualification_refs: list[str],
    residual_refs: list[str],
    decomposed_refs: list[str],
) -> StructuredInferenceResult:
    request_body = dict(result.request_body)
    runtime = dict(request_body.get("runtime") or {})
    runtime.update(
        {
            "p16_v15_required_qualification_references": qualification_refs,
            "p16_v15_residual_requirement_references": residual_refs,
            "p16_v15_deterministic_decomposition_references": decomposed_refs,
            "p16_v15_residual_obligation_hints": "source_semantic",
            "p16_v15_concept_type_contract": True,
        }
    )
    request_body["runtime"] = runtime
    return replace(result, request_body=request_body)


class V15CandidateAnalysisProvider(V14CandidateAnalysisProvider):
    """Reuse v14 typed/depth boundary with v15 residual strength semantics."""

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        payload = kwargs.get("user_payload") or {}
        analysis_fields = payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise AnalysisValidationError("P1.6 v15 runtime is missing analysis_fields")

        effective_fields, qualification_refs, residual_refs, additional_plan = (
            _v15_candidate_evidence_view(analysis_fields)
        )
        decomposed_refs = decomposed_requirement_references(analysis_fields)
        try:
            result = self._run_once(
                kwargs=kwargs,
                system_prompt=str(kwargs.get("system_prompt") or ""),
                original_fields=analysis_fields,
                effective_fields=effective_fields,
                qualification_refs=qualification_refs,
                residual_refs=residual_refs,
                additional_plan=additional_plan,
                decomposed_refs=decomposed_refs,
            )
        except AnalysisValidationError as first_error:
            correction_prompt = (
                str(kwargs.get("system_prompt") or "")
                + "\n\nP1.6 V15 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nCorrect only the violated boundary. Preserve exact evidence, mandatory "
                "qualification items, residual coverage decisions, structured required skills, "
                "source-supported requirement strength, and concept-type semantics."
            )
            result = self._run_once(
                kwargs=kwargs,
                system_prompt=correction_prompt,
                original_fields=analysis_fields,
                effective_fields=effective_fields,
                qualification_refs=qualification_refs,
                residual_refs=residual_refs,
                additional_plan=additional_plan,
                decomposed_refs=decomposed_refs,
            )
            request_body = dict(result.request_body)
            runtime = dict(request_body.get("runtime") or {})
            runtime["p16_v15_candidate_recovery"] = True
            runtime["p16_v15_first_error"] = str(first_error)
            request_body["runtime"] = runtime
            result = replace(result, request_body=request_body)

        return _mark_v15_runtime(
            result,
            qualification_refs=qualification_refs,
            residual_refs=residual_refs,
            decomposed_refs=decomposed_refs,
        )


def build_v15_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV15:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisServiceV15(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V15CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = [
    "V15CandidateAnalysisProvider",
    "_v15_candidate_evidence_view",
    "build_v15_candidate_analysis_service",
]
