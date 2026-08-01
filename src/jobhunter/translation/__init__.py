"""Translation providers and English-projection services."""

from jobhunter.translation.base import (
    TranslationBatchResult,
    TranslationError,
    TranslationProvider,
)
from jobhunter.translation.google_cloud import GoogleCloudTranslationProvider

__all__ = [
    "GoogleCloudTranslationProvider",
    "TranslationBatchResult",
    "TranslationError",
    "TranslationProvider",
]
