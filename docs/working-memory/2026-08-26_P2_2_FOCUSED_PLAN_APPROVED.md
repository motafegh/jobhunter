# P2.2 Focused Plan Approved — Job Work Intelligence v1 Next

**Date:** 2026-08-26  
**Status:** CURRENT DECISION RECORD  
**Branch:** `main`  
**Controlling focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

## Decision

The post-P2.1 governance discussion is complete and the next Phase-2 plan is approved.

P2.2 is not being treated as an exhaustive responsibility-canonicalization program. Its first product goal is to reduce the time and cognitive effort required to understand what a vacancy actually involves.

Approved sequence:

```text
P2.2A Job Work Intelligence v1
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

## P2.2A architectural decisions

1. Primary input is accepted/current English P1.6 v20/v5.
2. Capability v9 is not an authoritative P2.2A dependency; this keeps the first work-intelligence layer close to accepted factual work evidence.
3. Existing canonical mappings may be attached when available but cannot gate generation.
4. Work themes must own at least one accepted responsibility or role-purpose reference. Requirements may support a theme but may not independently manufacture duties.
5. P2.2A persists a versioned generated/candidate `JobWorkIntelligenceArtifact` under working contract `job-work-intelligence-v1`.
6. Persistence means reproducible generated interpretation, not human acceptance or canonical promotion.
7. Candidate output does not enter a `pending human approval` state merely because a model generated it.
8. Relative work emphasis uses `primary`, `supporting`, or `uncertain`; no fake percentages.
9. Interpretive confidence uses high/medium/low without claiming calibrated probability.
10. Deliverables may be `source_explicit` or `strongly_implied_by_work`; generic tool knowledge cannot manufacture them.
11. Candidate role/archetype interpretation may exist for one job, but stable reusable archetype promotion is later Tier B work.
12. `tmBK` is the deliberate limited-evidence anchor: with accepted requirements but no direct responsibility/role-purpose evidence, Work Intelligence must not invent duties.
13. `tG9K`, `t4qV`, and `tmyX` are the initial responsibility-rich semantic/product acceptance anchors.
14. P2.2A is browser-first; CLI exists for one-job generation/inspection/debugging, not a large review workflow.
15. P2.2 state is local by default. No registry/Work Intelligence/family/archetype public-corpus publication is authorized.

## Acceptance model

P2.2A uses:

```text
Tier A
- persistence/dependency/currentness/reference/privacy invariants

Tier C
- useful, traceable, uncertainty-aware job-level interpretation
```

It does not require promotion-grade Tier B acceptance for every generated artifact.

Product acceptance must explicitly judge whether the Work Intelligence view is faster and clearer than manually reading and grouping the vacancy responsibilities.

## Stop lines

During P2.2A:

- do not bulk-map remaining responsibility/requirement claims;
- do not create global families/archetypes just to finish the increment;
- do not start P2.3 capability requirement profiles;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not publish P2.2 state into `corpus/`;
- do not reopen P1.6 v20, Capability v9, or P2.1 without a material repeatable defect or dependency change.

## Exact next implementation action

Begin P2.2A with the smallest durable vertical slice:

```text
typed Work Intelligence contract
→ persistence/currentness identity
→ bounded service over accepted/current P1.6
→ deterministic reference validation
→ one-job generation/inspection
→ smallest browser-visible Work Intelligence view
```

Start with one responsibility-rich accepted job before broadening to the full initial acceptance set.
