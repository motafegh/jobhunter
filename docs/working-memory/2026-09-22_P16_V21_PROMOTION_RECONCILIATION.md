# P1.6 v21 Promotion and Current-State Reconciliation

**Date:** 2026-09-22  
**Status:** PROMOTED / CURRENT — I7 REMAINS HOLD  
**Branch:** `main`

## Decision

English P1.6 `job-analysis-english-v21 / job-analysis-v5` is promoted as the public/current
generation and review contract.

The promotion changes prompt/runtime identity but intentionally keeps the v5 persisted schema.
V21 adds exact item-scoped candidate evidence beneath durable parent coverage so concept-specific
depth, obligation, experience type, compound candidate facts, and duty coverage can fail closed
without borrowing meaning from neighboring source text.

## Compatibility rule

The five already accepted public P1.6 anchors remain their exact v20/v5 artifacts. They are
accepted-only compatibility-current under v21 and are not regenerated merely to change contract
identity.

```text
new English generation            v21/v5
accepted existing v20 artifact    reusable/current-compatible
pending v20 candidate             NOT v21-current
rejected v20 candidate            NOT v21-current
artifact prompt/schema identity   always preserved and inspectable
```

This is a read-compatibility rule, not artifact relabeling. A reused v20 artifact remains v20 in
persistence and user-visible lineage.

## Promotion evidence

The promotion is based on the bounded evidence already recorded in
`2026-09-20_MARKET_I7_TVMM_BOUNDED_CLOSURE.md`:

- complete 27-projection exact-source/catalog/transport regression;
- read-only v21 validation of all 85 requirements in the five accepted P1.6 anchors;
- dedicated handling for exact item depth, shared preferred scope, headingless candidate
  experience, compound candidate facts, mixed knowledge/experience facts, candidate/product
  subject separation, and exact duty-list coverage;
- repeated retained-response replay that converted concrete failures into fail-closed regressions;
- final single non-persistent `tvMm` evaluation that passed complete manual source review with
  22 requirements and all 11 duties while leaving SQLite byte-identical.

That case-level evidence is not a claim of universal model reliability. The semantic-review gate
therefore remains mandatory.

## Repository promotion hardening

The initial local promotion switched the current runtime but left stale tests/docs. The follow-up
reconciliation added two required protections:

1. `AnalysisJobResult` carries the exact persisted prompt/schema identity, and CLI output
   distinguishes current-v21 routing from physical v20 compatibility reuse.
2. Regression tests prove that accepted v20 artifacts can satisfy v21 current reads while pending
   v20 candidates cannot.

Verification:

```text
promotion hardening head: dc7d856b51fd616ed8bdf00dfdc287e446567004
GitHub Actions run:       1294 / 35753325406
entrypoint smoke:         PASS
Ruff:                     PASS
pytest:                   690 passed
pytest -W error:          690 passed
```

## Market consequence

This promotion does **not** change I7 to PASS.

The remaining first-slice gate is operational evidence:

```text
normal current v21 generation for the selected core case
→ persist pending artifact
→ complete semantic review
→ accept only if genuinely valid
→ new immutable Market snapshot/profile
→ accepted-semantic requirement/responsibility aggregate + evidence drill-down
→ real CLI/browser verification
→ SQLite integrity/FK + publication/privacy checks
→ PASS only if all hold
```

Do not repeat the earlier non-persistent tuning evaluations, switch vacancy/model to manufacture
success, auto-accept v21 output, or regenerate accepted v20 anchors without a material reason.
