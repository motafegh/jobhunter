# P1.6 v20 — Public Routing Implemented / Deterministic CI PASS

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** public routing implementation complete; local artifact-reuse verification pending

## Decision state

The bounded v20 calibration had already passed on dense `tG9K` artifact 36 and sparse `t4jp` artifact 37. This checkpoint records the next gate: the public-current P1.6 routing has now been implemented directly on `main` and passed the complete deterministic CI suite.

The public-current contract is intentionally mode-specific:

```text
English P1.6:
  prompt: job-analysis-english-v20
  schema: job-analysis-v5

Original-language P1.6:
  prompt: job-analysis-original-v9
  schema: job-analysis-v4
```

Historical versioned implementation modules retain their original meaning and remain reproducible.

## Implemented routing

A neutral `src/jobhunter/analysis_current.py` facade now owns the current public P1.6 boundary.

It delegates:

```text
English analysis  → JobAnalysisServiceV20 / v20 runtime
Original analysis → historical v9 service/runtime
```

It also provides bounded English/original batch execution with the existing partial-failure summary semantics.

The following public consumers now resolve through the promoted mode-specific contract:

- targeted `jobhunter jobs analyze` CLI;
- complete `jobhunter run` Phase-1 analysis eligibility and batch execution;
- Market current-analysis scope used by the complete runner;
- local browser analysis generation;
- browser dashboard/list/system current-analysis status;
- browser Market scope;
- Review Snapshot current analysis lookup;
- Capability v7 current P1.6 dependency selection.

Review Snapshot now queries English v20/v5 and original v9/v4 independently rather than assuming one schema for both modes.

Capability v7 remains the accepted capability contract, but its public-current service now requires a current English P1.6 v20/v5 dependency. Historical Capability implementation modules are unchanged.

## Historical safety

Promotion did not mutate the meaning of `analysis_service.py` or historical `analysis_service_v*` modules. This avoids a circular dependency because v20 intentionally reuses shared historical types/helpers.

The promotion also does not rewrite old persisted artifacts. Contract identity continues to determine which artifact is current.

## Regression adjustments

Several tests intentionally seeded the previous public v9/v4 contract. After current routing moved to v20/v5, those fixtures correctly stopped counting as current and were updated to seed the promoted contract instead. Historical-version tests remain unchanged.

The final browser corpus-health fixture was likewise updated so its test artifact uses the same current contract that `WebRepository` now queries.

## Deterministic verification

Final promotion-routing head:

```text
7bd77fd66ba5c12a738dad4d9333ac4eeb3c48d6
```

GitHub Actions CI run **801**:

```text
Ruff                         PASS
full pytest                  PASS
pytest warnings-as-errors    PASS
workflow conclusion          success
```

This closes the code-level promotion-routing gate.

## Remaining live verification

The assistant cannot access the user's local SQLite database or LM Studio runtime. Before declaring the operational promotion fully closed, verify locally that the already-accepted v20 artifacts remain current/reusable through the new public route:

```text
tG9K → expected English artifact 36 reuse/current
 t4jp → expected English artifact 37 reuse/current
```

Also export normal public Review Snapshots and confirm they select those v20/v5 artifacts.

No Capability regeneration should occur before this reuse/current check passes.

## Next boundary

If local reuse/current verification passes:

```text
P1.6 v20 public promotion COMPLETE
→ rebuild/review Capability v7 against promoted P1.6 artifact 36
→ continue heterogeneous Python/software, network/security, and operations/platform live review
```

If either artifact is not reused/current, stop and diagnose contract/dependency identity before generating replacement artifacts.

Phase 2 remains gated.
