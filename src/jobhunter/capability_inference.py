"""Instructor-backed local inference for JobHunter capability intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI

from jobhunter.capability_models import JobCapabilityIntelligence
from jobhunter.inference import InferenceConnectionError, InferenceResponseError


@dataclass(frozen=True, slots=True)
class CapabilityInferenceResult:
    model: str
    intelligence: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    finish_reason: str | None


class CapabilityInferenceProvider:
    """Run bounded typed capability reasoning against a local OpenAI-compatible endpoint."""

    def __init__(
        self,
        *,
        base_url: str,
        configured_model: str,
        api_token: str | None = None,
        timeout_seconds: float = 120.0,
        network_retries: int = 1,
        validation_retries: int = 1,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not configured_model.strip():
            raise ValueError("A concrete capability-intelligence model is required")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if not 0 <= network_retries <= 5:
            raise ValueError("network_retries must be between 0 and 5")
        if not 0 <= validation_retries <= 3:
            raise ValueError("validation_retries must be between 0 and 3")
        self._base_url = base_url.rstrip("/")
        self._model = configured_model.strip()
        self._api_token = api_token
        # Capability reasoning can legitimately produce several thousand tokens. A shared
        # 30-second inference timeout is too short for that workload on a local model, so keep
        # a long-form floor while still allowing callers to configure a larger value.
        self._timeout_seconds = max(float(timeout_seconds), 120.0)
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
    ) -> CapabilityInferenceResult:
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")
        analysis_fields = user_payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise InferenceResponseError(
                "Capability intelligence requires dictionary analysis_fields"
            )

        # Like Role Blueprint generation, this is a long-running local generation. Keep
        # connection establishment bounded but do not automatically replay a full generation
        # after a read timeout. Instructor retries remain reserved for completed responses that
        # fail the typed/semantic validation contract.
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
        client = instructor.from_openai(
            openai_client,
            mode=instructor.Mode.JSON_SCHEMA,
        )
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
                response_model=JobCapabilityIntelligence,
                messages=messages,
                context={"analysis_fields": analysis_fields},
                max_retries=self._validation_retries,
                temperature=0,
                seed=seed,
                max_tokens=max_tokens,
            )
        except (APIConnectionError, APITimeoutError) as exc:
            raise InferenceConnectionError(
                "Could not complete local capability intelligence within "
                f"{self._timeout_seconds:g}s: {exc}"
            ) from exc
        except Exception as exc:
            raise InferenceResponseError(
                "Instructor could not produce a JobHunter-valid capability intelligence "
                f"artifact after {self._validation_retries} bounded validation retries: {exc}"
            ) from exc
        finally:
            http_client.close()

        finish_reason = completion.choices[0].finish_reason if completion.choices else None
        request_body = {
            "model": self._model,
            "messages": messages,
            "temperature": 0,
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
                "response_model": "JobCapabilityIntelligence",
                "validation_retries": self._validation_retries,
                "schema": JobCapabilityIntelligence.model_json_schema(),
            },
        }
        return CapabilityInferenceResult(
            model=self._model,
            intelligence=result.model_dump(mode="json"),
            request_body=request_body,
            raw_response=completion.model_dump(mode="json"),
            finish_reason=str(finish_reason) if finish_reason is not None else None,
        )
