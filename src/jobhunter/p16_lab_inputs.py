"""Read-only exact frozen case binding for all planned P1.6 cells.

No current-store lookup, source acquisition, model dispatch or review promotion.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.p16_lab import ROOT, SNAPSHOTS, checked_path, digest, file_digest, load_requirements
from jobhunter.p16_lab_a0 import PRIVATE_SOURCES
from jobhunter.translation_store import (
    TranslationArtifact,
    TranslationSourceVersion,
    _artifact_from_row,
)


@dataclass(frozen=True, slots=True)
class BoundCase:
    alias: str
    snapshot_group: str
    snapshot_sha256: str
    selection_sha256: str
    source: TranslationSourceVersion
    projection: TranslationArtifact
    original_html_sha256: str
    raw_html: bytes


def projection_digest(artifact: TranslationArtifact) -> str:
    return digest(
        json.dumps(
            {
                "fields": artifact.fields,
                "segment_provenance": artifact.segment_provenance,
                "schema": artifact.translation_schema_version,
            },
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode()
    )


def verify_projection(source: TranslationSourceVersion, projection: TranslationArtifact):
    if (
        projection.id <= 0
        or projection.source_job_id != source.source_job_id
        or projection.job_detail_version_id != source.job_detail_version_id
        or projection.source_semantic_sha256 != source.semantic_sha256
        or projection.target_language != "en"
        or projection.translation_schema_version != "english-projection-v2"
        or projection_digest(projection) != projection.translation_sha256
    ):
        raise ValueError("frozen projection identity/content mismatch")


def _closed_snapshot(path: Path, expected: str):
    if not path.is_file() or file_digest(path) != expected:
        raise ValueError("frozen snapshot mismatch")
    for suffix in ("-wal", "-journal"):
        sidecar = Path(str(path) + suffix)
        if sidecar.is_symlink() or (sidecar.exists() and sidecar.stat().st_size):
            raise ValueError("snapshot has active sidecar")


def bind_case(alias: str, root: Path = ROOT) -> BoundCase:
    freeze, protocol = load_requirements(root)
    selection = checked_path(root, PRIVATE_SOURCES)
    raw = selection.read_bytes()
    selection_hash = digest(raw)
    if selection_hash != freeze["private_source_manifest_sha256"]:
        raise ValueError("frozen source selection mismatch")
    private = json.loads(raw)
    matches = [c for c in protocol["cases"] if c["alias"] == alias]
    if len(matches) != 1:
        raise ValueError("unknown frozen case")
    case = matches[0]
    group = case["snapshot"]
    expected = [
        r
        for r in private["sources"]
        if r["case"] == case["retained_id"] and r["source_group"] == group
    ]
    if len(expected) != 1 or private["snapshot_sha256"] != freeze["frozen_snapshot_sha256"]:
        raise ValueError("ambiguous frozen case mapping")
    row = expected[0]
    dbpath = checked_path(root, SNAPSHOTS[group])
    snapshot_sha = freeze["frozen_snapshot_sha256"][group]
    _closed_snapshot(dbpath, snapshot_sha)
    with closing(sqlite3.connect(dbpath.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA query_only=ON")
        v = db.execute(
            """SELECT v.*,p.source_job_id,p.source FROM job_detail_versions v
               JOIN job_postings p ON p.id=v.job_posting_id WHERE v.id=?""",
            (row["source_version"],),
        ).fetchone()
        if (
            v is None
            or v["source_job_id"] != row["case"]
            or v["source"] != "jobinja"
            or v["parse_status"] != "parsed"
            or v["semantic_sha256"] != row["source_semantic_sha256"]
            or v["content_sha256"] != row["original_html_sha256"]
        ):
            raise ValueError("frozen source row mismatch")
        fields = json.loads(v["fields_json"])
        description = fields["description"]
        if (
            _semantic_sha256(fields) != v["semantic_sha256"]
            or digest(description.encode()) != row["original_description_sha256"]
            or len(description) != case["description_chars"]
            or fields.get("language") != row["source_language"]
        ):
            raise ValueError("frozen source content mismatch")
        source = TranslationSourceVersion(
            row["case"], v["id"], v["semantic_sha256"], row["source_language"], fields
        )
        t = db.execute(
            """SELECT t.*,p.source_job_id FROM job_translation_artifacts t
               JOIN job_detail_versions v ON v.id=t.job_detail_version_id
               JOIN job_postings p ON p.id=v.job_posting_id WHERE t.id=?""",
            (row["translation_id"],),
        ).fetchone()
        if t is None:
            raise ValueError("frozen translation missing")
        projection = _artifact_from_row(t)
        verify_projection(source, projection)
        english = projection.fields["description"]
        if (
            projection.translation_sha256 != row["translation_sha256"]
            or projection.provider_model != row["translation_model"]
            or len(english) != case["english_chars"]
            or (english == description) != case["native_description_identity"]
        ):
            raise ValueError("frozen projection differs")
        if group == "nov23":
            evidence = Path(v["evidence_path"])
            rel = evidence.relative_to(root) if evidence.is_absolute() else evidence
            if not rel.is_relative_to(Path(SNAPSHOTS[group]).parent / "evidence"):
                raise ValueError("unapproved original evidence path")
        else:
            rel = (
                Path(SNAPSHOTS[group]).parent
                / "evidence"
                / (group + "_" + row["case"] + "_raw_html.html")
            )
        html = checked_path(root, str(rel)).read_bytes()
        if digest(html) != row["original_html_sha256"]:
            raise ValueError("frozen original HTML differs")
    _closed_snapshot(dbpath, snapshot_sha)
    if file_digest(selection) != selection_hash:
        raise ValueError("selection changed during binding")
    return BoundCase(
        alias,
        group,
        snapshot_sha,
        selection_hash,
        source,
        projection,
        row["original_html_sha256"],
        html,
    )


def bind_cell(cell_id: str, root: Path = ROOT) -> tuple[dict, BoundCase]:
    _, protocol = load_requirements(root)
    cells = [c for c in protocol["cells"] if c["cell_id"] == cell_id]
    if len(cells) != 1:
        raise ValueError("unknown frozen schedule cell")
    cell = cells[0]
    if cell["architecture"] in {"A0", "A1"} and cell["language"] != "L0":
        raise ValueError("incumbent representation mismatch")
    return cell, bind_case(cell["case"], root)
