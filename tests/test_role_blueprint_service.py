from types import SimpleNamespace

import pytest

from jobhunter.role_blueprint_inference import RoleBlueprintInferenceResult
from jobhunter.role_blueprint_service import RoleBlueprintError, RoleBlueprintService
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
            analysis={"requirements": [{"concept": "Python"}]},
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
                "description": (
                    "Integrate AI tools with CRM and email. Process shipping documents. "
                    "Python is an advantage."
                ),
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
                "role_read": (
                    "This is probably applied AI automation/integration work rather than "
                    "model-training research."
                ),
                "likely_role_shape": "Applied AI Automation / Integration Engineer",
                "capability_areas": [
                    {
                        "name": "Python integration engineering",
                        "interpretation_strength": "highly_likely",
                        "likely_depth": "Practical intermediate application/API engineering.",
                        "why_this_matters": (
                            "The described work connects AI APIs, documents and internal systems."
                        ),
                        "likely_subskills": ["HTTP/JSON", "validation", "error handling"],
                        "likely_tools_or_examples": [
                            {
                                "name": "httpx",
                                "relationship": "likely_example",
                                "why_relevant": "Typical Python HTTP client for API integration.",
                            }
                        ],
                        "likely_work_products": ["Document-to-CRM automation service"],
                        "likely_failure_modes_or_operational_concerns": [
                            "timeouts",
                            "malformed AI output",
                        ],
                        "probably_not_required": ["deep model training"],
                    }
                ],
                "hidden_requirements": [
                    {
                        "title": "Human review boundaries",
                        "explanation": (
                            "Consequential document fields likely need validation/review."
                        ),
                        "interpretation_strength": "highly_likely",
                    }
                ],
                "likely_end_to_end_scenarios": [
                    {
                        "name": "Document automation",
                        "why_likely": "The posting directly combines document AI and integrations.",
                        "flow_steps": [
                            "Ingest document",
                            "Extract fields",
                            "Validate",
                            "Update CRM",
                        ],
                        "engineering_concerns": ["idempotency", "auditability"],
                        "interpretation_strength": "highly_likely",
                    }
                ],
                "what_probably_does_not_matter": ["training foundation models"],
                "important_unknowns": ["Exact CRM platform is not stated."],
                "bottom_line": "The role is about reliable applied-AI business automation.",
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


def test_role_blueprint_uses_all_upstream_context_and_reuses() -> None:
    service, provider, store = _service()

    first = service.build("job1")
    second = service.build("job1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert second.artifact_id == first.artifact_id == 50
    assert len(provider.calls) == 1
    payload = provider.calls[0]["user_payload"]
    assert payload["analysis_fields"]["title"] == "AI Automation Specialist"
    assert payload["accepted_extraction"]["requirements"][0]["concept"] == "Python"
    assert payload["capability_intelligence"]["capabilities"][0]["capability_label"] == (
        "AI integration"
    )
    assert store.artifact is not None
    assert store.artifact.blueprint["capability_areas"][0]["likely_tools_or_examples"][0][
        "name"
    ] == "httpx"
    assert [attempt["outcome"] for attempt in store.attempts] == ["completed", "reused"]


def test_role_blueprint_requires_current_capability_intelligence() -> None:
    capability_store = _CapabilityStore()
    capability_store.capability = None
    service, provider, _store = _service(capability_store=capability_store)

    with pytest.raises(RoleBlueprintError, match="Build current Capability Intelligence"):
        service.build("job1")

    assert provider.calls == []


def test_role_blueprint_rejects_stale_capability_dependency() -> None:
    capability_store = _CapabilityStore(
        capability=SimpleNamespace(
            id=40,
            job_detail_version_id=9,
            translation_artifact_id=30,
            analysis_artifact_id=20,
            intelligence={},
        )
    )
    service, provider, _store = _service(capability_store=capability_store)

    with pytest.raises(RoleBlueprintError, match="stale for the current source version"):
        service.build("job1")

    assert provider.calls == []
