"""Provider-neutral translation boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class TranslationError(RuntimeError):
    """Raised when a translation provider cannot return a valid translation."""


@dataclass(frozen=True, slots=True)
class TranslationBatchResult:
    """One ordered batch returned by a translation provider."""

    texts: tuple[str, ...]
    detected_languages: tuple[str | None, ...]


class TranslationProvider(Protocol):
    """Minimal provider interface used by the English-projection pipeline."""

    @property
    def name(self) -> str:
        """Stable provider identifier."""

    @property
    def model(self) -> str:
        """Stable model identifier recorded with translation artifacts."""

    def translate_texts(
        self,
        texts: tuple[str, ...],
        *,
        source_language: str | None,
        target_language: str,
    ) -> TranslationBatchResult:
        """Translate texts while preserving input ordering."""
