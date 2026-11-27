"""Safe summary of independent R2/R3 and original-board R4 offline checks."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import asdict
from pathlib import Path

from verify_p16_a1_r1_replay import REPLAY, REPLAY_SHA, outcome

from jobhunter.evidence_refs_v21 import build_responsibility_coverage_plan_v21
from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)
from jobhunter.p16_lab import ROOT, SNAPSHOTS, checked_path, digest, file_digest, load_requirements
from jobhunter.p16_lab_a0 import PRIVATE_SOURCES
from jobhunter.p16_lab_a1_r4 import board_skill_observations, verify_board_observations
from jobhunter.p16_lab_a1_r23 import (
    AnalysisRequirementR2,
    JobAnalysisResponseR2,
    corrected_duty_plan,
)
from jobhunter.translation_store import TranslationSourceVersion


def verify(root: Path = ROOT) -> dict:
    freeze, _ = load_requirements(root)
    path = checked_path(root, REPLAY)
    assert file_digest(path) == REPLAY_SHA
    cases = json.loads(path.read_bytes())
    r2, r3 = [], []
    for case in cases:
        for row in case["replays"]:
            matches = row["replays"]
            assert len(matches) == 1
            ctx = case["captures"][matches[0]["partition"] - 1]["context"]
            raw = row["raw"]
            old, old_errors = outcome(JobAnalysisResponseV30, raw, ctx)
            new, new_errors = outcome(JobAnalysisResponseR2, raw, ctx)
            recovered = []
            for i, item in enumerate(raw["requirements"]):
                previous, _ = outcome(AnalysisRequirementV30, item, ctx)
                current, _ = outcome(AnalysisRequirementR2, item, ctx)
                if previous is None and current is not None:
                    assert current.depth_signal is None
                    assert current.concept == item["concept"]
                    assert current.requirement_type == item["requirement_type"]
                    recovered.append(i)
            r2.append(
                {
                    "diagnostic": row["diagnostic"],
                    "recovered": recovered,
                    "before_valid": old is not None,
                    "after_valid": new is not None,
                    "before_errors": old_errors,
                    "after_errors": new_errors,
                }
            )
            old_plan = build_responsibility_coverage_plan_v21(ctx["analysis_fields"])
            corrected, removed = corrected_duty_plan(ctx["analysis_fields"])
            # Compare planner output to the captured partition; duty coverage is
            # assigned only to the first partition in the actual provider.
            if matches[0]["partition"] != 1:
                assert not ctx["responsibility_coverage_plan"]
                continue
            assert old_plan == ctx["responsibility_coverage_plan"]
            if not removed:
                continue
            updated = {**ctx, "responsibility_coverage_plan": corrected}
            result, errors = outcome(JobAnalysisResponseV30, raw, updated)
            negative = None
            if result is not None:
                mutated = {**raw, "responsibilities": raw["responsibilities"][1:]}
                negative, _ = outcome(JobAnalysisResponseV30, mutated, updated)
                assert negative is None
            r3.append(
                {
                    "diagnostic": row["diagnostic"],
                    "before_duties": len(old_plan),
                    "after_duties": len(corrected),
                    "removed": list(removed),
                    "before_valid": old is not None,
                    "after_valid": result is not None,
                    "errors": errors,
                    "missing_genuine_duty_rejected": result is not None and negative is None,
                }
            )
    assert sum(len(r["recovered"]) for r in r2) == 2
    assert not any(r["after_valid"] for r in r2)
    assert sum(r["after_valid"] for r in r3) == 1
    assert sum(r["missing_genuine_duty_rejected"] for r in r3) == 1
    assert file_digest(path) == REPLAY_SHA
    selection = checked_path(root, PRIVATE_SOURCES)
    assert file_digest(selection) == freeze["private_source_manifest_sha256"]
    counts = []
    for group in SNAPSHOTS:
        dbpath = checked_path(root, SNAPSHOTS[group])
        assert file_digest(dbpath) == freeze["frozen_snapshot_sha256"][group]
        for suffix in ("-wal", "-journal"):
            sidecar = Path(str(dbpath) + suffix)
            assert not sidecar.is_symlink() and (not sidecar.exists() or not sidecar.stat().st_size)
        with closing(sqlite3.connect(dbpath.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
            for row in json.loads(selection.read_bytes())["sources"]:
                if row["source_group"] != group:
                    continue
                raw = db.execute(
                    "SELECT v.fields_json,v.semantic_sha256,p.source_job_id "
                    "FROM job_detail_versions v JOIN job_postings p ON p.id=v.job_posting_id "
                    "WHERE v.id=?",
                    (row["source_version"],),
                ).fetchone()
                assert raw and raw[1] == row["source_semantic_sha256"] and raw[2] == row["case"]
                fields = json.loads(raw[0])
                assert digest(fields["description"].encode()) == row["original_description_sha256"]
                source = TranslationSourceVersion(
                    raw[2], row["source_version"], raw[1], row["source_language"], fields
                )
                board = board_skill_observations(source)
                verify_board_observations(source, [asdict(b) for b in board])
                counts.append(
                    {
                        "group": group,
                        "source_version": row["source_version"],
                        "board_tags": len(board),
                        "employer_obligation_asserted": 0,
                    }
                )
        assert file_digest(dbpath) == freeze["frozen_snapshot_sha256"][group]
    assert len(counts) == 12
    return {
        "r2": r2,
        "r3": r3,
        "r4": {"sources": counts, "total_tags": sum(r["board_tags"] for r in counts)},
        "model_calls": 0,
        "authority": "offline_diagnostic_only",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
