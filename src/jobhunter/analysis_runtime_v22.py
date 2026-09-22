"""Runtime wiring for the isolated P1.6 v22 candidate contract."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v21 import V21CandidateAnalysisProvider
from jobhunter.analysis_service_v22 import JobAnalysisServiceV22
from jobhunter.config import Settings
from jobhunter.inference.instructor_lm_studio_v22 import (
    complete_analysis_partition_with_instructor_v22,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V22CandidateAnalysisProvider(V21CandidateAnalysisProvider):
    """Use v22 ontology abstention while retaining the v5 persistable shape."""

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        return complete_analysis_partition_with_instructor_v22(**kwargs)

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        persisted = persisted_v20_shape(structured)
        return {str(key): value for key, value in persisted.items()}


def build_v22_analysis_service(settings: Settings) -> JobAnalysisServiceV22:
    """Build an explicit v22 service without changing public/current routing."""

    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV22(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V22CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V22CandidateAnalysisProvider", "build_v22_analysis_service"]
