# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-29  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED  
**Active increment:** Market candidate interpretation V3.2 / contract v5 — V4 real-model rerun failed safely on a prose/source-evidence mismatch; V5 reduces blast radius by filtering only unsafe generated elements, with green regression gates and a fresh snapshot-15 rerun pending.

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

- [x] Phase 1 CLOSED.
- [x] P2.1 Canonical Registry CLOSED.
- [x] P2.2A Job Work Intelligence CLOSED.
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.
- [x] Market foundation investigation PASS.
- [x] Market I1-I7 ACCEPTED / bounded first vertical slice CLOSED.
- [x] Same-target coverage follow-up complete in snapshots 14-15: ten qualified members, six core, six accepted-current P1.6.
- [x] Current English P1.6 generation contract: `job-analysis-english-v30 / job-analysis-v5`.
- [x] Public corpus current baseline: 420 jobs, 51 parsed details, 29 English projections, 11 accepted English P1.6, 5 Capability artifacts.

Do not reopen accepted historical work without a repeatable current contradiction.

Key closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`

Historical HOLD-era execution remains evidence only and does not control current routing.

---

## B. Active Market candidate interpretation

Current record:

`docs/working-memory/2026-09-29_MARKET_CANDIDATE_INTERPRETATION_V1.md`

Current implementation:

- [x] Historical v3 bounded Gemma/MiMo/browser evaluation completed over snapshot 15.
- [x] Owner usefulness review of the captured v3 report completed: the synthesis is useful enough to continue, but v3 is not persistence-ready.
- [x] Concrete v3 defects recorded: duplicate overall source display, available-vs-cited evidence mislabeling, internal compact-ID leakage, weak prose/source binding, unbound alternatives, and one-posting role candidates presented too much like reusable subfamilies.
- [x] V3.1 used `market-role-family-candidate-v4 / market-role-family-candidate-prompt-v4` because the response/evidence contract changed materially.
- [x] Real V4 snapshot-15 run on 2026-09-30 failed safely with `source_alias_without_matching_evidence`; no candidate report entered browser cache.
- [x] V3.2 advances to `market-role-family-candidate-v5 / market-role-family-candidate-prompt-v5` because post-generation integrity handling changed materially.
- [x] Reads one immutable Market snapshot and accepted, exact-identity P1.6 only.
- [x] Overall observations, interpretation points, and alternatives are individually evidence-bound.
- [x] Internal compact `C*` IDs in user-facing prose are rejected at the generated-element boundary.
- [x] A source alias mentioned by an interpretation must be backed by evidence from that same source; violating elements are omitted rather than rendering unsupported prose.
- [x] Employer names and job titles are withheld from model input; source details must come from cited claims.
- [x] Application owns distinct-source support, available-vs-cited evidence counts, posting counts, confidence caps, and responsibility-vs-requirement support basis.
- [x] One-posting role candidates are separated as specialty/outlier candidates rather than counted as multi-posting role subfamilies.
- [x] Report remains ephemeral: no Market/report persistence and no corpus publication.
- [x] CLI and browser share the same generator.
- [x] V5 post-validation is partial-safe: invalid observations, alternatives, groups, or model caveats are omitted with path/code diagnostics; the whole report still fails if no integrity-safe interpretation survives.
- [x] Dedicated regression coverage includes evidence binding, compact-ID rejection, source-alias/source-evidence consistency, partial filtering, invalid-alternative retention of safe groups, all-unsafe failure, singleton specialty handling, exact identity rejection, CLI model override, browser rendering, and non-persistence.
- [x] CI `36758263560` passed Ruff + 816 tests + 816 warnings-as-errors tests.
- [~] Fresh real-model/browser re-evaluation of snapshot 15 under v5.
- [ ] After that rerun, make the explicit report disposition:
  - keep the interpretation ephemeral; or
  - separately authorize a persisted/versioned `RoleFamilyIntelligenceReport` contract.
- [ ] Only after representative evidence supports it, decide whether any responsibility-family / role-archetype interpretation deserves reviewed promotion.

Acceptance boundary:

```text
useful bounded interpretation
+ traceable evidence
+ regression-protected contract
!= promoted taxonomy
```

Do not promote role families from the current six-posting sample.

---

## C. Permanent Market / authority invariants

- [x] target identity is separate from immutable target-definition meaning.
- [x] search/acquisition envelope != target membership truth.
- [x] source-level membership is `core_match / adjacent_match / uncertain / excluded`.
- [x] target-scoped work does not spill into unrelated backlog.
- [x] `uncertain` is a successful semantic outcome.
- [x] adjacent/uncertain/excluded never silently enter the primary core denominator.
- [x] missing/pending/failed/rejected P1.6 never means zero demand.
- [x] only accepted-current P1.6 contributes to strong semantic statistics.
- [x] snapshot members reference exact dependencies.
- [x] snapshots and aggregate profiles remain immutable historical authority.
- [x] first-slice denominator remains `qualified source postings`, not unproven unique demand.
- [x] numeric counts are deterministic application responsibilities.
- [x] browser and CLI share state/service owners.
- [x] Market state remains local/private by default.

---

## D. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families without representative reviewed evidence.
- [-] P2.2D stable promoted role archetypes without representative reviewed evidence.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as mandatory Market gates.
- [-] automatic repost/new-ID collapse without real evidence.
- [-] broad-market trend / emerging / forecasting claims before comparable snapshots.
- [-] Market → You / personal readiness, gaps or scoring before reviewed personal evidence.
- [-] Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure without demonstrated need.

---

## E. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden the active semantic authorization.

---

## Exact next action

```text
pull/restart the current app
→ regenerate snapshot 15 candidate interpretation under v5
→ capture and review the new report against the recorded v3 defects
→ make the explicit ephemeral-vs-persisted report decision
→ only then proceed to broader Phase-2 responsibility-family / capability-profile work
```
