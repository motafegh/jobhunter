# P2.2A `tG9K` v1.2 Persisted Action Inflation and v1.3 Authority Review

**Date:** 2026-08-27  
**Scope:** P2.2A Job Work Intelligence live semantic/product acceptance  
**Status:** v1.2 prompt-only action-authority refinement proven insufficient; v1.3 semantic authority-review stage implemented and CI-accepted; fresh `tG9K` v1.3 live generation next

## 1. Triggering live result

After the v1.2 prompt refinement and bounded post-validation repair retry were implemented, the real local command:

```bash
python -m jobhunter.work_intelligence_cli generate tG9K
```

completed successfully as:

```text
artifact:          5
state:             candidate / sufficient
model:             gemma-4-e2b-it
P1.6 dependency:   artifact 36
prompt identity:   job-work-intelligence-v1.2
themes:            4
```

The useful grouping remained:

```text
ML Model Development and Validation       primary / high
Data Engineering and Handling             primary / high
Process Analytics and Problem Framing     primary / high
MLOps and Production Readiness             primary / high
```

The result remained materially useful for compressing the eight accepted industrial-ML responsibilities.

## 2. Semantic problem that remained

Artifact 5 summary still said:

```text
building, validating, and deploying Machine Learning/AI models
```

The accepted direct-work responsibility says:

```text
Partner with the semiconductor technical lead and engineering to move models toward production.
```

The accepted requirements include `model deployment`, but requirements are supporting context and may not independently manufacture a stronger duty.

Therefore the exact semantic issue that motivated v1.2 still survived a prompt-only refinement:

```text
collaborate / move toward production
→ direct deploying
```

This is not treated as employer truth and artifact 5 must not be promoted as proof that the employer explicitly assigned deployment ownership.

## 3. Product/architecture conclusion

Prompt-only instruction is not sufficient to reliably preserve action authority with the current local model.

Do **not** respond by creating a deterministic verb-equivalence table such as:

```text
move toward production -> forbid deploy
provide -> forbid implement
```

That would turn a context-dependent semantic relationship into brittle lexical machinery and would conflict with the current utility/epistemic governance direction.

Instead add a dedicated semantic authority-review stage before persistence.

## 4. v1.3 generation pipeline

For jobs with direct accepted work evidence, the current pipeline is now:

```text
accepted/current P1.6
→ structured Work Intelligence generation
→ deterministic reference/coverage validation
→ bounded one-time service-level repair if those guards reject the draft
→ semantic authority review against direct-work statements
→ deterministic reference/coverage/scope validation again
→ persist candidate artifact
```

The authority-review pass is model-semantic rather than a deterministic action-verb classifier.

Its narrow job is to audit:

- action strength;
- ownership relationship;
- lifecycle scope;
- unsupported transfer from requirements/shared evidence.

It is instructed to preserve useful theme boundaries, IDs, emphasis, confidence, and structured references by default and prefer minimal prose rewrites over regrouping.

Examples explicitly encoded in the review instruction include:

```text
develop/provide
!= automatically implement

partner/collaborate to move models toward production
!= automatically deploy models or own production deployment
```

Supporting requirements remain context only.

## 5. Versioning decision

Because the generation pipeline itself changed materially, artifact identity is advanced:

```text
contract/schema:  job-work-intelligence-v1
old prompt:       job-work-intelligence-v1.2
current prompt:   job-work-intelligence-v1.3
```

Existing artifacts remain immutable historical evidence:

```text
artifact 2  t4qV  v1.1
artifact 3  tmyX  v1.1
artifact 4  tG9K  v1.1
artifact 5  tG9K  v1.2
```

They are not silently rewritten or considered current under v1.3.

## 6. Auditability

For a direct-work candidate persisted under v1.3, stored request/raw-response provenance now keeps separate stages:

```text
generation
semantic repair metadata when applicable
authority_review
```

This preserves the original generated draft and final semantic-review response for later diagnosis.

## 7. Regression coverage

Focused regressions now establish:

1. one post-validation scope failure may be repaired once, then still receives authority review;
2. authority review can soften `deploys` to collaborative `move toward production` language without changing the theme ID/emphasis;
3. a second failed deterministic semantic-repair attempt still hard-fails before persistence;
4. normal direct-work generation now uses two model calls: generation + authority review;
5. requirement-only deterministic limited-work behavior still does not call the model;
6. prompt identity is v1.3 while schema remains v1.

The first full CI run after adding the stage had one expected stale assertion (`provider.calls == 1`); all other 529 tests passed. That assertion was advanced to two calls.

Final code/test head:

```text
086349e6e42b6a7a5ccf2def4595a3552efc33f0
```

Observed final CI:

```text
Ruff                         PASS
full pytest                  PASS — 530 tests
pytest warnings-as-errors    PASS
overall quality job          PASS
```

Do not ask the repository owner to rerun these repository gates locally.

## 8. Exact next live action

Pull current `main` and regenerate `tG9K` under v1.3:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Review whether the persisted/output candidate:

1. keeps the useful industrial-ML grouping;
2. no longer upgrades collaborative production-readiness work into direct model deployment ownership;
3. avoids unsupported lifecycle/scope language;
4. remains faster and clearer than manually synthesizing all eight responsibilities.

If v1.3 succeeds on `tG9K`, use `tmyX` next as the independent earlier `develop/provide -> implementing` action-strengthening case. Then regenerate `t4qV` for current prompt identity before moving to `tmBK`, reuse, browser UX, and P2.2A closure.

## 9. Boundaries

- Artifact 5 is useful historical v1.2 candidate evidence, not current v1.3 output.
- P2.2A remains open.
- P2.2B is not authorized yet.
- Do not create deterministic action-verb equivalence machinery.
- Do not add a fixed primary-theme quota; `tG9K` v1.1 already showed the emphasis field can produce supporting themes.
- Do not publish Work Intelligence.
