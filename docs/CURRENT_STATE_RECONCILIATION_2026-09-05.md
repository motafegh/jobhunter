# JobHunter Current-State Reconciliation — 2026-09-05

**Status:** CURRENT-STATE RECONCILIATION / STATUS-ONLY OVERLAY  
**Date:** 2026-09-05  
**Branch:** `main`  
**Scope:** Reconcile obsolete current-status wording in large controlling documents without rewriting historical acceptance narrative or changing product semantics.

## 1. Purpose

Several large 2026-08-23 controlling documents still contain status sentences written before Phase 1, P2.1, and P2.2A closed. Later/current governance, implementation evidence, working memory, and portfolio audit already record the true state consistently.

This document resolves that narrow ambiguity.

It does **not** redesign the roadmap, change product meaning, authorize new features, alter semantic contracts, or rewrite historical chronology.

## 2. Current authoritative operating state

For present-tense execution/status interpretation, use:

```text
Phase 1                         CLOSED / ACCEPTED
P2.1 Canonical Registry        CLOSED / ACCEPTED
P2.2A Job Work Intelligence    CLOSED / ACCEPTED
P2.2B-B1                       IN PROGRESS / ta9l local P1.6 acceptance gate
P2.2C                          BLOCKED
Blueprint v6                   EXPERIMENTAL / HISTORICAL / NON-AUTHORITATIVE
```

Current public/accepted contracts remain:

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6:                 job-analysis-english-v20 / job-analysis-v5
Original P1.6:                job-analysis-original-v9 / job-analysis-v4
Capability:                   job-capability-intelligence-v9 / job-capability-intelligence-v5
Work Intelligence:            job-work-intelligence-v2 / v2.0
Canonical Registry:           jobhunter-canonical-concept-registry-v1
Public Corpus:                jobhunter-public-corpus-v1
```

Current accepted heterogeneous P1.6 → Capability anchors are:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

## 3. Status wording superseded for current-state reading

The following older present-tense status statements must not be used as current execution truth:

### `docs/ROADMAP.md`

Older wording includes, in substance:

- heterogeneous role-family validation is active;
- P2.2A semantic/product acceptance is active;
- Stage R0 / Phase 1 is `Active now`;
- Phase 2 is blocked as though P2.1/P2.2A had not yet progressed.

Current interpretation:

```text
heterogeneous validation → CLOSED
Phase 1                  → CLOSED / ACCEPTED
P2.1                     → CLOSED / ACCEPTED
P2.2A                    → CLOSED / ACCEPTED
Phase-2 current frontier → P2.2B-B1
```

The roadmap's strategic sequencing, permanent rules, proposal disposition, and future-stage design remain controlling unless separately amended. Only obsolete present-tense status wording is superseded here.

### `docs/IMPLEMENTATION_PLAN.md`

The stage table still contains the older entry:

```text
Phase 1 | Active
```

Later sections of the same document correctly state that Phase 1 closed on 2026-08-23.

Current interpretation:

```text
Phase 1 → CLOSED / ACCEPTED
Phase 2 → ACTIVE IN BOUNDED INCREMENTS
current exact increment → P2.2B-B1 selective responsibility promotion pilot
```

Historical Phase-1 gate descriptions remain historical acceptance evidence and are not converted into current work.

### `docs/PRODUCT_SPECIFICATION.md`

Older passages still describe heterogeneous validation as active and do not fully reflect the later P2.1/P2.2A accepted surfaces.

Current interpretation:

- the product specification's product purpose, authority model, functional requirements, and permanent boundaries remain controlling;
- current implemented/accepted status is read together with `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/EXECUTION_TODO.md`, `docs/WORKING_MEMORY.md`, and the active P2.2 plans;
- P2.1 Canonical Registry and P2.2A Work Intelligence are accepted current functionality;
- P2.2B-B1 is the current product-development gate.

## 4. Current exact product-development gate

Controlling focused plan:

```text
docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md
```

Current evidence state:

```text
repo-side recurrence scan complete
→ ta9l selected as the single additional evidence-bearing job
→ no accepted/current ta9l P1.6 yet
→ no responsibility promotion yet
```

Exact next product action remains:

```text
ta9l current English projection
→ ta9l English P1.6 v20 generation
→ semantic review / acceptance decision
→ report exact accepted responsibility shape
→ compare against tG9K P1.6 36 responsibility[5]
→ final non-lossy correspondence review
→ only then possible one-concept/two-mapping registry mutation
```

If `ta9l` does not preserve the selected responsibility shape, stop before canonical mutation and record the evidence-based decision.

## 5. Parallel portfolio/release state

Portfolio-readiness work is a separate track and does not advance the product semantic gate.

Current portfolio state:

```text
PR0–PR8    COMPLETE / repository-side complete as recorded
PR9-A      final repository/public audit COMPLETE
PR9-B      owner/external release blockers PENDING
PR9-C      intentional v0.1.0 release PENDING
PR9-D      CV/interview package COMPLETE
PR9-E      owner mastery PREPARED / NOT VERIFIED
```

Remaining PR9 blockers/actions are intentionally not fabricated or auto-resolved:

1. owner license-policy decision;
2. GitHub description/topics settings action;
3. real browser screenshots from the actual local application plus privacy review;
4. final current-count/version check and CI confirmation;
5. intentional `v0.1.0` tag/release;
6. owner mastery verification.

Portfolio work must not bypass P2.2B-B1, promote registry state, or start P2.2C.

## 6. Precedence rule for stale status text

When a historical/current-status sentence conflicts with the accepted state above:

```text
product/domain/source/architecture invariants
→ utility/epistemic reasoning policy
→ strategic roadmap/implementation semantics
→ this current-state reconciliation for obsolete present-tense status only
→ active focused plan
→ EXECUTION_TODO / WORKING_MEMORY
→ implementation/tests/live acceptance
```

This reconciliation has no authority to weaken higher-level product/domain/source/architecture meaning. Its only job is to prevent old status labels from being mistaken for the current execution frontier.

## 7. Closure decision

The documentation issue identified by the PR9 audit is now bounded and explicitly reconciled:

```text
KEEP historical chronology
→ DO NOT broad-rewrite large master documents merely for cosmetic consistency
→ SUPERSEDE obsolete present-tense status wording explicitly
→ keep one current product frontier: P2.2B-B1 / ta9l P1.6 gate
→ keep portfolio release work separate
```

Future deliberate rewrites of `ROADMAP.md`, `IMPLEMENTATION_PLAN.md`, or `PRODUCT_SPECIFICATION.md` may fold these status corrections directly into those documents. Until then, this record is the current status bridge and prevents the known stale passages from controlling execution.
