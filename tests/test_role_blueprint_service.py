from types import SimpleNamespace

import pytest

from jobhunter.role_blueprint_inference_v5 import RoleBlueprintInferenceResult
from jobhunter.role_blueprint_service import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
    RoleBlueprintError,
    RoleBlueprintService,
)
from jobhunter.role_blueprint_store import RoleBlueprintArtifact


class _SourceStore:
    def latest_source_version(self, source_job_id: str):
        return SimpleNamespace(source_job_id=source_job_id, job_detail_version_id=10)


class _AnalysisStore:
    def __init__(self, analysis=None) -> None:
        self.analysis = analysis or SimpleNamespace(
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

    def latest_current(self, _source_job_id: str, **_kwargs):
        return self.analysis


class _CapabilityStore:
    def __init__(self, capability=None) -> None:
        self.capability = capability
        if capability is None:
            self.capability = SimpleNamespace(
                id=40,
                job_detail_version_id=10,
                translation_artifact_id=30,
                analysis_artifact_id=20,
                intelligence={
                    "role_interpretation": "Derived prose should not reach Blueprint v5.",
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
                "company_description": "Excluded from the v5 model context.",
                "description": "Excluded long source description.",
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
                        "interpretation_uncertainty": (
                            "The vacancy does not state the exact integration boundary."
                        ),
                        "professional_considerations": [
                            {
                                "statement": "Input validation may matter in integration work.",
                                "interpretation_strength": "plausible",
                                "uncertainty": (
                                    "The vacancy does not state the serving boundary."
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


def _service(*, capability_store=None):
    provider = _Provider()
    blueprint_store = _BlueprintStore()
    service = RoleBlueprintService(
        source_store=_SourceStore(),
        analysis_store=_AnalysisStore(),
        capability_store=capability_store or _CapabilityStore(),
        blueprint_store=blueprint_store,
        provider=provider,
        analysis_model="analysis-model",
        capability_model="capability-model",
        blueprint_model="blueprint-model",
    )
    return service, provider, blueprint_store


def test_role_blueprint_v5_attaches_upstream_truth_and_reuses() -> None:
    service, provider, store = _service()

    first = service.build("job1")
    second = service.build("job1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert len(provider.calls) == 1
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

    payload = provider.calls[0]["user_payload"]
    assert "accepted_extraction" not in payload
    assert "capability_intelligence" not in payload
    capability_input = payload["blueprint_inputs"]["capabilities"][0]
    assert "summary" not in capability_input
    assert "sub_capabilities" not in capability_input
    assert payload["contract"]["capability_interpretation_count"] == 1


def test_role_blueprint_requires_current_capability_intelligence() -> None:
    capability_store = _CapabilityStore()
    capability_store.capability = None
    service, provider, _store = _service(capability_store=capability_store)

    with pytest.raises(RoleBlueprintError, match="Build current Capability Intelligence"):
        service.build("job1")

    assert provider.calls == []


def test_role_blueprint_requires_capability_v7_source_truth() -> None:
    capability_store = _CapabilityStore(
        capability=SimpleNamespace(
            id=40,
            job_detail_version_id=10,
            translation_artifact_id=30,
            analysis_artifact_id=20,
            intelligence={"capabilities": [{"capability_label": "AI integration"}]},
        )
    )
    service, provider, _store = _service(capability_store=capability_store)

    with pytest.raises(RoleBlueprintError, match="requires accepted Capability v7 source truth"):
        service.build("job1")

    assert provider.calls == []
