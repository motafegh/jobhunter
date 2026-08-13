# P1.6 v13 Semantic Failure and v14 Complete Decomposition

**Date:** 2026-08-13  
**Status:** v13 rejected for sparse semantic acceptance; v14 active isolated candidate  
**Trigger job:** `t4jp`  
**Rejected artifact:** `32` / `job-analysis-english-v13` / `job-analysis-v4`  
**Active candidate:** `job-analysis-english-v14` / `job-analysis-v4`

## v13 result

Artifact 32 was mechanically strong:

- 0 responsibilities;
- 7 requirements;
- all 3 structured skills retained;
- all 4 deterministic comma-list qualification items retained;
- coarse description coverage recorded as `decomposed_requirement`;
- no unsupported depth;
- benefits, location and teachability did not become requirements or duties.

The artifact still failed full semantic review for two generic reasons.

### 1. Incomplete decomposition coverage

v13 suppressed the whole coarse requirement coverage span after proving that it contained several
item-level qualifications. That prevented the model from being responsible for requirement-bearing
residual prose inside the same source span.

For `t4jp`, this caused the explicit employer expectation below to disappear:

```text
Ethics and your work commitment are important to us.
```

The original Persian source expresses the same expectation. This is not optional context or a
benefit; it is explicit employer qualification/trait evidence and must be accounted for.

### 2. Capability concept normalization

The fourth v13 qualification used exact evidence correctly but normalized its concept as:

```text
Ability to produce visual content full-time and part-time
```

That concept mixes:

- a qualification wrapper (`Ability to ...`),
- the underlying capability (visual-content production), and
- work-schedule wording (`full-time and part-time`).

The reusable capability concept should name the underlying capability while preserving the full
exact source text as evidence.

## v14 design

v14 keeps v13's exact item coverage and deterministic provenance ownership but makes decomposition
complete.

When a broad requirement span is suppressed, JobHunter now exposes two candidate-only subcoverage
surfaces:

1. mandatory exact qualification-item references;
2. exact residual sentences remaining after the qualification list.

Mandatory qualification items cannot be excluded. Residual sentences must be either extracted as
requirements or explicitly excluded as non-requirement context.

For `t4jp`, the expected residual evidence is:

```text
the work is teachable.
Ethics and your work commitment are important to us.
Please do not send your resume for remote work.
(Location: West Tehran) Benefits include ...
```

Expected semantic disposition:

- teachability → exclude as non-career qualification context;
- ethics/work commitment → extract as explicit employer expectation;
- remote-work application instruction → exclude as application/logistics context;
- location/benefits → exclude as non-qualification context.

v14 also rejects capability concepts that retain an `Ability to ...` wrapper or `full-time` /
`part-time` schedule wording. Exact evidence is not modified.

## Ownership boundary

```text
model:
  semantic claim / concept / obligation / residual classification

JobHunter:
  exact evidence references
  complete source accounting
  deterministic coarse-span decomposition
  durable provenance
```

This preserves the established principle that deterministic bookkeeping is not delegated to the
model while avoiding the opposite failure of suppressing source evidence that still requires
semantic classification.

## Production isolation

Public P1.6 remains:

```text
job-analysis-english-v9
job-analysis-v4
```

v14 is candidate-only. The normal `jobhunter jobs analyze` path and accepted dense `tG9K` artifact
29 remain unchanged until heterogeneous acceptance succeeds.

## Implementation

```text
src/jobhunter/analysis_service_v14.py
src/jobhunter/analysis_runtime_v14.py
src/jobhunter/inference/instructor_lm_studio_v13.py  # optional candidate subcoverage seam
src/jobhunter/p16_v14_snapshot.py
src/jobhunter/p16_v14_audit.py
scripts/run_p16_v14_candidate.py
scripts/export_p16_v14_candidate_snapshot.py
scripts/audit_p16_v14_candidate_snapshot.py
tests/test_analysis_v14_candidate.py
```

The shared v13 Instructor helper gained an optional additional-coverage parameter. Existing v13
behavior is unchanged because v13 does not supply that parameter.

## Repository gate

Exact implementation head:

```text
020e828a859ade4d553624f1a5b55a8b2aa3a890
```

CI run 661:

```text
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## Sparse acceptance gate

Run v14 on `t4jp` only.

Require mechanically:

- 3/3 structured required skills;
- 4/4 qualification-list items;
- complete residual coverage decisions;
- at least one `decomposed_requirement` record;
- no qualification-derived responsibility;
- no capability concept containing the `Ability to ...` wrapper or full-time/part-time schedule
  wording.

Then perform full semantic review.

Sparse semantic PASS additionally requires:

- ethics and work commitment preserved as explicit employer expectation(s);
- teachability excluded;
- remote-work application instruction excluded;
- location/benefits excluded;
- visual-content-production concept normalized without schedule wording;
- no unsupported depth, duties, tooling, engineering scope or role purpose.

Only after sparse semantic PASS may v14 be run on dense `tG9K` and compared against accepted v9
artifact 29. Capability must not be generated above `t4jp` before P1.6 passes.
