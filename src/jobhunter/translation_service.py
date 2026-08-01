"""Create idempotent English projections for parsed Jobinja versions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from jobhunter.translation import TranslationError, TranslationProvider
from jobhunter.translation.projection import (
    TRANSLATION_SCHEMA_VERSION,
    build_english_projection,
    collect_translatable_texts,
    translation_required,
)
from jobhunter.translation_store import (
    TranslationArtifact,
    TranslationSourceVersion,
    TranslationStore,
)


class TranslationSourceNotFoundError(LookupError):
    """Raised when a job has no parsed source version to translate."""


class TranslationProviderUnavailableError(RuntimeError):
    """Raised when Persian content needs a provider but none is configured."""


@dataclass(frozen=True, slots=True)
class TranslationJobResult:
    source_job_id: str
    job_detail_version_id: int
    artifact_id: int
    outcome: str
    provider_name: str
    provider_model: str
    translated_segment_count: int
    native_segment_count: int


@dataclass(frozen=True, slots=True)
class TranslationFailure:
    source_job_id: str
    error: str


@dataclass(frozen=True, slots=True)
class TranslationBatchSummary:
    attempted: int
    results: tuple[TranslationJobResult, ...]
    failures: tuple[TranslationFailure, ...]

    @property
    def completed(self) -> int:
        return sum(result.outcome == "completed" for result in self.results)

    @property
    def reused(self) -> int:
        return sum(result.outcome == "reused" for result in self.results)


class TranslationService:
    """Translate Persian/mixed source fields while preserving native English text."""

    def __init__(
        self,
        *,
        store: TranslationStore,
        provider: TranslationProvider | None,
        target_language: str = "en",
        clock=lambda: datetime.now(UTC),
    ) -> None:
        if target_language != "en":
            raise ValueError("The current English projection pipeline requires target_language='en'")
        self._store = store
        self._provider = provider
        self._target_language = target_language
        self._clock = clock

    def _provider_identity(
        self,
        source: TranslationSourceVersion,
    ) -> tuple[str, str]:
        if not translation_required(source.fields):
            return "source-identity", "native-english"
        if self._provider is None:
            raise TranslationProviderUnavailableError(
                "Persian or mixed content requires a configured translation provider"
            )
        return self._provider.name, self._provider.model

    def _existing_artifact(
        self,
        source: TranslationSourceVersion,
        *,
        provider_name: str,
        provider_model: str,
    ) -> TranslationArtifact | None:
        return self._store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            target_language=self._target_language,
            provider_name=provider_name,
            provider_model=provider_model,
            translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        )

    def _translate_source(self, source: TranslationSourceVersion) -> TranslationJobResult:
        provider_name, provider_model = self._provider_identity(source)
        attempted_at = self._clock()
        existing = self._existing_artifact(
            source,
            provider_name=provider_name,
            provider_model=provider_model,
        )
        if existing is not None:
            self._store.record_attempt(
                source=source,
                attempted_at=attempted_at,
                target_language=self._target_language,
                provider_name=provider_name,
                provider_model=provider_model,
                translation_schema_version=TRANSLATION_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return TranslationJobResult(
                source_job_id=source.source_job_id,
                job_detail_version_id=source.job_detail_version_id,
                artifact_id=existing.id,
                outcome="reused",
                provider_name=provider_name,
                provider_model=provider_model,
                translated_segment_count=existing.translated_segment_count,
                native_segment_count=existing.native_segment_count,
            )

        try:
            translations: dict[str, str] = {}
            texts = collect_translatable_texts(source.fields)
            if texts:
                if self._provider is None:
                    raise TranslationProviderUnavailableError(
                        "A translation provider is required for Persian content"
                    )
                translated = self._provider.translate_texts(
                    texts,
                    source_language="fa",
                    target_language=self._target_language,
                )
                if len(translated.texts) != len(texts):
                    raise TranslationError(
                        "Translation provider returned a mismatched result count"
                    )
                translations = dict(zip(texts, translated.texts, strict=True))

            projection = build_english_projection(
                source.fields,
                translations=translations,
            )
            artifact_id = self._store.record_artifact(
                source=source,
                target_language=self._target_language,
                provider_name=provider_name,
                provider_model=provider_model,
                translation_schema_version=TRANSLATION_SCHEMA_VERSION,
                fields=projection.fields,
                english_document=projection.document,
                segment_provenance=projection.segment_provenance,
                translated_segment_count=projection.translated_segment_count,
                native_segment_count=projection.native_segment_count,
                translation_sha256=projection.projection_sha256,
                created_at=attempted_at,
            )
            self._store.record_attempt(
                source=source,
                attempted_at=attempted_at,
                target_language=self._target_language,
                provider_name=provider_name,
                provider_model=provider_model,
                translation_schema_version=TRANSLATION_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
            return TranslationJobResult(
                source_job_id=source.source_job_id,
                job_detail_version_id=source.job_detail_version_id,
                artifact_id=artifact_id,
                outcome="completed",
                provider_name=provider_name,
                provider_model=provider_model,
                translated_segment_count=projection.translated_segment_count,
                native_segment_count=projection.native_segment_count,
            )
        except Exception as exc:
            self._store.record_attempt(
                source=source,
                attempted_at=attempted_at,
                target_language=self._target_language,
                provider_name=provider_name,
                provider_model=provider_model,
                translation_schema_version=TRANSLATION_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

    def translate_job(self, source_job_id: str) -> TranslationJobResult:
        """Create or reuse the English artifact for one job's latest source version."""

        source = self._store.latest_source_version(source_job_id)
        if source is None:
            raise TranslationSourceNotFoundError(
                f"Job {source_job_id!r} has no local parsed detail version"
            )
        return self._translate_source(source)

    def missing_source_versions(
        self,
        *,
        limit: int,
        preferred_ids: tuple[str, ...] = (),
    ) -> tuple[TranslationSourceVersion, ...]:
        """Return latest source versions missing the effective English artifact."""

        if not 1 <= limit <= 50:
            raise ValueError("translation limit must be between 1 and 50")
        sources = list(self._store.latest_source_versions(limit=5000))
        preferred_rank = {job_id: index for index, job_id in enumerate(preferred_ids)}
        sources.sort(
            key=lambda source: (
                0 if source.source_job_id in preferred_rank else 1,
                preferred_rank.get(source.source_job_id, source.job_detail_version_id),
                source.job_detail_version_id,
            )
        )
        selected: list[TranslationSourceVersion] = []
        for source in sources:
            try:
                provider_name, provider_model = self._provider_identity(source)
            except TranslationProviderUnavailableError:
                provider_name = "unavailable"
                provider_model = "unavailable"
            artifact = self._store.find_artifact(
                job_detail_version_id=source.job_detail_version_id,
                target_language=self._target_language,
                provider_name=provider_name,
                provider_model=provider_model,
                translation_schema_version=TRANSLATION_SCHEMA_VERSION,
            )
            if artifact is not None:
                continue
            selected.append(source)
            if len(selected) >= limit:
                break
        return tuple(selected)

    def run(
        self,
        *,
        source_job_ids: tuple[str, ...] = (),
        missing: bool = False,
        limit: int = 20,
        preferred_ids: tuple[str, ...] = (),
    ) -> TranslationBatchSummary:
        """Translate an explicit set or a bounded missing-artifact queue."""

        if source_job_ids and missing:
            raise ValueError("Choose explicit job IDs or missing translation selection, not both")
        if not 1 <= limit <= 50:
            raise ValueError("translation limit must be between 1 and 50")

        if source_job_ids:
            job_ids = tuple(dict.fromkeys(source_job_ids))
            if len(job_ids) > 50:
                raise ValueError("At most 50 explicit jobs may be translated per batch")
        else:
            sources = self.missing_source_versions(
                limit=limit,
                preferred_ids=preferred_ids,
            )
            job_ids = tuple(source.source_job_id for source in sources)

        results: list[TranslationJobResult] = []
        failures: list[TranslationFailure] = []
        for source_job_id in job_ids:
            try:
                results.append(self.translate_job(source_job_id))
            except Exception as exc:
                failures.append(
                    TranslationFailure(source_job_id=source_job_id, error=str(exc))
                )
        return TranslationBatchSummary(
            attempted=len(job_ids),
            results=tuple(results),
            failures=tuple(failures),
        )


