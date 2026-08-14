# P1.6 v16 Dense Regression Failure and State Reconciliation

**Date:** 2026-08-14  
**Gate:** CI-3 heterogeneous P1.6 validation  
**Dense job:** `tG9K`  
**Status:** **v16 sparse acceptance stands; dense regression failed before persistence; no fix authorized yet**

## 1. Why this record exists

This file reconciles the current P1.6 calibration state after the first dense `tG9K` v16 run. It is intentionally a documentation/state record only. It does **not** authorize or implement a correction.

Earlier version-specific records remain valid for their historical scope. This file captures the pieces that were not yet written together in one current resume point, especially:

- what the v9→v16 sparse-calibration sequence established;
- what v14/v15/v16 implementation boundaries now exist;
- what sparse v16 actually accepted;
- what the dense-safe audit change did;
- exactly how the first dense v16 run failed;
- what additional semantic warning signals are visible in the failed outputs;
- what remains authoritative while the dense gate is blocked.

## 2. Current contract and authority state

Public/accepted production P1.6 is still:

```text
job-analysis-english-v9
job-analysis-v4
```

Dense accepted baseline remains `tG9K` artifact `29`.

Active isolated candidate is:

```text
job-analysis-english-v16
job-analysis-v4
```

v16 is accepted **only for the bounded sparse `t4jp` case**. It is not promoted to the public P1.6 identity and is not yet approved as the heterogeneous Phase-1 P1.6 contract.

Capability remains gated. Do not generate/rebuild Capability v7 above v16 until dense P1.6 regression passes and a P1.6 promotion decision is made.

## 3. Sparse calibration history — what each version proved

| Candidate | Result | Main lesson / failure class |
|---|---|---|
| public v9, artifact 30 on `t4jp` | rejected | structured `skills[]` could disappear; qualification wording leaked into responsibility |
| v10, artifact 31 | mechanical PASS / semantic FAIL | deterministic structured-skill coverage worked, but coarse description coverage still hid explicit neighboring qualifications |
| v11 | failed before persistence | qualification spans were supplied outside the evidence-reference protocol |
| v12 | failed before persistence | first-class qualification references worked, but old coarse coverage bookkeeping still remained model-owned |
| v13, artifact 32 | semantic FAIL | deterministic coarse decomposition worked, but whole-span suppression hid Ethics/work commitment; capability concept retained Ability-to/schedule wording |
| v14, artifact 33 | mechanical PASS / semantic FAIL | complete residual accounting worked; remaining defects were trait ontology (`skill` vs `other`) and residual coverage incorrectly forcing `required` |
| v15, artifact 34 | mechanical PASS / semantic FAIL | trait ontology and residual-strength separation worked; remaining defect was malformed normalization `Visual content production ( )` and unsupported `experience` typing for ability evidence |
| v16, artifact 35 | **sparse mechanical + semantic PASS** | clean visual-content concept, correct `skill` typing, complete source accounting, no fabricated duty/purpose, correct residual handling |

This sequence established a durable architectural direction:

```text
model owns bounded semantic interpretation
+
JobHunter owns deterministic evidence identity, mandatory coverage, provenance, accounting, and fail-closed guards
```

## 4. Implemented boundaries accumulated through v14→v16

The current candidate path now includes the following generic protections.

### Exact structured-skill coverage

Non-empty top-level `skills[]` entries are first-class source requirements and cannot silently disappear.

### Qualification-list itemization

Comma/list-like qualification text can be surfaced as exact item-level evidence instead of relying on one coarse paragraph reference.

### Deterministic coarse-span decomposition

When a coarse requirement span is superseded by exact item-level evidence, JobHunter owns the decomposition bookkeeping rather than asking the model to reconstruct it.

### Complete residual accounting

Residual sentences left after qualification decomposition must be either:

```text
extracted_requirement
or
excluded_non_requirement
```

They cannot silently disappear.

### Qualification-vs-responsibility boundary

Qualification wording is not allowed to become a responsibility merely because it describes an ability or availability.

### Coverage obligation vs employer strength

A source span being mandatory to account for does not imply the employer marked it `required`.

Residual coverage is strength-neutral; `required` / `preferred` / `contextual` must come from source semantics.

### Schedule-vs-depth boundary

Work-arrangement wording such as `full-time` / `part-time` cannot become a technical `depth_signal`.

### Capability-concept normalization

Reusable capability labels must not retain:

- `Ability to ...` linguistic wrappers;
- full-time/part-time schedule wording;
- empty punctuation debris introduced by cleanup.

Exact evidence remains unchanged.

### Concept-type ontology

The candidate contract explicitly distinguishes:

