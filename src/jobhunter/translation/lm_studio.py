"""LM Studio translation provider using structured local inference."""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

from jobhunter.translation.base import TranslationBatchResult, TranslationError

_PROVIDER_NAME = "lm-studio-translation-v1"
_MAX_TEXTS_PER_REQUEST = 32
_DEFAULT_CHARACTER_TARGET = 6_000
_DEFAULT_MAX_TOKENS = 4_096

_SYSTEM_PROMPT = """You are JobHunter's translation engine.
Translate each supplied Persian or mixed Persian-English job-ad segment into precise,
natural English.

Rules:
- Preserve meaning, factual strength, modality, uncertainty, negation, numbers, dates,
  names, product names, acronyms, and technical terminology.
- Do not strengthen weak requirements. For example, familiarity must not become
  proficiency, and preferred must not become required.
- Preserve standard English technical tokens such as Python, Docker, Kubernetes,
  RAG, LLM, NLP, MLOps, SIEM, SOC, GitHub, TensorFlow, and PyTorch when they already
  appear naturally in the source.
- Translate the complete supplied text. Do not summarize, omit, explain, classify,
  infer, or add information.
- Return exactly one translation for every input id and no extra ids.
"""


class LMStudioTranslationProvider:
    """Translate source segments through LM Studio's OpenAI-compatible local API."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str | None = None,
        api_token: str | None = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
        max_tokens: int = _DEFAULT_MAX_TOKENS,
        request_character_target: int = _DEFAULT_CHARACTER_TARGET,
        transport: httpx.BaseTransport | None = None,
        sleep=time.sleep,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        if not 256 <= max_tokens <= 32_768:
            raise ValueError("max_tokens must be between 256 and 32768")
        if not 1_000 <= request_character_target <= 100_000:
            raise ValueError(
                "request_character_target must be between 1000 and 100000"
            )

        self._base_url = f"{base_url.rstrip('/')}/"
        self._configured_model = configured_model.strip() if configured_model else None
        self._api_token = api_token.strip() if api_token else None
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._max_tokens = max_tokens
        self._request_character_target = request_character_target
        self._transport = transport
        self._sleep = sleep
        self._resolved_model: str | None = None

    @property
    def name(self) -> str:
        """Stable provider-and-prompt contract identifier."""

        return _PROVIDER_NAME

    @property
    def model(self) -> str:
        """Resolve and return the exact LM Studio model identifier."""

        return self._resolve_model()

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = {"Accept": "application/json"}
        if self._api_token:
            headers["Authorization"] = f"Bearer {self._api_token}"

        last_connection_error: httpx.HTTPError | None = None
        for attempt in range(self._max_retries + 1):
            try:
                with httpx.Client(
                    base_url=self._base_url,
                    headers=headers,
                    timeout=self._timeout_seconds,
                    transport=self._transport,
                ) as client:
                    response = client.request(method, path, **kwargs)
                if response.status_code >= 500 and attempt < self._max_retries:
                    self._sleep(min(0.25 * (2**attempt), 1.0))
                    continue
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                body = exc.response.text[:500]
                raise TranslationError(
                    f"LM Studio returned HTTP {exc.response.status_code}: {body}"
                ) from exc
            except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
                last_connection_error = exc
                if attempt < self._max_retries:
                    self._sleep(min(0.25 * (2**attempt), 1.0))
                    continue

        raise TranslationError(
            f"Could not reach LM Studio at {self._base_url}: {last_connection_error}"
        ) from last_connection_error

    @staticmethod
    def _json_object(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except json.JSONDecodeError as exc:
            raise TranslationError("LM Studio returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise TranslationError("LM Studio response must be a JSON object")
        return payload

    def list_models(self) -> tuple[str, ...]:
        """Return exact model identifiers visible through LM Studio."""

        payload = self._json_object(self._request("GET", "models"))
        data = payload.get("data")
        if not isinstance(data, list):
            raise TranslationError("LM Studio model response is missing a data list")
        return tuple(
            item["id"]
            for item in data
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        )

    def _resolve_model(self) -> str:
        if self._resolved_model is not None:
            return self._resolved_model
        if self._configured_model:
            self._resolved_model = self._configured_model
            return self._resolved_model

        models = self.list_models()
        if len(models) == 1:
            self._resolved_model = models[0]
            return self._resolved_model
        if not models:
            raise TranslationError(
                "LM Studio is reachable but no models are visible. Load a model or set "
                "translation_lm_studio_model."
            )
        preview = ", ".join(models[:8])
        suffix = " ..." if len(models) > 8 else ""
        raise TranslationError(
            "LM Studio exposes multiple models, so JobHunter will not choose one "
            "implicitly. Set translation_lm_studio_model to one exact identifier. "
            f"Visible models: {preview}{suffix}"
        )

    def _request_chunks(self, texts: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        chunks: list[tuple[str, ...]] = []
        current: list[str] = []
        current_characters = 0
        for text in texts:
            would_exceed_count = len(current) >= _MAX_TEXTS_PER_REQUEST
            would_exceed_target = (
                bool(current)
                and current_characters + len(text) > self._request_character_target
            )
            if would_exceed_count or would_exceed_target:
                chunks.append(tuple(current))
                current = []
                current_characters = 0
            current.append(text)
            current_characters += len(text)
        if current:
            chunks.append(tuple(current))
        return tuple(chunks)

    def _translate_chunk(
        self,
        texts: tuple[str, ...],
        *,
        source_language: str | None,
        target_language: str,
    ) -> TranslationBatchResult:
        model = self._resolve_model()
        input_items = [
            {"id": index, "text": text}
            for index, text in enumerate(texts)
        ]
        schema = {
            "type": "object",
            "properties": {
                "translations": {
                    "type": "array",
                    "minItems": len(texts),
                    "maxItems": len(texts),
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "translation": {"type": "string"},
                        },
                        "required": ["id", "translation"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["translations"],
            "additionalProperties": False,
        }
        request_body = {
            "model": model,
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "source_language": source_language or "auto",
                            "target_language": target_language,
                            "items": input_items,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            "temperature": 0,
            "seed": 0,
            "max_tokens": self._max_tokens,
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "jobhunter_translation_batch",
                    "strict": True,
                    "schema": schema,
                },
            },
        }

        payload = self._json_object(
            self._request("POST", "chat/completions", json=request_body)
        )
        try:
            first_choice = payload["choices"][0]
            content = first_choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise TranslationError(
                "LM Studio translation response is missing choices[0].message.content"
            ) from exc
        if not isinstance(content, str):
            raise TranslationError("LM Studio translation response content is not text")

        finish_reason = first_choice.get("finish_reason")
        try:
            structured = json.loads(content.strip())
        except json.JSONDecodeError as exc:
            raise TranslationError(
                "LM Studio did not return valid structured translation JSON "
                f"(model={model!r}, finish_reason={finish_reason!r})"
            ) from exc
        raw_translations = (
            structured.get("translations") if isinstance(structured, dict) else None
        )
        if not isinstance(raw_translations, list) or len(raw_translations) != len(texts):
            raise TranslationError(
                "LM Studio returned a translation count that does not match the input"
            )

        by_id: dict[int, str] = {}
        for item in raw_translations:
            if not isinstance(item, dict):
                raise TranslationError("LM Studio returned an invalid translation item")
            item_id = item.get("id")
            translation = item.get("translation")
            if not isinstance(item_id, int) or not isinstance(translation, str):
                raise TranslationError("LM Studio translation item has invalid fields")
            cleaned = translation.strip()
            if not cleaned:
                raise TranslationError("LM Studio returned an empty translation")
            if item_id in by_id:
                raise TranslationError("LM Studio returned a duplicate translation id")
            by_id[item_id] = cleaned

        expected_ids = set(range(len(texts)))
        if set(by_id) != expected_ids:
            raise TranslationError(
                "LM Studio returned missing or unexpected translation ids"
            )
        ordered = tuple(by_id[index] for index in range(len(texts)))
        detected = tuple(source_language for _ in texts)
        return TranslationBatchResult(texts=ordered, detected_languages=detected)

    def translate_texts(
        self,
        texts: tuple[str, ...],
        *,
        source_language: str | None,
        target_language: str,
    ) -> TranslationBatchResult:
        """Translate an ordered batch locally while preserving exact item count/order."""

        if not texts:
            return TranslationBatchResult(texts=(), detected_languages=())
        if target_language != "en":
            raise ValueError("LM Studio translation currently supports target_language='en'")

        translated: list[str] = []
        detected: list[str | None] = []
        for chunk in self._request_chunks(texts):
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
