# P2.2A `tG9K` Useful Candidate and Action-Authority v1.2 Refinement

**Date:** 2026-08-27  
**Scope:** P2.2A Job Work Intelligence live semantic/product acceptance  
**Status:** `tG9K` v1.1 candidate useful; prompt-level action-authority refinement implemented as v1.2; v1.2 live regeneration pending

## 1. Starting point

The accepted factual dependency remains:

```text
source_job_id:       tG9K
English P1.6:        artifact 36
P1.6 prompt/schema:  job-analysis-english-v20 / job-analysis-v5
responsibilities:    8
role_purpose:        0
```

The preceding empty-role-purpose reference defect was repaired generically and CI-accepted before this generation.

## 2. First successful `tG9K` candidate

Real-local generation under Work Intelligence prompt `job-work-intelligence-v1.1` completed as:

```text
artifact:          4
state:             candidate / sufficient
model:             gemma-4-e2b-it
P1.6 dependency:   artifact 36
themes:            4
```

Candidate summary:

```text
This role involves applying Machine Learning and AI techniques to complex semiconductor
manufacturing data to solve operational challenges, focusing on building, validating, and
deploying robust analytical models within an industrial setting.
```

Themes:

```text
ML Model Development and Validation                         primary / high
Industrial Data Analysis and Feature Engineering           primary / high
MLOps, Pipeline Engineering, and Production Readiness       primary / high
Problem Framing and Collaboration                          supporting / high
```

## 3. Product assessment

The grouping is useful and materially reduces manual synthesis effort across the eight accepted responsibilities.

It successfully separates:

- model construction/validation;
- industrial sensor/metrology analysis and manufacturing analytics;
- pipelines, monitoring, governance, and production-readiness work;
- problem framing/collaboration as a supporting rather than primary theme.

This also resolves the prior product-quality watch that all themes might always become `primary`:

```text
t4qV → 4 primary
tmyX → 4 primary
tG9K → 3 primary + 1 supporting
```

Therefore do **not** add a deterministic quota or forced primary/supporting ratio. The current emphasis field is capable of producing useful differentiation.

## 4. Repeated action-authority issue

The `tG9K` candidate introduced a second independent example of action-strengthening:

```text
accepted responsibility:
Partner with the semiconductor technical lead and engineering to move models toward production.

candidate summary:
focusing on ... deploying robust analytical models
```

The accepted requirements also contain `model deployment`, but requirements are supporting context and may not independently manufacture a duty.

This follows the earlier `tmyX` example:

```text
accepted role purpose: develop and provide ... hardening solutions
candidate summary:     implementing hardening solutions
```

Across two heterogeneous jobs, the pattern is now sufficient to justify a general semantic refinement.

## 5. Decision

Do **not** build a deterministic action-verb equivalence table or validator. Action relation is semantic and context-dependent.

Instead strengthen the model reasoning contract so Work Intelligence must preserve action strength and responsibility relationship from accepted direct-work statements.

The prompt now explicitly states that it must not upgrade advisory, collaborative, transitional, or solution-provision wording into stronger execution/ownership claims. Examples include:

```text
develop/provide
≠ automatically implement

partner to move toward production
≠ automatically deploy or own production deployment
```

Supporting requirements may clarify domain/tools but cannot supply a stronger action verb, ownership claim, or lifecycle stage than direct-work statements establish.

## 6. Versioning

The semantic prompt changed, so reproducibility requires a prompt-identity bump:

```text
contract/schema:  job-work-intelligence-v1
old prompt:       job-work-intelligence-v1.1
current prompt:   job-work-intelligence-v1.2
```

Artifacts generated under v1.1 remain immutable historical candidate evidence. They are not silently rewritten or treated as current under v1.2.

Historical local artifacts at this point:

```text
artifact 2  t4qV  v1.1  previously accepted candidate product anchor
artifact 3  tmyX  v1.1  useful candidate with recorded action-strengthening limitation
artifact 4  tG9K  v1.1  useful candidate; emphasis validated; action-strengthening observed
```

## 7. Implementation / CI evidence

Implementation commit:

```text
eb6a5e6e5ad001eee52b10e1e304e66782772ac2
fix: preserve P2.2A action authority in reasoning
```

The first CI run failed only because an existing regression intentionally hard-coded the prior prompt identity `job-work-intelligence-v1.1`. All other tests passed.

The prompt-identity regression was advanced to v1.2:

```text
58118b69e50a073697c350c80093f7ecefa14fd1
test: advance P2.2A prompt identity expectation
```

Observed CI on that final code/test head:

```text
Ruff                         PASS
full pytest                  PASS — 527 tests
pytest warnings-as-errors    PASS
overall quality job          PASS
```

Do not ask the repository owner to rerun those repository quality gates locally.

## 8. Exact next live action

Pull current `main` and regenerate `tG9K` under v1.2:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Review whether:

1. the useful four-theme compression remains;
2. `Problem Framing and Collaboration` or another appropriate theme remains sensibly supporting rather than forcing all-primary;
3. the summary/theme wording preserves `move models toward production` as collaborative production-readiness work instead of silently turning it into direct deployment ownership;
4. no new source/authority inflation appears.

After `tG9K` v1.2 is understood, rerun `tmyX` to verify the same general action-authority refinement against the earlier `develop/provide → implementing` case. `t4qV` can then be regenerated for current prompt identity without reopening already-resolved scope issues.

## 9. Boundaries

- P2.2A remains open.
- P2.2B is not authorized yet.
- Do not create deterministic action-verb equivalence machinery from these examples.
- Do not add a fixed primary-theme quota.
- Do not publish Work Intelligence.
- Preserve all v1.1 artifacts as historical evidence.
