# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-10-17
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`  
**P2.2 plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Current direction decision:** `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`  
**R3 decision:** `docs/working-memory/2026-10-17_P2_2B_B2_R3_SEMANTIC_DECISION.md`  
**R4-R6 decisions:** `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / ROLE-FAMILY REPORT R1-R4 ACCEPTED / P2.2B-B2 ACTIVE  
**Active increment:** P2.2B-B2 snapshot-15 selective responsibility normalization using existing P2.1 Canonical Registry review machinery. Semantic review of R1-R6 is complete; R3-R6 local Registry application/verification is the active operation. P2.2C/P2.2D/P2.3/P2.4 remain unauthorized.

Status vocabulary:

```text
[ ] not started
[~] in progress / acceptance incomplete
[x] accepted/completed for stated scope
[!] blocking defect
[-] deliberately deferred
```

---

## A. Closed accepted substrate

- [x] Phase 1 CLOSED / ACCEPTED.
- [x] P2.1 Canonical Registry CLOSED / ACCEPTED.
- [x] P2.2A Job Work Intelligence v2 CLOSED / ACCEPTED.
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.
- [x] Market foundation PASS / COMPLETE.
- [x] Market I1-I7 ACCEPTED / bounded first vertical slice CLOSED.
- [x] Same-target coverage follow-up COMPLETE: snapshots 14-15 contain ten qualified members, six core and six accepted-semantic core postings.
- [x] Candidate interpretation V6 CLOSED / accepted for bounded reporting.
- [x] `RoleFamilyIntelligenceReport` R1-R4 ACCEPTED / CLOSED.
- [x] R4 final artifact #2 accepted for bounded analytical use; artifact #1 preserved pending as historical pre-repair evidence.
- [x] R4 exact reuse proven: attempts `(1, completed, 1)`, `(2, completed, 2)`, `(3, reused, 2)` with two total report artifacts.
- [x] Current English P1.6 generation contract: `job-analysis-english-v30 / job-analysis-v5` with accepted-only compatibility inputs under exact dependency rules.
- [x] Capability current contract: `job-capability-intelligence-v9 / job-capability-intelligence-v5`.
- [x] Public corpus baseline: 420 jobs / 52 parsed details / 30 English projections / 11 accepted English P1.6 / 5 Capability artifacts.
- [x] Previously local `tNpG` source/detail + English projection intentionally published 2026-10-17; no P1.6, Capability, Registry, or Market authority was added by that publication.

Key closure/current records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`
- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R3_SEMANTIC_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`

Do not reopen accepted historical work without a repeatable material contradiction.

---

## B. Phase-2 direction decision — CLOSED

- [x] Reconstructed P2.1 Canonical Registry boundary.
- [x] Reconstructed P2.2A Work Intelligence v2 boundary.
- [x] Re-read B1 NO-PROMOTION evidence.
- [x] Established that B1 failed because no accepted second P1.6 claim authority existed, not because responsibility correspondence was disproven.
- [x] Audited snapshot-15 accepted-semantic responsibility evidence: 35 duties across `tvMm`, `tmvA`, `tjgi`, `tNVe`.
- [x] Audited Capability v9 authority and current canonical-coverage limits.
- [x] Compared Direction A vs B vs C.
- [x] Selected Direction A at the **P2.2B normalization layer**, not P2.2C family promotion.
- [x] Deferred P2.3 without rejecting its long-term value.
- [x] Kept P2.4 downstream.
- [x] Confirmed existing `jobhunter-registry` machinery is sufficient for the next tranche; no new subsystem is justified yet.

Decision:

```text
Direction A                          SELECTED
P2.2B-B2                             AUTHORIZED
P2.2C ResponsibilityFamily           NOT AUTHORIZED
P2.2D stable RoleArchetype           NOT AUTHORIZED
P2.3 capability profiles             DEFERRED / NOT AUTHORIZED
P2.4 Market v2                       DOWNSTREAM / NOT AUTHORIZED
```

---

## C. P2.2B-B2 — ACTIVE

### B2.1 Read-only maintainer baseline

