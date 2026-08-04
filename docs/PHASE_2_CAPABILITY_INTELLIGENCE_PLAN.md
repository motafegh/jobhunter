# JobHunter Capability Intelligence Implementation Plan

**Status:** Active bounded design/vertical-slice plan  
**Date:** 2026-08-04  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/ROADMAP.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, and `docs/PRODUCT_SPECIFICATION.md`  
**Scope:** Per-job capability/depth intelligence above accepted P1.6 English extraction. This plan does **not** authorize corpus-wide canonical taxonomy/Market-v2 rollout before Phase-1 closure.

---

## 1. Why this plan exists

Live acceptance exposed an important product distinction:

```text
P1.6 strict semantic extraction
    !=
career capability intelligence
```

P1.6 is intentionally conservative. It answers:

- what responsibilities did the posting explicitly state?
- what requirements did it explicitly state?
- what exact evidence supports those claims?
- what requirement strength/type was stated?

That behavior is useful and should remain strict. However, a useful career-intelligence product must additionally answer:

- what kind of engineer/person is this role actually asking for?
- what work activities connect the listed tools, requirements, company context, and responsibilities?
- what broad capability is implied by those activities?
- which sub-capabilities are likely needed?
- what underlying knowledge is reasonably necessary?
- what independence/ownership and operational depth are implied?
- what can be inferred versus what remains unknown?

The new layer therefore **builds on P1.6** rather than weakening it.

---

## 2. Layering contract

The intended per-job flow is:

```text
original source
    ↓
English projection v2
    ↓
P1.6 English semantic extraction
(strict facts + exact evidence)
    ↓
Capability Intelligence
(reasoning + decomposition + explicit inference status)
    ↓
future canonical mapping / Market v2 / personal gap comparison
```

Permanent rule:

> Use deterministic/strict extraction to establish what the employer said; use the capability-intelligence layer to reason about what the work likely requires.

The two layers must not be collapsed into one prompt or one artifact.

---

## 3. Current activation boundary

The master implementation plan still gates full Phase 2 on Phase-1 closure. This plan therefore activates only a **bounded per-job vertical slice** now because live P1.6 acceptance itself requires evaluating whether the derived analysis is useful enough to support the later capability model.

Allowed now:

- define/version the capability-intelligence contract;
- create per-job derived artifacts;
- run manually on reviewed jobs;
- compare output quality across real examples;
- record/reuse exact source/extraction dependencies;
- add deterministic regression fixtures;
- expose the result per job once the service contract is stable.

Still gated until Phase-1 closure:

- corpus-wide capability inference;
- canonical taxonomy auto-population;
- Market-v2 aggregation over inferred capability profiles;
- role archetype generation from these profiles;
- personal readiness/gap scoring;
- automated learning-plan recommendations.

This prevents the exploratory slice from silently becoming a premature Phase-2 rollout.

---

## 4. Product behavior

### 4.1 P1.6 remains factual

Example posting text:

```text
Mastery of VPN and network infrastructure.
Troubleshoot connectivity/security incidents.
Maintain secure remote access.
```

P1.6 may correctly preserve facts close to the source:

```text
VPN/network infrastructure required
troubleshoot connectivity/security incidents
maintain secure remote access
```

That is not considered a failure of P1.6.

### 4.2 Capability Intelligence adds synthesis

The new layer should instead be able to produce a profile such as:

```text
Capability: Secure network connectivity / VPN operations

Role interpretation:
The employee is expected to operate and troubleshoot secure network connectivity rather than
merely recognize VPN terminology.

Work activities:
- diagnose connectivity/security incidents
- maintain secure remote-access connectivity

Likely technical scope:
- VPN tunnel concepts
- routing/traffic-flow reasoning around tunnels
- authentication/access-control interaction
- troubleshooting tunnel/connectivity failures

Underlying knowledge:
- TCP/IP fundamentals
- routing/subnetting concepts relevant to troubleshooting

Evidence status:
- VPN/network infrastructure: source_explicit
- VPN troubleshooting: strongly_implied_by_work
- TCP/IP fundamentals: model_inferred_prerequisite

Unknown:
- exact VPN vendor
- site-to-site versus remote-access depth
- advanced cryptographic configuration
- scale/HA requirements
```

