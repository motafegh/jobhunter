from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.canonical_registry import build_canonical_registry_service
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.job_comparison import build_job_comparison
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.launcher import build_runtime_app

NOW = datetime(2026, 10, 26, 12, tzinfo=UTC)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path, evidence_dir=tmp_path / "evidence",
        database_path=tmp_path / "test.sqlite3", translation_enabled=False,
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
    )


def _seed(
    settings: Settings, job_id: str, *, status: str = "accepted",
    responsibilities: bool = True, grouping: bool = False, invalid_dependency: bool = False,
) -> tuple[int, int, int]:
    store = JobHunterStore(settings.database_path)
    store.initialize()
    url = f"https://jobinja.ir/companies/example/jobs/{job_id}/role"
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id, company_slug="example", canonical_url=url,
            observed_text="Python Engineer",
        ), observed_at=NOW,
    )
    detail = store.record_job_detail(
        job_posting_id=posting.job_posting_id, fetched_at=NOW,
        requested_url=url, final_url=url, status_code=200, content_sha256=job_id,
        semantic_sha256=job_id, evidence_path=Path("source.html"), metadata_path=Path("meta.json"),
        parser_version="jobinja-detail-v2", parse_status="parsed",
        fields={"language": "en", "title": f"Engineer {job_id}", "company": "Example",
                "description": "Build Python services. Python proficiency. SQL preferred.",
                "skills": ["Python"]},
    )
    translation = TranslationService(
        store=TranslationStore(settings.database_path), provider=None,
    ).translate_job(job_id)
    analysis_id = AnalysisStore(settings.database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model", prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "requirements": [
                {"concept": "Python proficiency", "concept_type": "language",
                 "requirement_type": "required", "depth_signal": "proficiency",
                 "evidence": "Python proficiency, SQL preferred"},
                {"concept": "SQL preferred", "concept_type": "language",
                 "requirement_type": "preferred", "depth_signal": None,
                 "evidence": "SQL preferred"},
            ],
            "responsibilities": [
                {"statement": "Build Python services", "evidence": "Build Python services."},
            ] if responsibilities else [],
        }, request_body={}, raw_response={}, created_at=NOW,
        semantic_review_status="pending" if status == "rejected" else status,
    )
    if grouping:
        profiles = [
            {"capability_label": label, "summary": "Existing job-local organization",
             "source_requirement_indices": [0],
             "source_responsibility_indices": [0] if responsibilities else [],
             "work_activities": [{"statement": "Build Python services",
                                  "evidence_status": "source_explicit"}],
             "unknown_scope": [{"statement": "Production scale is unknown",
                                "evidence_status": "unknown_or_unsupported"}]}
            for label in ("Python implementation", "Service engineering")
        ]
        CapabilityIntelligenceStore(settings.database_path).record_artifact(
            job_detail_version_id=detail.version_id,
            translation_artifact_id=translation.artifact_id,
            analysis_artifact_id=analysis_id, model="capability-model",
            prompt_version=CAPABILITY_PROMPT_VERSION, schema_version=CAPABILITY_SCHEMA_VERSION,
            intelligence={"capabilities": profiles}, request_body={}, raw_response={},
            created_at=NOW,
        )
        if invalid_dependency:
            with sqlite3.connect(settings.database_path) as connection:
                # A same-source artifact with a mismatched analysis is invalid for this view.
                connection.execute(
                    "UPDATE job_capability_intelligence_artifacts SET analysis_artifact_id = 999"
                )
    if status == "rejected":
        with sqlite3.connect(settings.database_path) as connection:
            connection.execute(
                "UPDATE job_analysis_artifacts SET semantic_review_status = 'rejected'"
            )
    return detail.version_id, translation.artifact_id, analysis_id


def _rows(settings: Settings) -> dict:
    with sqlite3.connect(settings.database_path) as connection:
        names = [r[0] for r in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        )]
        return {n: connection.execute(f'SELECT * FROM "{n}"').fetchall() for n in names}


