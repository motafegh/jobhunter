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

Capability candidate:         job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Role Blueprint:               role-capability-blueprint-v2
Blueprint schema:             role-capability-blueprint-v1

Review Snapshot:              job-review-snapshot-v1
```

Accepted English P1.6 anchor for the current dense live case is `tG9K` artifact **29**.

Capability v7/v4 is the active **B3 candidate runtime on `main`**, not an accepted semantic contract yet. Capability v6/v3 artifact 8 is retained as rejected live evidence. Capability v5 is a historical failed output-budget experiment. Do not call v4/v2, v5, or v6/v3 the current Capability runtime.

Do not rebuild the Role Blueprint until B3 Capability acceptance passes.

## 4. Current exact next-work rule

```text
1. run Capability v7/v4 against fixed tG9K P1.6 artifact 29
2. regenerate the tG9K Review Snapshot
3. run scripts/audit_capability_v7_snapshot.py
4. perform complete semantic review of the v7 artifact
5. if B3 passes, reconcile acceptance docs and continue to Blueprint B4
6. if B3 fails, diagnose the bounded structural/model failure; do not accumulate prompt patches
7. after B4, complete heterogeneous CI-3 review
8. finish Phase-1 Market/source/lifecycle/partial-success/P1.7 gates
9. close Phase 1
10. only then begin corpus-wide Phase 2
```

Do not rerun accepted P1.6 merely to test Capability. Keep model roles fixed during the first v7 `tG9K` comparison.

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

### Role Capability Blueprint

Blueprint is the later human-facing professional interpretation layer.

- technology list != architecture;
- examples remain examples;
- `highly_likely` must not contradict unresolved unknowns;
- source optionality survives downstream;
- technical correctness matters more than sophisticated prose;
- avoid domain-specific prompt-patch collections.

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

Current committed `tG9K` snapshot contains accepted P1.6 artifact 29 and rejected Capability v6/v3 artifact 8. It is negative B3 evidence until a live v7 snapshot replaces it.

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
