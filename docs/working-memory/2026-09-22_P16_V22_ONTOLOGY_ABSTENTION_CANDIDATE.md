# P1.6 v22 — ontology abstention candidate

**Date:** 2026-09-22  
**Status:** FIRST EVALUATION CLOSED / EVIDENCE-ALIAS REPAIR UNDER CI GATE  
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

## First non-persistent evaluation result

The one authorized evaluation was executed against the unchanged public `tvMm` English projection and
configured model. It failed closed after the provider's bounded validation retry. SQLite was unchanged.

The exact failure was:

```text
exact_item_concept_type_mismatch=[
  'field:description:v21:candidate:1=built an Agent yourself to date:experience'
]
```

Generation 1 had correctly emitted `concept_type=experience` for `built an Agent yourself to date`.
The defect was in v22's own pre-validator: it compared the model's raw evidence reference ID with the
candidate plan's source sentence before inherited evidence resolution. The lookup therefore missed the
exact checklist item and downgraded the valid experience label to `other`. Inherited v21 coverage then
correctly rejected the resulting mismatch.

Generation 2 responded to that validation error by changing the item to `skill`; v21 again correctly
rejected it because this exact checklist item is source-backed prior experience.

No artifact or operational state was produced.

## Evidence-alias repair

V22 now resolves the raw evidence value through the existing exact evidence catalog using the same
`_raw_evidence_text` boundary already owned by the earlier typed runtime before deciding whether
`experience` is source-proven.

This is a mechanical evidence-resolution repair, not a new ontology rule:

```text
raw evidence reference
→ resolve exact source evidence
→ check exact source-backed experience item / prior-exposure marker
→ preserve explicit experience OR abstain capability-only experience to other
```

New regressions reproduce the live reference-ID shape at both requirement and full-response scope.

Implementation: `f5a14a1`  
Response-level regression: `8383bc7`

An intermediate CI run exercised the resolver implementation with Ruff PASS, 702 tests PASS, and 702
warnings-as-errors PASS; it was marked cancelled only after successful quality steps due workflow
concurrency. The current-head response-level regression still requires a clean CI.

## Conditional post-repair evaluation decision

The original evaluation is closed. Do not treat the next call as an automatic retry.

Exactly one new non-persistent v22 evaluation becomes authorized only if the current pushed-head repair
CI passes all gates. That evaluation must use the unchanged `tvMm` projection, unchanged configured
model, existing provider limits, no SQLite/service persistence, no artifact/review/current-routing/corpus
mutation, and no vacancy/model switch.

If the repaired evaluation fails transport, validation, coverage, or semantic review, close it without
another invocation. If it passes complete semantic review, use that only as evidence for a separate v22
promotion/integration decision; I7 remains HOLD until a later accepted-current persisted chain exists.
