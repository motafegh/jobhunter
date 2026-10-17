# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-10-17  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / ROLE-FAMILY REPORT R1-R4 ACCEPTED / P2.2B-B2 ACTIVE  
**Current English P1.6:** `job-analysis-english-v30 / job-analysis-v5`; accepted v20/v21/v23/v28 v5 artifacts remain accepted-only compatibility inputs when exact dependencies match.  
**Committed public-corpus baseline:** 420 jobs / 52 parsed details / 30 English projections / 11 accepted English P1.6 / 5 Capability artifacts.  
**LM Studio maintainer endpoint:** `http://127.0.0.1:18080/v1`; fresh-clone `Settings` default remains port 1234.  
**Active increment:** P2.2B-B2 snapshot-15 selective responsibility normalization through the existing P2.1 Canonical Registry. Semantic review of R1-R6 is complete. R1/R2 are applied/verified; R3-R6 are accepted semantically and await local Registry application/verification. No P2.2C family, P2.2D archetype, P2.3 profile or P2.4 Market-v2 implementation is authorized.  
**Parallel product priority:** Whole-product usability/productivity, prioritizing understanding and comparing jobs or Market findings. The first navigation/UI slice is implemented and locally verified; owner repeated-use feedback remains pending.  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending.

This file is current-frontier oriented. Detailed historical execution belongs in dated records under `docs/working-memory/`.

## 1. Read this first

Stable authority:

1. `AGENTS.md`
2. `README.md`
3. `docs/PRODUCT_SPECIFICATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
6. `docs/SOURCE_POLICY.md`
7. `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`
8. `docs/ROADMAP.md`
9. `docs/IMPLEMENTATION_PLAN.md`
10. `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`
11. `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`
12. `docs/EXECUTION_TODO.md`

Current focused records:

- `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R3_SEMANTIC_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`
- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Historical entry/evidence records remain available but do not override the current-state overlay.

Permanent boundary:

```text
SOURCE FACT
!= NORMALIZED CORRESPONDENCE
!= ANALYTICAL INTERPRETATION
!= RECOMMENDATION / DECISION SYNTHESIS

GENERATED / CANDIDATE
!= REVIEWED / PROMOTED
```

---

## 2. Current accepted product state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence v2      CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2B-B2                            ACTIVE / AUTHORIZED
P2.2C promoted families             NOT AUTHORIZED
P2.2D stable archetypes             NOT AUTHORIZED
P2.3 capability profiles            DEFERRED / NOT AUTHORIZED
P2.4 Market v2                      DOWNSTREAM / NOT AUTHORIZED
Blueprint v6                        EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation                   PASS / COMPLETE
Market I1-I7                        ACCEPTED / CLOSED FOR BOUNDED SCOPE
Same-target coverage follow-up      COMPLETE
Candidate interpretation v6         ACCEPTED / CLOSED FOR BOUNDED REPORTING
RoleFamily report R1-R4             ACCEPTED / CLOSED
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
Role-family report             market-role-family-intelligence-report-v1
Role-family report review      market-role-family-report-review-v1
```

---

## 3. Closed Market/report substrate

Snapshot-15 accepted P1.6 factual set:

```text
tvMm  artifact 50  responsibilities 11  requirements 25
t7ck  artifact 52  responsibilities  0  requirements 18
tmvA  artifact 61  responsibilities  7  requirements 22
tjgi  artifact 60  responsibilities  9  requirements 25
t7Ay  artifact 62  responsibilities  0  requirements 26
tNVe  artifact 56  responsibilities  8  requirements 24

responsibilities 35
requirements    140
total claims    175
```

`t7ck` and `t7Ay` contribute no direct responsibilities and cannot create duties from requirement-only evidence.

Final accepted `RoleFamilyIntelligenceReport`:

```text
report id                         2
snapshot                          15
model                             gemma-4-e4b-it-ud
available claims                 175
cited claims                      27
work clusters                      4
multi-posting subfamilies          1
singleton specialties/outliers     2
integrity rejections               0
review state                      accepted_for_bounded_use
```

Candidate/report interpretation remains analytical, not taxonomy authority.

---

## 4. Phase-2 direction

Direction comparison:

```text
A  P2.2 responsibility/deliverable normalization and later family semantics
B  P2.3 corpus-scale capability requirement profiles
C  P2.4 Market v2
```

Decision:

```text
A selected at P2.2B level
B deferred, not rejected
C downstream
```

Reasoning remains in `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`.

---

## 5. P2.2B-B2 semantic review — COMPLETE

Objective:

```text
accepted/current P1.6 responsibility claims
→ bounded candidate cross-job correspondence
→ explicit semantic review
→ existing P2.1 Registry reviewed responsibility concept + exact immutable claim mappings
```

Decisions:

```text
R1  responsibility:design-implement-ai-agents
    tvMm 50[0] ↔ tNVe 56[0]
    ACCEPTED / APPLIED / VERIFIED

R2  responsibility:integrate-ai-systems-with-services
    tvMm 50[2] ↔ tNVe 56[2]
    ACCEPTED / APPLIED / VERIFIED

R3  responsibility:implement-llm-tool-calling
    tvMm 50[3] ↔ tNVe 56[3]
    ACCEPTED / LOCAL APPLICATION PENDING

R4  responsibility:develop-rag-systems
    tvMm 50[6] ↔ tNVe 56[4]
    ACCEPTED / LOCAL APPLICATION PENDING

R5  responsibility:design-develop-multi-step-ai-workflows
    tvMm 50[7] ↔ tNVe 56[5]
    ACCEPTED / LOCAL APPLICATION PENDING

R6  responsibility:evaluate-improve-ai-system-performance
    tvMm 50[8] ↔ tNVe 56[7]
    ACCEPTED / LOCAL APPLICATION PENDING
```

