"""Small LM Studio native-API helpers for deterministic local model runtime state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import httpx

from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError


@dataclass(frozen=True, slots=True)
class LMStudioContextState:
    """Observed/applied context configuration for one local model instance."""

    model_key: str
    instance_id: str
    context_length: int
    action: str


def _native_api_base_url(openai_base_url: str) -> str:
    parsed = urlsplit(openai_base_url.rstrip("/"))
    path = parsed.path.rstrip("/")
    if path.endswith("/v1"):
        path = path[:-3]
    native_path = f"{path}/api/v1/"
    while "//" in native_path:
        native_path = native_path.replace("//", "/")
    return urlunsplit((parsed.scheme, parsed.netloc, native_path, "", ""))


def _json_object(response: httpx.Response, *, operation: str) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise InferenceResponseError(
            f"LM Studio native API returned invalid JSON while {operation}"
        ) from exc
    if not isinstance(payload, dict):
        raise InferenceResponseError(
            f"LM Studio native API returned a non-object while {operation}"
        )
    return payload


def ensure_lm_studio_model_context(
    *,
    openai_base_url: str,
    model: str,
    context_length: int,
    api_token: str | None = None,
    connect_timeout_seconds: float = 10.0,
    transport: httpx.BaseTransport | None = None,
) -> LMStudioContextState:
    """Ensure a configured LM Studio model key is loaded with enough context.

    JobHunter keeps using the OpenAI-compatible endpoint for Instructor structured
    output. LM Studio's native v1 API is used only to inspect/reconfigure the loaded
    model before that call.
    """

    if context_length < 4096:
        raise ValueError("context_length must be at least 4096")
    if connect_timeout_seconds <= 0:
        raise ValueError("connect_timeout_seconds must be greater than zero")

    native_base_url = _native_api_base_url(openai_base_url)
    headers = {"Accept": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    timeout = httpx.Timeout(
        connect=min(float(connect_timeout_seconds), 10.0),
        read=None,
        write=30.0,
        pool=30.0,
    )

    try:
        with httpx.Client(
            base_url=native_base_url,
            headers=headers,
            timeout=timeout,
            transport=transport,
            trust_env=False,
        ) as client:
            response = client.get("models")
            response.raise_for_status()
            payload = _json_object(response, operation="listing models")
            raw_models = payload.get("models")
            if not isinstance(raw_models, list):
                raise InferenceResponseError(
                    "LM Studio native model response is missing a models list"
                )

            entry: dict[str, Any] | None = None
            for candidate in raw_models:
                if not isinstance(candidate, dict):
                    continue
                if candidate.get("key") == model:
                    entry = candidate
                    break

            if entry is None:
                raise InferenceResponseError(
                    "Automatic Blueprint context management requires "
                    f"blueprint_lm_studio_model={model!r} to be an LM Studio model key "
                    "returned by GET /api/v1/models."
                )

            max_context = entry.get("max_context_length")
            if isinstance(max_context, int) and max_context < context_length:
                raise InferenceResponseError(
                    f"LM Studio model {model!r} supports at most {max_context} context tokens, "
                    f"below JobHunter's required {context_length}."
                )

            raw_instances = entry.get("loaded_instances")
            instances = raw_instances if isinstance(raw_instances, list) else []
            exact_instance = next(
                (
                    item
                    for item in instances
                    if isinstance(item, dict) and item.get("id") == model
                ),
                None,
            )

            if exact_instance is not None:
                config = exact_instance.get("config")
                current_context = (
                    config.get("context_length") if isinstance(config, dict) else None
                )
                if current_context == context_length:
                    return LMStudioContextState(
                        model_key=model,
                        instance_id=model,
                        context_length=context_length,
                        action="reused",
                    )

                unload_response = client.post(
                    "models/unload",
                    json={"instance_id": model},
                )
                unload_response.raise_for_status()

            load_response = client.post(
                "models/load",
                json={
                    "model": model,
                    "context_length": context_length,
                    "echo_load_config": True,
                },
            )
            load_response.raise_for_status()
            loaded = _json_object(load_response, operation="loading model")
            instance_id = loaded.get("instance_id") or loaded.get("model_instance_id")
            if not isinstance(instance_id, str) or not instance_id:
                raise InferenceResponseError(
                    "LM Studio load response is missing the model instance identifier"
                )
            if instance_id != model:
                raise InferenceResponseError(
                    "LM Studio loaded the requested model under a different instance id "
                    f"({instance_id!r}); JobHunter requires the configured model key {model!r} "
                    "to remain the inference identifier."
                )

            load_config = loaded.get("load_config")
            applied_context = (
                load_config.get("context_length")
                if isinstance(load_config, dict)
                else None
            )
            if applied_context != context_length:
                raise InferenceResponseError(
                    "LM Studio did not apply the requested Blueprint context length: "
                    f"requested={context_length}, applied={applied_context!r}"
                )

            return LMStudioContextState(
                model_key=model,
                instance_id=instance_id,
                context_length=context_length,
                action="reloaded" if exact_instance is not None else "loaded",
            )
    except httpx.HTTPStatusError as exc:
        body = exc.response.text[:500]
        raise InferenceResponseError(
            "LM Studio native runtime configuration failed with "
            f"HTTP {exc.response.status_code}: {body}"
        ) from exc
    except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
        raise InferenceConnectionError(
            f"Could not configure LM Studio runtime at {native_base_url}: {exc}"
        ) from exc