def test_factual_fallback_preserves_strength_depth_and_literal_search(settings: Settings) -> None:
    _seed(settings, "direct")
    _seed(settings, "qualifications", responsibilities=False)
    result = build_job_comparison(settings, ("direct", "qualifications"), " PYTHON ")
    direct, qualifications = result.jobs
    assert len(direct.requirements) == len(direct.responsibilities) == 1
    assert direct.requirements[0].strength == "required"
    assert direct.requirements[0].depth_signal == "proficiency"
    assert qualifications.responsibilities == ()
    assert qualifications.total_responsibilities == 0
    assert not direct.groups
    assert all(c.mapping_state == "pending" for c in direct.claims)
    assert not build_job_comparison(settings, ("direct",), "PyTorch").jobs[0].matching_claims
    sql = build_job_comparison(settings, ("direct",), "SQL").jobs[0]
    assert len(sql.matching_claims) == 1  # Shared evidence cannot make Python match SQL.
    assert sql.requirements[0].strength == "preferred"


def test_optional_groups_keep_unique_facts_and_requirement_only_boundary(
    settings: Settings,
) -> None:
    _seed(settings, "direct", grouping=True)
    _seed(settings, "qualified", grouping=True, responsibilities=False)
    direct, qualified = build_job_comparison(settings, ("direct", "qualified")).jobs
    assert len(direct.claims) == len(direct.matching_claims) == 3
    assert len(direct.groups) == 2
    assert [g.shared_claim_count for g in direct.groups] == [2, 2]
    assert len(direct.requirements) == 2
    assert len(direct.responsibilities) == 1
    assert len(qualified.groups) == 2
    assert all(not g.interpretation.work_activities for g in qualified.groups)
    assert qualified.total_responsibilities == 0


@pytest.mark.parametrize("status", ["pending", "rejected"])
def test_unaccepted_analysis_never_feeds_comparison(settings: Settings, status: str) -> None:
    _seed(settings, "unaccepted", status=status, grouping=True)
    result = build_job_comparison(settings, ("unaccepted",))
    assert not result.jobs[0].claims
    assert not result.jobs[0].groups


def test_stale_source_excludes_old_accepted_claims(settings: Settings) -> None:
    _seed(settings, "changed", grouping=True)
    with sqlite3.connect(settings.database_path) as connection:
        # Clone the source observation as a new semantic version, with no current derivations.
        columns = [r[1] for r in connection.execute("PRAGMA table_info(job_detail_versions)")
                   if r[1] != "id"]
        fields = ", ".join(columns)
        values = ", ".join(
            "'new-content'" if name == "content_sha256" else
            "'new-semantics'" if name == "semantic_sha256" else name
            for name in columns
        )
        connection.execute(
            f"INSERT INTO job_detail_versions ({fields}) SELECT {values} FROM job_detail_versions"
        )
    result = build_job_comparison(settings, ("changed",))
    assert not result.jobs[0].claims
    assert not result.jobs[0].groups


def test_wrong_capability_dependency_withholds_only_overlay(settings: Settings) -> None:
    _seed(settings, "mismatch", grouping=True, invalid_dependency=True)
    result = build_job_comparison(settings, ("mismatch",))
    job = result.jobs[0]
    assert len(job.claims) == 3
    assert job.groups == ()
    assert "could not be validated" in job.grouping_notice


def test_reviewed_identity_stays_attached_to_exact_claim(settings: Settings) -> None:
    _seed(settings, "mapped")
    from jobhunter.canonical_registry import CanonicalRegistryStore

    CanonicalRegistryStore(settings.database_path).create_concept(
        concept_id="language:python", category="language", preferred_label="Python",
        description="Python language", reviewed_at=NOW, review_note="Reviewed test identity",
    )
    build_canonical_registry_service(settings).record_current_claim_mapping(
        "mapped", claim_kind="requirement", claim_index=0, disposition="mapped",
        canonical_concept_id="language:python", reviewed_at=NOW,
        review_note="Reviewed exact Python qualification",
    )
    result = build_job_comparison(settings, ("mapped",))
    assert result.canonical_labels == {"language:python": "Python"}
    assert result.jobs[0].requirements[0].mapping.canonical_concept_id == "language:python"
    assert result.jobs[0].requirements[1].mapping is None


