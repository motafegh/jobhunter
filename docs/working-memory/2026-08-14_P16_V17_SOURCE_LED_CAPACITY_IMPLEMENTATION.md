# P1.6 v17 Source-Led Capacity Implementation

**Date:** 2026-08-14  
**Status:** Historical implementation checkpoint / capacity correction retained / current state continues in dense-feedback record  
**Branch:** `agent/p16-v17-source-led-capacity`  
**Draft PR:** #5  
**Public accepted P1.6 remains:** `job-analysis-english-v9` / `job-analysis-v4`

> Current continuation: `docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md`
>
> The first live v17 dense run occurred after this checkpoint. It proved that the removed 32-item
> ceiling was not the active mechanism of that specific v17 failure and exposed a second mechanical
> blocker: fail-fast response-level coverage feedback under a one-retry policy. This file preserves
> the capacity-correction decision and implementation evidence; use the continuation record for the
> current execution point.

## 1. Why v17 exists

The first dense `tG9K` v16 regression failed before persistence twice. Both generations reached
exactly 32 requirements. The first retained education but omitted `field:minimum_experience`; the
bounded validation retry restored minimum experience but then omitted `field:education`.

Follow-up code and artifact analysis confirmed that the P1.6 response path contained an inherited
fixed 32-requirement ceiling in three independent places:

1. the Instructor/Pydantic typed response model;
2. the persisted `job-analysis-v4` JSON schema;
3. the independent final P1.6 evidence validator.

The ceiling predates the later source-led coverage rules. Accepted dense `tG9K` v9 already contains
27 factual requirements, while the later sparse-hardening contract additionally requires all six
non-empty top-level `skills[]` source items to remain represented. Those source surfaces can
therefore require at least 33 distinct requirement records before any semantically invalid
compression is considered.

The project has no product/domain rule saying a vacancy may contain at most 32 requirements.
Therefore the correct boundary is source-led factual coverage, not a fixed claim quota.

## 2. Decision

Do **not**:

- drop education, experience, skills, or another supported fact to fit 32;
- merge distinct source surfaces merely to reduce record count;
- weaken exact-evidence, optionality, depth, or coverage validation;
- change the accepted/public v9/v4 path in place;
- replace 32 with another arbitrary ceiling such as 64 and postpone the same defect.

Create an isolated candidate:

```text
job-analysis-english-v17
schema job-analysis-v5
```

The original v17 capacity increment changed representation capacity while retaining v16 semantic
boundaries. The later dense-feedback continuation adds only aggregate correction feedback; it does
not reverse this capacity decision.

## 3. Capacity implementation

### Typed response model

`src/jobhunter/inference/instructor_lm_studio_v17.py`

- inherits the v14 typed requirement item model and strict depth/evidence semantics;
- removes `requirements.max_length=32` for the candidate response;
- leaves accepted base and v14/public response paths unchanged.

The same candidate response model is later extended by the dense-feedback correction record to
replace only the inherited fail-fast response-level coverage loop.

### Candidate schema/service

`src/jobhunter/analysis_service_v17.py`

- prompt identity: `job-analysis-english-v17`;
- schema identity: `job-analysis-v5`;
- creates `_ANALYSIS_SCHEMA_V17` from a deep copy of accepted `_ANALYSIS_SCHEMA`;
- removes only `maxItems` from the candidate `requirements` array;
- explicitly tells the model that requirement count follows supported source assertions rather
  than a quota;
- keeps v16 semantic validation;
- persists candidate artifacts under schema v5, so v9/v4 artifact identity remains reproducible.

### Final validation

The accepted v9/v4 final validator remains unchanged and continues to enforce its historical 32
limit for accepted artifacts.

V17 adds `_validate_evidence_v17`:

- proves global requirement uniqueness across the whole candidate output;
- reuses the accepted independent evidence/depth validator in bounded 32-item requirement slices so
  the historical validator can be reused without inheriting its cardinality policy;
- therefore item 33+ still receives exact-evidence and semantic validation rather than bypassing
  the guard.

The 32 used inside this compatibility validation loop is a validator batch size, **not** an output
or semantic claim limit.

### Runtime

`src/jobhunter/analysis_runtime_v17.py`

- substitutes `JobAnalysisResponseV17` only inside the isolated candidate call and under the
  existing response-model lock;
- preserves v15 schedule normalization/decomposition behavior;
- then returns through inherited v16 clean-concept and experience-evidence guards;
- records explicit runtime provenance that the old 32-item candidate ceiling was removed.

### Runner

```bash
python scripts/run_p16_v17_candidate.py --job-id <job-id>
```

### Capacity regression tests

`tests/test_analysis_v17_candidate.py` proves:

- v17/v5 has a distinct contract identity;
- accepted `_ANALYSIS_SCHEMA` still has `maxItems: 32`;
- v17 schema does not mutate that accepted schema;
- v14 typed response rejects 33 requirements while v17 accepts 33;
- the v17 final guard accepts 33 grounded unique requirements;
- a duplicate crossing the old 32-item boundary still fails;
- ungrounded evidence after item 32 still fails.

The continuation record adds a separate aggregate dense-feedback regression.

## 4. Deterministic verification at this checkpoint

The initial source-led-capacity implementation passed the normal repository gate before its first
live dense run:

```text
CI run 717
head 8c335db685246d52b97058984cf207d310b336b6
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Later commits and CI are documented in the continuation record.

## 5. Historical acceptance boundary at this checkpoint

At this point v17 was mechanically ready but had not yet received its first live dense run.

Public truth remained:

```text
job-analysis-english-v9 / job-analysis-v4
P1.6 tG9K artifact 29
Capability v7 artifact 9 derived from artifact 29
```

That public boundary remains unchanged after the later failed v17 live run.

## 6. Current continuation

Use:

```text
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
```

for:

- the first live v17 `tG9K` result;
- the 15→16 requirement generations;
- the newly classified fail-fast correction-feedback defect;
- aggregate requirement + responsibility coverage feedback implementation;
- the current rerun gate.

## 7. Promotion boundary remains unchanged

Do not promote v17 until:

```text
deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Only after P1.6 promotion should Capability v7 be rebuilt against the promoted P1.6 artifact and
reviewed as a new dependency chain.

## 8. Follow-up engineering note

The same historical bounded-count pattern exists elsewhere (for example responsibilities and
coverage arrays). It is not the current blocker unless live evidence demonstrates a failure there,
but it should receive a separate source-led-capacity audit later so JobHunter does not merely move
from one arbitrary ceiling to the next.
