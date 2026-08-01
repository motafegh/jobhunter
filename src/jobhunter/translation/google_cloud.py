"""Google Cloud Translation Basic v2 provider."""

from __future__ import annotations

import json
import time
from html import unescape

import httpx

from jobhunter.translation.base import TranslationBatchResult, TranslationError

_GOOGLE_TRANSLATE_V2 = "https://translation.googleapis.com/language/translate/v2"
_MAX_TEXTS_PER_REQUEST = 128


class GoogleCloudTranslationProvider:
    """Translate plain text through the official Google Cloud Basic v2 API."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "nmt",
        endpoint: str = _GOOGLE_TRANSLATE_V2,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
        transport: httpx.BaseTransport | None = None,
        sleep=time.sleep,
    ) -> None:
        cleaned_key = api_key.strip()
        if not cleaned_key:
            raise ValueError("Google Cloud Translation API key must not be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        self._api_key = cleaned_key
        self._model = model.strip() or "nmt"
        self._endpoint = endpoint
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._transport = transport
        self._sleep = sleep

    @property
    def name(self) -> str:
        return "google-cloud-translation-v2"

    @property
    def model(self) -> str:
        return self._model

    def _translate_chunk(
        self,
        texts: tuple[str, ...],
        *,
        source_language: str | None,
        target_language: str,
    ) -> TranslationBatchResult:
        body: dict[str, object] = {
            "q": list(texts),
            "target": target_language,
            "format": "text",
            "model": self._model,
        }
        if source_language:
            body["source"] = source_language

        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                with httpx.Client(
                    timeout=self._timeout_seconds,
                    transport=self._transport,
                ) as client:
                    response = client.post(
                        self._endpoint,
                        headers={
                            "Accept": "application/json",
                            "Content-Type": "application/json; charset=utf-8",
                            "x-goog-api-key": self._api_key,
                        },
                        json=body,
                    )
                if response.status_code in {429, 500, 502, 503, 504}:
                    if attempt < self._max_retries:
                        self._sleep(min(0.5 * (2**attempt), 2.0))
                        continue
                response.raise_for_status()
                try:
                    payload = response.json()
                except json.JSONDecodeError as exc:
                    raise TranslationError(
                        "Google Cloud Translation returned invalid JSON"
                    ) from exc
                try:
                    raw_translations = payload["data"]["translations"]
                except (KeyError, TypeError) as exc:
                    raise TranslationError(
                        "Google Cloud Translation response is missing data.translations"
                    ) from exc
                if not isinstance(raw_translations, list):
                    raise TranslationError(
                        "Google Cloud Translation data.translations must be a list"
                    )
                translated: list[str] = []
                detected: list[str | None] = []
                for item in raw_translations:
                    if not isinstance(item, dict):
                        raise TranslationError(
                            "Google Cloud Translation returned an invalid translation item"
                        )
                    text = item.get("translatedText")
                    if not isinstance(text, str):
                        raise TranslationError(
                            "Google Cloud Translation item is missing translatedText"
                        )
                    translated.append(unescape(text))
                    detected_language = item.get("detectedSourceLanguage")
                    detected.append(
                        detected_language if isinstance(detected_language, str) else None
                    )
                if len(translated) != len(texts):
                    raise TranslationError(
                        "Google Cloud Translation returned a different number of texts"
                    )
                return TranslationBatchResult(
                    texts=tuple(translated),
                    detected_languages=tuple(detected),
                )
            except httpx.HTTPStatusError as exc:
                last_error = exc
                body_preview = exc.response.text[:500]
                raise TranslationError(
                    "Google Cloud Translation returned HTTP "
                    f"{exc.response.status_code}: {body_preview}"
                ) from exc
            except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt < self._max_retries:
                    self._sleep(min(0.5 * (2**attempt), 2.0))
                    continue
                break

        raise TranslationError(
            f"Could not reach Google Cloud Translation: {last_error}"
        ) from last_error

    def translate_texts(
        self,
        texts: tuple[str, ...],
        *,
        source_language: str | None,
        target_language: str,
    ) -> TranslationBatchResult:
        """Translate an arbitrary batch using API-sized chunks of at most 128 texts."""

        if not texts:
            return TranslationBatchResult(texts=(), detected_languages=())
        if not target_language.strip():
            raise ValueError("target_language must not be empty")

        translated: list[str] = []
        detected: list[str | None] = []
        for start in range(0, len(texts), _MAX_TEXTS_PER_REQUEST):
            chunk = texts[start : start + _MAX_TEXTS_PER_REQUEST]
            result = self._translate_chunk(
                chunk,
                source_language=source_language,
                target_language=target_language,
            )
            translated.extend(result.texts)
            detected.extend(result.detected_languages)
        return TranslationBatchResult(
            texts=tuple(translated),
            detected_languages=tuple(detected),
        )
