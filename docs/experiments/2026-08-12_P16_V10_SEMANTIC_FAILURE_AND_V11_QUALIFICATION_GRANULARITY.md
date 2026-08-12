# P1.6 v10 Semantic Failure and v11 Qualification Granularity

**Date:** 2026-08-12  
**Status:** Active isolated acceptance experiment; v11 is **not** promoted to the public P1.6 contract  
**Trigger job:** `t4jp`  
**Rejected predecessor:** artifact `31`, `job-analysis-english-v10` / `job-analysis-v4`  
**Active candidate:** `job-analysis-english-v11` / `job-analysis-v4`

## 1. Decision summary

P1.6 v10 fixed two important sparse-source defects:

- structured top-level required skills could no longer disappear;
- qualification wording could no longer be casually converted into responsibilities.

The live `t4jp` v10 artifact `31` therefore improved from v9 artifact `30`:

```text
v9 artifact 30
requirements:      4
responsibilities:  1
→ rejected

v10 artifact 31
requirements:      7
responsibilities:  0
structured skills: 3/3
mechanical audit:  PASS
→ semantic FAIL
```

The remaining failure was not hallucination or excess verbosity. It was **under-extraction caused by coarse deterministic coverage granularity**.

## 2. Exact v10 semantic failure

The hardened English description explicitly contains a comma-separated qualification sequence:

```text
Skills in content creation with AI,
creativity in creating visual and video content,
website design,
ability to produce visual content full-time and part-time,
the work is teachable.
```

Artifact `31` preserved `website design` and `Producing visual content`, but it did not preserve the distinct facts:

```text
content creation with AI
creativity in creating visual and video content
```

The structured skill tag:

```text
Artificial Intelligence
```

cannot substitute for the narrower source claim:

```text
Skills in content creation with AI
```

They have different semantic scope.

## 3. Root cause

The pre-existing v9 requirement coverage planner treats recognized requirement text as source segments/clauses. In this sparse posting, the qualification sequence survives as one broad segment rather than four independently auditable qualification items.

That creates an unsafe mechanical success condition:

```text
one broad paragraph/segment
→ one requirement cites that evidence
→ coverage says extracted_requirement
→ other explicit qualifications inside the same span may disappear
```

v10 added deterministic structured-skill coverage, but it did not change this description-side granularity.

Therefore v10 artifact `31` passed its mechanical checks while still losing source truth.

## 4. Why this becomes v11 rather than an in-place v10 change

Artifact `31` is already persisted with:

```text
job-analysis-english-v10
job-analysis-v4
```

Changing v10 semantics while retaining that identity would make artifact reuse and provenance dishonest. The correction therefore receives a new prompt/contract identity:

```text
job-analysis-english-v11
job-analysis-v4
```

The persisted JSON shape is unchanged; the semantic/validation contract changes.

## 5. v11 qualification-list boundary

v11 retains all v10 rules and adds a deterministic candidate list for **clearly introduced comma-separated qualification lists**.

A sentence is eligible only when its first comma-delimited clause starts with a generic qualification marker such as:

```text
skill / skills in
ability to
knowledge of
experience with / in
familiarity with
proficiency / proficient in / with
expertise in
competence / competency in
creativity in
understanding of
```

Subsequent short non-finite clauses may continue the list. Parsing stops when normal finite prose/directive wording resumes.

This is intentionally generic. It does not contain `t4jp`, Lora, AI, content-production, website, or social-network-specific rules.

Example:

```text
Skills in Python, SQL, Docker. The team builds internal tools.
```

becomes exact candidate qualification spans:

```text
Skills in Python
SQL
Docker
```

while:

```text
Benefits include insurance, parking, commission, annual bonus.
```

is not treated as a qualification list.

## 6. Required exact-item coverage

For every v11 candidate qualification span:

- a requirement must cite that exact span as evidence;
- a neighboring item cannot satisfy it;
- a broad paragraph cannot substitute for multiple items;
- qualification-list evidence cannot become a responsibility.

For current `t4jp`, v11 should deterministically require exact accounting for:

