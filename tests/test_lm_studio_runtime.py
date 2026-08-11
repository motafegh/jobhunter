import json

import httpx
import pytest

from jobhunter.inference import InferenceResponseError
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context


def _model_payload(*, context_length: int, max_context_length: int = 32768) -> dict:
    return {
        "models": [
            {
                "key": "model",
                "max_context_length": max_context_length,
                "loaded_instances": [
                    {
                        "id": "model",
                        "config": {"context_length": context_length},
                    }
                ],
            }
        ]
    }


def test_runtime_reuses_exact_context_without_reload() -> None:
    requests: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path))
        assert request.url.path == "/api/v1/models"
        return httpx.Response(200, json=_model_payload(context_length=16384))

    state = ensure_lm_studio_model_context(
        openai_base_url="http://127.0.0.1:1234/v1",
        model="model",
        context_length=16384,
        transport=httpx.MockTransport(handler),
    )

    assert requests == [("GET", "/api/v1/models")]
    assert state.model_key == "model"
    assert state.instance_id == "model"
    assert state.context_length == 16384
    assert state.action == "reused"


def test_runtime_reloads_insufficient_context() -> None:
    requests: list[tuple[str, str, dict | None]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else None
        requests.append((request.method, request.url.path, body))
        if request.method == "GET":
            return httpx.Response(200, json=_model_payload(context_length=4096))
        if request.url.path.endswith("/unload"):
            return httpx.Response(200, json={"instance_id": "model"})
        assert request.url.path.endswith("/load")
        return httpx.Response(
            200,
            json={
                "type": "llm",
                "instance_id": "model",
                "status": "loaded",
                "load_config": {"context_length": 16384},
            },
        )

    state = ensure_lm_studio_model_context(
        openai_base_url="http://127.0.0.1:1234/v1",
        model="model",
        context_length=16384,
        transport=httpx.MockTransport(handler),
    )

    assert requests == [
        ("GET", "/api/v1/models", None),
        ("POST", "/api/v1/models/unload", {"instance_id": "model"}),
        (
            "POST",
            "/api/v1/models/load",
            {"model": "model", "context_length": 16384, "echo_load_config": True},
        ),
    ]
    assert state.action == "reloaded"
    assert state.context_length == 16384


def test_runtime_rejects_model_with_too_small_native_context() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=_model_payload(context_length=4096, max_context_length=8192),
        )

    with pytest.raises(InferenceResponseError, match="supports at most 8192"):
        ensure_lm_studio_model_context(
            openai_base_url="http://127.0.0.1:1234/v1",
            model="model",
            context_length=16384,
            transport=httpx.MockTransport(handler),
        )
