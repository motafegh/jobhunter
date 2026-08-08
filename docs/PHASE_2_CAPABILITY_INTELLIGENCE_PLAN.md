# JobHunter Capability Intelligence Implementation Plan

**Status:** CI-1/CI-2 implemented; CI-3 semantic-quality acceptance active  
**Date:** 2026-08-08  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/ROADMAP.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, `docs/PRODUCT_SPECIFICATION.md`, and the current Phase-1 gate  
**Scope:** Bounded per-job capability/depth reasoning above accepted P1.6 English extraction. This plan does **not** authorize corpus-wide Phase-2 taxonomy/Market-v2 rollout before Phase-1 closure.

The detailed current quality sequence is defined in `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 1. Current contract and implementation state

Active identities:

```text
P1.6 English prompt/runtime:  job-analysis-english-v4
P1.6 schema:                  job-analysis-v2

Capability prompt/runtime:    job-capability-intelligence-v4
Capability schema:            job-capability-intelligence-v2
```

Current flow:

```text
current Jobinja source version
        ↓
exact English projection referenced by accepted P1.6
        ↓
accepted English P1.6 factual extraction
        ↓
JobHunter deterministic evidence catalog
  ├─ field references
  ├─ heading-aware long-description segments
  ├─ clause-level references where useful
  └─ P1.6 claim references
        ↓
Capability Intelligence v4 model reasoning
        ↓
Pydantic/Instructor validation
        ↓
reference resolution back to exact English source text
        ↓
independent final service validation
        ↓
versioned capability artifact + attempt history
        ↓
