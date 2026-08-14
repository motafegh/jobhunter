# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** first dense `tG9K` v17 live run failed before persistence because response-level requirement coverage exposed missing references one at a time; aggregate dense-coverage feedback is now implemented and deterministic CI passes; rerun dense `tG9K` next.

This file is not controlling. Product/domain/source/architecture constraints, roadmap/implementation plans, the active semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Detailed dated working-memory and experiment records preserve the evidence trail.

## 1. Product / architecture identity

JobHunter is a local-first personal career-intelligence application.

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Architecture remains a local Python modular monolith with SQLite structured state, immutable evidence, FastAPI/Uvicorn/Jinja browser UI, shared CLI services, and local-first LM Studio.

Do not introduce Node/npm/React, vector/RAG, graph DB, generic plugin frameworks, agent orchestration, or similar infrastructure without demonstrated need.

## 2. Accepted/public contracts remain frozen

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 accepted/public: job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 accepted schema:         job-analysis-v4
Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Accepted dense chain remains:

```text
tG9K English projection artifact 33
→ P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

Do not treat any candidate artifact as public truth until its acceptance gate passes. Capability artifact 9 remains tied to analysis artifact 29 and must not be represented as though it came from v16/v17.

## 3. Current isolated P1.6 candidate

```text
branch:                       agent/p16-v17-source-led-capacity
draft PR:                     #5
English P1.6 candidate:       job-analysis-english-v17
Candidate schema:             job-analysis-v5
Deterministic CI:             PASS (run 723 before documentation reconciliation)
Dense tG9K live status:       FAILED before persistence on first v17 live run
Current correction:           aggregate all dense coverage defects into one bounded retry
Sparse t4jp v17 regression:   waits for dense reviewable artifact
Public promotion:             NOT AUTHORIZED
```

Detailed current records:

```text
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
```

Previous dense-failure record:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

## 4. V16 capacity defect remains real, but was not the whole dense failure

The first dense `tG9K` v16 run failed before persistence after the initial generation plus one Instructor validation retry.

```text
generation 1: 32 requirements; education present; minimum_experience missing
generation 2: 32 requirements; minimum_experience present; education missing
```

Code analysis confirmed an inherited hard 32-requirement ceiling in the typed response model, accepted `job-analysis-v4` JSON schema, and final evidence validator. Accepted dense v9 already has 27 requirements, while later candidate hardening protects six additional structured `skills[]` source surfaces. There is no product/domain rule limiting a vacancy to 32 factual requirements.

V17 therefore correctly removed the arbitrary requirement-array ceiling in an isolated schema-v5 candidate while leaving accepted v9/v4 untouched.

However, the first v17 live run did not reach 32 requirements. It produced only 15 requirements initially and 16 on retry. Therefore the capacity defect was a real structural hazard, but not the active mechanism of this v17 failure.

## 5. First dense v17 live run — new confirmed blocker

Command:

```bash
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

No v17 artifact persisted.

### Generation 1

```text
role purpose:       1
responsibilities:   6
requirements:       15
coverage exclusions: 0
```

The generation preserved all six structured skills and these explicit depth signals:

```text
Solid
Strong
Hands-on
Comfort
Python expert
```

It omitted `field:minimum_experience`. The inherited response-level requirement coverage validator raised immediately on that first missing reference.

The generation also represented only six of the seven expected dense duty surfaces, but responsibility validation was never reached because requirement validation failed first.

### Generation 2

Instructor's one bounded retry saw only the minimum-experience error and repaired it with:

```text
Professional experience
three to six years
required
experience
```

The second response then failed on the next previously hidden mandatory reference:

```text
field:education
```

The retry budget was exhausted.

### Current failure classification

```text
dense initial output contains multiple coverage omissions
→ fail-fast requirement validator reveals only omission A
→ one bounded retry repairs A
→ validator reveals omission B
→ no retry remains
```

The primary current blocker is therefore **dense coverage feedback granularity / fail-fast response validation**.

## 6. Aggregate dense-coverage correction now implemented

The isolated `JobAnalysisResponseV17` response-level validator now overrides only the historical fail-fast coverage loop.

Accepted/public response models remain unchanged. Requirement-item evidence/depth/optionality semantics remain inherited from the strict v14/v16 path.

One validation error now aggregates, when present:

```text
missing non-excludable requirement references
unaccounted excludable requirement references
obligation mismatches
both-extracted-and-excluded references
illegal context-only extraction/exclusion
non-excludable references illegally excluded
missing responsibility references
```

