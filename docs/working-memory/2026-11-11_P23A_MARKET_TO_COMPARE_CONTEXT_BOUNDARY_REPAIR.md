# P2.3A — Market finding → job → comparison context repair

**Date:** 2026-11-11
**Status:** Experimental branch repair verified; no owner usefulness acceptance; no main-branch promotion
**Branch:** `experiment/p23a-compare-at-glance-2026-11-11`
**Prerequisites:** `docs/working-memory/2026-11-11_P23A_COMPARISON_FIRST_VIEW_PREDECISION.md`, `docs/working-memory/2026-11-11_P23A_COMPACT_OVERVIEW_REFINEMENT_RESULT.md`

## Reproduced issue

From the accepted local Market report #2, frozen snapshot #15, select a report-supported job and follow the `Compare requirements` action. The comparison preserved the originating report return path. However, after selecting a second job from the **same frozen snapshot**, its `Full job evidence` and `Open accepted analysis and source` links omitted the Market origin. The second job's detail page therefore no longer offered return to the original report finding.

The original implementation preserved context only when the selected job ID exactly equaled the first originating job ID. That condition was narrower than the frozen snapshot membership boundary.

The local snapshot contains **ten frozen member postings**; do not confuse that number with the accepted-semantic core denominator of the Market report.

## Minimal fix and provenance boundaries

- The existing validated `MarketJobOrigin` now carries immutable sets of *snapshot member IDs* and *members whose source has changed* since the frozen snapshot. They are derived from the same already-resolved snapshot membership, not from a new model or external lookup.
- `/compare` retains validated frozen Market-origin parameters in **all source/detail links belonging to that snapshot**, not just the original job.
- Jobs selected from outside the snapshot remain comparable by current evidence, but **do not** receive the originating frozen-context parameters. Their summary and detail cards clearly disclose that they were not evidence in the originating frozen Market snapshot.
- Any changed-source member also receives an explicit warning in comparison. The job-detail page independently validates that the selected job belongs to the claimed snapshot, and only then provides the report return path.
- No arbitrary return URL, new semantic correspondence, normalized cross-job demand, persistent profile, schema migration, or network/model call was added.

This repair does not change which facts qualify for `/compare`. The frozen Market report remains immutable while the comparison reads latest/current accepted local job evidence.

## Saved real-data evidence

The following public-safe files were automatically produced from the *existing local runtime* using an isolated online SQLite copy:

- `2026-11-11_p23a_market_navigation/REAL_SNAPSHOT_NAVIGATION_CHECK.json`: HTTP-level verification of report #2, snapshot #15, two valid public source-job members (`tNVe`, `tvMm`), and one outside public job (`tG9K`). All nine boolean boundary checks passed; report, job, and comparison returned HTTP 200; claiming snapshot context for `tG9K` was rejected with HTTP 404.
- `2026-11-11_p23a_market_navigation/BROWSER_NAVIGATION_CHECK.json`: actual Chromium/Playwright desktop (1440px) and mobile (390px) navigation through report → first job → comparison → second job → report. Both viewports passed all recorded navigation and provenance checks, with no observed JavaScript page errors or off-origin requests.

Raw local database copies, browser scripts, screenshots, source advertisements, model protocols, machine-specific paths, and credentials were **not committed**. The temporary browser server was loopback-only. The saved JSON reports contain fixed public job IDs and structural boolean/status evidence, not full employer text.

## Verification

In the checkout with project dev dependencies installed:

```bash
source .venv/bin/activate
pytest -q -W error tests/test_intelligence_navigation.py tests/test_job_comparison.py
pytest -q -W error
ruff check .
python -m pip check
git diff --check
```

The current focused tests passed **16/16**. The complete strict-warning test suite passed **880/880 in 48.39 seconds**, Ruff passed, and pip found no broken requirements. The new test covers another same-snapshot member, an outside-snapshot job, a source-version change, member-specific contextual links, and rejection of fraudulent outside-snapshot context.

These gates are engineering and navigation evidence, not proof of measured user effort reduction or semantic accuracy at market scale.

## Disposition

Keep this focused fix on the experimental branch. Do not merge the entire comparison UX experiment into `main` before evaluating the baseline against the prototype in actual repeated use. A provenance/context defect is independently actionable as a repair; the at-a-glance product usefulness decision remains separate.

**Next recommended work:** record owner comparison usefulness, decide whether to promote only the verified navigation repair or also the optional compact overview, and avoid extending P2.3 persistence or semantic cross-job equivalence without a separate evidence-supported gate.
