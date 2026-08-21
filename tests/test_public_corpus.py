from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_ANALYSIS_SCHEMA_VERSION,
    ORIGINAL_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.public_corpus import export_public_corpus, verify_public_corpus
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore


def _seed_source(database_path: Path) -> tuple[int, dict[str, object]]:
    store = JobHunterStore(database_path)
    store.initialize()
    now = datetime(2026, 8, 16, 18, 0, tzinfo=UTC)
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="fa01",
            company_slug="example-company",
            canonical_url="https://jobinja.ir/companies/example-company/jobs/fa01",
            observed_text="مهندس پایتون",
        ),
        observed_at=now,
    )
    fields: dict[str, object] = {
        "language": "fa",
        "parser_version": "jobinja-detail-v2",
        "title": "مهندس پایتون",
        "description": "توسعه سرویس‌های پایتون و لینوکس",
        "skills": ["Python", "Linux"],
    }
    detail = store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/example-company/jobs/fa01",
        final_url="https://jobinja.ir/companies/example-company/jobs/fa01",
        status_code=200,
        content_sha256="content-1",
        semantic_sha256="semantic-1",
        evidence_path=Path("/private/local/evidence/fa01.html"),
        metadata_path=Path("/private/local/evidence/fa01.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields=fields,
    )
    return detail.version_id, fields


def _seed_full_chain(database_path: Path) -> None:
    detail_id, source_fields = _seed_source(database_path)
    now = datetime(2026, 8, 16, 18, 5, tzinfo=UTC)

    translation_store = TranslationStore(database_path)
    translation_id = translation_store.record_artifact(
        source=TranslationSourceVersion(
            source_job_id="fa01",
            job_detail_version_id=detail_id,
            semantic_sha256="semantic-1",
            source_language="fa",
            fields=source_fields,
        ),
        target_language="en",
        provider_name="lm-studio",
        provider_model="translation-model",
        translation_schema_version="lm-studio-translation-v2",
        fields={
            "language": "en",
            "title": "Python Engineer",
            "description": "Develop Python and Linux services",
            "skills": ["Python", "Linux"],
        },
        english_document="Python Engineer\nDevelop Python and Linux services",
        segment_provenance={"title": "translated", "description": "translated"},
        translated_segment_count=2,
        native_segment_count=0,
        translation_sha256="translation-1",
        created_at=now,
    )

    analysis_store = AnalysisStore(database_path)
    english_analysis_id = analysis_store.record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={"requirements": [{"concept": "Python", "strength": "required"}]},
        request_body={"secret_protocol": "do-not-export"},
        raw_response={"raw": "do-not-export"},
        created_at=now,
    )
    analysis_store.record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=None,
        model="analysis-model",
        prompt_version=ORIGINAL_PROMPT_VERSION,
        schema_version=ORIGINAL_ANALYSIS_SCHEMA_VERSION,
        analysis={"requirements": [{"concept": "Python", "strength": "required"}]},
        request_body={"secret_protocol": "do-not-export"},
        raw_response={"raw": "do-not-export"},
        created_at=now,
    )

    CapabilityIntelligenceStore(database_path).record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=english_analysis_id,
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        intelligence={"capability_profiles": [{"label": "Python Engineering"}]},
        request_body={"secret_protocol": "do-not-export"},
        raw_response={"raw": "do-not-export"},
        created_at=now,
    )


