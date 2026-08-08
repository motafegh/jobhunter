# JobHunter Role Capability Blueprint Plan

**Status:** Implemented bounded per-job slice; semantic-quality acceptance active  
**Date:** 2026-08-08  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, the active Phase-1 gate, and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Human-facing professional interpretation above strict P1.6 and Capability Intelligence. No corpus-wide automatic generation is authorized yet.

---

## 1. Purpose

JobHunter deliberately separates three jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable machine reasoning / decomposition

Role Capability Blueprint
→ human-facing professional interpretation
```

The Blueprint answers:

> Given the complete vacancy, factual extraction, and evidence-qualified capability reasoning, what does this role probably require in practice when interpreted by an experienced practitioner in the relevant domain?

It should teach the user something useful beyond simply rereading the advertisement.

---

## 2. Current contract

Active identity:

```text
prompt/runtime: role-capability-blueprint-v2
schema:         role-capability-blueprint-v1
```

Persistence identity:

```text
job detail version
+ exact English projection artifact
+ exact English P1.6 artifact
+ exact Capability Intelligence artifact
+ exact Blueprint model
+ Blueprint prompt version
+ Blueprint schema version
```

Historical Blueprint prompt/runtime versions remain preserved and are not reused as v2 artifacts.

---

## 3. Inputs

The Blueprint reads together:

```text
analysis_fields
accepted_extraction
capability_intelligence
```

`analysis_fields` supplies the complete hardened English vacancy/company context.

`accepted_extraction` supplies strict factual duties/requirements.

`capability_intelligence` supplies auditable reasoning context, but it is not a cage. The Blueprint may reorganize, narrow, or improve the human explanation so long as it does not overwrite source truth.

---

## 4. Professional-frame rule

The model is a **senior practitioner/domain specialist**, not always a software engineer.

Use the professional frame that matches the vacancy:

- software role → software-engineering interpretation;
- ML role → ML/data/industrial interpretation;
- content/media role → content/media interpretation;
- operations role → operations/platform interpretation;
- security role → security/network interpretation;
- other domains → corresponding practitioner frame.

Do not force non-software jobs into engineering language merely because AI appears in the title.

---

## 5. Freedom contract

The Blueprint may:

- synthesize conclusions not literally present in source text;
- use relevant domain/technical knowledge;
- infer likely subskills and practical depth;
- suggest plausible libraries/frameworks/APIs/protocols/tools as examples;
- explain likely operational concerns/failure modes;
- propose plausible end-to-end workflows;
- identify hidden prerequisites that genuinely follow from the work;
- identify what probably does **not** matter despite belonging to the broad domain.

It must not:

- present inferred tools/libraries as employer-explicit requirements;
- invent factual company systems/vendors/scale/architecture;
- turn a technology list into a claimed architecture;
- turn optional/plus/helpful wording into mandatory mastery;
- dump a generic curriculum for every technology;
- repeat obvious advertisement facts without analytical purpose;
- use strong certainty where the source leaves important unknowns;
- silently redefine technical terms, metrics, protocols, libraries, or operational roles.

Guiding rule:

> Be professionally useful; label uncertainty instead of suppressing reasonable inference or disguising speculation as fact.

---

## 6. Interpretation strength

Use:

```text
highly_likely
plausible
speculative
```

These describe professional interpretation, not employer truth.

### `highly_likely`

Requires strong support from explicit work, repeated clues, or a direct domain dependency.

A `highly_likely` conclusion must not contradict an `important_unknown` that makes the conclusion unresolved.

### `plausible`

Reasonable and useful, but credible alternatives exist or the source does not establish the implementation path.

### `speculative`

Possible but weakly supported. Include only when it helps define uncertainty or decision space.

---

## 7. Tool/example relationship

Use:

```text
source_named
likely_example
possible_example
```

A tool marked `likely_example` or `possible_example` must never be described as mandatory, required, necessary, or employer-specified unless a separate source fact actually establishes that.

Named technologies also do not prove that the employer combines all of them into one deployed system.

---

## 8. Whole-job reasoning

Reason from combinations, not isolated keywords.

Good pattern:

```text
responsibility
+ deliverable
+ requirement
+ domain context
+ operational evidence
→ professional interpretation
```

Avoid:

```text
Python
→ generic Python curriculum

