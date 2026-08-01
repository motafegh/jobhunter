import json

import httpx

from jobhunter.translation.google_cloud import GoogleCloudTranslationProvider


def test_google_translation_uses_header_auth_and_preserves_order() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        body = request.read().decode("utf-8")
        assert '"target":"en"' in body.replace(" ", "")
        assert request.headers["x-goog-api-key"] == "secret-key"
        assert "key=" not in str(request.url)
        return httpx.Response(
            200,
            request=request,
            json={
                "data": {
                    "translations": [
                        {
                            "translatedText": "Artificial Intelligence Engineer",
                            "detectedSourceLanguage": "fa",
                        },
                        {
                            "translatedText": "Python and Docker",
                            "detectedSourceLanguage": "fa",
                        },
                    ]
                }
            },
        )

    provider = GoogleCloudTranslationProvider(
        api_key="secret-key",
        transport=httpx.MockTransport(handler),
        max_retries=0,
    )
    result = provider.translate_texts(
        ("مهندس هوش مصنوعی", "Python و Docker"),
        source_language="fa",
        target_language="en",
    )

    assert result.texts == (
        "Artificial Intelligence Engineer",
        "Python and Docker",
    )
    assert result.detected_languages == ("fa", "fa")
    assert len(requests) == 1


def test_google_translation_chunks_more_than_128_texts() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        request_sizes.append(len(payload["q"]))
        return httpx.Response(
            200,
            request=request,
            json={
                "data": {
                    "translations": [
                        {"translatedText": f"translated-{index}"}
                        for index, _text in enumerate(payload["q"])
                    ]
                }
            },
        )

    provider = GoogleCloudTranslationProvider(
        api_key="secret-key",
        request_character_target=100_000,
        transport=httpx.MockTransport(handler),
        max_retries=0,
    )
    result = provider.translate_texts(
        tuple(f"متن {index}" for index in range(129)),
        source_language="fa",
        target_language="en",
    )

    assert request_sizes == [128, 1]
    assert len(result.texts) == 129


def test_google_translation_packs_requests_by_character_target() -> None:
    request_sizes: list[int] = []
    request_characters: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read())
        texts = payload["q"]
        request_sizes.append(len(texts))
        request_characters.append(sum(len(text) for text in texts))
        return httpx.Response(
            200,
            request=request,
            json={
                "data": {
                    "translations": [
                        {"translatedText": f"translated-{index}"}
                        for index, _text in enumerate(texts)
                    ]
                }
            },
        )

    provider = GoogleCloudTranslationProvider(
        api_key="secret-key",
        request_character_target=1_000,
        transport=httpx.MockTransport(handler),
        max_retries=0,
    )
    result = provider.translate_texts(
        ("الف" * 200, "ب" * 200, "پ" * 200),
        source_language="fa",
        target_language="en",
    )

    assert request_sizes == [1, 1, 1]
    assert all(characters <= 1_000 for characters in request_characters)
    assert len(result.texts) == 3
