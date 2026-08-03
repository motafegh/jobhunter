import json

import httpx
import pytest

import jobhunter.inference.lm_studio as lm_studio_module
from jobhunter.inference import InferenceResponseError, LMStudioProvider


def test_lists_models_from_openai_compatible_endpoint() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/models"
        return httpx.Response(
            200,
            json={"object": "list", "data": [{"id": "model-a"}, {"id": "model-b"}]},
        )

    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        transport=httpx.MockTransport(handler),
    )

    assert provider.list_models() == ["model-a", "model-b"]


def test_local_inference_client_does_not_trust_proxy_environment(monkeypatch) -> None:
    real_client = httpx.Client
    trust_env_values: list[object] = []

    def client(*args, **kwargs):
        trust_env_values.append(kwargs.get("trust_env"))
        return real_client(*args, **kwargs)

    monkeypatch.setattr(lm_studio_module.httpx, "Client", client)
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        max_retries=0,
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                request=request,
                json={"object": "list", "data": [{"id": "model-a"}]},
            )
        ),
    )

    assert provider.list_models() == ["model-a"]
    assert trust_env_values == [False]


def test_rejects_malformed_model_response() -> None:
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(200, json={"models": []})
        ),
    )

    with pytest.raises(InferenceResponseError, match="data list"):
        provider.list_models()


def test_structured_smoke_test_requires_configured_model() -> None:
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        transport=httpx.MockTransport(
            lambda _request: pytest.fail("No request should be made without a model")
        ),
    )

    with pytest.raises(InferenceResponseError, match="No LM Studio model is configured"):
        provider.structured_smoke_test()


def test_structured_smoke_test_uses_json_schema() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        request_body = json.loads(request.content)
        assert request_body["model"] == "model-a"
        assert request_body["stream"] is False
        assert request_body["max_tokens"] == 128
        assert request_body["response_format"]["type"] == "json_schema"
        assert request_body["response_format"]["json_schema"]["strict"] is True
        status_schema = request_body["response_format"]["json_schema"]["schema"][
            "properties"
        ]["status"]
        assert status_schema == {"type": "string", "enum": ["ok"]}
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": '{"status":"ok"}'},
                    }
                ]
            },
        )

    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model-a",
        transport=httpx.MockTransport(handler),
    )

    assert provider.structured_smoke_test() == "model-a"


def test_structured_smoke_test_reports_invalid_content_preview() -> None:
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model-a",
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "finish_reason": "length",
                            "message": {"content": "not-json\ntruncated"},
                        }
                    ]
                },
            )
        ),
    )

    with pytest.raises(
        InferenceResponseError,
        match=r"finish_reason='length'.*content_preview='not-json\\ntruncated'",
    ):
        provider.structured_smoke_test()


def test_structured_smoke_test_rejects_unexpected_content() -> None:
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model-a",
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": '{"status":"wrong"}'},
                        }
                    ]
                },
            )
        ),
    )

    with pytest.raises(
        InferenceResponseError,
        match="structured response violated the requested JSON schema",
    ):
        provider.structured_smoke_test()
