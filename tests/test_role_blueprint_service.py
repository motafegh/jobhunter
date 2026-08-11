from types import SimpleNamespace

import pytest

from jobhunter.role_blueprint_inference import RoleBlueprintInferenceResult
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
                        "requirement_type": "contextual",
                        "depth_signal": None,
                        "evidence": ["Python"],
                    },
                    {
                        "concept": "Professional experience",
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
                    "capabilities": [{"capability_label": "AI integration"}],
                    "source_truth": {"role_level_requirement_indices": [1]},
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
            model="analysis-model",
            blueprint={
                "role_read": "This is applied AI automation/integration work.",
                "likely_role_shape": "Applied AI Automation / Integration Engineer",
                "capability_areas": [
                    {
                        "name": "AI integration engineering",
                        "source_capability_indices": [0],
                        "interpretation_strength": "highly_likely",
                        "likely_depth": "Practical application/API engineering.",
                        "why_this_matters": "The role connects AI tools and internal systems.",
                        "likely_subskills": ["HTTP/JSON", "validation"],
                        "likely_tools_or_examples": [
                            {
                                "name": "Python",
                                "relationship": "source_named",
                                "why_relevant": "Python is named for the work.",
                                "source_requirement_indices": [0],
                            }
                        ],
                        "likely_work_products": ["AI integration service"],
                        "likely_failure_modes_or_operational_concerns": ["timeouts"],
                        "probably_not_required": ["foundation-model pretraining"],
                    }
                ],
                "hidden_requirements": [],
                "likely_end_to_end_scenarios": [
                    {
                        "name": "Illustrative integration flow",
                        "why_likely": "A useful example of how the integration work could connect.",
                        "flow_steps": ["Receive input", "Call service", "Validate result"],
                        "engineering_concerns": ["idempotency"],
                        "interpretation_strength": "plausible",
                        "scenario_basis": "professional_example",
                        "source_capability_indices": [0],
                        "source_responsibility_indices": [0],
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
        capability_model="analysis-model",
        blueprint_model="analysis-model",
    )
    return service, provider, blueprint_store


def test_role_blueprint_v3_reconciles_upstream_truth_and_reuses() -> None:
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
    tool = store.artifact.blueprint["capability_areas"][0]["likely_tools_or_examples"][0]
    assert tool["source_requirement_strength"] == "contextual"


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
