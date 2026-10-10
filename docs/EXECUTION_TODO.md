# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-10-10  
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
- [x] Public corpus baseline: 420 jobs / 51 parsed details / 29 English projections / 11 accepted English P1.6 / 5 Capability artifacts.

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

- [ ] Pull current `main`; do not reset unrelated pre-existing local changes.
- [ ] Back up the configured SQLite database before Registry mutation.
- [ ] Record pre-run `PRAGMA integrity_check` and `PRAGMA foreign_key_check`.
- [ ] List exact accepted/current `responsibility` claims for `tvMm`, `tNVe`, `tjgi`, `tmvA`.
- [ ] Confirm expected P1.6 artifacts: `tvMm=50`, `tNVe=56`, `tjgi=60`, `tmvA=61`.
- [ ] Record existing Registry `responsibility` concepts and mapping states for the selected claims.
- [ ] Stop/re-evaluate any candidate whose exact claim is no longer accepted/current; do not silently substitute a different claim.

### B2.2 Owner semantic review — no mutation first

Review these six candidates one at a time as `ACCEPT | HOLD | REJECT`:

- [ ] R1 — design / implement AI agents.
- [ ] R2 — integrate AI systems with APIs / databases / services.
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
- [ ] Repository-safe `corpus/` remains unchanged; Registry publication is still unauthorized.
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

## D. Permanent authority invariants

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

## E. Explicitly deferred / not authorized

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

## F. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden the active semantic authorization.

---

## Exact next action

```text
P2.2B-B2.1 read-only baseline
→ local sync + SQLite backup/integrity
→ inspect exact current responsibility claims for tvMm/tNVe/tjgi/tmvA
→ inspect current Registry concepts/mapping states
→ bring the exact evidence into B2.2
→ review R1-R6 with the owner before any canonical mutation
```
