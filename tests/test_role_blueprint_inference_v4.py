from types import SimpleNamespace

import jobhunter.role_blueprint_inference_v4 as blueprint_inference
from jobhunter.role_blueprint_inference_v4 import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_v4_models import RoleBlueprintDraft


def _draft_payload() -> dict:
    return {
        "role_read": "This is applied AI integration work.",
        "likely_role_shape": "Applied AI Engineer",
        "capability_interpretations": [
            {
                "interpretation_strength": "plausible",
                "likely_depth": "Practical integration and validation work.",
                "why_this_matters": "The accepted capability centers on system integration.",
                "likely_subskills": ["validation"],
                "suggested_tools_or_examples": [],
                "likely_work_products": ["Integration workflow"],
                "likely_failure_modes_or_operational_concerns": ["timeouts"],
                "probably_not_required": [],
            }
        ],
        "hidden_requirements": [],
        "professional_example_scenarios": [],
        "what_probably_does_not_matter": [],
        "important_unknowns": [],
        "bottom_line": "Reliable applied integration work.",
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


def test_v4_inference_uses_semantic_draft_and_prepares_runtime_context(monkeypatch) -> None:
    captured: dict = {}
    runtime_call: dict = {}

    def fake_openai(**kwargs):
        captured.update(kwargs)
        return object()

    def fake_context(**kwargs):
        runtime_call.update(kwargs)
        return SimpleNamespace(
            context_length=16_384,
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
        system_prompt="Analyze the role.",
        user_payload={"source_job_id": "job1"},
        max_tokens=4096,
    )

    assert runtime_call["context_length"] == 16_384
    assert captured["max_retries"] == 0
    assert captured["timeout"].read is None
    assert result.request_body["runtime"]["context_length_tokens"] == 16_384
    assert result.request_body["instructor"]["response_model"] == "RoleBlueprintDraft"
    schema = result.request_body["instructor"]["schema"]
    assert "capability_interpretations" in schema["properties"]
    assert "source_capability_coverage" not in schema["properties"]
