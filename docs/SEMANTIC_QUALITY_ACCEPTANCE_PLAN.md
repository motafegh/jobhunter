# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-09  
**Scope:** P1.6 factual extraction, Capability Intelligence, Role Capability Blueprint, model-role comparison, and selected Review Snapshots  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints.

This plan does not authorize corpus-wide Phase-2 taxonomy/Market-v2 work.

## 1. Permanent acceptance principle

Intelligence depth follows evidence density:

```text
sparse evidence
→ modest strong conclusions
→ explicit unknowns
→ limited architecture/tool speculation

rich evidence
→ deeper work-linked decomposition
→ richer supported interpretation
```

Current opposite-end anchors:

```text
t4jp  sparse/ambiguous source
tG9K  rich semiconductor/industrial-ML source
```

## 2. Current contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
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

Capability v7/v4 is implemented but **not accepted** until the live B3 artifact passes.

## 3. Permanent layer contract

```text
P1.6
→ factual substrate
→ exact employer/source-supported facts
→ conservative strength/depth/evidence

Capability Intelligence
→ auditable reasoning above P1.6
→ grouping, prerequisites/context, unknown scope
→ no loss or strengthening of accepted source truth

Role Capability Blueprint
→ later human-facing professional interpretation
→ useful likely scope/examples/scenarios with calibrated uncertainty
```

A downstream layer never upgrades an incorrect or uncertain upstream claim into truth.

## 4. SQ-0 — Review Snapshot correctness

**Accepted.**

The normal repository-native review workflow is:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records effective analysis/capability/blueprint models, dependency identities, and current-chain flags while excluding raw responses/prompts, SQLite, secrets, and private state.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Accepted on `tG9K` artifact 29.**

Acceptance evidence:

- 27 requirements;
- 7 responsibilities;
- complete deterministic coverage accounting;
- Python `expert` preserved only for Python;
- `MATLAB a plus` and `C/C++ helpful` preserved as preference/optional evidence;
- individually unspecified technical-stack obligation represented as contextual;
- `Solid`, `Strong`, `Hands-on`, `Comfort`, and experience-duration depth preserved;
- education and experience included;
- exact evidence retained.

Current analysis role:

```text
gemma-4-e4b-it-ud
```

Keep artifact 29 fixed during current B3 calibration.

## 6. SQ-2 — Capability Intelligence calibration

**Current gate: active / not accepted.**

### Historical negative evidence

v4/v2 artifact 7:
- omitted explicit depth;
- over-strengthened stack/cloud/ownership;
- evidence-area leakage.

v5:
- prompt-heavy experimental correction;
- bounded retry exhausted output budget;
- reverted; no accepted artifact.

v6/v3 artifact 8:
- deterministic strength/depth worked for linked facts;
- model linked only 3/27 requirements and 2/7 responsibilities;
- missing links silently removed accepted source information from the profile view;
- unsupported autonomy and end-to-end ownership reappeared;
- contextual tools/cloud remained over-strengthened;
- dense role collapsed into one profile;
- evidence relevance remained imperfect.

v6 is therefore rejected B3 evidence.

### Current v7 boundary

```text
accepted P1.6
→ deterministic source partition
→ model semantic grouping + derived reasoning draft
→ complete-coverage validation
→ deterministic source_truth / strength / explicit depth / explicit work
→ persisted v7 artifact
```

v7 guarantees:

- complete accepted P1.6 source truth persists independently of the model;
- every capability-relevant accepted requirement is linked;
- every responsibility is linked;
- education and standalone experience-duration constraints remain role-level truth;
- dense sources require actual multi-profile decomposition;
- profile `requirement_strength` is deterministic;
- source-explicit depth is deterministic;
- source-explicit work activity is deterministic;
- positive autonomy/ownership synthesis is deferred;
- cross-capability synthesis is deferred.

### Current v7 mechanical gate for `tG9K`

Run:

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v7_snapshot.py
```

Expected:

```text
P1.6 artifact 29 fixed
Capability v7/v4 current-chain
>=2 profiles
25/25 capability requirements linked
7/7 responsibilities linked
all 27 requirements retained in source_truth
all 7 responsibilities retained in source_truth
all explicit depth retained in source_truth
role-level requirement indices [25, 26]
no positive independence expectation
cross_capability_observations []
no current Blueprint
```

### SQ-2 semantic gate

Mechanical validity is necessary but insufficient. Reject B3 if the artifact:

- groups unrelated facts solely to satisfy coverage;
- promotes contextual/preferred tools to mandatory/mastery/essential without support;
- treats cloud/edge lists as required architecture;
- attaches exact but semantically irrelevant evidence;
- invents generic curricula/prerequisites;
- produces technically weak derived conclusions;
- hides important unknowns;
- recreates ownership/autonomy claims elsewhere;
- is not materially more useful than P1.6.

If v7 is mechanically correct but E2B reasoning remains inadequate, compare one stronger Capability model with source, English projection, P1.6, prompt/schema, and rubric held fixed. Do not add another prompt-patch collection first.

## 7. SQ-3 — Blueprint calibration

Blocked until SQ-2/B3 passes.

Permanent rules:

1. technology list != architecture;
2. source optionality survives downstream;
3. possible/likely examples remain examples;
4. `highly_likely` cannot contradict unresolved unknowns;
5. technical correctness outranks sophisticated prose;
6. scenario detail scales with evidence;
7. avoid domain-specific prompt patches.

## 8. SQ-4 — Controlled model-role comparison

Use only when current-model quality evidence warrants it.

Hold fixed:

```text
source semantic version
English projection
accepted P1.6
Capability/Blueprint contract
review rubric
```

Change only the model. Compare technical correctness, calibration, useful decomposition, unsupported inference, uncertainty, and usefulness per token/time.

No multi-model voting/ensemble.

## 9. SQ-5 / CI-3 — heterogeneous live acceptance

After B3/B4, review materially different jobs:

1. `t4jp` sparse/ambiguous;
2. `tG9K` rich AI/ML;
3. Python/software;
4. network/security;
5. operations/platform/DevOps.

For each selected case inspect:

```text
source
→ English
→ P1.6
→ Capability
→ Blueprint
```

Record factual false positives/negatives, strength/depth mistakes, evidence mismatch, capability decomposition/status mistakes, unsupported prerequisites, missing unknowns, Blueprint technical/certainty mistakes, and model limitations separately from deterministic defects.

## 10. Stop rule

Do not polish semantic reasoning indefinitely.

Once the bounded semantic slice is accepted across heterogeneous evidence, stop expanding it and return to Phase-1 closure:

```text
Market truthfulness/sampling
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
```

Only after Phase-1 closure begin corpus-wide Phase 2.
