"""Current public Capability Intelligence service entrypoint.

Capability v9/v5 is the accepted public reasoning contract. The neutral facade keeps CLI,
browser, Review Snapshot, and other current consumers aligned while historical v7/v8/v9 modules
remain available for reproducibility.
"""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference_v8 import CapabilityV8InferenceProvider
from jobhunter.capability_service_v9 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
    CapabilityIntelligenceServiceV9,
    format_capability_v9,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.translation_store import TranslationStore


class CapabilityIntelligenceService(CapabilityIntelligenceServiceV9):
    """Current public Capability v9 service above accepted English P1.6 v20/v5."""

    def _current_dependencies(self, source_job_id: str) -> tuple[Any, Any, Any]:
        """Expose the established current-dependency boundary for compatibility and review tests."""

        return self._delegate._current_dependencies(source_job_id)


def build_capability_intelligence_service(settings: Settings) -> CapabilityIntelligenceService:
    """Build the accepted public Capability v9 service."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for the accepted English extraction")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")

    return CapabilityIntelligenceService(
        source_store=TranslationStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        provider=CapabilityV8InferenceProvider(
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


format_capability_intelligence = format_capability_v9


__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceError",
    "CapabilityIntelligenceResult",
    "CapabilityIntelligenceService",
    "build_capability_intelligence_service",
    "format_capability_intelligence",
]
