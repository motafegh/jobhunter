# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-17  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I5 ACCEPTED / I6 NEXT

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
- [x] upstream source/translation/P1.6 not invalidated by target-definition changes.

Acceptance: `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

### I2 — target-scoped affected work — ACCEPTED

- [x] target-only source missing/refresh planning.
- [x] target-only translation/P1.6 planning.
- [x] no global-backlog budget spill.
- [x] cautious lifecycle/freshness semantics.
- [x] exact downstream currentness/reuse.

Acceptance: `docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md`

### I3 — membership qualification — ACCEPTED

- [x] deterministic constraints first.
- [x] bounded semantic relevance only when needed.
- [x] exactly core/adjacent/uncertain/excluded.
- [x] title/skills alone cannot prove core.
- [x] accepted P1.6 optional evidence, pending not a gate.
- [x] exact dependency reuse and immutable corrections.
- [x] repository CI 1172 green with 608 tests twice.
- [x] bounded real-model evidence preserved.
- [x] target-definition boundary lesson recorded without a vacancy-specific prompt patch.

Acceptance: `docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md`

### I4 — immutable snapshot construction — ACCEPTED

- [x] completed/nonfailed Market run required.
- [x] exact current membership identities only.
- [x] stale/superseded membership rejected.
- [x] one source job at most once.
- [x] semantic coverage derived as accepted/pending/missing/failed/rejected.
- [x] core-only primary source corpus.
- [x] historical snapshot immutability.
- [x] CI 1182 green with 617 tests twice.

Acceptance: `docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`

### I5 — deterministic aggregate profile — ACCEPTED

- [x] aggregate reads one immutable I4 snapshot only.
- [x] explicit source-level core and accepted-semantic denominators.
- [x] exact historical source-detail employer/context authority.
- [x] unknown employer remains explicit.
- [x] accepted-semantic core only for requirement/responsibility prevalence.
- [x] one-posting-at-most-once concept/responsibility support.
- [x] requirement strength/depth and exact evidence drill-down.
- [x] deterministic employer breadth/concentration.
- [x] Canonical Registry enrichment only as-of snapshot time.
- [x] later Registry review does not alter historical deterministic replay.
- [x] no model-authored numeric values.
- [x] explicit repost-adjustment limitation and sample/coverage warnings.
- [x] immutable/idempotent aggregate persistence.
- [x] CI 1189 green with 622 tests twice.

Acceptance: `docs/working-memory/2026-09-17_MARKET_I5_DETERMINISTIC_AGGREGATE_PROFILE.md`

### I6 — thin browser + CLI Market workflow — NEXT

- [ ] expose target list/create.
- [ ] expose immutable target-definition create/inspect.
- [ ] expose run state/ledger/history.
- [ ] expose snapshot/profile history.
- [ ] render deterministic profile evidence-quality header and warnings.
- [ ] render source/core vs accepted-semantic denominators.
- [ ] render membership/semantic coverage counts.
- [ ] render requirement/responsibility evidence drill-down.
- [ ] CLI uses the same services/state as browser.
- [ ] browser remains primary repeat-use surface.
- [ ] preserve existing one-mutable-operation boundary.
- [ ] add a thin coordinator only where needed to connect accepted stages; no generic workflow engine.
- [ ] keep Market state local/private.
- [ ] focused browser/CLI/service tests.

### I7 — bounded real local acceptance — AFTER I6

- [ ] one representative real target run.
- [ ] verify acquisition bounds/noise visibility.
- [ ] verify target-definition semantics.
- [ ] verify unchanged rerun reuse.
- [ ] verify snapshot/profile denominators and drill-down.
- [ ] verify partial success.
- [ ] close first slice only after the real acceptance matrix passes.

---

## C. Permanent first-slice invariants

- [x] acquisition/search envelope != target membership truth.
- [x] primary source corpus = core only.
- [x] accepted P1.6 not required for membership.
- [x] accepted-current P1.6 required for semantic prevalence.
- [x] pending/missing/failed/rejected P1.6 != zero demand.
- [x] target-definition meaning materially affects semantic classification.
- [x] snapshot/profile history is point-in-time and immutable.
- [x] aggregate numbers are deterministic application responsibilities.
- [x] denominator language = qualified source postings.
- [x] repost/new-ID collapse remains unimplemented and explicitly disclosed.

---

## D. Explicitly deferred / not authorized

- [-] another B1 promotion/model matrix.
- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable role archetypes.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as first-slice gates.
- [-] automatic repost/new-ID collapsing.
- [-] semantic role-subfamily synthesis.
- [-] model-generated Market report narrative.
- [-] trend/emerging/forecasting.
- [-] personal readiness/gap/scoring/recommendations.
- [-] Market publication to `corpus/`.
- [-] vector/RAG/graph/autonomous-agent infrastructure.
- [-] generic second-source/plugin framework before a real source need.

---

## E. Parallel portfolio/release

- [x] MIT license.
- [x] repository-side release/CV/interview package prepared.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` release.
- [ ] owner mastery verification.

---

## Exact next action

```text
I6 only
→ thin browser + CLI Market workflow over accepted I1-I5 services/state
→ no duplicate business logic
→ focused UI/CLI/service tests
→ state reconciliation
→ then I7 bounded real local acceptance
```
