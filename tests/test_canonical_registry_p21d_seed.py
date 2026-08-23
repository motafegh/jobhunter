from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.canonical_registry import CanonicalRegistryStore
from jobhunter.canonical_registry_cli import main
from jobhunter.canonical_registry_review import build_canonical_registry_review_reader
from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.launcher import build_runtime_app

_NOW = datetime(2026, 8, 23, 19, tzinfo=UTC)

_CONCEPT_COMMANDS = (
    (
        "concepts",
        "add",
        "platform:linux",
        "--category",
        "platform",
        "--label",
        "Linux",
        "--reason",
        "Reviewed from accepted P1.6 artifact 36 requirement[12] and artifact 39 "
        "requirement[3]; shared Linux platform identity without source-specific depth.",
    ),
    (
        "concepts",
        "add",
        "tool:powershell",
        "--category",
        "tool",
        "--label",
        "PowerShell",
        "--reason",
        "Reviewed from accepted P1.6 artifact 46 requirement[11] as the canonical "
        "PowerShell tool identity.",
    ),
    (
        "concepts",
        "add",
        "education_credential:ccnp-security",
        "--category",
        "education_credential",
        "--label",
        "CCNP Security",
        "--reason",
        "Reviewed from accepted P1.6 artifact 44 requirement[4], explicitly classified "
        "as a preferred certification/education claim.",
    ),
    (
        "concepts",
        "add",
        "responsibility:manage-next-generation-firewalls",
        "--category",
        "responsibility",
        "--label",
        "Manage next-generation firewalls",
        "--reason",
        "Reviewed from accepted P1.6 artifact 44 responsibility[1]; grammatical "
        "normalization only, with exact source wording retained by the mapping.",
    ),
)

_ALIAS_COMMAND = (
    "aliases",
    "add",
    "platform:linux",
    "Linux operating system",
    "--provenance",
    "accepted_p16_claim",
    "--reference",
    "job=tmBK;analysis_artifact=39;claim=requirement[3]",
    "--reason",
    "Exact accepted tmBK P1.6 concept wording reviewed as an alias of Linux; "
    "Familiarity remains source depth rather than canonical identity.",
)

_DECISION_COMMANDS = (
    (
        "claims",
        "decide",
        "tG9K",
        "requirement",
        "12",
        "mapped",
        "--concept",
        "platform:linux",
        "--reason",
        "Exact accepted P1.6 Linux requirement corresponds to the reviewed Linux "
        "platform concept.",
    ),
    (
        "claims",
        "decide",
        "tmBK",
        "requirement",
        "3",
        "mapped",
        "--concept",
        "platform:linux",
        "--reason",
        "Exact accepted P1.6 Linux operating system requirement corresponds to Linux; "
        "Familiarity remains source depth.",
    ),
    (
        "claims",
        "decide",
        "t4jp",
        "requirement",
        "4",
        "unmapped",
        "--reason",
        "Trait-like creativity requirement has no appropriate current canonical "
        "category; preserve it unmapped rather than forcing a skill/knowledge "
        "classification.",
    ),
    (
        "claims",
        "decide",
        "t4qV",
        "requirement",
        "4",
        "mapped",
        "--concept",
        "education_credential:ccnp-security",
        "--reason",
        "Exact accepted P1.6 CCNP Security certification corresponds to the reviewed "
        "credential; preferred strength remains source metadata.",
    ),
    (
        "claims",
        "decide",
        "t4qV",
        "responsibility",
        "1",
        "mapped",
        "--concept",
        "responsibility:manage-next-generation-firewalls",
        "--reason",
        "Exact accepted responsibility Managing next-generation firewalls corresponds "
        "to the reviewed responsibility concept without added scope.",
    ),
    (
        "claims",
        "decide",
        "tmyX",
        "requirement",
        "11",
        "mapped",
        "--concept",
        "tool:powershell",
        "--reason",
        "Exact accepted P1.6 PowerShell structured requirement corresponds to the "
        "reviewed PowerShell tool concept.",
    ),
)

