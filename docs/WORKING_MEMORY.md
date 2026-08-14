# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** P1.6 v16 is accepted on sparse `t4jp`; first dense `tG9K` v16 regression failed before persistence; diagnosis/discussion comes before any fix.

This file is not controlling. Product/domain/source/architecture constraints, roadmap/implementation plans, the active semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Detailed dated working-memory and experiment records preserve the full evidence trail.

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

## 2. Current accepted/public contracts

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 accepted/public: job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4
Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Current isolated P1.6 candidate:

```text
English P1.6 candidate:       job-analysis-english-v16
Candidate schema:             job-analysis-v4
Sparse t4jp status:           ACCEPTED for bounded sparse case
Dense tG9K status:            FAILED before persistence on first regression run
Public promotion:             NOT AUTHORIZED
```

Current model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental only
```

## 3. Accepted dense baseline remains frozen

`tG9K` accepted chain remains:

```text
English projection artifact 33
→ accepted English P1.6 v9 artifact 29
→ accepted Capability v7 artifact 9
```

P1.6 artifact `29` remains the authoritative dense comparison baseline:

- 27 requirements;
- 7 responsibilities;
- complete accepted source accounting;
- optionality preserved;
- `Solid` statistics/signal-processing depth;
- Python-specific `expert` depth;
- MATLAB/C++ preferred;
- contextual stack contextual;
- industrial AI/ML experience `Strong`;
- process-control/manufacturing analytics `Hands-on`;
- high-dimensional sensor/time-series data `Comfort`;
- Master's degree;
- professional experience `three to six years`.

Capability artifact `9` remains accepted only against analysis artifact `29`.

Do not reuse that Capability artifact as if it were derived from v16. If a later P1.6 identity is promoted, Capability v7 must be rebuilt and reviewed against the promoted P1.6 artifact.

## 4. Blueprint remains deferred

Blueprint is implemented but not accepted for Phase-1 decision use.

Best bounded experimental evidence remains:

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
artifact 7 on tG9K
model gemma-4-12b-it-qat
```

Do not create Blueprint v7, weaken its validators, or reopen nearby model shopping during the current Phase-1 gate.

## 5. CI-3 workflow and target set

Target stack:

```text
source
→ English projection
→ semantically accepted P1.6 for that job
→ Capability v7 only after P1.6 passes
```

Target set:

```text
t4jp  sparse/ambiguous anchor — v16 P1.6 accepted for bounded sparse case
tG9K  rich industrial AI/ML anchor — v9/v7 accepted baseline; v16 dense regression blocked
+ Python/software
+ network/security
+ operations/platform/DevOps
```

Permanent workflow:

```text
snapshot current local state first
→ run matching mechanical audit
→ inspect source / projection / P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
→ never rerun accepted upstream stages merely to create a fresh artifact
```

## 6. Sparse calibration result through v16

The sparse `t4jp` sequence established the following progression:

```text
v9 artifact 30
→ rejected: structured skills could disappear; qualification became responsibility

v10 artifact 31
→ mechanical PASS / semantic FAIL: coarse coverage lost explicit neighboring qualifications

v11
→ failed before persistence: qualification spans were outside the evidence-reference protocol

v12
→ first-class qualification references worked
→ failed before persistence because coarse coverage still remained model-owned bookkeeping

v13 artifact 32
→ 0 responsibilities / 7 requirements
→ 3/3 structured skills + 4/4 qualification items
→ semantic FAIL: whole-span suppression hid Ethics/work commitment and one concept retained
  Ability-to + schedule wording

v14 artifact 33
→ complete mechanical sparse PASS
→ semantic FAIL: behavioral/value expectation typed as skill and residual coverage forced required

v15 artifact 34
→ mechanical PASS
→ semantic FAIL: `Visual content production ( )` + unsupported experience typing for ability evidence

v16 artifact 35
→ sparse mechanical PASS
→ sparse semantic PASS
```

Detailed records:

```text
docs/experiments/2026-08-12_P16_V10_SPARSE_STRUCTURED_SKILLS_BOUNDARY.md
docs/experiments/2026-08-12_P16_V10_SEMANTIC_FAILURE_AND_V11_QUALIFICATION_GRANULARITY.md
docs/experiments/2026-08-12_P16_V11_EVIDENCE_PROTOCOL_FAILURE_AND_V12_REFERENCE_FIX.md
docs/experiments/2026-08-13_P16_V12_COARSE_COVERAGE_FAILURE_AND_V13_DETERMINISTIC_DECOMPOSITION.md
docs/experiments/2026-08-13_P16_V13_SEMANTIC_FAILURE_AND_V14_COMPLETE_DECOMPOSITION.md
docs/working-memory/2026-08-13_P16_V15_HANDOFF.md
docs/working-memory/2026-08-14_P16_V15_SCHEDULE_CONCEPT_CORRECTION.md
docs/working-memory/2026-08-14_P16_V15_ABILITY_WRAPPER_CORRECTION.md
docs/working-memory/2026-08-14_P16_V16_HANDOFF.md
docs/working-memory/2026-08-14_P16_V16_SPARSE_ACCEPTANCE.md
```

## 7. What v14→v16 added generically

The current candidate path now contains these generic boundaries:

- deterministic coverage of non-empty structured `skills[]`;
- exact qualification-list item evidence;
- deterministic coarse-span decomposition bookkeeping;
- complete residual sentence accounting;
- qualification-vs-responsibility protection;
- separation of coverage obligation from employer strength;
- schedule wording cannot become technical depth;
- capability concepts cannot retain full-time/part-time wording;
- valid `Ability to ...` wrappers are normalized without changing exact evidence;
- normalization cannot leave empty grouping punctuation;
- behavioral/value/professional expectations use `other` rather than being forced into technical skill classes;
- `experience` requires evidence of prior applied exposure rather than mere ability wording;
- one bounded correction is allowed; failure after that remains fail-closed.

Core principle remains:

```text
model owns bounded semantic interpretation
JobHunter owns deterministic evidence identity, coverage, provenance, accounting, and fail-closed guards
```

## 8. Sparse v16 accepted artifact

`t4jp` v16 artifact `35`:

```text
Requirements:      8
Responsibilities:  0
Role purpose:      0
Structured skills: 3/3
Qualification items: 4/4
Residual decisions: 4/4
```

The formerly problematic evidence:

```text
ability to produce visual content full-time and part-time
```

is now represented as a clean `Production of visual content` skill, required, with null depth and exact source evidence retained.

Sparse acceptance is bounded only; it does not promote v16 globally.

## 9. Dense-safe mechanical audit change

Before dense regression, the v16 audit was generalized so `decomposed_requirement` is required only when qualification/residual decomposition is actually active.

This removed a sparse-only audit assumption without changing extraction semantics.

Regression coverage was added and CI run 706 passed Ruff, full pytest, and warnings-as-errors.

## 10. Current blocker — first dense tG9K v16 run

The first dense command:

```bash
python scripts/run_p16_v16_candidate.py --job-id tG9K
```

failed before persistence after the initial generation plus one bounded validation retry.

No v16 `tG9K` artifact exists.

### Generation 1

```text
role purpose:       1
responsibilities:   7
requirements:       32
coverage exclusions: 0
```

Failure:

```text
field:minimum_experience was not cited by a requirement
```

Education was present as Master's degree.

### Generation 2

The correction added:

```text
Professional experience
field:minimum_experience
three to six years
required
experience
```

but then omitted:

```text
field:education
```

The final failure was:

```text
Requirement coverage reference field:education must be cited by a requirement
or explicitly justified in coverage_exclusions
```

The retry budget was exhausted and the run failed closed.

Confirmed failure class so far:

```text
mandatory structured fields are individually representable,
but the current dense model/correction interaction did not preserve
education + minimum_experience simultaneously in one valid response
```

No fix/classification has been chosen yet.

## 11. Dense warning signals from the failed outputs

These are observations from failed, non-persisted generations—not accepted project truth.

### Explicit depth warnings

Both failed generations retained:

```text
Python → expert
process-control/manufacturing analytics → Hands-on
high-dimensional sensor/time-series work → Comfort
```

Generation 2 also retained:

```text
professional experience → three to six years
```

But both failed generations represented these accepted v9 facts with null depth:

```text
statistics and signal-processing fundamentals → expected Solid, got null
industrial/manufacturing AI/ML experience → expected Strong, got null
```

Any future persisted dense candidate must be checked explicitly for `Solid` and `Strong`; mechanical coverage alone is insufficient.

### Dense requirement-shape change

Each failed generation had 32 requirements while omitting one mandatory structured field.

All six top-level structured skills were represented as required:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

This is a consequence of the structured-skill coverage rule introduced because sparse v9 could lose those facts.

It is not automatically a regression, but it means v16 dense output is not expected to be a byte-for-byte or count-for-count copy of v9.

### Same-concept multi-surface question

The failed dense responses contain both:

```text
structured skills[] Python → required
prose Python (expert)       → contextual + expert depth
```

Open question:

```text
How should JobHunter preserve both source truths for one concept
without losing provenance, optionality, or depth and without presenting
a misleading duplicate/collapsed strength?
```

No reconciliation rule is accepted yet.

### Ontology differences to review later

Failed v16 output also changed some concept types relative to v9, such as SQL/framework/library classifications. Some may be improvements under the explicit v16 ontology; some may be regressions. Do not classify them until a valid dense artifact exists and receives semantic review.

## 12. Exact current decision boundary

```text
public v9 P1.6
→ remains authoritative

v16 sparse t4jp artifact 35
→ accepted for bounded sparse case

v16 dense tG9K
→ failed before persistence; diagnosis pending

v16 promotion
→ blocked

Capability v7 rebuild above v16
→ blocked

further heterogeneous role progression
→ wait until dense P1.6 decision
```

Do not fix the dense failure merely by reacting to the last validator message. The next discussion must distinguish:

1. mandatory structured-field coverage/retry behavior;
2. explicit-depth retention (`Solid`, `Strong`);
3. structured-skill/prose overlap and same-concept strength reconciliation;
4. ontology changes that are improvements vs regressions;
5. which layer should own any eventual correction.

## 13. Primary current resume record

Use this file for the detailed current state:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

When work resumes, diagnose first. Do not implement a fix until the failure class and desired generic semantics are agreed.
