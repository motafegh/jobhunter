# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-14  
**Active working branch:** `main`  
**Current-state reconciliation:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**Current product gate:** MARKET FIRST VERTICAL SLICE AUTHORIZED / I1 NEXT  
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
[~] in progress / implemented but acceptance incomplete
[x] accepted/completed for stated scope
[!] rejected/blocking defect
[-] deliberately deferred
```

---

## A. Accepted foundation — CLOSED

- [x] Jobinja discovery/acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2` parser and cautious lifecycle semantics.
- [x] `english-projection-v2` / `lm-studio-translation-v2`.
- [x] English P1.6 `job-analysis-english-v20 / job-analysis-v5`.
- [x] Capability `job-capability-intelligence-v9 / job-capability-intelligence-v5`.
- [x] Phase 1 CLOSED.
- [x] P2.1 Canonical Registry CLOSED / accepted.
- [x] P2.2A Job Work Intelligence v2 CLOSED / accepted.

Accepted/current P1.6 → Capability anchors:

```text
tG9K 36 → 11
t4jp 37 → 12
tmBK 39 → 13
t4qV 44 → 14
tmyX 46 → 15
```

Public-corpus baseline:

```text
known jobs:           353
fetched details:       43
English projections:   21
accepted P1.6:          5
Capability:             5
```

---

## B. P2.2B-B1 selective responsibility pilot — CLOSED / NO-PROMOTION / DEFER

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

- [x] selected `ta9l` as the one bounded additional evidence-bearing job.
- [x] created/reviewed English projection 40 on source detail 25.
- [x] attempt 98 failed without artifact.
- [x] artifact 47 from attempt 99 was materially incomplete and explicitly rejected/archived.
- [x] deterministic coverage-loss defects were reproduced and repaired.
- [x] explicit `deep understanding / deep knowledge` depth handling was repaired without changing historical validator vocabulary.
- [x] attempts 100 and 101 ended without an acceptable P1.6 artifact.
- [x] full recorded quality gate reached 552 passing tests with warnings as errors.
- [x] no canonical responsibility concept or mappings were created.
- [x] B1 disposition = **NO-PROMOTION / DEFER**.

Do not repeat `ta9l` translation/extraction or search another pair merely to manufacture a B1 promotion.

P2.2C/P2.2D promoted taxonomy remains unauthorized.

---

## C. Market / Role-Family foundation — COMPLETE / PASS

Research consolidation:

`docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`

Investigation protocol:

`docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`

Final decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

- [x] Q1–Q12 resolved for the first implementation slice.
- [x] representative source/membership boundary cases inspected.
- [x] target definition identity/version boundary decided.
- [x] target-aware orchestration/reuse boundary decided.
- [x] lifecycle/source snapshot eligibility decided.
- [x] membership states confirmed: `core_match / adjacent_match / uncertain / excluded`.
- [x] source-level membership separated from accepted-P1.6 semantic denominator.
- [x] P1.6 accepted/pending/missing/failed coverage policy decided.
- [x] repost/new-ID automatic collapse explicitly deferred for lack of defensible real evidence.
- [x] minimal SQLite persistence responsibilities decided.
- [x] deterministic first aggregate profile decided.
- [x] Capability/Work are not mandatory first-slice dependencies.
- [x] semantic role-subfamily synthesis deferred from first slice.
- [x] browser/CLI repeated-use workflow decided.
- [x] first-slice implementation acceptance matrix decided.
- [x] `FOUNDATION INVESTIGATION: PASS`.
- [x] `FIRST VERTICAL SLICE: AUTHORIZED`.

---

## D. Authorized first Market vertical slice — ACTIVE / NOT IMPLEMENTED YET

Exact authorized responsibility:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

### D1 — I1 domain + SQLite persistence — NEXT

- [ ] define minimal typed domain records/contracts for TargetMarket, definition version, research run, membership, snapshot/member and aggregate profile.
- [ ] add bounded SQLite tables/migrations using existing repository patterns.
- [ ] enforce immutable definition/snapshot/profile history.
- [ ] preserve exact upstream dependency IDs rather than copying source/P1.6 payloads.
- [ ] prove target-definition changes do not invalidate generic source/translation/P1.6 artifacts.
- [ ] add deterministic store/domain tests.

### D2 — I2 target-scoped eligibility / affected-work planning — AFTER I1

