# JobHunter Capability Intelligence Implementation Plan

**Status:** CI-1/CI-2 implemented; v2 deterministic/live acceptance pending  
**Date:** 2026-08-04  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/ROADMAP.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, and `docs/PRODUCT_SPECIFICATION.md`  
**Scope:** Per-job capability/depth intelligence above accepted P1.6 English extraction. This plan does **not** authorize corpus-wide canonical taxonomy/Market-v2 rollout before Phase-1 closure.

---

## 0. Current implementation status

The active contract is:

```text
job-capability-intelligence-v2
```

Implemented on `main`:

```text
accepted English P1.6 extraction
        ↓ exact referenced English projection
JobHunter deterministic evidence catalog
        ↓ stable evidence-reference IDs
JobCapabilityIntelligence v2 typed contract
        ↓
Instructor + Pydantic bounded reasoning
        ↓
reference resolution back to exact source text
        ↓
independent final validation
        ↓
versioned capability artifact + attempt history
        ↓
CLI / browser per-job review
```

Current surfaces:

```bash
jobhunter jobs capability <job-id>
```

and the **Capability Intelligence** link on a job page after a current English P1.6 artifact exists.

Implemented contracts include:

- exact dependency identity on source version + referenced English artifact + accepted English P1.6 artifact + model + capability prompt/schema;
- analytical statements may be synthesized;
- the model cites stable JobHunter evidence references instead of reproducing exact quotations;
- JobHunter resolves those references back to exact English source text before persistence;
- `source_explicit`, `strongly_implied_by_work`, `model_inferred_prerequisite`, and `unknown_or_unsupported` remain distinct;
- `depth_signals` can contain explicit or derived depth observations and relies on evidence status for provenance;
- mechanically misplaced unknown-scope items are normalized deterministically rather than consuming a full model retry;
- exact duplicate expectations are normalized deterministically;
- each capability must add genuinely derived reasoning or an explicit unknown-scope boundary rather than passing as pure source restatement;
- failed validation persists no accepted capability artifact;
- long local Capability Intelligence generation has no read-time ceiling, while connection setup remains bounded and transport replay is disabled;
- the layer remains opt-in and is not part of Market/full-workflow aggregation.

Historical `job-capability-intelligence-v1` artifacts remain preserved but are not reused as v2 artifacts.

Not yet accepted:

- deterministic gate results for v2;
- representative live quality across materially different jobs;
- current small-model adequacy;
- canonical concept mapping;
- corpus-wide aggregation;
- personal comparison/readiness/learning recommendations.

**Separate P1.6 debt discovered during this work:** the current `job_analysis_artifacts` table identity does not include `translation_artifact_id` in its uniqueness key. Capability Intelligence therefore follows the exact translation artifact already referenced by the accepted P1.6 artifact and does not guess from the latest translation row. Any future P1.6 identity migration must be designed/tested explicitly rather than hidden inside this capability slice.

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
deterministic evidence catalog
    ↓
Capability Intelligence v2
(reasoning + decomposition + evidence references)
    ↓
exact evidence resolution by JobHunter
    ↓
future canonical mapping / Market v2 / personal gap comparison
```

Permanent rule:

> Use deterministic/strict extraction to establish what the employer said; use the capability-intelligence layer to reason about what the work likely requires; keep quote/provenance bookkeeping in deterministic JobHunter code.

The layers must not be collapsed into one prompt or one artifact.

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

Depth signals:
- employer says mastery of VPN/network infrastructure: source_explicit
- independent fault diagnosis is implied by the listed troubleshooting work: strongly_implied_by_work

Likely technical scope:
- VPN tunnel concepts
- routing/traffic-flow reasoning around tunnels
- authentication/access-control interaction
- troubleshooting tunnel/connectivity failures

Underlying knowledge:
- TCP/IP fundamentals
- routing/subnetting concepts relevant to troubleshooting

Unknown:
- exact VPN vendor
- site-to-site versus remote-access depth
- advanced cryptographic configuration
- scale/HA requirements
```

Derived statements do **not** need to have literally appeared in the advertisement.

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

### strongly_implied_by_work

The employer did not state the sub-capability directly, but a listed responsibility/deliverable would normally be difficult to perform without it.

### model_inferred_prerequisite

General technical reasoning suggests the prerequisite is needed to perform supported work.

### unknown_or_unsupported

The broad capability is relevant but the posting does not justify a narrower conclusion.

The status expresses provenance. Section placement must not redundantly encode the same provenance rule when deterministic normalization can preserve the intended conclusion.

---

## 6. Artifact contract

The durable per-job artifact is `JobCapabilityIntelligence` persisted by `CapabilityIntelligenceStore`.

Identity:

```text
current job detail semantic version
+ exact English projection artifact referenced by accepted P1.6
+ current accepted P1.6 English analysis artifact
+ exact model
+ capability prompt version
+ capability schema version
```

### 6.1 Whole-job fields

```text
role_interpretation
capabilities[]
cross_capability_observations[]
uncertainties[]
```

### 6.2 Capability profile fields — v2

```text
capability_label
summary
requirement_strength
depth_signals[]
work_activities[]
sub_capabilities[]
underlying_knowledge[]
operational_practices[]
independence_expectation
operational_context[]
unknown_scope[]
overall_confidence
```

`depth_signals` replaces v1 `employer_stated_depth`. Explicit versus inferred depth is represented by `evidence_status` rather than by a brittle employer-only section rule.

