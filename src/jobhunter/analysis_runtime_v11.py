"""Runtime wiring for the isolated English P1.6 v11 candidate."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import RuntimeManagedAnalysisProvider, _translation_service
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v11 import (
    JobAnalysisServiceV11,
    validate_v11_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.translation_store import TranslationStore


class V11CandidateAnalysisProvider(RuntimeManagedAnalysisProvider):
    """Add one bounded v11 semantic correction above the existing Instructor path."""

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        analysis_fields = (kwargs.get("user_payload") or {}).get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise AnalysisValidationError("P1.6 v11 runtime is missing analysis_fields")

        result = super().complete_structured(**kwargs)
        try:
            validate_v11_candidate_structured(result.structured, analysis_fields)
            return result
        except AnalysisValidationError as first_error:
            correction_kwargs = dict(kwargs)
            correction_kwargs["system_prompt"] = (
                str(kwargs.get("system_prompt") or "")
                + "\n\nP1.6 V11 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nCorrect only the violated semantic boundary. Preserve exact source "
                "evidence, obligation strength, and all already-valid claims."
            )
            corrected = super().complete_structured(**correction_kwargs)
            validate_v11_candidate_structured(corrected.structured, analysis_fields)
            request_body = dict(corrected.request_body)
            runtime_payload = dict(request_body.get("runtime") or {})
            runtime_payload["p16_v11_candidate_recovery"] = True
            runtime_payload["p16_v11_first_error"] = str(first_error)
            request_body["runtime"] = runtime_payload
            return replace(corrected, request_body=request_body)


def build_v11_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV11:
    """Build the isolated v11 candidate without changing production v9 orchestration."""

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisServiceV11(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V11CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V11CandidateAnalysisProvider", "build_v11_candidate_analysis_service"]
