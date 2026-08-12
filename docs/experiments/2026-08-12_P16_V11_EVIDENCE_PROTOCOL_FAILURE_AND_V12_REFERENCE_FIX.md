# P1.6 v11 Evidence-Protocol Failure and v12 Reference Fix

**Date:** 2026-08-12  
**Status:** Active isolated acceptance experiment; v12 is **not** promoted to the public P1.6 contract  
**Trigger job:** `t4jp`  
**Failed predecessor:** `job-analysis-english-v11` / `job-analysis-v4` (no artifact persisted)  
**Active candidate:** `job-analysis-english-v12` / `job-analysis-v4`

## 1. Live v11 result

The first live v11 run failed closed before persistence:

```text
P1.6 v11 candidate is not ready:
P1.6 v11 omitted explicit qualification-list items:
Skills in content creation with AI |
creativity in creating visual and video content |
website design |
ability to produce visual content full-time and part-time
```

Therefore:

- no v11 analysis artifact exists for `t4jp`;
- the v11 exporter correctly refused to export a v11 artifact;
- the v11 audit correctly saw the previously committed v10 snapshot and failed the expected-contract check.

This is not a snapshot/export defect.

## 2. Root cause

v11 correctly identified the four deterministic qualification-list spans and passed them to the model-facing payload as:

```text
candidate_required_qualification_spans
```

However the production P1.6 evidence protocol says that model claims should cite one supplied `evidence_references` ID. Instructor builds those references from `analysis_fields` and removes the raw `analysis_fields` object before the model-facing JSON is sent.

The v11 candidate spans were separate raw strings, not first-class entries in `evidence_references`.

That created a contradictory model contract:

```text
normal P1.6 rule:
  cite a supplied evidence-reference ID

v11 rule:
  cite these raw candidate spans exactly
```

Instructor's validator can mechanically canonicalize an exact raw source excerpt if the model emits one, but the model was explicitly trained by the surrounding prompt not to use raw evidence when references are available.

The bounded v11 correction repeated the missing raw spans but did not resolve the reference-protocol contradiction. The model therefore continued to omit all four candidate items.

This failure is classified as **candidate evidence-plumbing / protocol design**, not as proof that the local analysis model cannot represent the four source facts.

## 3. Why v12 gets a new identity

Although v11 persisted no successful artifact, it was executed as a real contract and its failed attempt is part of the analysis history. Changing its model-facing evidence semantics in place would make the same prompt identity refer to two different protocols.

The correction therefore receives a new identity:

```text
job-analysis-english-v12
job-analysis-v4
```

The JSON schema remains unchanged; the model-facing evidence protocol changes.

## 4. v12 evidence-reference design

v12 preserves all v11 semantic rules:

- structured `skills[]` coverage;
- qualification-vs-duty boundary;
- exact comma-list qualification granularity;
- broad legacy coverage supersession;
- durable `decomposed_requirement` provenance.

The only material correction is that deterministic qualification items become normal evidence-reference-addressable values **before inference**.

The isolated v12 runtime creates a temporary derived field:

```text
__candidate_qualification_evidence
```

whose values are exactly the already-detected qualification spans.

For `t4jp`, Instructor therefore generates normal references:

```text
field:__candidate_qualification_evidence:0
field:__candidate_qualification_evidence:1
field:__candidate_qualification_evidence:2
field:__candidate_qualification_evidence:3
```

The model-facing payload separately receives:

```text
candidate_required_qualification_references
```

containing those IDs.

The v12 rule is now consistent with the permanent P1.6 rule:

```text
Every required qualification ID must be cited by a separate requirement evidence field.
Use the supplied evidence-reference ID exactly.
```

Instructor canonicalizes each emitted ID back to the exact source text before persistence.

## 5. Trust boundary

The temporary derived field is **not** a new employer/source field.

Invariant:

```text
for every derived qualification value:
    value must already be an exact contiguous excerpt of the real description
```

The v12 regression suite proves that all generated alias values occur verbatim in the original analysis description. No inferred, normalized, or paraphrased text is added to the evidence catalog.

The derived alias exists only in the candidate inference call. It does not mutate the persisted English projection.

## 6. Why production v9 is unchanged

The v12 evidence alias is implemented only inside:

```text
V12CandidateAnalysisProvider
```

The shared production Instructor implementation, accepted v9 analysis service, evidence catalog, and normal `jobhunter jobs analyze` path are unchanged.

This avoids silently changing future v9 behavior while the candidate is still under heterogeneous acceptance.

## 7. Implementation

```text
src/jobhunter/analysis_service_v12.py
src/jobhunter/analysis_runtime_v12.py
scripts/run_p16_v12_candidate.py
scripts/export_p16_v12_candidate_snapshot.py
scripts/audit_p16_v12_candidate_snapshot.py
tests/test_analysis_v12_candidate.py
```

The v12 mechanical audit retains the v11 checks and additionally requires at least one durable:

```text
decomposed_requirement
```

coverage decision for the sparse `t4jp` coarse qualification span.

## 8. Regression result before live generation

Repository gate on the v12 implementation:

```text
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

The tests specifically prove:

- distinct v12 contract identity;
- deterministic candidate evidence IDs are generated;
- each ID resolves through the normal evidence catalog;
- each aliased value is exact source text already present in the real description;
- v12 semantic validation accepts the expected exact canonicalized evidence shape.

This proves code-path correctness only. It does not prove sparse semantic acceptance.

## 9. Acceptance sequence

### Gate A — sparse `t4jp`

Run only v12.

Require:

- 3/3 structured required skills survive exactly;
- 4/4 qualification-list items survive exactly;
- no qualification-derived responsibility;
- no false role purpose;
- broad coarse qualification evidence does not survive as a catch-all requirement;
- at least one coarse legacy coverage decision is persisted as `decomposed_requirement`;
- benefits/location/teachability/employment arrangement do not become career requirements or duties;
- concept normalization remains sensible and source-bounded;
- mechanical audit PASS;
- complete semantic review PASS.

### Gate B — dense `tG9K`

Only after sparse v12 passes, run the same v12 candidate on `tG9K` and compare with accepted v9 artifact `29`.

Require no material regression in the accepted dense facts, including optionality, depth, education/experience, and responsibility coverage.

### Promotion

Only after sparse + dense v12 acceptance should JobHunter decide whether to promote v12 into the public P1.6 path.

Do not run Capability above `t4jp` until the P1.6 candidate is semantically accepted.
