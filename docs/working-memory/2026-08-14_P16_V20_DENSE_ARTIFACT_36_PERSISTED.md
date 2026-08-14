# P1.6 v20 — Dense Artifact 36 Persisted

**Date:** 2026-08-14  
**Status:** mechanical persistence PASS; semantic acceptance pending  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## Live result

The next dense `tG9K` v20 run completed successfully and persisted the first reviewable v20 dense artifact:

```text
Outcome: completed
English P1.6 v20 candidate for tG9K
Artifact: 36
Model: gemma-4-e4b-it-ud
Contract: job-analysis-english-v20 / job-analysis-v5
Responsibilities: 8
Requirements: 33
```

This is the first dense v20 run to pass the complete generation, partition, merge, deterministic materialization, inherited normalization, full source-led validation, and persistence path.

## What this proves

It proves the current v20 implementation can produce a mechanically valid dense artifact without the previous failure classes:

- fixed 32-requirement capacity ceiling;
- one-error-at-a-time dense coverage repair;
- model-owned structured education/minimum-experience formatting;
- optionality leaked into technical depth;
- unsupported depth vocabulary in normalized concepts;
- whole-answer retry oscillation;
- vague `some` preference extent treated as technical depth;
- `industrial / edge deployment` scope treated as technical depth.

It does **not** yet prove semantic acceptance. Counts alone are not sufficient.

## Current artifact

```text
source job:       tG9K
English projection artifact: 33
candidate P1.6 artifact:      36
prompt:                       job-analysis-english-v20
schema:                       job-analysis-v5
requirements:                 33
responsibilities:             8
```

Public/accepted truth remains unchanged until review passes:

```text
accepted P1.6:   job-analysis-english-v9 / job-analysis-v4
accepted tG9K P1.6 artifact: 29
Capability v7 artifact:      9 (derived from artifact 29)
```

## Review tooling

V20-specific snapshot export/audit entry points are being added so artifact 36 can be reviewed under its own prompt/schema identity rather than through an older candidate contract:

```bash
python scripts/export_p16_v20_candidate_snapshot.py --job-id tG9K
python scripts/audit_p16_v20_candidate_snapshot.py --job-id tG9K
```

The exported snapshot remains local review material and should not be committed.

## Dense semantic acceptance checklist

After mechanical snapshot audit, inspect artifact 36 against the source/projection and accepted v9 baseline for:

- required `Master's degree`;
- `Professional experience` with exact `three to six years` depth;
- all six structured skills;
- correct high-level role purpose versus concrete responsibilities;
- no silent dense factual loss;
- explicit depth attached to the correct concepts: `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`;
- MATLAB and C/C++ remain preferred with null technical depth unless independently supported;
- `industrial / edge deployment` retains scope without fabricated depth or experience;
- contextual technical-stack semantics remain contextual;
- semiconductor-domain concept contains no unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences are semantically defensible.

The responsibility count is 8 versus the accepted v9 baseline of 7, so role-purpose/duty classification requires explicit review rather than count-based acceptance.

## Decision boundary

Do **not** run sparse `t4jp` yet. Do not promote P1.6, rebuild Capability, advance heterogeneous-role review, or merge the candidate PR chain until artifact 36 passes mechanical snapshot audit and dense semantic review.

Only after dense PASS should sparse v20 non-regression run against `t4jp`.