_EXPECTED_DECISIONS = (
    ("tG9K", "requirement", 12, "mapped", "platform:linux"),
    ("tmBK", "requirement", 3, "mapped", "platform:linux"),
    ("t4jp", "requirement", 4, "unmapped", None),
    (
        "t4qV",
        "requirement",
        4,
        "mapped",
        "education_credential:ccnp-security",
    ),
    (
        "t4qV",
        "responsibility",
        1,
        "mapped",
        "responsibility:manage-next-generation-firewalls",
    ),
    ("tmyX", "requirement", 11, "mapped", "tool:powershell"),
)


def _settings(database_path: Path) -> Settings:
    return Settings(
        data_dir=database_path.parent,
        evidence_dir=database_path.parent / "evidence",
        database_path=database_path,
        analysis_lm_studio_model="analysis-model",
        translation_enabled=False,
    )


def _claims_with_target(
    *,
    job_id: str,
    target_index: int,
    target: dict[str, str | None],
    source_key: str,
) -> list[dict[str, str | None]]:
    values: list[dict[str, str | None]] = []
    for index in range(target_index + 1):
        text = f"Disposable placeholder {job_id} {source_key} {index}"
        values.append(
            {
                source_key: text,
                "concept_type": "context",
                "evidence": text,
            }
        )
    values[target_index] = target
    return values


def _seed_job(
    database_path: Path,
    *,
    job_id: str,
    requirements: list[dict[str, str | None]],
    responsibilities: list[dict[str, str | None]],
) -> tuple[int, int]:
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="p21d-disposable",
            canonical_url=(
                f"https://jobinja.ir/companies/p21d-disposable/jobs/{job_id}/role"
            ),
            observed_text=f"Disposable {job_id}",
        ),
        observed_at=_NOW,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW,
        requested_url=(
            f"https://jobinja.ir/companies/p21d-disposable/jobs/{job_id}/role"
        ),
        final_url=f"https://jobinja.ir/companies/p21d-disposable/jobs/{job_id}/role",
        status_code=200,
        content_sha256=f"content-{job_id}-v1",
        semantic_sha256=f"semantic-{job_id}-v1",
        evidence_path=Path(f"{job_id}-v1.html"),
        metadata_path=Path(f"{job_id}-v1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": f"Disposable {job_id}",
            "description": f"Disposable accepted source for {job_id}.",
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job(job_id)
    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "requirements": requirements,
            "responsibilities": responsibilities,
        },
        request_body={},
        raw_response={},
        created_at=_NOW,
        semantic_review_status="accepted",
    )
    return analysis_id, posting.job_posting_id


def _seed_approved_claim_shapes(database_path: Path) -> dict[str, tuple[int, int]]:
    return {
        "tG9K": _seed_job(
            database_path,
            job_id="tG9K",
            requirements=_claims_with_target(
                job_id="tG9K",
                target_index=12,
                target={
                    "concept": "Linux",
                    "concept_type": "tool",
                    "evidence": "Linux",
                },
                source_key="concept",
            ),
            responsibilities=[],
        ),
        "tmBK": _seed_job(
            database_path,
            job_id="tmBK",
            requirements=_claims_with_target(
                job_id="tmBK",
                target_index=3,
                target={
                    "concept": "Linux operating system",
                    "concept_type": "tool",
                    "evidence": "Familiarity with Linux operating system",
                    "depth_signal": "Familiarity",
                },
                source_key="concept",
            ),
            responsibilities=[],
        ),
        "t4jp": _seed_job(
            database_path,
            job_id="t4jp",
            requirements=_claims_with_target(
                job_id="t4jp",
                target_index=4,
                target={
                    "concept": "Creativity in creating visual and video content",
                    "concept_type": "other",
                    "evidence": "creativity in creating visual and video content",
                },
                source_key="concept",
            ),
            responsibilities=[],
        ),
        "t4qV": _seed_job(
            database_path,
            job_id="t4qV",
            requirements=_claims_with_target(
                job_id="t4qV",
                target_index=4,
                target={
                    "concept": "CCNP Security",
                    "concept_type": "education",
                    "evidence": "CCNP Security",
                    "requirement_strength": "preferred",
                },
                source_key="concept",
            ),
            responsibilities=_claims_with_target(
                job_id="t4qV",
                target_index=1,
                target={
                    "statement": "Managing next-generation firewalls",
                    "evidence": (
                        "designing and executing security solutions, managing "
                        "next-generation firewalls, and implementing security policies."
                    ),
                },
                source_key="statement",
            ),
        ),
        "tmyX": _seed_job(
            database_path,
            job_id="tmyX",
            requirements=_claims_with_target(
                job_id="tmyX",
                target_index=11,
                target={
                    "concept": "PowerShell",
                    "concept_type": "skill",
                    "evidence": "PowerShell",
                },
                source_key="concept",
            ),
            responsibilities=[],
        ),
    }


