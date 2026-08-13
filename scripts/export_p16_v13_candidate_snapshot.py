#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from jobhunter.config import Settings
from jobhunter.p16_v13_snapshot import export_candidate_snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("review-snapshots/jobs"))
    args = parser.parse_args()
    destination = export_candidate_snapshot(
        Settings.load(args.config), args.job_id, args.output_dir
    )
    print(destination.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
