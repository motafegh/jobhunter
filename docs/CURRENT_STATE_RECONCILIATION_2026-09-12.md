# JobHunter Current-State Reconciliation — 2026-09-12

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Last reconciled:** 2026-09-17  
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

Market foundation investigation     PASS / COMPLETE
Market I1 domain + persistence      ACCEPTED / CLOSED
Market I2 affected-work planning    ACCEPTED / CLOSED
Market I3 membership qualification ACCEPTED / CLOSED
Market I4 snapshot construction     ACCEPTED / CLOSED
Market I5 aggregate profile         NEXT / ACTIVE PRODUCT FRONTIER
Market I6-I7                        BLOCKED SEQUENTIALLY
Semantic subfamily/report synthesis DEFERRED FROM FIRST SLICE
Market → You                        LATER / NOT AUTHORIZED

Portfolio / release                 PARALLEL
MIT license                         COMPLETE
GitHub metadata/screenshots/release/owner mastery  PENDING
```

Current contracts relevant to the active slice:

```text
parser:                       jobinja-detail-v2
translation:                  english-projection-v2 / lm-studio-translation-v2
English P1.6:                 job-analysis-english-v20 / job-analysis-v5
Capability:                   job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry:           jobhunter-canonical-concept-registry-v1
Work Intelligence:            job-work-intelligence-v2 / job-work-intelligence-v2.0
Market membership:            market-membership-v1 / market-membership-v1.0
Market snapshot:              market-corpus-snapshot-v1
Market aggregate persistence: market-aggregate-profile-v1
Public Corpus:                jobhunter-public-corpus-v1
```

Repository-safe public corpus baseline remains:

```text
known/discovered Jobinja jobs: 353
fetched/parsed detail jobs:      43
current English projections:     21
accepted/current English P1.6:    5
accepted/current Capability:      5
```

---

## 2. Closed historical frontier

P2.2B-B1 remains **CLOSED / NO-PROMOTION / DEFER**.

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

No responsibility concept or claim mappings were created. Do not reopen B1 or select another candidate merely to manufacture promotion.

---

## 3. Market foundation — PASS

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

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

Permanent first-slice rules:

- Jobinja remains the only approved recurring source;
- acquisition/search recall is not target membership truth;
- `core_match | adjacent_match | uncertain | excluded` remain distinct;
- primary source-level corpus is `core_match` only;
- accepted P1.6 is not required for source-level membership;
- accepted-current P1.6 is required for strong semantic prevalence;
- pending/missing/failed/rejected P1.6 never means zero demand;
- Capability/Work are optional, not first-slice gates;
- repost/new-ID automatic collapse remains deferred;
- denominator wording is `qualified source postings`, not `unique demand units`;
- Market state remains local/private by default.

---

## 4. I1-I3 accepted state

Implementation records:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
```

I1 established immutable target/run/membership/snapshot/profile persistence.

I2 established target-scoped source/translation/P1.6 affected-work planning with no global-backlog spill and with `failed refresh != disappearance`.

I3 established target-relative membership qualification with exact dependency reuse, explicit correction history, valid `uncertain`, and optional accepted-P1.6 evidence.

