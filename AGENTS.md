# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product and engineering priority

JobHunter is a real repeated-use **local-first personal career-intelligence application**. Prefer dependable, inspectable, evidence-grounded behavior over impressive complexity. Speed means coherent useful increments, not bypassing tests, bounds, provenance, source policy, acceptance, or state.

The mature product is not merely a scraper, generic matcher, resume generator, or autonomous application bot.

## 2. Required reading order

Before material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
5. `docs/SOURCE_POLICY.md`
6. `docs/ROADMAP.md`
7. `docs/IMPLEMENTATION_PLAN.md`
8. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`
9. `docs/EXECUTION_TODO.md`
10. `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` while the semantic gate is active
11. `docs/WORKING_MEMORY.md`
12. task-specific docs and selected review snapshots as needed.

Proposal/experiment/working-memory files do not override controlling product, architecture, roadmap, implementation, or source-policy documents.

Authority:

```text
product/domain/source/architecture
→ roadmap
→ implementation plan
→ active phase/focused plan
→ execution TODO
→ implementation/tests/live acceptance
```

If artifacts conflict, reconcile them rather than choosing the convenient instruction.

## 3. Current exact implementation state

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Role Blueprint candidate:     role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5

Review Snapshot:              job-review-snapshot-v1
```

Accepted English P1.6 anchor for the current dense live case is `tG9K` artifact **29**. Accepted B3 Capability anchor is `tG9K` artifact **9**.

Capability v7/v4 passed the bounded B3 `tG9K` semantic gate and is frozen while B4 proceeds. This does not replace the later heterogeneous CI-3/B5 review. Capability v6/v3 artifact 8 remains rejected live evidence; Capability v5 remains a historical failed output-budget experiment.

Blueprint history:

- v3/v2 failed B4 structurally and semantically with E2B and E4B; preserve its validators and negative evidence;
- v4/v3 fixed deterministic provenance and passed its live mechanical audit, but failed B4 semantic calibration because generated prose manufactured employer-specific operating/topology/ownership claims;
- v5/v4 excluded Capability-derived prose and removed most expansion surfaces, but live `tG9K` artifact **6** still failed B4 because its free-form `practical_interpretation` described end-to-end infrastructure, telemetry streaming, automated MLOps workflows, and deployment-lifecycle scope while its uncertainty admitted ownership boundaries were unknown;
- v6/v5 removes the remaining free-form positive summary surface and is the active **B4 candidate runtime on `main`**.

Current controlled model roles are:

```text
English P1.6:  gemma-4-e4b-it-ud
Capability:    gemma-4-e2b-it
Blueprint:     gemma-4-e4b-it-ud
```

## 4. Current exact next-work rule

```text
1. keep tG9K English projection artifact 33 fixed
2. keep tG9K English P1.6 artifact 29 fixed
3. keep accepted Capability v7/v4 artifact 9 fixed
4. run Blueprint v6/v5 against that exact chain with Blueprint E4B
5. regenerate the tG9K Review Snapshot only after a valid v6 artifact exists
6. run scripts/audit_blueprint_v6_snapshot.py
7. perform complete semantic review of every v6 professional consideration and unknown
8. if B4 passes, freeze the bounded Blueprint contract and continue heterogeneous CI-3/B5
9. if B4 fails, diagnose the general contract/model failure; do not accumulate prompt patches
10. finish Phase-1 Market/source/lifecycle/partial-success/P1.7 gates
11. close Phase 1
12. only then begin corpus-wide Phase 2
```

Do not rerun translation, accepted P1.6 or Capability merely to test Blueprint.

## 5. Permanent semantic layer boundary

```text
source/original employer text
→ parsed fields
→ English projection
→ P1.6 factual extraction
→ Capability grouping/reasoning
→ Blueprint professional interpretation
```

No downstream layer replaces upstream authority. A mechanically linked downstream statement is not automatically semantically true.

### P1.6

P1.6 is the strict factual substrate:

- preserve explicit source facts and exact evidence;
- account for meaningful requirements on dense postings;
- keep obligation strength and technical depth separate;
- never spread one depth adjective across neighboring technologies;
- preserve optional/contextual wording;
- uncertain source claims remain contextual/unknown rather than forced.

