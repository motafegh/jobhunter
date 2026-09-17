# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-17  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I6 ACCEPTED / I7 NEXT

Status vocabulary:

```text
[ ] not started
[~] in progress / acceptance incomplete
[x] accepted/completed for stated scope
[!] blocking defect
[-] deliberately deferred
```

---

## A. Closed accepted substrate

- [x] Phase 1 CLOSED.
- [x] P2.1 Canonical Registry CLOSED.
- [x] P2.2A Job Work Intelligence CLOSED.
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.
- [x] Market foundation Q1-Q12 PASS / first vertical slice authorized.

Do not reopen accepted historical work without a repeatable current contradiction.

---

## B. Market first vertical slice

### I1 — domain + persistence — ACCEPTED

- [x] stable target + immutable definition versions.
- [x] run lifecycle/ledger persistence.
- [x] immutable exact-dependency memberships/corrections.
- [x] immutable snapshot/member history.
- [x] immutable deterministic aggregate-profile storage.
- [x] target-definition changes do not invalidate generic source/translation/P1.6.

Acceptance: `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

### I2 — target-scoped affected work — ACCEPTED

- [x] target-only source missing/refresh planning.
- [x] target-only translation/P1.6 planning.
- [x] no global-backlog budget spill.
- [x] failed refresh != disappearance/fresh evidence.
- [x] exact downstream currentness/reuse.

### I3 — membership qualification — ACCEPTED

- [x] deterministic constraints first.
- [x] bounded semantic relevance only when needed.
- [x] `core_match / adjacent_match / uncertain / excluded`.
- [x] title/skills alone cannot prove core.
- [x] accepted P1.6 optional; pending/missing P1.6 not a membership gate.
- [x] exact dependency reuse and immutable reviewed corrections.
- [x] real-model boundary evidence preserved under `docs/experiments/2026-09-17_market-i3-real-model-acceptance/`.

Acceptance: `docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md`

### I4 — immutable snapshot construction — ACCEPTED

- [x] terminal Market run required.
- [x] exact current membership identities only.
- [x] stale/superseded membership rejected.
- [x] semantic coverage preserved as accepted/pending/missing/failed/rejected.
- [x] only core enters primary corpus.
- [x] historical snapshot/member state immutable.

### I5 — deterministic aggregate profile — ACCEPTED

- [x] snapshot-only deterministic aggregation.
- [x] source/core vs accepted-semantic denominators remain separate.
- [x] per-posting concept deduplication.
- [x] immutable source-detail employer authority.
- [x] employer breadth/concentration warnings.
- [x] requirement strength and responsibility evidence drill-down.
- [x] Registry enrichment only as-of snapshot time.
- [x] no model-authored numeric facts.
- [x] repost/new-ID limitation explicit.

### I6 — shared browser + CLI workflow — ACCEPTED

Acceptance: `docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

- [x] one shared `MarketWorkspaceService` for browser/CLI.
- [x] immutable target acquisition/search envelope.
- [x] target search catalog version drift rejected.
- [x] bounded discovery/detail/translation/P1.6/membership controls.
- [x] explicit membership budget + remaining-work ledger.
- [x] partial-success run ledger preserves durable stage success.
- [x] read-only target preview does not construct model/provider runtime.
- [x] existing I5 aggregate contract restored/frozen after integration regression was caught.
- [x] CLI target/create-version/preview/run/run-show/snapshot-show.
- [x] browser `/market/targets`, run ledger and snapshot/profile drill-down.
- [x] existing one-mutable-web-operation boundary reused.
- [x] Market tables remain local/private; only existing upstream public artifacts may sync.
- [x] CI 1210 green: installed-entrypoint smoke, Ruff, 632 tests, 632 tests with warnings-as-errors.

### I7 — bounded real local acceptance — NEXT

Use one small representative target with explicit core-vs-adjacent meaning.

- [ ] confirm local runtime/SQLite/provider readiness without mutating operational state unnecessarily.
- [ ] create/reuse one stable target and intentional immutable definition version.
- [ ] preview the exact acquisition envelope and bounded controls.
- [ ] run bounded real Jobinja discovery/acquisition.
- [ ] inspect discovered candidate count/noise and confirm no global-backlog spill.
- [ ] inspect source refresh outcomes and confirm failure does not imply disappearance.
- [ ] inspect translation reuse/new work/failures.
- [ ] inspect P1.6 accepted/pending/missing/failed/rejected coverage.
- [ ] inspect membership decisions across core/adjacent/uncertain/excluded where present.
- [ ] inspect run partial-success ledger.
- [ ] inspect immutable snapshot membership/source/semantic identities.
- [ ] inspect primary source denominator vs accepted-semantic denominator.
- [ ] inspect deterministic requirement/responsibility aggregates and employer warnings.
- [ ] drill down from Market evidence to exact source job/P1.6 evidence.
- [ ] repeat unchanged run with bounded controls and verify meaningful reuse/currentness.
- [ ] verify browser and CLI expose the same durable state.
- [ ] verify Market tables/state remain local/private and are absent from public corpus export.
- [ ] record real acceptance evidence and any defects.
- [ ] PASS only if the complete first-slice path is correct/useful; otherwise repair the owning boundary and rerun.

---

## C. First-slice permanent invariants

- [x] target identity separate from immutable meaning versions.
- [x] target meaning does not invalidate generic upstream artifacts.
- [x] target-scoped work does not spill into unrelated backlog.
- [x] `uncertain` is a successful semantic outcome.
- [x] adjacent/uncertain/excluded never silently enter primary core denominator.
- [x] missing/pending/failed/rejected P1.6 never means zero demand.
- [x] only accepted-current P1.6 contributes to strong semantic statistics.
- [x] snapshot members reference exact dependencies.
- [x] snapshots remain immutable after future source/target/contract changes.
- [x] aggregate profiles reference one exact snapshot/contract.
- [x] first slice says `qualified source postings`, not unproven unique demand.
- [x] browser and CLI share state/service owners.
- [ ] real local end-to-end acceptance still required before first-slice closure.

---

## D. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable promoted role archetypes.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as mandatory Market gates.
- [-] automatic repost/new-ID collapse.
- [-] semantic role-subfamily report synthesis in first slice.
- [-] trends / emerging / forecasting.
- [-] Market → You / personal readiness/gap/scoring.
- [-] Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure.

---

## E. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics settings action.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden I7 authorization.

---

## Exact next action

```text
I7 only
→ bounded representative real local Market run
→ inspect acquisition/reuse/membership/denominators/evidence/browser+CLI/privacy
→ record acceptance evidence
→ PASS or bounded repair
→ close first Market vertical slice only from real evidence
```
