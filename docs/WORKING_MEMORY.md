# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** P1.6 v17 source-led-capacity candidate is implemented and deterministic CI passes; dense `tG9K` live semantic acceptance is the next gate.

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
Deterministic CI:             PASS (run 717)
Dense tG9K live status:       NOT RUN YET
Sparse t4jp v17 regression:   waits for dense reviewable artifact
Public promotion:             NOT AUTHORIZED
```

V17 keeps all v16 semantic boundaries and changes only the requirement representation-capacity contract.

Detailed implementation record:

```text
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
```

Previous dense-failure record:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

## 4. Why v17 was required

The first dense `tG9K` v16 run failed before persistence after the initial generation plus one Instructor validation retry.

```text
generation 1: 32 requirements; education present; minimum_experience missing
generation 2: 32 requirements; minimum_experience present; education missing
```

Analysis confirmed that P1.6 had an inherited hard 32-requirement ceiling in:

1. the Instructor/Pydantic response model;
2. the accepted `job-analysis-v4` JSON schema;
3. the independent final evidence validator.

That ceiling predates the later source-led coverage contract. Accepted dense v9 `tG9K` already has 27 requirements, and later candidate hardening requires all six non-empty structured `skills[]` source surfaces to remain represented. A valid dense representation can therefore require at least 33 distinct records.

There is no product/domain rule that a vacancy may have at most 32 factual requirements. The correct invariant is source-led evidence coverage, not a fixed claim quota.

## 5. V17 implementation boundary

V17 does **not** weaken semantics or compress facts to fit a quota.

It:

- introduces `job-analysis-english-v17`;
- introduces candidate schema identity `job-analysis-v5`;
- leaves accepted v9/v4 code and artifacts unchanged;
- removes the fixed requirement-array cap only for the v17 candidate;
- preserves exact evidence, obligation strength, explicit depth, structured-skill coverage, qualification-vs-duty rules, decomposition/residual accounting, concept normalization, and experience-evidence guards;
- keeps global duplicate detection across item 33+;
- keeps final exact-evidence validation for item 33+;
- records candidate runtime provenance for the removed legacy capacity ceiling.

Regression tests explicitly prove that v14/v4 still rejects 33 while v17 accepts 33 grounded unique requirements, and that duplicates or invented evidence beyond the old boundary still fail.

## 6. Deterministic verification

Normal repository CI on final code state before this documentation update:

```text
run 717
head 8c335db685246d52b97058984cf207d310b336b6
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Temporary CI diagnostics used to discover Ruff's canonical import order were reverted. `.github/workflows/ci.yml` is back to the normal repository gate.

## 7. Sparse calibration history remains valid

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

## 8. Generic semantic boundaries inherited by v17

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
- bounded correction and fail-closed behavior.

Core ownership principle remains:

```text
model owns bounded semantic interpretation
JobHunter owns deterministic evidence identity, coverage, provenance, accounting, and fail-closed guards
```

## 9. Next action — dense tG9K live gate

Run locally against the configured LM Studio/database:

```bash
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

A persisted artifact is only the first gate. Inspect source/projection/P1.6 semantics against accepted v9 artifact 29.

Required checks:

- Master's degree and `three to six years` professional experience coexist;
- all six structured skills are represented;
- no accepted dense factual assertion disappeared merely because requirement count exceeds 32;
- responsibility coverage remains correct;
- explicit depth is checked for `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`, and `three to six years`;
- MATLAB/C++ remain preferred;
- contextual stack remains contextual where source wording requires it;
- structured `Python` and prose `Python (expert)` remain provenance-distinct unless a later explicit reconciliation rule is accepted;
- ontology differences are reviewed separately after a valid dense artifact exists.

If the live run fails, classify the new concrete failure rather than assuming the old 32-slot failure remains.

## 10. Then sparse v17 non-regression

After dense v17 yields a reviewable artifact:

```bash
python scripts/run_p16_v17_candidate.py --job-id t4jp
```

Compare with v16 artifact 35. Removing a dense capacity ceiling must not create sparse over-extraction.

## 11. Capability / heterogeneous progression remains gated

Until P1.6 v17 passes dense + sparse semantic acceptance:

```text
v17 public promotion             → blocked
Capability v7 rebuild over v17   → blocked
Python/software CI-3 role        → blocked
network/security CI-3 role       → blocked
operations/platform CI-3 role    → blocked
```

After P1.6 promotion, Capability v7 must be rebuilt against the promoted P1.6 artifact and reviewed as a new dependency chain rather than reusing artifact 9.

## 12. Blueprint remains deferred

Blueprint is implemented but not accepted for Phase-1 decision use.

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
artifact 7 on tG9K
model gemma-4-12b-it-qat
```

Do not create Blueprint v7, weaken validators, or reopen nearby model shopping during this gate.

## 13. Follow-up capacity audit

Other historical list ceilings exist, notably responsibility/coverage bounds. They are not part of the current blocker unless live evidence demonstrates failure, but they should receive a separate source-led-capacity audit later so JobHunter does not simply move from one arbitrary ceiling to another.