### Capability Intelligence

Capability is auditable machine reasoning above accepted P1.6.

Current v7 boundary:

```text
accepted P1.6
→ JobHunter deterministic source partition
→ model semantic grouping + derived reasoning draft
→ complete-coverage validation
→ JobHunter deterministic source_truth / strength / explicit depth / explicit work
→ persisted Capability artifact
```

For v7:

- every capability-relevant accepted P1.6 requirement must be linked to at least one profile;
- every accepted responsibility must be linked to at least one profile;
- role-level education and standalone experience-duration constraints remain in deterministic `source_truth`;
- dense sources cannot collapse into one catch-all capability;
- `requirement_strength` is JobHunter-derived;
- source-explicit depth is JobHunter-derived;
- source-explicit work activities are JobHunter-derived;
- positive independence/ownership synthesis is deliberately deferred;
- cross-capability synthesis is deliberately deferred;
- model reasoning must not strengthen contextual/preferred tools into mandatory/mastery claims;
- evidence must be semantically relevant, not merely an exact quote.

B3 acceptance note: `docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md`.

Important downstream rule learned from B4: **accepted Capability grouping may flow downstream, but Capability model-derived prose is not automatically authoritative downstream context.**

### Role Capability Blueprint

Blueprint is the human-facing professional interpretation layer.

Current v6 boundary:

```text
accepted P1.6 + accepted Capability grouping
→ JobHunter builds source-grounded ordered Capability inputs
→ model emits only explicitly uncertain professional considerations + unknowns
→ JobHunter deterministically attaches Capability identity/coverage
→ JobHunter deterministically attaches P1.6 requirements/responsibilities/evidence
→ JobHunter deterministically attaches source role purpose and role-level constraints
→ persisted Blueprint v6/v5 artifact
```

For v6:

- the model does **not** receive Capability `summary`, `sub_capabilities`, `underlying_knowledge`, operational reasoning, or other derived Capability prose;
- the model does **not** receive duplicated long vacancy/company-description prose after P1.6 has established source truth;
- the model does **not** emit Capability, requirement, or responsibility numeric provenance;
- the model does not regroup, merge, split, or rename accepted Capability profiles;
- persisted Blueprint areas map one-to-one to accepted Capability profiles in source order;
- source role purpose, requirements, responsibilities, obligation strength, explicit depth, evidence and role constraints are JobHunter-owned deterministic anchors;
- there is no free-form model-generated `practical_interpretation`, role shape, likely depth, hidden requirement, tool recommendation, work-product list, scenario/topology, probably-not-required list, or bottom line;
- positive model output exists only as `professional_considerations` with `plausible` or `speculative` strength plus mandatory uncertainty;
- every Capability must expose at least one `important_unknown`;
- model-created obligation language and full/end-to-end lifecycle/stack/pipeline/system/infrastructure scope are rejected generically;
- technology list != architecture;
- high-volume data does not prove streaming;
- process control/anomaly detection does not prove real-time or low-latency behavior;
- APC/SPC terminology does not prove an automated feedback loop;
- cloud/edge names do not prove deployment placement;
- deployment/governance work does not prove lifecycle ownership;
- unknowns must not smuggle assumptions into their wording;
- contextual/preferred source items remain contextual/preferred;
- explicit depth remains attached to the exact source concept;
- technical correctness and calibrated uncertainty matter more than impressive prose;
- avoid domain-specific prompt-patch collections.

Historical v3 failure: `docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md`.  
Historical v4 provenance/semantic result: `docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md`.  
Historical v4 failure/v5 decision: `docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md`.  
Historical v5 failure/v6 decision: `docs/experiments/2026-08-11_BLUEPRINT_V5_SEMANTIC_FAILURE_AND_V6_BOUNDARY.md`.

## 6. Current live acceptance anchors

```text
t4jp  sparse/ambiguous AI-content source
tG9K  rich semiconductor/industrial-ML source
```

`t4jp` checks conservative behavior on weak evidence. `tG9K` checks dense factual coverage and deeper reasoning.

Selected review artifact:

```text
review-snapshots/jobs/tG9K.json
```