The derived statements do **not** need to repeat employer sentences. Evidence excerpts remain exact anchors, but the analytical statements may be synthesized.

---

## 5. Evidence-status contract

Every fine-grained expectation uses exactly one status:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

### source_explicit

The employer directly stated the capability/expectation.

Requirements:
- at least one exact evidence excerpt;
- rationale explains how the source statement maps to the normalized capability.

### strongly_implied_by_work

The employer did not state the sub-capability directly, but a listed responsibility/deliverable would normally be difficult to perform without it.

Requirements:
- one or more exact evidence excerpts from the job;
- explicit reasoning connecting the work to the inferred expectation;
- confidence.

### model_inferred_prerequisite

General technical reasoning suggests the prerequisite is needed to perform supported work.

Requirements:
- evidence from the job that creates the need;
- explicit rationale;
- never presented as employer wording;
- conservative scope.

### unknown_or_unsupported

The broad capability is relevant but the posting does not justify a narrower conclusion.

Requirements:
- no fabricated evidence;
- state what is unknown and why it cannot be concluded.

---

## 6. First artifact contract

The first durable per-job artifact is `JobCapabilityIntelligenceArtifact`.

Identity:

```text
current job detail semantic version
+ current English projection artifact
+ current accepted P1.6 English analysis artifact
+ exact model
+ capability prompt version
+ capability schema version
```

This ensures that changing source text, translation, P1.6 extraction, model, or capability contract creates a new derived identity rather than silently reusing stale reasoning.

### 6.1 Whole-job fields

```text
role_interpretation
capabilities[]
cross_capability_observations[]
uncertainties[]
```

### 6.2 Capability profile fields

Each capability initially contains:

```text
capability_label
summary
requirement_strength
employer_stated_depth[]
work_activities[]
sub_capabilities[]
underlying_knowledge[]
operational_practices[]
independence_expectation
operational_context[]
unknown_scope[]
overall_confidence
```

`capability_label` is job-local/provisional in this bounded slice. It is **not yet a reviewed canonical taxonomy identity**. Future Phase-2 mapping may attach a canonical concept ID without destroying this historical artifact.

### 6.3 Expectation fields

Every work activity/sub-capability/knowledge/practice/context expectation contains:

```text
statement
evidence_status
evidence[]
rationale
confidence
```

The `statement` is deliberately analytical and may be synthesized. `evidence[]` must contain exact source/English-projection excerpts used to support the reasoning.

---

## 7. Reasoning rules

The capability model is explicitly allowed to reason. It is **not** constrained to copy source wording into the analytical statement.

Required behavior:

1. Read the role title, job description, responsibilities, explicit requirements, experience/seniority signals, skill tags, and supported company/product context together.
2. Prefer responsibilities and deliverables over isolated keyword/skill tags when inferring practical scope.
3. Connect multiple source facts when a capability is supported by their combination.
4. Decompose a broad capability only as far as the supported work justifies.
5. Infer ordinary prerequisites when they are genuinely necessary for the supported work and label them `model_inferred_prerequisite`.
6. Use `unknown_or_unsupported` rather than filling the rest of a technology curriculum from generic knowledge.
7. Treat employer-stated depth words separately from work-implied depth.
8. Treat independence/ownership separately from technical complexity.
9. Company information may support context but may not create stereotypes.
10. Do not produce personal-fit/readiness conclusions.

---

## 8. Anti-extractor rule

A successful capability-intelligence artifact should add information beyond source restatement.

The model must not merely produce:

```text
statement = evidence sentence with minor rewording
```

for every field.

Instead, material capabilities should contain at least one of:

- connected work interpretation;
- technical decomposition;
- underlying prerequisite reasoning;
- independence/ownership interpretation;
- operational-context interpretation;
- explicit unknown-scope boundary.