```text
skill      = ability/proficiency to perform an activity
knowledge  = subject-matter understanding
practice   = method/discipline
domain     = industry/problem area
tool       = named technology/instrument
experience = prior applied exposure
education  = credential
other      = traits, values, behavioral expectations, professional qualities
```

`experience` is not allowed merely because evidence says a candidate has an `ability to ...`; prior applied exposure must be supported by source evidence.

### Bounded correction and fail-closed behavior

The candidate provider receives one bounded correction opportunity after a validation failure. If the corrected response still violates mandatory source accounting or semantic guards, the run fails and no artifact is persisted.

## 5. Sparse v16 accepted artifact

`t4jp` v16 artifact `35` is the first sparse candidate in this sequence to pass both mechanical and semantic review.

Accepted shape:

```text
Requirements:      8
Responsibilities:  0
Role purpose:      0
Structured skills: 3/3
Qualification items: 4/4
Residual decisions: 4/4
```

The previously problematic source evidence:

```text
ability to produce visual content full-time and part-time
```

is represented as:

```text
concept:          Production of visual content
concept_type:     skill
requirement_type: required
depth_signal:     null
```

with exact evidence preserved.

This sparse acceptance is recorded separately in:

```text
docs/working-memory/2026-08-14_P16_V16_SPARSE_ACCEPTANCE.md
```

## 6. Dense-safe audit correction already completed

Before running dense `tG9K`, the v16 mechanical audit was reviewed and one **audit-only** assumption was corrected.

The original sparse audit unconditionally required at least one `decomposed_requirement`. That is valid for `t4jp`, where qualification/residual decomposition is active, but it is not a universal dense-role invariant.

The audit was generalized so decomposition is required only when the source actually activates qualification/residual decomposition. Dense roles can therefore be mechanically reviewed without a false sparse-only failure.

Regression coverage was added, and CI run 706 passed:

```text
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

This audit change did not modify v16 extraction semantics.

## 7. First dense `tG9K` v16 run — exact failure

Command:

```bash
python scripts/run_p16_v16_candidate.py --job-id tG9K
```

Outcome:

```text
FAILED before persistence
2 total generations: initial + 1 bounded validation retry
no v16 artifact created for tG9K
```

### Generation 1

The model produced:

```text
Role purpose:      1
Responsibilities:  7
Requirements:      32
Coverage exclusions: 0
```

The validator rejected it because the mandatory structured source field:

```text
field:minimum_experience
```

was neither cited by a requirement nor explicitly excluded.

Exclusion was not permitted for this required structured source fact.

Generation 1 **did include**:

```text
field:education → Master's degree
```

but omitted minimum experience.

### Generation 2 — bounded correction

The correction prompt successfully repaired the first missing fact:

```text
field:minimum_experience
→ Professional experience
→ depth_signal: three to six years
→ required
→ experience
```

Generation 2 again produced:

```text
Role purpose:      1
Responsibilities:  7
Requirements:      32
Coverage exclusions: 0
```

However, it then omitted:

```text
field:education
```

The validator therefore rejected the second generation with:

```text
Requirement coverage reference field:education must be cited by a requirement
or explicitly justified in coverage_exclusions
```

The bounded retry budget was exhausted, so the candidate failed closed.

## 8. Confirmed current failure class

The confirmed blocker is **simultaneous mandatory structured-field coverage under dense load**.

The model demonstrated that it can represent both facts individually:

```text
generation 1: education present, minimum_experience missing
generation 2: minimum_experience present, education missing
```

But the current model/correction interaction did not retain both mandatory structured fields in the same valid response.

This is not yet classified as a model-capability failure, deterministic-plumbing failure, prompt failure, or correction-strategy failure. That diagnosis is intentionally deferred until we decide how to investigate it.

No code change is authorized by this record.

## 9. Additional warning signals visible in the failed dense outputs

These are **not accepted artifacts** and therefore are not project truth. They are important observations to preserve for the eventual dense diagnosis.

### 9.1 Two accepted explicit depth signals disappeared in both failed generations

Accepted v9 dense baseline preserves:

```text
Statistics and signal-processing fundamentals → Solid
Experience applying AI/ML to industrial/manufacturing data → Strong
```

In both failed v16 generations, the corresponding requirements were present but had:

```text
depth_signal: null
```

At the same time, these accepted depth signals did survive:

```text
Python → expert
Process-control/manufacturing analytics experience → Hands-on
High-dimensional sensor/time-series data → Comfort
```

Generation 2 also preserved:

```text
Professional experience → three to six years
```

Therefore dense v16 must not be judged only by eventual mechanical coverage. If a later run persists, semantic review must explicitly verify all accepted depth signals, especially `Solid` and `Strong`.

### 9.2 Structured-skill coverage changes the dense requirement shape

Each failed v16 generation contained **32 requirements** despite omitting one mandatory structured field.

The accepted public v9 dense artifact has 27 requirements.

The v16 candidate also surfaced all six top-level structured skills as required requirements:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

This behavior is consistent with the structured-skill coverage rule introduced during sparse calibration, but it changes the dense representation materially.

If both education and minimum experience were retained at once, the candidate would be expected to contain roughly the accepted dense requirement set plus these structured-skill facts, subject to semantic reconciliation.

This is not automatically a regression: v9's inability to guarantee structured `skills[]` coverage was one of the defects discovered by the sparse case. But the new dense shape must be reviewed rather than assumed correct.

### 9.3 Same-concept multi-surface strength collision is now visible

The dense source exposes Python through at least two source surfaces in the failed response:

```text
structured skills[]: Python → required
prose stack:         Python (expert) → contextual + depth expert
```

The current failed outputs retained both as separate requirements.

This creates an open dense semantic/reconciliation question:

```text
How should JobHunter preserve both source truths for the same concept
without silently collapsing requirement strength, losing depth, or creating a misleading duplicate?
```

No answer is adopted yet. This must be reasoned about before any promotion decision.

### 9.4 Concept-type changes are visible but not yet classified as defects

Compared with the accepted v9 representation, the failed v16 outputs changed some ontology choices, for example:

- `SQL`: `skill` → `tool`;
- ML/DL frameworks: `knowledge` → `tool`;
- pandas/NumPy/SciPy/statsmodels: `knowledge` → `tool`;
- validation/reproducibility/documentation discipline: `knowledge` → `other`;
- several techniques moved between `knowledge` and `skill`.

Some of these may be improvements under the explicit v15/v16 ontology; some may be undesirable. Because no v16 dense artifact exists, they remain review observations only.

A future persisted dense candidate must receive a deliberate concept-type comparison rather than an automatic equality check against v9.

## 10. What remains good despite the failed dense run

The failed outputs still showed useful positive evidence:

- all 7 accepted dense responsibilities were recalled in both generations;
- the accepted role-purpose statement was recalled;
- preferred MATLAB and C/C++ remained preferred;
- contextual stacks remained contextual rather than being globally promoted;
- industrial/edge deployment remained preferred;
- `expert`, `Hands-on`, and `Comfort` were preserved;
- exact evidence-reference discipline remained active;
- mandatory coverage validation correctly prevented persistence of an incomplete artifact.

The failure therefore demonstrates the value of the fail-closed boundary: no partially incomplete dense candidate was allowed to become durable evidence merely because most of the response looked good.

## 11. Current accepted / rejected / blocked state

```text
Public P1.6 v9 on tG9K artifact 29
→ accepted dense baseline

