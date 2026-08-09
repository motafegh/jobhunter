# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-09  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** B3 / SQ-2 Capability Intelligence  
**Purpose:** Resume from the real current repository state without reconstructing the recent semantic-calibration work from chat history.

This file is not a controlling specification. Higher-authority product/domain/source/architecture, roadmap, implementation, Phase-1, focused acceptance, and TODO documents win on conflict.

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

Current architecture remains a local Python modular monolith with SQLite structured state, immutable evidence, FastAPI/Uvicorn/Jinja browser UI, shared CLI services, and local-first LM Studio. Do not introduce Node/npm/React, vector/RAG, graph DB, generic plugin frameworks, or agent orchestration without demonstrated need.

## 2. Current contracts

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability candidate:         job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Blueprint:                    role-capability-blueprint-v2
Blueprint schema:             role-capability-blueprint-v1

Review Snapshot:              job-review-snapshot-v1
```

Current controlled model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e2b-it
```

## 3. Accepted upstream anchor

`tG9K` is the dense semiconductor/industrial-ML acceptance case.

Fixed upstream chain:

```text
English projection artifact 33
→ accepted English P1.6 artifact 29
```

Artifact 29 is B2/SQ-1 accepted:

- 7 responsibilities;
- 27 requirements;
- all 28 requirement-coverage inputs accounted for;
- all 8 duty-coverage inputs accounted for;
- explicit optionality preserved;
- explicit depth preserved;
- Python `expert` does not spread to neighboring frameworks;
- education and 3–6 years experience are present.

Do **not** rerun English analysis for current Capability calibration.

## 4. Capability history

### v4/v2

Capability artifact 7 was structurally valid but failed B3 semantic review:

- accepted explicit depth disappeared;
- contextual frameworks/cloud were over-strengthened;
- pipelines/MLOps became unsupported end-to-end ownership;
- evidence leaked across capability areas.

### v5

Historical prompt-heavy experiment. Focused deterministic tests passed, but live bounded retry exhausted `max_tokens`; no accepted artifact. Do not reuse v5 identity.

### v6/v3 — live artifact 8, rejected

v6 added profile source indices plus deterministic requirement-strength and explicit-depth reconciliation.

The live `tG9K` generation completed and proved the mechanism works **for linked facts**, but B3 failed:

- only requirements `[22, 23, 3]` were linked out of 27;
- only responsibilities `[0, 3]` were linked out of 7;
- only `Strong` and `Hands-on` depth survived into profiles;
- Python `expert`, statistics `Solid`, high-dimensional-data `Comfort`, and 3–6 years were absent from the profile-level view;
- unsupported autonomy reappeared;
- unsupported end-to-end lifecycle ownership reappeared;
- contextual tools/cloud were still strengthened in prose;
- the dense role collapsed into one catch-all capability;
- cross-capability synthesis existed despite one profile;
- exact evidence could still be semantically irrelevant.

Committed negative review snapshot:

```text
review-snapshots/jobs/tG9K.json
Capability artifact 8
job-capability-intelligence-v6 / v3
```

## 5. Current v7/v4 design

v7 moves source survival outside LLM control:

```text
accepted P1.6
→ deterministic source partition
→ model grouping + derived reasoning draft
→ complete coverage validator
→ deterministic source_truth / strength / explicit depth / explicit work
→ persisted v7 artifact
```

### Source partition

For capability grouping, all accepted requirements are capability-relevant except narrowly mechanical role-level constraints:

- education;
- standalone experience-duration constraints such as `three to six years`.

For current `tG9K` this should produce:

```text
capability requirements: 0..24
role-level requirements:  [25, 26]
responsibilities:         0..6
```

### Hard coverage

The model draft must link:

- every capability-relevant requirement;
- every responsibility.

Dense sources (>=12 requirements and >=5 responsibilities) require at least two profiles. Missing coverage is a validation failure rather than silent loss.

### Persisted source truth

`source_truth` deterministically retains:

- complete role purpose;
- all 27 requirements with index/type/strength/depth/evidence/confidence;
- all 7 responsibilities;
- role-level/capability partition;
- linked/unlinked coverage;
- all explicit-depth indices.

### Deterministic profile facts

JobHunter owns:

- `requirement_strength`;
- source-explicit depth;
- source-explicit work activities.

The model supplies semantic grouping and derived reasoning only.

### Deliberately deferred

Because two live artifacts repeatedly overreached:

- positive `independence_expectation` is cleared in v7; exact autonomy remains unknown unless a future explicit authority contract is designed;
- `cross_capability_observations` are cleared in v7; broader professional synthesis belongs downstream after Capability itself is accepted.

## 6. Current implementation files

Current public runtime:

```text
src/jobhunter/capability_service.py
→ re-exports v7 current service
```

New/changed v7 files:

```text
src/jobhunter/capability_v7_models.py
src/jobhunter/capability_service_v7.py
src/jobhunter/capability_inference.py
tests/test_capability_v7.py
tests/test_capability_inference.py
scripts/audit_capability_v7_snapshot.py
```

Historical v6 service is retained at:

```text
src/jobhunter/capability_service_v6.py
```

Experiment records:

```text
docs/experiments/2026-08-09_CAPABILITY_V6_DETERMINISTIC_RECONCILIATION.md
docs/experiments/2026-08-09_CAPABILITY_V7_SOURCE_TRUTH_BOUNDARY.md
```

## 7. Deterministic status

Current v7 implementation CI is green on `main`:

```text
ruff check .                  PASS
python -m pytest             PASS
python -m pytest -W error    PASS
```

B3 is still **not accepted** because the live v7 semantic artifact has not yet been reviewed.

## 8. Exact next action

Keep the accepted P1.6/model setup fixed.

Local sequence:

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v7_snapshot.py
```

Do not run:

```text
Analyze English / P1.6 again
Blueprint
full jobhunter run
```

until the v7 B3 decision is made.

Expected mechanical result for `tG9K`:

```text
Capability v7/v4 current-chain
>= 2 capability profiles
25/25 capability requirements linked
7/7 responsibilities linked
source_truth retains all 27 requirements
source_truth retains all 7 responsibilities
source_truth retains all 6 explicit depth signals
role-level requirement indices [25, 26]
no positive independence expectation
cross_capability_observations []
no current Blueprint
```

A mechanical pass is necessary but not sufficient.

## 9. Semantic review after the live push

Review whether:

- capability groupings are coherent rather than coverage-driven catch-alls;
- contextual/preferred tools remain contextual/preferred in prose;
- cloud/edge is not turned into required architecture;
- evidence is directly relevant to each derived claim;
- prerequisites are technically defensible rather than generic curriculum;
- unknown boundaries are useful;
- no hidden ownership/autonomy language reappears elsewhere;
- the artifact is materially more useful than P1.6.

### Decision after review

If v7 passes:
1. mark B3/SQ-2 accepted;
2. reconcile accepted-state docs;
3. move to B4 Blueprint calibration.

If v7 is mechanically valid but E2B remains semantically weak:
1. keep source/P1.6/prompt/schema/rubric fixed;
2. run a controlled stronger Capability-model comparison;
3. compare technical correctness/calibration, not prose quality.

If v7 fails completeness/validation/output-budget:
1. inspect the exact failure/attempt;
2. prefer bounded partitioning/output reduction or a justified model comparison;
3. do not respond with another large prompt-patch collection.

## 10. Phase sequence after B3

```text
B4 Blueprint calibration/model comparison if needed
→ B5/CI-3 heterogeneous review
→ Market truthfulness
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 final report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```
