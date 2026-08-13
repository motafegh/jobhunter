"""Runtime wiring for isolated English P1.6 v14 candidate."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v12 import _candidate_evidence_view
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import (
    decomposed_requirement_references,
    inject_decomposition_exclusions,
)
from jobhunter.analysis_service_v14 import (
    JobAnalysisServiceV14,
    residual_requirement_spans,
    validate_v14_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.instructor_lm_studio_v13 import complete_analysis_with_instructor_v13
from jobhunter.inference.instructor_lm_studio_v14 import JobAnalysisResponseV14
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation_store import TranslationStore

_ANALYSIS_CONTEXT_LENGTH = 16_384
_RESIDUAL_FIELD = "__candidate_residual_requirement_evidence"


def _v14_candidate_evidence_view(
    analysis_fields: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str], dict[str, dict[str, Any]]]:
    """Expose exact qualification and residual evidence with explicit coverage semantics."""

    effective_fields, qualification_refs = _candidate_evidence_view(analysis_fields)
    residuals = residual_requirement_spans(analysis_fields)
    effective_fields[_RESIDUAL_FIELD] = residuals
    residual_refs = [f"field:{_RESIDUAL_FIELD}:{index}" for index in range(len(residuals))]

    additional_plan: dict[str, dict[str, Any]] = {}
    qualification_values = effective_fields["__candidate_qualification_evidence"]
    for reference in qualification_refs:
        index = int(reference.rsplit(":", 1)[1])
        additional_plan[reference] = {
            "text": qualification_values[index],
            "source_kind": "candidate_qualification_item",
            "obligation_hint": "required",
            "allow_exclusion": False,
        }
    for reference in residual_refs:
        index = int(reference.rsplit(":", 1)[1])
        additional_plan[reference] = {
            "text": residuals[index],
            "source_kind": "candidate_residual_sentence",
            "obligation_hint": "required",
            "allow_exclusion": True,
        }
    return effective_fields, qualification_refs, residual_refs, additional_plan


class V14CandidateAnalysisProvider:
    """Run complete candidate subcoverage with one bounded semantic correction."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str,
        api_token: str | None,
        timeout_seconds: float,
        max_retries: int,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._configured_model = configured_model
        self._api_token = api_token
        self._timeout_seconds = float(timeout_seconds)
        self._max_retries = int(max_retries)

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

        result = complete_analysis_with_instructor_v13(
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
            response_model=JobAnalysisResponseV14,
        )
        structured = inject_decomposition_exclusions(result.structured, original_fields)
        validate_v14_candidate_structured(structured, original_fields)
        request_body = dict(result.request_body)
        runtime_payload = dict(request_body.get("runtime") or {})
        runtime_payload.update(
            {
                "context_length_tokens": runtime.context_length,
                "context_action": runtime.action,
                "model_instance_id": runtime.instance_id,
                "exclusive_llm": True,
                "p16_v14_required_qualification_references": qualification_refs,
                "p16_v14_residual_requirement_references": residual_refs,
                "p16_v14_deterministic_decomposition_references": decomposed_refs,
                "p16_v14_schedule_depth_normalization": True,
            }
        )
        request_body["runtime"] = runtime_payload
        return replace(result, structured=structured, request_body=request_body)

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        payload = kwargs.get("user_payload") or {}
        analysis_fields = payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise AnalysisValidationError("P1.6 v14 runtime is missing analysis_fields")

        effective_fields, qualification_refs, residual_refs, additional_plan = (
            _v14_candidate_evidence_view(analysis_fields)
        )
        decomposed_refs = decomposed_requirement_references(analysis_fields)
        try:
            return self._run_once(
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
                + "\n\nP1.6 V14 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nCorrect only the violated boundary. Preserve all exact evidence, mandatory "
                "qualification items, residual coverage decisions, and structured required skills."
            )
            corrected = self._run_once(
                kwargs=kwargs,
                system_prompt=correction_prompt,
                original_fields=analysis_fields,
                effective_fields=effective_fields,
                qualification_refs=qualification_refs,
                residual_refs=residual_refs,
                additional_plan=additional_plan,
                decomposed_refs=decomposed_refs,
            )
            request_body = dict(corrected.request_body)
            runtime_payload = dict(request_body.get("runtime") or {})
            runtime_payload["p16_v14_candidate_recovery"] = True
            runtime_payload["p16_v14_first_error"] = str(first_error)
            request_body["runtime"] = runtime_payload
            return replace(corrected, request_body=request_body)


def build_v14_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV14:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisServiceV14(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V14CandidateAnalysisProvider(
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
    "V14CandidateAnalysisProvider",
    "_v14_candidate_evidence_view",
    "build_v14_candidate_analysis_service",
]
