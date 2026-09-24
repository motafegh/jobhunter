# R05 — Proportional item-level review and partial utility

**Date:** 2026-09-24  
**Status:** USER-AGREED DESIGN DIRECTION / DISCUSSION ONLY — NOT AN IMPLEMENTATION OR ACCEPTANCE DECISION  
**Discussion owner:** [P1.6 semantic strictness and utility refinements — active discussion](2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md), following R01–R04. This companion note preserves the R05 decision without superseding that active record or the controlling repository instructions.

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

## Open decisions before design or implementation

1. For an ambiguous item with an evidently source-supported alternative wording, when—if ever—may JobHunter correct it deterministically, and when must it retain the original for review? Require an auditable before/after record and source proof.
2. Which errors block item display, whole-artifact promotion, or all downstream use? Identify actual current consumers and authority boundaries before proposing a state machine or schema.
3. How can the system detect and expose omitted requirements without claiming completeness from absence of a detected gap?
4. Which existing candidate/review/acceptance representations already address some of this, to avoid duplicate architecture?

**No product source, schema, planner, validator, test, current accepted artifact, Market state, or model evaluation is changed or authorized by this discussion note.**