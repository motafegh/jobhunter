# JobHunter Role Capability Blueprint Plan

**Status:** Blueprint v3/v2 implemented as active B4 candidate; live semantic acceptance open  
**Date:** 2026-08-11  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, the active Phase-1 gate, and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Human-facing professional interpretation above accepted P1.6 and Capability Intelligence. No corpus-wide automatic generation is authorized yet.

## 1. Purpose

JobHunter separates three semantic jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable machine reasoning / decomposition

Role Capability Blueprint
→ human-facing professional interpretation
```

The Blueprint answers:

> Given the vacancy, accepted factual substrate, and accepted Capability reasoning, what does this role probably require in practice when interpreted by an experienced practitioner in the relevant domain?

It should teach the user something useful beyond rereading the advertisement without disguising professional inference as employer fact.

## 2. Current contract

Active B4 candidate:

```text
prompt/runtime: role-capability-blueprint-v3
schema:         role-capability-blueprint-v2
```

Persistence identity remains:

```text
job detail version
+ exact English projection artifact
+ exact English P1.6 artifact
+ exact Capability Intelligence artifact
+ exact Blueprint model
+ Blueprint prompt version
+ Blueprint schema version
```

Historical Blueprint v2/v1 artifacts remain historical and are not current-chain v3 artifacts.

## 3. Inputs and authority

The Blueprint reads:

```text
analysis_fields
accepted_extraction
capability_intelligence
```

Authority remains:

```text
source
→ English projection
→ accepted P1.6 facts
→ accepted Capability source truth/reasoning
→ Blueprint interpretation
```

`analysis_fields` gives complete vacancy/company context. `accepted_extraction` supplies strict duties/requirements. `capability_intelligence` supplies accepted Capability profiles and deterministic source truth.

Blueprint may reorganize and explain; it must not overwrite upstream truth.

## 4. Professional-frame rule

The model is a **senior practitioner/domain specialist**, not automatically a software engineer.

Use the frame appropriate to the vacancy: software, ML/data/industrial, content/media, operations/platform, security/network, or another relevant discipline.

Do not force non-software jobs into engineering language merely because AI appears in the title.

## 5. v3 grounding contract

### Capability areas

Every Blueprint capability area carries:

```text
source_capability_indices[]
```

Across all Blueprint areas, the union must cover every accepted Capability profile. This is deterministic coverage, not an instruction to copy Capability wording one-for-one.

### Source-named tools

Each tool/example has:

```text
relationship
source_requirement_indices[]
source_responsibility_indices[]
source_requirement_strength
source_depth_signals[]
```

Relationships remain:

```text
source_named
likely_example
possible_example
```

For `source_named`, the model links accepted P1.6 facts. JobHunter deterministically derives `source_requirement_strength` and `source_depth_signals`.

Consequences:

- Python `expert` cannot automatically spread to PyTorch/TensorFlow/XGBoost/etc.;
- a contextual or preferred tool cannot silently become required;
- source-named tools must actually be traceable to accepted P1.6;
- `likely_example`/`possible_example` cannot carry employer-source strength/depth or claim employer specification.

### Role-level constraints

Blueprint contains deterministic:

```text
source_role_constraints[]
```

These are copied from Capability v7 role-level source truth rather than inferred by the model. On current `tG9K`, expected constraints are Master's degree and three-to-six-years professional experience.

### Hidden requirements

A `highly_likely` hidden requirement must link accepted Capability profiles and/or responsibilities. It remains a professional interpretation, not a new employer fact.

### End-to-end scenarios

Each scenario declares:

```text
scenario_basis:
  source_stated_workflow
  professional_example

source_capability_indices[]
source_responsibility_indices[]
assumptions[]
```

Rules:

- `source_stated_workflow` requires accepted responsibility grounding;
- `professional_example` is practitioner-created and cannot be `highly_likely`;
- highly-likely scenarios cannot depend on unresolved assumptions;
- unstated topology, latency, vendor, batch/stream mode, cloud/edge placement, scale, or ownership must remain assumptions/unknowns rather than hidden facts.

## 6. Freedom contract

Blueprint may:

- synthesize conclusions not literally present in source text;
- use relevant domain/technical knowledge;
- infer likely subskills and practical depth;
- suggest plausible tools/protocols/libraries as examples;
- explain likely operational concerns/failure modes;
- propose coherent professional-example workflows;
- identify hidden prerequisites that genuinely follow from the work;
- identify what probably does not matter despite belonging to the broad domain.

It must not:

- present inferred tools/libraries as employer requirements;
- invent factual company systems/vendors/scale/architecture;
- turn a technology list into a claimed architecture;
- turn optional/plus/helpful wording into mandatory mastery;
- spread explicit depth from one technology to neighboring tools;
- dump a generic curriculum;
- use strong certainty where material unknowns remain;
- silently redefine technical terms, metrics, protocols, libraries, or operational roles.

Guiding rule:

> Be professionally useful; preserve the distinction between source truth, strong inference, plausible examples, and unresolved uncertainty.

## 7. Interpretation strength

```text
highly_likely
plausible
speculative
```

These describe professional interpretation, not employer truth.

`highly_likely` requires strong upstream support and no unresolved assumption that makes the conclusion uncertain.

`plausible` is useful and credible, but alternatives remain or implementation details are unstated.

`speculative` is weakly supported and should be included only when it clarifies the decision/uncertainty space.

## 8. Whole-job reasoning

Reason from combinations:

```text
responsibility
+ deliverable
+ requirement
+ accepted Capability
+ domain context
+ operational evidence
→ professional interpretation
```

Avoid:

```text
Python
→ generic Python curriculum