### 6.3 Expectation fields

```text
statement
evidence_status
evidence[]
rationale
confidence
```

During model generation, `evidence[]` contains stable evidence-reference IDs only. JobHunter resolves those IDs to exact source text during Pydantic validation. Persisted artifacts therefore retain exact source text while the model avoids quotation-transcription work.

Example generation-time evidence:

```text
p1:requirements:0
p1:responsibilities:2
field:company_description
```

Historical/test exact-text evidence remains supported as a fallback, but it is no longer the preferred model contract.

---

## 7. Reasoning rules

Required behavior:

1. Read the role title, job description, responsibilities, explicit requirements, experience/seniority signals, skill tags, and supported company/product context together.
2. Prefer responsibilities and deliverables over isolated keyword/skill tags when inferring practical scope.
3. Connect multiple source facts when a capability is supported by their combination.
4. Decompose a broad capability only as far as the supported work justifies.
5. Infer ordinary prerequisites when genuinely necessary and label them `model_inferred_prerequisite`.
6. Use `unknown_or_unsupported` rather than filling the rest of a technology curriculum from generic knowledge.
7. Treat requirement strength separately from depth.
8. Use `depth_signals` for explicit or work-implied depth and let evidence status carry provenance.
9. Treat independence/ownership separately from technical complexity.
10. Company information may support context but may not create stereotypes.
11. Do not produce personal-fit/readiness conclusions.

---

## 8. Anti-extractor rule

A successful capability-intelligence artifact must add information beyond source restatement.

The current typed contract requires each capability profile to include at least one genuinely derived `strongly_implied_by_work` / `model_inferred_prerequisite` conclusion or an explicit `unknown_or_unsupported` boundary.

This is a quality/acceptance rule, not a reason to fabricate unsupported detail.

---

## 9. Structured inference and validation

Use Instructor + Pydantic for the contract.

### Deterministic responsibilities

- response shape/types/enums/bounds;
- build stable evidence references from exact source/P1.6 evidence;
- resolve evidence references back to exact source text;
- reject unknown/invented evidence references;
- preserve exact source/P1.6/translation dependency identity;
- normalize mechanically implied unknown-scope section placement;
- duplicate handling;
- independent service re-validation before persistence;
- fail closed when a completed artifact still violates a non-mechanical contract.

### Probabilistic/reviewed responsibilities

- whether a technical prerequisite is reasonable;
- whether work actually implies the stated sub-capability;
- whether decomposition is too broad/narrow;
- semantic depth/independence interpretation;
- omissions.

Instructor may perform one bounded retry for a genuinely invalid completed response. It must not be used as a quotation editor or section-bookkeeping repair engine.

### Runtime policy for long local reasoning

```text
connection establishment: bounded
read timeout: none
transport replay: disabled
max_tokens: bounded
validation retry: bounded separately
```

Once LM Studio is connected and actively generating, JobHunter does not impose an arbitrary 30/120-second read deadline.

---

## 10. Persistence

Separate tables exist for capability-intelligence artifacts and attempts.

Artifacts retain:

- source detail version;
- exact referenced English translation artifact ID;
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

## 11. Implementation tranches

### CI-1 — Contract + persistence + inference core — V2 IMPLEMENTED / ACCEPTANCE PENDING

Implemented:

- typed capability models;
- v2 prompt/schema identities;
- deterministic evidence catalog;
- evidence-reference generation contract;
- exact evidence resolution before persistence;
- `depth_signals` model;
- mechanical unknown-scope normalization;
- Instructor-backed local inference;
- artifact/attempt store;
- dependency-aware service;
- independent final service validation;
- reuse semantics;
- no-read-deadline long-form inference policy;
- deterministic regression tests written.

Still required:

- local Ruff/pytest/warnings-as-errors observation on v2;
- live per-job inference acceptance.

### CI-2 — Per-job product surface — V2 IMPLEMENTED / ACCEPTANCE PENDING

Implemented:

- `jobhunter jobs capability <job-id>`;
- browser **Capability Intelligence** link after English analysis;
- dedicated capability review page;
- depth/evidence-status/unknown-scope rendering;
- resolved exact evidence display;
- operation-manager integration;
- artifact provenance display.

### CI-3 — Representative quality acceptance — OPEN

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

### CI-4 — Promotion decision — OPEN

Only after reviewed examples:

- decide whether current model is adequate;
- decide whether a stronger dedicated capability model is warranted;
- freeze capability contract v2 or revise it;
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

The v2 per-job capability-intelligence slice is acceptable when:

1. P1.6 stays unchanged as the strict extraction source.
2. Capability artifacts are independently versioned and persisted.
3. Capability reasoning follows the exact English projection referenced by accepted P1.6.
4. The model cites only stable evidence references during generation.
5. JobHunter resolves those references to exact source evidence before persistence.
6. Statements can synthesize/infer rather than copy source sentences.
7. Explicit/implied/inferred/unknown statuses remain distinct.
8. Unknown scope is actively represented without brittle section/status failures.
9. Exact duplicate expectations cannot inflate the profile.
10. Failures are fail-closed and inspectable.
11. At least one real reviewed job produces materially more useful intelligence than the P1.6 extraction alone.
12. Re-running the unchanged job reuses the exact v2 artifact.
13. Important live failures and abandoned approaches are documented under `docs/incidents/` and the engineering-lessons record.
14. Full deterministic test/lint gates are observed green on the user's environment.