This is a quality/acceptance rule, not a reason to fabricate unsupported detail.

---

## 9. Structured inference and validation

Use Instructor + Pydantic for the new contract.

Validation responsibilities:

### Deterministic

- response shape/types/enums/bounds;
- exact evidence excerpts exist in the selected English projection;
- inferred/implied expectations require rationale;
- unsupported/unknown items cannot pretend to be source-explicit;
- duplicate identical expectations are collapsed/rejected deterministically;
- current source/translation/P1.6 dependency identity is exact;
- failed validation persists no accepted artifact.

### Probabilistic/reviewed

- whether a technical prerequisite is reasonable;
- whether work actually implies the stated sub-capability;
- whether decomposition is too broad/narrow;
- semantic depth/independence interpretation;
- omissions.

Instructor retries validation/shape failures. It must not be used to disguise poor semantic reasoning by repeatedly forcing an answer until one passes.

---

## 10. Persistence

Create separate tables for capability-intelligence artifacts and attempts.

Artifacts retain:

- source detail version;
- translation artifact ID;
- accepted P1.6 analysis artifact ID;
- model;
- prompt/schema versions;
- structured capability JSON;
- request body;
- raw provider response;
- creation timestamp.

Attempts retain:

```text
completed
failed
reused
```

No capability artifact mutates P1.6 artifacts.

---

## 11. First implementation tranches

### CI-1 — Contract + persistence + inference core

- define Pydantic capability models;
- define prompt/schema versions;
- add Instructor-backed local inference;
- add artifact/attempt store;
- add dependency-aware service;
- exact evidence validation;
- reuse semantics;
- deterministic tests.

### CI-2 — Per-job product surface

- add `Build Capability Intelligence` action after English P1.6 exists;
- display role interpretation;
- display capability cards with evidence-status badges;
- separate explicit/implied/inferred/unknown sections visually;
- show model/prompt/schema/dependency provenance;
- rerun should reuse unchanged artifact.

### CI-3 — Representative quality acceptance

Review at least 5 materially different jobs where possible:

- network/security role;
- Python/software role;
- AI/ML role;
- operations/platform role;
- one sparse/ambiguous posting.

For each review:

- useful synthesis beyond restatement;
- correct source-explicit/implied/inferred/unknown status;
- reasonable decomposition;
- no generic curriculum dumping;
- correct unknown boundaries;
- no invented company stereotypes;
- traceable evidence;
- acceptable omissions/false inferences.

Every repeatable failure becomes a test or a documented model-quality limitation.

### CI-4 — Promotion decision

Only after reviewed examples:

- decide whether current model is adequate;
- decide whether a stronger dedicated analysis model is warranted;
- freeze capability contract v1 or revise it;
- then continue into canonical concept mapping and Market-v2 under the Phase-2 gate.

---

## 12. Non-goals for this slice

Do not build yet:

- universal technology curricula;
- auto-growing canonical taxonomy;
- corpus-wide capability aggregation;
- personal skill/readiness scoring;
- application ranking;
- learning-plan generation;
- vector/RAG infrastructure;
- agent orchestration;
- multi-model voting;
- arbitrary repeated LLM repair loops.

---

## 13. Acceptance criteria for the bounded slice

The first per-job capability-intelligence slice is acceptable when:

1. P1.6 stays unchanged as the strict extraction source.
2. Capability artifacts are independently versioned and persisted.
3. A changed P1.6 artifact invalidates capability-artifact reuse.
4. Statements can synthesize/infer rather than copy source sentences.
5. Every supported inference is anchored to job evidence.
6. Explicit/implied/inferred/unknown statuses remain distinct.
7. Unknown scope is actively represented.
8. Exact duplicate expectations cannot inflate the profile.
9. Failures are fail-closed and inspectable.
10. At least one real reviewed job produces materially more useful intelligence than the P1.6 extraction alone.
11. Re-running the unchanged job reuses the exact artifact.
12. Important live failures and abandoned approaches are documented in `docs/SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md`.
