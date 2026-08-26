# Utility / Epistemic Governance Reorientation

Date: 2026-08-26  
Status: **ACCEPTED GOVERNANCE REORIENTATION / P2.2 DESIGN NEXT**

## 1. Trigger

After closing P2.1, review of the next Phase-2 step exposed a product-governance risk: JobHunter's successful Phase-1/P2.1 evidence discipline was beginning to generalize into an assumption that useful semantic interpretation should wait for deterministic proof, exhaustive canonical mapping, or human promotion.

The repository owner challenged that direction because JobHunter's product purpose is to help the user understand jobs and make career decisions faster and better than manual vacancy-by-vacancy reading.

The resulting decision is not to weaken source truth. It is to **separate strict substrate authority from useful analytical reasoning**.

## 2. What remains unchanged

The following remain strict:

- source evidence and source wording;
- source identity/version/lifecycle safety;
- translation/source separation;
- P1.6 factual substrate boundaries;
- accepted artifact/dependency/currentness identity;
- persistence/history/idempotency invariants;
- canonical registry mutation/review constraints;
- privacy/publication boundaries;
- stable canonical Market statistics when they are eventually built.

P2.1 remains accepted/closed. Its strong review was appropriate because it created durable reusable canonical state.

## 3. New permanent interpretation model

```text
Level 1 — source fact
strict evidence/provenance

Level 2 — normalized correspondence
source wording preserved; reviewed/deterministic mapping

Level 3 — analytical interpretation
semantic/model reasoning is allowed and expected
confidence/evidence/uncertainty communicated
not employer wording

Level 4 — recommendation / decision synthesis
explainable reasoning over qualified market + later personal inputs
```

The project must also distinguish:

```text
GENERATED / CANDIDATE
useful immediately; revisable; low/medium blast radius

REVIEWED / PROMOTED
reusable durable authority; stronger acceptance proportional to downstream reuse
```

Human review is primarily a promotion boundary rather than a prerequisite for every useful interpretation.

## 4. Failure semantics correction

Hard failures remain appropriate for integrity problems such as wrong/stale dependencies, fabricated facts, invalid persistence, unsafe lifecycle conclusions, privacy violations, and invalid canonical mutation.

Interpretive uncertainty should normally fail soft:

```text
uncertain role family
multiple plausible archetypes
small sample
ambiguous responsibility grouping
incomplete technical scope

→ confidence/alternatives/unknowns/warnings
→ useful bounded output may still be shown
```

## 5. Product acceptance correction

Definition-of-done now asks both:

```text
INTEGRITY
Does the increment preserve source/state/provenance/privacy and applicable contract invariants?

UTILITY
Does it materially reduce user effort or improve the speed/quality of a real career-intelligence task?
```

Evidence gathering, review ceremonies, and deterministic machinery are not product value by themselves.

## 6. Files added/modified

### Controlling policy

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

Defines:

- utility target;
- determinism boundary;
- epistemic levels;
- candidate vs promoted intelligence;
- proportional strictness;
- hard vs soft failures;
- two-speed intelligence;
- human-review promotion policy;
- sample-size semantics;
- implementation/acceptance rules.

### Repository instructions

`AGENTS.md`

Updated so future assistants/contributors must follow the new policy and must not turn interpretive uncertainty into unnecessary blockers or repeat completed validation without meaningful reason.

### Roadmap amendment

`docs/ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md`

Preserves P2.1 → P2.2 → P2.3 → P2.4 sequencing while allowing useful job-level interpretation before exhaustive canonical promotion.

### Implementation-plan amendment

`docs/IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md`

Defines Tier A integrity/persistence acceptance, Tier B promoted semantic acceptance, and Tier C bounded analytical interpretation acceptance.

### Proposal refinement

`docs/proposals/05A_FAST_INTERPRETATION_PROMOTION_AND_ROLE_INTELLIGENCE_REFINEMENT.md`

Refines responsibility families, Role DNA, title mismatch, archetypes, deliverables, and capability relationships into candidate versus promoted states.

### Execution amendment

`docs/EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md`

Records the current Phase-2 operational state without rewriting closed historical checklist detail.

## 7. Why the higher product/domain/architecture specs were not rewritten wholesale

Review found that the higher-level documents already contain the correct foundational principles:

- Product Specification: JobHunter is a repeated-use utility and daily usefulness matters;
- Domain Model: `model-inferred` is a legitimate provenance class; confidence/unknown/review states already exist;
- Architecture: `Models may reason; they do not manufacture source truth.`

The drift was mainly in **operational interpretation of those rules**, especially over-applying promotion-grade evidence/acceptance to low-blast-radius analysis.

Therefore the correction is intentionally concentrated in a controlling reasoning-policy companion plus roadmap/implementation/assistant amendments, rather than rewriting accurate historical/domain material for cosmetic consistency.

## 8. P2.2 consequence

The next focused plan should no longer be framed primarily as an evidence-sufficiency gate.

Preferred shape:

```text
P2.2A responsibility/work intelligence contract
- exact factual inputs
- fast job-level work composition
- candidate vs promoted states
- confidence/uncertainty
- promotion boundary

P2.2B selective canonical responsibility/deliverable expansion

P2.2C responsibility-family candidate + promotion model

P2.2D role-archetype/work-composition intelligence
- candidate interpretation may appear early
- stable archetype promotion requires stronger repeated evidence
```

P2.2 may adjust these labels during focused planning, but it must preserve the authority distinction.

## 9. Exact current state

```text
Phase 1                              CLOSED
P2.1                                 CLOSED / ACCEPTED
P1.6 v20/v5                          ACCEPTED / FROZEN INPUT
Capability v9/v5                     ACCEPTED / FROZEN INPUT
Canonical registry v1                ACCEPTED
Registry publication                 NOT AUTHORIZED
Utility/epistemic policy             ACCEPTED / CONTROLLING COMPANION
Roadmap reasoning amendment          ACCEPTED
Implementation reasoning amendment   ACCEPTED
Agent governance                     RECONCILED
Next implementation code             NOT YET AUTHORIZED
Next design step                      FOCUSED P2.2 PLAN
```

## 10. Permanent caution

Do not react to this correction by swinging to the opposite extreme.

The new rule is not `LLM output is fine`. The rule is:

> JobHunter should be trustworthy because it knows what kind of claim it is making and communicates that authority honestly—not because every useful interpretation has been forced through the strongest evidence gate.
