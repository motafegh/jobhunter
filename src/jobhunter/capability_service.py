"""Current Capability Intelligence service entrypoint.

Capability v7 remains the accepted reasoning contract. The public-current service binds it to the
promoted English P1.6 v20/v5 dependency while preserving the historical v7 implementation module
for reproducibility.
"""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.capability_inference import CapabilityInferenceProvider
from jobhunter.capability_service_v7 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
    CapabilityIntelligenceService as CapabilityIntelligenceServiceV7,
    format_capability_intelligence,
)
from jobhunter.capability_store import (
    CapabilityIntelligenceStore,
    CapabilityTranslationDependency,
)
from jobhunter.config import Settings
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


class CapabilityIntelligenceService(CapabilityIntelligenceServiceV7):
    """Capability v7 bound to the current accepted English P1.6 contract."""

    def _current_dependencies(
        self,
        source_job_id: str,
    ) -> tuple[Any, CapabilityTranslationDependency, AnalysisArtifact]:
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise CapabilityIntelligenceError(
                "Job has no current successfully parsed source version"
            )
        analysis = self._analysis_store.latest_current(
            source_job_id,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        )
        if analysis is None:
            raise CapabilityIntelligenceError(
                "Job has no current accepted English P1.6 analysis; run Analyze English first"
            )
        if analysis.job_detail_version_id != source.job_detail_version_id:
            raise CapabilityIntelligenceError(
                "English analysis does not belong to the current source semantic version"
            )
        if analysis.translation_artifact_id is None:
            raise CapabilityIntelligenceError(
                "English analysis has no referenced hardened English projection"
            )

        translation = self._capability_store.translation_dependency(
            analysis.translation_artifact_id
        )
        if translation is None:
            raise CapabilityIntelligenceError(
                "English analysis references a missing English projection artifact"
            )
        if translation.source_job_id != source_job_id:
            raise CapabilityIntelligenceError(
                "English analysis references a translation artifact from another job"
            )
        if translation.job_detail_version_id != source.job_detail_version_id:
            raise CapabilityIntelligenceError(
                "English analysis references an English projection from an older source version"
            )
        if translation.target_language != "en":
            raise CapabilityIntelligenceError(
                "English analysis references a non-English translation artifact"
            )
        if translation.translation_schema_version != TRANSLATION_SCHEMA_VERSION:
            raise CapabilityIntelligenceError(
                "English analysis references a historical English projection and requires v2 repair"
            )
        return source, translation, analysis


def build_capability_intelligence_service(settings: Settings) -> CapabilityIntelligenceService:
    """Build current Capability v7 above promoted English P1.6 v20/v5."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for the accepted English extraction")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    translation_store = TranslationStore(settings.database_path)
    return CapabilityIntelligenceService(
        source_store=translation_store,
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        provider=CapabilityInferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=capability_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceError",
    "CapabilityIntelligenceResult",
    "CapabilityIntelligenceService",
    "build_capability_intelligence_service",
    "format_capability_intelligence",
]
