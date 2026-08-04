# Decision: Separate Expert Role Blueprint from Auditable Capability Intelligence

**Date:** 2026-08-04  
**Status:** Active

## Context

Live review of Capability Intelligence showed that its output was useful for machine-readable reasoning but not sufficient as the primary human experience. It correctly preserved evidence status, confidence, rationale and exact source anchors, yet still read like an analytical database report.

The desired user experience is different: a senior engineer/domain specialist should read the entire vacancy and explain what the person probably needs to know and do, including useful sub-skills, likely implementation patterns, plausible tools/examples, expected practical depth, hidden operational concerns and realistic end-to-end work that the advertisement may not spell out.

## Decision

Keep three separate contracts:

```text
Strict English extraction
    -> employer facts / truth substrate

Capability Intelligence
    -> auditable machine-facing reasoning

Role Capability Blueprint
    -> freer expert human-facing interpretation
```

Do not merge these layers.

## Why Capability Intelligence stays

Its evidence-qualified structure is useful for:

- provenance;
- later canonicalization;
- aggregation;
- confidence-aware machine comparisons;
- market statistics;
- debugging analytical claims.

Removing its constraints would damage those uses.

## Why the Blueprint is freer

The user needs answers such as:

- "Python is mentioned, but which parts probably matter here?"
- "How deeply would I likely need to use AI APIs?"
- "What could n8n/Make/Zapier imply about actual workflows?"
- "What systems would this person probably be expected to build or debug?"
- "Which libraries/frameworks are sensible examples even though the employer did not name them?"
- "What hidden reliability/security/data-quality concerns follow from the actual work?"
- "What broad-domain topics probably do not matter for this vacancy?"

These questions require professional inference beyond exact source wording.

## Permanent rules

1. The Blueprint may infer; it must not pretend inference is employer fact.
2. The Blueprint does not require exact evidence quotes per statement.
3. Capability Intelligence is input context, not an authoritative decomposition the Blueprint must repeat.
4. Whole-job combinations matter more than isolated keyword expansion.
5. Tool/library suggestions are examples unless source-named.
6. Avoid generic technology curricula.
7. Avoid trivial statements that merely repeat the advertisement.
8. Use `highly_likely`, `plausible`, and `speculative` to communicate interpretation strength.
9. Keep only operational bounds on calls/output size; do not constrain professional reasoning to audit rules.
10. Live semantic quality must be reviewed before any bulk/corpus-wide rollout.

## Rabbit holes this prevents

Do not respond to shallow human-facing output by:

- loosening strict extraction evidence rules;
- adding more evidence fields to the human explanation;
- forcing every inference through exact-quote validation;
- asking the model to restate its Capability Intelligence artifact in prettier prose;
- adding broad technology checklists that ignore the actual role context;
- assuming a structurally valid model response is professionally useful.

## Model-quality note

The first implementation intentionally reuses the configured analysis model so the contract change can be evaluated independently. If the Blueprint remains shallow, compare a stronger model on the **same vacancy and same prompt/schema** before adding more prompt patches.
