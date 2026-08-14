# P1.6 v20 — Promotion Routing Design

**Date:** 2026-08-15  
**Status:** design checkpoint; promotion implementation not yet applied  
**Working branch:** `main`  
**Base:** accepted/calibrated P1.6 v20 work now merged into `main`

## 1. Why promotion needs routing work

Dense `tG9K` artifact 36 and sparse `t4jp` artifact 37 have passed the bounded v20 calibration gates. That authorizes promotion work, but the current public runtime still points to the historical v9 service.

Promotion cannot be a one-line alias because the current module graph has two important constraints:

1. v20 modules import shared types/helpers from `analysis_service.py`, which is the historical v9 implementation;
2. public CLI, Phase-1 orchestration, browser, Review Snapshot and Capability dependency selection import current contract/service objects from that same v9 module.

Making `analysis_service.py` simply import v20 would create circular-import risk and would also incorrectly replace the still-valid original-language v9 path.

## 2. Contract split required after promotion

After English promotion, public P1.6 is intentionally asymmetric:

```text
English P1.6:
  prompt: job-analysis-english-v20
  schema: job-analysis-v5

Original-language P1.6:
  prompt: job-analysis-original-v9
  schema: job-analysis-v4
```

Therefore the current single `ANALYSIS_SCHEMA_VERSION` assumption cannot be used for both modes at public routing boundaries. Public routing needs explicit English and original schema constants.

## 3. Recommended architecture

Keep historical/candidate modules immutable in meaning:

```text
analysis_service.py          historical v9 implementation + shared helpers
analysis_service_v10..v20    historical/candidate evolution
analysis_runtime.py          historical v9 runtime helper
analysis_runtime_v20.py      accepted v20 English runtime implementation
```

Add a small neutral public-current facade, for example:

```text
analysis_current.py
```

Responsibilities:

- expose current English prompt/schema = v20/v5;
- expose current original prompt/schema = v9/v4;
- delegate English per-job analysis to `JobAnalysisServiceV20` / v20 runtime;
- delegate original-language analysis to the existing v9 service/runtime;
- provide a bounded English batch `run()`/`run_english()` surface compatible with the existing Phase-1 orchestrator;
- provide `run_original()` through v9;
- reuse the established `AnalysisJobResult`, `AnalysisFailure`, `AnalysisBatchSummary`, and formatting types without changing their historical semantics.

This avoids circular imports and preserves reproducibility of old candidate modules/artifacts.

## 4. Public consumers that must move together

### Targeted CLI

`src/jobhunter/entrypoint.py`

Current behavior imports `build_job_analysis_service` from v9 runtime and one shared schema constant. Promotion must route:

- `jobs analyze <id> --mode english` → v20/v5;
- `jobs analyze <id> --mode original` → v9/v4;
- displayed contract must use the mode-specific schema.

### Complete Phase-1 runner

`src/jobhunter/phase1_run.py`

Current code directly instantiates v9 `JobAnalysisService`, uses v9 prompt/schema for eligibility, and gives those identities to Market.

Promotion must make the batch English stage use v20/v5. Otherwise targeted CLI could be v20 while `jobhunter run` silently remained v9.

### Browser

`src/jobhunter/web/app.py`

Current browser wiring directly constructs v9 `JobAnalysisService` and uses v9 prompt/schema for Market/current-analysis queries. It must use the same public-current English route as CLI/batch.

### Review Snapshot

`src/jobhunter/review_snapshot.py`

Current snapshot lookup uses one shared P1.6 schema for both English and original. Promotion must query:

```text
English:  job-analysis-english-v20 / job-analysis-v5
Original: job-analysis-original-v9 / job-analysis-v4
```

Capability/Blueprint current-chain flags must continue to depend on exact artifact IDs.

### Capability dependency selection

`src/jobhunter/capability_service_v6.py` (inherited by v7)

Current `_current_dependencies()` selects English P1.6 using public prompt/schema constants. After promotion it must select v20/v5.

The Capability model currently receives `accepted_extraction` including free-form requirement rationale. Preserve the permanent authority boundary: normalized P1.6 concept/type/strength/depth/evidence are authoritative; model-generated rationale prose must not override them.

## 5. Required regression tests

Promotion tests should prove at minimum:

1. public English constants are v20/v5;
2. public original constants remain v9/v4;
3. targeted English analysis delegates to v20;
4. targeted original analysis delegates to v9;
5. public English batch `run()` uses v20 and retains partial-failure summary behavior;
6. Phase-1 eligibility/current-artifact lookup uses v20/v5;
7. Market current-analysis scope uses v20/v5;
8. browser analysis service/current queries use v20/v5;
9. Review Snapshot selects v20/v5 English and v9/v4 original independently;
10. Capability v7 dependency selection requires current v20/v5 English analysis;
11. historical v9/v10...v20 modules still import without circular dependency;
12. accepted artifact 36 and 37 identities remain reusable/current under promoted English routing.

## 6. Promotion gate

Promotion is complete only after implementation plus:

```text
Ruff PASS
full pytest PASS
pytest warnings-as-errors PASS
public English routing verified as v20/v5
public original routing verified as v9/v4
CLI / batch / browser / snapshot / Capability dependency selection aligned
historical artifact/module reproducibility preserved
```

Until then:

- public English P1.6 remains v9/v4;
- Capability artifact 9 remains tied to analysis artifact 29;
- do not rebuild Capability over v20 as if promotion already happened;
- do not begin corpus-wide Phase 2.

## 7. Repository workflow rule

From this checkpoint forward, JobHunter development proceeds directly on `main` unless the user explicitly changes that rule. Do not create a new working branch by default.
