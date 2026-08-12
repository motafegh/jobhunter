# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-12  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** heterogeneous semantic validation of P1.6 + Capability v7  
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

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5

Review Snapshot:              job-review-snapshot-v1
```

Current configured model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental only
```

Blueprint runtime uses automatic LM Studio model preparation with an 8,192-token context and exclusive LLM loading to avoid keeping multiple large LLMs resident. This is runtime behavior, not semantic acceptance.

## 3. Accepted dense `tG9K` chain

```text
English projection artifact 33
→ accepted English P1.6 artifact 29
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

Freeze Capability v7 unless heterogeneous evidence shows a repeatable material correctness defect.

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

### Best bounded experimental Blueprint artifact

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

Mechanical audit passed:

```text
2 Capability areas
25 deterministic source requirements
7 deterministic source responsibilities
4 professional considerations
4 important unknowns
2 role-level constraints
1 role-purpose item
```

CI passed too.

B4 still failed semantic review because some model-created unknowns/considerations smuggled source-unstated assumptions, including automated APC/SPC feedback-loop framing, assumed cloud/on-prem model-hosting choices, `raw sensor physics`, and strict data-lineage/model-weight versioning tied to unspecified quality standards.

Do not accept artifact 7 as employer truth or an authoritative downstream decision layer.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

### Phase-1 Blueprint rule

Do not:

- create Blueprint v7;
- weaken v6 validators;
- add vacancy/domain-specific prompt patches;
- continue adjacent model shopping;
- use Blueprint in Market, personal readiness, automatic recommendations, or other authoritative Phase-1 decisions.

Blueprint may be observed as non-gating research evidence only. Reopen only when a materially different grounding/inference approach or a demonstrated product-value gap justifies it.

## 5. Current active semantic gate

Validate the accepted stack across materially different roles:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Target set:

```text
t4jp  sparse/ambiguous anchor
tG9K  rich industrial AI/ML baseline
+ Python/software
+ network/security
+ operations/platform/DevOps
```

For each role inspect:

### P1.6

- factual false positives/negatives;
- responsibilities vs candidate qualifications;
- requirement strength;
- optional/contextual wording;
- explicit depth attachment;
- education/experience;
- evidence relevance/exactness;
- dense-source completeness vs sparse-source restraint.

### Capability v7

- complete capability-relevant requirement coverage;
- complete responsibility coverage;
- coherent grouping;
- role-level requirement partition;
- deterministic source truth;
- source strength/depth/work reconciliation;
- no unsupported ownership/autonomy;
- no contextual/preferred tool promotion.

Repeatable deterministic failures become tests. Model limitations are documented separately. Do not patch one vacancy at a time.

## 6. Current implementation notes

Blueprint v6 implementation remains:

```text
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v6.py
src/jobhunter/role_blueprint_inference_v6.py
src/jobhunter/role_blueprint_v6_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v6_snapshot.py
```

The current `tG9K` Review Snapshot contains accepted P1.6/Capability anchors plus rejected experimental Blueprint artifact 7. Current-chain status does not imply semantic acceptance.

`*.egg-info/` is ignored so editable installs do not dirty normal Git status.

## 7. Exact next work

Do **not** rerun `tG9K` Blueprint again for calibration.

Next:

1. choose/confirm the heterogeneous review jobs;
2. build or reuse their current English/P1.6/Capability chain;
3. export Review Snapshots;
4. review each source → English → P1.6 → Capability chain;
5. fix only repeatable general defects;
6. freeze P1.6 + Capability v7 when the bounded heterogeneous sample passes.

After semantic acceptance:

```text
Market truthfulness
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```
