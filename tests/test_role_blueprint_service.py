from types import SimpleNamespace

import pytest

from jobhunter.role_blueprint_inference_v4 import RoleBlueprintInferenceResult
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
                    "role_interpretation": "Applied AI automation work.",
                    "capabilities": [
                        {
                            "capability_label": "AI integration",
                            "summary": "Integrate AI capability into internal workflows.",
                            "source_requirement_indices": [0],
                            "source_responsibility_indices": [0],
                            "sub_capabilities": [],
                            "underlying_knowledge": [],
                            "operational_practices": [],
                            "operational_context": [],
                            "unknown_scope": [],
                        }
                    ],
                    "source_truth": {
                        "role_purpose": [],
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
                "company_description": "International freight-forwarding company.",
                "description": "Integrate AI tools with CRM and email. Python is listed.",
                "language": "en",
                "parser_version": "test",
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
                "role_read": "This is applied AI automation/integration work.",
                "likely_role_shape": "Applied AI Automation / Integration Engineer",
                "capability_interpretations": [
                    {
                        "interpretation_strength": "highly_likely",
                        "likely_depth": "Practical application and integration engineering.",
                        "why_this_matters": (
                            "The accepted work connects AI tools and internal systems."
                        ),
                        "likely_subskills": ["HTTP/JSON", "validation"],
                        "suggested_tools_or_examples": [],
                        "likely_work_products": ["AI integration service"],
                        "likely_failure_modes_or_operational_concerns": ["timeouts"],
                        "probably_not_required": ["foundation-model pretraining"],
                    }
                ],
                "hidden_requirements": [],
                "professional_example_scenarios": [
                    {
                        "name": "Illustrative integration flow",
                        "why_useful": "Shows one possible way the integration work could connect.",
                        "flow_steps": ["Receive input", "Call service", "Validate result"],
                        "engineering_concerns": ["idempotency"],
                        "interpretation_strength": "plausible",
                        "assumptions": ["Exact internal platform is not stated."],
                    }
                ],
                "what_probably_does_not_matter": ["training foundation models"],
                "important_unknowns": ["Exact CRM platform is not stated."],
                "bottom_line": "The role is about reliable applied-AI integration.",
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


def test_role_blueprint_v4_attaches_upstream_truth_and_reuses() -> None:
    service, provider, store = _service()

    first = service.build("job1")
    second = service.build("job1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert len(provider.calls) == 1
    assert store.artifact is not None
    assert store.artifact.prompt_version == BLUEPRINT_PROMPT_VERSION
    assert store.artifact.schema_version == BLUEPRINT_SCHEMA_VERSION
    assert store.artifact.blueprint["source_capability_coverage"] == [0]
    assert store.artifact.blueprint["source_role_constraints"][0]["requirement_index"] == 1
    area = store.artifact.blueprint["capability_areas"][0]
    assert area["source_capability_index"] == 0
    assert area["source_requirements"][0]["requirement_index"] == 0
    assert area["source_requirements"][0]["depth_signal"] == "expert"

    payload = provider.calls[0]["user_payload"]
    assert "accepted_extraction" not in payload
    assert "capability_intelligence" not in payload
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
