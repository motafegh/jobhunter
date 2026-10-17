# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-10-17
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`  
**P2.2 plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Current decision:** `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / ROLE-FAMILY REPORT R1-R4 ACCEPTED / P2.2B-B2 ACTIVE  
**Active increment:** P2.2B-B2 snapshot-15 selective responsibility normalization using existing P2.1 Canonical Registry review machinery. P2.2C/P2.2D/P2.3/P2.4 remain unauthorized.

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

Verified on 2026-10-15 at `bf016c7`: SQLite integrity `ok`, foreign keys empty; exact artifacts 50/56/60/61 remain accepted/current; all 35 selected responsibility claims are pending Registry review. Baseline backup: `data/local-acceptance/project-alignment-2026-10-15/baseline-181157.sqlite3`. Repeat the baseline only if dependencies/state change before mutation.

### B2.2 Owner semantic review — no mutation first

Review these six candidates one at a time as `ACCEPT | HOLD | REJECT`:

- [x] R1 — ACCEPTED / APPLIED 2026-10-16: `responsibility:design-implement-ai-agents`, exact mappings #7 (50[0]) and #8 (56[0]); broader cases pending. Idempotency, rendered browser/CLI agreement, integrity, and non-mutation checks passed; see focused decision §14.
- [x] R2 — ACCEPTED / APPLIED 2026-10-16: `responsibility:integrate-ai-systems-with-services`, mappings #9 (50[2]) and #10 (56[2]); broader cases pending. Idempotency, rendered browser/CLI agreement, integrity, and preservation checks passed; focused decision §15.
- [ ] R3 — implement LLM Tool / Function Calling.
- [ ] R4 — develop RAG / knowledge-retrieval systems.
- [ ] R5 — design / develop multi-step AI workflows.
- [ ] R6 — evaluate / improve AI-system performance.

Exact pairs, tentative IDs and boundary members are controlled by:

`docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`

Rules:

- [ ] semantic equivalence must be reviewed from exact accepted responsibilities, not shared keywords;
- [ ] preserve source-specific technology/object/context/lifecycle scope;
- [ ] no requirement-only job may create a responsibility fact;
- [ ] broader candidate members remain separate boundary tests unless explicitly accepted;
- [ ] no numeric quota forces any correspondence to pass.

### B2.3 Apply accepted correspondences only

For each accepted candidate only:

- [ ] create/reuse the reviewed `responsibility:*` canonical concept through existing Registry tooling;
- [ ] map only the explicitly approved exact claims;
- [ ] add aliases only when they have independent lexical reuse value, not to duplicate source claim wording;
- [ ] add no unrelated concepts/mappings.

Claims not reviewed into an accepted correspondence remain pending unless a specific semantic decision justifies another disposition.

### B2.4 Verification

- [ ] Reapply the same reviewed concept/mapping commands and prove idempotent reuse/no duplicate state.
- [ ] CLI Registry views show the exact approved concepts/mappings/source wording.
- [ ] Browser Registry views show the same reviewed state.
- [ ] Post-run `PRAGMA integrity_check = ok`.
- [ ] Post-run `PRAGMA foreign_key_check = []`.
- [ ] Accepted P1.6 artifacts and Market snapshot identities remain unchanged.
- [ ] Repository-safe `corpus/` remains unchanged by Registry review/application; Registry publication is still unauthorized.
- [ ] If no product/code defect appears, do not create code/test changes merely to accompany semantic local-state review.
- [ ] If execution exposes a real product/contract defect, fix only that defect, add focused regression evidence, and run normal CI before continuing.

### B2.5 Closure

- [ ] Record exact accepted canonical concepts and mapped claims.
- [ ] Record held/rejected candidate groups and why their boundaries did not justify normalization.
- [ ] Record local row IDs where useful plus CLI/browser/idempotency/integrity proof.
- [ ] State explicitly: reviewed canonical responsibility correspondence != ResponsibilityFamily != market prevalence.
- [ ] Close B2 as ACCEPTED for the bounded tranche or NO-PROMOTION / DEFER if no candidate survives review.
- [ ] STOP after B2; make a separate P2.2C-vs-P2.3 readiness decision.

---

## D. Product usability alongside semantic work

- [x] Owner priority confirmed: improve whole-product usability, productivity, and usefulness; prioritize understanding/comparing jobs and Market findings.
- [x] Source-level journey review identified broad-processing-first Overview, document-first job detail, opaque evidence link labels, and loss of explicit finding context when returning from a job.
- [x] Prepare the first bounded screen/interaction design: Overview leads with read-only Market and interested-job entry points; daily navigation separates from maintenance; job detail leads with accepted work/requirements and keeps full documents/processing inspectable; pinned source-version labels identify supporting jobs; validated snapshot/report parameters provide a return path and explicit current-versus-historical context.
- [x] Implement the owner-authorized navigation/UI slice (2026-10-15). Overview now leads with existing intelligence; navigation groups daily research and management; job detail leads with an accepted-fact preview; exact-version role/company labels and validated return context connect findings to jobs and Work/Capability views. Processing/full source remain available through disclosures.
- [x] Use existing accepted artifacts and R3 presentation; retain exact historical/current distinction, source evidence, uncertainty, and review boundaries. Viewing pages does not generate artifacts or append review state.
- [x] Verify the retained snapshot-15/report-2 journey in a real browser on a SQLite copy, desktop and 390px viewport: return to the same finding, human-readable source labels, visible mobile back action, keyboard skip, no horizontal overflow or page errors. 834 warnings-as-errors tests pass, including changed-source historical-label and invalid-origin regressions.
- [ ] Owner repeated-use assessment of comprehension and remaining friction; no subjective acceptance or measured time savings is claimed by the browser checks.
- [ ] Scope any subsequent small-set job comparison separately; use accepted facts, approved B2 correspondences where available, and clearly labeled interpretation. No personal scoring or automatic taxonomy promotion.

The owning UX direction is in `docs/ROADMAP.md` §13. The first navigation/UI slice is implemented and locally verified; owner usefulness review remains distinct. B2.2 review of R3-R6 remains next for the semantic stream. No job-comparison feature or new semantic layer was added.

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
P2.2B-B2.1 read-only baseline COMPLETE (2026-10-15)
→ R1/R2 approved/applied/verified (2026-10-16)
→ B2.2 review R3-R6 with the owner
→ R3 exact pair is artifact 50 responsibility[3] ↔ artifact 56 responsibility[3]
→ no canonical mutation before explicit semantic approval
→ apply only accepted correspondences, then verify and close B2
```
