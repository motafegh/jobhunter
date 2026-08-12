# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-12  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** heterogeneous semantic validation of P1.6 + Capability v7; isolated P1.6 v12 candidate active on sparse `t4jp`  
**Purpose:** Resume from the real repository state without reconstructing recent semantic-calibration work.

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
English P1.6 candidate:       job-analysis-english-v12
Candidate schema:             job-analysis-v4
Status:                       NOT promoted; sparse + dense validation required
```

Historical sparse candidates:

```text
v9 artifact 30  → rejected
v10 artifact 31 → mechanical PASS / semantic FAIL
v11             → failed closed before persistence: evidence-reference protocol mismatch
v12             → active isolated candidate
```

The normal `jobhunter jobs analyze` path remains v9. Candidate-only v12 tooling is listed below.

Current configured model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental only
```

Analysis/Blueprint runtime automatically prepare LM Studio rather than requiring manual model/context commands.

## 3. Accepted dense `tG9K` chain

```text
English projection artifact 33
→ accepted English P1.6 v9 artifact 29
→ accepted Capability v7 artifact 9
```

P1.6 artifact `29` remains the dense accepted baseline:

- 27 requirements;
- 7 responsibilities;
- deterministic coverage accounting;
- optionality preserved;
- Python-specific `expert` depth preserved;
- MATLAB/C++ preferred;
- contextual stack contextual;
- education and 3–6 years experience retained.

Capability artifact `9` remains the bounded accepted B3 baseline:

- 25/25 capability-relevant requirements linked;
- 7/7 responsibilities linked;
- all 27 requirements retained in deterministic source truth;
- six explicit depth facts retained;
- education/experience role-level partition retained;
- no positive ownership/independence synthesis;
- no cross-capability synthesis.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze Capability v7 unless heterogeneous evidence reveals a repeatable material defect. If P1.6 is promoted to a new identity, Capability v7 must be rebuilt against the promoted analysis artifact; do not reuse v9-linked Capability artifacts.

## 4. Blueprint experiment conclusion

Blueprint is implemented but **not accepted for Phase-1 decisions**.

Best bounded experimental evidence remains:

```text
job: tG9K
Blueprint artifact: 7
analysis artifact: 29
Capability artifact: 9
prompt/schema: role-capability-blueprint-v6 / role-capability-blueprint-v5
model: gemma-4-12b-it-qat
snapshot commit: 671bd6e3c43555c631958531671a0f1be9726554
```

Mechanical checks passed, but semantic review still found source-unstated feedback-loop/platform/implementation assumptions. Do not create Blueprint v7, weaken its validators, or reopen nearby model shopping during Phase 1.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## 5. CI-3 heterogeneous validation

Target stack:

```text
source
→ English projection
→ semantically accepted P1.6 for that job
→ Capability v7 only after P1.6 passes
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
→ matching mechanical audit
→ inspect source / projection / P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
```

Do not patch one vacancy at a time. Repeatable deterministic failures become tests; model limitations are documented separately.

## 6. Sparse `t4jp` source/projection

Current source facts:

```text
job detail version: 41
English projection: artifact 34
title:              Artificial Intelligence Expert
category:           Content Production and Management
education:          it doesn't matter
experience:         it doesn't matter
```

Structured required skills:

```text
Artificial Intelligence
Video content production
social networks
```

Sparse English description begins:

```text
Skills in content creation with AI, creativity in creating visual and video content,
website design, ability to produce visual content full-time and part-time, the work is
teachable. Ethics and your work commitment are important to us. ...
```

No explicit responsibility section exists.

## 7. `t4jp` v9 artifact 30 — rejected

```text
prompt/schema:    job-analysis-english-v9 / job-analysis-v4
artifact:         30
responsibilities: 1
requirements:     4
snapshot commit:  f77f1378ad638eba5ab66ccd36762386a140eabd
```

General defects:

1. top-level structured `skills[]` were outside deterministic requirement coverage, allowing explicit `social networks` to disappear;
2. qualification wording (`ability to ...`) was paraphrased into a responsibility despite no explicit duty section.

Capability must not be generated above artifact `30`.

## 8. `t4jp` v10 artifact 31 — mechanical PASS / semantic FAIL

v10 added exact structured-skill coverage and stricter qualification-vs-duty validation.

Live result:

```text
prompt/schema:       job-analysis-english-v10 / job-analysis-v4
artifact:            31
model:               gemma-4-e4b-it-ud
responsibilities:    0
requirements:        7
structured skills:   3/3
mechanical audit:    PASS
snapshot commit:     23348b2
```

v10 fixed its targeted defects but still failed semantic acceptance because coarse description coverage allowed explicit neighboring qualifications to disappear. Artifact `31` omitted distinct source facts including:

