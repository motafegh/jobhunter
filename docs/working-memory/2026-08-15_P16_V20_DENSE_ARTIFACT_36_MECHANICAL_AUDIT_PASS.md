# P1.6 v20 — Dense Artifact 36 Mechanical Audit Pass

**Date:** 2026-08-15  
**Status:** mechanical audit passed; semantic acceptance pending  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Job:** `tG9K`  
**Artifact:** 36  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## Local audit result

The v20-specific snapshot exporter produced:

```text
review-snapshots/jobs/tG9K.json
```

The v20-specific mechanical audit then passed:

```text
Mechanical P1.6 v20 candidate checks: PASS
Snapshot: review-snapshots/jobs/tG9K.json
Job: tG9K
Artifact: 36
Requirements: 33
Responsibilities: 8
Role purpose statements: 0
Structured required skills covered: 6/6
Qualification-list items covered: 0/0
Residual coverage decisions: 0/0
Decomposed coarse coverage decisions: 0
Coverage decisions: 34
```

## What this proves

Artifact 36 is correctly bound to the v20 candidate/projection chain and passes the current deterministic snapshot checks, including structured-skill coverage and mechanical concept/depth/evidence hygiene.

This advances the dense gate from **mechanical persistence pending** to **mechanical snapshot audit PASS**.

It does **not** establish semantic acceptance.

## Immediate semantic review signal

Artifact 36 contains:

```text
responsibilities:       8
role_purpose statements: 0
```

The accepted v9 dense baseline contained 7 responsibilities and represented the high-level role-purpose surface separately. Therefore purpose-vs-duty classification is a mandatory semantic-review item. The count difference alone is not proof of a defect, but `role_purpose=0` makes it a concrete review risk.

## Current gate

Do not run sparse `t4jp` yet.

Artifact 36 must now be semantically reviewed against its exported source/projection snapshot and accepted v9 artifact 29 for:

- required `Master's degree`;
- `Professional experience` with exact `three to six years` depth;
- all six structured skills;
- role purpose versus concrete duties;
- no silent dense factual loss;
- accepted explicit-depth surfaces (`Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`);
- MATLAB/C++ preferred semantics with null technical depth unless independently supported;
- industrial/edge deployment as scope, not fabricated depth/experience;
- contextual technical-stack obligation;
- semiconductor-domain normalization;
- provenance-distinct structured Python versus prose `Python (expert)`;
- defensible concept-type choices.

## Promotion boundary

Public v9/v4 remains authoritative. Capability artifact 9 remains tied to P1.6 artifact 29. PR #8 remains draft/unmerged. Sparse `t4jp`, Capability rebuild, heterogeneous-role progression, and P1.6 promotion remain blocked until dense artifact 36 passes semantic review.
