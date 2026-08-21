from types import SimpleNamespace

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisArtifact
from jobhunter.capability_service import CapabilityIntelligenceService
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION


class _SourceStore:
    def latest_source_version(self, source_job_id: str):
        assert source_job_id == "job1"
        return SimpleNamespace(job_detail_version_id=1)


class _AnalysisStore:
    def __init__(self, artifact: AnalysisArtifact) -> None:
        self.artifact = artifact

    def latest_current(self, source_job_id: str, **kwargs):
        assert source_job_id == "job1"
        assert kwargs["model"] == "analysis-model"
        assert kwargs["prompt_version"] == ENGLISH_PROMPT_VERSION
        assert kwargs["schema_version"] == ENGLISH_ANALYSIS_SCHEMA_VERSION
        assert kwargs["accepted_only"] is True
        return self.artifact


class _CapabilityStore:
    def translation_dependency(self, artifact_id: int):
        assert artifact_id == 2
        return SimpleNamespace(
            id=2,
            source_job_id="job1",
            job_detail_version_id=1,
            target_language="en",
            translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        )


def test_current_capability_dependency_excludes_p16_rationale_from_reasoning_view() -> None:
    persisted = AnalysisArtifact(
        id=36,
        source_job_id="job1",
        job_detail_version_id=1,
        translation_artifact_id=2,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                {
                    "concept": "Visual content production",
                    "concept_type": "skill",
                    "requirement_type": "required",
                    "depth_signal": None,
                    "evidence": "Visual content production",
                    "confidence": "high",
                    "rationale": "Misleading explanatory prose must not become model input.",
                }
            ],
            "coverage": [
                {
                    "evidence": "Visual content production",
                    "disposition": "extracted_requirement",
                    "rationale": "Coverage explanation is not a source claim either.",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at="2026-08-15T00:00:00+00:00",
    )
    service = CapabilityIntelligenceService(
        source_store=_SourceStore(),
        analysis_store=_AnalysisStore(persisted),
        capability_store=_CapabilityStore(),
        provider=object(),
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    _, _, reasoning = service._current_dependencies("job1")

    assert reasoning.id == persisted.id
    assert reasoning.translation_artifact_id == persisted.translation_artifact_id
    requirement = reasoning.analysis["requirements"][0]
    assert requirement["concept"] == "Visual content production"
    assert requirement["depth_signal"] is None
    assert requirement["evidence"] == "Visual content production"
    assert "rationale" not in requirement
    assert "rationale" not in reasoning.analysis["coverage"][0]
    assert persisted.analysis["requirements"][0]["rationale"].startswith("Misleading")
