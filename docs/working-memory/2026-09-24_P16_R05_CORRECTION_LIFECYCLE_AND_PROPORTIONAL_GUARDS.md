# R05 — Correction boundary, record lifecycles, and proportional guard review

**Date:** 2026-09-24  
**Status:** USER-AGREED DESIGN DIRECTION / DISCUSSION ONLY — NOT AN IMPLEMENTATION, PROMOTION, OR ACCEPTANCE DECISION  
**Parent:** [Active P1.6 semantic strictness and utility discussion](2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md); [R05 item review and structural-diagnostics decision](2026-09-24_P16_R05_ITEM_LEVEL_REVIEW_DIRECTION.md). These subordinate notes do not supersede repository governance or controlling specifications.

## Agreed correction boundary

Preserve the original model output, claims, and source evidence. Do not overwrite original candidate content or silently substitute a revised claim. A *narrow, demonstrably mechanical* correction (for example harmless formatting or a uniquely provable exact reference reconciliation) may be proposed for deterministic application under an explicit versioned rule with before/after provenance and tests. Changing employer-facing meaning, strength, scope, depth, prior-experience implication, or other material semantics is **not** a mechanical fix: retain the original, attach a distinct proposed source-backed correction, and require an appropriate review/promotion decision. Merely passing structural validation, or changing `concept_type` to `other`, does not authorize a semantic correction or accepted employer-fact status. Unsupported claims remain non-authoritative and missing source statements remain coverage gaps, not silently repaired extracted items.

**`tvMm` example:** Preserve the disputed label `Agent reliability in real product experience`. `Ability to turn an Agent into a reliable system in a real product` may be shown as a separate, source-supported *proposed* capability wording, not as a silently overwritten or automatically accepted replacement. Its review and the omitted preferred prior-Agent demonstration/project evidence are separate issues. Refer to the parent R01–R04 and fixed v22 evaluation linked there.

## Agreed record/lifecycle direction

1. **Generation attempt:** operational outcome and exact available model/prompt/schema/source/projection/dependency identities, with available error information; does not by itself represent an accepted analysis.
2. **Structural-failure diagnostic:** local, non-authoritative available original response, validation stage/errors, source/contract dependencies and inspectable fragments, captured only where actually available. Not a pending P1.6 artifact; never enters analysis-current/reuse, Capability, authoritative Market statistics, public corpus, or other promoted factual consumers. If no usable response was received, retain only actual attempt/error evidence, never invent a response. Define secure storage, redaction and retention before implementation.
3. **Structurally valid candidate analysis:** source-linked generated claims available for clearly marked, bounded job-level inspection even while pending review. Candidate visibility is not factual promotion.
4. **Review record:** separate item findings (supported / needs clarification / unsupported), coverage gaps, original-to-proposed correction links, evidence and reasons, and whole-artifact disposition. Keep `concept_type`, item review status, and artifact acceptance distinct. Materially unresolved items/gaps cannot silently cross the existing complete-artifact acceptance and downstream authority boundary.
5. **Approved correction/revision:** when a correction is approved, preserve a new traceable version/revision and its relationship to the original candidate, rather than editing historical generated claims in place. The concrete revision identity, storage, invalidation, review action, and promotion state machine remain to be designed against existing persistence and immutable Market history.

Do not confuse a diagnostic record with an otherwise valid but semantically disputed pending candidate. Do not change the accepted English v21/v5 public route, promote the isolated v22 candidate, reopen accepted anchors, run further models, or mark Market I7 PASS on this design agreement.

## Cross-project proportional-strictness direction

**User agreement:** When inspecting existing guards and failure modes across JobHunter, proactively identify *evidence-backed* over-strictness that destroys useful output or unnecessarily blocks progress, and refine its design proportionately. This is permission to analyze and propose targeted refinements during this work, **not blanket authorization** to delete guards, modify unrelated modules, change accepted contracts, or relax the current Market I7 acceptance conditions.

For each relevant guard, record: (a) the invariant/risk it protects; (b) the actual failure shape and available real evidence; (c) the affected product surface and its authority/blast radius; (d) whether the issue is corruption/fabricated employer fact versus interpretive uncertainty, bounded incompleteness, or recoverable representation error; (e) the smallest safe action (hard fail, quarantine diagnostic, annotate, lower confidence, show alternatives, propose item correction, or block promotion only); and (f) non-regression tests and a stopping rule. Avoid designing new global machinery where current review, attempt tracking, candidate presentation, or Capability grouping already suffices.

**Keep hard guards** for identity/currentness/provenance violations, invented or unsupported employer facts *when promoted as facts*, privacy/security errors, corrupt persistence, invalid irreversible transitions, inaccurate deterministic counts/denominators, and authoritative downstream contamination. **Prefer soft handling** for qualified semantic ambiguity, incomplete technical scope, benign representational uncertainty, potentially useful non-promoted fragments, and inspectable structural failures when their evidence can be securely retained. Fail-soft does not mean declaring the whole result complete or moving unresolved source coverage into accepted Market prevalence. Strictness scales with the consumer: job-level candidate view < reviewed P1.6 factual substrate < durable Market/Capability decision inputs.

## Next design/verification questions

- Which existing validation stages and provider APIs make original-response diagnostic capture feasible without storing secrets or corrupting accepted analysis tables?
- What exactly counts as uniquely provable mechanical reconciliation versus a meaning-changing proposal, and how is before/after evidence linked?
- What constitutes a materially unresolved item or coverage gap for whole-artifact acceptance, and how are item outcomes represented without treating missing detection as evidence of completeness?
- How do new revisions relate to immutable source versions, translation dependencies, accepted downstream Capability/Registry links and Market snapshots?
- What representative positive/negative real-posting cases show a guard blocks usefulness disproportionally, and what tests preserve its original integrity guarantee?

**No product source, schemas, validators, tests, prompts, accepted artifacts, Market state, or model evaluations were changed by recording these design decisions.**
