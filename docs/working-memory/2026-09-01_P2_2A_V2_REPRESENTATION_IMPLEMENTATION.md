# P2.2A Job Work Intelligence v2 Representation Implementation

**Status:** IMPLEMENTED / REPOSITORY QUALITY GREEN / REAL-LOCAL ACCEPTANCE NEXT  
**Date:** 2026-09-01  
**Scope:** P2.2A candidate-vs-assembled representation redesign only  
**Controlling design:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`

## 1. Why this increment existed

Repeated `tG9K` and `tmyX` trials established that free-form model prose was useful for grouping and interpretation but did not reliably preserve factual action relationships such as:

```text
partner ... to move models toward production
!=
direct deployment

and

develop and provide ... hardening solutions
!=
direct hardening implementation
```

The approved redesign therefore moved factual action authority out of model-authored summaries and into exact accepted P1.6 work statements assembled by deterministic code.

## 2. Implemented contract identities

```text
persisted Work Intelligence schema: job-work-intelligence-v2
prompt/runtime identity:            job-work-intelligence-v2.0
limited deterministic identity:     jobhunter-deterministic-limited-work-v2
```

Historical v1 artifacts and attempts remain immutable and are not reused as current v2 artifacts.

## 3. Implemented authority split

Model candidate output now owns only bounded interpretation and structured references:

```text
theme label / grouping
relative emphasis
confidence
supporting requirement references
optional grouping rationale
candidate deliverables
candidate role label / alternatives / limitations
```

The persisted final artifact is assembled separately. Each final theme and deliverable contains exact accepted P1.6 work items:

```text
kind: responsibility | role_purpose
index: zero-based accepted P1.6 index
statement: exact accepted P1.6 statement
confidence: copied accepted P1.6 confidence when present
```

The model cannot author or replace that factual statement field.

## 4. Removed v1 action-bearing representation

The v2 persisted representation removes these free-form factual-looking fields:

```text
JobWorkIntelligence.work_summary
WorkTheme.summary
DeliverableCandidate.summary
CandidateRoleInterpretation.summary
```

Optional theme/deliverable rationale remains explicitly JobHunter interpretation.

## 5. Implemented service flow

Current direct-work path:

```text
accepted/current English P1.6
→ indexed factual model input
→ one typed CandidateJobWorkIntelligence generation
→ deterministic reference / full-work coverage / scope validation
→ at most one bounded regeneration only if deterministic guards reject
→ deterministic exact P1.6 work-item assembly
→ assembled artifact exact-statement/currentness validation
→ immutable candidate artifact persistence
→ browser + CLI presentation
```

The dedicated second semantic authority-review model call from v1.3 was removed. Normal valid direct-work generation therefore uses one model call. The bounded post-validation repair path remains at a maximum of two candidate-generation calls.

Requirement-only jobs retain the deterministic `limited` path and still make no model call.

## 6. Reuse/currentness hardening

A current/reused v2 artifact is revalidated against its exact accepted P1.6 dependency before it is returned:

- work-item `kind` must select the correct P1.6 section;
- `index` must exist;
- persisted `statement` must equal the accepted P1.6 statement exactly;
- copied confidence must match the accepted P1.6 confidence representation;
- every accepted responsibility/role-purpose item must remain covered by at least one theme;
- supporting requirement indices must remain valid.

A structurally valid but factually mismatched persisted v2 artifact therefore fails rather than being displayed.

## 7. Browser and CLI

The browser now presents this hierarchy directly:

```text
JobHunter candidate theme
→ Accepted P1.6 work
   → exact statement + responsibility/role-purpose index
→ optional JobHunter interpretation
```

Candidate deliverables use the same accepted-work-support pattern. Candidate role interpretation no longer contains a free-form action-bearing summary.

CLI formatting mirrors the same hierarchy so browser and CLI do not communicate different authority semantics.

Work Intelligence remains local and outside the public-corpus mutation path.

## 8. Regression coverage added/updated

Focused regressions now cover:

- candidate schema requires structured direct-work references;
- empty-section impossible-reference normalization remains bounded;
- scope-intensifier guard runs on model-owned candidate interpretation;
- normal direct-work generation uses one model call;
- bounded semantic repair uses at most one regeneration and no second reviewer;
- exact `tG9K` production-readiness statement is injected unchanged even when the candidate label is stronger;
- exact `tmyX` hardening-related role-purpose statement is injected unchanged;
- final themes do not persist v1 `work_summary`, `summary`, or direct-work index arrays as factual presentation;
- out-of-range and omitted direct-work references fail;
- historical v1 artifact remains readable but is not reused as v2;
- persisted `kind/index/statement` mismatch fails on current-artifact lookup;
- limited-work path remains deterministic and non-fabricating;
- browser and CLI expose exact work separately from interpretation;
- browser Work Intelligence mutation remains outside corpus publication.

## 9. Repository quality evidence

Latest implementation head before this documentation record:

```text
d8e7f5d0a064dcec5e662101eac67d624ff925b1
```

GitHub Actions CI run:

```text
33548003449
quality job: SUCCESS
Ruff: PASS
full pytest: PASS
pytest warnings-as-errors: PASS
```

A prior implementation/test commit (`2bf365ef844dc76bb28f3cbe96758a6ff480359d`) also completed all three quality steps successfully before its workflow was superseded by the later CLI-only push.

No live LM Studio or real local SQLite semantic/product acceptance was performed by this remote implementation session. CI proves repository mechanics/regressions, not real-model usefulness.

## 10. Files changed

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_cli.py
src/jobhunter/web/templates/work_intelligence.html

tests/test_work_intelligence.py
tests/test_work_intelligence_generation_schema.py
tests/test_work_intelligence_empty_section_reference_normalization.py
tests/test_work_intelligence_scope_guard.py
tests/test_work_intelligence_semantic_repair.py
```

No SQL migration was required because artifact payload identity/versioning already lives in the existing immutable JSON artifact store.

## 11. Exact next acceptance sequence

Do not return to prompt/model action-authority experiments.

```text
1. t4qV
   → generate current v2 candidate on the real local accepted P1.6 chain
   → review grouping usefulness + exact-work presentation

2. tmBK
   → verify deterministic limited result and zero invented duties

3. reuse
   → rerun an unchanged current v2 job and prove artifact reuse

4. browser
   → inspect the same real artifacts for fast comprehension and visible fact/interpretation separation

5. CLI
   → confirm the same assembled semantics are shown

6. P2.2A acceptance decision

7. only then decide whether P2.2B has enough demonstrated reuse value to start
```

`tG9K` and `tmyX` already supplied the design-defect evidence. They do not need another model-trial matrix merely to prove the same action-authority problem.

## 12. Stop lines remain

Until P2.2A is accepted:

- do not start P2.2B;
- do not bulk-map responsibilities;
- do not create global responsibility families/archetypes merely to finish P2.2A;
- do not add deterministic verb-equivalence machinery;
- do not revive the second semantic authority-review model pass;
- do not publish Work Intelligence/registry state;
- do not start Market v2 or personal readiness/scoring/recommendations;
- do not reopen P1.6, Capability v9, P2.1, or Blueprint without a separate material defect/evidence trigger.
