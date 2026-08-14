# P1.6 v17 Source-Led Capacity Implementation

**Date:** 2026-08-14  
**Status:** Implemented candidate / deterministic CI PASS / live semantic acceptance pending  
**Branch:** `agent/p16-v17-source-led-capacity`  
**Draft PR:** #5  
**Public accepted P1.6 remains:** `job-analysis-english-v9` / `job-analysis-v4`

## 1. Why v17 exists

The first dense `tG9K` v16 regression failed before persistence twice. Both generations reached
exactly 32 requirements. The first retained education but omitted `field:minimum_experience`; the
bounded validation retry restored minimum experience but then omitted `field:education`.

Follow-up code and artifact analysis confirmed that this was not merely a prompt-retry accident.
The P1.6 response path contained an inherited fixed 32-requirement ceiling in three independent
places:

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

V17 changes requirement representation capacity only. Every v16 semantic boundary remains in
force.

## 3. Implementation

### Typed response model

`src/jobhunter/inference/instructor_lm_studio_v17.py`

- inherits the v14 typed requirement model and its strict depth/evidence semantics;
- removes only `requirements.max_length=32` for the candidate response;
- leaves accepted base and v14 models unchanged.

### Candidate schema/service

`src/jobhunter/analysis_service_v17.py`

- prompt identity: `job-analysis-english-v17`;
- schema identity: `job-analysis-v5`;
- creates `_ANALYSIS_SCHEMA_V17` from a deep copy of accepted `_ANALYSIS_SCHEMA`;
- removes only `maxItems` from the candidate `requirements` array;
- explicitly tells the model that requirement count follows supported source assertions rather
  than a quota;
- keeps v16 validation semantics;
- persists candidate artifacts under schema v5, so v9/v4 artifact identity remains reproducible.

### Final validation

The accepted v9/v4 final validator remains unchanged and continues to enforce its historical 32
limit for accepted artifacts.

V17 adds `_validate_evidence_v17`:

- proves global requirement uniqueness across the whole candidate output;
- reuses the accepted independent evidence/depth/coverage validator in bounded 32-item validation
  slices so the historical validator can be reused without inheriting its cardinality policy;
- therefore item 33+ still receives exact-evidence and semantic validation rather than bypassing
  the guard.

The 32 used inside this compatibility validation loop is a validator batch size, **not** an output
or semantic claim limit.

### Runtime

`src/jobhunter/analysis_runtime_v17.py`

- substitutes `JobAnalysisResponseV17` only inside the isolated candidate call and under the
  existing response-model lock;
- preserves v15 schedule normalization/decomposition behavior;
- then returns through the inherited v16 clean-concept and experience-evidence guards;
- records explicit runtime provenance that the old 32-item candidate ceiling was removed.

### Runner

```bash
python scripts/run_p16_v17_candidate.py --job-id <job-id>
```

### Regression tests

`tests/test_analysis_v17_candidate.py` proves:

- v17/v5 has a distinct contract identity;
- accepted `_ANALYSIS_SCHEMA` still has `maxItems: 32`;
- v17 schema does not mutate that accepted schema;
- v14 typed response rejects 33 requirements while v17 accepts 33;
- the v17 final guard accepts 33 grounded unique requirements;
- a duplicate crossing the old 32-item boundary still fails;
- ungrounded evidence after item 32 still fails.

## 4. Deterministic verification

Final normal CI run on the candidate branch:

```text
CI run 717
head 8c335db685246d52b97058984cf207d310b336b6
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Temporary CI diagnostic changes used while resolving Ruff import ordering were fully reverted. The
branch ends on the repository's normal CI workflow.

## 5. Current acceptance boundary

V17 is **mechanically ready but not semantically accepted**.

Public truth remains:

```text
job-analysis-english-v9 / job-analysis-v4
P1.6 tG9K artifact 29
Capability v7 artifact 9 derived from artifact 29
```

Do not rebuild or promote Capability over v17 yet.

## 6. Next live gate — dense tG9K

Run locally with the configured LM Studio model and current JobHunter database:

```bash
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

A persisted artifact is necessary but not sufficient. Review it against accepted v9 artifact 29
and the source/projection.

Required dense checks:

- education and `three to six years` minimum experience coexist in the same valid artifact;
- all six structured `skills[]` surfaces remain represented;
- accepted dense factual coverage is not silently lost merely because the output exceeds 32;
- 7 accepted duty surfaces remain represented correctly;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`, and `three to six years` are checked
  for correct depth attachment;
- MATLAB/C++ preference remains preferred;
- contextual technical-stack semantics remain contextual where source wording requires it;
- structured `Python` and prose `Python (expert)` remain provenance-distinct unless a later
  explicit semantic reconciliation rule is accepted;
- concept-type differences are reviewed separately rather than treating every difference from v9
  as either automatically correct or automatically wrong.

If dense generation still fails, classify the new concrete failure rather than reopening the old
32-slot diagnosis by assumption.

## 7. Sparse non-regression gate

Only after dense v17 produces a reviewable artifact, run:

```bash
python scripts/run_p16_v17_candidate.py --job-id t4jp
```

Compare with bounded sparse v16 artifact 35. Removing an artificial dense capacity ceiling must not
cause sparse over-extraction. Expected invariant remains sparse evidence → restrained supported
claims.

## 8. Promotion boundary

Do not promote v17 until:

```text
deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Only after P1.6 promotion should Capability v7 be rebuilt against the promoted P1.6 artifact and
reviewed as a new dependency chain.

## 9. Follow-up engineering note

The same historical bounded-count pattern exists elsewhere (for example responsibilities and
coverage arrays). It is not part of this immediate blocker unless live evidence demonstrates a
failure there, but it should receive a separate source-led-capacity audit later so JobHunter does
not merely move from one arbitrary ceiling to the next.