```text
Skills in content creation with AI
creativity in creating visual and video content
website design
ability to produce visual content full-time and part-time
```

in addition to the three top-level structured required skills already enforced by v10.

## 7. Coarse coverage supersession

The old v9 coverage plan may still contain one broad requirement-bearing description segment that contains multiple v11 item spans.

Keeping a broad requirement merely to satisfy that legacy coverage item would defeat v11's evidence-granularity goal. Therefore v11 uses a controlled decomposition rule:

```text
coarse requirement-bearing coverage span
+ multiple exact v11 qualification items
→ coarse span is superseded
→ model records its coverage reference in coverage_exclusions
→ granular exact requirements become authoritative claims
```

This is not semantically a `non_requirement` exclusion. The source span is requirement-bearing; it is simply decomposed.

Therefore v11 rewrites the durable coverage disposition for this case to:

```text
decomposed_requirement
```

rather than falsely retaining the legacy generic label:

```text
excluded_non_requirement
```

The exact item-level facts are persisted separately as:

```text
extracted_requirement
```

## 8. Bounded correction and failure behavior

The isolated v11 runtime keeps the same bounded philosophy as v10:

1. normal Instructor/Pydantic generation and validation;
2. v11 semantic validation;
3. at most one v11-specific correction request if needed;
4. revalidation;
5. fail closed on another violation.

No open-ended retry, model voting, or vacancy-specific prompt repair is introduced.

## 9. Candidate implementation

```text
src/jobhunter/analysis_service_v11.py
src/jobhunter/analysis_runtime_v11.py
scripts/run_p16_v11_candidate.py
scripts/export_p16_v11_candidate_snapshot.py
scripts/audit_p16_v11_candidate_snapshot.py
tests/test_analysis_v11_candidate.py
```

The regression suite covers:

- distinct v11 artifact identity;
- qualification-list detection;
- no benefits-list false positive;
- generic technical list (`Python, SQL, Docker`);
- missing-item rejection;
- broad/coarse-evidence rejection after decomposition;
- qualification-list evidence rejected as a responsibility;
- structured skill + granular list coverage persistence;
- truthful `decomposed_requirement` provenance.

## 10. Acceptance sequence

### Gate A — sparse `t4jp`

Run only v11 on `t4jp`.

Require:

- all 3 structured required skills survive exactly;
- all 4 explicit comma-separated qualification items survive exactly;
- no qualification-derived responsibility;
- no false role purpose;
- coarse source evidence is not reused as a catch-all requirement for multiple list items;
- any coarse legacy coverage span is truthfully marked `decomposed_requirement`;
- no location/benefits/teachability/employment-arrangement inflation;
- exact evidence and sensible concept normalization;
- mechanical audit PASS;
- complete semantic review PASS.

### Gate B — dense `tG9K` regression

Only after sparse v11 passes, run v11 against `tG9K` and compare with accepted v9 artifact `29`.

Require no material regression in:

- 27 requirements;
- 7 responsibilities;
- contextual/preferred strength;
- Python-only `expert` depth;
- MATLAB/C++ optionality;
- explicit depth facts;
- education and 3–6 years experience;
- dense duty/requirement coverage;
- evidence specificity.

### Promotion

Only if both sparse and dense gates pass should v11 be considered for promotion from isolated candidate to the public English P1.6 contract.

Promotion must update together:

- public analysis service identity;
- normal `jobhunter jobs analyze` routing;
- Review Snapshot selection;
- CI-3 audit identity;
- Phase-1 orchestration semantics;
- relevant docs;
- downstream current-chain expectations.

Capability v7 must then be rebuilt/reviewed against the promoted P1.6 artifact identity. Existing Capability artifacts tied to v9 must not be relabeled or silently reused.

## 11. Stop rules

Do not:

- run Capability above v9 artifact `30` or v10 artifact `31`;
- run `tG9K` v11 before sparse `t4jp` passes semantic review;
- promote v11 because CI or mechanical audit alone passes;
- weaken exact-item validators to accommodate model output;
- add Lora/AI/content-specific phrase patches;
- silently replace v9 in production before sparse+dense proof.
