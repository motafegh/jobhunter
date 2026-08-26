# JobHunter Utility, Epistemic Authority, and Reasoning Policy

**Status:** CONTROLLING GOVERNANCE COMPANION  
**Date:** 2026-08-26  
**Scope:** All current and future derived intelligence, semantic interpretation, canonicalization, aggregation, recommendations, and assistant behavior  
**Authority:** Subordinate to `PRODUCT_SPECIFICATION.md`, `DOMAIN_AND_ANALYSIS_MODEL.md`, `SOURCE_POLICY.md`, and `ARCHITECTURE.md`; controlling for how their evidence/uncertainty principles are operationalized when roadmap, implementation, plans, proposals, tests, or assistant behavior are ambiguous.

---

## 1. Why this policy exists

JobHunter exists to help a user understand real job-market information and make career decisions **faster and better than manual vacancy-by-vacancy reading**, while remaining trustworthy and inspectable.

The project must avoid two opposite failure modes:

```text
UNDER-GROUNDED
fast but opaque or fabricated intelligence

OVER-GATED
trustworthy substrate, but useful interpretation is blocked until everything
is deterministic, human-reviewed, canonically promoted, or statistically mature
```

Both are product failures.

Evidence is a safety rail underneath intelligence. **Evidence collection, deterministic machinery, and acceptance ceremonies are not the product by themselves.**

The permanent optimization target is:

> **maximize useful, decision-relevant career intelligence per unit of user time, subject to source integrity, provenance, privacy, and honest uncertainty.**

---

## 2. Core distinction: trustworthiness is not the same as determinism

Determinism is required where the problem is deterministic. It must not be used as a substitute for semantic reasoning.

### 2.1 Keep deterministic

Examples:

```text
logical IDs and stable keys
artifact/dependency/currentness identity
source versions and immutable history
exact employer/source wording
evidence references and indices
counts and deterministic aggregates
deduplication and bookkeeping
lifecycle state transitions where rules are explicit
review/promotion state
registry collision/supersession constraints
```

### 2.2 Allow semantic/model reasoning

Examples:

```text
responsibility similarity
job work composition
likely responsibility families
candidate role archetypes
capability/work relationships
strongly work-implied expectations
comparative summaries
what appears important or unusual in a vacancy
career-oriented synthesis
later explainable recommendations
```

A model-generated interpretation is not source truth, but it can still be useful product intelligence.

Permanent rule:

> **Determinism protects bookkeeping, provenance, and authority. It does not replace reasoning.**

---

## 3. Epistemic levels

Every consequential derived conclusion should be representable at the level that matches what is actually known.

### Level 1 — source fact

Direct employer/source fact or deterministic source-derived fact.

Examples:

```text
"PowerShell"
"three to six years"
"Managing next-generation firewalls"
```

Policy:
- strict source/provenance rules;
- do not fabricate;
- do not silently strengthen or rewrite employer meaning.

### Level 2 — normalized correspondence

A reviewed or deterministic correspondence that preserves original wording.

Examples:

```text
"Linux operating system" -> platform:linux
"Managing NGFW equipment" -> reviewed canonical responsibility
```

Policy:
- preserve exact source wording and mapping provenance;
- promotion into reusable canonical knowledge requires the relevant review rules;
- unresolved correspondence is valid.

### Level 3 — analytical interpretation

A semantic synthesis or inference supported by source/derived evidence but not claimed as employer wording.

Examples:

```text
"This vacancy appears primarily to combine network-security architecture,
firewall operations, VPN/segmentation work, and troubleshooting."

"This responsibility likely belongs to both Security Assessment and
Security Automation candidate families."
```

Policy:
- **allowed as a first-class product output without prior canonical promotion**;
- preserve supporting evidence/reasons where consequential;
- expose confidence/uncertainty where useful;
- never display it as employer-authored fact;
- ambiguity normally reduces confidence instead of blocking output.

### Level 4 — recommendation / decision synthesis

An explainable system recommendation that combines market intelligence, user state, constraints, and later personal evidence.

Policy:
- may use probabilistic/model reasoning;
- must expose material reasons and uncertainty;
- must not invent personal evidence or employer facts;
- consequential durable recommendations follow the applicable reviewed personal-evidence and decision-policy boundaries.

