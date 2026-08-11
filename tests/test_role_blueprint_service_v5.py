from types import SimpleNamespace

from jobhunter.role_blueprint_inference_v5 import RoleBlueprintInferenceResult
from jobhunter.role_blueprint_service_v5 import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
    RoleBlueprintService,
)
from jobhunter.role_blueprint_store import RoleBlueprintArtifact


class _SourceStore:
    def latest_source_version(self, source_job_id: str):
        return SimpleNamespace(source_job_id=source_job_id, job_detail_version_id=10)


class _AnalysisStore:
    def latest_current(self, _source_job_id: str, **_kwargs):
        return SimpleNamespace(
            id=20,
            job_detail_version_id=10,
            translation_artifact_id=30,
            analysis={
                "role_purpose": [
                    {
                        "statement": "Integrate AI tools with internal systems",
                        "evidence": ["Integrate AI tools with internal systems"],
                    }
                ],
                "responsibilities": [
                    {
                        "statement": "Integrate AI tools with internal systems",
                        "evidence": ["Integrate AI tools with internal systems"],
                    }
                ],
                "requirements": [
                    {
                        "concept": "Python",
                        "concept_type": "skill",
                        "requirement_type": "contextual",
                        "depth_signal": "expert",
                        "evidence": ["Python (expert)"],
                    },
                    {
                        "concept": "Professional experience",
                        "concept_type": "experience",
                        "requirement_type": "required",
                        "depth_signal": "three years",
                        "evidence": ["three years"],
                    },
                ],
            },
        )


class _CapabilityStore:
    def __init__(self) -> None:
        self.capability = SimpleNamespace(
            id=40,
            job_detail_version_id=10,
            translation_artifact_id=30,
            analysis_artifact_id=20,
            intelligence={
                "role_interpretation": "Derived prose should not reach the v5 model.",
                "capabilities": [
                    {
                        "capability_label": "AI integration",
                        "summary": "Derived summary should be excluded.",
                        "source_requirement_indices": [0],
                        "source_responsibility_indices": [0],
                        "sub_capabilities": [
                            {
                                "statement": "Derived sub-capability should be excluded.",
                                "evidence_status": "strongly_implied_by_work",
                            }
                        ],
                    }
                ],
                "source_truth": {
                    "role_purpose": [
                        {"statement": "Integrate AI tools with internal systems"}
                    ],
                    "requirements": [
                        {
                            "index": 0,
                            "concept": "Python",
                            "concept_type": "skill",
                            "requirement_type": "contextual",
                            "depth_signal": "expert",
                            "evidence": ["Python (expert)"],
                        },
                        {
                            "index": 1,
                            "concept": "Professional experience",
                            "concept_type": "experience",
                            "requirement_type": "required",
                            "depth_signal": "three years",
                            "evidence": ["three years"],
                        },
                    ],
                    "responsibilities": [
                        {
                            "index": 0,
                            "statement": "Integrate AI tools with internal systems",
                            "evidence": ["Integrate AI tools with internal systems"],
                        }
                    ],
                    "role_level_requirement_indices": [1],
                },
            },
        )

    def latest_current(self, _source_job_id: str, **_kwargs):
        return self.capability

    def translation_dependency(self, artifact_id: int):
        assert artifact_id == 30
        return SimpleNamespace(
            id=30,
            source_job_id="job1",
            job_detail_version_id=10,
            fields={
                "title": "AI Automation Specialist",
                "company_description": "This field should not reach the v5 role context.",
                "description": "This source description should not be duplicated.",
                "language": "en",
            },
        )


class _Provider:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def complete(self, **kwargs):
        self.calls.append(kwargs)
        return RoleBlueprintInferenceResult(
            model="blueprint-model",
            blueprint={
                "capability_interpretations": [
                    {
                        "practical_interpretation": (
                            "This area involves applying Python in internal AI integrations."
                        ),
                        "professional_considerations": [
                            {
                                "statement": (
                                    "Input validation may matter in integration-heavy work."
                                ),
                                "interpretation_strength": "plausible",
                                "uncertainty": (
                                    "The vacancy does not state the integration boundary."
                                ),
                            }
                        ],
                        "probably_not_required": [
                            "Foundation-model pretraining is probably not central."
                        ],
                        "important_unknowns": ["The internal platform is not stated."],
                    }
                ],
                "overall_unknowns": ["Exact production topology is not stated."],
            },
            request_body={"fake": True},
            raw_response={"id": "fake"},
            finish_reason="stop",
        )


class _BlueprintStore:
    def __init__(self) -> None:
        self.artifact: RoleBlueprintArtifact | None = None
        self.attempts: list[dict] = []

    def find_artifact(self, **_kwargs):
        return self.artifact

    def record_artifact(self, **kwargs):
        self.artifact = RoleBlueprintArtifact(
            id=50,
            source_job_id="job1",
            job_detail_version_id=kwargs["job_detail_version_id"],
            translation_artifact_id=kwargs["translation_artifact_id"],
            analysis_artifact_id=kwargs["analysis_artifact_id"],
            capability_artifact_id=kwargs["capability_artifact_id"],
            model=kwargs["model"],
            prompt_version=kwargs["prompt_version"],
            schema_version=kwargs["schema_version"],
            blueprint=kwargs["blueprint"],
            request_body=kwargs["request_body"],
            raw_response=kwargs["raw_response"],
            created_at=kwargs["created_at"].isoformat(),
        )
        return 50

    def record_attempt(self, **kwargs):
        self.attempts.append(kwargs)
        return len(self.attempts)


def test_v5_service_excludes_derived_capability_prose_and_attaches_source_truth() -> None:
    provider = _Provider()
    store = _BlueprintStore()
    service = RoleBlueprintService(
        source_store=_SourceStore(),
        analysis_store=_AnalysisStore(),
        capability_store=_CapabilityStore(),
        blueprint_store=store,
        provider=provider,
        analysis_model="analysis-model",
        capability_model="capability-model",
        blueprint_model="blueprint-model",
    )

    first = service.build("job1")
    second = service.build("job1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert len(provider.calls) == 1

    payload = provider.calls[0]["user_payload"]
    inputs = payload["blueprint_inputs"]
    assert inputs["role_context"] == {"title": "AI Automation Specialist"}
    capability = inputs["capabilities"][0]
    assert capability["capability_label"] == "AI integration"
    assert "summary" not in capability
    assert "capability_reasoning" not in capability
    assert "sub_capabilities" not in capability
    assert "company_description" not in inputs["role_context"]

    assert store.artifact is not None
    assert store.artifact.prompt_version == BLUEPRINT_PROMPT_VERSION
    assert store.artifact.schema_version == BLUEPRINT_SCHEMA_VERSION
    blueprint = store.artifact.blueprint
    assert blueprint["source_capability_coverage"] == [0]
    assert blueprint["source_role_constraints"][0]["requirement_index"] == 1
    assert blueprint["source_role_purpose"][0]["statement"].startswith("Integrate")
    area = blueprint["capability_areas"][0]
    assert area["source_capability_index"] == 0
    assert area["interpretation_strength"] == "plausible"
    assert area["source_requirements"][0]["requirement_index"] == 0
    assert area["source_requirements"][0]["depth_signal"] == "expert"
