# JobHunter Master Implementation Plan

## 1. Purpose and authority

This is the single product-level implementation plan for JobHunter. It defines the delivery
order, dependencies, acceptance gates, and what completion means from the current foundation
through the sustained local product.

It is not a learning roadmap and it does not pre-decide low-level architecture that should be
chosen only after later evidence exists.

Detailed Phase 1 source/analysis execution remains subordinate to
[Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

Authority order:

```text
product/specification documents
        ↓
this master implementation plan
        ↓
phase-specific execution plans
        ↓
implementation/tests/live acceptance
```

If a subordinate plan becomes stale, this document controls until the subordinate plan is
reconciled.

## 2. Delivery rules

- Build operable vertical slices rather than disconnected framework work.
- Keep acquisition usable when LM Studio is unavailable.
- Preserve raw evidence before parsing, translation, or analysis.
- Keep source, translation, model analysis, market aggregation, and personal/user state
  separate.
- Prefer local-first providers when they satisfy the requirement.
- Keep search coverage data-driven and acquisition bounded.
- Retry only failure classes explicitly marked retryable.
- Require deterministic tests before live acceptance.
- Require reviewed live examples before trusting model-derived layers at scale.
- Keep browser and CLI on the same application services/database.
- Add UI/product complexity only where repeated operation benefits.
- Preserve historical artifacts rather than silently rewriting them when contracts change.
- Never promote a derived representation above authoritative employer/source evidence.
- Do not infer personal capability or readiness without explicit reviewed personal evidence.

## 3. Product stages

| Stage | Outcome | Status |
|---|---|---|
| M0 | Runnable local foundation, SQLite, LM Studio boundary, tests | Accepted |
| Phase 1 | Complete Jobinja workflow through evidence-backed analysis/reporting | Active |
| Phase 2 | Canonical market intelligence and role/capability taxonomy | Planned |
| Phase 3 | Personal capability evidence and gap intelligence | Planned |
| Phase 4 | Explainable decision/action and application-readiness layer | Planned |
| Phase 5 | Sustained operation, trends, recovery, quality and maintenance | Planned |

## 4. Previously accepted foundation

Before the current hardening/analysis increment, live evidence established:

- repeat-safe Jobinja discovery and identical-rerun idempotency;
- a browser sync with 40/40 search requests, 273 unique postings, 241 new postings,
  32 already-known postings, and zero search failures;
- bounded detail acquisition with 10/10 selected detail pages succeeding;
- 26/26 current parsed jobs structurally clean under parser-v2 audit at that point;
- immutable raw evidence, semantic versions, and fetch observations remaining distinct;
- data-driven Persian/English search profiles and packs;
- local LM Studio translation, artifact reuse, and bounded output-truncation recovery;
- 15/15 English artifacts under translation v1 before a real field-association defect was
  discovered on later translations;
- local browser application, guided sync controls, Quick Add, concise operation summaries,
  and missing-detail backlog acquisition working against the real corpus.

Translation v1 remains historical because field-to-translation association corruption was
observed in real data.

## 5. Current stabilization gate — do this before more features

The current large implementation is not accepted until this sequence is green in order.

### S0.1 Database migration compatibility

Purpose: older JobHunter SQLite files must upgrade cleanly before newer translation/analysis
repositories query modern columns or tables.

Required:

- core `JobHunterStore.initialize()` performs source-schema migration first;
- dependent repositories initialize the core schema before their own tables/queries;
- legacy migration tests pass;
- no existing source/evidence/history rows are rewritten destructively.

### S0.2 P1.6 authoritative evidence boundary

Only actual employer/job fields may enter the authoritative evidence pool.

Exclude parser metadata such as:

```text
language
parser_version
```

from:

- the P1.6 authoritative-source prompt payload;
- evidence-substring validation;
- any future claim citation path.

### S0.3 Deterministic quality gate

Run in order:

```text
ruff check .
pytest
pytest -W error
```

Fix actual residual failures one root cause at a time. Do not interpret cascaded database
failures as independent defects until migration/initialization failures are removed.

### S0.4 Real-corpus migration gate

Only after the deterministic suite is green:

1. open the existing real database through the new code;
2. confirm migration is non-destructive;
3. confirm old v1 translation artifacts still exist historically;
4. confirm they no longer count as current v2 artifacts;
5. repair one previously corrupted job to v2;
6. inspect it manually;
7. repair a second previously corrupted job;
8. inspect it manually;
9. repair the remaining current parsed corpus in bounded batches;
10. export only current v2 English artifacts.

### S0.5 First semantic-analysis acceptance

1. choose one reviewed current v2 job;
2. run P1.6 analysis;
3. inspect every role-purpose/responsibility/requirement claim;
4. verify its evidence is an exact excerpt of employer text;
5. verify required/preferred/contextual/inferred strength is preserved;
6. verify unsupported concepts were omitted or rejected;
7. rerun and confirm artifact reuse;
8. analyze a small batch, default 5;
9. inspect the Market page only after that reviewed sample is acceptable.

No large-scale analysis before this gate passes.

## 6. Phase 1 — complete source-to-market workflow

### P1.0 Repository alignment and controlling plan

Status: accepted.

### P1.1 Search acquisition and persisted discovery

Status: accepted.

Capabilities:

- approved public Jobinja source boundary;
- immutable search-page evidence;
- stable logical posting identity;
- repeat-safe discovery.

### P1.2 Bounded pagination, multiple searches, repeat-safe discovery

Status: accepted.

Capabilities:

- global request budget;
- page limits;
- Persian/English search profiles/packs;
- cross-search deduplication;
- deterministic round-robin search windows.

### P1.3 Detail acquisition, response classification and retry policy

Status: implementation present; acceptance pending.

Current/required classes:

```text
active
rate_limited
access_denied
challenge
auth_required
not_found
gone
server_error
network_error
unexpected_page
expired_explicit
```

Required behavior:

- preserve normal successful evidence before parsing;
- bounded retry only for transient network/429/selected 5xx classes;
- never blindly retry CAPTCHA/challenge/auth/access-denied/not-found classes;
- expose classification and retryability in operations/history;
- add representative fixtures and live examples where safely reproducible.

Definition of done:

- deterministic classification/retry tests green;
- real normal/expired/error examples inspected;
- acquisition remains independent from LM Studio.

### P1.4 Parser, multilingual handling and hardened English projection

Parser status: accepted foundation.

Translation-v2 status: implemented; stabilization/live migration pending.

Current v2 contract:

```text
current parsed source version
→ collect Persian/mixed semantic strings
→ bounded one-segment local translation requests
→ content-derived response identity
→ structured-output validation
→ deterministic source/English integrity checks
→ persist english-projection-v2 only when clean
```

Requirements:

- v1 remains historical;
- current export accepts v2 only;
- corrupt field permutations never become current artifacts;
- translation failure never mutates source evidence/version history;
- native-English jobs retain identity projections without model calls;
- add a reviewed Persian→English golden corpus before choosing a permanent translation
  model based on quality claims.

### P1.5 Identity, lifecycle, user triage and acquisition priority

Status: semantic versions/observations accepted; lifecycle/triage/priority implementation
pending acceptance.

Lifecycle rules:

- normal successful detail -> active;
- explicit source expiry -> expired;
- first 404/410 -> possibly_unavailable;
- repeated 404/410 evidence may transition -> removed;
- rate limit/access/challenge/server/network failure must not become destructive lifecycle
  conclusions.

User workflow state remains separate from source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Priority selection may use discovery/search/title evidence to decide which missing details to
fetch first. It must not be presented as personal fit or market importance.

Remaining P1.5 work:

- last-successful-check and consecutive-failure summaries;
- stronger lifecycle UI;
- repost/near-duplicate classification after enough corpus evidence exists;
- bulk triage/fetch/translate/analyze acceptance over real corpus.

### P1.6 Evidence-backed local semantic analysis

Status: implemented; pending deterministic and reviewed live acceptance.

Artifact identity:

```text
source detail version
+ current hardened English artifact
+ exact LM Studio model
+ prompt version
+ analysis schema version
```

Current schema:

- role purpose;
- responsibilities;
- requirements;
- requirement strength: required / preferred / contextual / inferred;
- concept type: tool / skill / knowledge / practice / domain / experience / education / other;
- confidence;
- exact original-source evidence excerpt;
- rationale for inferred concepts.

Rules:

- original employer fields are authoritative;
- English v2 is comprehension aid only;
- parser metadata is not employer evidence;
- unsupported/hallucinated evidence rejects the artifact;
- raw model request/response is retained for auditability;
- model/prompt/schema changes create distinct derived artifacts;
- uncertain claims should be omitted rather than guessed.

After first live acceptance, add a review/correction workflow only if real analysis quality
shows that human correction is needed often enough to justify it.

### P1.7 Individual outputs, aggregate market view and complete Phase-1 run

Status: partial implementation.

Already implemented:

- per-job analysis surface;
- first Market aggregation over accepted current analysis artifacts;
- search-effectiveness/provenance views.

Remaining:

1. individual job analysis/report view with clear source/English/model provenance;
2. operation result links to newly fetched/transformed/analyzed jobs;
3. combined current-corpus report;
4. bounded ready-job analysis queue;
5. final `jobhunter run` orchestration;
6. equivalent browser action using the same services;
7. summary of source/translation/analysis failures without hiding partial successes;
8. deterministic and live end-to-end Phase-1 acceptance.

Final Phase-1 run should conceptually perform:

```text
bounded discovery
→ detail acquisition/refresh
→ parser audit
→ current v2 English repair/build
→ select new/changed analysis-ready jobs
→ bounded P1.6 analysis
→ update aggregate market view/report
```

Each expensive/model step remains independently bounded and inspectable.

## 7. Cross-cutting Phase-1 product work

These are implemented alongside the increments above, not as separate architecture projects.

### Browser/UX

- normal daily interface remains the local browser app;
- CLI remains automation/debug/advanced interface;
- pagination as corpus size grows beyond practical single-table rendering;
- bulk actions with explicit bounds;
- clear badges for source complete / English current / analysis current / needs review;
- operation completion links;
- LM Studio connection/model visibility;
- understandable lifecycle and translation-integrity states.

### Search effectiveness

Measure, do not auto-prune:

- distinct postings found;
- unique contributions;
- overlap;
- participating runs;
- discovery provenance per job.

Later JobHunter may suggest catalog changes, but a human must approve vocabulary changes.

### Quality

- normal tests never contact Jobinja, Google or LM Studio;
- version prompts/schemas/provider contracts;
- migration tests for every durable schema change;
- retain exact source/model provenance;
- do not call a structural parser audit a semantic-quality certification.

## 8. Phase 2 — canonical market intelligence

Start only after Phase 1 produces a reviewed body of accepted semantic analyses.

### P2.1 Canonical concept registry

Create reviewed canonical concepts for:

```text
tools
skills
knowledge areas
practices
domains
experience signals
education signals
```

Do not silently collapse aliases by model guess.

### P2.2 Alias/synonym mapping

Examples such as:

```text
Postgres ↔ PostgreSQL
K8s ↔ Kubernetes
LLM ↔ Large Language Model
```

require reviewable mappings and provenance.

### P2.3 Responsibility families

Group recurring responsibilities into stable reviewed families while retaining original
job-level claims/evidence.

### P2.4 Role archetypes

Build evidence-backed role archetypes from the analyzed corpus, not from generic occupational
knowledge alone.

### P2.5 Market matrices

Produce:

- concept demand by role/archetype;
- required/preferred/contextual distributions;
- responsibility-family prevalence;
- co-occurrence matrices;
- technology/domain combinations;
- seniority/depth signals where evidence supports them.

Every aggregate states sample size and provenance.

### P2.6 Market segmentation

Allow views by available source dimensions such as category/location/employment/experience,
plus reviewed role archetypes.

### P2.7 Phase-2 quality gate

- canonical mappings reviewed;
- aggregate counts reproducible from accepted analysis artifacts;
- no double-counting caused by aliases;
- sample size visible;
- job-level drill-down remains possible.

## 9. Phase 3 — personal capability evidence and gap intelligence

Start only after the market concept model is stable enough to compare against.

### P3.1 Personal evidence schema

Define explicit evidence records rather than treating conversation memory as proof.

Potential evidence classes:

```text
work experience
projects
source-code evidence
learning/practice evidence
assessments
demonstrated tools/technologies
reviewed self-report
```

### P3.2 Capability depth model

Represent depth explicitly, for example:

```text
introduced
practiced
working
independent
advanced
```

Exact labels must be finalized from real use; do not mark a concept simply complete/not
complete.

### P3.3 Capability evidence/provenance

Every personal capability claim records:

- concept;
- depth;
- evidence source;
- date/freshness;
- confidence/review state.

### P3.4 Market-to-person mapping

Map personal canonical capabilities to Phase-2 market concepts through reviewed identity/
alias relations.

### P3.5 Gap classes

Distinguish, at minimum:

```text
no evidence
introduced but shallow
practical depth gap
missing production evidence
outdated evidence
strong/adequate evidence
```

### P3.6 Personal comparison UI

Show the evidence behind every claimed strength/gap and allow correction.

### P3.7 Phase-3 quality gate

- no personal claim without evidence;
- depth preserved;
- no automatic optimism/pessimism;
- gap conclusions trace to both market evidence and personal evidence.

## 10. Phase 4 — explainable career decisions and application readiness

Start only after Phase 3 has reviewed capability evidence.

### P4.1 Opportunity relevance

Rank/filter jobs using explainable market + personal evidence, separate from acquisition
priority.

### P4.2 Fit/readiness explanation

Avoid opaque percentage scores unless a defensible calibrated method exists. Prefer explicit
breakdowns such as:

- strong evidence matches;
- partial matches;
- missing critical requirements;
- preferred-only gaps;
- uncertainty.

### P4.3 Learning priorities

Prioritize gaps by:

- market demand;
- required/preferred strength;
- dependency structure;
- current personal depth;
- evidence cost/time where known.

### P4.4 Application priorities

Surface jobs worth considering now versus after specific evidence-building work.

### P4.5 Role/path comparison

Compare role families and career directions using actual collected market evidence and
personal evidence.

### P4.6 Application-readiness artifacts

Only after the evidence model supports them, add bounded assistance such as tailored
application checklists or source-grounded resume targeting. Do not automate applications.

### P4.7 Phase-4 quality gate

Every recommendation must explain:

```text
what evidence supports it
what evidence contradicts it
what is uncertain
what action follows
```

## 11. Phase 5 — sustained local product

### P5.1 Historical market trends

Track changes in demand, requirements, archetypes and source lifecycle over time without
mixing old/new analysis contracts silently.

### P5.2 Scheduled operation

Add explicit local scheduling only after the final Phase-1 run is stable and idempotent.

### P5.3 Notifications

Notify only about meaningful completed/failed runs, new high-priority evidence, or configured
conditions. Avoid noisy per-request notifications.

### P5.4 Backup/restore

Provide tested backup and restore for:

- SQLite database;
- evidence files;
- local configuration excluding secrets where appropriate;
- exports/reviewed personal evidence.

### P5.5 Durable migrations

Version and test schema migrations; old supported databases must upgrade without manual SQL.

### P5.6 Retention/storage management

Define evidence retention and optional cleanup only after real storage growth is measured.
Never delete authoritative evidence silently.

### P5.7 Model/prompt regression quality

Maintain reviewed test corpora for translation and semantic analysis so model/prompt upgrades
can be compared rather than guessed.

### P5.8 Performance

Optimize only measured bottlenecks: queries, pagination, inference batching, evidence I/O,
startup and large-corpus views.

### P5.9 Observability and recovery UX

Expose operation health, last successful run, failure classes, retryability, migration state,
and recovery instructions in the app.

### P5.10 Sustained-operation acceptance

Prove repeated operation over time without duplicate logical jobs, silent stale artifacts,
destructive lifecycle guesses, or unrecoverable local state.

## 12. Explicitly deferred unless evidence justifies them

Do not add these merely because they are common application features:

- unrestricted web crawling;
- automated login/CAPTCHA bypass;
- automatic job applications;
- cloud deployment/accounts/authentication;
- mobile/native-app rewrite;
- React/Node rewrite while server-rendered Python is sufficient;
- vector database before a measured retrieval requirement exists;
- embeddings for the entire corpus without a concrete use case;
- salary prediction without adequate data quality/sample size;
- opaque career-fit percentages;
- personal capability assumptions from chat memory alone.

## 13. Definition of done for every increment

An increment is accepted only when:

1. intended workflow works locally;
2. durable schema migrations are safe where relevant;
3. deterministic tests pass;
4. `ruff check .` passes;
5. `pytest -W error` passes;
6. live acceptance passes when network/model behavior matters;
7. failures are inspectable and bounded;
8. provenance is retained;
9. browser/CLI behavior stays consistent where both expose the feature;
10. documentation matches actual behavior;
11. no unrelated future capability is claimed.

## 14. Current exact execution order

Do not add more features until this sequence completes:

```text
1. Confirm/fix legacy DB migration ordering
2. Exclude parser metadata from P1.6 employer evidence
3. Resolve remaining Ruff findings
4. Run full Ruff
5. Run full pytest
6. Run pytest -W error and fix residual root causes
7. Open/migrate the real database only after deterministic green
8. Repair/inspect previously corrupted v1 translations into v2
9. Repair the wider parsed corpus in bounded batches
10. Run one real P1.6 analysis and manually inspect evidence
11. Expand to a small reviewed analysis batch
12. Inspect/validate the Market page
13. Finish remaining P1.3/P1.5 acceptance
14. Finish P1.7 final run/reporting
15. Only then begin Phase 2
```

## 15. Current non-claims

Until the current stabilization/live gates pass, JobHunter must not claim:

- translation-v2 quality across the full corpus;
- complete source lifecycle/repost resolution;
- production-quality semantic extraction across all role types;
- canonical market taxonomy;
- full-market conclusions from a small analyzed sample;
- personal capability gaps, readiness scores, or career recommendations;
- arbitrary-web Quick Add ingestion;
- final Phase-1 end-to-end reporting automation.
