# R05 — Proportional item-level review and partial utility

**Date:** 2026-09-24  
**Status:** USER-AGREED DESIGN DIRECTION / DISCUSSION ONLY — NOT AN IMPLEMENTATION OR ACCEPTANCE DECISION  
**Discussion owner:** [P1.6 semantic strictness and utility refinements — active discussion](2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md), following R01–R04. This companion note preserves the R05 decisions without superseding that active record or the controlling repository instructions.

## Agreed direction

A semantic problem affecting one extracted item should not automatically make otherwise useful, source-backed analysis unavailable. Distinguish **what a concept means** (`concept_type`: skill, experience, knowledge, other, etc.) from **whether and how an extracted claim may be used** (review status and authority). Moving an uncertain item into `concept_type=other` is not sufficient if its wording still makes an unsupported claim.

The proposed item-level handling categories are:

- **Supported claim:** its exact source supports the represented claim and qualifiers; retain its provenance and make it available under the applicable existing authority rules.
- **Needs clarification:** useful source-related item whose standalone wording, typing, scope, or implied obligation is ambiguous; preserve it as a reviewable candidate with its exact source and keep uncertain interpretations out of authoritative conclusions until resolved.
- **Unsupported claim:** its employer-facing assertion is not established by the source; do not present that assertion as employer fact or silently promote it, while retaining review evidence and considering a justified correction.
- **Coverage gap:** an employer statement not extracted at all; track and address it separately. Reclassifying the extracted items cannot restore missing source information.

A partially useful **candidate-level view** and a **complete accepted factual artifact** are distinct states. R05 does not authorize partial or unresolved items to enter accepted-current P1.6, authoritative Market aggregation, personal-readiness determinations, or other high-authority consumers. Preserve explicit source evidence, obligation strength, depth, provenance and the R03 grouping / R04 proof-of-ability distinctions.

## Concrete `tvMm` motivation