- [x] Pull current `main`; do not reset unrelated pre-existing local changes.
- [x] Back up the configured SQLite database before Registry mutation.
- [x] Record pre-run `PRAGMA integrity_check` and `PRAGMA foreign_key_check`.
- [x] List exact accepted/current `responsibility` claims for `tvMm`, `tNVe`, `tjgi`, `tmvA`.
- [x] Confirm expected P1.6 artifacts: `tvMm=50`, `tNVe=56`, `tjgi=60`, `tmvA=61`.
- [x] Record existing Registry `responsibility` concepts and mapping states for the selected claims.
- [x] Stop/re-evaluate any candidate whose exact claim is no longer accepted/current; do not silently substitute a different claim.

Verified on 2026-10-15 at `bf016c7`: SQLite integrity `ok`, foreign keys empty; exact artifacts 50/56/60/61 remain accepted/current. At that historical baseline all 35 selected responsibility claims were pending Registry review. Baseline backup: `data/local-acceptance/project-alignment-2026-10-15/baseline-181157.sqlite3`.

### B2.2 Semantic review — COMPLETE

- [x] R1 — ACCEPTED / APPLIED / VERIFIED: `responsibility:design-implement-ai-agents`, exact mappings 50[0] + 56[0].
- [x] R2 — ACCEPTED / APPLIED / VERIFIED: `responsibility:integrate-ai-systems-with-services`, exact mappings 50[2] + 56[2].
- [x] R3 — ACCEPTED / APPLICATION PENDING: `responsibility:implement-llm-tool-calling`, exact approved pair 50[3] + 56[3]. `Structured Output` remains source-specific.
- [x] R4 — ACCEPTED / APPLICATION PENDING: `responsibility:develop-rag-systems`, exact approved pair 50[6] + 56[4]. The earlier tentative `...rag-knowledge-retrieval` identity was narrowed because `Knowledge-based systems` != `Knowledge Retrieval`; only the common RAG-development core is normalized.
- [x] R5 — ACCEPTED / APPLICATION PENDING: `responsibility:design-develop-multi-step-ai-workflows`, exact approved pair 50[7] + 56[5]. Reliability and Multi-Agent/Email/Ticketing/module-integration scope remain source-specific.
- [x] R6 — ACCEPTED / APPLICATION PENDING: `responsibility:evaluate-improve-ai-system-performance`, exact approved pair 50[8] + 56[7]. Debugging and specific quality/reliability/latency/cost dimensions remain source-specific.
- [x] R6 boundary `tvMm` 50[9] remains pending; “paying attention to” cost/latency/reliability/output quality is not the same explicit evaluate/improve action.

Semantic review rule results:

- [x] equivalence reviewed from exact accepted responsibilities, not shared keywords;
- [x] source-specific technology/object/context/lifecycle scope preserved;
- [x] no requirement-only job created a responsibility fact;
- [x] broader/boundary claims stayed separate unless explicitly accepted;
- [x] no numeric quota forced promotion.

### B2.3 Apply accepted correspondences only — ACTIVE

Current proven local Registry state is still R1/R2 only: 4 of 35 selected responsibilities mapped, 31 pending.

Before R3-R6 mutation:

- [~] Pull current `main` and preserve unrelated local state.
- [~] Back up configured SQLite to a fresh pre-R3-R6 backup.
- [~] Verify `PRAGMA integrity_check = ok` and `PRAGMA foreign_key_check = []`.
- [~] Reconfirm all eight approved claims are still accepted/current and pending:
  - `tvMm` 50[3], 50[6], 50[7], 50[8]
  - `tNVe` 56[3], 56[4], 56[5], 56[7]
- [~] Create/reuse only these concepts:
  - `responsibility:implement-llm-tool-calling`
  - `responsibility:develop-rag-systems`
  - `responsibility:design-develop-multi-step-ai-workflows`
  - `responsibility:evaluate-improve-ai-system-performance`
- [~] Map only the eight explicitly approved claims.
- [x] Add no aliases for R3-R6.
- [x] Leave `tvMm` 50[9] and broader R1/R2 boundary claims pending.

Exact command protocol is controlled by:

`docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`

If all eight claims remain eligible, the expected verified post-state is 12/35 mapped and 23 pending. Do not record that as current state before application proves it.

### B2.4 Verification

After local R3-R6 application:

