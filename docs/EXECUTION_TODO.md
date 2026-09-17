# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-17  
**Active working branch:** `main`  
**Current-state reconciliation:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**I1 acceptance:** `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`  
**I2 acceptance:** `docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md`  
**I3 acceptance:** `docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md`  
**I4 acceptance:** `docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`  
**I3 real-model evidence:** `docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`  
**Current product gate:** MARKET I1-I4 ACCEPTED / I5 NEXT  
**Parallel portfolio gate:** MIT complete / GitHub metadata + screenshots + release + owner mastery pending

Repository workflow:

```text
current work → main
next work    → main
```

Do not create a branch unless the repository owner explicitly changes this rule.

Status vocabulary:

```text
[ ] not started
[~] in progress / acceptance incomplete
[x] accepted/completed for stated scope
[!] blocking defect
[-] deliberately deferred
```

---

## A. Accepted foundation — CLOSED

- [x] Jobinja discovery/acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2` parser and cautious lifecycle semantics.
- [x] `english-projection-v2 / lm-studio-translation-v2`.
- [x] English P1.6 `job-analysis-english-v20 / job-analysis-v5`.
- [x] Capability `job-capability-intelligence-v9 / job-capability-intelligence-v5`.
- [x] Phase 1 CLOSED.
- [x] P2.1 Canonical Registry CLOSED.
- [x] P2.2A Job Work Intelligence CLOSED.
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.

Do not reopen B1 merely to manufacture promotion.

---

## B. Market / Role-Family foundation — COMPLETE / PASS

- [x] Q1–Q12 resolved.
- [x] `FOUNDATION INVESTIGATION: PASS`.
- [x] first vertical slice authorized.
- [x] source-level membership separated from accepted-P1.6 semantic denominator.
- [x] first-slice dispositions fixed to `core_match / adjacent_match / uncertain / excluded`.
- [x] Capability/Work not mandatory first-slice dependencies.
- [x] repost/new-ID automatic collapse deferred.
- [x] semantic role-subfamily/report synthesis deferred from first slice.

---

## C. Authorized first Market vertical slice — ACTIVE

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

### C1 — I1 domain + SQLite persistence — ACCEPTED / CLOSED

- [x] typed Market domain records.
- [x] SQLite Market persistence/history.
- [x] stable target vs immutable definition versions.
- [x] run lifecycle + ledger persistence.
- [x] exact-dependency immutable membership history.
- [x] immutable snapshot/member history.
- [x] immutable aggregate-profile persistence.
- [x] target-definition changes do not invalidate source/translation/P1.6.
- [x] CI 1160 green through `pytest -W error`.

### C2 — I2 target-scoped source eligibility + affected-work planning — ACCEPTED / CLOSED

- [x] exact target candidate/source-state representation.
- [x] deterministic current-active source eligibility.
- [x] target-only missing-detail and refresh/repair selection.
- [x] target-only translation and P1.6 affected-work planning.
- [x] exact translation/P1.6 reuse/currentness.
- [x] pending-current P1.6 preserved as pending-review.
- [x] `failed refresh != disappearance` and `failed refresh != fresh evidence`.
- [x] global-backlog spill regressions covered.
- [x] CI 1167 green through `pytest -W error`.

### C3 — I3 membership qualification — ACCEPTED / CLOSED

- [x] deterministic constraints before model reasoning.
- [x] bounded semantic role/work interpretation.
- [x] exactly `core_match / adjacent_match / uncertain / excluded`.
- [x] title/skill keywords alone cannot prove core membership.
- [x] accepted P1.6 optional evidence, not a membership gate.
- [x] pending P1.6 not consumed or regenerated.
- [x] exact dependency identity + immutable correction history.
- [x] provider/runtime/stale-dependency failures remain failures, not saved uncertainty.
- [x] CI 1172 passed 608 tests under normal and warnings-as-errors gates.
- [x] bounded real-model evidence preserved.
- [x] broad target: 7/8 expected outcomes overall; only `tGM0` disagreed.
- [x] clarified target: 8/8 post-hoc boundary-calibration outcomes with model/prompt/evidence fixed.
- [x] target-definition lesson recorded; no vacancy-specific prompt patch added.

### C4 — I4 immutable snapshot construction — ACCEPTED / CLOSED

Acceptance:
`docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`

- [x] snapshot requires `completed` or `completed_with_failures` Market run.
- [x] exact I3 membership IDs are validated against run target definition and current I2 source state.
- [x] stale source-version membership is rejected.
- [x] superseded membership correction ancestor is rejected.
- [x] one source job may contribute at most once to one snapshot.
- [x] model membership must consume current translation and current accepted P1.6 when available.
- [x] deterministic source-only membership remains source-only as membership identity.
- [x] I4 derives semantic coverage; callers do not supply trusted coverage authority.
- [x] `accepted / pending / missing / failed / rejected` coverage states are frozen explicitly.
- [x] failed/rejected coverage is scoped to the current source/translation/P1.6 contract boundary.
- [x] only `core_match` enters the primary source-level corpus.
- [x] accepted-semantic core denominator remains narrower and explicit.
- [x] pending/missing/failed/rejected never becomes zero semantic demand.
- [x] historical snapshots remain immutable after later source/membership changes.
- [x] CI 1182 passed Ruff and 617 tests under normal and warnings-as-errors gates.

### C5 — I5 deterministic aggregate profile — NEXT

- [ ] calculate only from one immutable I4 snapshot; no live-current reconstruction.
- [ ] explicit target/snapshot/run/evidence-quality header.
- [ ] qualified core source-posting denominator.
- [ ] accepted-current-P1.6 semantic sub-denominator.
- [ ] preserve core/adjacent/uncertain/excluded and semantic-coverage counts from snapshot authority.
- [ ] source-level employer breadth/concentration with explicit denominator semantics.
- [ ] deterministic P1.6 requirement concept/type/strength support counts.
- [ ] one posting contributes at most once per normalized concept support count.
- [ ] distinct-employer support per semantic concept.
- [ ] accepted responsibility/work evidence counts + exact drill-down without inventing role families.
- [ ] reviewed Canonical Registry mappings may enrich where available; unmapped evidence remains visible.
- [ ] explicit no-repost-adjustment limitation.
- [ ] small-sample/concentration warnings where justified.
- [ ] no model-authored counts, opaque scores, bands, trends, forecasts, or semantic subfamilies.
- [ ] persist immutable deterministic profile through existing `market_aggregate_profiles` contract.
- [ ] focused deterministic tests for denominator, dedup-within-posting, employer breadth and replay integrity.

### C6 — I6 browser + CLI thin workflow — AFTER I5

- [ ] browser primary workflow.
- [ ] same services/state for CLI.
- [ ] one mutable Market operation at a time.
- [ ] Market state remains local/private by default.

### C7 — I7 bounded real acceptance — AFTER I6

- [ ] one representative real local target run.
- [ ] verify acquisition bounds/noise, reuse, membership, denominators, evidence drill-down and partial success.
- [ ] verify clarified target-definition semantics in a real repeated workflow.
- [ ] run all applicable quality gates.
- [ ] close first slice only after acceptance matrix passes.

---

## D. First-slice invariants

Already proven through I4:

- [x] stable target identity vs immutable definition versions.
- [x] target-definition changes do not invalidate generic upstream artifacts.
- [x] target affected-work planning cannot fill from global backlog.
- [x] failed refresh does not imply disappearance or freshness.
- [x] source/translation/P1.6 currentness is exact-dependency aware.
- [x] membership decisions are immutable and correction-aware.
- [x] `uncertain` is a valid bounded membership outcome.
- [x] target membership quality depends on sufficiently explicit target meaning.
- [x] non-core membership dispositions remain outside the primary snapshot denominator.
- [x] pending/missing/failed/rejected P1.6 remains explicit snapshot state rather than zero demand.
- [x] only accepted-current P1.6 forms accepted-semantic snapshot coverage.
- [x] point-in-time snapshot/member identity is immutable.

Still to prove in I5+:

- [ ] every aggregate percentage has recoverable denominator semantics.
- [ ] one posting contributes at most once per concept-support count.
- [ ] distinct-employer support/concentration is calculated deterministically.
- [ ] first profile exposes `qualified source postings`, not unproven `unique demand units`.
- [ ] browser/CLI use the same accepted services/state.
- [ ] one real target run is useful and repeatable end-to-end.

---

## E. Explicitly deferred / not authorized

- [-] another B1 model matrix.
- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable promoted role archetypes.
- [-] P1.6 auto-acceptance.
- [-] first-slice Capability/Work gating.
- [-] automatic repost/new-ID collapse.
- [-] semantic role-subfamily synthesis in first slice.
- [-] persisted model-generated Role-Family Intelligence Report in first slice.
- [-] trend / emerging / forecasting.
- [-] personal readiness/gap/scoring/recommendations.
- [-] Market publication to `corpus/`.
- [-] vector/RAG/graph/autonomous-agent infrastructure.
- [-] generic multi-source/plugin framework before a real second source.

---

## F. Portfolio / release — PARALLEL

- [x] PR0–PR8 repository-side work complete.
- [x] PR9-A repository/public audit complete.
- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` release.
- [x] release/CV/interview package prepared.
- [ ] owner mastery verification.

---

## Exact next action

```text
I5 only
→ deterministic aggregate profile from one immutable I4 snapshot
→ explicit source vs accepted-semantic denominators
→ one-posting-at-most-once support semantics
→ employer breadth/concentration + evidence drill-down
→ persist exact profile through existing immutable store
→ focused tests + state reconciliation
→ only then proceed to I6
```
