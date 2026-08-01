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

    assert result.texts == ("Artificial Intelligence Engineer", "Python and Docker")
    assert result.detected_languages == ("fa", "fa")
    assert len(requests) == 1


def test_google_translation_chunks_more_than_128_texts() -> None:
    request_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = __import__("json").loads(request.read())
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
