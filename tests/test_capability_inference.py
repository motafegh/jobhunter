from types import SimpleNamespace

import jobhunter.capability_inference as capability_inference
from jobhunter.capability_inference import CapabilityInferenceProvider
from jobhunter.capability_v7_models import CapabilityReasoningDraft


class _Result:
    def model_dump(self, *, mode: str):
        assert mode == "json"
        return {
            "role_interpretation": "A sufficiently long capability interpretation for testing.",
            "capabilities": [],
            "cross_capability_observations": [],
            "uncertainties": [],
        }


class _Completion:
    choices = [SimpleNamespace(finish_reason="stop")]

    def model_dump(self, *, mode: str):
        assert mode == "json"
        return {"id": "fake"}


class _InstructorClient:
    def __init__(self) -> None:
        self.kwargs: dict = {}

    def create_with_completion(self, **kwargs):
        self.kwargs = kwargs
        return _Result(), _Completion()


def test_capability_uses_managed_context_and_unbounded_read(monkeypatch) -> None:
    captured: dict = {}
    runtime_calls: list[dict] = []
    instructor_client = _InstructorClient()

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return object()

    def fake_runtime(**kwargs):
        runtime_calls.append(kwargs)
        return SimpleNamespace(
            context_length=16_384,
            action="loaded",
            instance_id="model",
        )

    monkeypatch.setattr(capability_inference, "OpenAI", fake_openai)
    monkeypatch.setattr(
        capability_inference,
        "ensure_lm_studio_model_context",
        fake_runtime,
    )
    monkeypatch.setattr(
        capability_inference.instructor,
        "from_openai",
        lambda *_args, **_kwargs: instructor_client,
    )

    provider = CapabilityInferenceProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model",
        timeout_seconds=30,
        network_retries=4,
    )
    accepted_extraction = {
        "requirements": [],
        "responsibilities": [],
        "role_purpose": [],
    }
    result = provider.complete(
        system_prompt="Analyze the job capabilities.",
        user_payload={
            "analysis_fields": {"description": "Job text."},
            "accepted_extraction": accepted_extraction,
            "evidence_reference_ids": ["field:description"],
        },
        evidence_catalog={"field:description": "Job text."},
        max_tokens=4096,
    )

    assert runtime_calls == [
        {
            "openai_base_url": "http://127.0.0.1:1234/v1",
            "model": "model",
            "context_length": 16_384,
            "api_token": None,
            "connect_timeout_seconds": 10.0,
            "exclusive_llm": True,
        }
    ]
    assert captured["max_retries"] == 0
    assert captured["timeout"].read is None
    assert captured["timeout"].connect == 10.0
    assert instructor_client.kwargs["context"]["evidence_catalog"] == {
        "field:description": "Job text."
    }
    assert instructor_client.kwargs["context"]["accepted_extraction"] == accepted_extraction
    assert instructor_client.kwargs["response_model"] is CapabilityReasoningDraft
    assert result.request_body["runtime"] == {
        "read_timeout_seconds": None,
        "connect_timeout_seconds": 10.0,
        "transport_retries": 0,
        "configured_network_retries": 4,
        "context_length_tokens": 16_384,
        "context_action": "loaded",
        "model_instance_id": "model",
        "exclusive_llm": True,
    }
    assert result.request_body["instructor"]["response_model"] == "CapabilityReasoningDraft"
