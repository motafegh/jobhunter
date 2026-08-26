# P2.2A Job Work Intelligence v1 — Implementation Record

**Status:** IMPLEMENTED / REPOSITORY QUALITY PASS / REAL-LOCAL SEMANTIC ACCEPTANCE PENDING  
**Date:** 2026-08-26  
**Focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Working contract:** `job-work-intelligence-v1`

## 1. What was implemented

P2.2A now has a complete first vertical slice:

```text
accepted/current English P1.6 v20/v5
→ bounded job-level work reasoning
→ deterministic source-index/currentness validation
→ immutable candidate Work Intelligence artifact
→ CLI inspection/generation
→ browser-first Work Intelligence page
```

Implemented files:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_store.py
src/jobhunter/work_intelligence_inference.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_cli.py
src/jobhunter/web/work_intelligence.py
src/jobhunter/web/templates/work_intelligence.html
tests/test_work_intelligence.py
```

Updated integration:

```text
pyproject.toml
src/jobhunter/web/launcher.py
src/jobhunter/web/templates/job_detail.html
```

CLI entrypoint:

```text
jobhunter-work generate <job-id>
jobhunter-work show <job-id>
```

Browser route:

```text
/jobs/<job-id>/work-intelligence
```

Accepted English-analysis job pages now expose a `Work Intelligence` link.

## 2. Authority and persistence decisions implemented

### Exact factual dependency

A current P2.2A artifact requires the exact current semantically accepted English P1.6 artifact:

```text
job-analysis-english-v20 / job-analysis-v5
```

The service resolves the current parsed source, current configured English projection, and exact accepted P1.6 artifact. Historical Work Intelligence remains preserved but is not returned as current after its P1.6 dependency changes.

Capability v9 is not an authoritative P2.2A input.

### Candidate persistence

Generated output is stored as `JobWorkIntelligenceArtifact` with:

- exact P1.6 analysis artifact dependency;
- Work Intelligence model identity;
- prompt/schema identity;
- typed intelligence JSON;
- request/response history;
- immutable `candidate` semantic state;
- completed/failed/reused attempt history.

Persistence means reproducible/regenerable local analytical state. It does **not** mean human review, canonical responsibility-family membership, or promoted role archetype.

### Initial model configuration

P2.2A deliberately reuses the existing configured Capability reasoning-model fallback chain instead of adding another user configuration surface before usage demonstrates a need for a dedicated Work Intelligence model.

This does not couple P2.2A to Capability artifacts or prose. Work Intelligence retains its own prompt, schema, contract, persistence and evidence semantics.

## 3. Typed analytical contract

The candidate document distinguishes:

```text
evidence_status: sufficient | limited
work themes:      primary | supporting | uncertain
confidence:       high | medium | low
deliverables:     source_explicit | strongly_implied_by_work
candidate role interpretation
limitations / alternatives
```

No numeric Role-DNA percentages or invented time allocation are allowed.

A work theme must reference at least one responsibility or role-purpose item. Supporting requirements may clarify a theme but can never create a duty by themselves.

## 4. Deterministic integrity boundaries

After model reasoning, JobHunter deterministically validates:

- every responsibility index exists;
- every role-purpose index exists;
- every supporting requirement index exists;
- every accepted responsibility is represented by at least one work theme;
- every accepted role-purpose item is represented by at least one work theme;
- candidate role interpretation references only generated theme IDs.

This is intentionally anti-omission/source-integrity validation, not deterministic semantic grouping.

## 5. No-direct-work boundary

When accepted P1.6 contains requirements but no responsibilities or role purpose, P2.2A does **not** call the model and does not fabricate duties.

It persists a deterministic candidate artifact with:

```text
evidence_status = limited
work_themes = []
deliverables = []
role_interpretation = null
explicit limitation explaining that qualifications are not duties
```

`tmBK` is the intended real acceptance anchor for this behavior.

## 6. Browser/publication boundary

The browser generation POST is CSRF protected but deliberately does **not** use `WebOperationManager`.

Reason: the existing operation-manager success hook synchronizes the public corpus. P2.2A Work Intelligence publication has not been authorized.

Therefore:

```text
local SQLite candidate persistence     AUTHORIZED / IMPLEMENTED
browser/CLI local inspection           AUTHORIZED / IMPLEMENTED
public-corpus Work Intelligence export NOT AUTHORIZED
```

The browser explicitly labels the output as JobHunter interpretation / candidate state and preserves access to P1.6 source-reference indices.

## 7. Regression coverage

`tests/test_work_intelligence.py` covers:

- requirements-only limited-work behavior without a model call;
- idempotent candidate artifact reuse;
- direct-work candidate persistence;
- complete responsibility/role-purpose coverage;
- rejection of out-of-range source references;
- rejection of omitted accepted work evidence;
- historical artifact preservation plus currentness invalidation after a new accepted P1.6 dependency;
- pending P1.6 rejection;
- browser limited-work generation/rendering;
- proof that the P2.2A browser route does not trigger public-corpus synchronization.

## 8. Repository quality evidence

CI run `32996495178` on implementation head `c77635c63ec3140146315980fb0c80522b03d0cf` completed successfully.

Observed steps:

```text
Run Ruff                         PASS
Run tests                        PASS
Run tests with warnings errors   PASS
overall CI quality job           PASS
```

The exact test count was not needed/recorded from the GitHub run response; do not invent one.

## 9. Acceptance still required

P2.2A is implemented but **not yet semantically accepted**.

Next real-local acceptance should use the existing real database and current configured local model on:

```text
tG9K  responsibility-rich industrial ML / manufacturing AI
t4qV  responsibility-rich network/security
tmyX  responsibility-rich security infrastructure / Microsoft services
tmBK  accepted requirements but no direct work evidence
```

Review questions:

1. Is each work composition materially faster/easier to understand than manually reading all responsibilities?
2. Are all accepted responsibilities represented without forcing one-item-per-theme output?
3. Are theme labels/summaries useful and restrained?
4. Are deliverables genuinely source-explicit or work-implied rather than generic profession knowledge?
5. Is the role interpretation clearly candidate/inferred and appropriately confidence-qualified?
6. Are ambiguity/alternatives/limitations useful rather than blocker-like?
7. Does `tmBK` correctly remain limited without invented duties?
8. Does rerunning reuse the artifact for the same dependency/model/contract?
9. Does the browser communicate employer fact versus JobHunter interpretation clearly?

Do not promote responsibility families/archetypes, start P2.2B, publish Work Intelligence, start Market v2, or add personal intelligence until P2.2A real-local semantic acceptance is decided.
