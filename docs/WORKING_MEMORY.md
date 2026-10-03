# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-10-03  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED  
**Current English P1.6:** `job-analysis-english-v30 / job-analysis-v5`; accepted v20/v21/v23/v28 v5 artifacts remain accepted-only compatibility inputs when exact dependencies match.  
**Current public corpus:** 420 jobs / 51 parsed details / 29 English projections / 11 accepted English P1.6 / 5 Capability artifacts.  
**LM Studio maintainer endpoint:** `http://127.0.0.1:18080/v1`; fresh-clone `Settings` default remains port 1234.  
**Active increment:** `RoleFamilyIntelligenceReport` R1 domain + persistence. Candidate V6 is accepted/closed for bounded reporting; the next work is immutable local report/attempt/review persistence under `market-role-family-intelligence-report-v1`. Taxonomy promotion remains unauthorized.  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending.

This file is intentionally current-frontier oriented. Detailed historical execution belongs in dated records under `docs/working-memory/`.

## 1. Read this first

Authority and stable context:

1. `AGENTS.md`
2. `README.md`
3. `docs/PRODUCT_SPECIFICATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
6. `docs/SOURCE_POLICY.md`
7. `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`
8. `docs/ROADMAP.md`
9. `docs/IMPLEMENTATION_PLAN.md`
10. `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`
11. `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`
12. `docs/EXECUTION_TODO.md`

Current focused record:

`docs/working-memory/2026-09-29_MARKET_CANDIDATE_INTERPRETATION_V1.md`

Accepted Market closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`

Do not follow older I7 HOLD, v20/v21/v22 retry, or open-B1 instructions when they conflict with current owners.

---

## 2. Current accepted product state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
Blueprint v6                        EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation                   PASS / COMPLETE
Market I1                           ACCEPTED
Market I2                           ACCEPTED
Market I3                           ACCEPTED
Market I4                           ACCEPTED
Market I5                           ACCEPTED
Market I6                           ACCEPTED
Market I7                           PASS / CLOSED FOR BOUNDED SCOPE
Same-target coverage follow-up      COMPLETE
Candidate interpretation v6         ACCEPTED / CLOSED FOR BOUNDED REPORTING
Market → You                        LATER / NOT AUTHORIZED
```

Current primary contracts:

```text
parser                         jobinja-detail-v2
translation                    lm-studio-translation-v2
English projection             english-projection-v2
English P1.6 generation         job-analysis-english-v30 / job-analysis-v5
Original P1.6                   job-analysis-original-v9 / job-analysis-v4
Capability                     job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry             jobhunter-canonical-concept-registry-v1
Job Work Intelligence          job-work-intelligence-v2 / job-work-intelligence-v2.0
Market membership              market-membership-v1 / market-membership-v1.0
Market snapshot                market-corpus-snapshot-v1
Market aggregate               market-aggregate-profile-v1
Public Corpus                  jobhunter-public-corpus-v1
Candidate generator            market-role-family-candidate-v6
Role-family report              market-role-family-intelligence-report-v1
Role-family report review       market-role-family-report-review-v1
```

Accepted-only historical P1.6 compatibility does not relabel old artifacts. Exact prompt/schema/dependency identity remains visible.

---

## 3. Frozen Market first-slice rules

```text
source = Jobinja only
search/acquisition envelope != target membership truth
membership = core_match | adjacent_match | uncertain | excluded
primary source corpus = core_match only
accepted P1.6 is not required for source-level membership
accepted-current P1.6 is required for strong semantic prevalence
pending/missing/failed/rejected P1.6 != zero demand
Capability/Work optional, not gates
repost/new-ID collapse deferred
use "qualified source postings", not "unique demand units"
Market state local/private by default
```

Accepted sequence:

```text
I1 domain + persistence
→ I2 target-scoped affected work
→ I3 membership qualification
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ I6 shared browser/CLI workflow
→ I7 bounded real-local acceptance
→ same-target coverage follow-up
```

Snapshots 14-15 contain ten qualified members, six core postings and six accepted-semantic core postings. The unchanged rerun reused the same member and analysis identities.

---

## 4. Active increment — RoleFamilyIntelligenceReport R1

Candidate interpretation V6 is accepted/closed for bounded reporting.

Final real acceptance evidence:

```text
snapshot:                    15
accepted-semantic core:       6
available P1.6 claims:      175
unique cited claims:         49
work clusters:                4
multi-posting subfamilies:    1
singleton specialty:          1
C* leakage:                   0
integrity rejections:         0
```

Exact artifact:

`docs/working-memory/review-artifacts/2026-10-03_snapshot15_candidate_report_v6.html`

Disposition:

```text
candidate generator v6        ACCEPT for bounded reporting
durable report persistence    AUTHORIZED
taxonomy promotion            NOT AUTHORIZED
V7 repair                     NOT AUTHORIZED
```

Controlling persistence design:

`docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`

R1 scope only:

- typed `MarketRoleFamilyIntelligenceReport`, attempt and review records;
- immutable local SQLite report persistence;
- deterministic input/generation/report fingerprints;
- append-only terminal attempts;
- append-only review history;
- effective review state from latest event;
- exact generation reuse plus explicit regeneration support;
- deterministic Tier-1 tests;
- no LM Studio requirement in normal CI;
- no browser/CLI implementation yet;
- no public-corpus publication;
- no taxonomy promotion.

Authority remains:

```text
exact immutable snapshot
→ V6 bounded generator
→ application validation/normalization
→ immutable persisted analytical report
→ append-only human review
!= canonical taxonomy
```

---

## 5. Exact continuation sequence

```text
A. R1 domain model
   - report artifact
   - generation attempt
   - append-only review event

B. R1 local persistence
   - tables + FKs + indexes
   - immutable report/review triggers
   - canonical JSON hashes/fingerprints

C. R1 store semantics
   - record/get/list reports
   - exact generation lookup/reuse
   - explicit regeneration allowed
   - record terminal attempts
   - append review / derive effective state

D. R1 deterministic tests
   - no model/network dependency
   - immutability
   - multiple artifacts per snapshot
   - failed attempt creates no report
   - review history/effective state
   - no upstream Market/P1.6 mutation

E. R1 closure
   - CI green
   - docs reconciled
   - then authorize R2 service + V6 integration
```

Do not start R2 browser/model integration before R1 closure.