---

## 4. Candidate versus promoted intelligence

JobHunter must distinguish **useful interpretation** from **reusable system authority**.

```text
GENERATED / CANDIDATE
- useful immediately
- model reasoning allowed
- evidence/reasons/confidence visible as appropriate
- not automatically reusable canonical truth

        ↓ optional review/promotion

REVIEWED / PROMOTED
- reusable durable knowledge
- stronger invariants and review
- may feed stable canonical aggregation or downstream authority
```

Examples:

```text
candidate job-level interpretation:
"security-hardening + automation heavy"

promoted reusable knowledge:
canonical responsibility family / accepted role archetype
```

Human review is therefore primarily a **promotion boundary**, not a mandatory prerequisite for every useful interpretation.

---

## 5. Strictness must be proportional to authority and blast radius

Do not apply the strongest acceptance standard uniformly to every layer.

Use stronger validation when a result:

- rewrites or claims source truth;
- changes immutable/current dependency state;
- becomes a reusable canonical concept/family/archetype;
- feeds corpus-wide statistics as stable taxonomy;
- materially affects later personal gap/readiness decisions;
- is published or reused across many jobs/users/runs.

Use lighter-weight validation when a result:

- is a bounded job-level interpretation;
- is clearly labeled inferred/candidate;
- is easy to regenerate/revise;
- has limited downstream blast radius;
- exists to reduce manual reading effort rather than establish permanent market truth.

Permanent rule:

> **The cost of proving a conclusion should scale with the authority and consequences assigned to that conclusion.**

---

## 6. Hard failures versus soft uncertainty

### 6.1 Fail hard for integrity defects

Examples:

```text
wrong artifact/dependency identity
stale data presented as current
corrupt persistence or schema violation
unsupported source quote/evidence
fabricated employer fact
unsafe source/lifecycle transition
canonical mutation violating immutable review constraints
privacy/publication boundary violation
```

These may block persistence, promotion, publication, or the affected operation.

### 6.2 Fail soft for interpretive uncertainty

Examples:

```text
uncertain role family
ambiguous responsibility grouping
multiple plausible archetypes
small semantic sample
weakly supported work implication
incomplete technical scope
```

Preferred behavior:

```text
uncertainty
→ lower confidence / show alternatives / preserve unknowns / warn
→ still provide useful bounded interpretation when possible
```

Do **not** automatically convert interpretive uncertainty into a feature blocker.

---

## 7. Two-speed intelligence model

### 7.1 Fast intelligence

As soon as the substrate is sufficiently trustworthy for the question, JobHunter should be able to help the user understand a vacancy or bounded set of vacancies.

Examples:

- concise job/work summary;
- important requirements/responsibilities;
- likely work composition;
- candidate responsibility families;
- likely role/archetype interpretation;
- important technical emphasis;
- differences from similar jobs;
- unusual requirements;
- uncertainty and missing scope.

Fast intelligence may be generated/model-inferred. It must remain traceable and correctly labeled.

### 7.2 Promoted intelligence

Promoted knowledge is used for stable reuse and aggregation.

Examples:

- canonical concepts and aliases;
- accepted canonical responsibilities;
- accepted responsibility families;
- stable role archetypes;
- reviewed capability relationships;
- canonical Market v2 aggregates;
- later durable personal gap/readiness conclusions.

Promoted intelligence deserves stronger validation because errors propagate.

---

## 8. User-facing communication rules

For consequential outputs, JobHunter should make it possible to distinguish:

```text
what the employer explicitly said
what JobHunter normalized
what JobHunter inferred/interpreted
what remains uncertain or unsupported
```

Not every screen must show four labels on every sentence. The UX may summarize intelligently, but the underlying distinction must remain recoverable and material uncertainty must not be hidden.

Avoid two UX extremes:

- showing raw provenance machinery so aggressively that the user must perform the analysis manually;
- showing polished AI conclusions with no way to understand their basis.

The target is **fast comprehension with inspectable depth on demand**.

---

## 9. Human review policy

Human review is required when the applicable contract says a result is being promoted into durable reusable authority.

Human review is **not automatically required** for:

- transient job summaries;
- candidate responsibility-family suggestions;
- candidate archetype suggestions;
- bounded comparison/synthesis;
- low-blast-radius analytical views clearly marked inferred/candidate.

Do not invent manual review work merely because a model was involved.

When review is required, make it efficient: review the consequential semantic decision, not every deterministic intermediate representation.

---

## 10. Sample-size policy

Small samples do not automatically prohibit useful analysis.

Use sample size according to the claim:

```text
job-level interpretation
→ one job can be enough

candidate recurring pattern
→ a few jobs may justify a hypothesis with warning

stable role archetype / market prevalence claim
→ require stronger cross-job/employer support

broad market conclusion
→ require explicit sample/scope/concentration qualification
```

Do not demand market-scale evidence for a job-level question.
Do not present job-level evidence as a market-wide fact.

---

## 11. Phase-2 operational consequence

P2.1 remains accepted and closed. Its strict registry review was appropriate because it established durable reusable canonical state.

For P2.2 and later Phase-2 work:

```text
accepted P1.6 responsibility/work evidence
→ fast job-level responsibility/work interpretation allowed
→ candidate canonical responsibilities/families/archetypes allowed
→ review/promotion only where reusable durable authority is created
→ canonical aggregation only from the promoted subset required by that aggregate
```

P2.2 must not become a requirement to manually canonicalize every responsibility before JobHunter can provide role/work intelligence.

Role archetype **candidates** may be generated before there is enough evidence to promote a stable archetype. Lack of promotion evidence should not suppress useful job-level work-composition output.

---

## 12. Implementation and acceptance policy

Every increment still requires appropriate engineering quality, but definition-of-done must include product utility as well as correctness.

Ask both:

1. **Integrity:** does this preserve source truth, state, provenance, privacy, and applicable contract invariants?
2. **Utility:** does this materially reduce user effort or improve the speed/quality of a real career-intelligence task?

Avoid acceptance work whose only effect is to accumulate evidence for already-established low-risk behavior.

Do not require duplicate reruns or repeated manual evidence when the requested gate has already been credibly observed and recorded.

Tests should concentrate on:

- high-blast-radius invariants;
- repeatable real defects;
- dangerous hallucination/authority confusion;
- promotion/persistence boundaries;
- representative analytical behavior where deterministic assertions are meaningful.

Do not attempt to make intrinsically semantic output deterministic solely to simplify tests.

---

## 13. Assistant/contributor behavior

AI assistants and contributors must:

- distinguish integrity requirements from interpretive quality preferences;
- avoid turning every ambiguity into a blocker;
- avoid escalating every model inference into a new durable contract;
- avoid asking the user to repeat completed validation merely because pasted output is incomplete when the user has explicitly and credibly confirmed the result;
- prefer bounded useful progress with explicit uncertainty over unnecessary paralysis;
- preserve strict source/provenance/privacy rules;
- use stronger review only at the correct promotion boundary;
- challenge both under-grounded shortcuts **and** over-engineered evidence rituals.

When unsure whether a conclusion must be reviewed before use, ask:

> **Is this becoming reusable authority, or is it a transparent bounded interpretation?**

That distinction should determine the gate.

---

## 14. Non-goals

This policy does **not** authorize:

- fabricated source facts;
- silent replacement of employer wording;
- opaque recommendations;
- unsupported personal capability claims;
- unreviewed automatic canonical taxonomy growth;
- misleading market-wide conclusions from tiny samples;
- weakening privacy/source policy;
- bypassing deterministic persistence/state invariants;
- autonomous job applications or recruiter communication.

It also does not require every generated interpretation to be persisted. Ephemeral or regenerable intelligence is often preferable when durable authority is unnecessary.

---

## 15. Permanent summary

```text
SOURCE / STATE INTEGRITY
→ strict and deterministic where possible

INTERPRETATION
→ reasoning is allowed and expected
→ traceable, calibrated, uncertainty-aware

PROMOTION TO REUSABLE AUTHORITY
→ stronger review proportional to blast radius

USER EXPERIENCE
→ useful intelligence should arrive before exhaustive canonicalization
```

The project should be trustworthy **because it knows what kind of claim it is making**, not because every useful thought has been forced through the strongest possible evidence gate.
