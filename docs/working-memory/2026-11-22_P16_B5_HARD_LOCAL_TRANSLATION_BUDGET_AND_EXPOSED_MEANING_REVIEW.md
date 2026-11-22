# P1.6 B5 — enforced physical local-model budget and exposed translation-meaning review

**Date:** 2026-11-22
**Disposition:** B5 transport-budget engineering PASS on an exposed bounded pilot; B5 unseen semantic generalization NOT established, B6 production NOT authorized.

## Predecessor and problem

The November 21 B5 translation batch pilot proved source association for two preferred items. It did **not** enforce a cap on actual network attempts. The existing local provider can retry connection/HTTP failures, or issue another request with more output tokens when a structured response finishes at the token limit. A run that plans a single logical translation batch can therefore make multiple physical HTTP requests. Counting requests *after* execution does not prevent an accidental overrun.

The accepted English v30/original-language v9 pipeline, historical B2/B3/B4 artifacts, source snapshots and downstream authority are protected. The eight original B5 jobs had already been used for development after the first source-gate failure and are **not unseen verification**.

## Engineering implementation

New opt-in `src/jobhunter/source_bound_translation_budget_b5.py` provides a single-use, cumulative B5 physical-request guard:

- Counts the attempted HTTP **dispatch**, not logical batches, source items or successful responses, including transport retries, HTTP 5xx and truncated-output token recovery. A hard ceiling rejects the next dispatch *before* sending it. Failed/unfinished batch translations remain individually unresolved with original source identities.
- Restricts requests to local LM Studio (`127.0.0.1:18080` / loopback, `/v1/chat/completions`, HTTP POST); no cloud endpoints, no raw source or target payload in public-safe guard telemetry.
- Uses a POSIX main-thread process signal plus monotonic-clock checks for one session-wide wall deadline, even during a stalled response. A platform/thread unable to enforce that deadline must refuse the session. When the model creates short-lived HTTP clients and reenters the shared transport, the outer budget and timer remain active; successful and failed exits restore the previous signal handler.
- This first **exposed research** guard deliberately accepts only 1–8 model HTTP attempts and 1–900 seconds as policy parameters, and is not implicitly a budget for the future unseen complete B5 cohort. It leaves `LMStudioTranslationProvider` and the previously frozen `BoundedBatchLMStudioProvider` unchanged.

A new test suite `tests/test_source_bound_translation_budget_b5.py` validates physical counting, cumulative behavior across batches, 5xx retry, connection timeout retry, token truncation recovery, OS wall-clock interruption, clock expiration between calls, wrong host/path rejection, source/target-payload-free receipts, no implicit unbounded policy, signal cleanup and failed/unattempted source-item states.

## Frozen pre-model exposed evaluation

Before new model calls, five source-owned batches (ten original Persian items from **three previously exposed** jobs) were selected and the assistant's original-language source-only meanings sealed with exact item/source SHAs. Tested semantic dimensions: backend responsibilities and architecture; technical qualification **proficiency versus familiarity**; named vector-database tools; separately recruited security specializations; explicit **not all specialties required** negation; **one or more specialties** priority; and an **optional** security-tool clause.

The private frozen experiment predeclared **maximum 7 physical HTTP attempts**, **240 seconds wall time**, one retry allowance per provider invocation, and only local `gemma-4-e2b-it`. The B0 original **80-call paired-analysis ceiling is separate from translation**, and no unseen B5 translation budget has been silently approved.

## Real local result

| Metric | Verified |
| --- | ---: |
| Selected exposed source items | 10 |
| Selected translation batches | 5 |
| Physical HTTP attempt cap | 7 |
| Actual HTTP dispatch attempts | 5 |
| HTTP 200 responses | 5 |
| Time cap | 240 seconds |
| Measured elapsed | ~60.8 seconds |
| Valid source-bound English translation candidates | 10 |
| Request overrun or wall-budget hit | 0 |
| Production DB, public corpus or accepted authority changes | 0 |

No physical retries or truncation recovery were needed in this live sample; mock-transport tests independently prove the budget rejects overruns in those paths. One first model response took roughly 41.9 seconds; model warmup/order was not controlled. These are observed attempt and time counts, **not** a throughput or latency-speedup study.

## Source-grounded assistant review (after model outputs)

The same ten **pre-model** original-source assertions were compared to the returned English items, with per-item SHA references and full private HTTP payload receipts. An exposed, **not blind or independent**, assistant review found:

- **Nine** individual translations supported the selected original-language meanings, preserving duty context, proficiency versus familiarity, negation and one-or-more alternatives. No observed preferred-to-required strengthening in the selected items.
- **One** English item **omitted the technical token Secure SDLC**. It preserved the optional status of example security tools, but it is *not* a fully faithful complete item. The existing lexical source-bound review already warned that these named tokens were not obvious in the translation. Retain this as a material partial/mismatch pending any future correction or source-led alternative; **do not silently label it accepted**.

These are *counts within ten selected exposed items*, not market estimates, semantic accuracy rates, independent human judgments or evidence that the model never makes other mistakes. Neither the negative/OR rendering nor a mechanically valid source ID certifies a fully reviewed eligibility graph or durable employer fact.

## Reproducibility and privacy

`scripts/pilot_p16_b5_budget_guard_v1.py` verifies and freezes the source-only scope **before inference**, then executes the local-only budgeted session once. The entire raw review, source text, exact model request/response bodies and output stay in ignored `data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1/budgeted-variety-pilot-v1/`.

`scripts/verify_p16_b5_budget_guard_pilot.py` replays the sealed original item identities, pre-model source review, source/code/model hashes, each physical request/response receipt, HTTP status, model ID and JSON contract, bounded budget, original-to-English per-item candidate state and post-model assistant verdict; it checks unchanged production DB and public corpus. No inference or persistence write occurs during replay.

Public-safe aggregate and SHA receipts: `docs/working-memory/2026-11-22_p16_b5_budget_guard/SAFE_B5_BUDGET_GUARD_AND_EXPOSED_MEANING_REVIEW.json`.

## Decision and next authorization boundary

**Verification:** 1,169 local warnings-as-errors regression tests passed, including 19 focused physical-budget boundary tests. Ruff lint/format, dependency consistency, compileall, sealed exposed source/HTTP/model/meaning replay, and historical B2v2/B4v5/earlier B5 replays all passed. The production DB and corpus are SHA-identical to the pre-pilot state. GitHub CI is separately checked after publication.

**Milestone PASS:** a bounded and verified local **transport-level** request/time budget plus explicit semantic-review failure preservation, on exposed development evidence only.

**Not yet passed:** B5 independent source-first fresh cohort; any claim that batching is more accurate/faster; translation-specific physical-call/time budget for full fresh B5; complete source/alternative coverage; fair job-level B4-v30 paired comparison; B6 public route activation.

The next substantive milestone should define the *separate* fresh-cohort translation budget, preserve model version and response-correction discipline, and acquire a distinct unseen six-to-eight-job source set under B0's metadata selection and original-language source-first review before candidate inference. The first critical source or obligation error should stop downstream fact promotion, while noncritical interpretation uncertainty may remain visible without inventing authority. Existing accepted v30/v9 remain untouched.
