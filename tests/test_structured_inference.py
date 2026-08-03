import json

import httpx
import pytest

from jobhunter.inference import InferenceResponseError, LMStudioProvider

_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok"]},
        "count": {"type": "integer", "minimum": 0},
    },
    "required": ["status", "count"],
    "additionalProperties": False,
}


def _provider(payload: object, *, finish_reason: str = "stop") -> LMStudioProvider:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "finish_reason": finish_reason,
                        "message": {"content": json.dumps(payload)},
                    }
                ]
            },
        )

    return LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="test-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )


def _complete(provider: LMStudioProvider):
    return provider.complete_structured(
        system_prompt="test",
        user_payload={"input": "test"},
        schema_name="test_schema",
        schema=_SCHEMA,
        max_tokens=256,
    )


def test_accepts_structured_result_that_matches_local_schema() -> None:
    result = _complete(_provider({"status": "ok", "count": 2}))

    assert result.structured == {"status": "ok", "count": 2}


@pytest.mark.parametrize(
    "payload",
    [
        {"status": "ok"},
        {"status": "ok", "count": "2"},
        {"status": "ok", "count": -1},
        {"status": "ok", "count": 2, "unexpected": True},
        {"status": "wrong", "count": 2},
    ],
)
def test_rejects_provider_json_that_violates_requested_schema(payload: dict) -> None:
    with pytest.raises(InferenceResponseError, match="violated the requested JSON schema"):
        _complete(_provider(payload))


def test_rejects_truncated_structured_response_before_json_schema_acceptance() -> None:
    with pytest.raises(InferenceResponseError, match="was truncated"):
        _complete(_provider({"status": "ok", "count": 2}, finish_reason="length"))


def test_rejects_invalid_jobhunter_schema_before_accepting_provider_output() -> None:
    provider = _provider({"status": "ok", "count": 2})
    invalid_schema = {"type": "definitely-not-a-json-schema-type"}

    with pytest.raises(InferenceResponseError, match="invalid structured-output schema"):
        provider.complete_structured(
            system_prompt="test",
            user_payload={},
            schema_name="invalid",
            schema=invalid_schema,
        )
