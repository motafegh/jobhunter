# Current Runtime and Versioned Semantic Code

**Status:** Current / supporting engineering reference  
**Date:** 2026-09-02  
**Scope:** Runtime/versioned semantic-source orientation and PR4 disposition  
**Authority:** Subordinate to `AGENTS.md`, product/domain/source/architecture documents, and current accepted contracts.

JobHunter intentionally retains several versioned semantic implementations. A version suffix does **not** mean the module is dead code: later accepted contracts reuse earlier validators, models, providers, persistence helpers, and compatibility boundaries.

This document makes the current paths obvious without pretending that historical-looking files are safe to move or delete.

## 1. Read the neutral/current boundaries first

For normal development, start from these entrypoints rather than choosing the highest version number manually:

| Concern | Normal boundary | Current disposition |
| --- | --- | --- |
| P1.6 factual analysis | `src/jobhunter/analysis_current.py` | public-current facade |
| Capability Intelligence | `src/jobhunter/capability_service.py` | public-current facade |
| Role Capability Blueprint | `src/jobhunter/role_blueprint_service.py` | current experimental inspection facade; non-authoritative |
| Work Intelligence | `src/jobhunter/work_intelligence_service.py` | accepted/current v2 implementation |
| Canonical Registry | `src/jobhunter/canonical_registry.py` | accepted/current registry implementation |

Do not route new product code directly to an older versioned semantic module unless the current facade or an explicit compatibility/reproduction task requires it.

## 2. P1.6 current routing

Accepted contracts:

```text
English P1.6:          job-analysis-english-v20 / job-analysis-v5
Original-language:    job-analysis-original-v9 / job-analysis-v4
```

`analysis_current.py` owns this mode-specific public boundary:

```text
analysis_current.py
├── English  → analysis_runtime_v20 / analysis_service_v20
└── Original → analysis_runtime / analysis_service (accepted v9/v4 path)
```

The accepted English v20 path is layered. The PR4 dependency audit confirmed that v20 directly or transitively reuses earlier implementation pieces, including:

```text
analysis_runtime_v20
→ runtime helpers/providers from v19, v18, v17, v16, v15, v14, v12 and base runtime
→ service validators/helpers from v19, v17, v15, v14, v13, v11/v10 lineage and base service
→ versioned Instructor response/runtime helpers from v20, v19, v17, v14, v13
→ shared evidence, translation, LM Studio runtime and persistence services
```

Examples of current reuse include:

- v20 imports the v19 provider, v18 deterministic structured-fact logic, v15 concept normalization, and v14 context configuration;
- v19 reuses the v18 provider and v13 Instructor helper;
- v18 reuses v17;
- v17 reuses v16;
- v16 reuses v15;
- v15 reuses v14;
- v14 reuses v12 evidence-view logic and v13/v14 service helpers;
- v12 reuses v11 qualification-list logic;
- v11 service builds on v10 service behavior;
- v20 service reuses earlier persistence/evidence/schema helpers rather than duplicating them.

Therefore the earlier files participating in that chain are **current implementation substrate**, even when their own historical prompt identity is no longer the public contract.

### Standalone historical candidate runtimes

The audit did not find `analysis_runtime_v10.py`, `analysis_runtime_v11.py`, or `analysis_runtime_v13.py` in the accepted v20 runtime import chain. They remain isolated candidate-era runtime wiring and are paired with retained version-specific tests/audit history.

That does **not** authorize deletion:

- their associated service/helper lineage is partly reused by newer contracts;
- version-specific tests and audit scripts retain semantic regression/reproducibility value;
- deleting or moving them would require a separate proof that no replay, compatibility, test, script, or historical inspection path depends on them.

Current PR4 disposition: **keep in place as historical/reproducibility candidates; consider later physical isolation only after dependency removal/proof.**

## 3. Capability Intelligence current routing

Accepted public contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Normal routing:

```text
capability_service.py
→ capability_service_v9.py
→ staged v8 orchestration/inference + reused v6 result/evidence helpers
→ v7/v8/v9 model/reconciliation components where explicitly imported
```

Important consequence: Capability v8 and v6 files are not simply removable historical candidates. The accepted v9 service currently builds on them.

Capability v7 has a different mixed role:

- it is **not** the public-current Capability contract;
- its tests/audits remain historical regression evidence;
- the experimental Blueprint v6 is intentionally pinned to Capability v7 contract identity/semantics.

Current PR4 disposition:

| Family | Disposition | Reason |
| --- | --- | --- |
| Capability v9 | KEEP IN PLACE — CURRENT | accepted public path |
| Capability v8 substrate | KEEP IN PLACE — TRANSITIVE CURRENT | v9 orchestration/inference dependency |
| Capability v6 helpers | KEEP IN PLACE — TRANSITIVE CURRENT | reused result/evidence/service support |
| Capability v7 | KEEP IN PLACE — COMPATIBILITY/HISTORY | Blueprint v6 dependency + regression/audit evidence |
| older generic Capability support | KEEP pending later targeted audit | shared models/inference/tests; no benefit from cosmetic movement |

