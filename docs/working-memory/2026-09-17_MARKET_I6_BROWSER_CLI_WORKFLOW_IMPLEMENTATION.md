# Market I6 — Browser + CLI Thin Workflow

**Date:** 2026-09-17  
**Status:** ACCEPTED / CLOSED FOR I6  
**Branch:** `main`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

## 1. Decision

```text
MARKET I6: ACCEPTED / CLOSED
NEXT: I7 — BOUNDED REAL LOCAL ACCEPTANCE
```

I6 exposes the accepted I1-I5 Market responsibilities through one shared local workflow. Browser and CLI are adapters over the same Market state/services; neither owns separate business logic or persistence.

I7 remains required before the first Market vertical slice itself may be called accepted end-to-end.

## 2. Implemented surface

Shared service/coordinator:

```text
src/jobhunter/market_workspace.py
```

CLI:

```text
src/jobhunter/market_cli.py
src/jobhunter/app_entrypoint.py
```

Browser:

```text
src/jobhunter/web/market_workspace.py
src/jobhunter/web/launcher.py
src/jobhunter/web/templates/market_workspace.html
src/jobhunter/web/templates/market_run.html
src/jobhunter/web/templates/market_snapshot.html
src/jobhunter/web/templates/base.html
```

Focused tests:

```text
tests/test_market_workspace.py
tests/test_market_cli.py
tests/test_market_web.py
```

## 3. Shared target-scoped workflow

The bounded coordinator composes the existing accepted owners:

```text
immutable target definition
→ target-only search resolution
→ bounded Jobinja discovery
→ I2 source affected-work planning
→ bounded missing/refresh execution
→ I2 replan
→ bounded English projection work
→ I2 replan
→ bounded P1.6 generation work
→ I2 final source/currentness plan
→ bounded I3 membership qualification
→ terminal MarketResearchRun + partial-success ledger
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
```

It does not add another acquisition engine, currentness system, classifier, snapshot contract, aggregate contract, persistence system, semantic report layer, or publication path.

## 4. Important I6 integrity decisions

### Immutable acquisition meaning

Target search profiles/packs/terms/raw searches come from the exact immutable `TargetMarketDefinitionVersion`.

The definition's `search_catalog_version` must match the currently configured catalog before execution. A catalog meaning change therefore requires a new target-definition version instead of silently changing a historical target.

### Target-only work

The coordinator continues to use I2 target-only affected-work selection. Remaining source/translation/P1.6 work cannot fall through to unrelated global backlog.

### Membership budget

The initial unfinished I6 coordinator would have qualified every source-ready candidate and could therefore issue an unbounded number of membership-model calls.

I6 acceptance added an explicit `membership_limit` (0-50) alongside source/translation/P1.6 budgets. The run ledger records:

```text
eligible
selected
remaining
succeeded
failed
dispositions
```

This is a deliberate first-slice batch boundary. I7 must exercise a representative target within explicit bounded controls and inspect remaining work where applicable.

### Partial success

Per-stage failures are recorded without erasing earlier durable success. Membership failure is allowed to produce a `completed_with_failures` run while successful membership decisions remain available for the frozen snapshot.

### Read-only preview

Target/scope preview is deliberately lightweight. Rendering or inspecting a target definition resolves only its immutable search envelope and does not construct the complete model/provider runtime.

Candidate-specific affected-work preview constructs the I2 planner only when candidate IDs are explicitly supplied.

### Accepted I5 remains frozen

During I6 integration an attempted convenience factory accidentally changed accepted I5 aggregate semantics. Repository tests caught the regression before acceptance.

The exact accepted I5 aggregate implementation was restored, and I6 now composes `MarketAggregateService` directly without modifying its deterministic contract.

This recovery is part of the I6 acceptance evidence: no I5 requirement-strength, employer, source-context, denominator, or historical-reproducibility semantics were intentionally changed by I6.

## 5. CLI workflow