The correction message explicitly tells the single bounded retry to repair **all listed defects in the same response**.

This does not increase retry count and does not weaken fail-closed behavior.

Regression coverage proves one error can simultaneously expose minimum experience, education, another unaccounted requirement, and a missing responsibility.

## 7. Deterministic verification

After the aggregate-feedback correction and lint cleanup:

```text
CI run 723
head e55ee3776f6d5d1ff9a751fb5f71727ade39c3ec
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Documentation reconciliation commits occur after that head and must keep the normal CI gate green before merge/promotion decisions.

## 8. Sparse calibration history remains valid

```text
v9 t4jp artifact 30
→ rejected: structured skills could disappear; qualification became responsibility

v10 artifact 31
→ structured skills fixed; coarse coverage still hid explicit neighboring qualifications

v11
→ failed: qualification spans were outside evidence-reference protocol

v12
→ first-class qualification references worked; coarse bookkeeping still model-owned

v13 artifact 32
→ deterministic decomposition worked; residual facts/concept normalization still wrong

v14 artifact 33
→ complete mechanical sparse coverage; trait ontology/residual strength wrong

v15 artifact 34
→ mechanical PASS; punctuation debris + ability→experience typing wrong

v16 artifact 35
→ bounded sparse mechanical + semantic PASS
```

V16 sparse acceptance remains valid. V17 must prove it does not regress that restraint after the dense gate.

## 9. Generic semantic boundaries inherited by v17

- deterministic coverage of non-empty structured `skills[]`;
- exact qualification-list item evidence;
- deterministic coarse-span decomposition bookkeeping;
- complete residual sentence accounting;
- qualification-vs-responsibility protection;
- coverage obligation separated from employer requirement strength;
- schedule wording cannot become technical depth;
- schedule wording removed from reusable capability concepts without changing evidence;
- valid `Ability to ...` wrapper normalization;
- no empty grouping punctuation in normalized concepts;
- explicit ontology for skill/tool/knowledge/practice/domain/experience/education/other;
- behavioral/value expectations use `other` instead of being forced into technical classes;
- `experience` requires prior-applied-exposure evidence rather than mere ability wording;
- one bounded correction and fail-closed behavior.

Core ownership principle remains:

```text
model owns bounded semantic interpretation
JobHunter owns deterministic evidence identity, coverage, provenance, accounting, and fail-closed guards
```

## 10. Next action — rerun dense tG9K only

Update the local candidate branch and rerun:

```bash
git pull --ff-only origin agent/p16-v17-source-led-capacity
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

Do not run sparse `t4jp` yet.

If a v17 artifact persists, inspect it against accepted v9 artifact 29 and source/projection for:

- Master's degree and `three to six years` professional experience coexisting;
- all six structured skills represented;
- complete dense requirement coverage without quota-driven fact loss;
- all seven accepted duty surfaces represented;
- explicit depth: `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`, `three to six years`;
- MATLAB/C++ preference preserved;
- contextual stack semantics preserved where source wording requires it;
- structured `Python` and prose `Python (expert)` kept provenance-distinct unless an explicit later reconciliation rule is accepted;
- concept-type differences reviewed only after a valid artifact exists.

If the rerun still fails, classify the new aggregate error/output rather than increasing retries or weakening coverage.

## 11. Then sparse v17 non-regression

Only after dense v17 yields a reviewable artifact:

```bash
python scripts/run_p16_v17_candidate.py --job-id t4jp
```

Compare with v16 artifact 35. Removing dense capacity and improving correction feedback must not create sparse over-extraction.

## 12. Capability / heterogeneous progression remains gated

Until P1.6 v17 passes dense + sparse semantic acceptance:

```text
v17 public promotion             → blocked
Capability v7 rebuild over v17   → blocked
Python/software CI-3 role        → blocked
network/security CI-3 role       → blocked
operations/platform CI-3 role    → blocked
```

After P1.6 promotion, Capability v7 must be rebuilt against the promoted P1.6 artifact and reviewed as a new dependency chain rather than reusing artifact 9.

## 13. Blueprint remains deferred

Blueprint is implemented but not accepted for Phase-1 decision use.

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
artifact 7 on tG9K
model gemma-4-12b-it-qat
```

Do not create Blueprint v7, weaken validators, or reopen nearby model shopping during this gate.

## 14. Follow-up capacity audit

Other historical list ceilings exist, notably responsibility/coverage bounds. They are not the current blocker unless live evidence demonstrates failure, but they should receive a separate source-led-capacity audit later so JobHunter does not simply move from one arbitrary ceiling to another.