## 4. Blueprint routing

Blueprint is implemented and inspectable but remains experimental/non-authoritative.

Current inspection route:

```text
role_blueprint_service.py
→ role_blueprint_service_v6.py
→ role_blueprint_inference_v6.py + role_blueprint_v6_models.py
→ historical Capability v7 dependency semantics
```

The v6 service deliberately does not silently rebase onto current Capability v9. That historical dependency is part of the meaning of existing Blueprint artifacts and review evidence.

Older Blueprint v3/v4/v5 implementation/model/inference families are not current product authority, but their version-specific tests and snapshot-audit scripts preserve the experiment sequence and failure evidence.

Current PR4 disposition:

```text
Blueprint v6      KEEP IN PLACE — CURRENT EXPERIMENTAL/COMPATIBILITY PATH
Blueprint v3-v5   KEEP IN PLACE — HISTORICAL REGRESSION/REPRODUCIBILITY
```

Do not treat Blueprint version history as a current architectural recommendation.

## 5. Tests, scripts, and historical evidence are part of the disposition decision

The repository deliberately contains version-specific regression tests for P1.6, Capability, and Blueprint, together with audit utilities such as historical P1.6 candidate-snapshot and Blueprint/Capability snapshot checks.

These files provide more than Git history alone:

- executable regression expectations;
- preserved contract identities;
- evidence of why a later boundary exists;
- reproducible inspection of historical artifacts/snapshots;
- protection against accidentally changing accepted compatibility behavior.

A historical implementation is therefore not considered removable merely because normal CLI/browser code does not call it directly.

## 6. PR4 disposition matrix

Use these categories when reading `src/jobhunter/`:

### KEEP IN PLACE — CURRENT / TRANSITIVE CURRENT

Includes:

- current neutral/public facades;
- accepted P1.6 v20 and original v9 routing;
- earlier P1.6 runtime/service/inference components imported by the accepted path;
- Capability v9 and its v8/v6 implementation substrate;
- Work Intelligence and Canonical Registry current modules.

These are normal runtime code, regardless of version suffix.

### KEEP IN PLACE — COMPATIBILITY / EXPERIMENTAL

Includes currently inspectable behavior whose dependency identity is intentionally historical, notably Blueprint v6 → Capability v7.

These are not public authoritative product layers, but moving them would currently create compatibility/reproducibility churn.

### KEEP IN PLACE — HISTORICAL REGRESSION / REPRODUCIBILITY

Includes version-specific candidate implementations that are no longer the normal accepted route but remain covered by tests, audit scripts, experiment records, or historical artifact semantics.

Examples include standalone earlier P1.6 candidate runtime wiring and older Blueprint/Capability experiment families.

### ISOLATE / ARCHIVE — DEFERRED

No broad family is authorized for physical relocation by PR4.

A later PR5 or dedicated cleanup may isolate a proven historical-only cluster only when the move materially improves maintainability and the complete import/test/script/doc/replay impact is handled in the same bounded change.

### REMOVE AFTER PROOF — NONE AUTHORIZED

PR4 found no broad versioned family for which deletion value clearly exceeds reproducibility and migration risk.

## 7. Removal or relocation gate

Before moving or deleting any versioned semantic module, prove all of the following:

1. **No current import dependency** from public facades, current services, web, CLI, report/corpus/review code, or transitive current modules.
2. **No compatibility dependency** required to inspect or preserve an intentionally historical artifact contract.
3. **No meaningful regression dependency** from tests.
4. **No audit/replay dependency** from `scripts/`, review snapshots, experiment tooling, or accepted historical workflows.
5. **No persisted-contract assumption** that requires the old identity/shape to remain inspectable.
6. The proposed replacement/isolation has a concrete maintainability benefit, not merely a tidier directory listing.
7. Imports, documentation references, tests, scripts, packaging and CI are updated and validated together.

Git history alone is not a substitute for executable compatibility/regression evidence when the repository still uses that evidence intentionally.

## 8. What PR4 deliberately does not change

PR4 does not:

- alter semantic contracts;
- rebase Blueprint onto Capability v9;
- flatten historical implementations into v20/v9 files;
- rename version identities;
- move source modules merely for portfolio appearance;
- delete historical tests or audit scripts;
- change SQLite/persisted artifact meaning.

The professional repository improvement is **making the current boundaries and historical roles explicit**, while preserving the engineering evidence that explains how the accepted contracts evolved.

## 9. Guidance for PR5

PR5 may improve current-code readability without confusing version history. Prefer:

- clearer current facades and service-construction boundaries;
- reducing unnecessary coupling where a current contract reaches deeply into an older implementation;
- extracting genuinely shared, version-neutral helpers when behavior is already stable and tests prove equivalence;
- isolating historical-only runtime adapters only after current imports have been removed;
- preserving version-specific contract logic when extraction would erase meaningful historical behavior.

The goal is not to make every filename unversioned. The goal is to make **current responsibility, dependency direction, and maintenance ownership obvious**.
