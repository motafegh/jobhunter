from types import SimpleNamespace

import jobhunter.analysis_runtime as analysis_runtime
from jobhunter.inference.lm_studio import StructuredInferenceResult


def test_analysis_provider_establishes_managed_context_before_generation(monkeypatch) -> None:
    runtime_calls: list[dict] = []
    parent_calls: list[dict] = []

    def fake_runtime(**kwargs):
        runtime_calls.append(kwargs)
        return SimpleNamespace(
            context_length=16_384,
            action="reloaded",
            instance_id="analysis-model",
        )

    def fake_complete(_self, **kwargs):
        parent_calls.append(kwargs)
        return StructuredInferenceResult(
            model="analysis-model",
            structured={
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [],
                "coverage_exclusions": [],
            },
            request_body={
                "runtime": {
                    "read_timeout_seconds": None,
                    "connect_timeout_seconds": 10.0,
                }
            },
            raw_response={"id": "fake"},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        analysis_runtime,
        "ensure_lm_studio_model_context",
        fake_runtime,
    )
    monkeypatch.setattr(
        analysis_runtime.LMStudioProvider,
        "complete_structured",
        fake_complete,
    )

    provider = analysis_runtime.RuntimeManagedAnalysisProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="analysis-model",
        api_token=None,
        timeout_seconds=30.0,
        max_retries=1,
    )
    result = provider.complete_structured(
        system_prompt="Analyze only supplied fields.",
        user_payload={
            "source_job_id": "t4jp",
            "analysis_mode": "english",
            "analysis_fields": {"description": "Sparse posting."},
        },
        schema_name="jobhunter_job_analysis_english_v9",
        schema={"type": "object"},
        model="analysis-model",
        max_tokens=8192,
    )

    assert runtime_calls == [
        {
            "openai_base_url": "http://127.0.0.1:1234/v1",
            "model": "analysis-model",
            "context_length": 16_384,
            "api_token": None,
            "connect_timeout_seconds": 10.0,
            "exclusive_llm": True,
        }
    ]
    assert len(parent_calls) == 1
    assert result.request_body["runtime"] == {
        "read_timeout_seconds": None,
        "connect_timeout_seconds": 10.0,
        "context_length_tokens": 16_384,
        "context_action": "reloaded",
        "model_instance_id": "analysis-model",
        "exclusive_llm": True,
    }
