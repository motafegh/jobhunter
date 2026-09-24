"""Local review commands for source-anchored P1.6 candidates."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from jobhunter.analysis_item_review import AnalysisItemReviewStore
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings


def main(argv: Sequence[str] | None = None, *, config_path: Path | None = None) -> int:
    parser = argparse.ArgumentParser(prog="jobhunter item-review")
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("show", "begin", "finish"):
        cmd = sub.add_parser(name)
        cmd.add_argument("artifact_id", type=int)
        if name == "finish":
            cmd.add_argument("--note", required=True)
    item = sub.add_parser("item")
    item.add_argument("artifact_id", type=int)
    item.add_argument("kind", choices=("requirements", "responsibilities", "role_purpose"))
    item.add_argument("index", type=int)
    item.add_argument("finding", choices=("supported", "needs_clarification", "unsupported"))
    item.add_argument("--note", required=True)
    item.add_argument("--minor", action="store_true")
    item.add_argument("--propose")
    gap = sub.add_parser("gap")
    gap.add_argument("artifact_id", type=int)
    gap.add_argument("finding", choices=("gap_open", "gap_dismissed"))
    gap.add_argument("--source-excerpt", required=True)
    gap.add_argument("--note", required=True)
    gap.add_argument("--minor", action="store_true")
    gap.add_argument("--propose")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.artifact_id < 1:
        parser.error("artifact_id must be positive")

    settings = Settings.load(config_path)
    if not settings.database_path.is_file():
        parser.error("No local JobHunter database at the configured path")
    store = AnalysisItemReviewStore(settings.database_path)
    try:
        if args.action == "show":
            artifact = AnalysisStore(settings.database_path).artifact_by_id(args.artifact_id)
            if artifact is None:
                raise ValueError("Analysis artifact not found")
            for kind in ("role_purpose", "responsibilities", "requirements"):
                for index, claim in enumerate(artifact.analysis.get(kind, [])):
                    print(json.dumps({
                        "kind": kind, "index": index, "original_claim": claim,
                    }, ensure_ascii=False, sort_keys=True))
            for event in store.events(args.artifact_id):
                print(json.dumps({
                    "event_id": event.id, "kind": event.kind,
                    "index": event.item_index, "finding": event.finding,
                    "material": event.material, "note": event.note,
                    "source_excerpt": event.source_excerpt,
                    "proposed_text": event.proposed_text,
                }, ensure_ascii=False, sort_keys=True))
            print(json.dumps({"item_review_complete": store.is_complete(args.artifact_id)}))
        elif args.action == "begin":
            store.begin(args.artifact_id)
            print(f"Item review opened for artifact {args.artifact_id}")
        elif args.action == "item":
            event_id = store.review_item(
                args.artifact_id, kind=args.kind, index=args.index,
                finding=args.finding, note=args.note, material=not args.minor,
                proposed_text=args.propose,
            )
            print(f"Recorded item-review event {event_id}; original candidate unchanged")
        elif args.action == "gap":
            event_id = store.review_gap(
                args.artifact_id, source_excerpt=args.source_excerpt,
                finding=args.finding, note=args.note, material=not args.minor,
                proposed_text=args.propose,
            )
            print(f"Recorded source-coverage event {event_id}; no analysis item added")
        else:
            store.complete(args.artifact_id, note=args.note)
            print("Complete-item review recorded; separate artifact acceptance still required")
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