- [ ] compose existing Jobinja discovery/detail/lifecycle/observation owners.
- [ ] ensure bounded target runs do not consume unrelated global missing/refresh/model backlog.
- [ ] reuse current translation/P1.6 artifacts by exact existing identity.
- [ ] preserve partial-success stage ledger.
- [ ] preserve `failed refresh != disappearance`.

### D3 — I3 membership qualification — AFTER I2

- [ ] deterministic eligibility first.
- [ ] bounded semantic relevance only where necessary.
- [ ] support `core_match / adjacent_match / uncertain / excluded`.
- [ ] store exact target/source/classifier/artifact dependency identity.
- [ ] accepted P1.6 may strengthen membership but must not be required for source-level membership.
- [ ] Capability/Work must not become mandatory gates.

### D4 — I4 immutable snapshot — AFTER I3

- [ ] freeze exact definition version, members, source versions, membership decisions and semantic coverage state.
- [ ] preserve core/adjacent/uncertain/excluded counts and P1.6 coverage.
- [ ] keep old snapshots immutable after source/target/contract changes.

### D5 — I5 deterministic aggregate profile — AFTER I4

- [ ] explicit target/corpus/evidence-quality header.
- [ ] qualified core source-posting denominator.
- [ ] accepted-current-P1.6 semantic sub-denominator.
- [ ] requirement concept/type/strength support counts.
- [ ] distinct-employer support and concentration warnings.
- [ ] accepted responsibility/work evidence drill-down.
- [ ] explicit repost/new-ID adjustment warning.
- [ ] no model-authored counts or opaque scores.

### D6 — I6 browser + CLI thin workflow — AFTER I5

- [ ] browser primary: target → definition version → preview → run → ledger → membership → snapshot/profile → evidence drill-down/history.
- [ ] reuse existing one-mutable-web-operation pattern.
- [ ] CLI exposes same underlying services/state for advanced inspection/automation.
- [ ] Market state remains local; no implicit corpus publication.

### D7 — I7 bounded real acceptance — AFTER I6

- [ ] run one representative real target locally.
- [ ] verify acquisition bounds/noise are visible rather than hidden.
- [ ] verify unchanged rerun reuses upstream work.
- [ ] verify membership and denominator display.
- [ ] verify missing/pending/failed P1.6 remains explicit.
- [ ] verify evidence drill-down.
- [ ] verify partial success.
- [ ] run complete applicable quality gates.
- [ ] close the slice only if the implementation-specific acceptance matrix passes.

---

## E. First-slice invariants

- [ ] stable target identity is separate from immutable definition versions.
- [ ] target-definition change does not invalidate generic source/translation/P1.6.
- [ ] target run queues are target-scoped.
- [ ] failed refresh never means disappearance by itself.
- [ ] `adjacent_match`, `uncertain`, and `excluded` never silently enter core prevalence.
- [ ] missing/pending/failed P1.6 never means zero semantic demand.
- [ ] only accepted-current P1.6 contributes to strong semantic statistics.
- [ ] every percentage has recoverable denominator semantics.
- [ ] one posting contributes at most once per concept-support count.
- [ ] snapshots are immutable.
- [ ] aggregate profile references exact snapshot/contract identity.
- [ ] first slice uses `qualified source postings`, not unproven `unique demand units`.
- [ ] ordinary CI requires no Jobinja/LM Studio network/model access.

---

## F. Explicitly deferred / not authorized

- [-] another B1 responsibility-promotion/model matrix.
- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable promoted role archetypes.
- [-] first-slice Capability/Work gating.
- [-] P1.6 auto-acceptance.
- [-] automatic repost/new-ID collapsing.
- [-] semantic role-subfamily synthesis in the first slice.
- [-] persisted model-generated Role-Family Intelligence Report in the first slice.
- [-] trend / `emerging` / forecasting.
- [-] personal evidence/readiness/gap/scoring/recommendations.
- [-] Market publication to `corpus/`.
- [-] vector/RAG/graph/autonomous-agent infrastructure.
- [-] generic multi-source/plugin framework before a real second source.

---

## G. Portfolio / release — PARALLEL

- [x] PR0–PR8 repository-side work complete as recorded.
- [x] PR9-A final repository/public audit complete.
- [x] MIT license decision/application complete.
- [ ] GitHub description/topics settings action.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/GitHub release after remaining blockers/final CI.
- [x] release/CV/interview package prepared.
- [ ] owner mastery verification.

Portfolio work cannot broaden the Market implementation authorization.

---

## Exact next action

```text
implement Market first-slice I1
→ domain models + SQLite persistence
→ deterministic tests
→ reconcile docs/working memory
→ then proceed to I2 only if I1 is clean
```
