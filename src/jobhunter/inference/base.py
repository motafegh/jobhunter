"""Inference-provider contracts and shared errors."""

from __future__ import annotations

from typing import Protocol


class InferenceProviderError(RuntimeError):
    """Base error for local inference-provider failures."""


class InferenceConnectionError(InferenceProviderError):
    """Raised when the provider cannot be reached."""


class InferenceResponseError(InferenceProviderError):
    """Raised when a provider returns an invalid or unsuccessful response."""


class InferenceProvider(Protocol):
    """Minimal provider contract required by the M0 health checks."""

    def list_models(self) -> list[str]:
        """Return model identifiers available from the provider."""

    def structured_smoke_test(self, model: str | None = None) -> str:
        """Return the model used after a bounded structured-output smoke test."""
