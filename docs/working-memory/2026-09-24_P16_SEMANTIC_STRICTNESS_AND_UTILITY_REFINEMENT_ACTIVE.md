# P1.6 semantic strictness and product-utility refinements — active discussion

**Opened:** 2026-09-24  
**Status:** ACTIVE DISCUSSION / FINDINGS AND PROPOSALS ONLY — NO IMPLEMENTATION APPROVAL  
**Scope:** Evaluate whether current P1.6 generation, validation, review, and whole-result acceptance reject useful source-backed intelligence because of conceptual overlap or disproportionate strictness. Accumulate issues and jointly settle refinements before planning code changes.  
**Working rule:** Record observations, source evidence, interpretations, options, decisions, and unresolved questions separately. Do not silently turn a discussion proposal into a controlling contract.

## Starting context and authority

- [Repository instructions](../../AGENTS.md): maximize useful, decision-relevant intelligence per user time; preserve source integrity; fail soft on interpretive uncertainty; scale strictness with authority and blast radius.
- [Utility/epistemic reasoning policy](../UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md): distinguish source facts from analytical interpretation and candidate output from reviewed/promoted authority; avoid both under-grounded and over-gated product behavior.
- [2026-09-24 v22 post-alias evaluation closure](2026-09-24_P16_V22_POST_ALIAS_EVALUATION_CLOSURE.md): the immediate concrete example, its review outcome, and unresolved preferred-proof-of-work coverage.
- [Rolling working memory](../WORKING_MEMORY.md) and [current-state reconciliation](../CURRENT_STATE_RECONCILIATION_2026-09-12.md): current operational status. This document is a subordinate discussion record and does not supersede them.

**Unchanged operational baseline:** English P1.6 public/current = `job-analysis-english-v21 / job-analysis-v5`; v22 remains an isolated unpromoted candidate; Market I7 remains HOLD. Accepted anchors, semantic promotion rules, Market history, and the stop line on further live generation remain unchanged. No implementation, model call, new acceptance, or authorization to relax an existing gate follows from opening this file.

## Issue R01 — Overlap among capability, practical experience, and proof of ability

### Concrete source/result

For `tvMm` (AI Agent Engineer), an employer expectation says the candidate should be able to **turn an Agent into a reliable system in a real product**. The v22 model produced the concept label `Agent reliability in real product experience`, initially typed as `experience`; v22 changed the ontology to `other` but preserved the phrase. The 2026-09-24 semantic review rejected this as an unsupported assertion of prior experience, and the follow-up guard rejects type-only abstention when experience wording survives. Separately, this source explicitly treats showing/explaining a previously built Agent and supplying a GitHub repository/sample project/demo as valued preferred evidence; the v22 result and requirement ledger omitted that preference. See the v22 closure for precise source/result and comparison-job evidence.

### User's concern / proposed interpretation

Ability to perform complex engineering work and hands-on experience are often closely related; capability, experience, and demonstrable work can legitimately overlap in a job description. A concise generated concept containing `experience` may be a reasonable shorthand for relevant practice rather than an assertion that the employer strictly requires having performed the identical work previously in paid production employment. Automatically treating all such overlap as a fatal error could discard useful information and contribute to repeated whole-analysis failures.

### Refinement identified in discussion (not an approved contract)

1. **Separate the claim from its representation and downstream use.** The source explicitly states a capability expectation. Prior hands-on experience may reasonably support that capability, but the precise requirement of prior professional delivery of that same system is not established by the quoted statement alone. Other parts of the same vacancy may independently state experience or preferred project proof.
2. **Allow non-exclusive concepts and bounded interpretation.** Capability, practice/experience, and evidence of ability need not be forced into a mutually exclusive taxonomy. A source-backed interpretation can describe their relationship if clearly distinguished from employer-authored facts.
3. **Assess semantic materiality and authority, not a keyword alone.** `Agent reliability in real product experience` is ambiguous as a standalone label; it is more consequential if rendered or consumed as a mandatory prior-production-employment condition than as reviewable shorthand. The presence of `experience` alone does not resolve which claim the user or downstream consumer receives.
4. **Prefer a precise source-fact representation plus an optional inference**, e.g. factual expectation: `Ability to turn an Agent into a reliable system in a real product`; associated interpretation: `Relevant hands-on agent/product engineering experience may demonstrate this ability`; preserve separately stated preferred prior-Agent project/demo evidence.
5. **Proportionate failure behavior is a design candidate.** Consider local clarification, lower-authority candidate output, uncertainty marking, or correction of the affected claim instead of rejecting an otherwise useful complete analysis for a non-material wording ambiguity. Do not automatically promote a genuinely unsupported mandatory employer requirement or let uncertain candidate claims silently enter authoritative Market prevalence or personal-readiness conclusions.

### What is and is not established

**Established:** The source's reliable-product wording is a capability expectation; the generated concept is potentially ambiguous; capability and relevant experience can overlap; the observed v22 output lacked separately stated preferred proof-of-work evidence; v22 review rejected the full candidate and I7 remains HOLD.

**Not yet established:** Whether the generated phrase actually causes a harmful user-facing or downstream claim in present code; whether the v22 result could have been safely accepted under the current v5 factual-substrate contract; whether whole-analysis rejection is mandated by an invariant or is an over-broad review policy; whether a lexical guard can safely distinguish material false claims from benign shorthand; whether selective repair/provisional display is feasible without changing authority semantics.

### Questions to resolve before implementation

- Where is `concept` shown or consumed across job detail, review, Capability, and Market? Does `concept_type` change its meaning or downstream treatment?
- Which source-backed distinctions are required for P1.6 factual claims versus allowed only in an explicitly inferred/candidate analytical layer?
- What constitutes a **material** unsupported claim: false mandatory condition, unsupported prior-employment assertion, harmless compressed label, or uncertain implication? Which cases merit item correction, partial display, or whole-result rejection?
- Can one problematic item be isolated without silently losing source coverage, obligation strength, evidence, or accepted-current integrity? What does a useful non-promoted result look like?
- How should explicit preferred work-sample/project proof be covered without misclassifying later application-submission instructions as job qualifications?
- What representative cases, user-facing inspections, and non-regression checks are sufficient before any versioned design/implementation decision?

**Provisional direction:** Preserve explicit source truth and consequence-sensitive validation; revisit over-strict *classification, wording review, and whole-result failure granularity* rather than simply deleting guards. No particular code change, new contract, validator weakening, live generation, or I7 acceptance is decided here.

## Discussion ledger

| ID | Topic | Status | Next discussion |
| --- | --- | --- | --- |
| R01 | Capability ↔ experience ↔ demonstrable work overlap; ambiguous concept-label materiality; whole-analysis rejection | First discussion recorded; refinement proposals OPEN | Determine actual downstream consequences and the right claim/authority boundary |
| R02+ | Additional strictness, failure, coverage, model, planner, and utility issues | NOT YET DISCUSSED | Add separate source-backed entries as the discussion continues |

## Change authorization boundary

Keep this file as the active place to append discussion findings and explicit decisions. Do not modify prompts, source, tests, validators, accepted artifacts, Market state, controlling governance/plans, or run the model solely on this record's proposals. When we finish issue review, separately agree on prioritized refinements, owning layers, versioning, tests, and any bounded evaluation authorization under the controlling repository rules.