CLI / browser / Review Snapshot
```

Current CLI:

```bash
jobhunter jobs capability <job-id>
```

Current browser surface: **Capability Intelligence** on a job with current accepted English analysis.

Historical Capability prompt/runtime versions remain preserved and are not silently reused as v4 artifacts.

---

## 2. Why the layer exists

P1.6 and Capability Intelligence have different uncertainty contracts.

### P1.6

Answers what the employer/source actually supports:

- role purpose;
- responsibilities;
- requirements;
- strength/optionality;
- concept type;
- exact evidence;
- confidence/rationale where applicable.

### Capability Intelligence

Answers what the work likely requires in practice:

- role interpretation;
- work activities;
- depth signals;
- technical sub-capabilities;
- underlying knowledge/prerequisites;
- operational practices;
- independence/ownership;
- operational context;
- unknown/unsupported scope;
- whole-role cross-capability observations.

Permanent rule:

> Strict extraction establishes what the employer said; Capability Intelligence reasons about what the work likely requires; deterministic JobHunter code owns provenance/bookkeeping.

Do not collapse the two layers into one prompt/artifact.

---

## 3. Activation boundary

Allowed before Phase-1 closure:

- define/version the per-job capability contract;
- persist independent capability artifacts/attempts;
- run manually on reviewed real jobs;
- compare semantic quality across heterogeneous cases;
- configure a dedicated capability model;
- generate Review Snapshots for quality review;
- add deterministic regression fixtures from real incidents.

Still gated:

- corpus-wide automatic capability inference;
- automatic canonical-taxonomy population;
- Market-v2 aggregation over inferred profiles;
- role-archetype generation from these profiles;
- personal readiness/gap scoring;
- automated learning/project recommendations.

---

## 4. Artifact contract

`JobCapabilityIntelligence` contains:

```text
role_interpretation
capabilities[]
cross_capability_observations[]
uncertainties[]
```

Each capability profile contains:

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

Each expectation contains:

```text
statement
evidence_status
evidence[]
rationale
confidence
```

Evidence status:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

Requirement strength remains separate from evidence status and depth:

```text
required
preferred
contextual
inferred
mixed
unspecified
```

---

## 5. Evidence-reference contract

The model cites only evidence reference IDs supplied by JobHunter.

Examples:

```text
p1:requirements:0
p1:responsibilities:2
field:description:segment:4
field:description:segment:4:clause:1
field:company_description
```

JobHunter resolves references back to exact English source text before persistence.

### Deterministic resilience rules

1. Supported claim + valid evidence + invalid extra reference:
   - keep the proven evidence;
   - discard the invalid extra.

2. Supported claim + invalid-only evidence:
   - fail closed.

3. `unknown_or_unsupported` + invalid-only evidence:
   - normalize evidence to `[]`;
   - preserve the uncertainty statement;
   - do not spend another full generation fixing meaningless bookkeeping.

4. Historical exact-text evidence remains supported as a mechanical compatibility fallback.

The `tG9K` failure that invented `p1:requirements:19` established rule 3. The model's uncertainty conclusion was usable; only the reference was invalid, and unknown scope is explicitly allowed to have no evidence.

---

## 6. Runtime policy

Capability inference uses Instructor + Pydantic over the local LM Studio OpenAI-compatible endpoint.

Runtime policy:

```text
connection establishment: bounded
read timeout after connection: none
transport replay: disabled
max output tokens: bounded
Instructor validation retry: one bounded retry
```

This intentionally avoids killing legitimate long local reasoning after an arbitrary 30/120-second read deadline.

---

## 7. Independent model role

Configuration supports:

```toml
capability_lm_studio_model = "..."
```

Effective model resolution:

```text
dedicated capability model
→ effective analysis model
```

The best strict factual extractor is not assumed to be the best capability-reasoning model.

Model comparison must keep source, translation, accepted P1.6 artifact, prompt/schema contract, and review criteria fixed while changing the model.

---

## 8. CI-1 — Contract, persistence and inference core

**Status: implemented.**

Implemented:

- typed Capability contract;
- versioned prompt/schema identity;
- deterministic evidence catalog;
- heading/clause evidence references for dense postings;
- exact evidence resolution before persistence;
- `depth_signals` model;
- explicit/implied/inferred/unknown statuses;
- mechanical unknown-scope normalization;
- exact duplicate normalization;
- bounded Instructor validation retry;
- no arbitrary read deadline for long local generation;
- dependency-aware persistence/reuse;
- independent final service validation;
- completed/failed/reused attempt history;
- regression coverage for important evidence-reference failure classes.

---

## 9. CI-2 — Product surfaces

**Status: implemented.**

Implemented:

- `jobhunter jobs capability <job-id>`;
- browser Capability Intelligence page;
- operation-manager integration;
- resolved evidence display;
- provenance/model/prompt/schema display;
- dedicated capability model routing;
- Review Snapshot export of the current capability chain.

---

## 10. CI-3 — Representative semantic-quality acceptance

**Status: active; not passed.**

Current live cases:

### `t4jp` — sparse/ambiguous posting

Use to test conservative inference. The posting has limited technical evidence, so correct behavior is modest depth and explicit unknowns rather than a sophisticated invented architecture.

### `tG9K` — rich semiconductor/industrial-ML posting

The current v4 chain completes successfully and is reviewable in:

```text
review-snapshots/jobs/tG9K.json
```

Positive evidence:

- full long-posting runtime succeeds;
- evidence references resolve correctly;
- useful role/capability decomposition is produced;
- unknown-scope invalid references no longer cause wasteful full retries;
- capability artifacts are dependency-correct and reusable.

Remaining quality findings:

- `depth_signals` are underused despite explicit depth/experience evidence;
- upstream P1.6 coverage/strength errors can be amplified downstream;
- broad technical-stack membership can still become too strongly `required`;
- optional edge/cloud wording can become overly strong operational context;
- capability-area grouping can leak unrelated uncertainty/context into another capability;
- some statements are useful but more certain than their evidence justifies.

### CI-3 required sample

Review at least five materially different jobs where possible:

1. sparse/ambiguous (`t4jp` currently serves this role);
2. rich AI/ML (`tG9K` currently serves this role);
3. Python/software;
4. network/security;
5. operations/platform/DevOps.

For each:

- inspect P1.6 substrate first;
- inspect useful synthesis beyond restatement;
- inspect evidence status calibration;
- inspect requirement-strength/depth preservation;
- inspect decomposition and unknown boundaries;
- inspect omissions/false inferences;
- inspect company-context stereotypes;
- inspect domain/tool correctness;
- create/update a repository Review Snapshot;
- turn repeatable deterministic failures into regression fixtures.

Do not accept Capability quality when the upstream P1.6 factual artifact is known to be materially wrong.

---

## 11. CI-4 — Model/promotion decision

**Status: open.**

After the deterministic semantic-quality tranches and representative CI-3 sample:

- decide whether the current Gemma capability reasoning is adequate;
- if not, compare one stronger dedicated local model under the same evidence/prompt/schema;
- select the model based on reviewed technical correctness and calibration, not eloquence;
- freeze/revise the bounded Capability contract only after evidence;
- document model-quality limitations that cannot be solved deterministically;
- then return to Phase-1 closure work.

CI-4 does **not** authorize corpus-wide Phase-2 aggregation.

---

## 12. Current acceptance criteria

The bounded Capability slice is acceptable when:

1. P1.6 remains the strict factual source.
2. Capability artifacts are independently versioned/persisted.
3. The exact English projection and P1.6 artifact dependencies are retained.
4. Model evidence uses only JobHunter references during generation.
5. Persisted evidence resolves to exact source text.
6. Unsupported supported-claim evidence fails closed.
7. Unknown scope can remain evidence-empty without wasteful retry.
8. Explicit/implied/inferred/unknown remain distinct.
9. Requirement strength is not systematically inflated.
10. Depth signals are used when evidence supports them.
11. Capability decomposition adds useful reasoning without generic curricula.
12. Re-running unchanged dependencies reuses the artifact.
13. At least five materially different reviewed examples support bounded promotion.
14. Important live failure classes are regression-tested or documented as model limitations.
15. Ruff, pytest, and warnings-as-errors are observed green on the user's environment for the accepted head.

---

## 13. Known technical debt kept explicit

The current `job_analysis_artifacts` table identity does not include `translation_artifact_id` directly in its uniqueness key. Capability Intelligence therefore follows the exact translation artifact already referenced by the accepted P1.6 artifact rather than guessing from the latest translation row.

Any future P1.6 identity migration must be designed/tested explicitly. Do not hide it inside semantic-quality tuning.

---

## 14. Non-goals

Do not build yet:

- universal technology curricula;
- auto-growing taxonomy;
- corpus-wide capability aggregation;
- personal skill/readiness scoring;
- application ranking;
- learning-plan generation;
- vector/RAG infrastructure;
- agent orchestration;
- multi-model voting;
- arbitrary repeated LLM repair loops;
- domain-specific prompt-patch collections.
