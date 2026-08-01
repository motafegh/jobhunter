from datetime import UTC, datetime, timedelta
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.base import TranslationBatchResult
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


class _Provider:
    name = "test-provider"
    model = "test-model-v1"

    def __init__(self) -> None:
        self.calls: list[tuple[str, ...]] = []

    def translate_texts(self, texts, *, source_language, target_language):
        assert source_language == "fa"
        assert target_language == "en"
        self.calls.append(tuple(texts))
        mapping = {
            "مهندس هوش مصنوعی": "Artificial Intelligence Engineer",
            "تهران": "Tehran",
            "تسلط بر Python": "Proficiency in Python",
            "مهندس ارشد هوش مصنوعی": "Senior Artificial Intelligence Engineer",
        }
        return TranslationBatchResult(
            texts=tuple(mapping[text] for text in texts),
            detected_languages=tuple("fa" for _ in texts),
        )


def _add_version(
    database_path: Path,
    *,
    job_id: str,
    fields: dict,
    semantic_sha256: str,
    fetched_at: datetime,
) -> int:
    store = JobHunterStore(database_path)
    store.initialize()
    job = store.get_job(job_id)
    if job is None:
        upserted = store.upsert_job(
            job=DiscoveredJobLink(
                source_job_id=job_id,
                company_slug="acme",
                canonical_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
                observed_text=str(fields.get("title") or "job"),
            ),
            observed_at=fetched_at,
        )
        posting_id = upserted.job_posting_id
    else:
        posting_id = job.id
    result = store.record_job_detail(
        job_posting_id=posting_id,
        fetched_at=fetched_at,
        requested_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        final_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        status_code=200,
        content_sha256=f"raw-{semantic_sha256}",
        semantic_sha256=semantic_sha256,
        evidence_path=Path(f"{job_id}-{semantic_sha256}.html"),
        metadata_path=Path(f"{job_id}-{semantic_sha256}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields=fields,
    )
    return result.version_id


def test_translates_persian_and_reuses_same_artifact(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _add_version(
        database_path,
        job_id="abc1",
        fields={
            "title": "مهندس هوش مصنوعی",
            "location": "تهران",
            "skills": ["Python"],
            "description": "تسلط بر Python",
            "language": "mixed",
            "parser_version": "jobinja-detail-v2",
        },
        semantic_sha256="semantic-1",
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    provider = _Provider()
    service = TranslationService(
        store=TranslationStore(database_path),
        provider=provider,
        clock=lambda: datetime(2026, 8, 1, 1, tzinfo=UTC),
    )

    first = service.translate_job("abc1")
    second = service.translate_job("abc1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert second.artifact_id == first.artifact_id
    assert len(provider.calls) == 1
    artifact = TranslationStore(database_path).latest_artifact("abc1")
    assert artifact is not None
    assert artifact.fields["title"] == "Artificial Intelligence Engineer"
    assert artifact.fields["skills"] == ["Python"]
    assert artifact.segment_provenance["skills[0]"] == "native"


def test_native_english_creates_identity_artifact_without_provider(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _add_version(
        database_path,
        job_id="eng1",
        fields={
            "title": "Security Engineer",
            "skills": ["Python", "SIEM"],
            "description": "Build detection automation.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
        semantic_sha256="english-1",
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    service = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    )

    result = service.translate_job("eng1")

    assert result.outcome == "completed"
    assert result.provider_name == "source-identity"
    assert result.translated_segment_count == 0


def test_new_semantic_version_requires_new_translation_artifact(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    base_time = datetime(2026, 8, 1, tzinfo=UTC)
    _add_version(
        database_path,
        job_id="abc1",
        fields={
            "title": "مهندس هوش مصنوعی",
            "description": "تسلط بر Python",
            "language": "mixed",
            "parser_version": "jobinja-detail-v2",
        },
        semantic_sha256="semantic-1",
        fetched_at=base_time,
    )
    provider = _Provider()
    service = TranslationService(
        store=TranslationStore(database_path),
        provider=provider,
    )
    first = service.translate_job("abc1")

    second_version_id = _add_version(
        database_path,
        job_id="abc1",
        fields={
            "title": "مهندس ارشد هوش مصنوعی",
            "description": "تسلط بر Python",
            "language": "mixed",
            "parser_version": "jobinja-detail-v2",
        },
        semantic_sha256="semantic-2",
        fetched_at=base_time + timedelta(hours=1),
    )
    assert TranslationStore(database_path).latest_artifact("abc1") is None

    second = service.translate_job("abc1")

    assert second.outcome == "completed"
    assert second.job_detail_version_id == second_version_id
    assert second.artifact_id != first.artifact_id
    assert len(provider.calls) == 2
