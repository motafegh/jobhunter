# P1.6 v17 Dense Coverage Feedback Correction

**Date:** 2026-08-14  
**Status:** Candidate correction implemented / deterministic CI PASS / dense live rerun required  
**Branch:** `agent/p16-v17-source-led-capacity`  
**Draft PR:** #5  
**Public accepted P1.6 remains:** `job-analysis-english-v9` / `job-analysis-v4`

## 1. Live evidence that changed the diagnosis

After the v17 source-led-capacity implementation passed deterministic CI, the local dense command
was run:

```bash
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

The run still failed before persistence after the initial generation plus the one bounded
Instructor validation retry. No v17 `tG9K` artifact was created.

Unlike the earlier v16 failure, the two v17 generations did **not** reach the old 32-item ceiling:

```text
generation 1: 15 requirements
generation 2: 16 requirements
```

Therefore the removed 32-item ceiling remains a real structural defect/hazard, but it was **not the
active failure mechanism in this v17 run**. The live run exposed a second independent mechanical
problem in dense correction feedback.

## 2. Generation 1

Generation 1 produced:

```text
role purpose:      1
responsibilities:  6
requirements:      15
coverage exclusions: 0
```

It correctly retained all six structured `skills[]` surfaces and these explicit depth facts:

```text
statistics/signal processing → Solid
industrial/manufacturing AI/ML experience → Strong
process-control/manufacturing analytics → Hands-on
high-dimensional sensor/time-series work → Comfort
Python prose surface → expert
```

But it omitted the mandatory structured minimum-experience field. Pydantic reported only:

```text
field:minimum_experience must be cited by a requirement
```

The output also represented only six of the seven expected dense duty surfaces; one responsibility
surface was missing, but response validation did not reach responsibility coverage because the
first requirement-coverage error terminated validation.

## 3. Generation 2

Instructor gave the one bounded correction using the first validation error. The model repaired
exactly that visible defect by adding:

```text
Professional experience
field:minimum_experience
three to six years
required
experience
```

Generation 2 therefore had 16 requirements and preserved the same explicit depth signals, including
`three to six years`.

Validation then advanced to the next hidden missing structured field and failed on:

```text
field:education must be cited by a requirement
```

The retry budget was exhausted. No artifact persisted.

## 4. Confirmed root cause of the current blocker

The inherited response-level requirement coverage validator iterated the coverage plan and raised
immediately on the **first** missing reference.

That behavior is incompatible with the deliberately bounded one-retry policy on dense postings:

```text
initial output has several omissions
→ validator reveals omission A only
→ single retry repairs A
→ validator reveals omission B
→ retry budget exhausted
```

Responsibility coverage already had the better behavior: it computed and reported the complete set
of missing duty references together. Requirement coverage did not.

The current blocker is therefore classified as:

> **dense coverage feedback granularity / fail-fast validation, not requirement-array capacity.**

The old 32-item capacity defect remains fixed by v17 because complete dense correction may still
legitimately produce more than 32 requirement records.

## 5. Correction implemented

The isolated `JobAnalysisResponseV17` response-level validator now overrides only the inherited
fail-fast coverage loop. Accepted/public response models remain unchanged.

V17 still uses the same strict requirement-item validators for:

- evidence grounding;
- explicit depth;
- optionality;
- concept semantics inherited from the v14/v16 candidate path.

But response-level coverage validation now aggregates all defects before raising one error.

One correction message can now contain, together:

```text
missing non-excludable requirement references
unaccounted excludable requirement references
obligation mismatches
references both extracted and excluded
illegal context-only extraction/exclusion
non-excludable references illegally excluded
missing responsibility references
```

The error explicitly instructs the bounded retry to correct **all listed defects in the same
response** rather than stopping after the first one.

This does not increase the retry budget and does not weaken fail-closed behavior.

## 6. Regression coverage

`tests/test_analysis_v17_candidate.py` now includes a dense-feedback regression proving that one
validation error simultaneously exposes:

```text
field:minimum_experience
field:education
another unaccounted requirement reference
a missing responsibility reference
```

The previous v17 regression tests remain:

- v14/v4 rejects 33 requirements while v17 accepts 33;
- v17 schema does not mutate accepted v4;
- duplicate claims across the old 32 boundary fail;
- ungrounded evidence after item 32 fails.

## 7. Deterministic verification

After the aggregate-feedback correction and lint cleanup:

```text
CI run 723
head e55ee3776f6d5d1ff9a751fb5f71727ade39c3ec
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

The correction is mechanically ready for another local dense run.

## 8. Important semantic observations from the failed v17 output

These observations are from failed/non-persisted generations and are not accepted project truth.

Positive signals compared with the failed v16 outputs:

- `Solid` was preserved;
- `Strong` was preserved;
- Python `expert` was preserved;
- `Hands-on` was preserved;
- `Comfort` was preserved;
- generation 2 preserved `three to six years`.

Still unresolved until a valid persisted artifact exists:

- full requirement coverage across the remaining technical-stack/qualification references;
- Master's degree coexisting with minimum experience;
- all seven duty surfaces in one valid response;
- structured `Python → required` versus prose `Python (expert) → contextual + expert` provenance;
- final concept-type review;
- whether the fully corrected dense output actually needs more than 32 requirements.

## 9. Next gate

Pull the latest candidate branch and rerun only dense `tG9K`:

```bash
git pull --ff-only origin agent/p16-v17-source-led-capacity
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

Do not run sparse `t4jp` yet.

If the dense run persists an artifact, review it against accepted v9 artifact 29 before any further
candidate progression.

If it still fails, use the new aggregate validation error/output to classify the next concrete
failure. Do not increase retries or weaken coverage merely to force persistence.

## 10. Promotion boundary unchanged

```text
public v9/schema v4                     → authoritative
v17 deterministic implementation       → PASS
v17 dense live semantic acceptance     → pending
v17 sparse t4jp non-regression          → waits for dense
Capability rebuild over v17             → blocked
v17 promotion                           → blocked
heterogeneous CI-3 role progression     → blocked
```
