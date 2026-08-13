# P1.6 v12 Coarse-Coverage Failure and v13 Deterministic Decomposition

**Date:** 2026-08-13  
**Status:** Active isolated acceptance experiment; v13 is **not** promoted to the public P1.6 contract  
**Trigger job:** `t4jp`  
**Failed predecessor:** `job-analysis-english-v12` / `job-analysis-v4` (no artifact persisted)  
**Active candidate:** `job-analysis-english-v13` / `job-analysis-v4`

## 1. Live v12 result

The live v12 run proved that first-class qualification evidence references fixed the v11 evidence-protocol problem.

Generation 1 emitted all seven expected sparse requirements:

- 4 exact qualification-list items;
- 3 structured required skills;
- 0 responsibilities.

Instructor rejected one incorrect `depth_signal` because `ability to produce visual content full-time and part-time` is qualification wording, not a technical-depth or experience-extent signal.

Generation 2 corrected that field to `null` and retained the seven source-grounded requirements.

The remaining failure was:

```text
Requirement coverage reference field:description:segment:0 must be cited by a requirement
or explicitly justified in coverage_exclusions
```

No v12 artifact was persisted.

## 2. Root cause

The remaining failure was not semantic recall and not model capability.

JobHunter had already deterministically decomposed the broad qualification paragraph into exact item-level evidence references, but the generic Instructor coverage plan still required the model to account for the original coarse paragraph.

That created an unnecessary bookkeeping obligation:

```text
JobHunter knows coarse paragraph → exact qualification items
+
model must still emit coverage_exclusions for coarse paragraph
```

The model correctly focused on semantic claims and omitted the bookkeeping exclusion, so Instructor failed before candidate-specific persistence could mark the coarse span as `decomposed_requirement`.

## 3. v13 ownership correction

v13 makes the ownership boundary explicit:

```text
model owns semantic claims
JobHunter owns deterministic decomposition provenance
```

For a broad requirement-coverage reference to be suppressed before Instructor validation, JobHunter must mechanically prove:

1. the reference exists in the normal requirement coverage plan;
2. it is `allow_exclusion=True`;
3. its exact source text contains at least two deterministic qualification-list items.

Structured/non-excludable requirements such as education cannot be suppressed.

The broad reference remains available as source evidence, but it is removed from the model/Pydantic coverage checklist.

After generation, JobHunter deterministically injects the corresponding coverage exclusion into the internal structured result so legacy persistence can account for the source span. Durable coverage then records:

```text
decomposed_requirement
```

rather than pretending the source was a non-requirement.

## 4. Candidate identity and production isolation

```text
job-analysis-english-v13
job-analysis-v4
```

The accepted/public P1.6 path remains v9. The shared production Instructor function is unchanged.

v13 uses a candidate-only Instructor helper and candidate-only runtime. This prevents the acceptance experiment from silently changing production v9 behavior.

## 5. Implementation

```text
src/jobhunter/analysis_service_v13.py
src/jobhunter/analysis_runtime_v13.py
src/jobhunter/inference/instructor_lm_studio_v13.py
src/jobhunter/p16_v13_snapshot.py
src/jobhunter/p16_v13_audit.py
scripts/run_p16_v13_candidate.py
scripts/export_p16_v13_candidate_snapshot.py
scripts/audit_p16_v13_candidate_snapshot.py
tests/test_analysis_v13_candidate.py
```

Regression coverage proves:

- distinct v13 artifact identity;
- the sparse coarse requirement span is detected deterministically;
- only excludable coverage references may be suppressed;
- non-excludable structured requirements cannot be suppressed;
- deterministic decomposition bookkeeping is injected without model ownership;
- persistence records `decomposed_requirement`;
- exact qualification items and structured skills remain independently covered.

## 6. Repository gate

The v13 implementation passed:

```text
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

This proves implementation correctness only. It does not prove sparse semantic acceptance.

## 7. Exact acceptance sequence

### Gate A — sparse `t4jp`

Run only v13.

Require:

- 3/3 structured required skills;
- 4/4 granular qualification-list items;
- no qualification-derived responsibility;
- no false role purpose;
- `ability to ...` does not become a depth signal;
- broad coarse evidence does not become a catch-all requirement;
- at least one durable `decomposed_requirement` coverage decision;
- no benefits/location/teachability/employment-arrangement inflation;
- mechanical audit PASS;
- complete semantic review PASS.

### Gate B — dense `tG9K`

Only after sparse v13 passes, run v13 on `tG9K` and compare against accepted v9 artifact `29`.

Require no material regression in the accepted dense facts, optionality, depth, education/experience, or responsibility coverage.

### Promotion

Only after sparse + dense v13 acceptance should JobHunter decide whether to promote v13 into the public P1.6 path.

Do not run Capability above `t4jp` until the P1.6 candidate is semantically accepted.
