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
**Active increment:** P2.2B-B2 snapshot-15 selective responsibility normalization through the existing P2.1 Canonical Registry. R1/R2 are approved/applied/verified; R3 is the next owner semantic review. No P2.2C family, P2.2D archetype, P2.3 profile or P2.4 Market-v2 implementation is authorized.  
**Parallel product priority:** Whole-product usability/productivity, prioritizing understanding and comparing jobs or Market findings. The first navigation/UI slice is implemented and locally verified under `docs/ROADMAP.md` §13 and the execution TODO; owner repeated-use feedback remains pending.
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
- `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_ENTRY.md` — closed entry/history.
- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-10-10_MARKET_R4_RECOVERY_IDENTITY_REPAIR.md`

Historical B1 evidence:

- `docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`
- `docs/working-memory/2026-09-01_P2_2B_B1_REPO_EVIDENCE_SELECTION.md`

Do not follow older I7 HOLD, open-B1, R4-active, or Phase-2-reconciliation-active instructions when they conflict with the current decision/state overlay.

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

## 3. Closed Market/report state

Snapshots 14-15 contain ten qualified members, six core postings and six accepted-semantic core postings.

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

Candidate interpretation V6 is accepted for bounded reporting, not taxonomy authority.

`RoleFamilyIntelligenceReport` R1-R4 is accepted/closed. Final accepted real-local report:

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

Historical pre-repair report #1 remains immutable/pending.

Exact reuse history:

```text
(1, completed, artifact 1)
(2, completed, artifact 2)
(3, reused,    artifact 2)
reports = 2
```

R4 final SQLite/public-corpus/upstream invariants passed. Do not start R5 or promote report labels.

---

## 4. Phase-2 direction decision

The 2026-10-10 reconciliation compared:

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

Why:

- old B1 failed because no accepted second P1.6 responsibility existed for its selected pair; it did not semantically disprove cross-job normalization;
- snapshot 15 now contains 35 accepted direct responsibility claims across four jobs;
- P2.2A already proved safe exact-fact + candidate-interpretation separation;
- P2.1 Registry already supports reviewed canonical responsibilities and immutable exact claim mappings;
- P2.3 has strong per-job Capability v9 architecture but lacks reviewed cross-job canonical relationship coverage over the current Market set;
- P2.4 is defined to aggregate reviewed canonical mappings/profiles and is therefore downstream.

Controlling decision:

`docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`

---

## 5. Active P2.2B-B2 tranche

Objective:

```text
accepted/current P1.6 responsibility claims
→ bounded candidate cross-job correspondence
→ owner semantic review
→ existing P2.1 Registry reviewed responsibility concept + exact immutable claim mappings
```

No new software subsystem is required unless execution proves a concrete gap in existing Registry tooling.

Initial candidate review set:

```text
R1  design / implement AI agents
    strict pair: tvMm[0] ↔ tNVe[0]
    boundary: tjgi[2], tmvA[3]
    ACCEPTED / APPLIED / VERIFIED

R2  integrate AI systems with APIs / databases / services
    strict pair: tvMm[2] ↔ tNVe[2]
    boundary: tjgi[3], tmvA[2]
    ACCEPTED / APPLIED / VERIFIED

R3  implement LLM Tool / Function Calling
    pair: tvMm[3] ↔ tNVe[3]
    NEXT OWNER REVIEW

R4  develop RAG / knowledge retrieval
    pair: tvMm[6] ↔ tNVe[4]

R5  design / develop multi-step AI workflows
    pair: tvMm[7] ↔ tNVe[5]

R6  evaluate / improve AI-system performance
    strict pair: tvMm[8] ↔ tNVe[7]
    boundary: tvMm[9]
```

Tentative concept IDs and exact boundary notes are in the controlling decision file. R1/R2 are the only approved/applied concepts so far; R3-R6 remain unapproved until owner semantic review.

Promotion rule:

- at least two exact accepted/current responsibility claims from distinct postings must share one defensible reusable responsibility core;
- review semantic action/subject/outcome, not shared keywords;
- preserve exact source-specific context and scope;
- requirement-only evidence cannot create duties;
- no quota forces all six candidates to pass;
- subset or zero accepted correspondences is valid.

---

## 6. Exact continuation sequence

```text
B2.1 read-only local baseline COMPLETE (2026-10-15)
   - main aligned at bf016c7 / pre-existing tNpG corpus changes preserved
   - SQLite backup
   - PRAGMA integrity + foreign keys
   - inspect exact current responsibility claims for tvMm/tNVe/tjgi/tmvA
   - verify artifacts 50/56/60/61
   - inspect current Registry concepts/mapping states

B2.2 R1/R2 APPROVED / APPLIED / VERIFIED (2026-10-16)
   - R3-R6 owner review next, one at a time
   - ACCEPT | HOLD | REJECT
   - no mutation first

B2.3 apply only accepted correspondences
   - existing jobhunter-registry concept/mapping commands
   - no unrelated mappings/aliases

B2.4 verify
   - idempotency
   - browser/CLI same reviewed state
   - SQLite integrity/foreign keys
   - P1.6/Market unchanged
   - Registry publication remains unauthorized

B2.5 disposition
   - record accepted mappings + held/rejected boundaries
   - close accepted or no-promotion/defer
   - STOP
   - separate P2.2C vs P2.3 readiness decision
