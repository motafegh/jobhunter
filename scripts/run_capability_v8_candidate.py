#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jobhunter.capability_service_v6 import CapabilityIntelligenceError
from jobhunter.capability_service_v7 import format_capability_intelligence
from jobhunter.capability_service_v8 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    build_capability_v8_candidate_service,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.inference import InferenceProviderError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run isolated source-led Capability v8 reasoning for one current job."
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()

    try:
        settings = Settings.load(args.config)
        result = build_capability_v8_candidate_service(settings).analyze_job(args.job_id)
        artifact = CapabilityIntelligenceStore(settings.database_path).latest_current(
            args.job_id,
            model=result.model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Capability v8 artifact is unavailable after successful analysis")
    except (ConfigLoadError, CapabilityIntelligenceError, ValueError) as exc:
        print(f"Capability v8 candidate is not ready: {exc}", file=sys.stderr)
        return 2
    except (InferenceProviderError, OSError, RuntimeError) as exc:
        print(f"Capability v8 candidate failed: {exc}", file=sys.stderr)
        return 1

    print(f"Outcome: {result.outcome}")
    print(format_capability_intelligence(artifact))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
