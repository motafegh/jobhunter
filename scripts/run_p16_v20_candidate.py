#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jobhunter.analysis_runtime_v20 import build_v20_candidate_analysis_service
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v20 import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.inference import InferenceProviderError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run isolated English P1.6 v20 source-led partitioned analysis for one job."
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    try:
        settings = Settings.load(args.config)
        result = build_v20_candidate_analysis_service(settings).analyze_english_job(args.job_id)
    except (ConfigLoadError, AnalysisValidationError, ValueError) as exc:
        print(f"P1.6 v20 candidate is not ready: {exc}", file=sys.stderr)
        return 2
    except (InferenceProviderError, OSError, RuntimeError) as exc:
        print(f"P1.6 v20 candidate failed: {exc}", file=sys.stderr)
        return 1
    print(f"Outcome: {result.outcome}")
    print(f"English P1.6 v20 candidate for {result.source_job_id}")
    print(f"Artifact: {result.artifact_id}")
    print(f"Model: {result.model}")
    print(f"Contract: {ENGLISH_PROMPT_VERSION} / {ANALYSIS_SCHEMA_VERSION}")
    print(f"Responsibilities: {result.responsibilities}")
    print(f"Requirements: {result.requirements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