The normal `jobhunter` entrypoint now routes:

```text
jobhunter market target list
jobhunter market target create
jobhunter market definition create TARGET_ID
jobhunter market show
jobhunter market preview DEFINITION_ID
jobhunter market run DEFINITION_ID
jobhunter market run-show RUN_ID
jobhunter market snapshot-show SNAPSHOT_ID
```

`market run` accepts explicit search/detail/refresh/translation/P1.6/membership budgets.

Only `market run` participates in the existing public-corpus synchronization wrapper because it may create upstream repository-safe English/P1.6 artifacts. Market target/definition/membership/run/snapshot/profile tables remain local/private and are not added to public-corpus export.

## 6. Browser workflow

Primary Market navigation now enters:

```text
/market/targets
```

The pre-existing `/market` page remains available as a legacy current-corpus aggregate view; it is not deleted or redefined as the target-scoped authority.

Browser workflow supports:

```text
select/create TargetMarket
→ create immutable target-definition version
→ inspect exact acquisition envelope
→ submit bounded Market run through existing WebOperationManager
→ inspect persisted run controls + partial-success ledger
→ inspect membership history
→ inspect immutable snapshot
→ inspect source vs accepted-semantic denominators
→ inspect deterministic requirements/responsibilities/warnings
→ drill down to exact source job evidence
```

All mutable browser actions use the existing single-mutable-operation manager and CSRF boundary.

## 7. Deterministic acceptance coverage

Focused I6 tests prove at minimum:

1. membership work stops at the explicit budget and records remaining eligible candidates;
2. one membership failure preserves successful decisions and partial-success state;
3. invalid/unbounded membership controls are rejected;
4. search-catalog drift cannot silently change an immutable target definition;
5. CLI target/definition creation and inspection operate over the same persisted Market state;
6. top-level `jobhunter market ...` routing does not fall through to a separate legacy path;
7. only Market run triggers existing upstream public-corpus synchronization;
8. browser runtime registers the target/run/snapshot routes;
9. browser target view renders state created through the shared workspace service;
10. unknown run/snapshot history returns 404 instead of fabricated state;
11. read-only target rendering does not require the complete executable provider runtime;
12. all pre-existing I1-I5 regression suites remain green.

Ordinary CI uses deterministic fixtures/fake providers and does not require Jobinja network access or LM Studio.

## 8. Final technical evidence

Accepted technical head before status-document reconciliation:

```text
4076bb731b3485aa99fbdf63bf73a96dc7a5773b
```

GitHub Actions:

```text
run:       1210
run id:    35263630011
conclusion SUCCESS
```

Quality gate:

```text
package install                  PASS
pip dependency consistency       PASS
installed public entrypoints     PASS
Ruff                             PASS
pytest                           632 passed
pytest -W error                  632 passed
```

## 9. What I6 does not claim

I6 does **not** prove yet that:

- current real Jobinja target acquisition has acceptable recall/noise;
- the configured local translation/P1.6/membership models work reliably through the full target run;
- a real unchanged rerun demonstrates the expected reuse behavior end-to-end;
- the browser workflow is useful and legible on the owner's actual runtime/data;
- one real target's membership/semantic denominators are product-useful;
- acquisition/model failures are displayed acceptably in the real local workflow;
- the complete first Market vertical slice is accepted.

Those are I7 responsibilities.

## 10. Exact next action

```text
I7 only
→ one small representative real local target
→ bounded search/acquisition/model budgets
→ inspect discovery/noise and target scope
→ inspect source/translation/P1.6/membership reuse
→ inspect core/adjacent/uncertain/excluded decisions
→ inspect source vs accepted-semantic denominators
→ inspect exact evidence drill-down
→ inspect partial-success behavior where naturally encountered or safely injected
→ repeat unchanged run to verify reuse/currentness
→ privacy/publication check
→ close or repair the first Market vertical slice from real evidence
```
