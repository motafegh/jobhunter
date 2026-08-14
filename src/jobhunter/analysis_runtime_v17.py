"""Runtime wiring for isolated English P1.6 v17 source-led requirement capacity."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v14 import (
    _ANALYSIS_CONTEXT_LENGTH,
    _V14_TYPED_MODEL_LOCK,
)
from jobhunter.analysis_runtime_v15 import _normalize_v15_schedule_concepts
from jobhunter.analysis_runtime_v16 import V16CandidateAnalysisProvider
from jobhunter.analysis_service_v13 import (
    decomposed_requirement_references,
    inject_decomposition_exclusions,
)
from jobhunter.analysis_service_v15 import validate_v15_candidate_structured
from jobhunter.analysis_service_v17 import JobAnalysisServiceV17
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference import instructor_lm_studio_v13 as instructor_v13
from jobhunter.inference.instructor_lm_studio_v17 import JobAnalysisResponseV17
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation_store import TranslationStore


def _complete_with_v17_response_model(**kwargs: Any) -> StructuredInferenceResult:
    """Run the historical candidate helper with the v17 source-led typed response model."""

    with _V14_TYPED_MODEL_LOCK:
        original_model = instructor_v13.JobAnalysisResponse
        instructor_v13.JobAnalysisResponse = JobAnalysisResponseV17
        try:
            return instructor_v13.complete_analysis_with_instructor_v13(**kwargs)
        finally:
            instructor_v13.JobAnalysisResponse = original_model


class V17CandidateAnalysisProvider(V16CandidateAnalysisProvider):
    """Preserve v16 semantics while removing only the inherited 32-requirement ceiling."""

    def _run_once(
        self,
        *,
        kwargs: dict[str, Any],
        system_prompt: str,
        original_fields: dict[str, Any],
        effective_fields: dict[str, Any],
        qualification_refs: list[str],
        residual_refs: list[str],
        additional_plan: dict[str, dict[str, Any]],
        decomposed_refs: list[str],
    ) -> StructuredInferenceResult:
        selected_model = str(kwargs.get("model") or self._configured_model).strip()
        runtime = ensure_lm_studio_model_context(
            openai_base_url=self._base_url,
            model=selected_model,
            context_length=_ANALYSIS_CONTEXT_LENGTH,
            api_token=self._api_token,
            connect_timeout_seconds=min(self._timeout_seconds, 10.0),
            exclusive_llm=True,
        )
        payload = dict(kwargs.get("user_payload") or {})
        payload["analysis_fields"] = effective_fields
        payload["candidate_required_qualification_references"] = qualification_refs
        payload["candidate_residual_requirement_references"] = residual_refs

        result = _complete_with_v17_response_model(
            base_url=f"{self._base_url}/",
            api_token=self._api_token,
            timeout_seconds=self._timeout_seconds,
            network_retries=self._max_retries,
            selected_model=selected_model,
            system_prompt=system_prompt,
            user_payload=payload,
            schema=kwargs["schema"],
            max_tokens=int(kwargs.get("max_tokens") or 8192),
            seed=int(kwargs.get("seed") or 0),
            suppressed_requirement_coverage_references=decomposed_refs,
            additional_requirement_coverage_plan=additional_plan,
            validation_retries=1,
        )
        structured, normalized_indexes = _normalize_v15_schedule_concepts(result.structured)
        structured = inject_decomposition_exclusions(structured, original_fields)
        validate_v15_candidate_structured(structured, original_fields)

        request_body = dict(result.request_body)
        runtime_payload = dict(request_body.get("runtime") or {})
        runtime_payload.update(
            {
                "context_length_tokens": runtime.context_length,
                "context_action": runtime.action,
                "model_instance_id": runtime.instance_id,
                "exclusive_llm": True,
                "p16_v17_source_led_requirement_capacity": True,
                "p16_v17_removed_legacy_requirement_cap": 32,
                "p16_v15_schedule_depth_normalization": True,
                "p16_v15_schedule_concept_normalization": normalized_indexes,
            }
        )
        request_body["runtime"] = runtime_payload
        return replace(result, structured=structured, request_body=request_body)


def build_v17_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV17:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV17(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V17CandidateAnalysisProvider(
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
    "V17CandidateAnalysisProvider",
    "_complete_with_v17_response_model",
    "build_v17_candidate_analysis_service",
]
