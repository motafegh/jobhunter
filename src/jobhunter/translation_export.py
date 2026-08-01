"""Export derived English artifacts for analysis and machine-learning workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from jobhunter.translation_store import TranslationStore

EXPORT_SCHEMA_VERSION = "jobhunter-english-corpus-v1"


@dataclass(frozen=True, slots=True)
class TranslationExportResult:
    path: Path
    records: int


def export_english_corpus(
    store: TranslationStore,
    *,
    output_path: Path,
    limit: int = 500,
) -> TranslationExportResult:
    """Write the latest English artifact per job as UTF-8 JSON Lines."""

    artifacts = store.list_latest_artifacts(target_language="en", limit=limit)
    selected_path = output_path.expanduser()
    selected_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = selected_path.with_name(f".{selected_path.name}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            for artifact in artifacts:
                record = {
                    "schema_version": EXPORT_SCHEMA_VERSION,
                    "source": "jobinja",
                    "source_job_id": artifact.source_job_id,
                    "source_detail_version_id": artifact.job_detail_version_id,
                    "source_semantic_sha256": artifact.source_semantic_sha256,
                    "source_language": artifact.source_language,
                    "target_language": artifact.target_language,
                    "english_origin": (
                        "native"
                        if artifact.provider_name == "source-identity"
                        else "translated_or_mixed"
                    ),
                    "translation": {
                        "artifact_id": artifact.id,
                        "provider": artifact.provider_name,
                        "model": artifact.provider_model,
                        "schema_version": artifact.translation_schema_version,
                        "created_at": artifact.created_at,
                        "sha256": artifact.translation_sha256,
                        "translated_segment_count": artifact.translated_segment_count,
                        "native_segment_count": artifact.native_segment_count,
                    },
                    "segment_provenance": artifact.segment_provenance,
                    "english_fields": artifact.fields,
                    "english_document": artifact.english_document,
                }
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
                handle.write("\n")
        temporary.replace(selected_path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise
    return TranslationExportResult(path=selected_path, records=len(artifacts))
