from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.canonical_registry import CanonicalRegistryStore
from jobhunter.canonical_registry_review import build_canonical_registry_review_reader
from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.launcher import build_runtime_app

_NOW = datetime(2026, 8, 23, 18, 30, tzinfo=UTC)


def _settings(database_path: Path) -> Settings:
    return Settings(
        data_dir=database_path.parent,
        evidence_dir=database_path.parent / "evidence",
        database_path=database_path,
        analysis_lm_studio_model="analysis-model",
        translation_enabled=False,
    )


def _seed_accepted_analysis(database_path: Path, *, job_id: str = "registry-web") -> None:
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="example",
            canonical_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
            observed_text="Python Engineer",
        ),
        observed_at=_NOW,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW,
        requested_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        final_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        status_code=200,
        content_sha256=f"content-{job_id}",
        semantic_sha256=f"semantic-{job_id}",
        evidence_path=Path(f"{job_id}.html"),
        metadata_path=Path(f"{job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": "Python Engineer",
            "description": "Build Python services.",
            "skills": ["Python"],
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job(job_id)
    AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "requirements": [
                {
                    "concept": "Python",
                    "concept_type": "language",
                    "evidence": "Python",
                    "strength": "required",
                    "depth_signal": "working",
                },
                {
                    "concept": "Internal platform",
                    "concept_type": "context",
                    "evidence": "Internal platform",
                },
            ],
            "responsibilities": [
                {
                    "statement": "Build Python services",
                    "evidence": "Build Python services.",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at=_NOW,
        semantic_review_status="accepted",
    )


def test_runtime_app_registers_registry_review_routes(tmp_path: Path) -> None:
    app = build_runtime_app(_settings(tmp_path / "jobhunter.sqlite3"))
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in (getattr(route, "methods", None) or set())
    }

    assert ("/registry", "GET") in route_methods
    assert ("/registry/concepts/{concept_id}", "GET") in route_methods
    assert ("/registry/claims", "GET") in route_methods
    assert ("/registry/concepts", "POST") in route_methods
    assert ("/registry/concepts/{concept_id}/aliases", "POST") in route_methods
    assert ("/registry/concepts/{concept_id}/deprecate", "POST") in route_methods
    assert ("/registry/claims/decide", "POST") in route_methods


def test_registry_overview_is_empty_and_explicit_before_seed(tmp_path: Path) -> None:
    response = TestClient(
        build_runtime_app(_settings(tmp_path / "jobhunter.sqlite3"))
    ).get("/registry")

    assert response.status_code == 200
    assert "Canonical registry" in response.text
    assert "No automatic taxonomy growth" in response.text
    assert "0 concepts" in response.text
    assert "No reviewed canonical concepts" in response.text


def test_registry_browser_requires_csrf_and_persists_reviewed_concept_alias(
    tmp_path: Path,
) -> None:
    settings = _settings(tmp_path / "jobhunter.sqlite3")
    app = build_runtime_app(settings)
    token = app.state.csrf_token

    with TestClient(app) as client:
        rejected = client.post(
            "/registry/concepts",
            data={
                "csrf_token": "wrong",
                "concept_id": "language:python",
                "category": "language",
                "preferred_label": "Python",
                "reason": "Reviewed Python language concept",
            },
            follow_redirects=False,
        )
        created = client.post(
            "/registry/concepts",
            data={
                "csrf_token": token,
                "concept_id": "language:python",
                "category": "language",
                "preferred_label": "Python",
                "reason": "Reviewed Python language concept",
            },
            follow_redirects=False,
        )
        alias = client.post(
            "/registry/concepts/language:python/aliases",
            data={
                "csrf_token": token,
                "alias_text": "Python 3",
                "provenance": "manual",
                "reference": "review:python-3",
                "reason": "Reviewed common Python alias",
            },
            follow_redirects=False,
        )
        detail = client.get("/registry/concepts/language:python")

    assert rejected.status_code == 403
    assert created.status_code == 303
    assert alias.status_code == 303
    assert detail.status_code == 200
    assert "Python 3" in detail.text
    assert "review:python-3" in detail.text
    concept = CanonicalRegistryStore(settings.database_path).get_concept("language:python")
    assert concept is not None
    assert concept.preferred_label == "Python"


def test_registry_claim_queue_maps_exact_current_claim_and_shows_source_backing(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_accepted_analysis(database_path)
    settings = _settings(database_path)
    app = build_runtime_app(settings)
    token = app.state.csrf_token

    with TestClient(app) as client:
        pending = client.get(
            "/registry/claims",
            params={"job_id": "registry-web", "state": "pending"},
        )
        assert pending.status_code == 200
        assert "requirement[0] · Python" in pending.text
        assert "Build Python services" in pending.text

        created = client.post(
            "/registry/concepts",
            data={
                "csrf_token": token,
                "concept_id": "language:python",
                "category": "language",
                "preferred_label": "Python",
                "reason": "Reviewed Python language concept",
            },
            follow_redirects=False,
        )
        assert created.status_code == 303

        mapped = client.post(
            "/registry/claims/decide",
            data={
                "csrf_token": token,
                "job_id": "registry-web",
                "kind": "requirement",
                "claim_index": "0",
                "disposition": "mapped",
                "canonical_concept_id": "language:python",
                "reason": "Reviewed exact Python mapping",
            },
            follow_redirects=False,
        )
        assert mapped.status_code == 303

        concept_detail = client.get("/registry/concepts/language:python")

    reader = build_canonical_registry_review_reader(settings)
    mapped_items = reader.list_current_claims(
        source_job_id="registry-web",
        mapping_state="mapped",
    )
    assert len(mapped_items) == 1
    assert mapped_items[0].mapping is not None
    assert mapped_items[0].mapping.canonical_concept_id == "language:python"
    assert concept_detail.status_code == 200
    assert "registry-web" in concept_detail.text
    assert "Python" in concept_detail.text
    assert "current" in concept_detail.text


def test_registry_browser_rejects_immutable_mapping_rewrite(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_accepted_analysis(database_path)
    settings = _settings(database_path)
    store = CanonicalRegistryStore(database_path)
    store.create_concept(
        concept_id="language:python",
        category="language",
        preferred_label="Python",
        description=None,
        reviewed_at=_NOW,
        review_note="Reviewed Python language concept",
    )
    app = build_runtime_app(settings)
    token = app.state.csrf_token

    with TestClient(app) as client:
        first = client.post(
            "/registry/claims/decide",
            data={
                "csrf_token": token,
                "job_id": "registry-web",
                "kind": "requirement",
                "claim_index": "0",
                "disposition": "mapped",
                "canonical_concept_id": "language:python",
                "reason": "Reviewed exact Python mapping",
            },
            follow_redirects=False,
        )
        rewrite = client.post(
            "/registry/claims/decide",
            data={
                "csrf_token": token,
                "job_id": "registry-web",
                "kind": "requirement",
                "claim_index": "0",
                "disposition": "unmapped",
                "reason": "Attempted immutable review rewrite",
            },
            follow_redirects=False,
        )

    assert first.status_code == 303
    assert rewrite.status_code == 400
    assert "already has a reviewed mapping decision" in rewrite.text


def test_registry_review_write_does_not_trigger_public_corpus_export(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path / "jobhunter.sqlite3")
    exports: list[Path] = []
    monkeypatch.setattr(
        "jobhunter.web.launcher._synchronize_public_corpus",
        lambda active_settings: exports.append(active_settings.database_path),
    )
    app = build_runtime_app(settings)
    token = app.state.csrf_token

    with TestClient(app) as client:
        response = client.post(
            "/registry/concepts",
            data={
                "csrf_token": token,
                "concept_id": "language:python",
                "category": "language",
                "preferred_label": "Python",
                "reason": "Reviewed Python language concept",
            },
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert exports == []
