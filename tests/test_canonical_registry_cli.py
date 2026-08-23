from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.canonical_registry import (
    CanonicalRegistryStore,
    ConceptCategory,
    build_canonical_registry_service,
)
from jobhunter.canonical_registry_cli import (
    build_canonical_registry_review_reader,
    main,
)
from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 8, 23, 18, tzinfo=UTC)


def _settings(database_path: Path) -> Settings:
    return Settings(
        data_dir=database_path.parent,
        database_path=database_path,
        analysis_lm_studio_model="analysis-model",
    )


def _seed_accepted_analysis(database_path: Path, *, job_id: str = "registry-cli") -> None:
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


def test_review_reader_lists_exact_current_claims_and_mapping_state(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_accepted_analysis(database_path)
    settings = _settings(database_path)

    reader = build_canonical_registry_review_reader(settings)
    items = reader.list_current_claims(source_job_id="registry-cli")

    assert [(item.claim_kind, item.claim_index, item.mapping_state) for item in items] == [
        ("requirement", 0, "pending"),
        ("requirement", 1, "pending"),
        ("responsibility", 0, "pending"),
    ]
    assert items[0].source_text == "Python"
    assert items[0].concept_type == "language"
    assert items[0].strength == "required"
    assert items[0].depth_signal == "working"

    store = CanonicalRegistryStore(database_path)
    store.create_concept(
        concept_id="language:python",
        category=ConceptCategory.LANGUAGE,
        preferred_label="Python",
        description=None,
        reviewed_at=_NOW,
        review_note="Reviewed Python language concept",
    )
    build_canonical_registry_service(settings).record_current_claim_mapping(
        "registry-cli",
        claim_kind="requirement",
        claim_index=0,
        disposition="mapped",
        canonical_concept_id="language:python",
        reviewed_at=_NOW,
        review_note="Reviewed exact Python mapping",
    )

    mapped = reader.list_current_claims(mapping_state="mapped")
    assert len(mapped) == 1
    assert mapped[0].mapping is not None
    assert mapped[0].mapping.canonical_concept_id == "language:python"
    pending = reader.list_current_claims(mapping_state="pending")
    assert len(pending) == 2


def test_manual_registry_cli_reviews_concept_alias_and_deprecation(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    settings = _settings(database_path)
    monkeypatch.setattr(
        "jobhunter.canonical_registry_cli._load_settings",
        lambda _path: settings,
    )

    assert main(
        [
            "concepts",
            "add",
            "language:python",
            "--category",
            "language",
            "--label",
            "Python",
            "--reason",
            "Reviewed Python language concept",
        ]
    ) == 0
    assert main(
        [
            "aliases",
            "add",
            "language:python",
            "Python 3",
            "--provenance",
            "manual",
            "--reference",
            "review:python-3",
            "--reason",
            "Reviewed common Python alias",
        ]
    ) == 0
    capsys.readouterr()

    assert main(["concepts", "show", "language:python"]) == 0
    shown = capsys.readouterr().out
    assert "Preferred label: Python" in shown
    assert "Python 3 [active] manual: review:python-3" in shown

    assert main(
        [
            "concepts",
            "deprecate",
            "language:python",
            "--reason",
            "Reviewed concept deprecation without successor",
        ]
    ) == 0
    assert "Deprecated concept: language:python" in capsys.readouterr().out


def test_manual_registry_cli_lists_and_records_immutable_claim_decisions(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_accepted_analysis(database_path)
    settings = _settings(database_path)
    monkeypatch.setattr(
        "jobhunter.canonical_registry_cli._load_settings",
        lambda _path: settings,
    )
    store = CanonicalRegistryStore(database_path)
    store.create_concept(
        concept_id="language:python",
        category=ConceptCategory.LANGUAGE,
        preferred_label="Python",
        description=None,
        reviewed_at=_NOW,
        review_note="Reviewed Python language concept",
    )

    assert main(
        [
            "claims",
            "list",
            "--job-id",
            "registry-cli",
            "--state",
            "pending",
        ]
    ) == 0
    pending = capsys.readouterr().out
    assert "requirement[0] state=pending" in pending
    assert "Source: Python" in pending

    assert main(
        [
            "claims",
            "decide",
            "registry-cli",
            "requirement",
            "0",
            "mapped",
            "--concept",
            "language:python",
            "--reason",
            "Reviewed exact Python mapping",
        ]
    ) == 0
    assert "-> mapped" in capsys.readouterr().out

    assert main(
        [
            "claims",
            "list",
            "--job-id",
            "registry-cli",
            "--state",
            "mapped",
        ]
    ) == 0
    mapped = capsys.readouterr().out
    assert "Canonical: language:python" in mapped

    assert main(
        [
            "claims",
            "decide",
            "registry-cli",
            "requirement",
            "0",
            "unmapped",
            "--reason",
            "Attempted immutable decision rewrite",
        ]
    ) == 2
    error = capsys.readouterr().err
    assert "already has a reviewed mapping decision" in error


def test_manual_registry_cli_requires_concept_only_for_mapped_decisions(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    settings = _settings(tmp_path / "jobhunter.sqlite3")
    monkeypatch.setattr(
        "jobhunter.canonical_registry_cli._load_settings",
        lambda _path: settings,
    )

    assert main(
        [
            "claims",
            "decide",
            "missing-job",
            "requirement",
            "0",
            "mapped",
            "--reason",
            "Reviewed mapping without target",
        ]
    ) == 2
    assert "mapped disposition requires --concept" in capsys.readouterr().err
