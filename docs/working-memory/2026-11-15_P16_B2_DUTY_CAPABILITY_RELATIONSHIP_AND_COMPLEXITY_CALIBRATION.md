# Stage B2 decision — retain duty/capability relationships without over-constraining inference

**Date:** 2026-11-15
**Disposition:** Approved planning refinement for B2; **not** B2 implementation or a new accepted product contract
**Parent:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`
**Baseline:** `main` at `a758952aa2a7e90ed63312dc228327c89df5039f` (B1 design complete)
**Authority:** Existing `docs/DOMAIN_AND_ANALYSIS_MODEL.md` sections 6.1–6.6 and 7.3–7.4 and `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md` sections 3, 6–7, 12–13 already recognize work-implied capabilities and calibrated uncertainty

## Why this clarification matters

Duties, qualifications and underlying operational capabilities are often strongly related or partly overlapping. A rigid, mutually exclusive interpretation that prevents duty-derived capability reasoning loses useful intelligence. Conversely, collapsing an assigned task into a *previous professional experience required* claim fabricates employer eligibility policy. Both errors harm job comprehension and eventual candidate-readiness recommendations.

The right separation is **evidence authority**, not a prohibition on relationships:

1. **Employer-stated fact:** the advertisement assigns developing LLM features; the employer explicitly does or does not require prior LLM familiarity.
2. **Work-implied capability candidate:** developing LLM applications normally calls for relevant LLM application-development ability. This is an analytical inference *linked* to the assigned work, **not** a newly employer-stated prior-experience requirement.
3. **Candidate evidence/readiness, later:** personal work, open-source contributions, employment and project evidence can establish varying levels of ability. Lacking previous paid LLM employment is not itself formal disqualification; lacking demonstrated ability may be an important readiness gap. Neither individual fit nor a rigid eligibility score is implemented in B2.

A duty may overlap qualification concepts, carry shared wording or support multiple plausible capability relations. Categories are not a rule that suppresses such meaning; they prevent source-authority conflation. The broader domain already has `source_explicit`, `strongly_implied_by_work`, `model_inferred_prerequisite` and `unknown_or_unsupported`. Reuse those conceptual evidence levels later; do **not** immediately force a new B1 JSON enum/schema or a universal skill ontology into B2.

## Minimal and flexible engineering application

- **B2 core:** identify exact source items, preserve employer modality, headings, arrangements, eligibility alternatives and metadata provenance. Allow overlapping/compound source spans where legitimate. Keep source item category separate from optional, linked *work-implied capability* hints; do not silently write the hint into employer `required` fields.
- **B2 optional candidate link:** if a duty naturally supports a capability, preserve a bounded, evidence-linked interpretation (or defer that relation to B4); it may be probabilistic and should carry uncertainty. It is **not** a new mandatory item field or required extraction coverage count.
- **No technology explosion:** `develop LLM applications` can imply LLM application engineering; it cannot by itself impose LangChain, LangGraph, Kubernetes, a specific vector database, a professional-years threshold, or independent senior ownership.
- **No artificial rigidity:** do not force exclusive role-purpose/duty/qualification semantics when one phrase legitimately serves more than one function. Preserve the original and a reasonable interpretation; use `unresolved` only for material uncertainty, not every plausible cross-category relationship.
- **Do not turn this into a prompt checklist:** prefer the model interpreting a coherent, sufficiently intact job-context passage with a short instruction to distinguish employer wording from inference; avoid multiplying mandatory labels, huge per-case rules, repetitive tool-specific regexes, validation retries and postprocessing that strips meaningful relationships.
- **Deterministic hard checks remain narrow:** protect hashes, exact provenance, stale currentness, invalid source offsets, metadata origin and false factual promotion. A plausible source-bound inferred capability is *not* a fatal employer-fact integrity error when clearly labeled; a fabricated employer-stated mandatory qualification is.
- **Keep cost bounded:** reuse the accepted sidecar/Stage A anchors; no immediate B1 schema change, new canonical taxonomy, database migration, additional model-call phase, individual readiness score, or UI rollout. Introduce any new contract fields *only* after measured need and a separately justified gate.

## Diagnostic examples and expected behavior

| Source situation | Useful candidate behavior | Wrong behavior |
| --- | --- | --- |
| Duties include developing LLM products; prior LLM familiarity is explicitly optional (`tNhZ`) | Duty preserved; LLM engineering capability is relevant/possibly strongly work-implied; prior familiarity remains preferred or nonmandatory as originally stated | Delete LLM capability relevance because it was not in requirements; or auto-promote prior professional experience to employer-required |
| Job lists specific tasks requiring Python but no separate Python requirement | Link the work to Python implementation capability when adequately supported; exact employer requirement stays not established | Declare no relevant Python skill, or invent mandatory years of paid Python employment |
| Duty mentions an LLM implementation without naming frameworks | Do not assume any named LLM framework is employer-required | Automatically demand LangChain, LangGraph, fine-tuning, Kubernetes and a vector database |
| Applicant `can use OWASP methods` but duty scope is unspecified (`tMjm`) | Qualification is present and relevant; do not invent exact day-to-day penetration-testing engagements | Manufacture operational duty list or claim the posting needs no capability |
| A combined clause mixes assigned work, desired experience and employment conditions | Keep its intact source context and disambiguate only where grounded; mark specific unclear parts unresolved | Fragment and force exclusive roles until meaning is lost |
| Explicit employer experience requirement vs portfolio/personal project | Preserve the employer's *actual* eligibility condition; consider project work as potential capability evidence only in a later qualified personal-assessment stage | Rewrite employer's formal years requirement or automatically reject a capable applicant based on invented policy |

## Calibrated acceptance, not a new rigid gate

B2 must test both **false promotion** (unsupported mandatory requirements, fabricated assignments) **and false suppression** (useful capabilities or intertwined duty/qualification context lost through over-separation). Review source correctness, coverage and understandable partial results together; count abstentions and relevant omissions, not just schema compliance. A prompt/heuristic expansion is justified only if it improves these outcomes at acceptable time, complexity and failure rates on the exposed cases and generalized counterexamples. B5 will provide genuinely fresh, independently assessed cases; four exposed postings cannot prove generalization.

B2 remains the source-item/metadata **candidate** gate. B3 retains bilingual meaning responsibility. B4 can synthesize compact operational capability links and job understanding; later Capability/personal-readiness stages can evaluate project-versus-employment evidence. B6 alone authorizes durable product promotion.

**Implementation instruction:** prefer one simple candidate approach and at most one evidence-justified corrective revision. If extra constraints reduce completeness, contextual understanding or model success, **simplify/remove the constraints** rather than assuming more strictness must be better. No owner per-ad review is necessary by default.
