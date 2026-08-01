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
