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

Role Blueprint candidate:     role-capability-blueprint-v4
Blueprint schema:             role-capability-blueprint-v3

Review Snapshot:              job-review-snapshot-v1
```

Accepted English P1.6 anchor for the current dense live case is `tG9K` artifact **29**. Accepted B3 Capability anchor is `tG9K` artifact **9**.

Capability v7/v4 passed the bounded B3 `tG9K` semantic gate and is frozen while B4 proceeds. This does not replace the later heterogeneous CI-3/B5 review. Capability v6/v3 artifact 8 remains rejected live evidence; v5 remains a historical failed output-budget experiment.

Blueprint v3/v2 failed B4 with both E2B and E4B. Both models confused P1.6 requirement indices with Capability-profile indices; E4B's bounded repair also placed requirement IDs into the depth field. Both runs retained material semantic overreach around streaming, cloud/edge, MLOps and end-to-end architecture. Preserve v3/v2 as negative evidence; do not weaken its validators or revive it with prompt patches.

Blueprint v4/v3 is the active **B4 candidate runtime on `main`**. It is not semantically accepted until a live Blueprint built from Capability artifact 9 passes the v4 mechanical audit and complete semantic review.

Current controlled model roles are:

```text
English P1.6:  gemma-4-e4b-it-ud
Capability:    gemma-4-e2b-it
Blueprint:     gemma-4-e4b-it-ud
```

## 4. Current exact next-work rule

```text
1. keep tG9K English P1.6 artifact 29 fixed
2. keep accepted Capability v7/v4 artifact 9 fixed
3. run Blueprint v4/v3 against that exact chain with Blueprint E4B
4. regenerate the tG9K Review Snapshot only after a valid Blueprint artifact exists
5. run scripts/audit_blueprint_v4_snapshot.py
6. perform complete semantic review of the Blueprint artifact
7. if B4 passes, freeze the bounded Blueprint contract and continue heterogeneous CI-3/B5
8. if B4 fails, diagnose the structural/model/semantic failure; do not accumulate prompt patches
9. finish Phase-1 Market/source/lifecycle/partial-success/P1.7 gates
10. close Phase 1
11. only then begin corpus-wide Phase 2
```

Do not rerun accepted P1.6 or Capability merely to test Blueprint. Keep the accepted upstream artifacts and model roles fixed during the first v4 `tG9K` comparison.

## 5. Permanent semantic layer boundary

```text
source/original employer text
→ parsed fields
→ English projection
→ P1.6 factual extraction
→ Capability reasoning
→ Blueprint interpretation
```

No downstream layer replaces upstream authority.

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

### Role Capability Blueprint

Blueprint is the human-facing professional interpretation layer.

Current v4 boundary:

```text
accepted P1.6 + Capability v7
→ JobHunter builds compact ordered capability inputs
→ model interprets exactly one item per accepted Capability profile
→ JobHunter deterministically attaches Capability identity/coverage
→ JobHunter deterministically attaches P1.6 requirements/responsibilities
→ JobHunter deterministically attaches role-level constraints
→ persisted Blueprint v4/v3 artifact
```

For v4:

- the model does **not** emit Capability, requirement, or responsibility numeric provenance;
- the model does not regroup, merge, split, or rename accepted Capability profiles;
- persisted Blueprint areas map one-to-one to accepted Capability profiles in source order;
- source requirements/responsibilities, obligation strength, explicit depth and evidence are JobHunter-owned anchors;
- source-named technologies remain visible through those deterministic source requirements rather than model-created `source_named` tool records;
- model-created `suggested_tools_or_examples` are only `likely_example` or `possible_example` and carry no source provenance;
- suggested tools cannot become required/mandatory/necessary or inherit expert/mastery depth;
- role-level degree/experience constraints are copied deterministically from Capability source truth;
- model-created hidden requirements are only `plausible` or `speculative`;
- model-created scenarios are always `professional_example` and only `plausible` or `speculative`;
- illustrative scenarios must state assumptions for unstated topology, latency, vendor, batch/stream mode, cloud/edge placement, scale, ownership, orchestration, or feedback-loop behavior;
- technology list != architecture;
- examples remain examples;
- source optionality and exact depth survive downstream;
- technical correctness matters more than sophisticated prose;
- avoid domain-specific prompt-patch collections.

Historical negative evidence: `docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md`.
Current B4 redesign: `docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md`.

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

The current committed `tG9K` snapshot contains accepted P1.6 artifact 29 and accepted B3 Capability v7/v4 artifact 9. It has no accepted current-chain Blueprint yet; the next live step is to generate Blueprint v4/v3 from that exact chain.

The Capability CLI showing five of six explicit depth facts inside profiles is intentional: the sixth depth fact is role-level professional experience (`three to six years`, requirement 26) and remains in deterministic source truth instead of being forced into a capability profile.

## 7. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally; never commit the live SQLite DB, WAL/SHM, raw model responses/prompts, secrets, local config, logs, raw HTML contents, or future private user state.

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

Blueprint runtime prepares the selected LM Studio model automatically at a 16,384-token context window. Do not require manual LM Studio context reconfiguration for normal Blueprint execution.

Independent model roles are supported:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Use controlled same-job comparison when model adequacy is the variable. Do not change evidence, contract, and model simultaneously. No multi-model voting unless future measured evidence justifies it.

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