def format_translation_batch_summary(summary: TranslationBatchSummary) -> str:
    lines = [
        "English translation projection batch",
        f"Attempted: {summary.attempted}",
        f"Completed: {summary.completed}",
        f"Reused: {summary.reused}",
        f"Failures: {len(summary.failures)}",
    ]
    if summary.results:
        lines.append("Results:")
        for result in summary.results:
            lines.append(
                f"- {result.source_job_id}: {result.outcome}, artifact {result.artifact_id}, "
                f"provider={result.provider_name}/{result.provider_model}, "
                f"translated={result.translated_segment_count}, "
                f"native={result.native_segment_count}"
            )
    if summary.failures:
        lines.append("Failures:")
        lines.extend(
            f"- {failure.source_job_id}: {failure.error}"
            for failure in summary.failures
        )
    return "\n".join(lines)


def format_translation_artifact(artifact: TranslationArtifact) -> str:
    return "\n".join(
        [
            f"English projection: {artifact.source_job_id}",
            f"Source semantic version: {artifact.job_detail_version_id}",
            f"Source language: {artifact.source_language}",
            f"Provider: {artifact.provider_name}",
            f"Model: {artifact.provider_model}",
            f"Schema: {artifact.translation_schema_version}",
            f"Translated segments: {artifact.translated_segment_count}",
            f"Native segments: {artifact.native_segment_count}",
            f"Projection SHA-256: {artifact.translation_sha256}",
            f"Created at: {artifact.created_at}",
            "",
            artifact.english_document,
        ]
    )
