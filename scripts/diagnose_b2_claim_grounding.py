"""Read-only, source-safe B2 advisory claim-link diagnostic.

The existing native v3 model output contains *no source item IDs*. This
script therefore does not invent links by keyword matching or Persian/English
substring equivalence. Optional reviewer links must be explicitly supplied,
bound to each exact model claim digest, and kept in ignored local data.

Example (run from repository root, no source/network/model writes):
  python scripts/diagnose_b2_claim_grounding.py --database PRIVATE_B0_SQLITE \\
    --trial PRIVATE_NATIVE_V3_JSON --annotations PRIVATE_REVIEW_LINKS_JSON \\
    --out data/local-acceptance/.../PRIVATE_LINKED_RECONCILIATION.json \\
    --safe-out docs/working-memory/.../SAFE_CLAIM_GROUNDING_METRICS.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from reconcile_b2_native_trials import _parse_model_json

from jobhunter.source_claim_reconciliation_b2 import (
    FIELDS,
    AdvisoryClaim,
    advisory_claim_sha256,
    reconcile_advisory_claims,
)
from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.translation_store import TranslationStore

CASES = ("tNhZ", "tMps", "tNDx", "tMjm")
B0_SHA256 = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
V3_CONTRACT = "jobhunter-b2-original-context-native-corrective-v3"
ANNOTATION_AUTHORITY = "assistant_prior_context_exposed_not_independent"
OUT_CONTRACT = "jobhunter-b2-advisory-grounding-diagnostic-v1"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_bytes())
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return data


def _inside(path: Path, root: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


def evaluate(
    database: Path,
    trial_path: Path,
    annotations_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """No provider calls, no production/currentness writes, no semantic acceptance."""
    db_hash = _sha(database.read_bytes())
    if db_hash != B0_SHA256:
        raise ValueError("Frozen B0 database identity mismatch")
    raw_trial = trial_path.read_bytes()
    trial = json.loads(raw_trial)
    if (
        trial.get("contract") != V3_CONTRACT
        or trial.get("source_database_sha256") != db_hash
        or trial.get("reasoning") != "off"
        or trial.get("authority") != "research_only_no_downstream_reuse"
        or set(trial.get("cases", {})) != set(CASES)
    ):
        raise ValueError("Trial source/model contract mismatch")
    annotations = _load_object(annotations_path)
    if (
        annotations.get("contract") != "jobhunter-b2-exposed-manual-links-v1"
        or annotations.get("authority") != ANNOTATION_AUTHORITY
        or annotations.get("source_database_sha256") != db_hash
        or annotations.get("trial_file_sha256") != _sha(raw_trial)
        or set(annotations.get("links", {})) != set(CASES)
    ):
        raise ValueError("Private exposed link annotation provenance mismatch")

    private: dict[str, Any] = {
        "contract": OUT_CONTRACT,
        "source_database_sha256": db_hash,
        "trial_file_sha256": _sha(raw_trial),
        "model": trial.get("model"),
        "model_prompt_sha256": trial.get("prompt_sha256"),
        "review_authority": ANNOTATION_AUTHORITY,
        "semantic_approval": False,
        "cases": {},
    }
    summary: dict[str, Any] = {
        "contract": OUT_CONTRACT,
        "source_database_sha256": db_hash,
        "trial_file_sha256": _sha(raw_trial),
        "model_prompt_sha256": trial.get("prompt_sha256"),
        "review_authority": ANNOTATION_AUTHORITY,
        "cohort": "four_exposed_cases_not_independent_holdout",
        "source_links_are_semantic_proof": False,
        "b2_gate": "OPEN_NO_PROMOTION",
        "accepted_employer_facts": 0,
        "cases": {},
    }

    with tempfile.TemporaryDirectory(prefix="b2-link-copy-") as tmpdir:
        # sqlite online-backup from the immutable input to a private scratch DB.
        copied = Path(tmpdir) / "read_only_review.sqlite3"
        with (
            sqlite3.connect(f"file:{database.resolve()}?mode=ro", uri=True) as src,
            sqlite3.connect(copied) as dst,
        ):
            src.backup(dst)
        store = TranslationStore(copied)
        for job in CASES:
            source = store.latest_source_version(job)
            if source is None:
                raise ValueError("Missing frozen source job version")
            case = trial["cases"][job]
            if (
                case.get("source_job_id") != job
                or case.get("source_semantic_sha256") != source.semantic_sha256
                or case.get("outcome") != "response"
                or case.get("stats", {}).get("reasoning_output_tokens") != 0
                or not isinstance(case.get("content"), str)
                or case.get("content_sha256") != _sha(case["content"].encode("utf-8"))
            ):
                raise ValueError("Trial case or source fingerprint mismatch")
            parsed = _parse_model_json(case["content"])
            if set(parsed) != FIELDS or any(
                not isinstance(v, list)
                or any(not isinstance(text, str) or not text.strip() for text in v)
                for v in parsed.values()
            ):
                raise ValueError("Unexpected model field, type or empty claim")
            candidate = interpret_original_source_candidate(source)

            link_rows = annotations["links"][job]
            if not isinstance(link_rows, list):
                raise ValueError("Expected per-job link list")
            link_by_key: dict[tuple[str, int], tuple[str, ...]] = {}
            for row in link_rows:
                if not isinstance(row, dict):
                    raise ValueError("Invalid reviewer link row")
                field, index = row.get("field"), row.get("index")
                if (
                    field not in FIELDS
                    or isinstance(index, bool)
                    or not isinstance(index, int)
                    or not 0 <= index < len(parsed[field])
                ):
                    raise ValueError("Invalid reviewer claim reference")
                key = (field, index)
                if key in link_by_key:
                    raise ValueError("Duplicate reviewer claim link")
                if row.get("claim_sha256") != advisory_claim_sha256(
                    source, field, index, parsed[field][index]
                ):
                    raise ValueError("Reviewer link is stale for this exact model claim")
                anchors = row.get("source_anchor_ids")
                if (
                    not isinstance(anchors, list)
                    or not anchors
                    or any(not isinstance(a, str) or not a for a in anchors)
                ):
                    raise ValueError("Reviewer link missing exact source anchors")
                link_by_key[key] = tuple(anchors)

            claims = []
            for field in sorted(FIELDS):
                for index, text in enumerate(parsed[field]):
                    anchors = link_by_key.get((field, index), ())
                    claims.append(
                        AdvisoryClaim(
                            field=field,
                            index=index,
                            text=text,
                            source_anchor_ids=anchors,
                            link_provenance=("assistant_exposed_diagnostic" if anchors else "none"),
                        )
                    )
            reconciled = reconcile_advisory_claims(source, candidate, tuple(claims))
            counts = Counter(x.grounding_state for x in reconciled.claims)
            signals = Counter(flag for x in reconciled.claims for flag in x.diagnostic_signals)
            private["cases"][job] = {
                "source_semantic_sha256": source.semantic_sha256,
                "claims": [asdict(x) for x in reconciled.claims],
            }
            summary["cases"][job] = {
                "total_model_claims": len(reconciled.claims),
                "linked_claims": len(link_by_key),
                "unlinked_unknown": counts["unlinked_unknown"],
                "linked_semantics_unreviewed": counts["linked_semantics_unreviewed"],
                "source_candidate_disagreement": counts["source_candidate_disagreement"],
                "diagnostic_signals": dict(sorted(signals.items())),
                "promoted_claims": 0,
            }
    if _sha(database.read_bytes()) != db_hash:
        raise ValueError("B0 immutable input changed during evaluation")
    summary["totals"] = {
        "model_claims": sum(x["total_model_claims"] for x in summary["cases"].values()),
        "linked": sum(x["linked_claims"] for x in summary["cases"].values()),
        "unlinked_unknown": sum(x["unlinked_unknown"] for x in summary["cases"].values()),
        "source_candidate_disagreement": sum(
            x["source_candidate_disagreement"] for x in summary["cases"].values()
        ),
        "promoted": 0,
    }
    return private, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--trial", required=True, type=Path)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--safe-out", required=True, type=Path)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    private_root = root / "data/local-acceptance"
    public_root = root / "docs/working-memory/2026-11-16_p16_b2"
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter repository root")
    if not all(_inside(p, private_root) for p in (args.trial, args.annotations, args.out)):
        raise ValueError("Raw model, reviewer links and private output must remain ignored")
    if not _inside(args.safe_out, public_root):
        raise ValueError("Source-safe metrics must remain in B2 evidence directory")
    if args.out.exists() or args.safe_out.exists():
        raise FileExistsError("Evidence outputs must not overwrite previous runs")
    private, summary = evaluate(args.database, args.trial, args.annotations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.safe_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(private, indent=2, ensure_ascii=False) + "\n")
    args.safe_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