Kafka + Spark + Airflow + MLflow + Docker
→ invented end-to-end employer architecture
```

A technology list does not define runtime topology, data flow, latency model, ownership boundaries, or which alternatives are simultaneously used.

## 9. Artifact shape

`RoleCapabilityBlueprint` now contains:

```text
role_read
likely_role_shape
source_capability_coverage[]
source_role_constraints[]
capability_areas[]
hidden_requirements[]
likely_end_to_end_scenarios[]
what_probably_does_not_matter[]
important_unknowns[]
bottom_line
```

Each capability area includes `source_capability_indices[]` plus the existing depth/subskill/tool/work-product/failure-mode/probable-non-requirement interpretation fields.

No exact-quote requirement exists for ordinary Blueprint prose. Audit-grade source evidence remains upstream. Deterministically copied source constraints/tool strength/depth retain their upstream grounding.

## 10. Historical v2 lesson

The old `tG9K` v2 result proved the product structure was useful but exposed calibration failures:

- independently named technologies were assembled into one `highly_likely` architecture;
- a real-time anomaly-detection flow was called highly likely while latency remained unknown;
- optional edge deployment was treated too strongly;
- tools were assigned specific runtime roles the vacancy did not establish;
- plausible domain ideas became too specific/certain.

v3 addresses the general failure classes structurally rather than accumulating semiconductor-specific prompt patches.

## 11. Current implementation

Implemented:

- exact source/translation/P1.6/Capability dependency identity;
- independent Blueprint persistence/attempt history;
- bounded generation plus one structural validation retry;
- no arbitrary read deadline after successful local connection;
- dedicated Blueprint model configuration;
- browser/CLI/Review Snapshot integration;
- v3 typed grounding contract;
- deterministic Capability coverage validation;
- deterministic source-named tool strength/depth;
- deterministic role-level constraints;
- hidden-requirement grounding rule;
- scenario-basis/certainty/assumption rules;
- repository-native B4 audit script;
- regression tests for the generic v2 failure classes.

## 12. Current live B4 gate

Fixed chain:

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7 artifact 9
Blueprint model gemma-4-e2b-it
```

Run:

```bash
jobhunter jobs blueprint tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v3_snapshot.py
```

Do not rerun P1.6 or Capability merely to test Blueprint.

Mechanical acceptance requires current-chain/dependency correctness, full Capability coverage, deterministic source tool strength/depth, exact role constraints, and scenario-basis invariants.

Semantic acceptance additionally requires:

1. materially improved human understanding beyond the ad/Capability;
2. preserved upstream optionality/depth;
3. no systematic architecture invention from stack lists;
4. coherent interpretation-strength usage;
5. examples remain clearly examples;
6. acceptable technical/domain correctness;
7. no generic curriculum dumping;
8. useful probable non-requirements and unknowns;
9. professional-example scenarios are realistic but visibly hypothetical;
10. strong hidden requirements are defensible and grounded.

The exact acceptance sequence is controlled by `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` and `docs/EXECUTION_TODO.md`.

## 13. Independent Blueprint model role

Configuration:

```toml
blueprint_lm_studio_model = "..."
```

Effective fallback:

```text
dedicated Blueprint model
→ effective Capability model
```

First evaluate v3 on the existing E2B model. Only if the fixed contract is mechanically correct but semantically inadequate should a stronger Blueprint model be compared with source, P1.6, Capability, prompt/schema, and rubric held fixed.

Do not introduce multi-model voting.

## 14. Non-goals

Do not build yet:

- corpus-wide Blueprint generation;
- personal fit/readiness scoring;
- learning-plan generation;
- application ranking;
- model voting/ensembles;
- vector/RAG infrastructure;
- domain-specific prompt patch collections;
- automatic architecture generation presented as employer truth.
