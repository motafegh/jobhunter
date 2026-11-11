"""Run one *candidate-only* JobHunter capability-interpretation trial in local LM Studio.

The source evidence and raw model response stay ignored under data/local-acceptance.
A separate metadata-only JSON result is safe for a public GitHub repository.
This never writes to JobHunter's live SQLite or promotes semantic authority.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote, urlparse

import httpx
from openai import OpenAI

from jobhunter.capability_expectations import (
    ProposedInterpretation,
    build_capability_expectation_brief,
    decode_candidate_json,
    validate_interpretation_proposals,
)
from jobhunter.config import Settings

SYSTEM = """You produce bounded *candidate* career interpretation, never employer facts.

Given exact accepted JobHunter requirements and responsibilities for one job:
- Respect every exact source statement, obligation/depth and claim identity.
- "Required" on a statement listing X OR Y does NOT mean both X and Y are mandatory.
- A qualification MUST NOT become an asserted job responsibility.
- A directly stated responsibility may support a modest inference, but not fabricated
  ownership, cloud architecture, production deployment, autonomy, SLAs, or scale.
- Do NOT assume typical RAG, ML or Python sub-skills apply to this vacancy without evidence.
- Only cite provided exact source claim IDs (analysis_id:claim_kind:claim_index).
- If the job lacks concrete evidence for additional interpretation, return no proposals.
- Every item is non-authoritative and requires a human semantic review.
- Do not restate an accepted employer statement as a NEW strongly implied fact.
- A candidate based solely on a qualification cannot imply a job duty.
- If proposing an uncertainty about the alternatives, label it unknown_or_unsupported.

Respond with a JSON object containing "proposals", a list of zero to three objects:
{"text": "...", "status": "strongly_implied_by_work" |
"model_inferred_prerequisite" | "unknown_or_unsupported",
"confidence": "low" | "medium" | "high",
"supporting_refs": ["50:responsibility:6"],
"rationale": "..."}
Avoid generic questionnaires. Each proposal should add a *specific, evidence-linked*
interpretation or an explicit unknown relevant to career preparation.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="jobhunter.toml")
    parser.add_argument("--job", required=True)
    parser.add_argument("--phrase", required=True)
    parser.add_argument("--max-tokens", type=int, default=1400)
    args = parser.parse_args()
    if not Path("AGENTS.md").exists():
        parser.error("Run this script from the JobHunter repository root")
    if args.max_tokens < 500 or args.max_tokens > 2400:
        parser.error("max-tokens must be between 500 and 2400")
    settings = Settings.load(args.config)
    model = settings.effective_capability_lm_studio_model()
    if urlparse(settings.lm_studio_base_url).hostname not in (
        "127.0.0.1", "localhost", "::1"
    ):
        parser.error("Candidate trial requires a loopback-only LM Studio endpoint")
    if not model:
        parser.error("No configured local Capability model")
    local = Path("data/local-acceptance/p23b-capability-expectations")
    local.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="model-read-", dir=local) as temp:
        copy = Path(temp) / "copy.sqlite3"
        uri = "file:" + quote(str(settings.database_path.resolve()), safe="/") + "?mode=ro"
        source = sqlite3.connect(uri, uri=True)
        try:
            with sqlite3.connect(copy) as snapshot:
                source.backup(snapshot)
        finally:
            source.close()
        brief = build_capability_expectation_brief(
            settings.model_copy(update={"database_path": copy}), args.job, args.phrase
        )
    source_facts = [
        {"ref": f.ref, "kind": f.claim_kind, "statement": f.statement,
         "strength": f.strength, "explicit_depth": f.explicit_depth,
         "potential_alternatives": f.potential_alternatives}
        for f in brief.all_facts
    ]
    user_payload = {
        "job_id": brief.source_job_id,
        "capability_phrase": brief.capability_phrase,
        "factual_claims": source_facts,
        "no_matching_direct_duty": not bool(brief.source_responsibilities),
        "authority": "accepted employer facts only; model interpretations are candidates",
    }
    client = OpenAI(
        base_url=settings.lm_studio_base_url,
        api_key="lm-studio",
        max_retries=0,
        http_client=httpx.Client(trust_env=False, timeout=150),
    )
    now = datetime.now(UTC).isoformat()
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=args.max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
    )
    message = response.choices[0].message
    raw = message.content or ""
    outcome = "not_evaluable"
    error_kind = None
    count = 0
    validated: list[dict] = []
    try:
        parsed = decode_candidate_json(raw)
        if not isinstance(parsed, dict) or not isinstance(parsed.get("proposals"), list):
            raise ValueError("Expected JSON object with proposals list")
        if len(parsed["proposals"]) > 3:
            raise ValueError("More than three model candidates")
        candidate = tuple(
            ProposedInterpretation(
                text=item["text"], status=item["status"],
                confidence=item["confidence"],
                supporting_refs=tuple(item["supporting_refs"]),
                rationale=item["rationale"],
            )
            for item in parsed["proposals"]
        )
        validate_interpretation_proposals(brief, candidate)
        outcome = "structurally_valid_unreviewed"
        count = len(candidate)
        validated = parsed["proposals"]
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        outcome = "validation_rejected"
        error_kind = type(exc).__name__
    local_raw = local / f"{args.job}-{args.phrase.lower()}-model-local.json"
    local_raw.write_text(
        json.dumps(
            {
                "model": model,
                "endpoint": settings.lm_studio_base_url,
                "time_utc": now,
                "input": user_payload,
                "raw_model_content": raw,
                "validated_candidates": validated,
                "finish_reason": response.choices[0].finish_reason,
                "mechanical_outcome": outcome,
                "mechanical_error_class": error_kind,
            }, ensure_ascii=False, indent=2,
        ) + "\n", encoding="utf-8",
    )
    public_dir = Path(
        "docs/working-memory/2026-11-11_p23b_capability_expectation"
    )
    public_dir.mkdir(parents=True, exist_ok=True)
    public_path = public_dir / (
        f"LOCAL_MODEL_EVALUATION_{args.job}_{args.phrase.lower().replace(' ', '-')}.json"
    )
    public_path.write_text(
        json.dumps(
            {
                "contract": "p23b-local-model-eval-v0",
                "time_utc": now,
                "source_job_id": args.job,
                "capability_phrase": args.phrase,
                "model": model,
                "configured_local_endpoint": settings.lm_studio_base_url,
                "max_tokens": args.max_tokens,
                "finish_reason": response.choices[0].finish_reason,
                "output_nonempty": bool(raw.strip()),
                "mechanical_outcome": outcome,
                "mechanical_error_class": error_kind,
                "valid_unreviewed_candidate_count": count,
                "accepted_as_employer_truth": False,
                "owner_semantic_acceptance": False,
                "raw_response_public": False,
                "source_text_public": False,
                "database_mutated": False,
            }, sort_keys=True, indent=2,
        ) + "\n", encoding="utf-8",
    )
    print(
        f"Local model {model}: finish={response.choices[0].finish_reason}, "
        f"mechanical={outcome}, candidates={count}"
    )
    print(f"Raw local-only evidence: {local_raw}")
    print(f"Safe reviewable metadata: {public_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
