from types import SimpleNamespace

import jobhunter.capability_inference as capability_inference
from jobhunter.capability_inference import CapabilityInferenceProvider


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
    def create_with_completion(self, **_kwargs):
        return _Result(), _Completion()


def test_capability_timeout_has_120_second_floor() -> None:
    provider = CapabilityInferenceProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model",
        timeout_seconds=30,
    )

    assert provider._timeout_seconds == 120.0


def test_capability_disables_transport_replay_for_long_generation(monkeypatch) -> None:
    captured: dict = {}

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(capability_inference, "OpenAI", fake_openai)
    monkeypatch.setattr(
        capability_inference.instructor,
        "from_openai",
        lambda *_args, **_kwargs: _InstructorClient(),
    )

    provider = CapabilityInferenceProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model",
        timeout_seconds=30,
        network_retries=4,
    )
    result = provider.complete(
        system_prompt="Analyze the job capabilities.",
        user_payload={"analysis_fields": {"description": "Job text."}},
        max_tokens=4096,
    )

    assert captured["max_retries"] == 0
    assert captured["timeout"].read == 120.0
    assert result.request_body["runtime"] == {
        "timeout_seconds": 120.0,
        "transport_retries": 0,
        "configured_network_retries": 4,
    }
