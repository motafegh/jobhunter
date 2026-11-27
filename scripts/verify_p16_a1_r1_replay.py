"""Reproduce R1 on the frozen E1 replay context, without generating or exporting source text."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)
from jobhunter.p16_lab import ROOT, checked_path, file_digest, load_requirements
from jobhunter.p16_lab_a1_r1 import (
    AnalysisRequirementR1,
    JobAnalysisResponseR1,
    _compound_scopes,
)

REPLAY = "data/local-acceptance/p16-evolution-e1-2026-11-24/PRIVATE_E1_4_REPLAY.json"
REPLAY_SHA = "6e868598bd3cd0b7e912d682d0602de72b61f89a2d40a3b55277f7e42085f055"


def outcome(cls, raw, ctx):
    try:
        return cls.model_validate(raw, context=ctx), []
    except ValidationError as exc:
        # Never emit source, model output or validation message text.
        return None, [
            {"location": list(e["loc"]), "type": e["type"]}
            for e in exc.errors(include_url=False, include_context=False, include_input=False)
        ]


def verify(root: Path = ROOT) -> dict:
    load_requirements(root)
    path = checked_path(root, REPLAY)
    if file_digest(path) != REPLAY_SHA:
        raise ValueError("retained replay digest mismatch")
    cases = json.loads(path.read_bytes())
    rows = []
    target_count = 0
    for case in cases:
        for r in case["replays"]:
            matches = r["replays"]
            if len(matches) != 1:
                raise ValueError("ambiguous retained partition")
            ctx = case["captures"][matches[0]["partition"] - 1]["context"]
            before, before_errors = outcome(JobAnalysisResponseV30, r["raw"], ctx)
            after, after_errors = outcome(JobAnalysisResponseR1, r["raw"], ctx)
            targets = []
            for i, q in enumerate(r["raw"]["requirements"]):
                scopes = _compound_scopes(str(q.get("item_excerpt") or ""))
                if not scopes:
                    continue
                old, _ = outcome(AnalysisRequirementV30, q, ctx)
                new, _ = outcome(AnalysisRequirementR1, q, ctx)
                if old is not None or new is None:
                    raise ValueError("target replay outcome mismatch")
                scope = [s for s in scopes if s.subject.casefold() == new.concept.casefold()]
                if (
                    len(scope) != 1
                    or new.depth_signal != scope[0].degree
                    or new.item_excerpt != scope[0].item
                    or new.evidence != ctx["evidence_catalog"][q["evidence"]]
                ):
                    raise ValueError("target scope not preserved")
                targets.append(
                    {
                        "index": i,
                        "before_valid": False,
                        "after_valid": True,
                        "exact_parent_child_degree_preserved": True,
                    }
                )
                target_count += 1
            rows.append(
                {
                    "attempt": case["attempt"],
                    "diagnostic": r["diagnostic"],
                    "partition": matches[0]["partition"],
                    "before_full_valid": before is not None,
                    "after_full_valid": after is not None,
                    "before_errors": before_errors,
                    "after_errors": after_errors,
                    "targets": targets,
                }
            )
    if file_digest(path) != REPLAY_SHA or len(rows) != 6 or target_count != 4:
        raise ValueError("unexpected replay inventory")
    if any(r["before_full_valid"] or r["after_full_valid"] for r in rows):
        raise ValueError("unexpected whole response outcome; review independently")
    if any(r["before_errors"] != r["after_errors"] for r in rows if not r["targets"]):
        raise ValueError("unrelated replay outcome changed")
    return {
        "private_replay_sha256": REPLAY_SHA,
        "responses": rows,
        "target_items_recovered": target_count,
        "full_responses_valid": 0,
        "model_calls": 0,
        "authority": "offline_diagnostic_only",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
