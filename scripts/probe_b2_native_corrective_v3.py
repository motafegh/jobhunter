"""One bounded B2 corrective prompt experiment, same source and native settings.

The initial warm v1 was transport/response available but used its entire
completion budget reasoning and returned no visible answer. Native v2 with
reasoning off returned complete JSON, but showed specific source-semantic
errors. This is a single predeclared concise correction, not per-job tuning.
No accepted artifact or product route can be modified by this script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from probe_b2_local_semantics import PROMPT as ORIGINAL_PROMPT
from probe_b2_native_reasoning_off import run_trial

CONTRACT = "jobhunter-b2-original-context-native-corrective-v3"
CORRECTIVE_PROMPT = (
    ORIGINAL_PROMPT + " In duties, list only assigned work, not statements of applicant ability."
    " In alternatives, preserve eligibility paths and certificate-or-knowledge"
    " choices, not example implementation tools. Explicit advantages are"
    " preferred; leave unclear qualifications unresolved."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    result = run_trial(args.database, args.out, prompt=CORRECTIVE_PROMPT, contract=CONTRACT)
    print("B2_CORRECTIVE_FINISHED", result["attempted"], "of", result["total_planned"])


if __name__ == "__main__":
    main()