```

Do not start P2.2C, P2.2D, P2.3, P2.4, Blueprint authority, personal scoring, bulk mapping or a new model-review loop during B2.

## 7. Alignment and housekeeping checkpoint — 2026-10-15

The current entrypoints, product/architecture/plans, semantic/runtime guides, and corpus/snapshot guides were aligned to the October 10 overlay and B2 decision. Superseded September status and the executed R4 protocol are explicitly historical; accepted contracts and artifacts are unchanged.

B2.1 confirmed exact artifacts 50/56/60/61 and all 35 responsibilities as accepted/current and unmapped at that checkpoint. Registry was four concepts / six claim decisions. SQLite integrity was `ok`, foreign keys empty. Backup: `data/local-acceptance/project-alignment-2026-10-15/baseline-181157.sqlite3`.

At that checkpoint the `tNpG` source/projection/manifest changes were still local: local corpus 420 jobs / 52 parsed / 30 English / 11 P1.6 / 5 Capability while the committed baseline remained 420 / 51 / 29 / 11 / 5. That statement is historical. On 2026-10-17 the owner intentionally published those `tNpG` source/detail + English-projection changes, so the committed repository-safe baseline is now 420 / 52 / 30 / 11 / 5. The publication did not add P1.6, Capability, Registry mappings, or Market authority.

Verified alignment baseline on 2026-10-15: dependency consistency, Ruff, 830 warnings-as-errors tests, corpus verification, and read-only browser routes on a SQLite copy passed. CI `38078527873` passed on `bf016c7`. This housekeeping changed documentation/docstrings only; it did not repeat model generation or semantic acceptance.

Next after this historical baseline: owner B2.2 semantic review; R1/R2 have since been applied as recorded below, and R3-R6 remain pending. No later Phase-2 authorization was added.

## 8. Usability direction — 2026-10-15

Owner-selected first friction: understanding/comparing jobs or Market findings. Source review found that Overview still promoted the broad processing workflow, job detail led with complete source/translation documents, and Market evidence links often used job IDs while job detail returned to the general catalog. These are baseline source observations, not measured usability results.

Proposed first journey: easy entry to the existing Market intelligence → readable job context on evidence links → inspect a supporting job → return to the originating finding, preserving frozen/current evidence boundaries. Build on accepted R3; keep B2 review and its promotion rules intact. Small-set job comparison follows its own bounded design. See the existing roadmap/TODO owners rather than creating another plan.

The owner subsequently authorized implementation on 2026-10-15. Delivered: research-first Overview; grouped navigation with active-page/keyboard support; accepted-fact job preview before full documents; processing disclosures; frozen role/company evidence labels; and validated snapshot/report/finding return context retained through job/Work/Capability reading. Job pages explicitly show current local state and flag source changes relative to the originating snapshot. No generation, review, semantic contract, or comparison feature changed.

Verification: Ruff and 834 warnings-as-errors tests passed. A real Edge/Playwright run against a SQLite copy proved Overview → report #2 → job → Work → job → original finding, desktop/mobile layout, visible narrow-screen return action, keyboard skip, no horizontal overflow, and no page errors. Historical-label and invalid-origin regressions preserve source boundaries; UI subjective usefulness/time savings remain for owner use. Screenshots are local and untracked, not public-corpus exports.


## 9. B2 R1 execution — 2026-10-16

Owner approved the exact R1 definition and two mappings. Applied through existing
Registry CLI: `responsibility:design-implement-ai-agents`, mapping #7 to `tvMm`
artifact 50 responsibility[0] and #8 to `tNVe` artifact 56 responsibility[0].
Broader R1 cases remain pending. Registry totals: five concepts / eight mappings;
33 of the snapshot-selected 35 responsibilities remain pending.

Execution exposed a narrow write-validator defect: accepted-compatible v23/v5
was selected by currentness but rejected by Registry persistence. Fixed in
`dafdb05`, with 843 warnings-as-errors tests, Ruff, and successful normal CI
38893557722 before live application. Rehearsal and live idempotency, exact
provenance, rendered browser/CLI agreement, SQLite integrity/foreign keys, and
all other table/corpus preservation checks passed. Backups/results remain local
under `data/local-acceptance/b2-review-2026-10-16/`.

R2 was subsequently approved and applied as recorded below; its definition and
boundary exclusions remain in focused decision §14. B2 remains
active; no family, archetype, personal-readiness, or downstream authorization.


## 10. B2 R2 execution — 2026-10-16

Owner approved the exact R2 definition and pair. Applied
`responsibility:integrate-ai-systems-with-services` through the existing CLI,
with mapping #9 to `tvMm` artifact 50 responsibility[2] and #10 to `tNVe`
artifact 56 responsibility[2]. Broader R2 cases remain pending. Registry totals:
six concepts / ten mappings; four of the selected 35 responsibilities mapped,
31 pending. R1 rows and all other previous Registry rows are preserved.

Fresh backup and results remain local in
`data/local-acceptance/b2-review-2026-10-16/`. Exact current dependencies,
idempotency including review metadata, rendered browser/CLI agreement, SQLite
integrity/foreign keys, other-table preservation, and corpus hash preservation
passed. This was data-only: no code/model/source changes or full-suite rerun.

Next: owner review of R3, `responsibility:implement-llm-tool-calling`, exact
artifact 50/56 responsibility[3] pair. Proposed definition: implementing tool
calling or function calling for language-model-based systems. Structured Output
is additional scope only in the second posting. Exact wording, rationale, and
limits are in focused decision §15. No R3 mutation; B2 remains active.

## 11. State reconciliation — 2026-10-17

The owner published the previously local `tNpG` source/detail and English projection to `main`. Repository-safe corpus counts are now 420 jobs / 52 parsed details / 30 English projections / 11 accepted English P1.6 / 5 Capability artifacts. GitHub CI for the publication head passed.

The controlling current-state overlay, execution TODO, working memory, and top-level current-facing documentation are reconciled to the same present-tense state: R1/R2 are applied and verified; four of 35 selected responsibilities are mapped; R3 is the next semantic review. The October 15 statements describing all 35 responsibilities as pending or `tNpG` as unpublished remain historical evidence only.
