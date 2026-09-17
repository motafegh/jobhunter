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
Market I6 browser + CLI workflow    ACCEPTED / CLOSED
Market I7 real local acceptance     NEXT / ACTIVE PRODUCT FRONTIER
First Market vertical slice         NOT END-TO-END ACCEPTED UNTIL I7
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

## 3. Market foundation and accepted increments

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Accepted implementation sequence:

```text
I1  domain + SQLite persistence                 ACCEPTED
I2  target-scoped source/affected work          ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate profile             ACCEPTED
I6  browser + CLI thin workflow                 ACCEPTED
I7  bounded real local acceptance               NEXT
```

Latest I6 acceptance owner:

`docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

Earlier accepted Market evidence remains applicable:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
```

I3 real-model evaluation is preserved at:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/`

Its clarified-target 8/8 result is post-hoc boundary calibration, not a general model-accuracy benchmark.

---

## 4. Accepted I6 product path

The shared first-slice workflow now exists in repository code:

```text
TargetMarket
→ immutable TargetMarketDefinitionVersion
→ exact target acquisition envelope
→ bounded target-only Jobinja discovery
→ bounded I2 source/translation/P1.6 affected work
→ bounded I3 membership qualification
→ terminal MarketResearchRun + partial-success ledger
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ shared browser/CLI inspection
```

Browser primary surface:

```text
/market/targets
```

The older `/market` current-corpus aggregate page remains available as a legacy view. It is not the target-scoped historical authority.

CLI surface:

```text
jobhunter market target list
jobhunter market target create
jobhunter market definition create TARGET_ID
jobhunter market show
jobhunter market preview DEFINITION_ID
jobhunter market run DEFINITION_ID
jobhunter market run-show RUN_ID
jobhunter market snapshot-show SNAPSHOT_ID
```

I6 uses the existing `WebOperationManager` one-mutable-operation boundary. Browser and CLI use the same Market workspace/services/state.

Market target/definition/membership/run/snapshot/profile tables remain local/private and are not exported to the repository public corpus by default.

---

## 5. Permanent first-slice semantic/denominator boundaries

- acquisition/search vocabulary is not target-membership truth;
- target meaning is versioned and immutable;
- target search catalog version is locked to the definition meaning;
- `core_match / adjacent_match / uncertain / excluded` remain distinct;
- only core enters the primary corpus;
- accepted P1.6 is not required for source-level membership;
- accepted-current P1.6 is required for strong P1.6-backed prevalence statistics;
- pending/missing/failed/rejected P1.6 never means zero demand;
- Capability and Work are optional enrichments, not Market gates;
- automatic repost/new-ID collapse remains deferred;
- denominator language remains `qualified source postings`;
- no model-authored counts or opaque composite scores;
- semantic subfamily synthesis, trends, forecasts and personal scoring remain outside this slice.

---

## 6. I6 acceptance evidence

Accepted technical head before status reconciliation:

```text
4076bb731b3485aa99fbdf63bf73a96dc7a5773b
```

CI:

```text
run 1210 / 35263630011
installed entrypoint smoke     PASS
Ruff                           PASS
pytest                         632 passed
pytest -W error                632 passed
conclusion                     SUCCESS
```

During integration, repository tests caught an accidental attempted drift in accepted I5 aggregate semantics. The exact accepted I5 implementation was restored before I6 acceptance. Current I6 composes I5 directly and does not redefine the aggregate contract.

---

## 7. Exact active frontier — I7 only

I7 is the required **bounded real local acceptance** of the complete first Market vertical slice.

Use one small representative target, preferably a well-specified Applied AI / ML Engineering definition whose core-vs-adjacent boundary is explicit.

I7 must verify on the owner's actual local runtime:

```text
target creation/versioning or intentional reuse
→ exact search-scope preview
→ bounded Jobinja acquisition
→ candidate/noise inspection
→ source/translation/P1.6 affected-work behavior
→ membership core/adjacent/uncertain/excluded inspection
→ immutable run ledger
→ immutable snapshot
→ source/core denominator display
→ accepted-semantic denominator display
→ requirement/responsibility evidence drill-down
→ unchanged rerun reuse/currentness
→ partial-success behavior where naturally encountered or safely injected
→ privacy/publication boundary
→ browser usability + CLI parity
```

I7 may produce PASS, bounded repair work, or HOLD. Do not pre-commit to PASS.

The first Market vertical slice is not end-to-end accepted until I7 evidence supports closure.

---

## 8. I7 stop lines

During I7 do not:

- broaden into semantic role-subfamily synthesis;
- add trends/emerging/forecasting;
- add Market → You/personal readiness scoring;
- auto-accept P1.6;
- make Capability or Work mandatory;
- invent repost similarity thresholds;
- publish Market local tables to `corpus/`;
- reopen B1/P2.2C/P2.2D;
- introduce a second workflow/persistence/currentness stack;
- weaken deterministic tests merely to accommodate a live provider result.

If real evidence exposes a concrete correctness defect, repair only the owning boundary and rerun the relevant acceptance checks.

---

## 9. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1-I6 ACCEPTED
→ I7 NEXT
→ first Market vertical slice closure only from real local acceptance evidence
```

For present-tense status use this file together with `docs/EXECUTION_TODO.md` and `docs/WORKING_MEMORY.md`. Older dated `NEXT` wording is historical when it conflicts with this overlay.
