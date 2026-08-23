# P1.7 Report, Run, and Browser Acceptance Plan

**Status:** Accepted / closed
**Date:** 2026-08-23
**Scope:** P1.7 only; Phase 2 remains blocked
**Authority:** Subordinate to product/domain/source/architecture, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`

## 1. Objective

Close the final Phase-1 operational surface without adding a new authority layer:

```text
current SQLite/source/derived state
→ one deterministic current-corpus report
→ inspectable ready/review queues and per-job lineage
→ bounded shared CLI/browser run
→ rerun/idempotency and bounded live acceptance
```

The report is a read model. It does not replace SQLite, `corpus/`, Review Snapshot, Market, or any semantic artifact.

## 2. Required vertical slice

### P1.7A — Shared current-corpus report

Provide one neutral service consumed by CLI and browser. It must expose:

- discovered, parsed, current English, pending/accepted P1.6, and current Capability counts;
- exact current parser/translation/P1.6/Capability contract identities;
- jobs truly ready for English P1.6;
- P1.6 candidates awaiting semantic review;
- accepted P1.6 jobs ready for current Capability;
- per-job current source/translation/P1.6/Capability artifact lineage;
- current Market scope and warnings;
- explicit distinction between coverage, review state, and semantic acceptance.

Queue selection must use the same current dependency and `not_relevant` rules as execution. A pending P1.6 candidate is review work, not analysis-ready work.

### P1.7B — Operation result links

Browser operations should carry structured local links to affected jobs and relevant report/Market screens. Links are runtime convenience only and must never become durable analytical truth.

### P1.7C — Deterministic orchestration acceptance

Prove:

- CLI and browser share the same `Phase1RunService` and result formatter;
- bounds are enforced;
- exact partial-success accounting remains intact;
- no-work reruns are clean and do not manufacture artifacts;
- current accepted dependencies are reused;
- report counts/queues change only when durable state changes.

### P1.7D — Bounded live acceptance

After deterministic gates pass, run one deliberately bounded real workflow under the configured source/model policy. Record exact request and model bounds, outcomes, remaining eligible work, corpus verification, and any environment/provider blocker.

Do not force a live model/source call merely to obtain a green document. If an external/local provider is unavailable, preserve deterministic acceptance and record the exact bounded blocker.

## 3. Non-goals

- no Phase-2 taxonomy or corpus-wide capability-profile generation;
- no automatic Capability batch generation;
- no Blueprint reopening;
- no durable distributed operation queue;
- no new source or generic source abstraction;
- no personal readiness or recommendation logic;
- no automatic Git publication.

## 4. Acceptance

P1.7 is accepted only when:

- [x] the report reproduces from current SQLite state and is covered by deterministic fixtures;
- [x] CLI and browser render the same report object;
- [x] queue membership and lineage are dependency-correct;
- [x] operation links are safe local paths and point to inspectable results;
- [x] full Ruff/pytest/warnings gates pass;
- [x] bounded live acceptance is completed or recorded as an exact environment/provider blocker;
- [x] controlling docs state the exact remaining Phase-1 closure status without over-claiming.

Acceptance evidence is recorded in:

```text
docs/working-memory/2026-08-23_P1_7_AND_PHASE_1_CLOSURE.md
```
