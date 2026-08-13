# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-13  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7; isolated P1.6 v15 candidate active on sparse `t4jp`  
**Purpose:** Resume from the real repository state without reconstructing recent semantic-calibration work.

This file is not controlling. Product/domain/source/architecture, roadmap, implementation, active acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict.

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
English P1.6 candidate:       job-analysis-english-v15
Candidate schema:             job-analysis-v4
Status:                       NOT promoted; sparse + dense validation required
```

The normal `jobhunter jobs analyze` path remains public v9. Candidate-only v15 tooling is listed below.

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

Freeze Capability v7 unless heterogeneous evidence reveals a repeatable material defect. If P1.6 is promoted to a new identity, Capability v7 must be rebuilt against the promoted analysis artifact; do not reuse v9-linked Capability artifacts.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

## 4. Blueprint experiment conclusion

Blueprint is implemented but **not accepted for Phase-1 decisions**.

Best bounded experimental evidence remains Blueprint artifact `7` on `tG9K` using `role-capability-blueprint-v6 / role-capability-blueprint-v5` and model `gemma-4-12b-it-qat`.

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

## 7. Sparse P1.6 experiment history

```text
v9 artifact 30
→ rejected: structured skills could disappear; qualification became responsibility

v10 artifact 31
→ mechanical PASS / semantic FAIL: coarse coverage lost explicit neighboring qualifications

v11
→ failed before persistence: qualification spans were not first-class evidence-reference IDs

v12
→ evidence-reference problem fixed
→ failed before persistence because coarse coverage still remained model-owned bookkeeping

v13 artifact 32
→ 0 responsibilities / 7 requirements
→ 3/3 structured skills + 4/4 qualification items
→ semantic FAIL: whole-span suppression hid Ethics/work commitment and one concept retained
  Ability-to + schedule wording

v14 artifact 33
→ 0 responsibilities / 8 requirements
→ 3/3 structured skills + 4/4 qualification items + 4/4 residual decisions
→ 1 decomposed coarse span / 12 coverage decisions
→ complete mechanical PASS
→ semantic FAIL only at remaining ontology/strength boundary:
   1. Work commitment and ethics typed as `skill` instead of behavioral/value `other`
   2. residual coverage mechanically forced `obligation_hint = required`
```

Artifact `33` is important positive evidence: v14 solved the earlier recall, qualification-vs-duty, residual-loss, concept-normalization, and schedule-vs-depth failure classes. It is still not promotable because P1.6 concept type and requirement strength are downstream facts too.

Capability must not be generated above rejected sparse artifacts `30`, `31`, `32`, or `33`.

Detailed records:

```text
docs/experiments/2026-08-12_P16_V10_SPARSE_STRUCTURED_SKILLS_BOUNDARY.md
docs/experiments/2026-08-12_P16_V10_SEMANTIC_FAILURE_AND_V11_QUALIFICATION_GRANULARITY.md
docs/experiments/2026-08-12_P16_V11_EVIDENCE_PROTOCOL_FAILURE_AND_V12_REFERENCE_FIX.md
docs/experiments/2026-08-13_P16_V12_COARSE_COVERAGE_FAILURE_AND_V13_DETERMINISTIC_DECOMPOSITION.md
docs/experiments/2026-08-13_P16_V13_SEMANTIC_FAILURE_AND_V14_COMPLETE_DECOMPOSITION.md
docs/working-memory/2026-08-13_P16_V15_HANDOFF.md
```

## 8. Isolated P1.6 v15 candidate — active

Candidate identity:

```text
job-analysis-english-v15
job-analysis-v4
```

v15 preserves all successful v14 mechanics:

- structured `skills[]` deterministic coverage;
- qualification-vs-duty protection;
- exact qualification-list evidence references;
- complete coarse-span decomposition;
- exact residual sentence coverage;
- durable `decomposed_requirement` provenance;
- normalized capability concepts;
- schedule-only depth normalization;
- strict exact evidence and source accounting.

v15 changes only two remaining boundaries.

### Residual coverage no longer forces strength

```text
coverage obligation != employer obligation strength
```

Residual coverage uses:

```text
obligation_hint = null
```

Every residual still must be extracted or explicitly excluded, but required/preferred/contextual must come from exact source wording. Mandatory qualification-list items remain required because their qualification-list context establishes that strength.

### Concept-type ontology is explicit

```text
skill      = ability/proficiency to perform a task/activity
tool       = named technology/instrument
knowledge  = subject-matter understanding
practice   = method/discipline
domain     = industry/problem area
experience = prior applied exposure
education  = credential
other      = candidate traits, values, behavioral expectations, professional qualities
```

The type decision remains model-owned semantic judgment plus human review. No vacancy-specific `ethics`/`commitment` keyword patch was added.

v15 deterministic implementation/tests are green:

```text
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## 9. Exact next work

Do **not** run Capability for `t4jp` and do **not** run dense `tG9K` v15 yet.

Next:

1. run isolated v15 on `t4jp`;
2. if generation succeeds, export its candidate snapshot;
3. run the v15 mechanical audit;
4. commit/push the snapshot;
5. review every v15 requirement/responsibility/coverage decision against source/projection;
6. verify `Work commitment and ethics` is represented as `concept_type = other` and strength is source-supported rather than mechanically forced;
7. only if sparse v15 passes semantic review, run dense `tG9K` v15 regression against accepted artifact `29`;
8. only if sparse+dense pass, decide whether v15 replaces public v9;
9. only after P1.6 promotion/acceptance, rebuild and review Capability v7 on the promoted identity.

Candidate commands:

```bash
python scripts/run_p16_v15_candidate.py --job-id t4jp
python scripts/export_p16_v15_candidate_snapshot.py --job-id t4jp
python scripts/audit_p16_v15_candidate_snapshot.py --job-id t4jp
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