I3 real-model boundary evidence is preserved at:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`

Observed result:

```text
broad target meaning       7/8 expected outcomes; tGM0 sole disagreement
clarified target meaning   8/8 post-hoc boundary-calibration outcomes
```

This is not a population accuracy benchmark. It establishes that material core-vs-adjacent semantics belong in the immutable target definition rather than vacancy-specific prompt patches.

---

## 5. I4 immutable snapshot construction — ACCEPTED / CLOSED

Acceptance record:

`docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`

Implementation:

```text
src/jobhunter/market_snapshot_service.py
tests/test_market_snapshot_service.py
```

I4 now validates exact I3 membership IDs against one terminal Market run and current I2/source/dependency state before writing through the existing immutable snapshot store.

Accepted boundaries:

- snapshots require `completed` or `completed_with_failures` run state;
- membership must belong to the exact run target definition;
- stale source-version memberships are rejected;
- superseded memberships are rejected;
- one source job contributes at most once;
- model membership must still consume the current translation and current accepted P1.6 when available;
- deterministic source-only membership remains source-only as membership identity;
- semantic coverage is derived by I4 rather than trusted from the caller;
- coverage is explicitly `accepted / pending / missing / failed / rejected`;
- failed/rejected coverage is bounded to the current source/translation/P1.6 contract evidence;
- only `core_match` enters the primary source-level corpus;
- accepted-semantic core coverage remains a narrower denominator;
- historical snapshots remain immutable after later source/membership changes.

I4 freezes snapshot evidence-quality metadata such as disposition counts, primary core postings, semantic coverage counts, denominator language, and repost-adjustment status. It does **not** calculate the I5 final Market profile.

Technical acceptance:

```text
head: 4b5e83134202d32ee167f499c3aca9cb43478f56
CI 1182 / 35249049607
Ruff: PASS
pytest: 617 passed
pytest -W error: 617 passed
conclusion: SUCCESS
```

---

## 6. Exact current product action — I5

Current active frontier:

```text
I5 — deterministic Market aggregate profile
```

I5 must compute only from one exact immutable I4 snapshot and the exact historical source/P1.6 identities frozen by that snapshot. It must not rebuild the corpus from today's current state.

Minimum I5 output/authority:

```text
target + definition identity
snapshot + run identity/time
source/search scope
core / adjacent / uncertain / excluded counts
qualified core source-posting denominator
accepted / pending / missing / failed / rejected core P1.6 coverage
accepted-semantic core denominator
raw snapshot member count
repost-adjustment status
distinct employer count
largest-employer contribution/share
freshness/lifecycle/processing warnings
```

For accepted-semantic core members, I5 may deterministically aggregate P1.6 requirements/responsibilities with exact posting/artifact drill-down.

Required invariants:

- one posting supports one normalized concept at most once in concept-support count;
- strength support stays explicit (`required / preferred / contextual / inferred`);
- distinct-employer support is deterministic;
- Registry mappings may enrich reviewed correspondences where already available, but unmapped evidence remains visible;
- no model may author counts, percentages, scores, or denominators;
- no repost collapse, trend, forecasting, role-subfamily clustering, personal scoring, or browser/CLI work in I5.

---

## 7. Sequence

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate                     NEXT
I6  browser + CLI                               BLOCKED BY I5
I7  bounded real local acceptance               BLOCKED BY I6
```

---

## 8. Precedence for older status wording

For present-tense status only, this reconciliation supersedes old statements such as:

```text
B1 active
Market foundation incomplete
I1/I2/I3/I4 next or not implemented
I3 work not pushed / no CI claimed
```

Historical records remain evidence. Do not mass-edit dated history merely because its old `NEXT` action is no longer current.

---

## 9. Current execution owner set

Before I5 work, use:

```text
AGENTS.md
README.md
product/domain/source/architecture + reasoning policy
ROADMAP.md / IMPLEMENTATION_PLAN.md for durable semantics
THIS reconciliation for present-tense status
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md
docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

Use I1-I3 records when a specific dependency/history question requires them; do not repeat accepted investigations.

---

## 10. Current stop lines

During I5:

- do not build I6 browser/CLI workflow;
- do not start I7 operational real-target acceptance;
- do not auto-accept P1.6;
- do not make Capability/Work mandatory Market gates;
- do not invent repost similarity thresholds;
- do not reopen B1/I3 for harmless semantic variation;
- do not promote membership to Canonical Registry/P2.2C/P2.2D;
- do not add semantic role-subfamilies, trends/emerging/forecasting, or personal scoring;
- do not publish Market state to `corpus/`;
- do not add generic source/plugin/vector/RAG/graph/autonomous-agent infrastructure.

---

## 11. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1 ACCEPTED
→ I2 ACCEPTED
→ I3 ACCEPTED
→ I4 ACCEPTED
→ I5 NEXT
→ I6 after I5 acceptance
→ I7 bounded real local acceptance after I6
→ close first Market slice only when I7 acceptance matrix passes
```

This file remains a status-only overlay. It does not replace durable product/domain/source/architecture authority.
