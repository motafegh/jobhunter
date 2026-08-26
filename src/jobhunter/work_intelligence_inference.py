"""Typed local inference runtime for P2.2A Job Work Intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, TypeVar

import httpx
import instructor
from openai import APIConnectionError, APITimeoutError, OpenAI
from pydantic import BaseModel

from jobhunter.inference import InferenceConnectionError, InferenceResponseError
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context

_WORK_INTELLIGENCE_CONTEXT_LENGTH = 16_384
_ModelT = TypeVar("_ModelT", bound=BaseModel)


@dataclass(frozen=True, slots=True)
class WorkIntelligenceInferenceResult:
    model: str
    intelligence: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]
    finish_reason: str | None
    validated_model: BaseModel | None = None


class WorkIntelligenceInferenceProvider:
    """Run one bounded typed Work Intelligence reasoning call against LM Studio."""

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
            raise ValueError("A concrete Work Intelligence model is required")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if not 0 <= network_retries <= 5:
            raise ValueError("network_retries must be between 0 and 5")
        if not 0 <= validation_retries <= 3:
            raise ValueError("validation_retries must be between 0 and 3")
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
        response_model: type[_ModelT],
        system_prompt: str,
        user_payload: dict[str, Any],
        max_tokens: int = 4096,
        seed: int = 0,
    ) -> WorkIntelligenceInferenceResult:
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")

        runtime_context = None
        if self._transport is None:
            runtime_context = ensure_lm_studio_model_context(
                openai_base_url=self._base_url,
                model=self._model,
                context_length=_WORK_INTELLIGENCE_CONTEXT_LENGTH,
                api_token=self._api_token,
                connect_timeout_seconds=self._connect_timeout_seconds,
                exclusive_llm=True,
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
                response_model=response_model,
                messages=messages,
                max_retries=self._validation_retries,
                temperature=0,
                seed=seed,
                max_tokens=max_tokens,
            )
        except (APIConnectionError, APITimeoutError) as exc:
            raise InferenceConnectionError(
                f"Could not complete local Job Work Intelligence reasoning: {exc}"
            ) from exc
        except Exception as exc:
            raise InferenceResponseError(
                "Instructor could not produce valid Job Work Intelligence after "
                f"{self._validation_retries} bounded validation retries: {exc}"
            ) from exc
        finally:
            http_client.close()

        finish_reason = completion.choices[0].finish_reason if completion.choices else None
        runtime_payload: dict[str, Any] = {
            "read_timeout_seconds": None,
            "connect_timeout_seconds": self._connect_timeout_seconds,
            "transport_retries": 0,
            "configured_network_retries": self._network_retries,
        }
        if runtime_context is not None:
            runtime_payload.update(
                {
                    "context_length_tokens": runtime_context.context_length,
                    "context_action": runtime_context.action,
                    "model_instance_id": runtime_context.instance_id,
                    "exclusive_llm": True,
                }
            )

        request_body = {
            "model": self._model,
            "messages": messages,
            "temperature": 0,
            "seed": seed,
            "max_tokens": max_tokens,
            "stream": False,
            "runtime": runtime_payload,
            "instructor": {
                "mode": "JSON_SCHEMA",
                "response_model": response_model.__name__,
                "validation_retries": self._validation_retries,
                "schema": response_model.model_json_schema(),
            },
        }
        return WorkIntelligenceInferenceResult(
            model=self._model,
            intelligence=result.model_dump(mode="json"),
            request_body=request_body,
            raw_response=completion.model_dump(mode="json"),
            finish_reason=str(finish_reason) if finish_reason is not None else None,
            validated_model=result,
        )


__all__ = ["WorkIntelligenceInferenceProvider", "WorkIntelligenceInferenceResult"]
