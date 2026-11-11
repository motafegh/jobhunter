# P2.3A bounded comparison — final stage closure and next product gate

**Date:** 2026-11-11
**Status:** CLOSED for engineering/available factual comparison; NO PROMOTION of experimental summary.
**Authority:** Owner explicitly requested that the comparison-review stage be completed rather than continuing cosmetic increments. This decision closes the bounded P2.3A *engineering and incremental UX exploration* work, not the entire P2.3 capability program.
**Baseline:** `main` at `21f9d03` (2026-10-26) delivered the bounded read-only `/compare` feature.
**Follow-up evidence:** review branch `review/p23a-compare-usefulness-2026-11-06`; experimental branch `experiment/p23a-compare-at-glance-2026-11-11`.

## 1. Separate disposition of the two outcomes

**A. Baseline factual comparison: RETAIN.**
The existing job comparison preserves exact accepted/current claim evidence, requirement obligation and explicit depth, the separation of qualifications from direct duties, reviewed claim-level Registry correspondence, and optional job-local Capability grouping with overlap disclosed. A no-match is not no demand; lack of responsibilities does not license inferred duties. Small selected-job comparisons use existing database reads, not persistent profiles or automatic market prevalence.

**B. Cross-job Market-origin navigation defect: REPAIR / PROMOTE.**
The accepted October 26 baseline accidentally kept frozen Market context only on the *first* selected job's evidence links. If a second compared posting belonged to the same frozen snapshot, navigating to that posting dropped its report/finding return path. This is a reproducible correctness/continuity defect, not a cosmetic preference. The focused repair promotes only validated snapshot membership context to other member-job links, adds explicit changed-source and outside-snapshot disclosure, and withholds frozen provenance from unrelated job links. The pre-existing per-job Market reader continues to reject invalid membership with 404. No new database model, model inference, source acquisition, external link, or profile persistence.

**C. Optional “at a glance” prototype: NO PROMOTION / ARCHIVE.**
The prototype is fully implemented, tested and retained in its experimental branch for historical comparison; it is **not** merged into the accepted UI. It provided compact raw counts but no semantic alignment, moved details farther down the page, and made repeated editing one disclosure click more expensive in the refinement. The 390px RAG first-claim position was about 1,411px in baseline, 2,233px in first prototype, and 1,554px in refined prototype. The summary appears earlier, but these are document geometry observations only. No actual owner time-savings, comprehension improvement, adoption, or user-preference result was observed. Continuing to refine appearance without an independently demonstrated task benefit is not justified.

**Owner repeated-use outcome: NOT MEASURED / NOT CLAIMED.** We close the *engineering and optional-UX experiment* without inventing acceptance. It is not a pending condition for retaining the already-accepted factual comparison or fixing the proven context defect. Any future UX redesign should be triggered by real task friction or an explicit product requirement, not by keeping this prototype alive.

## 2. Evidence and safe provenance

Live local checks were performed only against SQLite online backups, including snapshot #15/report #2. The snapshot contains ten frozen members; this is **not** the six-job accepted-semantic core denominator.

A two-member comparison returned validated report context for `tNVe` and `tvMm`, with unrelated `tG9K` explicitly outside the snapshot. All nine structural boundary checks passed. A contextual request for the outside job returned HTTP 404. A real Chromium navigation exercise crossed report → first job → comparison → second member job → report at desktop and 390px width, with return context maintained, and no page errors or off-origin requests. See:
- `docs/working-memory/2026-11-11_p23a_market_navigation/REAL_SNAPSHOT_NAVIGATION_CHECK.json`
- `docs/working-memory/2026-11-11_p23a_market_navigation/BROWSER_NAVIGATION_CHECK.json`

The experimental branch reached 880 strict-warning tests. The isolated fix against the original `main` baseline independently passed **879 strict-warning tests in 48.44 seconds**, repository Ruff, Python dependency consistency, and real local snapshot-15/report-2 structural checks on an isolated SQLite backup. The one-test difference is intentional: the unpromoted experimental overview's regression is absent from `main`. GitHub Actions CI after publication is an independent final verification gate.

Historical investigations and prototype evaluations are retained on their separate GitHub branches. Only repository-safe aggregate evidence and explicit reviewed decisions are published; raw SQLite, local screenshots, employer-ad content, and model prompts are excluded.

## 3. Explicit stop lines / engineering close

- Do not reopen baseline /compare, re-run these same four scenarios repeatedly, or build more UX variants merely to keep P2.3A active.
- Do not merge the experimental at-a-glance template, mobile CSS, or disclosure just because tests pass.
- No claimed owner usability acceptance, general speedup, canonical semantic equality from lexical matching, model-generated P2.3 profile, personal fit, market-wide demand, or source-level responsibilities inferred from qualifications.
- The separately accepted B2 six-responsibility normalization remains 12 mapped/23 pending; do not reapply it or bulk-normalize the rest.
- The accepted October 26 factual projection, archived experimental outputs, and Market report #2 remain unchanged.
- After main-branch gates and CI, the bounded comparison engineering stage is CLOSED and **not** the active backlog.

## 4. Next substantive product gap, not another cosmetic task

The main user question now unanswered is: **“For this specific real job, what does the employer actually expect me to be able to do with a capability, how deep is the evidence, what is only inferred, and what remains unknown?”** Showing ten lexical matches or a raw count does not answer this.

The next proposed high-value slice is a **job-specific capability expectation / technical-work explanation** built from current accepted P1.6 facts and existing Capability-v9/Work/Registry boundaries, with exact evidence and bounded local model reasoning only where needed. Representative cases should contrast a requirement-only job and a job with explicit work, and distinguish broad labels (e.g. Python or RAG) from actual activities, concrete constraints, independence, and absent scope. This is a capability feature, not a UI refresh or cosmetic grouping.

The design/acceptance contract is in `docs/working-memory/2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md`. That document is a proposed next decision gate, not automatic authorization of new durable profile tables or mass generation.

**Next action:** finish/promote only the narrow navigation repair to `main`, record green validation, then take the new capability question as the next independently gated feature increment.
