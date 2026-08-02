# JobHunter Evidence, Provenance, Review, and Trust Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B007-B010, B086-B092, B184

---

## Purpose

This family focuses on the quality and inspectability of JobHunter's conclusions. The product already treats source evidence, translations, semantic analysis, human workflow state, and market aggregates as different authority layers. These proposals extend that discipline into richer provenance, review, contradiction handling, uncertainty, and reversible corrections.

---

## B007 — Field-level provenance

**Intent:** Make every important extracted or derived field answer “where did this come from?”

**Proposal:** Persist or reconstruct provenance for material values such as requirements, responsibilities, concepts, and later gap/recommendation claims. A visible `Python — required` claim should be traceable to exact employer evidence, source version, analysis contract, and any canonical mapping used afterward.

**Design direction:**

```text
claim
- value / classification
- source_job_id
- source semantic version
- original evidence field + excerpt
- derived artifact identity
- model / prompt / schema when applicable
- canonical mapping identity when applicable
```

**Guardrails:** Avoid duplicating large source text across every row when durable references and excerpts are sufficient. Provenance must reflect real derivation, not a decorative citation added after the fact.

**Promotion signal:** Extend incrementally whenever a new durable derived layer is introduced.

---

## B008 — Evidence Inspector

**Intent:** Give users and developers a single way to walk from a high-level conclusion back to raw evidence.

**Proposal:** Add an interactive Evidence Inspector capable of traversing chains such as:

```text
recommendation
→ gap
→ personal capability
→ market requirement
→ job analysis
→ exact employer excerpt
→ original evidence object
```

The same surface could work for market aggregates and personal claims.

**Design direction:** Begin with simple linked pages/breadcrumbs rather than a graph UI. Each hop should display authority class, artifact/version identity, and whether the link is deterministic, human-reviewed, or model-derived.

**Guardrails:** The inspector must not synthesize missing lineage. If a conclusion lacks a required provenance link, show that as a quality defect.

**Promotion signal:** Once Phase 2/3 introduce conclusions spanning several durable layers.

---

## B009 — Claim-level analysis quality review

**Intent:** Allow human correction of semantic analysis without discarding entire artifacts or silently editing model history.

**Proposal:** Add review state at the individual claim level, for example:

```text
unreviewed
accepted
corrected
rejected
uncertain
```

A correction would preserve the original model output and add a reviewed interpretation with reason/provenance.

**Design direction:**

- review responsibilities and requirements independently;
- allow correction of type, strength, concept mapping, or evidence association;
- record reviewer action and timestamp;
- keep source text immutable;
- allow aggregate market views to choose an explicit policy: accepted model claims, reviewed claims, or both with labels.

**Guardrails:** Human review is not automatically infallible. Corrections should remain reversible and auditable.

**Promotion signal:** After the first P1.6 live batch demonstrates recurring errors worth correcting rather than merely rejecting.

---

## B010 — Active-learning review queue

**Intent:** Spend scarce human review effort on the cases most likely to improve quality.

**Proposal:** Prioritize review items using observable uncertainty signals such as low confidence, evidence-validator edge cases, new/unmapped concepts, model disagreement, unusual requirement-strength classifications, high-impact common concepts, or translation-integrity suspicion.

**Design direction:**

- deterministic quality signals should drive priority where possible;
- models may propose uncertainty but cannot be the only source;
- review priority is operational workflow, not source truth;
- capture review outcomes so future evaluation can determine whether the queue actually surfaces useful cases.

**Guardrails:** Avoid a self-reinforcing model where the same model both creates and exclusively decides uncertainty. Keep a random/control sample for quality measurement.

**Promotion signal:** When review volume becomes large enough that reviewing everything is no longer practical.

---

## B086 — Data Quality Cockpit

**Intent:** Provide one operational surface for data/inference integrity problems.

**Proposal:** Add a future Data Quality page summarizing actionable states such as parser failures, partial parses, translation rejection, stale artifacts, evidence-validation failures, unreviewed semantic claims, unknown canonical concepts, duplicate uncertainty, and source drift warnings.

**Design direction:** Each metric should link to affected records and expose denominator/sample size. Quality defects should be grouped by layer rather than collapsed into one score.

**Guardrails:** Do not invent a single “data quality percentage” that hides different failure modes. Health summaries may exist, but underlying counts/states remain visible.

**Promotion signal:** As soon as operational quality issues span enough pages that diagnosing them manually becomes cumbersome.

---

## B087 — Corpus health summary

**Intent:** Give an immediate, honest picture of how much of the corpus is actually ready for each analytical layer.

**Proposal:** Display pipeline coverage such as:

```text
273 discovered
210 detail-fetched
198 parsed/current
176 English-v2 current
84 analyzed with current contract
22 human-reviewed
7 taxonomy uncertainties
```

