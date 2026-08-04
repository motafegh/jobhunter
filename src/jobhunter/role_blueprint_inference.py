"""Instructor-backed expert interpretation for Role Capability Blueprints."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI

from jobhunter.inference import InferenceConnectionError, InferenceResponseError
from jobhunter.role_blueprint_models import RoleCapabilityBlueprint

_BLUEPRINT_MIN_TIMEOUT_SECONDS = 120.0


@dataclass(frozen=True, slots=True)
class RoleBlueprintInferenceResult:
    model: str
    blueprint: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    finish_reason: str | None


class RoleBlueprintInferenceProvider:
    """Run one bounded but intentionally flexible expert-role interpretation call."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str,
        api_token: str | None = None,
        timeout_seconds: float = _BLUEPRINT_MIN_TIMEOUT_SECONDS,
        network_retries: int = 1,
        validation_retries: int = 1,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not configured_model.strip():
            raise ValueError("A concrete role-blueprint model is required")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if not 0 <= network_retries <= 5:
            raise ValueError("network_retries must be between 0 and 5")
        if not 0 <= validation_retries <= 2:
            raise ValueError("validation_retries must be between 0 and 2")
        self._base_url = base_url.rstrip("/")
        self._model = configured_model.strip()
        self._api_token = api_token
        # The shared inference timeout is intentionally short for normal calls. A Blueprint is a
        # much larger human-facing artifact, so never let a shared 30s setting cut it off mid-run.
        self._timeout_seconds = max(timeout_seconds, _BLUEPRINT_MIN_TIMEOUT_SECONDS)
        self._network_retries = network_retries
        self._validation_retries = validation_retries
        self._transport = transport

    def complete(
        self,
        *,
        system_prompt: str,
        user_payload: dict[str, Any],
        max_tokens: int = 8192,
        seed: int = 0,
    ) -> RoleBlueprintInferenceResult:
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")

        # Blueprints are intentionally long-form. Keep connection establishment bounded, but
        # allow the local model enough read time to finish the response. Do not let the OpenAI
        # client automatically replay an already-running long generation after a read timeout;
        # Instructor retries are reserved for completed responses that fail structural validation.
        timeout = httpx.Timeout(
            self._timeout_seconds,
            connect=min(10.0, self._timeout_seconds),
        )
        http_client = httpx.Client(
            timeout=timeout,
            transport=self._transport,
            trust_env=False,
        )
        openai_client = OpenAI(
            base_url=self._base_url,
            api_key=self._api_token or "lm-studio-local",
            timeout=timeout,
            max_retries=0,
            http_client=http_client,
        )
        client = instructor.from_openai(openai_client, mode=instructor.Mode.JSON_SCHEMA)
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(user_payload, ensure_ascii=False, sort_keys=True),
            },
        ]

        try:
            result, completion = client.create_with_completion(
                model=self._model,
                response_model=RoleCapabilityBlueprint,
                messages=messages,
                max_retries=self._validation_retries,
                temperature=0.2,
                seed=seed,
                max_tokens=max_tokens,
            )
        except (APIConnectionError, APITimeoutError) as exc:
            raise InferenceConnectionError(
                "Could not complete the local Role Capability Blueprint request "
                f"within {self._timeout_seconds:g}s: {exc}"
            ) from exc
        except Exception as exc:
            raise InferenceResponseError(
                "Instructor could not produce a structurally valid Role Capability Blueprint "
                f"after {self._validation_retries} bounded retries: {exc}"
            ) from exc
        finally:
            http_client.close()

        finish_reason = completion.choices[0].finish_reason if completion.choices else None
        request_body = {
            "model": self._model,
            "messages": messages,
            "temperature": 0.2,
            "seed": seed,
            "max_tokens": max_tokens,
            "stream": False,
            "runtime": {
                "timeout_seconds": self._timeout_seconds,
                "transport_retries": 0,
                "configured_network_retries": self._network_retries,
            },
            "instructor": {
                "mode": "JSON_SCHEMA",
                "response_model": "RoleCapabilityBlueprint",
                "validation_retries": self._validation_retries,
                "schema": RoleCapabilityBlueprint.model_json_schema(),
            },
        }
        return RoleBlueprintInferenceResult(
            model=self._model,
            blueprint=result.model_dump(mode="json"),
            request_body=request_body,
            raw_response=completion.model_dump(mode="json"),
            finish_reason=str(finish_reason) if finish_reason is not None else None,
        )
