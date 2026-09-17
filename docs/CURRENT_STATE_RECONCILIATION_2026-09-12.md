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
Market I5 aggregate profile         ACCEPTED / CLOSED
Market I6 browser + CLI workflow    NEXT / ACTIVE PRODUCT FRONTIER
Market I7 real local acceptance     BLOCKED BY I6
Semantic subfamily/report synthesis DEFERRED FROM FIRST SLICE
Market → You                        LATER / NOT AUTHORIZED

Portfolio / release                 PARALLEL
MIT license                         COMPLETE
GitHub metadata/screenshots/release/owner mastery  PENDING
```

Current first-slice contracts:

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

No responsibility concept or mappings were created. Do not reopen B1 merely to manufacture a promotion.

---

## 3. Market first-slice foundation

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

- Jobinja is the first recurring source;
- search/acquisition recall != target membership truth;
- dispositions remain `core_match / adjacent_match / uncertain / excluded`;
- primary source-level corpus is core only;
- accepted P1.6 is not required for source-level membership;
- accepted-current P1.6 is required for strong semantic prevalence;
- pending/missing/failed/rejected P1.6 != zero demand;
- Capability/Work are optional, not first-slice gates;
- repost/new-ID collapse remains deferred;
- denominator wording is `qualified source postings`, not `unique demand units`;
- Market state remains local/private by default.

I3 real-model evidence additionally established that material core-vs-adjacent semantics belong in the immutable target definition rather than vacancy-specific prompt patches.

---

## 4. I1-I5 accepted chain

Accepted records:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md
docs/working-memory/2026-09-17_MARKET_I5_DETERMINISTIC_AGGREGATE_PROFILE.md
```

### I1

Immutable target/definition/run/membership/snapshot/profile persistence and exact dependency history.

### I2

Target-scoped source/translation/P1.6 affected-work planning with no global backlog spill and cautious lifecycle/freshness semantics.

### I3

Target-relative membership qualification with exact evidence refs, valid `uncertain`, optional accepted P1.6, exact dependency reuse and immutable corrections.

Repository acceptance: implementation `0eaf04109a57846aa6d0a920d0563f89a4dfb535`, CI 1172 with 608 tests twice.

Real-model boundary evidence:

```text
broad target       7/8 expected outcomes; tGM0 sole disagreement
clarified target   8/8 post-hoc boundary-calibration outcomes
```

This is not a population accuracy benchmark.

### I4

Immutable point-in-time snapshot assembly from exact current I3 membership identities, with derived `accepted/pending/missing/failed/rejected` P1.6 coverage and core-only primary corpus.

Technical acceptance: CI 1182, 617 tests twice.

### I5

Deterministic aggregate profile over one exact immutable I4 snapshot.

Accepted boundaries:

- never reconstructs the historical corpus from today's current state;
- source denominator = qualified core source postings;
- semantic denominator = accepted-P1.6 core postings;
- employer/source context derives from exact immutable source-detail evidence;
- unknown employer remains explicit;
- requirement/responsibility semantic counts use accepted snapshot P1.6 only;
- one posting contributes at most once to a normalized support count;
- strength support remains explicit;
- evidence drill-down preserves source job, artifact and claim indexes;
- Canonical Registry enrichment is permitted only for mappings reviewed no later than the snapshot timestamp;
- later Registry review cannot silently change historical aggregate replay;
- no model writes counts/shares/denominators/scores;
- repost adjustment remains explicitly absent;
- deterministic profile persistence is immutable and replay-safe.

Technical acceptance:

```text
head 5defb23cb769a4be7a6b0d13ea7762d35ec0f4ba
CI 1189 / 35250174702
Ruff: PASS
pytest: 622 passed
pytest -W error: 622 passed
conclusion: SUCCESS
```

---

## 5. Exact current action — I6

Current active frontier:

```text
I6 — thin browser + CLI Market workflow
```

I6 must expose the accepted I1-I5 state/services through the existing product surfaces rather than creating duplicate business logic.

Minimum useful surface:

```text
list/create Market target
create/inspect immutable target definition
inspect target run state/ledger
inspect snapshot/profile history
render deterministic profile and warnings
show source vs accepted-semantic denominators
show membership/coverage counts
show requirement/responsibility evidence drill-down
```

The browser remains the primary repeat-use surface. CLI provides the same service/state access for automation/debugging.

A thin coordinator may connect the accepted stages for one bounded run, but I6 must preserve partial-success ledgers and existing one-mutable-operation behavior. Do not introduce a generic workflow engine.

I6 must not add model-generated report prose, role-subfamily clustering, repost heuristics, trends/forecasting, personal scoring, public corpus publication, or new infrastructure frameworks.

---

## 6. Sequence

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate                     ACCEPTED
I6  browser + CLI thin workflow                 NEXT
I7  bounded real local acceptance               BLOCKED BY I6
```

---

## 7. Precedence

For present-tense status only, this file supersedes older `B1 active`, `Market foundation incomplete`, or `I1-I5 next` language. Dated historical records remain evidence and should not be mass-rewritten.

Current owner set before I6:

```text
AGENTS.md
README.md
product/domain/source/architecture + reasoning policy
this reconciliation
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-17_MARKET_I5_DETERMINISTIC_AGGREGATE_PROFILE.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

---

## 8. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1-I5 ACCEPTED
→ I6 NEXT
→ I7 bounded real local acceptance
→ close first Market slice only after I7 acceptance
```

This file is a status-only overlay. It does not replace durable product/domain/source/architecture authority.