def test_rendered_view_is_read_only_and_counts_each_fact_once(settings: Settings) -> None:
    _seed(settings, "direct", grouping=True)
    with TestClient(build_runtime_app(settings)) as client:
        assert client.get("/compare", params={"job": "direct"}).status_code == 200
        before = _rows(settings)
        response = client.get("/compare", params={"job": "direct", "q": "Python"})
        assert response.status_code == 200
        assert "2</strong> distinct matching claims out of 3" in response.text
        assert response.text.count('class="comparison-fact"') == 2
        assert "Existing capability labels are job-local interpretation" in response.text
        assert "also appear in other groups" in response.text
        assert "claim-1-requirement-0" in response.text
        assert _rows(settings) == before


def test_browser_bounds_empty_state_and_origin_validation(settings: Settings) -> None:
    with TestClient(build_runtime_app(settings)) as client:
        assert "No accepted/current" in client.get("/compare").text
        assert client.get("/compare?job=unknown").status_code == 404
        assert client.get("/compare?job=a&job=b&job=c&job=d").status_code == 422
        assert client.get("/compare", params={"q": "x" * 121}).status_code == 422
        assert client.get("/compare?from_snapshot=1").status_code == 400
        assert client.get("/compare?origin_job=a&from_snapshot=invalid").status_code == 422


def test_source_wording_is_escaped_and_no_match_is_not_absence(settings: Settings) -> None:
    _seed(settings, "escaped")
    with sqlite3.connect(settings.database_path) as connection:
        connection.execute(
            "UPDATE job_analysis_artifacts SET analysis_json = "
            "replace(analysis_json, 'SQL preferred', '<script>alert(1)</script>')"
        )
    with TestClient(build_runtime_app(settings)) as client:
        response = client.get("/compare?job=escaped")
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in response.text
        assert "<script>alert(1)</script>" not in response.text
        no_match = client.get("/compare?job=escaped&q=NumPy")
        assert "not proof of absence" in no_match.text
        assert "not that the capability is unnecessary" in no_match.text


def test_compact_overview_uses_exact_distinct_facts_and_preserves_unknowns(
    settings: Settings,
) -> None:
    _seed(settings, "direct", grouping=True)
    _seed(settings, "qualified", responsibilities=False)
    with TestClient(build_runtime_app(settings)) as client:
        response = client.get("/compare?job=direct&job=qualified&q=Python")
        # The first Registry reader initializes its empty tables; compare subsequent GETs.
        before = _rows(settings)
        assert response.status_code == 200
        html = response.text
        assert html.count('class="text-link comparison-overview-job"') == 2
        assert "2 of 3 distinct accepted claims match this wording." in html
        assert "1 of 2 distinct accepted claims match this wording." in html
        assert "1</strong> matching direct duties" in html
        assert "0</strong> matching direct duties" in html
        assert "No direct duties stated in the accepted analysis." in html
        assert "1 matching qualifications state explicit depth." in html
        assert "they are not similarity, readiness, or demand scores." in html
        assert 'href="#comparison-job-1"' in html
        assert 'id="comparison-job-1"' in html
        assert 'href="#comparison-job-2"' in html
        assert 'id="comparison-job-2"' in html
        no_match = client.get("/compare?job=direct&q=java")
        assert "No wording match does not establish no demand." in no_match.text
        assert "Other duties exist; none matches this wording." in no_match.text
        assert 'id="comparison-overview"' not in client.get("/compare").text
        assert _rows(settings) == before
