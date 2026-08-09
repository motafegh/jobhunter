import jobhunter.inference.instructor_lm_studio as instructor_analysis
from jobhunter.inference import LMStudioProvider
from jobhunter.inference.lm_studio import StructuredInferenceResult


def _schema() -> dict:
    claim = {
        "type": "object",
        "properties": {
            "statement": {"type": "string"},
            "evidence": {"type": "string"},
            "confidence": {"type": "string"},
        },
        "required": ["statement", "evidence", "confidence"],
        "additionalProperties": False,
    }
    requirement = {
        "type": "object",
        "properties": {
            "concept": {"type": "string"},
            "depth_signal": {"type": ["string", "null"]},
            "requirement_type": {"type": "string"},
            "concept_type": {"type": "string"},
            "evidence": {"type": "string"},
            "confidence": {"type": "string"},
            "rationale": {"type": "string"},
        },
        "required": [
            "concept",
            "depth_signal",
            "requirement_type",
            "concept_type",
            "evidence",
            "confidence",
            "rationale",
        ],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "role_purpose": {"type": "array", "items": claim},
            "responsibilities": {"type": "array", "items": claim},
            "requirements": {"type": "array", "items": requirement},
            "coverage_exclusions": {"type": "array", "items": {"type": "object"}},
        },
        "required": [
            "role_purpose",
            "responsibilities",
            "requirements",
            "coverage_exclusions",
        ],
        "additionalProperties": False,
    }


def test_live_analysis_schema_routes_to_instructor_helper(monkeypatch) -> None:
    calls: list[dict] = []
    expected = StructuredInferenceResult(
        model="analysis-model",
        structured={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [],
            "coverage_exclusions": [],
        },
        request_body={"instructor": {"mode": "JSON_SCHEMA"}},
        raw_response={"id": "fake"},
        finish_reason="stop",
    )

    def fake_complete_analysis_with_instructor(**kwargs):
        calls.append(kwargs)
        return expected

    monkeypatch.setattr(
        instructor_analysis,
        "complete_analysis_with_instructor",
        fake_complete_analysis_with_instructor,
    )
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="analysis-model",
        max_retries=0,
    )

    result = provider.complete_structured(
        system_prompt="Analyze only supplied fields.",
        user_payload={
            "source_job_id": "tmyX",
            "analysis_mode": "english",
            "analysis_fields": {"education": "Bachelor's degree"},
        },
        schema_name="jobhunter_job_analysis_english_v2",
        schema=_schema(),
        max_tokens=8192,
    )

    assert result is expected
    assert len(calls) == 1
    assert calls[0]["selected_model"] == "analysis-model"
    assert calls[0]["validation_retries"] == 1
    assert calls[0]["transport"] is None
