"""Build the per-job semantic-analysis dependency graph without acquisition orchestration."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_service import JobAnalysisService
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference import LMStudioProvider
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation import GoogleCloudTranslationProvider, LMStudioTranslationProvider
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_ANALYSIS_CONTEXT_LENGTH = 16_384


class RuntimeManagedAnalysisProvider(LMStudioProvider):
    """Run P1.6 only after JobHunter establishes deterministic LM Studio runtime state."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str,
        api_token: str | None,
        timeout_seconds: float,
        max_retries: int,
    ) -> None:
        super().__init__(
            base_url=base_url,
            configured_model=configured_model,
            api_token=api_token,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )
        self._runtime_base_url = base_url.rstrip("/")
        self._runtime_model = configured_model
        self._runtime_api_token = api_token
        self._runtime_connect_timeout = min(float(timeout_seconds), 10.0)

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        selected_model = str(kwargs.get("model") or self._runtime_model).strip()
        runtime = ensure_lm_studio_model_context(
            openai_base_url=self._runtime_base_url,
            model=selected_model,
            context_length=_ANALYSIS_CONTEXT_LENGTH,
            api_token=self._runtime_api_token,
            connect_timeout_seconds=self._runtime_connect_timeout,
            exclusive_llm=True,
        )
        result = super().complete_structured(**kwargs)
        request_body = dict(result.request_body)
        runtime_payload = dict(request_body.get("runtime") or {})
        runtime_payload.update(
            {
                "context_length_tokens": runtime.context_length,
                "context_action": runtime.action,
                "model_instance_id": runtime.instance_id,
                "exclusive_llm": True,
            }
        )
        request_body["runtime"] = runtime_payload
        return replace(result, request_body=request_body)


def _translation_service(settings: Settings) -> TranslationService:
    """Build the translation-store view needed by English P1.6 analysis.

    The provider is configured consistently with the existing Phase-1/browser paths, but a
    targeted analysis command only reads an already-current English projection; it does not
    create or repair translations implicitly.
    """

    provider = None
    if (
        settings.translation_enabled
        and settings.translation_provider == "google-cloud"
        and not settings.google_translation_api_key
    ):
        raise ValueError(
            "Google translation is enabled but "
            "JOBHUNTER_GOOGLE_TRANSLATION_API_KEY is not configured"
        )
    if settings.translation_enabled and settings.translation_provider == "lm-studio":
        provider = LMStudioTranslationProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.effective_translation_lm_studio_model(),
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
            max_tokens=settings.translation_lm_studio_max_tokens,
            request_character_target=settings.translation_lm_studio_character_target,
        )
    elif settings.translation_enabled and settings.translation_provider == "google-cloud":
        provider = GoogleCloudTranslationProvider(
            api_key=settings.google_translation_api_key or "",
            model=settings.google_translation_model,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
        )
    return TranslationService(
        store=TranslationStore(settings.database_path),
        provider=provider,
        target_language=settings.translation_target_language,
    )


def build_job_analysis_service(settings: Settings) -> JobAnalysisService:
    """Build P1.6 analysis for explicit jobs without discovery/sync/batch side effects."""

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisService(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=RuntimeManagedAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )
