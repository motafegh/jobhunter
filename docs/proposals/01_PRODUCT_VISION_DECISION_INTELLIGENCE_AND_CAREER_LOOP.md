# JobHunter Product Vision, Decision Intelligence, and Career Loop Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B001, B137-B145, B147, B200

---

## Purpose

This file contains proposals that define what JobHunter could ultimately become as a product and how it could make evidence-backed career decisions without collapsing into a generic job board, opaque recommendation engine, or autonomous application bot.

The central product direction is a closed but inspectable loop:

```text
market evidence
    ↓
role and requirement intelligence
    ↓
personal evidence
    ↓
gaps and constraints
    ↓
learning / project / application decisions
    ↓
new evidence and outcomes
    ↓
updated understanding
```

Every proposal below is a candidate. Promotion into implementation requires explicit placement in the controlling master plan and acceptance criteria appropriate to the capability.

---

## B001 — Career-intelligence system as the product identity

**Intent:** Define JobHunter as more than a scraper or job aggregator.

**Proposal:** Treat the long-term product as an evidence-grounded personal career-intelligence system with five cooperating domains: market intelligence, role intelligence, personal capability intelligence, gap intelligence, and action intelligence. Job acquisition remains a necessary input, not the product's final value.

**Design direction:**

- preserve employer/source evidence as the highest-authority market layer;
- derive role and market structures from reviewed analysis rather than titles alone;
- represent personal capability only through explicit evidence contracts;
- derive recommendations from inspectable market/personal relationships;
- make every consequential recommendation explainable and challengeable.

**Guardrails:** Do not turn this vision into an excuse to implement every future subsystem at once. The current modular monolith, current phase gates, and acceptance order remain controlling.

**Promotion signal:** Revisit when deciding product-level Phase 2-5 boundaries or when a new feature needs to be tested against the long-term identity of JobHunter.

---

## B137 — Career hypothesis testing

**Intent:** Let the user test a career direction as a falsifiable hypothesis instead of committing to it because it sounds attractive.

**Proposal:** Introduce a future `CareerHypothesis` concept. A hypothesis could state, for example, that a target role family is realistically reachable or strategically attractive. JobHunter would accumulate evidence for and against the hypothesis from market volume, responsibility patterns, required capability bundles, personal overlap, gaps, constraints, and observed application outcomes.

**Design direction:**

- hypotheses are user-created or explicitly approved;
- supporting and contradicting evidence are stored separately;
- evidence is timestamped and reproducible from a market snapshot;
- conclusions may be `supported`, `mixed`, `weakly supported`, or `insufficient evidence`, not only true/false;
- the system should show what evidence would materially change the conclusion.

**Guardrails:** Do not infer life goals from conversation history or silently create career hypotheses. Do not equate a small job sample with market viability.

**Promotion signal:** After canonical market intelligence and personal-evidence comparison are accepted.

---

## B138 — Explicit Target Role Specification

**Intent:** Replace vague remembered intent with a durable, user-controlled definition of what JobHunter is optimizing for.

**Proposal:** Create a versioned Target Role Specification describing primary roles, adjacent roles, excluded/low-priority role families, geographic scope, and optional role-specific preferences. Acquisition can remain broad, but ranking, comparison, gap analysis, and reports can use this explicit target context.

**Design direction:**

```text
TargetRoleSpecification
- primary role families
- adjacent role families
- excluded/deprioritized families
- geography / work-mode scope
- effective date / version
- user notes
```

The specification should reference canonical role/archetype concepts once Phase 2 has them, rather than storing arbitrary model prose as durable truth.

**Guardrails:** Search vocabulary must remain distinct from target-role truth. A term appearing in a search pack does not automatically become a target role.

**Promotion signal:** Before personal gap analysis becomes a normal repeated workflow.

---

## B139 — Multiple career scenarios

**Intent:** Compare plausible paths without overwriting one global career target.

**Proposal:** Allow independent scenarios such as `AI Security`, `Applied AI`, or `Security Automation`. Each scenario would reuse the same authoritative market and personal evidence but apply different role targets, constraints, and decision policies.

**Design direction:**

- one source corpus, not duplicated databases;
- scenario-specific target roles and preference weights;
- scenario-specific gap and opportunity views;
- deterministic side-by-side comparison of market size, major responsibilities, required capability bundles, personal evidence overlap, and unresolved gaps;
- explicit active/default scenario for normal UI use.

**Guardrails:** Do not duplicate personal capabilities per scenario. Do not fabricate precise success probabilities for scenarios.

**Promotion signal:** When the personal evidence layer is stable enough that multiple target interpretations become useful rather than speculative.

---

## B140 — Personal constraints as a separate decision layer

**Intent:** Distinguish technical/capability fit from real-life feasibility.

**Proposal:** Model user-controlled constraints such as location, relocation, work authorization, language, remote/hybrid preferences, compensation floor, travel, on-call tolerance, and other practical conditions separately from capability evidence.

**Design direction:** A job may be technically aligned but operationally impossible. JobHunter should be able to explain both dimensions independently:

```text
capability assessment: plausible
constraint assessment: blocked by location requirement
```

Constraints should have provenance (`user-provided`) and effective dates where useful.

**Guardrails:** Never infer sensitive or private constraints from unrelated data. Do not conflate preferences with skill gaps.

**Promotion signal:** Before application-readiness recommendations are presented as decision support.

---

## B141 — Preference strength model

**Intent:** Avoid treating every personal preference as an absolute filter.

**Proposal:** Represent preferences using explicit strength classes such as `hard_constraint`, `strong_preference`, `soft_preference`, and `neutral`. This lets JobHunter explain tradeoffs rather than silently eliminating opportunities.

**Design direction:**

- hard constraints can exclude a job from recommendation views while retaining it in evidence/history;
- strong/soft preferences influence ordering and explanation but do not become capability claims;
- the user can inspect which preference affected a decision;
- preference changes create a new effective configuration/version rather than rewriting historical decisions.

**Guardrails:** No opaque weighted score is required. Categorical policy is preferable until a more complex approach proves useful.

**Promotion signal:** Alongside the personal-constraints model.

---

## B142 — Decision explanation contract

**Intent:** Make every significant recommendation answer “why?” in a consistent way.

**Proposal:** Define a future explanation contract for opportunity and career recommendations. At minimum, an explanation should separate market alignment, personal evidence, critical gaps, preferences/constraints, uncertainty, and source freshness.

**Design direction:**

```text
DecisionExplanation
- conclusion
- supporting market evidence
- supporting personal evidence
- blocking gaps
- non-blocking gaps
- constraints/preferences
- uncertainty / missing evidence
- data snapshot / analysis contract
```

The explanation should link back to inspectable evidence, not merely contain generated prose.

**Guardrails:** The explanation is derived. It does not become higher authority than the evidence it cites.

**Promotion signal:** Before any “apply / prepare / skip” recommendation becomes a normal product surface.

---

## B143 — Recommendation challenge mode

**Intent:** Reduce confirmation bias and make JobHunter actively search for reasons its own recommendation may be wrong.

**Proposal:** Add a “Challenge this recommendation” action that constructs a bounded counter-analysis using contradictory requirements, missing personal evidence, constraints, uncertainty, sample limitations, and competing interpretations.

**Design direction:** Challenge mode should prioritize already-known evidence before invoking an LLM. Model synthesis may summarize contradictions, but deterministic facts and exact evidence remain visible.

**Possible output:**

```text
Reasons the current recommendation may be too optimistic
- required production Kubernetes evidence is absent
- five years of security-operations experience is explicitly requested
- German C1 is a hard employer requirement
```

**Guardrails:** This is not pessimism mode. It is evidence-adversarial review. It should also be able to challenge an overly negative conclusion.

**Promotion signal:** After recommendation explanations and personal gap states are stable.

---

## B144 — “What would change the conclusion?”

**Intent:** Turn a static recommendation into an actionable threshold.

**Proposal:** For a decision such as `prepare first`, identify the smallest evidence or constraint changes that could plausibly change the result. Examples: independent Docker evidence, verified language level, one missing hard requirement, or resolution of an unknown employment constraint.

**Design direction:**

- operate on explicit missing/partial evidence states;
- separate “could change conclusion” from “guarantees success”;
- allow multiple alternative paths;
- use counterfactual calculations where deterministic mappings exist;
- preserve the original conclusion and snapshot for reproducibility.

**Guardrails:** Never present acquiring one skill as guaranteeing an interview or offer.

**Promotion signal:** After counterfactual gap analysis is available.

---

## B145 — End-to-end data provenance graph

**Intent:** Make high-level career conclusions traceable through every derivation layer.

**Proposal:** Represent logical lineage from raw evidence through parsing, translation, semantic claims, canonical concepts, market aggregates, personal mappings, gaps, and recommendations.

**Conceptual path:**

```text
raw evidence
  → parsed source field
  → semantic claim
  → canonical concept
  → market aggregate
  → gap assessment
  → recommendation
```

**Design direction:** Start with relational identifiers and provenance links already natural to SQLite. A graph database is not required. The UI may later render a graph or breadcrumb path over those relations.

**Guardrails:** Do not create a generic graph platform before actual lineage queries justify it. Every edge must have defined semantics.

**Promotion signal:** Incrementally as Phase 2-4 introduce cross-layer derived entities.

---

## B147 — Career Digital Twin as a conceptual model

**Intent:** Provide a possible long-term product framing for the continuously updated state of market, target, personal evidence, constraints, and decisions.

**Proposal:** Treat “Career Digital Twin” only as a conceptual umbrella, not as a new technical subsystem. It describes the combined current state produced by existing domain records:

```text
market state
+ target-role state
+ personal capability evidence
+ constraints/preferences
+ decisions/outcomes
```

**Design direction:** If the term is used in UI or documentation, every component must map to concrete versioned records. No hidden AI memory should be considered part of the twin.

**Guardrails:** Avoid marketing language that implies predictive certainty or complete knowledge of the user. The system remains an incomplete evidence model.

**Promotion signal:** Only if the concept improves product communication after the underlying layers exist.

---

## B200 — The Market → Gap → Learn → Build → Evidence → Apply loop

**Intent:** Define the strongest candidate repeated-use loop for the mature product.

**Proposal:** JobHunter should eventually connect market observation to practical career action through an evidence-preserving feedback loop:

```text
MARKET
what employers actually request
    ↓
GAP
what evidence is missing or weak
    ↓
LEARN
what prerequisite understanding is needed
    ↓
BUILD
what bounded work can create evidence
    ↓
VERIFY
what the user can actually demonstrate
    ↓
APPLY
which opportunities now make sense
    ↓
OUTCOME
what happened and what was explicitly learned
    ↓
updated evidence and decisions
```

**Design direction:** Each transition should be its own inspectable contract. Learning does not automatically become capability evidence; project completion does not automatically become independent mastery; rejection does not automatically identify a causal skill gap.

**Guardrails:** This loop must remain evidence-grounded and user-controlled. It is not an autonomous career manager.

**Promotion signal:** Use this loop as a product-level integration test when Phases 2-5 are planned.

---

## Category-level recommendation

These proposals should influence architecture and future planning, but most should not produce immediate code. The best near-term use is to keep them as decision criteria while JobHunter finishes the current Phase-1 acceptance sequence and begins a disciplined Phase-2 market-intelligence design.