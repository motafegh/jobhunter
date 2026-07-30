"""Local inference-provider integrations."""

from jobhunter.inference.base import (
    InferenceConnectionError,
    InferenceProvider,
    InferenceProviderError,
    InferenceResponseError,
)
from jobhunter.inference.lm_studio import LMStudioProvider

__all__ = [
    "InferenceConnectionError",
    "InferenceProvider",
    "InferenceProviderError",
    "InferenceResponseError",
    "LMStudioProvider",
]
