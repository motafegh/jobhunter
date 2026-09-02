# PR5 — Current-code structure and web-boundary closure

**Status:** CLOSED / ACCEPTED  
**Date:** 2026-09-02  
**Track:** Portfolio readiness / current-code structure and readability  
**Product-development authority:** unchanged; P2.2B-B1 remains blocked on the machine-local `ta9l` P1.6 gate.

## Scope

PR5 evaluated current runtime structure for maintainability and reviewer readability without treating file size, historical versioning, or portfolio aesthetics as automatic refactor authority.

The bounded review covered the current browser composition/route layer, CLI entrypoints, Work Intelligence service boundary, and Canonical Registry persistence/domain boundary.

## Accepted decisions

### KEEP — current architectural boundaries

Keep without structural refactor in this increment:

- the Python modular-monolith architecture;
- `src/jobhunter/web/launcher.py` as the local-app launch/composition boundary;
- `src/jobhunter/app_entrypoint.py` as the public-corpus synchronization wrapper around the established CLI;
- `src/jobhunter/entrypoint.py` as the current parser/command-dispatch boundary;
- Work Intelligence's existing service / inference / models / store separation;
- the Canonical Registry's persistence/domain contract and SQLite constraints;
- independently registered feature route modules for Capability, Blueprint, Registry, and Work Intelligence.

The CLI and Registry files are not to be split merely because they are comparatively large. Their inspected responsibilities remain coherent enough that a structural rewrite would add churn without a demonstrated maintenance benefit.

## Implemented refactor — shared feature-route web primitives

The concrete duplication found across independently registered feature route modules was small but important: each module independently implemented parts of the same browser trust/navigation boundary.

Added:

```text
src/jobhunter/web/common.py
```

It now owns the shared primitives used by the feature route modules:

- constant-time local CSRF validation;
- common Jinja template construction;
- common template context (`request`, `page`, CSRF token, active operation);
- URL-encoded local notice redirects;
- validated local return paths for operation redirects.

Migrated to this shared boundary:

```text
src/jobhunter/web/capability.py
src/jobhunter/web/blueprint.py
src/jobhunter/web/work_intelligence.py
src/jobhunter/web/registry.py
```

Added focused regression coverage:

```text
tests/test_web_common.py
```

The tests cover shared context, accepted/rejected CSRF tokens, encoded notices with existing query strings, encoded operation return paths, and rejection of external/protocol-relative redirect targets.

## Explicit non-change

No accepted semantic contract, persisted artifact shape, registry rule, Work Intelligence rule, route URL, source-policy rule, publication boundary, or local database authority changed in PR5.

Work Intelligence deliberately remains outside `WebOperationManager` for its persistence action because successful operation-manager mutations refresh the public corpus and publication of Work Intelligence has not been authorized.

## `web/app.py` decision

`src/jobhunter/web/app.py` is a real future refactor candidate. It currently combines:

- base acquisition/translation/analysis service construction;
- source-sync and complete-processing orchestration;
- validation and operation helpers;
- base HTML/JSON routes;
- multiple mutation handlers.

However PR5 does **not** authorize a wholesale split merely because the file is about 45 KB.

A later extraction should occur only when one or more concrete triggers exist, for example:

1. a new feature needs to reuse one of the base workflow/service-construction responsibilities;
2. repeated edits create merge/conflict or testing friction;
3. a responsibility can move behind a stable interface with clearly bounded tests;
4. route growth makes one coherent route family independently maintainable;
5. an implementation task already touching the relevant code can perform the extraction with low additional risk.

When that happens, prefer responsibility-based modules over arbitrary line-count slicing.

Two small cleanup candidates observed during this audit are `_successful_detail_ids` and `_translation_output`; no current references were found during the bounded repository search. They may be removed later when `web/app.py` is already being changed and normal tests can prove the cleanup safely. They are not a reason to reopen the file now.

## Validation

Cumulative implementation/test commit:

```text
9d7242ef324c70f671417cceef3bb7603cfc1fca
```

GitHub Actions CI run `1071` completed successfully on 2026-09-02, including:

```text
Ruff
pytest
pytest -W error
```

Earlier intermediate runs were superseded/cancelled by the repository's CI concurrency policy as newer commits arrived; the final cumulative run is the validation authority for this increment.

## PR5 closure decision

```text
KEEP coherent current boundaries
→ REFACTOR duplicated feature-route trust/navigation primitives
→ TEST the shared boundary directly
→ DEFER broad web/app.py extraction until evidence supplies a real trigger
→ DO NOT perform readability churn for portfolio appearance alone
```

PR5 is closed. The next portfolio-readiness phase is PR6: reproducible demo / public-corpus experience.
