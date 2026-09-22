# P1.6 v22 — ontology abstention candidate

**Date:** 2026-09-22  
**Status:** OFFLINE GATES PASSED / ONE NON-PERSISTENT EVALUATION AUTHORIZED  
**Current public English contract:** `job-analysis-english-v21 / job-analysis-v5`  
**Candidate:** `job-analysis-english-v22 / job-analysis-v5`

## Problem

The first normal persisted v21 `tvMm` run after promotion failed closed after its bounded validation
retry. The second generation corrected two invalid depth fields but again labeled the source-backed
capability `turn an Agent into a reliable system in a real product` as `concept_type=experience`.

The source states a required capability. It does not state that the candidate previously performed that
exact work. V21 correctly rejected the unsupported historical-experience interpretation.

## Design decision

V22 introduces one narrow fail-soft ontology rule under a distinct prompt/runtime identity.

When all of the following are true:

1. the requirement itself is source-backed and otherwise valid;
2. the model labels it `concept_type=experience`;
3. the exact candidate item does not prove prior applied exposure; and
4. no exact source-backed checklist item explicitly requires experience,

JobHunter preserves the factual requirement but changes only the unsupported ontology label to
`concept_type=other`.

This is an abstention, not a semantic guess. V22 does not deterministically choose `skill`,
`practice`, `knowledge`, or another specific ontology merely because `experience` is unsupported.

## Preserved boundaries

V22 inherits v21:

- exact item scope and parent evidence;
- obligation and preferred-parent inheritance;
- technical-depth validation;
- headingless candidate-experience coverage;
- compound/mixed fact coverage;
- responsibility/duty coverage;
- subject attribution and source-section boundaries;
- fail-closed provenance and exact-source validation;
- candidate-only `item_excerpt` removal before unchanged v5 persistence.

Explicit prior experience remains experience. Source-backed exact checklist items typed as experience
remain experience. Non-experience model labels are not rewritten.

## Downstream compatibility

The accepted P1.6 schema already permits `concept_type=other`. Capability's deterministic source truth
for requirement strength/depth does not depend on this ontology label. Market aggregation preserves
source concept types transparently as grouping metadata. Therefore neutral abstention does not manufacture
stronger downstream authority.

## Offline evidence

Implementation:

- `src/jobhunter/inference/instructor_lm_studio_v22.py`
- `src/jobhunter/analysis_service_v22.py`
- `src/jobhunter/analysis_runtime_v22.py`
- `tests/test_analysis_v22_ontology_abstention.py`

Evidence includes:

- capability-only item mislabeled experience → `other`;
- explicit practical experience → remains `experience`;
- exact candidate-experience checklist item → remains `experience`;
- knowledge and other non-experience labels → unchanged;
- the exact `tvMm` reliable-product shape validates through ontology abstention;
- v5 persistence still removes candidate-only `item_excerpt`;
- current routing remains v21;
- all six accepted historical experience requirements preserve their exact type;
- v22 inherits exactly the v21 requirement and responsibility ledgers for all 27 public English projections;
- explicit v22 runtime metadata records item-scoped evidence and ontology abstention.

CI run `1304 / 35761148349` passed:

```text
Ruff: PASS
pytest: 701 passed
pytest -W error: 701 passed
```

## Currentness

No promotion has occurred.

```text
public/current generation = v21/v5
accepted v20/v5 anchors = accepted-only compatibility-current
v22 = isolated candidate only
Market I7 = HOLD
```

Do not mass-regenerate accepted anchors and do not allow pending/rejected historical artifacts to cross
currentness boundaries.

## One authorized evaluation

The offline evidence is broad enough for exactly one direct non-persistent v22 provider evaluation using:

- unchanged public `tvMm` English projection;
- existing configured analysis model;
- existing provider/runtime limits;
- one normal bounded validation retry;
- no SQLite/service persistence;
- no analysis attempt/artifact;
- no corpus mutation;
- no current-routing change;
- no vacancy/model switch.

Review the complete merged structured result. It must preserve the required reliable-product capability
without inventing prior experience, architecture knowledge versus system-building experience, headingless
API/Agent/worked-with experience, exact familiarity depth, required/preferred strength, framework
alternatives, Python/TypeScript, all eleven duties, structured skill facts, and candidate-versus-product
subject boundaries.

Any transport, validation, coverage, or semantic failure closes this evaluation. Do not retry to obtain
PASS.

A semantically valid result is evidence for a separate bounded v22 integration/promotion decision. It is
not itself an accepted-current artifact and does not close Market I7.
