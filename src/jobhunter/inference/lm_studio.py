"""LM Studio implementation of the local inference-provider boundary."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

import httpx
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from jobhunter.inference.base import (
    InferenceConnectionError,
    InferenceResponseError,
    InferenceTruncatedError,
)

_MAX_STRUCTURED_TOKENS = 32_768


@dataclass(frozen=True, slots=True)
class StructuredInferenceResult:
    """Validated JSON result plus raw provider evidence."""

    model: str
    structured: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    finish_reason: str | None


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
                    trust_env=False,
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

    @staticmethod
    def _validate_structured_result(
        structured: dict[str, Any],
        schema: dict[str, Any],
    ) -> None:
        """Verify provider output locally instead of trusting response-format claims."""

        try:
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(structured)
        except SchemaError as exc:
            raise InferenceResponseError(
                f"JobHunter supplied an invalid structured-output schema: {exc.message}"
            ) from exc
        except ValidationError as exc:
            path = ".".join(str(item) for item in exc.absolute_path) or "<root>"
            raise InferenceResponseError(
                "LM Studio structured response violated the requested JSON schema "
                f"at {path}: {exc.message}"
            ) from exc

    def list_models(self) -> list[str]:
        payload = self._json_object(self._request("GET", "models"))
        data = payload.get("data")
        if not isinstance(data, list):
            raise InferenceResponseError("LM Studio model response is missing a data list")
        return [
            item["id"]
            for item in data
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]

    def _selected_model(self, model: str | None = None) -> str:
        selected_model = model or self._configured_model
        if not selected_model:
            raise InferenceResponseError(
                "No LM Studio model is configured for structured inference; "
                "set a dedicated analysis model or lm_studio_model"
            )
        return selected_model

    def _complete_structured_once(
        self,
        *,
        selected_model: str,
        system_prompt: str,
        user_payload: dict[str, Any],
        schema_name: str,
        schema: dict[str, Any],
        max_tokens: int,
        seed: int,
    ) -> StructuredInferenceResult:
        request_body = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=False, sort_keys=True),
                },
            ],
            "temperature": 0,
            "seed": seed,
            "max_tokens": max_tokens,
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
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
            raise InferenceResponseError(
                "LM Studio chat response is missing choices[0].message.content"
            ) from exc
        if not isinstance(content, str):
            raise InferenceResponseError("LM Studio structured response content is not text")
        finish_reason = first_choice.get("finish_reason")
        if finish_reason == "length":
            preview = content[:240]
            raise InferenceTruncatedError(
                "LM Studio structured response was truncated "
                f"(model={selected_model!r}, finish_reason={finish_reason!r}, "
                f"content_preview={preview!r}, max_tokens={max_tokens})"
            )
        try:
            structured = json.loads(content.strip())
        except json.JSONDecodeError as exc:
            preview = content[:240]
            raise InferenceResponseError(
                "LM Studio model did not return valid structured JSON "
                f"(model={selected_model!r}, finish_reason={finish_reason!r}, "
                f"content_preview={preview!r})"
            ) from exc
        if not isinstance(structured, dict):
            raise InferenceResponseError("Structured LM Studio content must be a JSON object")
        self._validate_structured_result(structured, schema)
        return StructuredInferenceResult(
            model=selected_model,
            structured=structured,
            request_body=request_body,
            raw_response=payload,
            finish_reason=str(finish_reason) if finish_reason is not None else None,
        )

    def complete_structured(
        self,
        *,
        system_prompt: str,
        user_payload: dict[str, Any],
        schema_name: str,
        schema: dict[str, Any],
        model: str | None = None,
        max_tokens: int = 8192,
        max_recovery_tokens: int | None = None,
        seed: int = 0,
    ) -> StructuredInferenceResult:
        """Run structured inference; analysis adds Instructor/Pydantic validation."""

        if not 1 <= max_tokens <= _MAX_STRUCTURED_TOKENS:
            raise ValueError("max_tokens must be between 1 and 32768")
        recovery_ceiling = (
            _MAX_STRUCTURED_TOKENS
            if max_recovery_tokens is None
            else max_recovery_tokens
        )
        if not max_tokens <= recovery_ceiling <= _MAX_STRUCTURED_TOKENS:
            raise ValueError(
                "max_recovery_tokens must be between max_tokens and 32768"
            )

        selected_model = self._selected_model(model)

        if schema_name.startswith("jobhunter_job_analysis_"):
            from jobhunter.inference.instructor_lm_studio import (
                complete_analysis_with_instructor,
            )

            result = complete_analysis_with_instructor(
                base_url=self._base_url,
                api_token=self._api_token,
                timeout_seconds=self._timeout_seconds,
                network_retries=self._max_retries,
                transport=self._transport,
                selected_model=selected_model,
                system_prompt=system_prompt,
                user_payload=user_payload,
                schema=schema,
                max_tokens=max_tokens,
                seed=seed,
                validation_retries=1,
            )
            self._validate_structured_result(result.structured, schema)
            return result

        current_max_tokens = max_tokens
        while True:
            try:
                return self._complete_structured_once(
                    selected_model=selected_model,
                    system_prompt=system_prompt,
                    user_payload=user_payload,
                    schema_name=schema_name,
                    schema=schema,
                    max_tokens=current_max_tokens,
                    seed=seed,
                )
            except InferenceTruncatedError:
                if current_max_tokens >= recovery_ceiling:
                    raise
                current_max_tokens = min(current_max_tokens * 4, recovery_ceiling)

    def structured_smoke_test(self, model: str | None = None) -> str:
        """Prove schema-conforming local inference with bounded truncation recovery."""

        selected_model = self._selected_model(model)
        result = self.complete_structured(
            system_prompt="Return only the requested structured health-check result.",
            user_payload={
                "instruction": "Report that the JobHunter local inference check is okay."
            },
            schema_name="jobhunter_health_check",
            schema={
                "type": "object",
                "properties": {"status": {"type": "string", "enum": ["ok"]}},
                "required": ["status"],
                "additionalProperties": False,
            },
            model=selected_model,
            max_tokens=128,
            max_recovery_tokens=2048,
        )
        if result.structured != {"status": "ok"}:
            raise InferenceResponseError(
                "Unexpected structured smoke result "
                f"from {selected_model!r} (finish_reason={result.finish_reason!r}): "
                f"{result.structured!r}"
            )
        return selected_model
