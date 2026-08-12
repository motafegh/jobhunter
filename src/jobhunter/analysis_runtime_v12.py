"""Runtime wiring for the isolated English P1.6 v12 candidate."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import RuntimeManagedAnalysisProvider, _translation_service
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v11 import qualification_list_spans
from jobhunter.analysis_service_v12 import (
    JobAnalysisServiceV12,
    validate_v12_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.translation_store import TranslationStore

_DERIVED_QUALIFICATION_FIELD = "__candidate_qualification_evidence"


def _candidate_evidence_view(
    analysis_fields: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Expose exact qualification spans as normal evidence-reference-addressable values.

    The extra field exists only inside the candidate inference call. Every value is an exact
    excerpt already present in the real description; no new source fact is introduced.
    """

    spans = qualification_list_spans(analysis_fields)
    effective_fields = dict(analysis_fields)
    effective_fields[_DERIVED_QUALIFICATION_FIELD] = spans
    references = [
        f"field:{_DERIVED_QUALIFICATION_FIELD}:{index}"
        for index in range(len(spans))
    ]
    return effective_fields, references


class V12CandidateAnalysisProvider(RuntimeManagedAnalysisProvider):
    """Add first-class evidence IDs plus one bounded v12 semantic correction."""

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        original_payload = kwargs.get("user_payload") or {}
        analysis_fields = original_payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise AnalysisValidationError("P1.6 v12 runtime is missing analysis_fields")

        effective_fields, required_references = _candidate_evidence_view(analysis_fields)
        candidate_payload = dict(original_payload)
        candidate_payload["analysis_fields"] = effective_fields
        candidate_payload["candidate_required_qualification_references"] = required_references
        candidate_kwargs = dict(kwargs)
        candidate_kwargs["user_payload"] = candidate_payload

        result = super().complete_structured(**candidate_kwargs)
        try:
            validate_v12_candidate_structured(result.structured, analysis_fields)
            return result
        except AnalysisValidationError as first_error:
            correction_kwargs = dict(candidate_kwargs)
            correction_kwargs["system_prompt"] = (
                str(candidate_kwargs.get("system_prompt") or "")
                + "\n\nP1.6 V12 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nEvery ID in candidate_required_qualification_references must be cited "
                "by a separate requirement evidence field. Use the supplied evidence-reference "
                "ID exactly. Preserve all already-valid claims and source obligation strength."
            )
            corrected = super().complete_structured(**correction_kwargs)
            validate_v12_candidate_structured(corrected.structured, analysis_fields)
            request_body = dict(corrected.request_body)
            runtime_payload = dict(request_body.get("runtime") or {})
            runtime_payload["p16_v12_candidate_recovery"] = True
            runtime_payload["p16_v12_first_error"] = str(first_error)
            runtime_payload["p16_v12_required_qualification_references"] = required_references
            request_body["runtime"] = runtime_payload
            return replace(corrected, request_body=request_body)


def build_v12_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV12:
    """Build the isolated v12 candidate without changing production v9 orchestration."""

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisServiceV12(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V12CandidateAnalysisProvider(
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
    "V12CandidateAnalysisProvider",
    "_candidate_evidence_view",
    "build_v12_candidate_analysis_service",
]
