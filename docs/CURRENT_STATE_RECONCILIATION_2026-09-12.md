# JobHunter Current-State Reconciliation — 2026-09-12

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Last reconciled:** 2026-09-16  
**Branch:** `main`  
**Scope:** Present-tense project state and execution routing.  
**Supersedes for current-state reading:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-05.md`

## 1. Current authoritative operating state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2C promoted responsibility       NOT ACTIVE / NOT AUTHORIZED
P2.2D stable role archetypes        LATER / NOT AUTHORIZED
Blueprint v6                        EXPERIMENTAL / HISTORICAL / NON-AUTHORITATIVE

Market / Role-Family research       COMPLETE ENOUGH
Market foundation investigation     PASS / COMPLETE
Market I1 domain + persistence      ACCEPTED / CLOSED
Market I2 source eligibility/plan   NEXT / ACTIVE PRODUCT FRONTIER
Market I3-I7                        NOT ACTIVE YET
Semantic subfamily/report synthesis DEFERRED FROM FIRST SLICE
Market → You                        LATER / NOT AUTHORIZED

Portfolio / release                 parallel track
MIT license                         COMPLETE
GitHub metadata/screenshots/release/owner mastery  PENDING
```

Current accepted/public contracts remain:

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6:                 job-analysis-english-v20 / job-analysis-v5
Original P1.6:                job-analysis-original-v9 / job-analysis-v4
Capability:                   job-capability-intelligence-v9 / job-capability-intelligence-v5
Work Intelligence:            job-work-intelligence-v2 / job-work-intelligence-v2.0
Canonical Registry:           jobhunter-canonical-concept-registry-v1
Public Corpus:                jobhunter-public-corpus-v1
Market snapshot:              market-corpus-snapshot-v1
Market aggregate persistence: market-aggregate-profile-v1
```

Current public-corpus baseline remains:

```text
known/discovered Jobinja jobs: 353
fetched/parsed detail jobs:      43
current English projections:     21
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Accepted P1.6 → Capability anchors remain:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

---

## 2. P2.2B-B1 remains closed

B1 is closed as **NO-PROMOTION / DEFER**.

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

No responsibility concept or claim mappings were created. Do not repeat the `ta9l` translation/extraction/model matrix or select another candidate merely to manufacture promotion.

The retained B1 repairs remain part of the accepted source/P1.6 substrate. B1 is not a prerequisite for continuing the authorized first Market slice.

---

## 3. Market foundation — PASS / COMPLETE

Controlling plan:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Authorized first slice:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

Permanent first-slice boundaries:

- reuse existing Jobinja/source/lifecycle/translation/P1.6 authority;
- target runs must use target-scoped affected-work queues rather than spill budget into unrelated global backlog;
- `core_match | adjacent_match | uncertain | excluded` remain distinct;
- accepted P1.6 is not required for source-level membership;
- accepted/current P1.6 is required for strong semantic prevalence statistics;
- missing/pending/failed P1.6 remains explicit and never means zero demand;
- Capability and Work are not mandatory first-slice gates;
- automatic repost/new-ID collapse remains deferred;
- denominator wording is `qualified source postings`, not `unique demand units`;
- Market state remains local/private by default.

---

## 4. Market I1 — ACCEPTED / CLOSED

Acceptance record:

`docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

Implemented:

```text
src/jobhunter/market_models.py
src/jobhunter/market_store.py
tests/test_market_store.py
tests/test_market_i1_invalidation.py
```

I1 established the following SQLite/history owners:

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

Accepted I1 invariants:

- stable target identity is separate from immutable definition versions;
- normalized identical definitions reuse the same definition version;
- a materially changed target definition creates a new immutable version;
- target-definition changes do not invalidate generic source/translation/P1.6 artifacts;
- research runs preserve exact target definition, controls and partial-success ledger state;
- membership reuse is keyed by exact target/source/classifier/artifact dependencies;
- changed membership decisions require explicit superseding history instead of overwrite;
- P1.6 may feed membership only when it belongs to the exact source/translation chain and is accepted;
- snapshot/member history is immutable;
- `accepted / pending / missing / failed / rejected` semantic coverage remains explicit;
- only `core_match` is persisted as primary-corpus inclusion at this state layer;
- aggregate-profile persistence is immutable and deterministic over exact snapshot + contract;
- conflicting deterministic replay for one snapshot/contract is an integrity error.

Final technical I1 head before status reconciliation:

```text
f0cded55a9887c061898d0dcab7f5e6b10300d8e
```

Final technical acceptance CI:

```text
run 1160 / 35108236384
package install                   PASS
pip dependency consistency        PASS
installed entrypoint smoke        PASS
Ruff                              PASS
pytest                            PASS
pytest -W error                   PASS
conclusion                        SUCCESS
```

I1 does **not** claim that target source eligibility, affected-work planning, semantic membership qualification, production snapshot construction, aggregate calculation, browser/CLI workflow, or real local acceptance are complete. Those remain I2-I7 responsibilities.

---

## 5. Exact current product action — I2

Current active product frontier:

```text
I2 — target-scoped source eligibility + affected-work planning
```

I2 must answer one bounded question:

> Given one immutable target definition and current JobHunter source/runtime state, which target candidates are source-eligible and which target-scoped source/translation/P1.6 work is missing or stale, without consuming unrelated global backlog and without treating refresh failure as disappearance?

I2 should compose existing owners rather than create parallel authority:

```text
search_registry / config search definitions
jobinja discovery/sync/batch
job catalog
job-detail observations
lifecycle
source storage
translation store/service
P1.6 currentness/store/service
phase1_run only as orchestration precedent
Market I1 domain/store
```

I2 acceptance must prove at minimum:

- one target-scoped candidate/source-state representation;
- deterministic source eligibility from current parsed source + lifecycle/freshness evidence;
- target-only missing-detail selection;
- target-only refresh-due selection;
- target-only translation affected-work selection;
- target-only P1.6 affected-work selection;
- exact reuse recognition for already-current artifacts;
- explicit reusable/needed/unavailable/failed/remaining state suitable for a later run ledger;
- `failed refresh != disappearance`;
- no semantic target-membership inference yet.

Important regression boundary:

> Global Phase-1 helpers may legitimately fill remaining capacity from global backlog. I2 must not inherit that behavior for a target Market run.

---

## 6. First-slice sequence from this checkpoint

```text
I1  domain + SQLite persistence                  ACCEPTED / CLOSED
I2  target source eligibility / affected work    NEXT
I3  membership qualification                     BLOCKED BY I2
I4  immutable snapshot construction              BLOCKED BY I3
I5  deterministic aggregate profile              BLOCKED BY I4
I6  browser + CLI thin workflow                  BLOCKED BY I5
I7  bounded real local acceptance                BLOCKED BY I6
```

Do not jump ahead merely because I1 already provides persistence tables for later responsibilities.

---

## 7. Precedence for older status wording

For **present-tense status only**, this reconciliation supersedes older statements such as:

```text
B1 active / ta9l P1.6 next
Market foundation blocked/not started
first Market slice implementation not authorized
I1 next / not implemented
```

Durable product/domain/source/architecture semantics in older controlling documents remain applicable unless explicitly superseded by accepted later evidence.

In particular:

- `docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md` is a closed B1 plan;
- `docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md` is an executed protocol;
- `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md` remains the long-term Market plan;
- `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md` is the accepted I1 evidence record;
- `docs/EXECUTION_TODO.md` and `docs/WORKING_MEMORY.md` route the next bounded implementation increment.

Do not mass-edit dated history merely because its historical `NEXT` action is no longer current.

---

## 8. Current execution owner set

Before I2 work, use:

```text
AGENTS.md
README.md
product/domain/source/architecture + reasoning policy
ROADMAP.md / IMPLEMENTATION_PLAN.md for durable semantics
THIS reconciliation for present-tense status
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

Load older research records only when a specific I2 decision requires them; do not repeat the foundation investigation.

---

## 9. Current stop lines

During I2:

- do not implement semantic membership classification yet;
- do not assemble production Market snapshots yet;
- do not calculate the final Market aggregate yet;
- do not build browser/report UI yet;
- do not auto-accept P1.6;
- do not make Capability/Work mandatory Market gates;
- do not invent repost similarity thresholds;
- do not reopen B1 or start P2.2C/P2.2D promotion;
- do not add trends/emerging/forecasting;
- do not add personal readiness/gap/scoring/recommendations;
- do not publish Market state to `corpus/`;
- do not add generic source/plugin/vector/RAG/graph/autonomous-agent infrastructure.

---

## 10. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1 ACCEPTED / CLOSED
→ I2 NEXT
→ I3-I6 only after their preceding increment is accepted
→ I7 bounded local real acceptance
→ close first Market slice only when its acceptance matrix passes
```

This file remains a status-only overlay. It does not replace durable product/domain/source/architecture authority or rewrite historical evidence.
