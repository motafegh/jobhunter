# P1.6 v20 — Sparse Artifact 37 Acceptance

**Date:** 2026-08-15  
**Status:** sparse v20 mechanical + semantic non-regression PASS  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Job:** `t4jp`  
**Artifact:** 37  
**Baseline:** accepted sparse v16 artifact 35  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## 1. Live result

The local v20 run completed and persisted:

```text
Outcome: completed
English P1.6 v20 candidate for t4jp
Artifact: 37
Model: gemma-4-e4b-it-ud
Contract: job-analysis-english-v20 / job-analysis-v5
Responsibilities: 0
Requirements: 8
```

The v20 snapshot exporter and mechanical auditor then passed:

```text
Mechanical P1.6 v20 candidate checks: PASS
Snapshot: review-snapshots/jobs/t4jp.json
Job: t4jp
Artifact: 37
Requirements: 8
Responsibilities: 0
Role purpose statements: 0
Structured required skills covered: 3/3
Qualification-list items covered: 4/4
Residual coverage decisions: 4/4
Decomposed coarse coverage decisions: 1
Coverage decisions: 12
```

CI on snapshot commit `38df8d4f0cd519517402e6bf994c3fe469798068` also passed (run 777).

## 2. Semantic comparison with accepted sparse v16 artifact 35

Artifact 37 preserves the accepted sparse source truth exactly at the claim/evidence level.

### Structured required skills — 3/3

```text
Artificial Intelligence
Video content production
social networks
```

All remain required and directly grounded in structured `skills[]` evidence.

V20 classifies `social networks` as `tool` rather than v16's `skill`. This is a defensible ontology normalization: the source fact, required strength, evidence and candidate obligation are unchanged.

### Qualification-list items — 4/4

```text
Skills in content creation with AI
creativity in creating visual and video content
website design
ability to produce visual content full-time and part-time
```

V20 represents them as:

```text
Content creation with AI                         required / skill
Creativity in creating visual and video content required / other
Website design                                   required / skill
Visual content production                        required / skill
```

The final source item contains schedule wording (`full-time and part-time`). V20 correctly keeps the reusable concept as `Visual content production` with `depth_signal=null`; schedule wording does not enter concept or depth.

### Residual accounting — 4/4

```text
the work is teachable.                                     excluded_non_requirement
Ethics and your work commitment are important to us.       extracted_requirement
Please do not send your resume for remote work.            excluded_non_requirement
Location / benefits / travel / bonus sentence              excluded_non_requirement
```

This matches the accepted v16 semantic decisions. `Ethics and work commitment` remains one required `other` requirement.

### Sparse restraint

```text
Responsibilities: 0
Role purpose:     0
```

No duty or role purpose was fabricated from a source that contains qualifications, logistics and benefits but no explicit employee-duty section.

No education or minimum-experience requirement was fabricated from `it doesn't matter` fields.

## 3. Non-gating rationale hygiene observation

One v20 requirement has the correct authoritative fields:

```text
concept:          Visual content production
requirement_type: required
concept_type:     skill
depth_signal:     null
evidence:         ability to produce visual content full-time and part-time
```

but its model-generated explanatory rationale says:

```text
Explicit qualification list item, capturing scope/schedule as depth.
```

That explanatory sentence is internally inaccurate because schedule wording was deliberately **not** captured as depth. The authoritative semantic fields are correct and the governing P1.6 acceptance rubric evaluates source fidelity, qualification/duty classification, obligation, depth, ontology, evidence and sparse restraint rather than free-form rationale prose. Therefore this does not fail sparse P1.6 non-regression.

Record it as a model-explanation hygiene observation. Do not allow free-form P1.6 rationale text to become more authoritative than normalized P1.6 fields/evidence in downstream reasoning. Capability review must continue to enforce that boundary.

## 4. Sparse verdict

```text
persistence:             PASS
mechanical snapshot:     PASS
semantic non-regression: PASS
```

Artifact 37 is accepted for the bounded sparse calibration case.

## 5. V20 calibration boundary now satisfied

```text
v20 deterministic CI PASS
+ dense tG9K artifact 36 persistence PASS
+ dense tG9K artifact 36 mechanical PASS
+ dense tG9K artifact 36 semantic PASS
+ sparse t4jp artifact 37 persistence PASS
+ sparse t4jp artifact 37 mechanical PASS
+ sparse t4jp artifact 37 semantic non-regression PASS
```

This authorizes the **P1.6 v20 promotion decision/work**, but does not itself make v20 public truth.

Until promotion is deliberately implemented and verified:

- accepted/public English P1.6 remains `job-analysis-english-v9` / `job-analysis-v4`;
- Capability artifact 9 remains tied to P1.6 artifact 29;
- PR #8 remains candidate/draft;
- do not rebuild Capability against candidate artifacts as if promotion already happened;
- do not begin corpus-wide Phase 2.

After P1.6 promotion, rebuild/review Capability v7 against the promoted P1.6 dependency and continue heterogeneous Python/software, network/security and operations/platform cases.