import json

import httpx
import pytest

from jobhunter.inference.base import InferenceProviderError, InferenceResponseError
from jobhunter.market_membership_inference import LMStudioMembershipProvider


def _response(content, finish_reason="stop"):
    return httpx.Response(
        200,
        json={
            "id": "fixture",
            "object": "chat.completion",
            "created": 1,
            "model": "test-model",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": finish_reason,
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        },
    )


def test_local_provider_structured_uncertainty_is_one_successful_call():
    requests = []

    def handle(request):
        requests.append(request)
        return _response(
            json.dumps(
                {
                    "disposition": "uncertain",
                    "reason": "Scope is sparse.",
                    "confidence": "low",
                    "evidence_refs": ["source:title"],
                }
            )
        )

    provider = LMStudioMembershipProvider(
        base_url="http://local.test/v1",
        model="test-model",
        api_token="private-token",
        validation_retries=2,
        transport=httpx.MockTransport(handle),
    )
    result = provider.classify({"evidence": {"source:title": "AI engineer"}})
    assert result.disposition == "uncertain"
    assert len(requests) == 1
    request = requests[0]
    payload = json.loads(request.content)
    assert payload["max_tokens"] == 2048
    assert payload["response_format"]["type"] == "json_schema"
    assert "tools" not in payload
    assert request.extensions["timeout"]["read"] is None
    assert request.extensions["timeout"]["connect"] <= 10
    assert "private-token" not in json.dumps(provider.identity)
    assert "local.test" not in json.dumps(provider.identity)


def test_transport_failure_is_not_replayed():
    requests = []

    def handle(request):
        requests.append(request)
        raise httpx.ConnectError("offline", request=request)

    provider = LMStudioMembershipProvider(
        base_url="http://local.test/v1",
        model="test-model",
        validation_retries=2,
        transport=httpx.MockTransport(handle),
    )
    with pytest.raises(InferenceProviderError):
        provider.classify({"evidence": {"source:title": "AI engineer"}})
    assert len(requests) == 1


@pytest.mark.parametrize("finish", ["length", "content_filter"])
def test_incomplete_completion_is_not_membership(finish):
    provider = LMStudioMembershipProvider(
        base_url="http://local.test/v1",
        model="test-model",
        transport=httpx.MockTransport(
            lambda request: _response(
                json.dumps(
                    {
                        "disposition": "core_match",
                        "reason": "Work fits.",
                        "confidence": "high",
                        "evidence_refs": ["source:description"],
                    }
                ),
                finish,
            )
        ),
    )
    with pytest.raises(InferenceResponseError):
        provider.classify({"evidence": {"source:description": "Build models."}})