Capability v7 artifact 9 on tG9K
→ accepted bounded baseline tied to P1.6 artifact 29

P1.6 v16 on t4jp artifact 35
→ accepted bounded sparse candidate

P1.6 v16 on tG9K
→ BLOCKED: first dense regression failed before persistence

P1.6 v16 public promotion
→ NOT AUTHORIZED

Capability v7 rebuild above v16
→ NOT AUTHORIZED

Further heterogeneous roles
→ wait until dense P1.6 regression decision
```

## 12. Current problem statement to resume from

The immediate technical question is no longer the sparse `t4jp` decomposition problem.

The current gate is:

> Can the v16 candidate preserve **all mandatory dense source facts simultaneously**, while also preserving the accepted dense optionality/depth semantics and truthfully reconciling newly enforced structured skills with overlapping prose requirements?

The first dense run says **not yet demonstrated**.

The next discussion should diagnose this question before implementation. In particular, distinguish:

1. mandatory structured-field coverage/retry behavior;
2. explicit-depth retention (`Solid`, `Strong`);
3. structured-skill + prose duplicate/reconciliation semantics;
4. ontology changes that are improvements vs regressions;
5. whether the correction belongs in deterministic accounting, model-facing evidence/coverage planning, prompt semantics, or another bounded layer.

Do not choose or implement a fix until that diagnosis is explicitly made.

## 13. Resume rule

When work resumes:

```text
start from this record
→ inspect the failed dense generations and accepted v9 baseline
→ classify confirmed defects vs semantic observations
→ decide the smallest generic correction
→ create a new candidate identity only if persisted/intended contract semantics materially change
→ keep public v9 and Capability v7 frozen until dense acceptance
```

Do not rerun acquisition, translation, accepted v9 P1.6, or Capability merely to obtain fresh artifacts. The dense failure is downstream of already-accepted source/English state.
