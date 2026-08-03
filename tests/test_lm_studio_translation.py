import hashlib
import json

import httpx
import pytest

import jobhunter.translation.lm_studio as lm_studio_module
from jobhunter.translation.base import TranslationError
from jobhunter.translation.lm_studio import LMStudioTranslationProvider


def _id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:24]


def _response(request: httpx.Request, source: str, translation: str) -> httpx.Response:
    return httpx.Response(
        200,
        request=request,
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": json.dumps(
                            {
                                "translations": [
                                    {"id": _id(source), "translation": translation}
                                ]
                            }
                        )
                    },
                }
            ]
        },
    )


def _provider(handler) -> LMStudioTranslationProvider:
    return LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="local-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )


def test_local_translation_client_does_not_trust_proxy_environment(monkeypatch) -> None:
    real_client = httpx.Client
    trust_env_values: list[object] = []

    def client(*args, **kwargs):
        trust_env_values.append(kwargs.get("trust_env"))
        return real_client(*args, **kwargs)

    monkeypatch.setattr(lm_studio_module.httpx, "Client", client)
    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        max_retries=0,
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                request=request,
                json={"data": [{"id": "only-model"}]},
            )
        ),
    )

    assert provider.list_models() == ("only-model",)
    assert trust_env_values == [False]


def test_lm_studio_translation_uses_content_ids_and_isolates_segments() -> None:
    calls: list[str] = []
    mapping = {"متن اول": "First text", "متن دوم": "Second text"}

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        assert payload["model"] == "local-model"
        assert payload["temperature"] == 0
        assert payload["seed"] == 0
        assert payload["response_format"]["type"] == "json_schema"
        items = json.loads(payload["messages"][1]["content"])["items"]
        assert len(items) == 1
        source = items[0]["text"]
        assert items[0]["id"] == _id(source)
        calls.append(source)
        return _response(request, source, mapping[source])

    provider = _provider(handler)
    result = provider.translate_texts(
        ("متن اول", "متن دوم"), source_language="fa", target_language="en"
    )

    assert provider.name == "lm-studio-translation-v2"
    assert calls == ["متن اول", "متن دوم"]
    assert result.texts == ("First text", "Second text")


def test_lm_studio_translation_auto_selects_exactly_one_visible_model() -> None:
    paths: list[str] = []
    source = "متن نمونه"

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/v1/models":
            return httpx.Response(200, request=request, json={"data": [{"id": "only-model"}]})
        return _response(request, source, "Sample text")

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    result = provider.translate_texts((source,), source_language="fa", target_language="en")

    assert result.texts == ("Sample text",)
    assert provider.model == "only-model"
    assert paths == ["/v1/models", "/v1/chat/completions"]


def test_lm_studio_translation_refuses_ambiguous_model_selection() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            json={"data": [{"id": "model-a"}, {"id": "model-b"}]},
        )

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(TranslationError, match="multiple models"):
        provider.translate_texts(("متن",), source_language="fa", target_language="en")


def test_lm_studio_translation_rejects_wrong_content_id_via_local_schema() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": json.dumps(
                                {
                                    "translations": [
                                        {"id": "wrong-id", "translation": "Sample"}
                                    ]
                                }
                            )
                        },
                    }
                ]
            },
        )

    with pytest.raises(TranslationError, match="violated the requested response schema"):
        _provider(handler).translate_texts(
            ("متن",),
            source_language="fa",
            target_language="en",
        )


def test_lm_studio_translation_rejects_extra_structured_fields_locally() -> None:
    source = "متن"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": json.dumps(
                                {
                                    "translations": [
                                        {
                                            "id": _id(source),
                                            "translation": "Text",
                                            "explanation": "I also summarized it",
                                        }
                                    ]
                                }
                            )
                        },
                    }
                ]
            },
        )

    with pytest.raises(TranslationError, match="violated the requested response schema"):
        _provider(handler).translate_texts(
            (source,),
            source_language="fa",
            target_language="en",
        )


def test_lm_studio_translation_rejects_empty_translation_via_local_schema() -> None:
    source = "متن"

    def handler(request: httpx.Request) -> httpx.Response:
        return _response(request, source, "")

    with pytest.raises(TranslationError, match="violated the requested response schema"):
        _provider(handler).translate_texts(
            (source,),
            source_language="fa",
            target_language="en",
        )


def test_lm_studio_translation_never_batches_independent_segments() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        items = json.loads(payload["messages"][1]["content"])["items"]
        request_sizes.append(len(items))
        return _response(request, items[0]["text"], "Translated")

    provider = _provider(handler)
    result = provider.translate_texts(
        tuple(f"متن {index}" for index in range(5)),
        source_language="fa",
        target_language="en",
    )

    assert request_sizes == [1, 1, 1, 1, 1]
    assert len(result.texts) == 5


def test_lm_studio_translation_increases_budget_for_single_truncated_segment() -> None:
    max_token_budgets: list[int] = []
    source = "متن طولانی"

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        max_token_budgets.append(payload["max_tokens"])
        if payload["max_tokens"] == 4096:
            return httpx.Response(
                200,
                request=request,
                json={"choices": [{"finish_reason": "length", "message": {"content": "{"}}]},
            )
        return _response(request, source, "Complete translation")

    provider = _provider(handler)
    result = provider.translate_texts((source,), source_language="fa", target_language="en")

    assert max_token_budgets == [4096, 8192]
    assert result.texts == ("Complete translation",)