Kafka + Spark + Airflow + MLflow + Docker
→ invented end-to-end architecture
```

A vacancy's tool list defines candidate evidence and possibilities. It does not automatically define runtime topology, data flow, latency model, ownership boundaries, or which alternatives are simultaneously used.

---

## 9. Artifact shape

`RoleCapabilityBlueprint` contains:

```text
role_read
likely_role_shape
capability_areas[]
hidden_requirements[]
likely_end_to_end_scenarios[]
what_probably_does_not_matter[]
important_unknowns[]
bottom_line
```

Each capability area contains:

```text
name
interpretation_strength
likely_depth
why_this_matters
likely_subskills[]
likely_tools_or_examples[]
likely_work_products[]
likely_failure_modes_or_operational_concerns[]
probably_not_required[]
```

Each scenario contains:

```text
name
why_likely
flow_steps[]
engineering_concerns[]
interpretation_strength
```

No exact-quote requirement exists in the Blueprint. Audit-grade exact evidence belongs upstream.

---

## 10. Current implementation

Implemented:

- independent Blueprint persistence/attempt history;
- exact source/translation/P1.6/Capability dependency identity;
- one bounded generation plus one structural validation retry;
- no arbitrary long-read deadline after successful local connection;
- dedicated Blueprint model configuration;
- browser Blueprint page;
- CLI `jobhunter jobs blueprint <job-id>`;
- Review Snapshot export;
- interpretation-strength enum;
- source-named/likely-example/possible-example tool relationships;
- structural certainty-language checks for some obvious contradictions;
- practitioner/domain-specialist prompt framing;
- generic optionality and evidence-density calibration rules.

---

## 11. Live acceptance evidence

### `t4jp`

Sparse AI/content posting. Useful for checking that the Blueprint does not manufacture sophisticated engineering depth from a weak advertisement.

Observed lesson:

- source weakness must remain visible;
- `child health` company context does not automatically prove a highly regulated/clinical workflow;
- `website design` does not prove a CMS/backend/deployment stack;
- AI-assisted content work does not automatically mean AI pipeline engineering.

### `tG9K`

Rich semiconductor/industrial-ML posting. Current full chain completed successfully and is available through:

```text
review-snapshots/jobs/tG9K.json
```

The product structure proved useful, but the first v2 snapshot still showed expert-judgment calibration problems:

- independently named technologies were assembled into one `highly_likely` architecture;
- a real-time anomaly-detection flow was called highly likely while required latency remained unknown;
- optional edge deployment was treated too strongly;
- some named tools were assigned specific runtime roles not established by the vacancy;
- plausible domain ideas became more specific than the source justified.

These are not reasons to weaken the layer into source restatement. They are reasons to improve general certainty discipline and compare stronger reasoning models.

---

## 12. Quality strategy

Do not build a prompt patch list for individual semiconductor mistakes.

General rules:

1. A technology list is not an architecture specification.
2. Optional source wording must remain optional.
3. `highly_likely` cannot coexist with a directly contradictory unresolved unknown.
4. Tool/framework/protocol/metric names keep their normal technical meaning.
5. Company-domain text supports context but does not manufacture regulation, scale, or proprietary systems.
6. Scenario detail scales with evidence density.
7. Reasonable alternatives remain visible when the vacancy does not pick one.
8. Prefer useful narrowing over curriculum dumping.
9. Technical correctness matters more than sophisticated prose.

Repeatable deterministic contradictions may become validators/tests. Domain correctness should primarily be evaluated through heterogeneous live examples and model comparison rather than hard-coding domain lessons.

---

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

The Blueprint model may therefore be stronger than the P1.6 extractor without changing factual extraction.

Controlled comparison keeps source, translation, P1.6, Capability artifact, prompt/schema, and review rubric fixed while changing the Blueprint model.

Do not introduce multi-model voting.

---

## 14. Acceptance gate

Blueprint v2 is accepted for the bounded slice only when representative review shows that it:

1. materially improves human understanding beyond the advertisement;
2. preserves upstream optionality and unknowns;
3. does not systematically invent architecture from stack lists;
4. uses `highly_likely`, `plausible`, and `speculative` coherently;
5. keeps inferred tools/examples clearly non-employer-factual;
6. demonstrates acceptable domain/tool correctness across materially different roles;
7. avoids generic curriculum dumping;
8. provides useful probable non-requirements and unknowns;
9. persists/reuses exact dependency identity;
10. is reviewable through repository snapshots;
11. passes deterministic Ruff/pytest/warnings gates for the accepted head;
12. is not automatically generated across the corpus before CI-3 acceptance.

The representative job set and exact execution order are controlled by `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 15. Non-goals

Do not build yet:

- corpus-wide Blueprint generation;
- personal fit/readiness scoring;
- learning-plan generation;
- application ranking;
- model voting/ensembles;
- vector/RAG infrastructure;
- domain-specific prompt patch collections;
- automatic architecture generation presented as employer truth.
