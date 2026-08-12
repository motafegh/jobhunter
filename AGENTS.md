# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product and engineering priority

JobHunter is a repeated-use **local-first personal career-intelligence application**. Prefer dependable, inspectable, evidence-grounded behavior over impressive complexity. Speed means coherent useful increments, not bypassing tests, provenance, bounds, source policy, acceptance, or state.

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
12. task-specific experiment records and selected review snapshots as needed.

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

## 3. Current implementation and acceptance state

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5

Review Snapshot:              job-review-snapshot-v1
```

Accepted dense anchors:

```text
tG9K English projection artifact 33
tG9K English P1.6 artifact 29
tG9K Capability v7 artifact 9
```

P1.6 artifact 29 passed bounded factual coverage/optionality/depth review. Capability artifact 9 passed bounded B3/SQ-2 review with 25/25 capability-relevant requirements and 7/7 responsibilities linked plus complete deterministic source truth.

Capability v7/v4 is frozen unless heterogeneous evidence reveals a repeatable material correctness defect.

## 4. Blueprint disposition

Blueprint is implemented and remains inspectable, but **is not an accepted Phase-1 decision layer**.

Experiment history:

- v3/v2 failed provenance/index handling and semantic calibration with E2B/E4B;
- v4/v3 fixed deterministic provenance but broad generated prose still manufactured employer-specific operating/topology/ownership claims;
- v5/v4 removed Capability-derived prose and most expansion surfaces but free-form interpretation still inflated end-to-end/streaming/lifecycle scope;
- v6/v5 removed free-form role-summary generation and limited the model to uncertain professional considerations + unknowns;
- v6/E4B still failed structured repair and introduced assumptions;
- controlled v6/12B artifact 7 passed mechanical audit and CI and was materially better, but complete semantic review still found assumption-bearing unknowns/considerations.

Best bounded experimental Blueprint evidence:

```text
job: tG9K
artifact: 7
prompt: role-capability-blueprint-v6
schema: role-capability-blueprint-v5
model: gemma-4-12b-it-qat
snapshot commit: 671bd6e3c43555c631958531671a0f1be9726554
```

Do not call that artifact accepted.

During Phase 1:

- do not create Blueprint v7;
- do not weaken validators;
- do not add vacancy/domain-specific prompt patches;
- do not continue adjacent model shopping;
- do not use Blueprint for Market, personal readiness, automatic recommendations, or other authoritative decisions;
- Blueprint may be observed only as non-gating research evidence.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

Reopen Blueprint only when a materially different grounding/inference approach or a demonstrated product-value gap justifies it.

## 5. Current exact next-work rule

The active semantic gate is heterogeneous validation of the accepted stack:

```text
source
→ English projection
→ P1.6 factual extraction
→ Capability v7
```

Target materially different roles:

```text
t4jp  sparse/ambiguous anchor
tG9K  rich industrial AI/ML baseline
+ Python/software
+ network/security
+ operations/platform/DevOps
```

For each selected role review factual coverage, evidence, requirement strength, explicit depth, role-level constraints, Capability coverage/grouping/source truth, and optionality calibration.

Convert repeatable deterministic defects into tests. Record model limitations separately. Do not patch one vacancy at a time.

After heterogeneous semantic acceptance:

```text
Market truthfulness/sampling
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```

## 6. Permanent semantic boundaries

### P1.6

P1.6 is the strict factual substrate:

- preserve explicit source facts and exact evidence;
- account for meaningful requirements on dense postings;
- remain restrained on sparse postings;
- keep obligation strength and technical depth separate;
- never spread one depth adjective across neighboring technologies;
- preserve optional/contextual wording;
- uncertain source claims remain contextual/unknown rather than forced.

### Capability Intelligence

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

- every capability-relevant accepted P1.6 requirement must link to at least one profile;
- every accepted responsibility must link to at least one profile;
- role-level education/experience-duration constraints remain deterministic source truth;
- dense sources cannot collapse into one catch-all profile;
- source strength/depth/work are JobHunter-derived;
- positive ownership/independence synthesis is deferred;
- cross-capability synthesis is deferred;
- contextual/preferred tools must not become mandatory/mastery claims;
- evidence must be semantically relevant, not merely exact text.

Important downstream lesson: **Capability grouping and deterministic source truth may flow downstream; Capability model-derived explanatory prose is not automatically authoritative.**

### Blueprint

Blueprint is experimental professional interpretation above accepted source truth. Its code may remain available, but its generated prose is not Phase-1 authority.

No downstream layer replaces upstream authority. Mechanical linkage never certifies semantic truth.

## 7. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally; never commit SQLite/WAL/SHM, raw model responses/prompts, secrets, logs, raw HTML contents, or future private user state.

The current committed `tG9K` snapshot contains Blueprint artifact 7 as **experimental rejected B4 evidence**, while P1.6 artifact 29 and Capability artifact 9 remain accepted bounded anchors.

The `status` object determines whether downstream artifacts belong to the selected dependency chain; current-chain status is not semantic acceptance.

The tracked `jobhunter.toml` is public project configuration. Never place actual API tokens/passwords/keys in it; use an ignored local secret mechanism.

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

Permanent constraints:

- loopback-first browser binding;
- CSRF on mutating forms;
- restrictive security headers and local static assets;
- acquired content is untrusted data;
- one mutable browser operation at a time unless concurrency is proven safe;
- no application/login automation, CAPTCHA/access bypass, proxy rotation, or autonomous recruiter messages;
- network/429/5xx/challenge/auth failures are **not** equivalent to an expired/removed vacancy;
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

Independent model roles are supported. The current experimental Blueprint model is `gemma-4-12b-it-qat`; this does not make Blueprint accepted.

Use controlled same-job comparison when model adequacy is genuinely the variable. Do not change evidence, contract and model simultaneously. No multi-model voting unless future measured evidence justifies it.

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
