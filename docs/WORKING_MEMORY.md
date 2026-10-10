# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-10-10  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED; ROLE-FAMILY REPORT R1-R4 ACCEPTED / CLOSED  
**Current English P1.6:** `job-analysis-english-v30 / job-analysis-v5`; accepted v20/v21/v23/v28 v5 artifacts remain accepted-only compatibility inputs when exact dependencies match.  
**Current public corpus:** 420 jobs / 51 parsed details / 29 English projections / 11 accepted English P1.6 / 5 Capability artifacts.  
**LM Studio maintainer endpoint:** `http://127.0.0.1:18080/v1`; fresh-clone `Settings` default remains port 1234.  
**Active increment:** Phase-2 semantic direction reconciliation. `RoleFamilyIntelligenceReport` R1-R4 is accepted/closed; no promoted responsibility-family, stable role-archetype, corpus-scale capability-profile, or Market-v2 implementation is authorized until the next bounded semantic increment is explicitly selected and planned.  
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

Current focused/closure records:

- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-10-10_MARKET_R4_RECOVERY_IDENTITY_REPAIR.md`
- `docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`
- `docs/working-memory/2026-10-04_MARKET_R3_DURABLE_WORKFLOW_AND_UX_CLOSURE.md`

The R4 final acceptance record supersedes the earlier plan's present-tense `R4 active` wording. The persistence plan remains design/history after closure.

Accepted Market closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`

The candidate-interpretation record remains predecessor/history after V6 acceptance.

Do not follow older I7 HOLD, v20/v21/v22 retry, open-B1, or pre-R4 continuation instructions when they conflict with the current closure records.

---

## 2. Current accepted product state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2C promoted families             NOT ACTIVE / NOT AUTHORIZED
P2.2D stable archetypes             LATER / NOT AUTHORIZED
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
RoleFamily report R1-R4             ACCEPTED / CLOSED
Phase-2 semantic direction          RECONCILIATION ACTIVE / IMPLEMENTATION NOT YET AUTHORIZED
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
→ bounded V6 candidate interpretation
→ durable RoleFamilyIntelligenceReport R1-R4
```

Snapshots 14-15 contain ten qualified members, six core postings and six accepted-semantic core postings. The unchanged rerun reused the same member and analysis identities.

---

## 4. RoleFamilyIntelligenceReport R1-R4 closure

Candidate interpretation V6 is accepted/closed for bounded reporting.

Earlier V6 usefulness evidence:

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

Exact predecessor artifact:

`docs/working-memory/review-artifacts/2026-10-03_snapshot15_candidate_report_v6.html`

Authority remains:

```text
exact immutable snapshot
→ V6 bounded generator
→ application validation/normalization
→ immutable persisted analytical report
→ append-only human review
!= canonical taxonomy
```

R1 accepted implementation:

- typed `MarketRoleFamilyIntelligenceReport`, attempt and review records;
- dedicated `market_role_family_report_store.py` local SQLite owner;
- immutable reports and append-only terminal attempts/reviews;
- canonical input/generation/report fingerprints and read-time corruption checks;
- exact generation reuse lookup plus explicit immutable regeneration support;
- effective review state / accepted-report selection;
- CI `37217405526`: Ruff + 825 tests + 825 warnings-as-errors green.

R2 accepted implementation:

- exact preparation before inference plus accepted V6 generation step;
- one `market_role_family_report_service.py` orchestration owner;
- ordinary exact match → reuse + `reused` attempt + no LM call;
- explicit regenerate → new immutable artifact + `completed` attempt;
- generation/identity failure → `failed` attempt + no report artifact;
- review/effective-state/latest-accepted selection through the service;
- CI `37220490754`: Ruff + 830 tests + 830 warnings-as-errors green.

R3 accepted implementation:

- browser and CLI use durable report IDs/history/review state from the same service;
- report detail survives app restart;
- CLI `role-report list|generate|show|review` shares the same state;
- Market workspace guides target → scope → refresh → intelligence with progressive disclosure;
- snapshot/report presentation prioritizes decision-relevant findings while retaining exact evidence/provenance drill-down;
- closure record: `docs/working-memory/2026-10-04_MARKET_R3_DURABLE_WORKFLOW_AND_UX_CLOSURE.md`;
- CI `37223301900`: Ruff + 830 tests + 830 warnings-as-errors green.

R4 real-local acceptance: PASS / CLOSED.

Final accepted real artifact:

```text
report id                         2
snapshot                          15
model                             gemma-4-e4b-it-ud
report SHA-256                    b6331a227c95de27954ca3e9f3298c69c0dd5372eb1bddffa73e9b0ec51e6d7b
generation fingerprint            963e6d18cfb8d68ec3c735f66c3fb494b0c199efaa894dc6962e55a84b496d1e
source postings                    6
available claims                 175
cited claims                      27
work clusters                      4
multi-posting subfamilies          1
singleton specialties/outliers     2
integrity rejections               0
review state                      accepted_for_bounded_use
```

R4 exposed and repaired an incomplete generation identity on historical artifact #1. The repaired identity records:

```text
initial max_tokens                  2048
truncation recovery multiplier         4
maximum recovery tokens            32768
successful request max_tokens       8192
```

Artifact #1 remains immutable/pending historical evidence. It was not deleted or accepted.

Exact reuse proof after repair:

```text
(1, completed, artifact 1)
(2, completed, artifact 2)
(3, reused,    artifact 2)
reports = 2
```

Final integrity/non-mutation proof:

```text
SQLite integrity                  ok
foreign-key violations            []
snapshot members                  10
accepted-semantic members          6
pre-existing corpus file hashes   unchanged from pre-R4 baseline
```

Repair CI `38068073900`: Ruff + 830 tests + 830 warnings-as-errors green.

Final record:

`docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Disposition:

```text
RoleFamilyIntelligenceReport R1-R4  ACCEPTED / CLOSED
report #2                           ACCEPTED FOR BOUNDED ANALYTICAL USE
report #1                           PENDING HISTORICAL REPAIR EVIDENCE
canonical taxonomy promotion        NOT AUTHORIZED
R5/report-infrastructure expansion   NOT AUTHORIZED
```

---

## 5. Exact continuation sequence

```text
A. Re-orient Phase-2 semantic state
   - P2.1 Canonical Registry accepted boundary
   - P2.2A Job Work Intelligence accepted boundary
   - P2.2B-B1 NO-PROMOTION / DEFER evidence
   - P2.2/P2.3/P2.4 controlling plan semantics

B. Reconcile what changed
   - Market I1-I7 now accepted with six accepted-semantic core postings
   - V6 bounded interpretation demonstrated useful non-canonical synthesis
   - durable reviewed report is now an accepted analytical artifact
   - none of this automatically creates promoted responsibility families/archetypes

C. Compare next semantic directions
   - responsibilities/deliverables and promotion prerequisites
   - corpus-scale capability requirement profiles
   - prerequisites for Market v2 reviewed canonical aggregation

D. Select one bounded responsibility
   - explicit authority level
   - representative evidence/sample
   - persistence/review/promotion boundary
   - deterministic vs semantic ownership
   - stop lines and acceptance proof

E. Write/reconcile the focused plan
   - no implementation before the decision is explicit
   - no automatic P2.2C/P2.2D promotion

F. Only then authorize the next implementation increment
```

Do not reopen RoleFamilyIntelligenceReport infrastructure, promote generated report labels, or start personal scoring while this semantic direction reconciliation is active.