- [~] Reapply the same concept/mapping commands and prove idempotent reuse/no duplicate state.
- [~] CLI Registry views show all four accepted concepts, all eight approved mappings, and exact source wording.
- [~] Browser Registry views show the same reviewed state.
- [~] Post-run `PRAGMA integrity_check = ok`.
- [~] Post-run `PRAGMA foreign_key_check = []`.
- [~] R1/R2 and all unrelated Registry rows remain unchanged.
- [~] `tvMm` 50[9] remains pending.
- [~] Accepted P1.6 artifacts and Market snapshot identities remain unchanged.
- [~] Repository-safe `corpus/` hashes remain unchanged by Registry mutation; Registry publication remains unauthorized.
- [ ] If no product/code defect appears, do not create code/test changes merely to accompany semantic local-state review.
- [ ] If execution exposes a real product/contract defect, fix only that defect, add focused regression evidence, and run normal CI before continuing.

### B2.5 Closure

- [ ] Record exact applied concept/mapping row identities.
- [ ] Record pending boundary claims and why they were not normalized.
- [ ] Record idempotency, CLI/browser, integrity/FK and preservation proof.
- [ ] State explicitly: reviewed canonical responsibility correspondence != ResponsibilityFamily != market prevalence.
- [ ] Close B2 for the bounded six-candidate tranche.
- [ ] STOP after B2; make a separate P2.2C-vs-P2.3 readiness decision.

---

## D. Product usability alongside semantic work

- [x] Owner priority confirmed: improve whole-product usability, productivity, and usefulness; prioritize understanding/comparing jobs and Market findings.
- [x] Source-level journey review identified broad-processing-first Overview, document-first job detail, opaque evidence link labels, and loss of explicit finding context when returning from a job.
- [x] Implemented the owner-authorized first navigation/UI slice: research-first Overview; grouped navigation; accepted-fact job preview; processing disclosures; frozen role/company evidence labels; validated snapshot/report/finding return context through job/Work/Capability reading.
- [x] Viewing pages does not generate artifacts or append review state; current-versus-historical source boundaries remain explicit.
- [x] Real Edge/Playwright verification on a SQLite copy covered desktop and 390px viewport, same-finding return, mobile back action, keyboard skip, no horizontal overflow/page errors, and relevant regressions; 834 warnings-as-errors tests passed for that slice.
- [ ] Owner repeated-use assessment of comprehension and remaining friction.
- [ ] Scope any subsequent small-set job comparison separately; use accepted facts, approved B2 correspondences where available, and clearly labeled interpretation. No personal scoring or automatic taxonomy promotion.

The first navigation/UI slice is implemented and locally verified. R3-R6 local Registry application/verification is now the active semantic operation. No job-comparison feature or later semantic layer is authorized by B2.

## E. Permanent authority invariants

- [x] source fact != normalized correspondence != analytical interpretation != recommendation/decision synthesis.
- [x] generated/candidate != reviewed/promoted.
- [x] exact P1.6 claim remains recoverable after canonical mapping.
- [x] Work Intelligence candidate labels do not auto-promote.
- [x] RoleFamilyIntelligenceReport labels do not auto-promote.
- [x] target identity is separate from immutable target-definition meaning.
- [x] search/acquisition envelope != target membership truth != canonical role taxonomy.
- [x] pending/missing/failed/rejected P1.6 != zero demand.
- [x] only accepted-current P1.6 contributes to strong semantic statistics.
- [x] numeric Market counts/denominators remain deterministic application responsibilities.
- [x] Market/Registry/personal state remains local/private unless separately authorized for publication.

---

## F. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families during B2.
- [-] P2.2D stable promoted role archetypes during B2.
- [-] bulk normalization of all 35 responsibility claims.
- [-] requirement/capability canonicalization in this B2 tranche.
- [-] P2.3 corpus-scale capability requirement profiles.
- [-] P2.4 Market v2.
- [-] P1.6 auto-acceptance.
- [-] authoritative Blueprint use.
- [-] automatic repost/new-ID collapse without real evidence.
- [-] broad-market trend/emerging/forecasting claims before comparable snapshots.
- [-] Market → You / personal readiness, gaps or scoring before reviewed personal evidence.
- [-] Registry/Work/Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure without demonstrated need.

---

## G. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden the active semantic authorization.

---

## Exact next action

```text
B2.1 baseline COMPLETE
→ R1/R2 applied + verified
→ R3-R6 semantic review COMPLETE / ACCEPTED
→ apply exact R3-R6 concepts + eight approved mappings to maintainer SQLite
→ verify idempotency + CLI/browser agreement + integrity/FK + preservation
→ record final B2 disposition
→ STOP
→ separate P2.2C-vs-P2.3 readiness decision
```
