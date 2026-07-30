"""LM Studio implementation of the local inference-provider boundary."""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError


class LMStudioProvider:
    """Small synchronous client for LM Studio's OpenAI-compatible API."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str | None = None,
        api_token: str | None = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._base_url = f"{base_url.rstrip('/')}/"
        self._configured_model = configured_model
        self._api_token = api_token
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._transport = transport

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
                    response.raise_for_status()
                    return response
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                if status_code >= 500 and attempt < self._max_retries:
                    time.sleep(min(0.25 * (2**attempt), 1.0))
                    continue
                body = exc.response.text[:500]
                raise InferenceResponseError(
                    f"LM Studio returned HTTP {status_code}: {body}"
                ) from exc
            except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
                last_connection_error = exc
                if attempt < self._max_retries:
                    time.sleep(min(0.25 * (2**attempt), 1.0))
                    continue

        raise InferenceConnectionError(
            f"Could not reach LM Studio at {self._base_url}: {last_connection_error}"
        ) from last_connection_error

    @staticmethod
    def _json_object(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except json.JSONDecodeError as exc:
            raise InferenceResponseError("LM Studio returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise InferenceResponseError("LM Studio response must be a JSON object")
        return payload

    def list_models(self) -> list[str]:
        """List model identifiers visible to LM Studio."""

        payload = self._json_object(self._request("GET", "models"))
        data = payload.get("data")
        if not isinstance(data, list):
            raise InferenceResponseError("LM Studio model response is missing a data list")

        model_ids: list[str] = []
        for item in data:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                model_ids.append(item["id"])
        return model_ids

    def structured_smoke_test(self, model: str | None = None) -> str:
        """Verify a bounded schema-conforming response from one configured model."""

        selected_model = model or self._configured_model
        if not selected_model:
            raise InferenceResponseError(
                "No LM Studio model is configured for structured inference; "
                "set lm_studio_model to an exact identifier returned by /v1/models"
            )

        request_body = {
            "model": selected_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Return only the requested structured health-check result.",
                },
                {
                    "role": "user",
                    "content": "Report that the JobHunter local inference check is okay.",
                },
            ],
            "temperature": 0,
            "max_tokens": 128,
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "jobhunter_health_check",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["ok"]}
                        },
                        "required": ["status"],
                        "additionalProperties": False,
                    },
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
            raise InferenceResponseError(
                "LM Studio chat response is missing choices[0].message.content"
            ) from exc

        if not isinstance(content, str):
            raise InferenceResponseError("LM Studio structured response content is not text")

        finish_reason = first_choice.get("finish_reason")
        try:
            structured = json.loads(content.strip())
        except json.JSONDecodeError as exc:
            preview = content[:240]
            raise InferenceResponseError(
                "LM Studio model did not return valid structured JSON "
                f"(model={selected_model!r}, finish_reason={finish_reason!r}, "
                f"content_preview={preview!r})"
            ) from exc

        if structured != {"status": "ok"}:
            raise InferenceResponseError(
                "Unexpected structured smoke result "
                f"from {selected_model!r} (finish_reason={finish_reason!r}): "
                f"{structured!r}"
            )
        return selected_model
