# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product and engineering priority

JobHunter is a repeated-use **local-first personal career-intelligence application**. Prefer dependable, inspectable, evidence-grounded behavior over impressive complexity. Speed means coherent useful increments, not bypassing tests, provenance, bounds, source policy, acceptance, or state.

The mature product is not merely a scraper, generic matcher, resume generator, or autonomous application bot.

## 2. Required reading order and authority

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
12. task-specific experiment/working-memory records, `corpus/README.md`, and selected review snapshots as needed.

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
parser:                     jobinja-detail-v2
translation provider:       lm-studio-translation-v2
English projection:         english-projection-v2

English P1.6 public:        job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:       job-analysis-original-v9 / job-analysis-v4

Capability public/current:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Capability v7:              historical
Capability v8:              historical / semantic reject

Blueprint experimental:     role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:            job-review-snapshot-v1
Public Corpus:              jobhunter-public-corpus-v1
```

Accepted/current opposite-end anchors:

```text
tG9K English P1.6 artifact 36 → Capability v9 artifact 11
t4jp English P1.6 artifact 37 → Capability v9 artifact 12
```

Capability v9 public promotion is closed and operationally verified. Normal public commands reuse artifacts 11/12 on P1.6 artifacts 36/37, Review Snapshot marks those chains current, and Blueprint remains non-current.

The public corpus is also operationally closed and remotely available. The accepted publication baseline is:

```text
known/discovered Jobinja jobs: 344
fetched/parsed detail jobs:      43
English projections:             33
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Do not reopen P1.6 v20 or Capability v9 merely for harmless non-authoritative wording variation. Reopen only for a repeatable material correctness/provenance/contract defect or a changed accepted dependency.

## 4. Blueprint disposition

Blueprint is implemented and inspectable but **is not an accepted Phase-1 decision layer**.

Historical v6/12B artifact 7 remains experimental evidence. Complete semantic review found assumption-bearing interpretation beyond vacancy authority even after mechanical provenance passed.

During Phase 1:

- do not create Blueprint v7;
- do not weaken Blueprint validators;
- do not add vacancy/domain-specific prompt patches merely to obtain a passing artifact;
- do not use Blueprint for Market, personal readiness, automatic recommendations, or other authoritative decisions;
- keep Blueprint v6 pinned to historical Capability v7 dependency semantics until an explicit evidence-backed reopening decision.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## 5. Current exact next-work rule

The public-corpus implementation/backfill/publish gate is **closed**. Heterogeneous live semantic validation is the active gate.

Current order:

```text
1. Python/software             → tmBK P1.6 39 / Capability 13 ACCEPTED
2. network/security            → t4qV P1.6 44 / Capability 14 ACCEPTED
3. operations/platform/DevOps  → tmyX P1.6 46 / Capability 15 ACCEPTED
```

The accepted Python/software anchor is:

```text
tmBK — Python Developer
source detail version:       44
English projection artifact: 38
P1.6 contract:               job-analysis-english-v20 / job-analysis-v5
accepted P1.6 artifact:      39
accepted Capability artifact: 13
```

`tmBK` is closed and accepted after complete P1.6 and Capability review. Artifact 39 has 16 requirements, 0 responsibilities, correct 7/7 explicit depth facts, and accepted semantic-review state. Capability 13 covers 16/16 requirements and 7/7 explicit depth facts with no fabricated duties or role-level inflation.

The network/security anchor `t4qV` (detail 30, English projection 20) is accepted on P1.6 artifact 44 and Capability artifact 14. P1.6 artifacts 40-43 remain rejected/archived evidence. General deterministic fixes from those reviews cover:

- exact structured-skill tags materialized deterministically rather than model-restated;
- composite preferred headings retain their optionality in exact evidence;
- explicit experience lower bounds such as `more than six years` remain intact;
- explicit `position/role ... responsible for` clauses enter responsibility coverage;
- explicit pre-heading `we are looking/seeking ... with experience in ...` clauses enter requirement coverage.

The operations/platform anchor `tmyX` (detail 35, English projection 24) is accepted on P1.6 artifact 46 and Capability artifact 15. Artifact 45 was rejected for missing the explicit opening role actions. Its reviews additionally fixed:

```text
generic heading words inside ordinary sentences no longer split evidence
explicit pre-heading candidate duty clauses enter responsibility coverage
Ability to / Skill in application wording stays non-depth without real depth markers
```

Fresh English v20 artifacts are `pending` by default. Pending artifacts must remain excluded from Capability, Market, accepted dashboard counts, and `corpus/`. Use `jobhunter jobs review-analysis <job-id> status|accept|reject`; acceptance/rejection requires a meaningful review note. Existing promoted artifacts 36/37 migrate as accepted.

Heterogeneous semantic validation, Market truthfulness/sampling, and source/lifecycle acceptance are closed. Do not rerun accepted anchors merely for wording variation. The exact next Phase-1 gate is partial-success semantics, followed by P1.7 report/run/browser acceptance.

For each heterogeneous role review factual coverage, evidence, requirement strength, explicit depth, role-level constraints, Capability coverage/grouping/source truth, and optionality calibration.

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
- uncertain source claims remain contextual/unknown rather than forced;
- structured source skills cannot silently disappear;
- qualification wording must not fabricate job duties.

