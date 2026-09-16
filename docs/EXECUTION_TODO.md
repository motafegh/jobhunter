# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-16  
**Active working branch:** `main`  
**Current-state reconciliation:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**I1 acceptance:** `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`  
**Current product gate:** MARKET I1 ACCEPTED / I2 NEXT  
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
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.

Do not reopen B1 or manufacture another responsibility-promotion/model matrix merely to obtain a promotion.

---

## B. Market / Role-Family foundation — COMPLETE / PASS

- [x] Q1–Q12 resolved for the first implementation slice.
- [x] `FOUNDATION INVESTIGATION: PASS`.
- [x] `FIRST VERTICAL SLICE: AUTHORIZED`.
- [x] source-level membership separated from accepted-P1.6 semantic denominator.
- [x] membership states fixed to `core_match / adjacent_match / uncertain / excluded` for the first slice.
- [x] Capability/Work are not mandatory first-slice dependencies.
- [x] automatic repost/new-ID collapse deferred pending defensible real evidence.
- [x] semantic role-subfamily/report synthesis deferred from first slice.

---

## C. Authorized first Market vertical slice — ACTIVE

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

### C1 — I1 domain + SQLite persistence — ACCEPTED / CLOSED

Acceptance record:

`docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

- [x] minimal typed Market domain records/contracts.
- [x] bounded SQLite persistence using the existing source → translation → analysis dependency chain.
- [x] stable target identity separated from immutable target-definition versions.
- [x] canonical definition fingerprint/version reuse.
- [x] research-run controls + stage ledger + running/terminal lifecycle.
- [x] immutable membership decisions with exact dependency identity and explicit correction history.
- [x] optional P1.6 membership evidence requires the exact accepted source/translation chain.
- [x] immutable snapshot/member history.
- [x] explicit accepted/pending/missing/failed/rejected semantic-coverage vocabulary.
- [x] only `core_match` is persisted as primary-corpus inclusion at this layer.
- [x] immutable deterministic aggregate-profile persistence over exact snapshot + contract.
- [x] target-definition change proven not to invalidate generic source/translation/P1.6 artifacts.
- [x] deterministic I1 tests.
- [x] final I1 CI 1160 passed install, dependency check, entrypoint smoke, Ruff, pytest and `pytest -W error`.

### C2 — I2 target-scoped source eligibility + affected-work planning — NEXT

- [ ] define one target-scoped candidate/source-state read model over existing Jobinja/source/lifecycle owners.
- [ ] compose existing discovery/detail/lifecycle/observation semantics rather than adding a second acquisition authority.
- [ ] prove target-run missing-detail selection cannot spill into unrelated global backlog.
- [ ] prove target-run refresh-due selection cannot spill into unrelated global backlog.
- [ ] plan translation only for target candidates missing the effective current English projection.
- [ ] plan P1.6 only for target candidates with current English evidence and no matching current artifact.
- [ ] reuse current translation/P1.6 artifacts by their existing exact identities.
- [ ] preserve explicit counts for reused / needed / unavailable / failed / remaining affected work.
- [ ] preserve `failed refresh != disappearance`.
- [ ] keep source eligibility deterministic; do not implement semantic membership inference yet.
- [ ] add focused deterministic tests for target-scoped selection/currentness/partial-success planning.

### C3 — I3 membership qualification — AFTER I2

- [ ] deterministic eligibility first.
- [ ] bounded semantic relevance only where necessary.
- [ ] support `core_match / adjacent_match / uncertain / excluded`.
- [ ] accepted P1.6 may strengthen membership but is not required for source-level membership.
- [ ] Capability/Work remain optional, not gates.

### C4 — I4 immutable snapshot construction — AFTER I3

- [ ] freeze exact definition, run, memberships, source versions and semantic coverage.
- [ ] keep core/adjacent/uncertain/excluded separate.
- [ ] keep historical snapshots immutable after source/target/contract changes.

### C5 — I5 deterministic aggregate profile — AFTER I4

- [ ] explicit target/corpus/evidence-quality header.
- [ ] qualified core source-posting denominator.
- [ ] accepted-current-P1.6 semantic sub-denominator.
- [ ] requirement concept/type/strength counts.
- [ ] employer breadth/concentration warnings.
- [ ] accepted responsibility/work evidence drill-down.
- [ ] explicit no-repost-adjustment limitation.
- [ ] no model-authored counts or opaque scores.

### C6 — I6 browser + CLI thin workflow — AFTER I5

- [ ] browser primary target/run/report workflow.
- [ ] reuse existing one-mutable-operation behavior.
- [ ] CLI uses the same services/state.
- [ ] Market state stays local/private by default.

### C7 — I7 bounded real acceptance — AFTER I6

- [ ] one representative real local target run.
- [ ] verify acquisition bounds/noise visibility.
- [ ] verify unchanged rerun reuse.
- [ ] verify membership/denominator/semantic-coverage display.
- [ ] verify evidence drill-down and partial success.
- [ ] run all applicable quality gates.
- [ ] close the first slice only after the implementation-specific acceptance matrix passes.

---

## D. First-slice invariants

Already proven in I1:

- [x] stable target identity is separate from immutable definition versions.
- [x] target-definition change does not invalidate generic source/translation/P1.6 artifacts.
- [x] membership decisions are immutable and exact-dependency keyed.
- [x] snapshots/members are immutable.
- [x] aggregate profile references exact snapshot/contract identity and rejects conflicting deterministic replay.
- [x] ordinary I1 CI requires no Jobinja or LM Studio network/model access.

Still to prove across later increments:

- [ ] target-run affected work is target-scoped.
- [ ] failed refresh never means disappearance by itself.
- [ ] `adjacent_match`, `uncertain`, and `excluded` never enter final core prevalence silently.
- [ ] pending/missing/failed P1.6 never becomes zero semantic demand.
- [ ] only accepted-current P1.6 contributes to strong semantic statistics.
- [ ] every percentage has recoverable denominator semantics.
- [ ] one posting contributes at most once per concept-support count.
- [ ] first slice says `qualified source postings`, not unproven `unique demand units`.

---

## E. Explicitly deferred / not authorized

- [-] another B1 responsibility-promotion/model matrix.
- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable promoted role archetypes.
- [-] P1.6 auto-acceptance.
- [-] first-slice Capability/Work gating.
- [-] automatic repost/new-ID collapsing.
- [-] semantic role-subfamily synthesis in the first slice.
- [-] persisted model-generated Role-Family Intelligence Report in the first slice.
- [-] trend / `emerging` / forecasting.
- [-] personal evidence/readiness/gap/scoring/recommendations.
- [-] Market publication to `corpus/`.
- [-] vector/RAG/graph/autonomous-agent infrastructure.
- [-] generic multi-source/plugin framework before a real second source.

---

## F. Portfolio / release — PARALLEL

- [x] PR0–PR8 repository-side work complete as recorded.
- [x] PR9-A final repository/public audit complete.
- [x] MIT license complete.
- [ ] GitHub description/topics settings action.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/GitHub release.
- [x] release/CV/interview package prepared.
- [ ] owner mastery verification.

Portfolio work cannot broaden Market implementation authorization.

---

## Exact next action

```text
I2 only
→ target-scoped source eligibility + affected-work planning
→ compose existing source/lifecycle/translation/P1.6 currentness owners
→ deterministic focused tests
→ reconcile state
→ only then proceed to I3
```
