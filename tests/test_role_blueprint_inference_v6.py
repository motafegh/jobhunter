from types import SimpleNamespace

import jobhunter.role_blueprint_inference_v6 as blueprint_inference
from jobhunter.role_blueprint_inference_v6 import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_v6_models import RoleBlueprintDraft


def _draft_payload() -> dict:
    return {
        "capability_interpretations": [
            {
                "professional_considerations": [
                    {
                        "statement": "Input validation may matter in production-oriented work.",
                        "interpretation_strength": "plausible",
                        "uncertainty": "The vacancy does not state the serving boundary.",
                    }
                ],
                "important_unknowns": ["The runtime topology is not stated."],
            }
        ],
        "overall_unknowns": ["Latency requirements are not stated."],
    }


class _Completion:
    choices = [SimpleNamespace(finish_reason="stop")]

    def model_dump(self, *, mode: str):
        assert mode == "json"
        return {"id": "fake"}


class _InstructorClient:
    def create_with_completion(self, **kwargs):
        assert kwargs["response_model"] is RoleBlueprintDraft
        return RoleBlueprintDraft.model_validate(_draft_payload()), _Completion()


def test_v6_inference_uses_bounded_draft_and_prepares_runtime_context(monkeypatch) -> None:
    captured: dict = {}
    runtime_call: dict = {}

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return object()

    def fake_context(**kwargs):
        runtime_call.update(kwargs)
        return SimpleNamespace(
            context_length=8_192,
            action="reused",
            instance_id="model",
        )

    monkeypatch.setattr(blueprint_inference, "OpenAI", fake_openai)
    monkeypatch.setattr(
        blueprint_inference,
        "ensure_lm_studio_model_context",
        fake_context,
    )
    monkeypatch.setattr(
        blueprint_inference.instructor,
        "from_openai",
        lambda *_args, **_kwargs: _InstructorClient(),
    )

    provider = RoleBlueprintInferenceProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="model",
        timeout_seconds=30,
        network_retries=4,
    )
    result = provider.complete(
        system_prompt="Analyze the role conservatively.",
        user_payload={"source_job_id": "job1"},
        max_tokens=4096,
    )

    assert runtime_call["context_length"] == 8_192
    assert runtime_call["exclusive_llm"] is True
    assert captured["max_retries"] == 0
    assert captured["timeout"].read is None
    assert result.request_body["runtime"]["context_length_tokens"] == 8_192
    assert result.request_body["instructor"]["response_model"] == "RoleBlueprintDraft"
    properties = result.request_body["instructor"]["schema"]["properties"]
    assert "capability_interpretations" in properties
    serialized = str(result.request_body["instructor"]["schema"])
    assert "practical_interpretation" not in serialized
    assert "likely_role_shape" not in serialized
    assert "hidden_requirements" not in serialized
    assert "professional_example_scenarios" not in serialized