def test_public_corpus_exports_current_public_chain_without_private_protocol(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    output_dir = tmp_path / "corpus"
    _seed_full_chain(database_path)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "UPDATE job_analysis_artifacts SET semantic_reviewed_at = ?, "
            "semantic_review_note = ? WHERE prompt_version = ?",
            (
                "2026-08-16T19:00:00+00:00",
                "private reviewer note must not export",
                ENGLISH_PROMPT_VERSION,
            ),
        )

    summary = export_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    assert summary.jobs == 1
    assert summary.english_projections == 1
    assert summary.english_analyses == 1
    assert summary.original_analyses == 1
    assert summary.capabilities == 1

    job_dir = output_dir / "jobs" / "fa01"
    source = json.loads((job_dir / "source.json").read_text(encoding="utf-8"))
    projection = json.loads(
        (job_dir / "english-projection.json").read_text(encoding="utf-8")
    )
    p16 = json.loads((job_dir / "p16-english.json").read_text(encoding="utf-8"))
    capability = json.loads((job_dir / "capability.json").read_text(encoding="utf-8"))
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))

    assert source["current_detail"]["fields"]["title"] == "مهندس پایتون"
    assert source["current_detail"]["fields"]["description"].startswith("توسعه")
    assert "evidence_path" not in source["current_detail"]
    assert "metadata_path" not in source["current_detail"]
    assert projection["fields"]["title"] == "Python Engineer"
    assert p16["translation_artifact_id"] == projection["artifact_id"]
    assert capability["analysis_artifact_id"] == p16["artifact_id"]
    assert "request_body" not in p16
    assert "raw_response" not in p16
    assert "semantic_review_note" not in p16
    assert "semantic_reviewed_at" not in p16
    assert "private reviewer note" not in json.dumps(p16)
    assert "request_body" not in capability
    assert "raw_response" not in capability
    assert manifest["counts"] == {
        "jobs": 1,
        "sources": 1,
        "english_projections": 1,
        "p16_english": 1,
        "p16_original": 1,
        "capabilities": 1,
    }
    assert manifest["jobs"][0]["artifact_ids"]["capability"] == capability["artifact_id"]

    verification = verify_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )
    assert verification.ok
    assert verification.errors == ()


def test_public_corpus_removes_stale_downstream_files_after_source_change(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    output_dir = tmp_path / "corpus"
    _seed_full_chain(database_path)
    export_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    store = JobHunterStore(database_path)
    posting = store.get_job("fa01")
    assert posting is not None
    store.record_job_detail(
        job_posting_id=posting.id,
        fetched_at=datetime(2026, 8, 16, 19, 0, tzinfo=UTC),
        requested_url=posting.canonical_url,
        final_url=posting.canonical_url,
        status_code=200,
        content_sha256="content-2",
        semantic_sha256="semantic-2",
        evidence_path=Path("/private/local/evidence/fa01-v2.html"),
        metadata_path=Path("/private/local/evidence/fa01-v2.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "fa",
            "parser_version": "jobinja-detail-v2",
            "title": "مهندس ارشد پایتون",
            "description": "نسخه جدید آگهی",
        },
    )

    export_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    job_dir = output_dir / "jobs" / "fa01"
    assert (job_dir / "source.json").exists()
    assert not (job_dir / "english-projection.json").exists()
    assert not (job_dir / "p16-english.json").exists()
    assert not (job_dir / "p16-original.json").exists()
    assert not (job_dir / "capability.json").exists()

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["jobs"][0]["stages"] == {
        "source": True,
        "english_projection": False,
        "p16_english": False,
        "p16_original": False,
        "capability": False,
    }


def test_public_corpus_excludes_pending_analysis_and_its_capability(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    output_dir = tmp_path / "corpus"
    _seed_full_chain(database_path)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "UPDATE job_analysis_artifacts SET semantic_review_status = 'pending' "
            "WHERE prompt_version = ?",
            (ENGLISH_PROMPT_VERSION,),
        )

    summary = export_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    job_dir = output_dir / "jobs" / "fa01"
    assert summary.english_analyses == 0
    assert summary.capabilities == 0
    assert not (job_dir / "p16-english.json").exists()
    assert not (job_dir / "capability.json").exists()


def test_public_corpus_verify_detects_tampering(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    output_dir = tmp_path / "corpus"
    _seed_full_chain(database_path)
    export_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    source_path = output_dir / "jobs" / "fa01" / "source.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["title_observed"] = "tampered"
    source_path.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")

    verification = verify_public_corpus(
        database_path,
        output_dir=output_dir,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )
    assert not verification.ok
    assert "fa01/source.json differs from SQLite state" in verification.errors