**Design direction:** Use exact current-contract definitions for each count. Allow drill-down into missing/stale/failed records.

**Guardrails:** Coverage is not quality. `84 analyzed` says nothing by itself about analysis correctness; keep it separate from review/evaluation metrics.

**Promotion signal:** Near-term candidate because the underlying counts already exist or can be derived from current stores.

---

## B088 — Provenance coverage metric

**Intent:** Measure whether derived claims can actually be traced to their required evidence.

**Proposal:** Define layer-specific provenance coverage rather than a vague global number. Examples:

- percentage of accepted P1.6 claims with validated source excerpts;
- percentage of canonical mappings linked to their originating claims;
- percentage of recommendations linked to market and personal evidence.

**Design direction:** The denominator and exact contract must always be shown. Missing provenance should create a concrete quality issue.

**Guardrails:** Never count the presence of a generic artifact ID as sufficient provenance if the layer requires claim-level evidence.

**Promotion signal:** Introduce alongside each new authority transition, not as a late reporting afterthought.

---

## B089 — Uncertainty-first UI vocabulary

**Intent:** Prevent the interface from presenting incomplete or model-derived information as certainty.

**Proposal:** Standardize visible states such as:

```text
known / source-explicit
reviewed derived
inferred
uncertain
missing
conflicting
stale
```

These labels can appear on requirements, role classifications, personal capabilities, gaps, and recommendations.

**Design direction:** Use a small consistent vocabulary with tooltips/explanations. Visual styling should reinforce authority without making uncertain information unusable.

**Guardrails:** Confidence percentages should not substitute for semantic state unless calibrated evidence justifies them.

**Promotion signal:** Can be introduced gradually as more derived intelligence enters the UI.

---

## B090 — Cross-field contradiction detection

**Intent:** Surface internally inconsistent job advertisements instead of forcing JobHunter to choose one interpretation.

**Proposal:** Detect contradictions such as a `Junior` title paired with senior ownership/experience expectations, or a `remote` headline paired with mandatory frequent office presence.

**Design direction:** Use deterministic rules for direct field conflicts and semantic analysis for nuanced conflicts. Store a contradiction artifact containing both supporting excerpts and a category, with optional human review.

**Guardrails:** Do not label an employer deceptive merely because wording is inconsistent. The output is `conflicting signals`, not a motive judgment.

**Promotion signal:** After role/seniority/work-mode semantics are normalized well enough to compare them.

---

## B091 — Requirement contradiction detector

**Intent:** Detect contradictions specifically within qualification/requirement language.

**Proposal:** Flag examples such as `no previous experience required` alongside `3+ years production Python required`, or one field marking a technology optional while another explicitly requires it.

**Design direction:** Preserve each statement independently and attach the contradiction relation. The system should avoid resolving the contradiction unless a deterministic precedence rule is justified.

**Guardrails:** Repeated wording or nuanced conditions can look contradictory out of context; every finding requires exact excerpts.

**Promotion signal:** After accepted semantic requirement extraction is stable.

---

## B092 — Suspicious-posting risk indicators

**Intent:** Help the user notice potentially risky or low-quality postings without making unsupported fraud accusations.

**Proposal:** Define bounded risk indicators such as malformed company identity, repeated spam-like duplicates, unusually vague role/company information, suspicious contact instructions, or clearly inconsistent compensation claims where the source data supports those observations.

**Design direction:** Display individual signals and source evidence. A future aggregate state might be `review recommended`, not `fraud`.

**Guardrails:** No black-box scam score, reputation scraping, or unsupported allegations. Legitimate unusual postings must remain inspectable.

**Promotion signal:** Only after there is evidence that suspicious postings are a real repeated-use problem.

---

## B184 — Reversible intelligence and correction history

**Intent:** Ensure model and human-derived knowledge can be corrected without destroying history.

**Proposal:** Every consequential correction should preserve:

```text
original output/value
replacement or correction
reason
review status
actor/source
created_at
supersedes / reverted_by relation
```

This applies to semantic analysis review, taxonomy mapping, personal evidence interpretation, and later recommendations where durable corrections are stored.

**Design direction:** Prefer append/supersede semantics for durable intelligence. Current views resolve the latest accepted interpretation while historical views remain reproducible.

**Guardrails:** Do not create event-sourcing complexity for ordinary mutable UI preferences that do not need analytical history. Use reversibility where authority or learning value justifies it.

**Promotion signal:** Before human corrections become significant inputs to market/personal intelligence.

---

## Category-level recommendation

Trust is a core differentiator for JobHunter. The near-term priority is not to implement every review surface, but to preserve enough lineage and state now that future corrections, quality metrics, and evidence inspection remain possible without schema reconstruction.