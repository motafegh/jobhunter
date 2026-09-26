# Market I7 — accepted core analysis and target reuse repair

**Date:** 2026-09-26
**Status:** ACCEPTED CORE SEMANTICS / MARKET I7 STILL HOLD

Normal persisted v23 `tvMm` analysis created **artifact 50**, source detail **47**,
English projection **41**, `job-analysis-english-v23 / job-analysis-v5`.
All 25 requirements, 11 duties, role-purpose entries, source evidence, strength,
depth, confidence and rationale exactly matched the separately reviewed full
non-persistent result. The whole artifact was explicitly accepted after source
review. Public corpus projection verified with **410 known jobs**, **27 English
projections**, **6 accepted English P1.6**, and **5 accepted Capability**.

The first post-acceptance Market run (run 3) used definition 1 with five one-page
searches, request budget 5, source/translation/analysis budgets zero, and the
original 168-hour refresh threshold. It completed with no stage failures,
discovered 53 search-page candidates including 16 newly known source IDs, and
created immutable snapshot/profile 3 with **zero members**. This is not zero
market demand: all eight previously qualified members were refresh-due and the
source-refresh budget was zero. Historical snapshots 1 and 2 remain authority
for their points in time.

The coordinator previously restricted its next candidate set to current search
pages. It now unions those IDs with source IDs from the latest nonempty snapshot
for the same immutable definition, de-duplicates in stable order, and records
discovery count, carry-forward count and total target candidate count separately.
The existing planner still decides source freshness, lifecycle, translation and
analysis currentness; membership and snapshot checks are unchanged. A recent
empty snapshot does not erase the last qualified target cohort. Regression tests
cover search-page turnover, overlap, and store lookup past an empty snapshot.

The read-only plan at 168 hours identifies all eight carried members as
`refresh_due`; raising the freshness threshold to 240 hours would mark them
current without a new source observation. Keep 168 hours and run a bounded
refresh instead. No Market state is published into `corpus/`.

Ruff PASS, full strict-warning suite **741 PASS**, public-corpus verification
PASS for **410 jobs**. Next: source refresh for at most eight carried members,
no fresh analysis unless a source dependency genuinely changes, then a new
immutable snapshot/profile and real CLI/browser accepted-semantic drill-down.
I7 remains HOLD until those checks pass.
