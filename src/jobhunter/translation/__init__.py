"""Translation providers and English-projection services."""

from jobhunter.translation.base import (
    TranslationBatchResult,
    TranslationError,
    TranslationProvider,
)
from jobhunter.translation.google_cloud import GoogleCloudTranslationProvider
from jobhunter.translation.lm_studio import LMStudioTranslationProvider

__all__ = [
    "GoogleCloudTranslationProvider",
    "LMStudioTranslationProvider",
    "TranslationBatchResult",
    "TranslationError",
    "TranslationProvider",
]