Important semantic limits:

- R3: `Structured Output` remains specific to `tNVe`.
- R4: the original tentative `develop-rag-knowledge-retrieval` identity was narrowed to `develop-rag-systems` because `Knowledge-based systems` and `Knowledge Retrieval` are not equivalent; only the common RAG-development core is normalized.
- R5: `reliable` remains specific to `tvMm`; Multi-Agent/Email/Ticketing/module integration remains specific to `tNVe`.
- R6: `debugging` remains specific to `tvMm`; quality/reliability/latency/cost remain explicit `tNVe` dimensions.
- `tvMm` 50[9] remains pending because “paying attention to” operational qualities does not assert the same evaluate/improve action.
- broader R1/R2 boundary claims remain pending.
- no R3-R6 aliases are authorized.

Current proven local Registry state remains **4/35 mapped, 31 pending** from R1/R2 only. If all eight R3-R6 claims remain accepted/current and pending, successful application is expected to produce **12/35 mapped, 23 pending**. Do not represent that expected state as current until local verification proves it.

---

## 6. Exact continuation sequence

```text
B2.1 baseline COMPLETE

B2.2 semantic review COMPLETE
   - R1-R6 reviewed individually
   - R1/R2 applied + verified
   - R3-R6 accepted semantically

B2.3 local Registry application NEXT
   - pull current main
   - fresh SQLite backup
   - integrity + foreign keys
   - reconfirm exact pending/current R3-R6 claims
   - create/reuse exactly four accepted concepts
   - map exactly eight approved claims
   - no aliases
   - leave tvMm 50[9] and broader R1/R2 boundaries pending

B2.4 verify
   - exact-command idempotency
   - CLI/browser same reviewed state
   - SQLite integrity/foreign keys
   - R1/R2 + unrelated Registry rows preserved
   - accepted P1.6 / Market unchanged
   - public corpus unchanged by Registry mutation

B2.5 close bounded tranche
   - record exact local row identities + proof
   - record pending boundary claims
   - state normalized correspondence != ResponsibilityFamily != prevalence
   - close B2
   - STOP
   - separate P2.2C vs P2.3 readiness decision
```

Exact commands and verification requirements:

`docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`

Do not start P2.2C, P2.2D, P2.3, P2.4, Blueprint authority, personal scoring, bulk mapping, or a new model-review loop during B2.

---

## 7. R1/R2 applied evidence

R1 applied `responsibility:design-implement-ai-agents` with mappings #7/#8 to exact artifact 50/56 responsibility[0] claims. R2 applied `responsibility:integrate-ai-systems-with-services` with mappings #9/#10 to exact artifact 50/56 responsibility[2] claims.

R1 exposed a narrow Registry write-validator defect for accepted-compatible historical P1.6 artifacts; commit `dafdb05` aligned Registry persistence with the accepted v20/v21/v23/v28/v30 v5 compatibility boundary. Ruff, 843 warnings-as-errors tests and normal CI passed before live application. R1/R2 idempotency, CLI/browser agreement, SQLite integrity/foreign keys, other-table preservation and corpus-hash preservation passed. Local backups/results remain ignored under `data/local-acceptance/b2-review-2026-10-16/`.

No later semantic decision changes those exact R1/R2 rows.

---

## 8. Public corpus / reconciliation state

The owner published the previously local `tNpG` source/detail and English projection on 2026-10-17. Current committed repository-safe counts:

```text
jobs                 420
parsed details        52
English projections   30
accepted English P1.6 11
Capability artifacts   5
```

`tNpG` adds no accepted P1.6, Capability, Registry mapping, or Market authority.

The October 15 statements that `tNpG` was unpublished or that all 35 B2 responsibilities were pending are historical checkpoint facts only.

---

## 9. Usability direction

Owner-selected friction: understanding/comparing jobs or Market findings.

Delivered first bounded UI slice:

- research-first Overview;
- navigation grouped into daily research versus management/processing;
- accepted-fact job preview before full source/translation documents;
- frozen role/company evidence labels;
- validated snapshot/report/finding return context through job/Work/Capability reading;
- explicit current-versus-historical source distinction.

Verification included Ruff, 834 warnings-as-errors tests, and a real Edge/Playwright journey on a SQLite copy across desktop and 390px viewport. Subjective repeated-use usefulness remains owner feedback, not mechanically proven acceptance.

No job-comparison feature or new semantic authority layer was added.

---

## 10. Current stop lines

Do not:

- create `ResponsibilityFamily` or stable `RoleArchetype` entities during B2;
- bulk-map the remaining snapshot responsibilities;
- canonicalize requirements in this tranche;
- start P2.3 capability profiles or P2.4 Market v2;
- use Blueprint as authority;
- add personal readiness/gap/scoring;
- publish local Registry/Market/Work state into `corpus/`;
- add new model-review loops merely to obtain promotion;
- treat accepted R1-R6 correspondences as market prevalence.

---

## 11. Exact next action

```text
R1/R2 applied + verified
R3-R6 semantic review complete / accepted
→ execute combined R3-R6 local Registry application protocol
→ verify idempotency + CLI/browser + integrity/FK + preservation
→ update current state to proven post-application counts
→ record B2 closure
→ STOP
→ make a separate P2.2C-vs-P2.3 readiness decision
```

GitHub cannot claim the R3-R6 SQLite rows exist because the maintainer runtime database is intentionally local and excluded from the repository.