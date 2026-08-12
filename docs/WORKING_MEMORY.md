# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-12  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** heterogeneous semantic validation of P1.6 + Capability v7; isolated P1.6 v10 candidate active on sparse `t4jp`  
**Purpose:** Resume from the real repository state without reconstructing the recent semantic-calibration work.

This file is not controlling. Product/domain/source/architecture, roadmap, implementation, active acceptance plan, and TODO win on conflict.

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

Architecture remains a local Python modular monolith with SQLite structured state, immutable evidence, FastAPI/Uvicorn/Jinja browser UI, shared CLI services, and local-first LM Studio. Do not introduce Node/npm/React, vector/RAG, graph DB, generic plugin frameworks, or agent orchestration without demonstrated need.

## 2. Current contracts

Accepted/public baseline:

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

Active isolated acceptance candidate:

```text
English P1.6 candidate:       job-analysis-english-v10
Candidate schema:             job-analysis-v4
Status:                       NOT promoted; sparse + dense validation required
```

The normal `jobhunter jobs analyze` path remains v9 during the v10 experiment. Candidate-only tooling is listed below.

Current configured model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental only
```

Analysis runtime and Blueprint runtime automatically prepare LM Studio rather than requiring manual model/context commands. Blueprint remains non-authoritative regardless of runtime correctness.

## 3. Accepted dense `tG9K` chain

```text
English projection artifact 33
→ accepted English P1.6 v9 artifact 29
→ accepted Capability v7 artifact 9
```

### P1.6 artifact 29

Accepted bounded evidence:

- 27 requirements;
- 7 responsibilities;
- deterministic coverage accounting;
- optionality preserved;
- Python-specific `expert` depth preserved;
- MATLAB/C++ remain preferred;
- contextual stack remains contextual;
- education and 3–6 years experience present.

### Capability artifact 9

Accepted bounded evidence:

- 25/25 capability-relevant requirements linked;
- 7/7 responsibilities linked;
- two coherent Capability profiles;
- all 27 requirements remain in deterministic source truth;
- all six explicit depth facts remain in source truth;
- requirements 25/26 remain role-level;
- no positive ownership/independence expectation;
- no cross-capability synthesis.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze Capability v7 unless heterogeneous evidence shows a repeatable material correctness defect. If P1.6 is promoted from v9 to v10, Capability v7 must be rebuilt against the new accepted analysis artifact; do not reuse an artifact tied to v9.

## 4. Blueprint experiment conclusion

Blueprint is implemented but **not accepted for Phase-1 decisions**.

Experiment history:

```text
v3/v2 + E2B/E4B
→ provenance/index confusion + semantic overreach

v4/v3 + E4B
→ deterministic provenance fixed; broad prose still overreached

v5/v4 + E4B
→ Capability-derived prose removed; remaining free-form summary still inflated scope

v6/v5 + E4B
→ narrow contract; structured repair failed and assumptions remained

v6/v5 + gemma-4-12b-it-qat
→ mechanically valid and materially better; still violated explicit semantic boundary
```

Best bounded experimental Blueprint artifact:

```text
job: tG9K
artifact: 7
analysis artifact: 29
Capability artifact: 9
prompt: role-capability-blueprint-v6
schema: role-capability-blueprint-v5
model: gemma-4-12b-it-qat
snapshot commit: 671bd6e3c43555c631958531671a0f1be9726554
```

B4 failed semantic review because model-created unknowns/considerations still smuggled source-unstated feedback-loop/platform/implementation assumptions.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

Do not create Blueprint v7, weaken its validators, or reopen model shopping during Phase 1. Blueprint may be observed as non-gating research evidence only.

## 5. CI-3 heterogeneous validation

Target stack:

```text
source
→ English projection
→ accepted/candidate P1.6 under review
→ Capability v7 only after P1.6 for that job is semantically accepted
```

Target set:

```text
t4jp  sparse/ambiguous anchor — active
tG9K  rich industrial AI/ML baseline
+ Python/software
+ network/security
+ operations/platform/DevOps
```

Permanent workflow:

```text
snapshot current local state first
→ mechanical audit
→ inspect source / projection / P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
```

Do not patch one vacancy at a time. Repeatable deterministic failures become tests; model limitations are documented separately.

## 6. `t4jp` v9 result and rejection

The evidence-first workflow produced English P1.6 artifact `30`:

```text
job:             t4jp
translation:     artifact 34
English P1.6:    artifact 30
prompt/schema:   job-analysis-english-v9 / job-analysis-v4
model:           gemma-4-e4b-it-ud
role purpose:    0
responsibilities:1
requirements:    4
snapshot commit: f77f1378ad638eba5ab66ccd36762386a140eabd
```

Artifact `30` is **not accepted for sparse CI-3**.

The source/projection contains explicit structured required skills:

```text
Artificial Intelligence
Video content production
social networks
```

Two general defects were identified:

1. v9 `build_requirement_coverage_plan()` did not include top-level structured `skills[]`, so an explicit skill such as `social networks` could disappear while validation still passed;
2. sparse qualification wording (`ability to produce visual content...`) was paraphrased into a responsibility despite the existing qualification-vs-duty rule.

Therefore Capability must **not** be generated above artifact `30`.

Experiment record:

```text
docs/experiments/2026-08-12_P16_V10_SPARSE_STRUCTURED_SKILLS_BOUNDARY.md
```

## 7. Isolated P1.6 v10 candidate

Candidate identity:

```text
job-analysis-english-v10
job-analysis-v4
```

v10 remains isolated so the accepted `tG9K` v9 chain is not invalidated before regression proof.

Candidate invariants:

- every non-empty structured `skills[]` item must survive as an exact-evidence `required` requirement;
- structured skills receive deterministic persisted coverage accounting;
- responsibility output may not reuse exact qualification evidence;
- `ability to ...` and other obvious qualification wording may not be paraphrased into work;
- one bounded candidate correction is allowed after the existing Instructor/Pydantic validation; second failure fails closed.

Implementation/tooling:

```text
src/jobhunter/analysis_service_v10.py
src/jobhunter/analysis_runtime_v10.py
scripts/run_p16_v10_candidate.py
scripts/export_p16_v10_candidate_snapshot.py
scripts/audit_p16_v10_candidate_snapshot.py
tests/test_analysis_v10_candidate.py
```

The v10 implementation gate is green:

```text
Ruff:                    PASS
full pytest:             PASS
warnings-as-errors:      PASS
```

This proves code correctness only, not semantic acceptance.

## 8. Exact next work

Do not run Capability for `t4jp` yet.

Next exact sequence:

1. run isolated v10 on `t4jp`;
2. export the candidate snapshot;
3. run the v10 candidate mechanical audit;
4. commit/push the candidate snapshot;
5. review every `t4jp` v10 requirement/responsibility against source and English projection;
6. if sparse semantics pass, run the same v10 candidate on dense `tG9K` and compare against accepted artifact `29`;
7. only if sparse + dense pass, decide whether to promote v10 into the public P1.6 path;
8. only after P1.6 promotion/acceptance, build Capability v7 for the heterogeneous roles.

Candidate commands:

```bash
python scripts/run_p16_v10_candidate.py --job-id t4jp
python scripts/export_p16_v10_candidate_snapshot.py --job-id t4jp
python scripts/audit_p16_v10_candidate_snapshot.py --job-id t4jp
```

After heterogeneous semantic acceptance:

```text
Market truthfulness
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```
