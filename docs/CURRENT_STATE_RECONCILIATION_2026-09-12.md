# JobHunter Current-State Reconciliation — 2026-09-12

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Last reconciled:** 2026-09-14  
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
Market research consolidation       COMPLETE
Market foundation investigation     PASS / COMPLETE
First Market vertical slice         AUTHORIZED / NEXT PRODUCT IMPLEMENTATION
Market implementation completion    NOT YET ACCEPTED
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
```

Current public-corpus baseline:

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

## 2. Final P2.2B-B1 disposition

B1 is closed as **NO-PROMOTION / DEFER**.

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

Exact outcome:

```text
ta9l source detail 25
→ English projection 40 reviewed/published
→ attempt 98 failed without artifact
→ attempt 99 produced artifact 47
→ artifact 47 materially incomplete and explicitly rejected/archived
→ deterministic source-coverage defects reproduced and repaired
→ depth-boundary defect reproduced and repaired
→ attempts 100 and 101 failed without an acceptable artifact
→ no accepted/current ta9l P1.6
→ no canonical responsibility concept
→ no claim mappings
→ B1 NO-PROMOTION / DEFER
```

The retained coverage/depth repairs passed the full 552-test warnings-as-errors suite recorded in the recovery evidence. The five accepted P1.6 anchors were not regenerated.

Do not:

- repeat `ta9l` translation or extraction to force a B1 promotion;
- select another B1 candidate without a new explicit focused decision;
- treat the defer result as proof that the proposed cross-job responsibility identity was semantically incompatible;
- infer that `ta9l` lacks duties merely because accepted P1.6 could not be produced within the bounded recovery.

The old B1 plan and pre-local records remain historical evidence; their former `NEXT` actions no longer control execution.

---

## 3. Market foundation investigation — COMPLETE

Controlling future plan:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Research consolidation:

`docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`

Prepared investigation protocol:

`docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`

Final investigation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

The authorized first slice is:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

### First-slice permanent boundaries

- reuse current Jobinja source identity/provenance, lifecycle, observation, translation and P1.6 machinery;
- target runs must use target-scoped affected-work queues rather than spill bounded budgets into unrelated global backlog;
- source-level membership uses `core_match | adjacent_match | uncertain | excluded`;
- accepted P1.6 is a strong semantic-statistics boundary, not a prerequisite for source-level target membership;
- core source postings and core+accepted-P1.6 are distinct denominators;
- pending/missing/failed P1.6 must remain visible and never become zero demand;
- Capability and Work Intelligence are not mandatory first-slice dependencies;
- reviewed Registry mappings may enrich where available but unmapped evidence remains valid;
- first-slice repost/new-ID collapse is deliberately deferred because no defensible real Jobinja pair set established an authority rule;
- denominator wording is `qualified source postings`, not `unique demand units`;
- snapshot history is immutable;
- numeric aggregation is deterministic;
- Market state remains local by default.

### Explicitly outside the authorized first slice

```text
model-generated/persisted Role-Family Intelligence Report
semantic role-subfamily synthesis
P2.2C/P2.2D promoted taxonomy
repost/new-ID automatic collapse
trend / emerging / forecasting
personal Market → You scoring/recommendations
Market publication
new workflow/vector/graph/RAG/agent infrastructure
```

Implementation completion is not pre-accepted. A bounded real local target run remains part of first-slice acceptance after the source implementation exists.

---

## 4. Exact next product action

Follow the implementation order from the foundation decision:

```text
I1  Target/definition/run/membership/snapshot/profile domain + SQLite persistence
→ I2 target-scoped source eligibility and affected-work planning
→ I3 membership qualification service/contract
→ I4 immutable snapshot construction
→ I5 deterministic target aggregate profile
→ I6 browser + CLI thin workflow
→ I7 bounded local real acceptance + reuse rerun
```

Start with **I1**. Do not implement later semantic report/subfamily responsibilities during I1 merely because they appear in the long-term Market plan.

---

## 5. Parallel portfolio / release state

```text
PR0–PR8    COMPLETE / repository-side complete as recorded
PR9-A      final repository/public consistency audit COMPLETE
PR9-B      MIT license COMPLETE
           GitHub description/topics PENDING
           real browser screenshots + privacy review PENDING
PR9-C      intentional v0.1.0 tag/release PENDING
PR9-D      release/CV/interview package COMPLETE
PR9-E      owner mastery PREPARED / NOT VERIFIED
```

Portfolio work remains independent and may not silently alter semantic contracts or broaden the authorized Market slice.

---

## 6. Precedence for older status wording

Several controlling/historical documents intentionally retain wording that was correct at their original checkpoint. For **present-tense status only**, this reconciliation supersedes statements such as:

```text
Phase 1 active
P2.1/P2.2A not closed
P2.2B-B1 active / ta9l P1.6 next
Market foundation investigation blocked by B1
Market foundation investigation not started
license undecided
```

Their durable product/design/architecture semantics remain controlling where not superseded by a later accepted decision.

In particular:

- `docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md` is now a closed B1 plan;
- `docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md` is an executed investigation protocol, not the current next action;
- `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md` remains the controlling long-term Market direction, but its old B1-open status wording is superseded;
- `docs/PORTFOLIO_RELEASE_STATE_AMENDMENT_2026-09-06_MIT_LICENSE.md` supersedes older license-pending wording.

Do not mass-edit dated experiments/incidents/working memories merely because their historical next action is no longer current.

---

## 7. Current execution owner set

Before implementing the first Market slice, use:

```text
AGENTS.md
README.md
product/domain/source/architecture + reasoning policy
ROADMAP.md / IMPLEMENTATION_PLAN.md for durable semantics
THIS reconciliation for present-tense status
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md
docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

Load the entry protocol and six research records only when a specific implementation decision needs their detail; do not repeat the broad investigation.

---

## 8. Current stop lines

During the authorized first Market slice:

- do not reopen B1 or force another `ta9l` P1.6 matrix;
- do not implement P2.2C/P2.2D promoted families/archetypes;
- do not make Capability/Work mandatory Market gates;
- do not auto-accept P1.6;
- do not claim repost-adjusted unique demand;
- do not add trends/emerging/forecasting;
- do not add personal evidence/readiness/gap/scoring/recommendations;
- do not publish Market state without a separate privacy/publication decision;
- do not add graph/vector/RAG/autonomous-agent infrastructure without demonstrated need;
- do not build a generic source/plugin framework before a real second approved source exists.

---

## 9. Current routing

```text
B1 CLOSED / NO-PROMOTION / DEFER
→ Market foundation investigation PASS
→ first vertical slice AUTHORIZED
→ implement I1 next
→ continue I2–I6 only within the authorized boundary
→ run I7 bounded local real acceptance
→ close the slice only if its implementation-specific acceptance matrix passes
```

This file remains a status-only overlay. It does not replace durable product/domain/source/architecture authority or rewrite historical evidence.
