# Working Memory — P1.6 v15 Schedule-Concept Correction

**Date:** 2026-08-14  
**Status:** Active addendum to `2026-08-13_P16_V15_HANDOFF.md`  
**Gate:** sparse CI-3 on `t4jp`

## First live v15 run

The first live v15 run failed closed before persistence with:

```text
P1.6 v14 requirement[6] concept mixes capability with full-time/part-time schedule wording
```

No v15 artifact was created. The later snapshot commit attempt correctly had nothing to commit.

## Classification

This is not a new source-recall, coverage, duty, or depth failure. Instructor returned structured
output, but v15 inherited v14 `_run_once`, which invoked the strict concept validator before v15
could normalize schedule wording out of a capability concept.

No v16 is warranted: no v15 artifact exists and the v15 semantic contract already requires
schedule-free normalized capability concepts.

## Correction

`src/jobhunter/analysis_runtime_v15.py` now performs bounded deterministic normalization before the
unchanged strict v14/v15 concept validator:

```text
real capability + full-time/part-time wording
→ strip only schedule wording from concept
→ keep exact evidence unchanged
→ validate strictly

pure schedule/logistics concept
→ do not manufacture a capability
→ leave unchanged
→ strict validator rejects it
```

Regression examples:

```text
Producing visual content full-time and part-time
→ Producing visual content

Full-time availability
→ remains invalid / fails closed
```

Tests are in `tests/test_analysis_v14_candidate.py` alongside the prior v15 boundary tests.

## Verification

CI run 689 on commit `2403bc3d86bdabf002e7ca9b81a6e2957d3dd168` passed:

```text
Ruff: PASS
full pytest: PASS
warnings-as-errors: PASS
```

## Next step

Run sparse v15 again only. Do not run Capability or dense `tG9K` yet.
