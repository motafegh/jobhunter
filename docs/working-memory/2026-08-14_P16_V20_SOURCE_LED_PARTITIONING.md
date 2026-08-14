# P1.6 v20 — Source-Led Bounded Semantic Partitioning

**Date:** 2026-08-14  
**Status:** Implemented candidate / deterministic CI PASS / dense live acceptance pending  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Stacked PR:** #8  
**Prompt:** `job-analysis-english-v20`  
**Schema shape:** `job-analysis-v5`

## Trigger

The dense `tG9K` v19 live run did not fail on the previous v18 depth/optionality defects. Instead it exposed whole-answer retry oscillation.

Generation 1 retained the segment-13 surfaces (`Python (expert)`, SQL, MATLAB preferred, C/C++ preferred) but omitted structured Python plus the long contextual stack. The aggregate validator reported the missing set.

Generation 2 repaired structured Python and the long contextual stack, but dropped the four segment-13 surfaces that generation 1 had already represented correctly. No artifact persisted.

This is classified as a dense retry-state / cognitive-load defect, not a new semantic-rule defect and not a reason to loosen validation or increase one giant output budget.

## V20 design

V20 stops asking one model response to own every independent dense requirement surface simultaneously.

JobHunter now:

1. builds the complete model-owned source coverage ledger;
2. preserves v18 deterministic education/minimum-experience ownership;
3. partitions model-owned requirement coverage into bounded slices of at most 8 references;
4. processes core/non-excludable/required/preferred/structured-skill coverage before contextual/excludable coverage;
5. assigns responsibility coverage only to the first partition;
6. gives every partition the full exact evidence catalog for grounding but only its own explicit coverage ledger;
7. rejects requirements, duties, role purpose, or exclusions that leak outside the assigned partition;
8. merges independently validated partitions by exact identity;
9. materializes deterministic structured facts;
10. runs the existing v15/v16/v17/v18/v19 normalization and whole-artifact strict validators against the original source.

No coverage reference is discarded merely because it is contextual. No accepted/public v9/v4 behavior is modified.

## Regression evidence

`tests/test_analysis_v20_candidate.py` proves:

- every dense coverage reference is assigned exactly once;
- every partition is bounded by the configured size;
- the v19 oscillation shape can preserve the segment-13 subset and long contextual subset simultaneously;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- only exact duplicate identities are deduplicated;
- cross-partition requirement/duty/exclusion leakage is rejected;
- v20 keeps schema-v5 source-led requirement capacity.

## Deterministic verification

CI run 747 on implementation head passed:

```text
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

## Acceptance boundary

Public/accepted P1.6 remains `job-analysis-english-v9` / schema v4. Accepted dense artifact 29 and Capability v7 artifact 9 remain authoritative.

Next live gate is dense `tG9K` only:

```bash
git fetch origin
git switch agent/p16-v20-source-led-partitioning
git pull --ff-only origin agent/p16-v20-source-led-partitioning
python scripts/run_p16_v20_candidate.py --job-id tG9K
```

Do not run sparse `t4jp` until dense v20 persists and passes semantic review.

If dense v20 passes, then run sparse `t4jp` non-regression before any promotion or Capability rebuild.
