# P1.6 v20 Public Promotion Acceptance

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** ACCEPTED / PUBLIC-CURRENT

## Decision

English P1.6 v20 is now the public-current JobHunter extraction contract:

```text
English P1.6:  job-analysis-english-v20 / job-analysis-v5
Original P1.6: job-analysis-original-v9 / job-analysis-v4
```

The original-language path remains on its independently validated v9/v4 contract. Historical P1.6 modules and artifacts remain available for reproducibility.

## Evidence already satisfied before promotion

Dense calibration (`tG9K`, artifact 36):

- persistence PASS;
- mechanical audit PASS;
- semantic review PASS WITH ACCEPTABLE DIFFERENCE;
- 33 requirements;
- 8 responsibilities;
- 0 role-purpose statements;
- all accepted dense v9 facts preserved plus six structured skills.

Sparse calibration (`t4jp`, artifact 37):

- persistence PASS;
- mechanical audit PASS;
- semantic non-regression PASS;
- 8 requirements;
- 0 responsibilities;
- 0 role-purpose statements;
- structured skills 3/3;
- qualification-list items 4/4;
- residual decisions 4/4.

## Promotion implementation

The public-current routing now aligns all live English P1.6 consumers on v20/v5 while preserving original-language v9/v4:

- targeted `jobhunter jobs analyze`;
- complete Phase-1 batch runner;
- browser generation and current-analysis status;
- Market current-analysis scope;
- Review Snapshot;
- Capability v7 dependency selection.

The neutral public boundary is `src/jobhunter/analysis_current.py`. Historical `analysis_service.py` and versioned candidate/accepted modules remain versioned rather than being rewritten into aliases.

## Deterministic verification

Promotion implementation passed the complete CI gate on `main`:

```text
Ruff               PASS
full pytest         PASS
warnings-as-errors PASS
```

The reconciled promotion head also passed CI after documentation updates.

## Local current-chain proof

The normal public Review Snapshot route resolved the accepted artifacts as current:

```text
tG9K
  Artifact: 36
  Prompt: job-analysis-english-v20
  Schema: job-analysis-v5
  Translation matches: True

t4jp
  Artifact: 37
  Prompt: job-analysis-english-v20
  Schema: job-analysis-v5
  Translation matches: True
```

The normal public analysis command then reused both artifacts without model regeneration:

```text
tG9K
Outcome: reused
Artifact: 36
Contract: job-analysis-english-v20 / job-analysis-v5
Responsibilities: 8
Requirements: 33

t4jp
Outcome: reused
Artifact: 37
Contract: job-analysis-english-v20 / job-analysis-v5
Responsibilities: 0
Requirements: 8
```

This closes the P1.6 v20 promotion gate.

## Downstream consequence

Existing Capability/Blueprint artifacts built from older P1.6 dependencies may still physically exist, but they are not current-chain artifacts. This is correct dependency behavior.

Before rebuilding Capability v7, the public-current Capability boundary is being tightened so model reasoning cannot treat P1.6 free-form `rationale` prose as authoritative source truth. Normalized P1.6 concept/type/strength/depth/evidence and provenance remain authoritative; persisted P1.6 artifacts remain unchanged.

## Next gate

```text
promoted P1.6 artifact 36
→ rebuild Capability v7 against artifact 36
→ mechanical/current-chain review
→ semantic review
→ then continue heterogeneous role calibration
```

Do not resume Blueprint tuning or Phase 2 during this gate.
