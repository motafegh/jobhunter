import hashlib
import json

import httpx
import pytest

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

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="local-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
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


def test_lm_studio_translation_rejects_wrong_content_id() -> None:
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

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="local-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(TranslationError, match="missing or unexpected"):
        provider.translate_texts(("متن",), source_language="fa", target_language="en")


def test_lm_studio_translation_never_batches_independent_segments() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        items = json.loads(payload["messages"][1]["content"])["items"]
        request_sizes.append(len(items))
        return _response(request, items[0]["text"], "Translated")

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="local-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
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

    provider = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="local-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    result = provider.translate_texts((source,), source_language="fa", target_language="en")

    assert max_token_budgets == [4096, 8192]
    assert result.texts == ("Complete translation",)
