# PR4 — Historical/Versioned Source Disposition

**Status:** CLOSED / ACCEPTED — disposition audit complete; no source relocation/removal authorized  
**Date:** 2026-09-02  
**Track:** Portfolio readiness / repository quality  
**Product gate:** P2.2B-B1 remains unchanged and locally blocked on `ta9l` English P1.6 acceptance.

## Objective

Determine whether JobHunter's visible versioned semantic source families should remain, be isolated, archived, or removed before portfolio release.

PR4 was deliberately an evidence-first disposition audit. It did not authorize semantic changes or cosmetic mass cleanup.

## Evidence inspected

The audit followed current/public facades and representative transitive dependencies across:

- `src/jobhunter/analysis_current.py`;
- P1.6 runtime/service versions through the accepted v20 route;
- versioned Instructor/LM Studio helpers;
- `src/jobhunter/capability_service.py` and v9/v8/v6 implementation dependencies;
- `src/jobhunter/role_blueprint_service.py` and Blueprint v6 dependencies;
- the repository test inventory;
- version-specific audit scripts;
- package entrypoints in `pyproject.toml`;
- current governance/documentation constraints.

## Findings

### 1. P1.6 versioned files are layered, not a simple archive

Current `analysis_current.py` routes:

```text
English  → analysis_runtime_v20 / analysis_service_v20
Original → analysis_runtime / analysis_service (accepted v9/v4 path)
```

The English v20 path directly/transitively reuses earlier runtime, service, validator, evidence, persistence, and Instructor components. Confirmed dependencies include v19/v18/v17/v16/v15/v14/v12 runtime lineage plus older service/helper lineage.

Therefore many older-looking modules are current implementation substrate.

`analysis_runtime_v10.py`, `analysis_runtime_v11.py`, and `analysis_runtime_v13.py` were not found in the accepted v20 runtime import route inspected during PR4. They remain standalone candidate-era runtime wiring with retained historical tests/audit context. Their associated service/helper families are not uniformly dead, so no deletion is authorized.

### 2. Capability v9 deliberately reuses earlier Capability versions

Current route:

```text
capability_service.py
→ capability_service_v9.py
→ v8 staged orchestration/inference
→ reused v6 result/evidence helpers
```

Capability v8/v6 therefore cannot be classified as removable historical code.

Capability v7 is not the public-current Capability contract, but Blueprint v6 intentionally depends on Capability v7 semantics/identity. It also retains regression/audit value.

### 3. Blueprint history remains meaningful compatibility/research evidence

Current experimental route:

```text
role_blueprint_service.py
→ role_blueprint_service_v6.py
→ v6 inference/models
→ historical Capability v7 dependency semantics
```

Blueprint v3-v5 are not current product authority, but version-specific tests and snapshot-audit scripts preserve their experiment/failure history.

### 4. Tests and audit scripts materially affect disposition

The test suite contains explicit historical/current coverage for P1.6 versions, Capability v7/v8/v9, and Blueprint versions. `scripts/` retains version-specific P1.6, Capability, and Blueprint audit utilities.

This executable evidence is intentionally more useful than relying on Git history alone for semantic regression/reproducibility.

## Accepted dispositions

```text
KEEP IN PLACE — CURRENT / TRANSITIVE CURRENT
- current facades
- P1.6 English v20 + original v9 route
- older P1.6 components imported by accepted paths
- Capability v9 + v8/v6 implementation substrate
- current Work Intelligence / Registry code

KEEP IN PLACE — COMPATIBILITY / EXPERIMENTAL
- Blueprint v6
- Capability v7 dependency required by Blueprint v6 semantics

KEEP IN PLACE — HISTORICAL REGRESSION / REPRODUCIBILITY
- earlier standalone P1.6 candidate runtime wiring not in current v20 route
- older Blueprint experiment families
- historical Capability paths not otherwise current
- corresponding version-specific tests/audit support

ISOLATE / ARCHIVE
- deferred; no broad family qualifies yet

REMOVE AFTER PROOF
- none authorized by PR4
```

## Repository presentation decision

The portfolio problem is solved at this stage by making current boundaries explicit, not by moving code for aesthetics.

Created:

```text
docs/CURRENT_RUNTIME_AND_VERSIONED_CODE.md
```

and linked it from `docs/README.md`.

A technical reviewer can now identify the normal current facades and understand why older versioned modules remain.

## Removal/relocation gate

Any later move/removal must prove:

1. no current direct/transitive import;
2. no compatibility/artifact-inspection dependency;
3. no meaningful regression-test dependency;
4. no audit/replay dependency;
5. no persisted-contract inspection requirement;
6. concrete maintainability benefit;
7. complete import/test/script/doc/package validation in the same bounded change.

## PR4 non-actions

PR4 deliberately did not:

- change product behavior;
- change accepted semantic contracts;
- rebase Blueprint to Capability v9;
- flatten versioned implementations;
- move source files;
- delete tests/scripts;
- rewrite Git history.

## Next portfolio phase

Proceed to **PR5 — Current-code structure and readability**.

PR5 should focus only on current maintainability problems supported by responsibility/coupling evidence. It may reduce deep historical coupling when a stable version-neutral helper can be extracted safely, but it must not perform arbitrary splits or historical cleanup merely because a module is large or versioned.
