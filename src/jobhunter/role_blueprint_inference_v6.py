"""Instructor-backed generation for the bounded Role Capability Blueprint v6 draft."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI

from jobhunter.inference import InferenceConnectionError, InferenceResponseError
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.role_blueprint_v6_models import RoleBlueprintDraft

_BLUEPRINT_CONTEXT_LENGTH = 8_192


@dataclass(frozen=True, slots=True)
class RoleBlueprintInferenceResult:
    model: str
    blueprint: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    finish_reason: str | None


class RoleBlueprintInferenceProvider:
    """Generate only bounded professional considerations and explicit unknowns."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str,
        api_token: str | None = None,
        timeout_seconds: float = 30.0,
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
        self._connect_timeout_seconds = min(float(timeout_seconds), 10.0)
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

        runtime_context = ensure_lm_studio_model_context(
            openai_base_url=self._base_url,
            model=self._model,
            context_length=_BLUEPRINT_CONTEXT_LENGTH,
            api_token=self._api_token,
            connect_timeout_seconds=self._connect_timeout_seconds,
            transport=self._transport,
        )

        timeout = httpx.Timeout(
            connect=self._connect_timeout_seconds,
            read=None,
            write=30.0,
            pool=30.0,
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
                response_model=RoleBlueprintDraft,
                messages=messages,
                max_retries=self._validation_retries,
                temperature=0.2,
                seed=seed,
                max_tokens=max_tokens,
            )
        except (APIConnectionError, APITimeoutError) as exc:
            raise InferenceConnectionError(
                f"Could not complete the local Role Capability Blueprint request: {exc}"
            ) from exc
        except Exception as exc:
            raise InferenceResponseError(
                "Instructor could not produce a structurally valid Role Capability Blueprint v6 "
                f"draft after {self._validation_retries} bounded retries: {exc}"
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
                "read_timeout_seconds": None,
                "connect_timeout_seconds": self._connect_timeout_seconds,
                "transport_retries": 0,
                "configured_network_retries": self._network_retries,
                "context_length_tokens": runtime_context.context_length,
                "context_action": runtime_context.action,
                "model_instance_id": runtime_context.instance_id,
            },
            "instructor": {
                "mode": "JSON_SCHEMA",
                "response_model": "RoleBlueprintDraft",
                "validation_retries": self._validation_retries,
                "schema": RoleBlueprintDraft.model_json_schema(),
            },
        }
        return RoleBlueprintInferenceResult(
            model=self._model,
            blueprint=result.model_dump(mode="json"),
            request_body=request_body,
            raw_response=completion.model_dump(mode="json"),
            finish_reason=str(finish_reason) if finish_reason is not None else None,
        )