def _apply_approved_seed() -> None:
    for command in _CONCEPT_COMMANDS:
        assert main(command) == 0
    assert main(_ALIAS_COMMAND) == 0
    for command in _DECISION_COMMANDS:
        assert main(command) == 0


def _decision_ids(
    settings: Settings,
    artifact_ids: dict[str, int],
) -> dict[tuple[str, str, int], int]:
    reader = build_canonical_registry_review_reader(settings)
    result: dict[tuple[str, str, int], int] = {}
    for job_id, kind, index, disposition, concept_id in _EXPECTED_DECISIONS:
        mapping = reader.mapping_for_claim(
            analysis_artifact_id=artifact_ids[job_id],
            claim_kind=kind,
            claim_index=index,
        )
        assert mapping is not None
        assert mapping.disposition == disposition
        assert mapping.canonical_concept_id == concept_id
        result[(job_id, kind, index)] = mapping.id
    return result


def test_approved_p21d_seed_is_idempotent_current_and_visible_across_surfaces(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    seeded = _seed_approved_claim_shapes(database_path)
    artifact_ids = {job_id: value[0] for job_id, value in seeded.items()}
    settings = _settings(database_path)
    monkeypatch.setattr(
        "jobhunter.canonical_registry_cli._load_settings",
        lambda _path: settings,
    )

    _apply_approved_seed()
    capsys.readouterr()

    store = CanonicalRegistryStore(database_path)
    assert [concept.concept_id for concept in store.list_concepts()] == [
        "education_credential:ccnp-security",
        "platform:linux",
        "responsibility:manage-next-generation-firewalls",
        "tool:powershell",
    ]
    reader = build_canonical_registry_review_reader(settings)
    aliases = reader.aliases_for_concept("platform:linux")
    assert len(aliases) == 1
    assert aliases[0].alias_text == "Linux operating system"
    assert aliases[0].provenance_kind == "accepted_p16_claim"
    assert (
        aliases[0].provenance_reference
        == "job=tmBK;analysis_artifact=39;claim=requirement[3]"
    )
    first_decision_ids = _decision_ids(settings, artifact_ids)
    first_alias_id = aliases[0].id

    _apply_approved_seed()
    capsys.readouterr()

    assert len(store.list_concepts()) == 4
    aliases_after_rerun = reader.aliases_for_concept("platform:linux")
    assert len(aliases_after_rerun) == 1
    assert aliases_after_rerun[0].id == first_alias_id
    assert _decision_ids(settings, artifact_ids) == first_decision_ids

    assert main(["claims", "list", "--state", "mapped"]) == 0
    cli_mapped = capsys.readouterr().out
    for expected in (
        "Source: Linux",
        "Canonical: platform:linux",
        "Source: Linux operating system",
        "Source: CCNP Security",
        "Canonical: education_credential:ccnp-security",
        "Source: Managing next-generation firewalls",
        "Canonical: responsibility:manage-next-generation-firewalls",
        "Source: PowerShell",
        "Canonical: tool:powershell",
    ):
        assert expected in cli_mapped

    assert main(["claims", "list", "--state", "unmapped"]) == 0
    cli_unmapped = capsys.readouterr().out
    assert "Source: Creativity in creating visual and video content" in cli_unmapped
    assert "state=unmapped" in cli_unmapped

    app = build_runtime_app(settings)
    with TestClient(app) as client:
        browser_mapped = client.get("/registry/claims", params={"state": "mapped"})
        browser_unmapped = client.get("/registry/claims", params={"state": "unmapped"})
        linux_detail = client.get("/registry/concepts/platform:linux")

    assert browser_mapped.status_code == 200
    assert browser_unmapped.status_code == 200
    assert linux_detail.status_code == 200
    for expected in (
        "Linux",
        "Linux operating system",
        "CCNP Security",
        "Managing next-generation firewalls",
        "PowerShell",
    ):
        assert expected in browser_mapped.text
    assert "Creativity in creating visual and video content" in browser_unmapped.text
    assert "Linux operating system" in linux_detail.text
    assert "job=tmBK;analysis_artifact=39;claim=requirement[3]" in linux_detail.text
    assert "tG9K" in linux_detail.text
    assert "tmBK" in linux_detail.text
    assert linux_detail.text.count(">current<") >= 2


def test_approved_p21d_seed_mapping_history_survives_stale_p16_dependency(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    seeded = _seed_approved_claim_shapes(database_path)
    artifact_ids = {job_id: value[0] for job_id, value in seeded.items()}
    settings = _settings(database_path)
    monkeypatch.setattr(
        "jobhunter.canonical_registry_cli._load_settings",
        lambda _path: settings,
    )
    _apply_approved_seed()
    capsys.readouterr()

    reader = build_canonical_registry_review_reader(settings)
    original = reader.mapping_for_claim(
        analysis_artifact_id=artifact_ids["tG9K"],
        claim_kind="requirement",
        claim_index=12,
    )
    assert original is not None

    source_store = JobHunterStore(database_path)
    posting_id = seeded["tG9K"][1]
    source_store.record_job_detail(
        job_posting_id=posting_id,
        fetched_at=_NOW + timedelta(minutes=1),
        requested_url="https://jobinja.ir/companies/p21d-disposable/jobs/tG9K/role",
        final_url="https://jobinja.ir/companies/p21d-disposable/jobs/tG9K/role",
        status_code=200,
        content_sha256="content-tG9K-v2",
        semantic_sha256="semantic-tG9K-v2",
        evidence_path=Path("tG9K-v2.html"),
        metadata_path=Path("tG9K-v2.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": "Disposable tG9K updated",
            "description": "Updated source makes the accepted v1 P1.6 chain stale.",
        },
    )
    TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job("tG9K")

    historical = reader.mapping_for_claim(
        analysis_artifact_id=artifact_ids["tG9K"],
        claim_kind="requirement",
        claim_index=12,
    )
    assert historical is not None
    assert historical.id == original.id
    assert historical.source_text == "Linux"

    linux_mappings = reader.concept_mappings("platform:linux")
    by_job = {item.mapping.source_job_id: item for item in linux_mappings}
    assert by_job["tG9K"].mapping.id == original.id
    assert by_job["tG9K"].current is False
    assert by_job["tmBK"].current is True

    assert main(
        ["claims", "list", "--job-id", "tG9K", "--state", "mapped"]
    ) == 0
    assert (
        "No accepted/current P1.6 claims matched the review filter."
        in capsys.readouterr().out
    )

    app = build_runtime_app(settings)
    with TestClient(app) as client:
        linux_detail = client.get("/registry/concepts/platform:linux")

    assert linux_detail.status_code == 200
    assert "tG9K" in linux_detail.text
    assert "tmBK" in linux_detail.text
    assert ">historical<" in linux_detail.text
    assert ">current<" in linux_detail.text