The currently committed snapshot contains Blueprint v5 artifact 6 as **rejected review evidence**, not an accepted B4 baseline. The next intended snapshot is generated only after the active v6 candidate succeeds.

The Capability CLI showing five of six explicit depth facts inside profiles is intentional: the sixth depth fact is role-level professional experience (`three to six years`, requirement 26) and remains in deterministic source truth instead of being forced into a capability profile.

## 7. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally; never commit the live SQLite DB, WAL/SHM, raw model responses/prompts, secrets, logs, raw HTML contents, or future private user state.

The tracked `jobhunter.toml` is public project configuration. It currently contains no secret. Never put an actual API token/password/key into tracked `jobhunter.toml`; use an ignored `.env` or other local secret mechanism.

The `status` object determines whether downstream artifacts belong to the selected current dependency chain. A stale Blueprint must not be exported as current.

## 8. Record boundaries

Never conflate:

```text
JobPosting
SearchPageSnapshot
JobPostingVersion
JobDetailFetchObservation
JobLifecycle state/event
JobTranslationArtifact
JobAnalysisArtifact
Capability artifact
Role Blueprint artifact
JobUserWorkflow
Market aggregate
Review Snapshot
Raw evidence
```

Preserve provenance and dependency identity across every derived layer.

## 9. Interaction, security, and source rules

```text
local browser UI   normal repeated human use
CLI                automation/debug/advanced operation
```

Both surfaces use shared services and state.

Permanent constraints:

- loopback-first browser binding;
- CSRF on mutating forms;
- restrictive security headers and local static assets;
- acquired content is untrusted data;
- one mutable browser operation at a time unless concurrency is proven safe;
- no application/login automation, CAPTCHA/access bypass, proxy rotation, or autonomous recruiter messages;
- source/network/429/5xx/challenge/auth failures are **not** equivalent to an expired/removed vacancy;
- bounded sequential/rate-limited acquisition;
- raw valid evidence before downstream processing;
- search vocabulary is TOML data, not hard-coded career taxonomy.

## 10. Translation and inference rules

Trusted translation contracts:

```text
lm-studio-translation-v2
english-projection-v2
```

Source remains authoritative; English is derived.

For local long reasoning:

```text
connect timeout: bounded
read timeout after connection: none
write/pool: bounded
transport replay: disabled
max tokens: bounded
validation retries: bounded separately
```

Blueprint runtime prepares the selected LM Studio model automatically at a 16,384-token context window. V6 caps its structured completion at 4,096 tokens. Do not require manual LM Studio context reconfiguration for normal Blueprint execution.

Independent model roles are supported:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Use controlled same-job comparison when model adequacy is the variable. Do not change evidence, contract, and model simultaneously. No multi-model voting unless future measured evidence justifies it.

Editable installs may create `*.egg-info/`; package metadata is ignored by Git.

## 11. Market and personal-evidence boundaries

Current Market aggregates accepted/current English P1.6 only. Preserve sample size, source/filter scope, requirement-strength semantics, contract identity, and concentration/small-sample warnings.

Do not implement durable personal readiness/gap/recommendation claims until a reviewed personal-evidence schema exists with depth, confidence, recency, evidence references, limitations, and AI-assistance/independence context.

## 12. Architecture-evolution discipline

- preserve the local modular monolith;
- keep SQLite until measured limits justify replacement;
- implement a real second source before a generic source/plugin abstraction;
- use structured/keyword retrieval before embeddings/RAG;
- no graph/vector DB or autonomous agent orchestration without demonstrated query/product need and explicit privacy/provenance/budget controls.

## 13. Development and definition of done

- build coherent vertical increments;
- separate deterministic logic from network/model/provider calls;
- keep handlers thin and SQL focused;
- use typed config and versioned contracts;
- preserve historical artifacts;
- reconcile current-state docs when behavior materially changes;
- normal tests never contact Jobinja/Google/LM Studio;
- convert repeatable deterministic incidents into fixtures when possible.

An increment is done only when the intended workflow works, Ruff/tests/warnings gates pass, live behavior is reviewed when required, failures remain bounded/inspectable, provenance is preserved, docs match behavior, and no unrelated future scope is claimed.

Work directly on `main` unless the repository owner explicitly requests isolation or a concrete isolation need is agreed first.
