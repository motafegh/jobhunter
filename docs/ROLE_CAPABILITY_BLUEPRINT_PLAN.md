# JobHunter Role Capability Blueprint Plan

**Status:** Blueprint v4/v3 implemented as active B4 candidate; live semantic acceptance open  
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
prompt/runtime: role-capability-blueprint-v4
schema:         role-capability-blueprint-v3
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

Historical Blueprint v3/v2 and earlier artifacts remain historical. V3/v2 failed B4 with both E2B and E4B and must not be revived by weakening validators or adding model-specific prompt patches.

## 3. Authority and input boundary

Authority remains:

```text
source
→ English projection
→ accepted P1.6 facts
→ accepted Capability source truth/reasoning
→ Blueprint interpretation
```

V4 does **not** send raw provenance namespaces to the model. JobHunter first builds a compact ordered projection containing:

```text
selected role/company context
role purpose
role-level source constraints for context
ordered accepted Capability labels
source requirement facts without numeric IDs
source responsibility statements without numeric IDs
compact accepted Capability reasoning
```

The long source description is not duplicated merely to reconstruct already accepted facts.

Blueprint may explain and interpret; it must not overwrite upstream truth.

## 4. Professional-frame rule

The model is a **senior practitioner/domain specialist**, not automatically a software engineer.

Use the frame appropriate to the vacancy: software, ML/data/industrial, content/media, operations/platform, security/network, or another relevant discipline.

Do not force non-software jobs into engineering language merely because AI appears in the title.

## 5. Why v3 failed

V3 attempted to make the LLM reproduce:

```text
Capability profile indices
P1.6 requirement indices
P1.6 responsibility indices
source-named tool provenance
scenario grounding/basis
```

Both E2B and E4B confused P1.6 requirement IDs with Capability-profile IDs. E4B's repair even recognized correct source requirement numbers but wrote them into `source_depth_signals` rather than `source_requirement_indices`.

Both models also retained semantic overreach by assembling technology lists into stronger streaming/MLOps/cloud/edge architecture than the accepted source established.

The architectural conclusion is:

> **The model reasons; JobHunter owns provenance bookkeeping.**

Detailed evidence is preserved in `docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md`.

## 6. V4 deterministic provenance contract

### One interpretation per accepted Capability

The model returns:

```text
capability_interpretations[]
```

with exactly one item per accepted Capability profile, in source order.

The model does not regroup, merge, split, rename, or create replacement Capability areas.

JobHunter constructs each persisted area with authoritative:

```text
name
source_capability_index
```

and deterministic total coverage.

### Source requirements and responsibilities

For each accepted Capability profile, JobHunter attaches the exact P1.6 items already linked by Capability v7.

Persisted source requirement anchors contain:

```text
requirement_index
concept
concept_type
requirement_type
depth_signal
evidence
```

Persisted source responsibility anchors contain:

```text
responsibility_index
statement
evidence
```

The model never reproduces these indices or source metadata.

Consequences:

- Python `expert` cannot spread to frameworks;
- contextual frameworks/platforms remain contextual;
- preferred MATLAB/C++/edge remain preferred;
- required industrial-experience depth remains attached to its exact concept;
- source evidence cannot disappear because the model forgot a provenance link.

### Role-level constraints

JobHunter deterministically copies Capability v7 role-level source truth into:

```text
source_role_constraints[]
```

For current `tG9K`, expected constraints are Master's degree and three-to-six-years professional experience.

## 7. Suggested tools / examples

Source-named technologies are already visible through deterministic source requirements. The model does not create `source_named` tool records.

Model-created tools live only under:

```text
suggested_tools_or_examples[]
```

with relationships:

```text
likely_example
possible_example
```

Rules:

- no source requirement/responsibility indices;
- no source strength/depth fields;
- cannot be described as mandatory/required/necessary;
- cannot claim expert/mastery depth;
- must remain examples, not employer specifications.

## 8. Hidden requirements

A model-created hidden requirement is professional inference, never employer fact.

V4 permits only:

```text
plausible
speculative
```

There is no `highly_likely` hidden-requirement mode. This avoids asking the model to fabricate provenance just to justify strong certainty.

Prefer a small number of role-specific, genuinely useful insights over generic curriculum prerequisites.

## 9. Professional example scenarios

All model-created workflows are persisted as:

```text
professional_example_scenarios[]
```

JobHunter injects:

```text
scenario_basis = professional_example
```

Allowed interpretation strengths:

```text
plausible
speculative
```

There is no v4 model-generated `source_stated_workflow` category. Source-stated responsibilities already survive independently as deterministic source anchors.

A professional example may choose a coherent implementation, but unstated choices must remain explicit assumptions, including:

```text
topology
latency / real-time behavior
vendor
batch vs stream mode
cloud vs edge placement
scale
ownership boundaries
orchestration
feedback/control-loop behavior
```

A technology list does not define runtime topology or prove that all alternatives are simultaneously used.

## 10. Freedom contract

Blueprint may:

- synthesize conclusions not literally present in source text;
- use relevant domain/technical knowledge;
- infer practical depth and subskills within each accepted Capability;
- suggest plausible implementation tools as examples;
- explain likely operational concerns/failure modes;
- propose coherent professional-example workflows with assumptions;
- identify useful hidden prerequisites at plausible/speculative strength;
- identify what probably does not matter despite belonging to the broad domain.

It must not:

- present inferred tools/libraries as employer requirements;
- invent factual company systems/vendors/scale/architecture;
- turn a technology list into a claimed architecture;
- turn optional/contextual wording into mandatory mastery;
- spread explicit depth from one technology to neighboring tools;
- dump a generic curriculum;
- use strong certainty where material unknowns remain;
- silently redefine technical terms, metrics, protocols, libraries, or operational roles.

Guiding rule:

> Be professionally useful; preserve the distinction between source truth, accepted Capability reasoning, professional inference, illustrative examples, and unresolved uncertainty.

## 11. Interpretation strength

Capability interpretations may use:

```text
highly_likely
plausible
speculative
```

because each interpretation is anchored by position to an accepted Capability profile.

Hidden requirements and professional examples may use only:

```text
plausible
speculative
```

These labels describe professional interpretation, not employer truth.

## 12. Artifact shape

Persisted `RoleCapabilityBlueprint` contains:

```text
role_read
likely_role_shape
source_capability_coverage[]
source_role_constraints[]
capability_areas[]
hidden_requirements[]
professional_example_scenarios[]
what_probably_does_not_matter[]
important_unknowns[]
bottom_line
```

Each capability area includes:

```text
name
source_capability_index
interpretation_strength
likely_depth
why_this_matters
likely_subskills[]
source_requirements[]
source_responsibilities[]
suggested_tools_or_examples[]
likely_work_products[]
likely_failure_modes_or_operational_concerns[]
probably_not_required[]
```

No exact-quote requirement exists for ordinary Blueprint prose. Audit-grade source evidence remains upstream and is copied deterministically into source anchors.

## 13. Current implementation

Active files:

```text
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v4.py
src/jobhunter/role_blueprint_inference_v4.py
src/jobhunter/role_blueprint_v4_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v4_snapshot.py
```

Implemented:

- exact source/translation/P1.6/Capability dependency identity;
- independent Blueprint persistence/attempt history;
- bounded generation plus one structural validation retry;
- no arbitrary read deadline after successful local connection;
- automatic 16,384-token LM Studio Blueprint context preparation;
- dedicated Blueprint model configuration;
- browser/CLI/Review Snapshot integration;
- model-facing provenance-free draft contract;
- deterministic one-to-one Capability mapping and coverage;
- deterministic P1.6 source requirement/responsibility attachment;
- deterministic role-level constraints;
- bounded inferred-tool contract;
- structurally downgraded hidden requirements/scenarios;
- repository-native B4 audit script;
- v4 regression tests.

Historical v3 implementation remains preserved for negative evidence and regression reference.

## 14. Current live B4 gate

Fixed chain:

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7 artifact 9
Blueprint model gemma-4-e4b-it-ud
```

Confirm active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v4
role-capability-blueprint-v3
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

Do not rerun translation, P1.6 or Capability merely to test Blueprint.

If a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v4_snapshot.py
```

Mechanical acceptance requires:

1. current-chain/dependency correctness;
2. exactly one area per accepted Capability profile, in exact order with exact label;
3. complete deterministic source-requirement/source-responsibility propagation;
4. exact role-level constraints;
5. no legacy v3 provenance fields in model-created content;
6. only likely/possible suggested tools;
7. only plausible/speculative hidden requirements and professional scenarios;
8. `professional_example` scenario basis.

Semantic acceptance additionally requires:

1. materially improved human understanding beyond the ad/Capability;
2. calibrated role identity rather than MLOps/platform inflation;
3. preserved upstream optionality/depth;
4. no architecture invention from stack lists;
5. coherent interpretation-strength usage;
6. examples remain visibly examples with material assumptions;
7. acceptable technical/domain correctness;
8. no generic curriculum dumping;
9. useful probable non-requirements and unknowns;
10. no unsupported real-time/microservice/CI-CD/model-registry/control-loop certainty.

The exact acceptance sequence is controlled by `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` and `docs/EXECUTION_TODO.md`.

## 15. Independent Blueprint model role

Configuration:

```toml
blueprint_lm_studio_model = "..."
```

Effective fallback:

```text
dedicated Blueprint model
→ effective Capability model
```

Current controlled B4 v4 model is `gemma-4-e4b-it-ud`. Do not change model and contract simultaneously during the first v4 live test. Do not introduce multi-model voting.

## 16. Non-goals

Do not build yet:

- corpus-wide Blueprint generation;
- personal fit/readiness scoring;
- learning-plan generation;
- application ranking;
- model voting/ensembles;
- vector/RAG infrastructure;
- domain-specific prompt patch collections;
- automatic architecture generation presented as employer truth.
