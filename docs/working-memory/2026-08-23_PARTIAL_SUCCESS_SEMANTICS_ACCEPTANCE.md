# Partial-Success Semantics Acceptance

Date: 2026-08-23

## Decision

Phase-1 gate P1-D / checklist C3 is accepted. This closes result truthfulness for the current bounded multi-stage workflows; it does not close P1.7 or Phase 1.

## Shared full-workflow contract

The CLI `jobhunter run` and browser complete workflow now both use:

```text
configured_searches
→ Phase1RunService
→ Phase1RunSummary
→ format_phase1_run_summary
```

The browser no longer owns a second discovery/translation/analysis selection or summary implementation.

The shared ledger exposes, where applicable:

```text
requested limits / selected work
attempted
completed
reused or unchanged
failed
skipped intentionally with reason
remaining eligible
```

English-projection eligibility is counted across the complete current parsed backlog independently from the bounded batch limit. Failed items remain in `remaining_eligible`; successful or reused items reduce it.

## Mixed and no-work behavior

- source/detail/translation/analysis successes remain durable if a later item or stage fails;
- mixed results return `completed_with_failures`, not simple `completed`;
- the browser public-corpus hook still runs after partial success so completed durable work is projected;
- Quick Add propagates discovery/detail/translation/analysis failures into its terminal result;
- an operator-not-requested downstream stage is an intentional skip;
- zero eligible translation/analysis work is a clean completed no-op, not an attempted failure;
- missing configured providers in the complete workflow remain attention-required skips because the requested end-to-end workflow is incomplete.

## Deterministic evidence

Focused tests cover:

- exact shared ledger counts and remaining-backlog behavior;
- translation-backlog counting independent from the batch limit;
- browser use of the shared Phase-1 service/formatter;
- propagation of `completed_with_failures`;
- clean no-eligible-work behavior;
- Quick Add translation and later-analysis failures;
- preservation of successful translation output when analysis fails;
- public-corpus projection after partial durable success.

The active next gate is P1.7 final report/run/browser acceptance.
