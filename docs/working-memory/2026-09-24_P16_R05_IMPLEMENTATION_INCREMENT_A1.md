# R05 implementation — A1 safe v21 failure history and local diagnostic foundation

**Date:** 2026-09-24  
**Branch:** `agent/r05-diagnostic-safety-2026-09-24`  
**Review:** [Merged PR #9](https://github.com/motafegh/jobhunter/pull/9)  
**Status:** MERGED TO `main`; REPOSITORY CI PASS; REAL-LOCAL VERIFICATION OUTSTANDING; NOT A COMPLETE R05 OR LIVE ACCEPTANCE

## Authority and rationale

Follows [R05 agreed direction](2026-09-24_P16_R05_ITEM_LEVEL_REVIEW_DIRECTION.md), [correction and proportional-guard decisions](2026-09-24_P16_R05_CORRECTION_LIFECYCLE_AND_PROPORTIONAL_GUARDS.md), [record design](2026-09-24_P16_R05_MINIMAL_RECORD_AND_DIAGNOSTIC_CAPTURE_DESIGN.md), and [revision/failure-capture findings](2026-09-24_P16_R05_REVISION_DEPENDENCIES_AND_FAILURE_CAPTURE_FINDINGS.md). Does not supersede governing product, source/privacy, architecture, utility/authority, Market or current-state owners.

## Implemented in this first increment

- `src/jobhunter/analysis_failure_diagnostics.py`: private SQLite sidecar for unsuccessful-generation diagnostics linked by foreign key to the existing `job_analysis_attempts` ID. Stores bounded available completion **message text** (not claimed to be lossless original HTTP bytes), retry ordinal when exposed, failure code and stage, and explicit unavailable/oversize states. Extracts from exception cause chains and known completion fields without stringifying arbitrary SDK objects. No failed output is inserted into `job_analysis_artifacts` or treated as pending P1.6. A private `list_for_attempt` read API exists; no public/browser export or inspection route was added.
- `src/jobhunter/analysis_service_v21.py`: v21 unsuccessful attempts keep the existing canonical attempt ledger, now receiving an application-authored failure code/message instead of potentially response-bearing arbitrary provider exception text. When configured, private diagnostic capture is best-effort and cannot mask the original failure. Inference connection/response exceptions surfaced to v21 callers are replaced with short safe messages; factual validators and success/promotion paths are unchanged.
- `src/jobhunter/analysis_runtime_v21.py`: shared CLI/browser/Market v21 service factory supplies the new sidecar. Historical v20/v5 compatibility and separate original-language analysis remain untouched.
- `tests/test_analysis_failure_diagnostics.py`: deterministic no-network regressions for safe messages, retry completion, no-response/oversize cases, attempt FK, non-artifact storage, v21 attempt linking, best-effort diagnostics and safe surfaced inference failure.

## Verification

Draft PR CI [run #1325](https://github.com/motafegh/jobhunter/actions/runs/36041755946) on commit `2483196b8eef054698128e4f77134fda6b68c876` completed successfully: installed entrypoint smoke, Ruff, full tests, and full tests with warnings as errors. An earlier CI lint failure was corrected before this run. No local LM Studio/model generation, live acceptance, local user database mutation, new P1.6 acceptance or Market snapshot was performed in this workstream.

## Deliberate incompleteness / remaining limits

A1 captures only a completion where its text is actually reachable through the existing error chain; SDK/provider failures can legitimately have no available response. The current service-level capture stage is `unclassified`; partition ordinal and preceding successful partitions are **not** yet retained when a later partition or whole-job guard fails. Error messages for other non-v21 paths were not globally changed. The diagnostic table remains local/private but a complete configurable retention/access/redaction policy and a user-facing read surface have not yet been implemented. Exact local installed Instructor/LM Studio behavior is not proven by synthetic CI fixtures. A1 deliberately does not implement R05 item-review annotations, source-coverage findings, semantic correction proposals, immutable revisions or revised-artifact promotion.

**Post-merge remaining verification:** verify real installed Instructor failure shapes without live model calls; define and enforce bounded local diagnostic retention and access; check caller/log/export privacy beyond the new v21 attempt path; demonstrate accurate failure-stage and partial-partition capture; test ordinary successful and failed candidate lifecycles, accepted-only consumers and historical snapshot invariance. Do not broaden accepted semantics, silently rewrite evidence, force `tvMm` retries, or mark Market I7 PASS as a consequence of A1.
