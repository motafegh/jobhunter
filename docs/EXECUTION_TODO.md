# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-16  
**Active working branch:** `main`  
**Current-state reconciliation:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**I1 acceptance:** `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`  
**I2 acceptance:** `docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md`  
**Current product gate:** MARKET I1 + I2 ACCEPTED / I3 NEXT  
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

Acceptance:
`docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

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

Acceptance:
`docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md`

- [x] exact target candidate/source-state representation.
- [x] deterministic current-active source eligibility.
- [x] target-only missing-detail selection.
- [x] target-only refresh/repair selection.
- [x] failed refresh does not freshen evidence or imply disappearance.
- [x] unchanged successful parsed check refreshes freshness without a new semantic version.
- [x] `possibly_unavailable` can remain usable with explicit warning when evidence is recent.
- [x] `expired` / `removed` excluded from current-active source eligibility.
- [x] target-only translation affected-work planning and exact artifact reuse.
- [x] target-only P1.6 affected-work planning and exact source+translation+contract reuse.
- [x] pending-current P1.6 preserved as pending-review rather than regenerated.
- [x] new source semantic version invalidates old downstream currentness without deleting history.
- [x] explicit selected / remaining / unavailable / blocked planning ledger.
- [x] critical global-backlog spill regressions covered.
- [x] no semantic membership inference added.
- [x] CI 1167 green through `pytest -W error`.

### C3 — I3 membership qualification — NEXT

- [ ] define one explicit first-slice membership classifier contract/version.
- [ ] consume only I2 source-eligible candidates.
- [ ] apply deterministic target constraints before any model call.
- [ ] use current source title/detail as factual authority.
- [ ] use current English projection only where language/semantic reasoning requires it.
- [ ] use accepted-current P1.6 opportunistically as stronger evidence, never as a prerequisite.
- [ ] support exactly `core_match / adjacent_match / uncertain / excluded`.
- [ ] preserve `uncertain` as a successful bounded outcome.
- [ ] store exact target/source/classifier/translation/P1.6 dependency identity through `MarketStore`.
- [ ] reuse exact membership decisions when dependencies match.
- [ ] require explicit superseding correction instead of hidden overwrite.
- [ ] title/keyword match alone must not prove core membership.
- [ ] Capability/Work remain optional and must not become gates.
- [ ] add deterministic/fake-provider boundary tests using representative core/adjacent/excluded/uncertain cases.
- [ ] do not auto-promote membership into Canonical Registry/P2.2C/P2.2D taxonomy.

### C4 — I4 immutable snapshot construction — AFTER I3

- [ ] freeze exact definition/run/membership/source/semantic coverage identities.
- [ ] keep core/adjacent/uncertain/excluded separate.
- [ ] preserve accepted/pending/missing/failed/rejected P1.6 coverage.

### C5 — I5 deterministic aggregate profile — AFTER I4

- [ ] explicit target/corpus/evidence-quality header.
- [ ] qualified core source-posting denominator.
- [ ] accepted-current-P1.6 semantic sub-denominator.
- [ ] requirement concept/type/strength counts.
- [ ] employer breadth/concentration warnings.
- [ ] accepted responsibility/work drill-down.
- [ ] explicit no-repost-adjustment limitation.
- [ ] no model-authored counts or opaque scores.

### C6 — I6 browser + CLI thin workflow — AFTER I5

- [ ] browser primary workflow.
- [ ] same services/state for CLI.
- [ ] one mutable Market operation at a time.
- [ ] Market state remains local/private by default.

### C7 — I7 bounded real acceptance — AFTER I6

- [ ] one representative real local target run.
- [ ] verify acquisition bounds/noise, reuse, membership, denominators, evidence drill-down and partial success.
- [ ] run all applicable quality gates.
- [ ] close first slice only after acceptance matrix passes.

---

## D. First-slice invariants

Already proven:

- [x] stable target identity vs immutable definition versions.
- [x] target-definition changes do not invalidate generic upstream artifacts.
- [x] target affected-work planning is target-scoped and does not fill from global backlog.
- [x] failed refresh does not imply disappearance.
- [x] source/translation/P1.6 currentness is exact-dependency aware.
- [x] pending current P1.6 is not silently regenerated or treated as accepted.
- [x] snapshot/member/profile persistence is immutable.
- [x] ordinary I1/I2 CI needs no Jobinja or LM Studio network/model access.

Still to prove:

- [ ] non-core membership dispositions cannot silently enter core denominator.
- [ ] `uncertain` behaves as valid successful classification.
- [ ] pending/missing/failed P1.6 never becomes zero semantic demand.
- [ ] only accepted-current P1.6 contributes to strong semantic statistics.
- [ ] every percentage has recoverable denominator semantics.
- [ ] one posting contributes at most once per concept-support count.
- [ ] first slice says `qualified source postings`, not unproven `unique demand units`.

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
I3 only
→ membership qualification contract + service
→ deterministic constraints first
→ bounded semantic relevance only where needed
→ exact dependency persistence/reuse
→ focused boundary tests
→ reconcile state
→ only then proceed to I4
```