### Capability Intelligence v9

Current accepted architecture:

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic source-link injection
→ deterministic reconciliation
→ persisted Capability
```

Authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Permanent v9 rules:

- every capability-relevant accepted P1.6 requirement must be covered;
- every accepted responsibility must be covered;
- source indices/evidence must be valid and grounded;
- dense sources cannot collapse into one catch-all group;
- source requirement strength, source-explicit depth, and source work are deterministic;
- role-level education/duration-only experience stay separate;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture claims are blocked or filtered;
- zero optional model enrichment is valid;
- redundant model `source_explicit` echoes are discarded; deterministic reconciliation remains authority;
- incomplete authoritative source truth cannot persist.

Important downstream lesson: **Capability grouping and deterministic source truth may flow downstream; model-owned explanatory prose is not automatically authoritative.**

### Blueprint

Blueprint is experimental professional interpretation above historical accepted source truth. Its generated prose is not Phase-1 authority.

No downstream layer replaces upstream authority. Mechanical linkage never certifies semantic truth.

## 7. Versioned public-corpus rules

The local SQLite database remains the operational/runtime authority:

```text
data/jobhunter.sqlite3
```

The repository-safe public projection is:

```text
corpus/
```

Contract:

```text
jobhunter-public-corpus-v1
```

Purpose:

- make every known public Jobinja job remotely inspectable;
- preserve original Persian/English parsed vacancy content as UTF-8 JSON;
- project current successful English projection, P1.6, and Capability artifacts with exact dependency/contract identities;
- support remote AI review, heterogeneous selection, reproducibility, Market work, and later Phase-2 analysis without direct access to local SQLite.

The public corpus is a deterministic projection, **not** a runtime input and **not** a replacement database.

Current layout:

```text
corpus/manifest.json
corpus/jobs/<job-id>/source.json
corpus/jobs/<job-id>/english-projection.json
corpus/jobs/<job-id>/p16-english.json
corpus/jobs/<job-id>/p16-original.json
corpus/jobs/<job-id>/capability.json
```

Optional stage files exist only when that stage is current for the current source dependency. If the source changes, stale downstream files must disappear until rebuilt. Git history preserves previously published states.

Never export into `corpus/`:

- SQLite/WAL/SHM files;
- machine-local evidence paths;
- raw HTML evidence;
- LM Studio request bodies/raw protocol responses;
- prompts/secrets/API credentials;
- logs/debug histories;
- local configuration;
- future private/personal evidence, applications, notes, profiles, or outcomes.

The public corpus contains only public job-domain facts and repository-safe derived intelligence. Any future schema expansion must explicitly review this privacy/public boundary before adding fields.

Normal mutating CLI workflows and completed web background operations synchronize the local `corpus/` projection **after** durable SQLite work. Projection failure must be surfaced but must never roll back durable SQLite success.

JobHunter does **not** automatically Git commit or push. Publishing remains intentional:

```bash
jobhunter-corpus verify
git diff -- corpus/
git add corpus/
git commit -m "data: update JobHunter public corpus"
git push origin main
```

Detailed format and command rules live in `corpus/README.md`.

## 8. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

`review-snapshots/` and `corpus/` are distinct:

```text
corpus/           complete current public dataset
review-snapshots/ selected semantic acceptance/review evidence
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally. Dependency-current flags remain distinct from the explicit P1.6 semantic-review status/time/note.

Never commit SQLite/WAL/SHM, raw model responses/prompts, secrets, logs, raw HTML contents, or future private user state.

The tracked `jobhunter.toml` is public project configuration. Never place actual API tokens/passwords/keys in it; use an ignored local secret mechanism.

## 9. Record boundaries

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
Public Corpus projection
Review Snapshot
Raw evidence
```

Preserve provenance and dependency identity across every derived layer.

## 10. Interaction, security, and source rules

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

## 11. Translation and inference rules

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

Independent model roles are supported. The current experimental Blueprint model does not make Blueprint accepted.

Use controlled same-job comparison when model adequacy is genuinely the variable. Do not change evidence, contract, and model simultaneously. No multi-model voting unless future measured evidence justifies it.

## 12. Market and personal-evidence boundaries

Current Market aggregates accepted/current English P1.6 only. Preserve sample size, source/filter scope, requirement-strength semantics, contract identity, and concentration/small-sample warnings.

Do not implement durable personal readiness/gap/recommendation claims until a reviewed personal-evidence schema exists with depth, confidence, recency, evidence references, limitations, and AI-assistance/independence context.

Personal/private state must never be added to the public corpus merely because it lives in the same local database in a future phase.

## 13. Architecture-evolution discipline

- preserve the local modular monolith;
- keep SQLite until measured limits justify replacement;
- keep runtime authority separate from the versioned public corpus projection;
- implement a real second source before a generic source/plugin abstraction;
- use structured/keyword retrieval before embeddings/RAG;
- no graph/vector DB or autonomous agent orchestration without demonstrated query/product need and explicit privacy/provenance/budget controls.

## 14. Development and definition of done

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