```text
Skills in content creation with AI
creativity in creating visual and video content
```

The broad structured tag `Artificial Intelligence` is not semantically equivalent to the narrower `content creation with AI` qualification.

Therefore:

- artifact `31` is rejected;
- do not run Capability above it;
- do not run dense `tG9K` under v10;
- v10 is concluded, not active.

Decision record:

```text
docs/experiments/2026-08-12_P16_V10_SPARSE_STRUCTURED_SKILLS_BOUNDARY.md
```

## 9. P1.6 v11 — failed evidence-reference protocol experiment

v11 correctly introduced generic qualification-list granularity and identified these four exact `t4jp` items:

```text
Skills in content creation with AI
creativity in creating visual and video content
website design
ability to produce visual content full-time and part-time
```

It also defined coarse-span supersession with durable:

```text
decomposed_requirement
```

provenance.

However the first live v11 generation failed closed before persistence:

```text
P1.6 v11 omitted explicit qualification-list items: all four expected items
```

Root cause was model-facing evidence protocol, not list detection. Production P1.6 tells the model to cite supplied `evidence_references` IDs, while v11 supplied its mandatory qualification items as separate raw strings under `candidate_required_qualification_spans`. Those strings were valid exact source excerpts but were not first-class evidence references. The bounded repair repeated the missing raw spans without resolving that contradiction.

Therefore:

- no v11 `t4jp` artifact was persisted;
- v11 is concluded as an evidence-plumbing failure;
- the failure is not classified as proof of model semantic incapability;
- v11 identity is not mutated in place.

Decision record:

```text
docs/experiments/2026-08-12_P16_V11_EVIDENCE_PROTOCOL_FAILURE_AND_V12_REFERENCE_FIX.md
```

## 10. Isolated P1.6 v12 candidate — active

Candidate identity:

```text
job-analysis-english-v12
job-analysis-v4
```

v12 preserves the v11 semantic boundary and changes the candidate evidence plumbing so every deterministic qualification item is addressable through the normal P1.6 reference protocol.

The isolated v12 runtime creates a temporary exact-source alias field only inside the inference call:

```text
__candidate_qualification_evidence
```

For `t4jp`, Instructor then exposes normal evidence IDs:

```text
field:__candidate_qualification_evidence:0
field:__candidate_qualification_evidence:1
field:__candidate_qualification_evidence:2
field:__candidate_qualification_evidence:3
```

The model receives those IDs in:

```text
candidate_required_qualification_references
```

and must cite each ID in a separate requirement. Instructor canonicalizes emitted IDs back to exact source text before persistence.

Trust boundary:

- every alias value is an exact contiguous excerpt already present in the real description;
- no inferred/paraphrased text is added to the evidence catalog;
- the persisted English projection is not mutated;
- production/public v9 Instructor and analysis paths remain unchanged.

v12 retains:

- v10 structured `skills[]` coverage;
- qualification-vs-duty protection;
- v11 qualification-list granularity;
- coarse requirement-span supersession;
- truthful `decomposed_requirement` provenance.

Implementation/tooling:

```text
src/jobhunter/analysis_service_v12.py
src/jobhunter/analysis_runtime_v12.py
scripts/run_p16_v12_candidate.py
scripts/export_p16_v12_candidate_snapshot.py
scripts/audit_p16_v12_candidate_snapshot.py
tests/test_analysis_v12_candidate.py
```

The v12 implementation gate is green:

```text
Ruff:                    PASS
full pytest:             PASS
warnings-as-errors:      PASS
```

This proves code-path correctness only, not sparse semantic acceptance.

Decision record:

```text
docs/experiments/2026-08-12_P16_V11_EVIDENCE_PROTOCOL_FAILURE_AND_V12_REFERENCE_FIX.md
```

## 11. Exact next work

Do **not** run Capability for `t4jp` and do **not** run `tG9K` v12 yet.

Next:

1. run isolated v12 on `t4jp`;
2. if generation succeeds, export its candidate snapshot;
3. run the v12 mechanical audit;
4. commit/push the snapshot;
5. review every v12 requirement/responsibility and coverage disposition against source/projection;
6. only if sparse v12 passes semantic review, run dense `tG9K` v12 regression against accepted artifact `29`;
7. only if sparse+dense pass, decide whether v12 should replace public v9;
8. only after P1.6 promotion/acceptance, rebuild and review Capability v7 on the promoted identity.

Candidate commands:

```bash
python scripts/run_p16_v12_candidate.py --job-id t4jp
python scripts/export_p16_v12_candidate_snapshot.py --job-id t4jp
python scripts/audit_p16_v12_candidate_snapshot.py --job-id t4jp
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
