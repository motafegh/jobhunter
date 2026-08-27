# P2.2A `tG9K` v1.3 2B Authority Review Insufficient and 4B Model-Role Trial

**Date:** 2026-08-27  
**Scope:** P2.2A Job Work Intelligence real-local semantic/product acceptance  
**Status:** `tG9K` artifact 6 useful but not accepted as current semantic anchor; Work Intelligence runtime moved from Capability 2B model to Analysis 4B model for the next controlled live trial

## 1. Starting point

Current factual dependency remains:

```text
source_job_id:       tG9K
English P1.6:        artifact 36
P1.6 prompt/schema:  job-analysis-english-v20 / job-analysis-v5
responsibilities:    8
role_purpose:        0
```

P2.2A contract/schema remains:

```text
job-work-intelligence-v1
```

Prompt/pipeline identity remains:

```text
job-work-intelligence-v1.3
```

v1.3 added a final semantic authority-review pass after generation and deterministic reference/scope validation.

## 2. Real-local v1.3 result: artifact 6

The owner regenerated `tG9K` after the v1.3 authority-review implementation.

Observed result:

```text
artifact:          6
state:             candidate / sufficient
model:             gemma-4-e2b-it
P1.6 dependency:   artifact 36
themes:            3
```

The grouping was useful:

```text
ML Model Development and Data Foundation
Industrial Analytics and Problem Framing
MLOps and Production Readiness
```

The result still materially reduced manual synthesis effort across the eight responsibilities.

## 3. Remaining authority defect

The final persisted summary still said:

```text
building, validating, and deploying Machine Learning/AI models
```

and later:

```text
... governance of the resulting models for production deployment
```

The accepted direct-work statement remains weaker:

```text
Partner with the semiconductor technical lead and engineering to move models toward production.
```

A supporting requirement includes deployment context, but requirements cannot independently turn collaborative production-readiness work into direct deployment ownership.

Therefore artifact 6 is useful analytical evidence but is **not accepted as the current semantic anchor** for the action-authority boundary.

## 4. What artifact 6 proves

The v1.3 wiring itself is not missing evidence:

- the authority reviewer receives indexed accepted responsibilities;
- it receives role-purpose and supporting requirements;
- it receives the full candidate document;
- it runs before persistence;
- deterministic reference and unsupported-scope validation runs after the review.

The failure is therefore not a missing-review-call or missing-evidence bug.

The review contract asked the same `gemma-4-e2b-it` model that generated the candidate to audit and rewrite its own valid-looking structured document. Real-local evidence shows this smaller model can preserve the same action-strength inflation despite explicit review instructions.

## 5. Decision: test model adequacy before adding protocol complexity

Tracked project configuration already distinguishes model roles:

```text
analysis_lm_studio_model    = gemma-4-e4b-it-ud
capability_lm_studio_model  = gemma-4-e2b-it
```

P2.2A had initially reused the Capability model to avoid premature configuration expansion.

That assumption is now challenged by real-local evidence. The 2B model provides useful grouping, but repeated action-authority preservation has been insufficient even with the v1.3 review stage.

The smallest evidence-backed next change is therefore:

```text
P2.2A generation + authority review
→ use the stronger existing analysis reasoning model
→ gemma-4-e4b-it-ud
```

No new configuration field is introduced yet.

## 6. Why no prompt-version bump is required

Work Intelligence artifact identity already includes the concrete model plus prompt/schema identity:

```text
analysis_artifact_id
model
prompt_version
schema_version
```

Therefore changing:

```text
gemma-4-e2b-it
→ gemma-4-e4b-it-ud
```

already produces a distinct artifact/currentness identity.

The semantic prompt itself remains v1.3. Artifact 6 stays immutable historical evidence and cannot be reused as the current 4B result.

## 7. Implementation and regression

Implementation commit:

```text
27c2484e15b09d45a8e5749ada09932435b3e1a6
fix: route P2.2A through analysis reasoning model
```

Focused regression commit:

```text
db17ce0d94c416e5ae78afe693a7fe82b9692419
test: lock P2.2A analysis-model routing
```

The regression configures distinct analysis/capability models and verifies that `build_work_intelligence_service()` selects the analysis model for Work Intelligence.

Observed CI on the exact regression head:

```text
Ruff                         PASS
full pytest                  PASS
pytest warnings-as-errors    PASS
overall quality job          PASS
```

Do not ask the repository owner to rerun those repository quality gates locally.

## 8. Controlled escalation rule

Do **not** immediately add a deterministic verb blacklist or action-equivalence table.

Do **not** immediately add another prompt-only patch.

Run one controlled real `tG9K` trial using the stronger 4B analysis model while keeping the v1.3 contract/prompt/evidence fixed.

If the 4B trial preserves useful grouping and removes unsupported direct-deployment wording, keep the simpler architecture and continue acceptance.

If the 4B trial still preserves material action-authority inflation, that becomes sufficient evidence for the next architecture step:

```text
candidate generation
→ explicit structured semantic authority verdict
→ targeted correction only when verdict = revise
→ deterministic provenance/scope validation
→ persistence
```

That future review protocol should remain semantic; do not replace it with a deterministic action-verb taxonomy.

## 9. Exact next action

On the owner's local environment:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Expected model line for a newly generated current artifact:

```text
Model: gemma-4-e4b-it-ud
```

Review specifically whether:

1. the useful industrial-ML grouping remains;
2. direct `deploying models` ownership is removed unless direct work actually establishes it;
3. production-readiness collaboration remains represented;
4. no unsupported lifecycle/scope inflation appears;
5. output remains faster to understand than the eight raw responsibilities.

## 10. Current boundaries

- P2.2A remains open.
- Artifact 6 is historical useful-but-not-accepted v1.3/2B evidence.
- Do not start P2.2B.
- Do not publish Work Intelligence.
- Do not rerun closed Phase-1/P2.1 gates.
- Do not add deterministic action-verb equivalence machinery.
