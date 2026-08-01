import json

import httpx
import pytest

from jobhunter.translation.base import TranslationError
from jobhunter.translation.lm_studio import LMStudioTranslationProvider


def test_lm_studio_translation_uses_structured_output_and_preserves_order() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert request.url.path == "/v1/chat/completions"
        payload = json.loads(request.read())
        assert payload["model"] == "local-model"
        assert payload["temperature"] == 0
        assert payload["seed"] == 0
        response_format = payload["response_format"]
        assert response_format["type"] == "json_schema"
        user_payload = json.loads(payload["messages"][1]["content"])
        assert [item["id"] for item in user_payload["items"]] == [0, 1]
        assert user_payload["items"][0]["text"] == "آشنایی با Docker"
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
                                        {"id": 1, "translation": "Proficiency in Python"},
                                        {"id": 0, "translation": "Familiarity with Docker"},
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
    result = provider.translate_texts(
        ("آشنایی با Docker", "تسلط بر Python"),
        source_language="fa",
        target_language="en",
    )

    assert result.texts == ("Familiarity with Docker", "Proficiency in Python")
    assert result.detected_languages == ("fa", "fa")
    assert len(requests) == 1


def test_lm_studio_translation_auto_selects_exactly_one_visible_model() -> None:
    paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/v1/models":
            return httpx.Response(
                200,
                request=request,
                json={"data": [{"id": "only-model"}]},
            )
        payload = json.loads(request.read())
        assert payload["model"] == "only-model"
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
                                        {"id": 0, "translation": "AI Engineer"}
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
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    result = provider.translate_texts(
        ("مهندس هوش مصنوعی",),
        source_language="fa",
        target_language="en",
    )

    assert result.texts == ("AI Engineer",)
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
        provider.translate_texts(
            ("مهندس امنیت",),
            source_language="fa",
            target_language="en",
        )


def test_lm_studio_translation_rejects_missing_ids() -> None:
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
                                        {"id": 0, "translation": "AI Engineer"},
                                        {"id": 2, "translation": "Unexpected"},
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
        provider.translate_texts(
            ("مهندس هوش مصنوعی", "امنیت شبکه"),
            source_language="fa",
            target_language="en",
        )


def test_lm_studio_translation_chunks_large_batches_and_sends_api_token() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer local-secret"
        payload = json.loads(request.read())
        user_payload = json.loads(payload["messages"][1]["content"])
        items = user_payload["items"]
        request_sizes.append(len(items))
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
                                            "id": item["id"],
                                            "translation": f"translated-{item['id']}",
                                        }
                                        for item in items
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
        api_token="local-secret",
        max_retries=0,
        request_character_target=100_000,
        transport=httpx.MockTransport(handler),
    )
    result = provider.translate_texts(
        tuple(f"متن {index}" for index in range(33)),
        source_language="fa",
        target_language="en",
    )

    assert request_sizes == [32, 1]
    assert len(result.texts) == 33


def test_lm_studio_translation_splits_multi_item_batch_after_truncation() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        items = json.loads(payload["messages"][1]["content"])["items"]
        request_sizes.append(len(items))
        if len(items) == 2:
            return httpx.Response(
                200,
                request=request,
                json={
                    "choices": [
                        {
                            "finish_reason": "length",
                            "message": {"content": "{"},
                        }
                    ]
                },
            )
        source_text = items[0]["text"]
        translation = "First translation" if source_text == "متن اول" else "Second translation"
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
                                        {"id": 0, "translation": translation}
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
    result = provider.translate_texts(
        ("متن اول", "متن دوم"),
        source_language="fa",
        target_language="en",
    )

    assert request_sizes == [2, 1, 1]
    assert result.texts == ("First translation", "Second translation")


def test_lm_studio_translation_increases_budget_for_single_truncated_segment() -> None:
    max_token_budgets: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        max_token_budgets.append(payload["max_tokens"])
        if payload["max_tokens"] == 4096:
            return httpx.Response(
                200,
                request=request,
                json={
                    "choices": [
                        {
                            "finish_reason": "length",
                            "message": {"content": "{"},
                        }
                    ]
                },
            )
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
                                        {"id": 0, "translation": "Complete translation"}
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
    result = provider.translate_texts(
        ("متن طولانی",),
        source_language="fa",
        target_language="en",
    )

    assert max_token_budgets == [4096, 8192]
    assert result.texts == ("Complete translation",)
