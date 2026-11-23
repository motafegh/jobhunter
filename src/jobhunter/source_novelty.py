"""Read-only exact original-description novelty gate across source versions.

Jobinja job IDs are not unique content identities. An employer can reissue the
same source description under a new ID. This utility is for provenance-aware
selection/audit, not automatically suppressing real listed jobs in the catalog.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceDescriptionIdentity:
    source_job_id: str
    source_version_id: int
    original_description_sha256: str
    database: str


@dataclass(frozen=True, slots=True)
class SourceNoveltyCheck:
    candidate: SourceDescriptionIdentity
    exact_description_found_in_archive: bool
    archived_matching_job_ids: tuple[str, ...]
    duplicate_under_different_job_id: bool
    archived_source_version_matches: int


def _original_version_fingerprints(
    database_path: Path, *, limit: int = 20000
) -> tuple[SourceDescriptionIdentity, ...]:
    """Never open a writable SQLite connection when inspecting old source data."""
    if not database_path.is_file():
        raise FileNotFoundError(f"Archived source database unavailable: {database_path}")
    records: list[SourceDescriptionIdentity] = []
    with sqlite3.connect(f"file:{database_path.resolve()}?mode=ro", uri=True) as conn:
        rows = conn.execute(
            "SELECT p.source_job_id, v.id, v.fields_json "
            "FROM job_detail_versions AS v JOIN job_postings AS p "
            "ON p.id = v.job_posting_id "
            "WHERE v.parse_status = 'parsed' ORDER BY v.id"
        )
        for jid, version_id, fields_json in rows:
            if len(records) >= limit:
                raise ValueError(
                    "Source novelty scan exceeds configured bound; cannot certify novelty"
                )
            fields = json.loads(fields_json)
            desc = fields.get("description")
            if not isinstance(desc, str) or not desc.strip():
                continue
            records.append(
                SourceDescriptionIdentity(
                    source_job_id=str(jid),
                    source_version_id=int(version_id),
                    original_description_sha256=hashlib.sha256(desc.encode("utf-8")).hexdigest(),
                    database=database_path.name,
                )
            )
    return tuple(records)


def compare_exact_original_descriptions(
    candidate_db: Path,
    job_ids: Iterable[str],
    archive_dbs: Iterable[Path],
    *,
    max_source_versions_per_db: int = 20000,
) -> tuple[SourceNoveltyCheck, ...]:
    """Classify exact-description duplication, never claim independent novelty.

    A candidate without a match is merely distinct relative to the supplied
    archives, not proof it was newly posted or unseen on all of Jobinja.
    """
    candidates = tuple(dict.fromkeys(job_ids))
    if not candidates or any(not x or len(x) > 128 for x in candidates):
        raise ValueError("At least one concrete source job ID is required")
    archives = tuple(archive_dbs)
    if not archives:
        raise ValueError("At least one archived-source database is required")
    archive_index: dict[str, list[SourceDescriptionIdentity]] = defaultdict(list)
    for path in archives:
        for record in _original_version_fingerprints(path, limit=max_source_versions_per_db):
            archive_index[record.original_description_sha256].append(record)
    latest: dict[str, SourceDescriptionIdentity] = {}
    for record in _original_version_fingerprints(candidate_db, limit=max_source_versions_per_db):
        if record.source_job_id in candidates:
            latest[record.source_job_id] = record
    if set(latest) != set(candidates):
        raise ValueError(
            "A selected candidate lacks a parsed original description: "
            + ", ".join(sorted(set(candidates) - set(latest)))
        )
    results: list[SourceNoveltyCheck] = []
    for jid in candidates:
        candidate = latest[jid]
        matches = archive_index.get(candidate.original_description_sha256, ())
        matching_ids = tuple(sorted({x.source_job_id for x in matches}))
        results.append(
            SourceNoveltyCheck(
                candidate=candidate,
                exact_description_found_in_archive=bool(matches),
                archived_matching_job_ids=matching_ids,
                duplicate_under_different_job_id=any(x.source_job_id != jid for x in matches),
                archived_source_version_matches=len(matches),
            )
        )
    return tuple(results)


def novelty_report(
    candidate_db: Path,
    job_ids: Iterable[str],
    archive_dbs: Iterable[Path],
) -> dict:
    """Local-only diagnostic JSON contains source IDs, never employer text."""
    results = compare_exact_original_descriptions(candidate_db, job_ids, archive_dbs)
    return {
        "scope": "exact_original_description_only_against_supplied_archives",
        "independent_new_source_certified": False,
        "all_distinct_within_supplied_archives": all(
            not x.exact_description_found_in_archive for x in results
        ),
        "cases": [asdict(x) for x in results],
    }
