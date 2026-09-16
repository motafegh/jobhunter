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
Market I2 affected-work planning    ACCEPTED / CLOSED
Market I3 membership qualification NEXT / ACTIVE PRODUCT FRONTIER
Market I4-I7                        NOT ACTIVE YET
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

---

## 2. P2.2B-B1 remains closed

B1 is closed as **NO-PROMOTION / DEFER**.

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

No responsibility concept or claim mappings were created. Do not repeat the `ta9l` extraction/model matrix or choose another B1 candidate merely to manufacture promotion.

---

## 3. Market foundation — PASS / COMPLETE

Controlling plan:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

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

Permanent boundaries:

- reuse existing Jobinja/source/lifecycle/translation/P1.6 authority;
- target runs must never fill unused budgets from unrelated global backlog;
- `core_match | adjacent_match | uncertain | excluded` remain distinct;
- accepted P1.6 is not required for source-level membership;
- accepted-current P1.6 is required for strong semantic prevalence;
- missing/pending/failed P1.6 remains explicit and never means zero demand;
- Capability and Work are not mandatory first-slice gates;
- automatic repost/new-ID collapse remains deferred;
- denominator wording is `qualified source postings`, not `unique demand units`;
- Market state remains local/private by default.

---

## 4. Market I1 — ACCEPTED / CLOSED

Acceptance:

`docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

Accepted I1 responsibilities:

- stable target identity separated from immutable target-definition versions;
- immutable Market run/membership/snapshot/member/profile history;
- exact upstream source/translation/P1.6 dependency references;
- target-definition evolution does not invalidate generic upstream artifacts;
- deterministic aggregate-profile persistence over exact snapshot + contract.

Technical acceptance:

```text
head: f0cded55a9887c061898d0dcab7f5e6b10300d8e
CI 1160 / 35108236384
Ruff / pytest / pytest -W error: PASS
```

---

## 5. Market I2 — ACCEPTED / CLOSED

Acceptance:

`docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md`

Implemented:

```text
src/jobhunter/job_detail_observations.py
src/jobhunter/market_affected_work.py
tests/test_market_affected_work.py
```

I2 established a read-only target-scoped affected-work planning boundary.

### Accepted target-scope behavior

The planner receives an exact persisted target candidate set and never fills unused capacity from unrelated global jobs.

It plans, only within that target set:

```text
missing source details
refresh/repair work
English projection work
P1.6 work
```

Target work may remain explicitly `remaining` even when unrelated global backlog exists.

### Accepted source/freshness behavior

Source state is deterministic over current source/lifecycle/observation evidence.

```text
current
missing_detail
refresh_due
invalid_current_detail
expired
removed
ineligible_lifecycle
```

Freshness uses the latest successful parsed detail check, falling back to the current parsed detail timestamp when no successful observation exists.

Therefore:

```text
failed refresh != disappearance
failed refresh != fresh evidence
```

A recent failed retry leaves prior valid evidence preserved and may leave the job refresh-due. An unchanged successful parsed check refreshes freshness without creating a new semantic source version.

`possibly_unavailable` may remain usable when recent valid evidence exists, with an explicit warning. `expired` and `removed` are outside current-active source eligibility.

### Accepted downstream currentness behavior

Only source-ready target candidates enter downstream planning.

Current translation reuse follows the existing exact provider/model/schema identity.

Current P1.6 reuse follows:

```text
exact current source detail
+ exact current English projection
+ configured model
+ job-analysis-english-v20
+ job-analysis-v5
```

Pending current P1.6 is preserved as pending review rather than regenerated. A new source semantic version invalidates downstream currentness without deleting historical artifacts.

### I2 planning ledger

The planner exposes deterministic counts for:

```text
source candidate / ready / blocked / selected / remaining / failed-refresh warning
translation reused / selected / remaining / unavailable / blocked
P1.6 accepted-current / pending-current / selected / remaining / unavailable / blocked
```

This is a planning ledger, not execution telemetry. Actual stage attempts/completions/failures remain the future thin Market coordinator's responsibility.

### I2 acceptance evidence

```text
head: 2ada4e92207f694bb5b7a4cba8c17108a67a4863
CI 1167 / 35123454023
package install: PASS
pip dependency consistency: PASS
installed entrypoint smoke: PASS
Ruff: PASS
pytest: PASS
pytest -W error: PASS
conclusion: SUCCESS
```

I2 makes no Jobinja network or LM Studio calls in CI and does not implement semantic membership classification.

---

## 6. Exact current product action — I3

Current active product frontier:

```text
I3 — membership qualification contract + service
```

I3 must consume **only I2 source-eligible candidates** and decide exactly one bounded disposition:

```text
core_match
adjacent_match
uncertain
excluded
```

Required staged shape:

```text
1. deterministic target constraints / obvious exclusions
2. bounded semantic role/work relevance when deterministic evidence is insufficient
3. persist/reuse immutable MarketJobMembership with exact dependencies
```

Minimum evidence boundary:

```text
current parsed source detail + title
+ current English projection when needed
+ accepted-current P1.6 opportunistically when available
```

Accepted P1.6 is not a prerequisite. Capability and Work remain optional and must not become gates.

I3 acceptance must prove:

- title/keyword equality alone cannot prove `core_match`;
- deterministic exclusions happen before model calls where evidence is sufficient;
- model output is bounded to the four dispositions plus short reason/evidence refs;
- `uncertain` is valid success, not an error/retry trigger;
- exact target/source/classifier/translation/P1.6 dependencies control membership reuse;
- changed source/target/classifier dependencies prevent stale membership reuse;
- exact reruns reuse immutable membership;
- reviewed corrections supersede rather than overwrite prior decisions;
- no Canonical Registry, P2.2C, or P2.2D promotion side effect.

Representative fixture boundary set remains:

```text
ta9l  → core source evidence despite missing accepted P1.6
tG9K  → core with accepted P1.6 support
tGM0  → adjacent backend/AI-platform role
t4jp  → excluded AI-title/content-production false positive
tmBK  → excluded Python/backend with AI-usage qualification
t4qV  → excluded network security
tmyX  → excluded infrastructure security
+ one sparse/borderline uncertain case
```

---

## 7. First-slice sequence

```text
I1  domain + SQLite persistence                  ACCEPTED / CLOSED
I2  target source eligibility / affected work    ACCEPTED / CLOSED
I3  membership qualification                     NEXT
I4  immutable snapshot construction              BLOCKED BY I3
I5  deterministic aggregate profile              BLOCKED BY I4
I6  browser + CLI thin workflow                  BLOCKED BY I5
I7  bounded real local acceptance                BLOCKED BY I6
```

Do not jump ahead because I1 persistence already contains later table shapes.

---

## 8. Precedence for older status wording

For present-tense status only, this reconciliation supersedes older statements such as:

```text
B1 active
Market foundation not complete
I1 next / not implemented
I2 next / not implemented
```

Historical records remain evidence; do not mass-edit their old `NEXT` wording.

Current implementation evidence owners are:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
```

---

## 9. Current execution owner set

Before I3 work, use:

```text
AGENTS.md
README.md
product/domain/source/architecture + reasoning policy
ROADMAP.md / IMPLEMENTATION_PLAN.md for durable semantics
THIS reconciliation for present-tense status
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

Load older research records only when a specific I3 decision requires their detail.

---

## 10. Current stop lines

During I3:

- do not build I4 snapshot construction early;
- do not calculate I5 aggregates early;
- do not build I6 browser/report UI early;
- do not auto-accept P1.6;
- do not make Capability/Work mandatory Market gates;
- do not invent repost similarity thresholds;
- do not promote membership to Canonical Registry/P2.2C/P2.2D;
- do not add trends/emerging/forecasting;
- do not add personal readiness/gap/scoring/recommendations;
- do not publish Market state to `corpus/`;
- do not add generic source/plugin/vector/RAG/graph/autonomous-agent infrastructure.

---

## 11. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1 ACCEPTED / CLOSED
→ I2 ACCEPTED / CLOSED
→ I3 NEXT
→ I4-I6 sequentially after preceding acceptance
→ I7 bounded local real acceptance
→ close first Market slice only when its acceptance matrix passes
```

This file remains a status-only overlay. It does not replace durable product/domain/source/architecture authority or rewrite historical evidence.
