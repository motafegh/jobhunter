# Long-posting extraction and evidence-reference failure

**Date:** 2026-08-06  
**Representative job:** Jobinja `tG9K`  
**Status:** Corrective implementation added; deterministic/live acceptance pending

## Symptom

A detailed semiconductor AI/ML posting produced an accepted English P1.6 artifact with:

```text
Responsibilities: 0
Requirements: 0
```

despite explicit sections describing model development, yield/process control, sensor/time-series
work, validation/monitoring, productionization, Python/SQL, ML frameworks, statistics, fab data
systems, MLOps, and cloud/edge work.

Capability Intelligence then reasoned over the complete English fields but failed validation after
citing invented references such as:

```text
field:skills:6
field:skills:7
field:skills:8
field:skills:9
```

The source `skills` list had only six items (`0..5`). The additional concepts lived inside one long
bullet-heavy `description` field.

## Root causes

### 1. Empty P1.6 was structurally valid

The P1.6 schema permits empty responsibility/requirement arrays. There was no source-richness guard,
so a semantically absurd empty extraction could still be accepted and persisted.

### 2. P1.6 still made the model copy exact evidence

For long postings, exact quotation bookkeeping increases model burden and can encourage overly
conservative/empty extraction. Exact evidence is a deterministic provenance concern; the model
should select a stable reference while JobHunter resolves it to source text.

### 3. Capability evidence references were too coarse for long descriptions

The v2 catalog exposed the entire description as `field:description` but did not expose its bullet
segments with text. The model attempted to create finer references by extending the unrelated
`field:skills:N` pattern.

## Correction

### Shared evidence-reference catalog

`src/jobhunter/evidence_refs.py` now creates:

- exact field/list references such as `field:skills:0`;
- deterministic segment references for bullet/newline-heavy text such as
  `field:description:segment:4`;
- a model-facing reference payload containing both the ID and exact text.

### English/original semantic analysis v3

The prompt identity moves to:

```text
job-analysis-english-v3
job-analysis-original-v3
```

The persisted analysis schema remains `job-analysis-v2`; only the inference/evidence-selection
contract changes.

Production Instructor analysis now:

1. builds the deterministic field evidence catalog;
2. gives the model the allowed IDs plus exact referenced text;
3. accepts evidence IDs internally;
4. resolves IDs back to exact source excerpts in Pydantic validation;
5. persists the same exact-evidence artifact shape as before;
6. rejects a completely empty responsibilities+requirements result when the selected source is
   clearly information-rich, allowing the one bounded Instructor correction attempt;
7. keeps connection establishment bounded but has no read deadline for a healthy local generation;
8. disables transport-level replay of a long generation.

### Capability prompt v3 / schema v2

Capability Intelligence keeps the v2 typed schema but advances the prompt identity to
`job-capability-intelligence-v3`. It now receives the detailed reference catalog with exact text and
is instructed to prefer specific description-segment references rather than inventing indexes.

## Permanent lessons

1. Analysis depth should scale with source evidence density, but a rich source may never silently
   collapse to an empty accepted extraction.
2. Exact evidence text belongs to deterministic provenance handling, not model transcription.
3. Long structured text needs addressable evidence segments; one giant field reference is too
   coarse for reliable model bookkeeping.
4. List reference indexes must come only from actual source list structure. Concepts inside prose
   do not create synthetic `field:skills:N` items.
5. Prompt/schema identity must change when inference semantics change so stale artifacts are not
   silently reused.
6. Long local inference should be bounded by connection/output limits rather than an arbitrary
   read-time ceiling.
