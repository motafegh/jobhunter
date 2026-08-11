from types import SimpleNamespace

import jobhunter.role_blueprint_inference as blueprint_inference
from jobhunter.role_blueprint_inference import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_models import RoleCapabilityBlueprint


def _blueprint_payload() -> dict:
    return {
        "role_read": "This is an applied AI systems role focused on production integration.",
        "likely_role_shape": "Applied AI / ML Systems Engineer",
        "capability_areas": [
            {
                "name": "Production AI integration",
                "source_capability_indices": [0],
                "interpretation_strength": "highly_likely",
                "likely_depth": "Independent implementation and debugging of production workflows.",
                "why_this_matters": "The role combines model usage with application delivery.",
                "likely_subskills": ["API integration", "validation"],
                "likely_tools_or_examples": [],
                "likely_work_products": ["A production AI-backed service"],
                "likely_failure_modes_or_operational_concerns": ["timeouts"],
                "probably_not_required": ["foundation-model pretraining"],
            }
        ],
        "hidden_requirements": [],
        "likely_end_to_end_scenarios": [
            {
                "name": "Illustrative request-to-answer flow",
                "why_likely": "A coherent professional example for an interactive AI system.",
                "flow_steps": ["Receive request", "Generate and validate response"],
                "engineering_concerns": ["latency"],
                "interpretation_strength": "plausible",
                "scenario_basis": "professional_example",
                "source_capability_indices": [0],
                "source_responsibility_indices": [],
                "assumptions": ["The source does not specify the serving topology."],
            }
        ],
        "what_probably_does_not_matter": [],
        "important_unknowns": [],
        "bottom_line": "The engineer turns AI capability into a reliable application.",
    }


class _Completion:
    choices = [SimpleNamespace(finish_reason="stop")]

    def model_dump(self, *, mode: str):
        assert mode == "json"
        return {"id": "fake"}


class _InstructorClient:
    def create_with_completion(self, **_kwargs):
        return RoleCapabilityBlueprint.model_validate(_blueprint_payload()), _Completion()


def test_blueprint_disables_read_timeout_and_prepares_runtime_context(monkeypatch) -> None:
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

    assert runtime_call["openai_base_url"] == "http://127.0.0.1:1234/v1"
    assert runtime_call["model"] == "model"
    assert runtime_call["context_length"] == 16_384
    assert captured["max_retries"] == 0
    assert captured["timeout"].read is None
    assert captured["timeout"].connect == 10.0
    assert result.request_body["runtime"] == {
        "read_timeout_seconds": None,
        "connect_timeout_seconds": 10.0,
        "transport_retries": 0,
        "configured_network_retries": 4,
        "context_length_tokens": 16_384,
        "context_action": "reused",
        "model_instance_id": "model",
    }
