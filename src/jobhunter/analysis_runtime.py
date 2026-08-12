"""Build the per-job semantic-analysis dependency graph without acquisition orchestration."""

from __future__ import annotations

from jobhunter.analysis_service import JobAnalysisService
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference import LMStudioProvider
from jobhunter.translation import GoogleCloudTranslationProvider, LMStudioTranslationProvider
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


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
        provider=LMStudioProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )
