import json
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.review_snapshot import SNAPSHOT_SCHEMA_VERSION, build_review_snapshot, write_review_snapshot
from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION
from jobhunter.role_blueprint_store import RoleBlueprintStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


def _prepare_complete_chain(database_path: Path) -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="snap1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/snap1/example",
            observed_text="ML Engineer",
        ),
        observed_at=now,
    )
    source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/acme/jobs/snap1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/snap1/example",
        status_code=200,
        content_sha256="content-snap1",
        semantic_sha256="semantic-snap1",
        evidence_path=Path("data/evidence/snap1.html"),
        metadata_path=Path("data/evidence/snap1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "ML Engineer",
            "company": "Acme",
            "description": "Build and validate production ML models. Python is required.",
            "skills": ["Python", "Machine learning"],
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )

    translation_store = TranslationStore(database_path)
    source = translation_store.latest_source_version("snap1")
    assert source is not None
    translation_id = translation_store.record_artifact(
        source=source,
        target_language="en",
        provider_name="source-identity",
        provider_model="native-english",
        translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        fields=source.fields,
        english_document="ML Engineer\nBuild and validate production ML models.",
        segment_provenance={"title": "native", "description": "native"},
        translated_segment_count=0,
        native_segment_count=2,
        translation_sha256="translation-snap1",
        created_at=now,
    )

    analysis_store = AnalysisStore(database_path)
    analysis_id = analysis_store.record_artifact(
        job_detail_version_id=source.job_detail_version_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
        analysis={
            "role_purpose": [],
            "responsibilities": [
                {
                    "statement": "Build and validate production ML models",
                    "evidence": "Build and validate production ML models.",
                    "confidence": "high",
                }
            ],
            "requirements": [
                {
                    "concept": "Python",
                    "requirement_type": "required",
                    "concept_type": "skill",
                    "evidence": "Python is required.",
                    "confidence": "high",
                    "rationale": "",
                }
            ],
        },
        request_body={"wire_secret": "analysis-request-must-not-export"},
        raw_response={"wire_secret": "analysis-raw-must-not-export"},
        created_at=now,
    )

    capability_store = CapabilityIntelligenceStore(database_path)
    capability_id = capability_store.record_artifact(
        job_detail_version_id=source.job_detail_version_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        intelligence={
            "role_interpretation": "Production-oriented ML engineering role.",
            "capabilities": [],
            "cross_capability_observations": [],
            "uncertainties": [],
        },
        request_body={"wire_secret": "capability-request-must-not-export"},
        raw_response={"wire_secret": "capability-raw-must-not-export"},
        created_at=now,
    )

    RoleBlueprintStore(database_path).record_artifact(
        job_detail_version_id=source.job_detail_version_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        capability_artifact_id=capability_id,
        model="blueprint-model",
        prompt_version=BLUEPRINT_PROMPT_VERSION,
        schema_version=BLUEPRINT_SCHEMA_VERSION,
        blueprint={
            "role_read": "A production ML role.",
            "likely_role_shape": "ML Engineer",
            "capability_areas": [],
            "hidden_requirements": [],
            "likely_end_to_end_scenarios": [],
            "what_probably_does_not_matter": [],
            "important_unknowns": [],
            "bottom_line": "Build reliable ML systems.",
        },
        request_body={"wire_secret": "blueprint-request-must-not-export"},
        raw_response={"wire_secret": "blueprint-raw-must-not-export"},
        created_at=now,
    )


def test_review_snapshot_contains_current_chain_without_raw_protocol(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare_complete_chain(database_path)

    snapshot = build_review_snapshot(database_path, "snap1")
    serialized = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)

    assert snapshot["snapshot_schema_version"] == SNAPSHOT_SCHEMA_VERSION
    assert snapshot["status"]["capability_is_current_chain"] is True
    assert snapshot["status"]["blueprint_is_current_chain"] is True
    assert snapshot["english_analysis"]["model"] == "analysis-model"
    assert snapshot["capability_intelligence"]["model"] == "capability-model"
    assert snapshot["role_capability_blueprint"]["model"] == "blueprint-model"
    assert "wire_secret" not in serialized
    assert "raw_response" not in serialized
    assert "request_body" not in serialized


def test_review_snapshot_write_is_stable_for_unchanged_artifacts(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare_complete_chain(database_path)
    output_dir = tmp_path / "review-snapshots" / "jobs"

    first = write_review_snapshot(database_path, "snap1", output_dir=output_dir)
    first_content = first.read_text(encoding="utf-8")
    second = write_review_snapshot(database_path, "snap1", output_dir=output_dir)

    assert first == second
    assert second.read_text(encoding="utf-8") == first_content