The isolated v22 result contains one disputed concept label, `Agent reliability in real product experience`, whose `concept_type` was changed from `experience` to `other` without changing its wording. The exact employer sentence expresses the capability to turn an Agent into a reliable system in a real product. Its materiality and safe presentation remain open for review; do not presume either that the label proves paid prior production work or that every use of it is harmless. Separately, the preferred prior-Agent demonstration and project/repository/demo proof is a *missing source-coverage item*, not a reason to erase the other recorded requirements and responsibilities. Evidence: [fixed v22 evaluation input/raw responses/validated output](https://github.com/motafegh/jobhunter/blob/0c656fba8fe65b8ec6fa38a317a62c5301e7ed54/docs/experiments/2026-09-24_p16-v22-tvmm-case-evidence/evaluation-original.json), [post-alias evaluation closure](2026-09-24_P16_V22_POST_ALIAS_EVALUATION_CLOSURE.md), and [active R01–R04 record](2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md).

## Existing implementation boundaries inspected (2026-09-24)

- [Public-current routing](../../src/jobhunter/analysis_current.py) uses English v21/v5; v22 is an isolated, unpromoted candidate. These discussion decisions do not change that.
- [Analysis generation](../../src/jobhunter/analysis_service_v20.py) persists a mechanically validated generation as a **pending artifact** with request/response and analysis. A generation/validation exception instead records a **failed attempt** without persisting a pending analysis artifact; item review alone cannot recover that result.
- [Analysis persistence/review](../../src/jobhunter/analysis_store.py) currently reviews the **whole artifact** as accepted or rejected. It retains rejection evidence/history and protects referenced historical Market snapshot identities. It does not have item-level review statuses.
- [Job-detail UI](../../src/jobhunter/web/templates/job_detail.html) already exposes pending claims and source excerpts with a pending notice, but its review action accepts or rejects the whole artifact. Extend this candidate-inspection capability rather than duplicating it.
- [Capability input](../../src/jobhunter/capability_service_v8.py) requires accepted P1.6; [Market I5](../../src/jobhunter/market_aggregate_service.py) uses accepted semantic core postings for factual requirement statistics and groups claims per normalized concept **once per posting**, retaining supporting source-claim indexes. Do not assert that raw repeated statements are currently counted five times as five postings. [Capability v9](../../src/jobhunter/capability_service_v9.py) already provides broad capability grouping for accepted inputs; examine reuse before designing separate R03 grouping.

**Design implication agreed:** preserve original generated claims and evidence; add separately traceable item-review annotations and, where justified, proposed source-backed corrections. Keep item classifications apart from `concept_type` and from whole-artifact review. Candidate display must explicitly label unpromoted/uncertain material; complete artifact acceptance and downstream promotion remain distinct. This is a design direction, not a choice of storage schema, validator change, or approval of any specific correction.

## Additional agreed requirement — diagnostic preservation for structurally invalid generations

**User agreement (2026-09-24):** Do not lose potentially useful diagnostic evidence merely because an output fails structural validation. Design an inspectable **diagnostic path distinct from pending P1.6 analysis and item-level semantic review**, with at least these cases:

1. **Mechanically valid generation:** retain an ordinary pending candidate for item/whole-artifact semantic review under the existing authority rules.
2. **Response received but structure/contract validation failed:** retain an explicitly non-authoritative, local diagnostic record with the *available* original model response, validation error(s), and relevant input, source/projection, model, prompt and schema identities needed to reproduce or investigate the defect. Show any inspectable fragments as diagnostic evidence, never as accepted employer claims. Preserve original bytes/content where available; no silent repair, invented missing fields, or automatic conversion into a pending artifact.
3. **Provider/inference failure before a usable response:** retain attempt metadata and available operational error information without asserting that a usable generation exists. Diagnostic capture must be best-effort and respect redaction/privacy/security boundaries.

**Authority and privacy:** A diagnostic record is **not** a pending or accepted P1.6 artifact. It must not appear in current/reuse analysis queries, enter Capability, Market semantic aggregation, personal-readiness facts, or public corpus, or mutate previously accepted artifacts and immutable snapshots. Keep the raw response and model-facing inputs local/private by default; do not automatically publish logs, tokens, sensitive headers, private paths or user data. Any derived fix must be separately evidenced, validated, versioned/reviewed and promoted through the existing authorized path. Distinguish captured evidence from unavailable data; neither an incomplete diagnostic nor an item-level annotation proves source coverage completeness.

**Scope boundary:** This is an explicit *design requirement*, not authorization to persist arbitrary invalid JSON in the analysis-artifact table, bypass fail-closed integrity checks, loosen validators, rerun `tvMm`, or implement any new pipeline. Determine the diagnostic record's storage, capture point, retention and redaction, replayability, review UI, and tests only after inspecting current logging/attempt mechanisms and applicable privacy/integrity owners. The concrete `tvMm` v22 direct evaluation is retained separately as an experiment; do not relabel it as an accepted or pending database artifact.

## Open decisions before design or implementation

1. For an ambiguous item with an evidently source-supported alternative wording, when—if ever—may JobHunter correct it deterministically, and when must it retain the original for review? Require an auditable before/after record and source proof.
2. Which errors block item display, whole-artifact promotion, or all downstream use? Identify actual current consumers and authority boundaries before proposing a state machine or schema.
3. How can the system detect and expose omitted requirements without claiming completeness from absence of a detected gap?
4. Which existing candidate/review/acceptance representations already address some of this, to avoid duplicate architecture?
5. For structurally invalid generations, what can reliably be captured at each failure point without compromising privacy or treating malformed output as authoritative? What diagnostics belong in attempts versus a separate local diagnostic store, and how are they inspected and eventually retired?

**No product source, schema, planner, validator, test, current accepted artifact, Market state, or model evaluation is changed or authorized by this discussion note.**