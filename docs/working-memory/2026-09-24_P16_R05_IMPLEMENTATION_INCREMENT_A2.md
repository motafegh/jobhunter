# R05 implementation increment A2 — scoped failure diagnostics and local inspection

**Date:** 2026-09-24  
**Status:** IMPLEMENTED ON FEATURE BRANCH / CI GREEN / UNMERGED / REAL-LOCAL VERIFICATION OUTSTANDING  
**Branch:** `agent/r05-diagnostic-safety-2026-09-24`  
**PR:** https://github.com/motafegh/jobhunter/pull/9  
**Parents:** `2026-09-24_P16_R05_IMPLEMENTATION_INCREMENT_A1.md`, `2026-09-24_P16_R05_REVISION_DEPENDENCIES_AND_FAILURE_CAPTURE_FINDINGS.md`.

## Implemented

- v21 provider attaches partition index/total to inference exceptions and retains model-validated structured output for earlier partitions in a per-invocation ContextVar. These fragments **have not necessarily passed parent scope or whole-analysis validation**. Post-partition failure is labeled conservatively; this implementation does not claim exact scope-vs-global diagnosis.
- Attempt-linked private diagnostic store preserves available failed completion text as a distinct payload kind, with explicit unavailable/oversize states, bounded item sizes/count and age-based cleanup. A1 records gain an initial retention timestamp on migration. No output is parsed as a valid candidate solely because it was captured.
- `jobhunter --config config/local.toml diagnostics list` and `... diagnostics show <attempt_id>` inspect local failed attempts. Old untrusted `error_message` and `error_type` are never printed. Response text is hidden unless `--include-response` is explicitly supplied. The CLI uses read-only SQLite and never synchronizes the public corpus.
- Synthetic fixture coverage for default-hidden response text, explicit raw opt-in, missing attempts, provider failure in partition 2 after partition 1 returns, post-partition failure without claiming completion, and expired-record cleanup.

## Verification and limits

GitHub Actions CI #1333 on commit `244a39ac28eb39d95ba0fc9c56bbaa86fd97e19c` passed Ruff, installed entrypoint smoke, full tests and full warnings-as-errors tests. No real LM Studio call, local user database migration, browser inspection acceptance or installer-level filesystem confidentiality test was executed. Diagnostic cleanup occurs on store access, not as an independent background timer; the read-only CLI does not itself prune expired payloads. The actual installed local Instructor and provider behavior requires a bounded real-local check before deployment approval.

## Authority and continuation

No public semantic version, P1.6 accepted/current selector, original evidence, historical Market snapshot, Capability, Registry or public-corpus export was changed. PR #9 remains draft and unmerged. The next distinct feature increment is pending-artifact item-level review with original claim provenance and an acceptance-side guard against unresolved material annotations; corrective revisions/promotion remain separate until identity migration is explicitly designed and verified.
