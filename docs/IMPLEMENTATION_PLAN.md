# JobHunter Master Implementation Plan

## 1. Purpose and authority

This is the controlling product-level **implementation plan** for JobHunter. It defines exact delivery order, dependencies, acceptance gates, and what completion means from the current foundation through the sustained local product.

It is not a learning roadmap and it does not pre-decide low-level architecture that should be chosen only after later evidence exists.

The strategic sequencing and proposal-disposition view lives in [JobHunter Roadmap](ROADMAP.md). The working checklist lives in [JobHunter Execution TODO](EXECUTION_TODO.md). Neither document may bypass the acceptance order defined here.

Detailed Phase-1 source/analysis execution remains subordinate to [Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

Authority order:

```text
product/specification/domain/source/architecture documents
        ↓
ROADMAP.md
strategic sequencing / proposal disposition
        ↓
this master implementation plan
exact delivery order / acceptance gates
        ↓
phase-specific execution plans
        ↓
EXECUTION_TODO.md
working checklist only
        ↓
implementation / tests / live acceptance
```

If a subordinate plan/checklist becomes stale, this document controls until the subordinate artifact is reconciled.

## 2. Delivery rules

- Build operable vertical slices rather than disconnected framework work.
- Keep acquisition usable when LM Studio is unavailable.
- Preserve raw evidence before parsing, translation, or analysis.
- Keep source, translation, model analysis, market aggregation, and personal/user state separate.
- Prefer local-first providers when they satisfy the requirement.
- Keep search coverage data-driven and acquisition bounded.
- Retry only failure classes explicitly marked retryable.
- Never equate provider/source failure with a legitimate empty result.
- Never let transient network/5xx/rate-limit/challenge failures become destructive lifecycle conclusions.
- Require deterministic tests before live acceptance.
- Require reviewed live examples before trusting model-derived layers at scale.
- Use representative review samples rather than only convenient/adjacent records when model quality is being accepted.
- Keep browser and CLI on the same application services/database.
- Add UI/product complexity only where repeated operation benefits.
- Preserve historical artifacts rather than silently rewriting them when contracts change.
- Never promote a derived representation above authoritative employer/source evidence.
- Do not infer personal capability or readiness without explicit reviewed personal evidence.
- Preserve partial success explicitly; successful durable work must not disappear merely because a later stage fails.
- Important real failure classes become offline regression fixtures.

## 3. Product stages

| Stage | Outcome | Status |
|---|---|---|
| M0 | Runnable local foundation, SQLite, LM Studio boundary, tests | Accepted |
| Phase 1 | Complete Jobinja workflow through evidence-backed analysis/reporting | Active |
| Phase 2 | Canonical market intelligence and role/capability taxonomy | Planned |
| Phase 3 | Personal capability evidence and gap intelligence | Planned |
| Phase 4 | Explainable decision/action and application-readiness layer | Planned |
| Phase 5 | Sustained operation, trends, recovery, quality and maintenance | Planned |

Additional future product programs such as multi-source expansion, a fuller application/interview workspace, advanced retrieval/RAG, model lab and specialist AI workers remain governed by `ROADMAP.md` and require explicit promotion before they become implementation scope.

## 4. Previously accepted foundation

Before the current hardening/analysis increment, live evidence established:

- repeat-safe Jobinja discovery and identical-rerun idempotency;
- a browser sync with 40/40 search requests, 273 unique postings, 241 new postings, 32 already-known postings, and zero search failures;
- bounded detail acquisition with 10/10 selected detail pages succeeding;
- 26/26 current parsed jobs structurally clean under parser-v2 audit at that point;
- immutable raw evidence, semantic versions, and fetch observations remaining distinct;
- data-driven Persian/English search profiles and packs;
- local LM Studio translation, artifact reuse, and bounded output-truncation recovery;
- 15/15 English artifacts under translation v1 before a real field-association defect was discovered on later translations;
- local browser application, guided sync controls, Quick Add, concise operation summaries, and missing-detail backlog acquisition working against the real corpus.

Translation v1 remains historical because field-to-translation association corruption was observed in real data.

## 5. Current stabilization gate — do this before more features

The current large implementation is not accepted until this sequence is green in order.

### S0.1 Database migration compatibility

Purpose: older JobHunter SQLite files must upgrade cleanly before newer translation/analysis repositories query modern columns or tables.

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

Fix actual residual failures one root cause at a time. Do not interpret cascaded database failures as independent defects until migration/initialization failures are removed.

Current/near-term deterministic regression expectations also include:

- source/provider failure cannot become a legitimate empty-result success;
- transient 5xx/network/rate-limit/challenge errors cannot become expiry/removal;
- unsupported semantic-analysis evidence is rejected;
- parser metadata cannot become employer evidence;
- acquired prompt-injection-like text remains inert data;
- Unicode/non-Latin normalization does not collapse distinct identities;
- mixed-success workflows report partial failure accurately.

### S0.4 Real-corpus migration gate

Only after the deterministic suite is green:

1. back up the current local workspace;
2. open the existing real database through the new code;
3. confirm migration is non-destructive;
4. confirm old v1 translation artifacts still exist historically;
5. confirm they no longer count as current v2 artifacts;
6. repair one previously corrupted job to v2;
7. inspect it manually;
8. repair a second previously corrupted job with materially different content/structure;
9. inspect it manually;
10. repair the remaining current parsed corpus in bounded batches;
11. export only current v2 English artifacts.

### S0.5 First semantic-analysis acceptance

1. choose one reviewed current v2 job with clear responsibilities and mixed requirement strengths where possible;
2. run P1.6 analysis;
3. inspect every role-purpose/responsibility/requirement claim;
4. verify its evidence is an exact excerpt of employer text;
5. verify required/preferred/contextual/inferred strength is preserved;
6. verify unsupported concepts were omitted or rejected;
7. rerun and confirm artifact reuse;
8. select a **small representative** follow-up batch, default around 5, intentionally varying company/title/role pattern/language/description length/requirement density where the available corpus permits;
9. include at least some ordinary/random examples rather than reviewing only known edge cases;
10. record semantic error classes and convert repeatable failures into regression fixtures;
11. inspect the Market page only after that reviewed sample is acceptable;
12. verify Market states exact sample scope and warns when the analyzed subset is too small/concentrated for broad conclusions.

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
- add representative fixtures and live examples where safely reproducible;
- treat `provider/source failure` and `no jobs/results` as different outcomes;
- ensure 500/502/503/504 and transient network errors never become `expired`/`removed`.

Definition of done:

- deterministic classification/retry tests green;
- real normal/expired/error examples inspected;
- acquisition remains independent from LM Studio;
- failure-vs-empty semantics are explicit.

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
- add a reviewed Persian→English golden corpus before choosing a permanent translation model based on quality claims.

### P1.5 Identity, lifecycle, user triage and acquisition priority

Status: semantic versions/observations accepted; lifecycle/triage/priority implementation pending acceptance.

Lifecycle rules:

- normal successful detail -> active;
- explicit source expiry -> expired;
- first 404/410 -> possibly_unavailable;
- repeated 404/410 evidence may transition -> removed;
- rate limit/access/challenge/server/network failure must not become destructive lifecycle conclusions.

User workflow state remains separate from source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Priority selection may use discovery/search/title evidence to decide which missing details to fetch first. It must not be presented as personal fit or market importance.

Remaining P1.5 work:

- last-successful-check and consecutive-failure summaries;
- stronger lifecycle UI;
- representative failure/lifecycle fixture/live acceptance;
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
- uncertain claims should be omitted rather than guessed;
- critical integrity rules are enforced by application validation/tests, not by prompt wording alone;
- acquired text is untrusted data even if it contains instruction-like strings.

After first live acceptance, add a review/correction workflow only if real analysis quality shows that human correction is needed often enough to justify it.

### P1.7 Individual outputs, aggregate market view and complete Phase-1 run

Status: partial implementation.

Already implemented:

- per-job analysis surface;
- first Market aggregation over accepted current analysis artifacts;
- search-effectiveness/provenance views;
- bounded browser workflow actions supporting the newer analysis path.

Remaining:

1. individual job analysis/report view with clear source/English/model provenance;
2. operation result links to newly fetched/transformed/analyzed jobs;
3. combined current-corpus report;
4. bounded ready-job analysis queue;
5. final `jobhunter run` orchestration;
6. equivalent browser action using the same services;
7. summary of source/translation/analysis failures without hiding partial successes;
8. explicit requested/attempted/completed/reused/skipped/failed/remaining result semantics for multi-stage work;
9. Market sample/concentration warnings sufficient to prevent broad claims from a small analyzed subset;
10. deterministic and live end-to-end Phase-1 acceptance.

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

Each expensive/model step remains independently bounded and inspectable. A later-stage failure must not roll back valid durable work from earlier stages merely to create an appearance of atomic success.

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
- understandable lifecycle and translation-integrity states;
- operation summaries must preserve partial-success semantics.

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
- do not call a structural parser audit a semantic-quality certification;
- add regression fixtures for important real incidents;
- use fault/model-chaos fixtures at network/model durability boundaries;
- use representative reviewed samples for model quality promotion decisions.

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

Group recurring responsibilities into stable reviewed families while retaining original job-level claims/evidence.

### P2.4 Role archetypes

Build evidence-backed role archetypes from the analyzed corpus, not from generic occupational knowledge alone.

### P2.5 Market matrices

Produce:

- concept demand by role/archetype;
- required/preferred/contextual distributions;
- responsibility-family prevalence;
- co-occurrence matrices;
- technology/domain combinations;
- seniority/depth signals where evidence supports them;
- posting-frequency and distinct-employer views where useful.

Every aggregate states sample size, source/filter scope and provenance. Duplicate-adjusted views remain unavailable until duplicate/repost identity is sufficiently reliable.

### P2.6 Market segmentation

Allow views by available source dimensions such as category/location/employment/experience, plus reviewed role archetypes.

### P2.7 Phase-2 quality gate

- canonical mappings reviewed;
- aggregate counts reproducible from accepted analysis artifacts;
- no double-counting caused by aliases;
- sample/source/filter scope visible;
- job-level drill-down remains possible;
- role/archetype definitions have reviewed representative examples.

Multi-source acquisition may begin after Phase-1 acceptance under the roadmap, but a generic source-adapter abstraction must be extracted from Jobinja plus at least one real second source rather than designed from imagination.

## 9. Phase 3 — personal capability evidence and gap intelligence

Start only after the market concept model is stable enough to compare against.

Before storing irreplaceable personal evidence, define explicit public/system/personal/secret data boundaries and provide tested backup/restore for the personal evidence domain.

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

Repository facts may generate evidence candidates later, but dependency names or AI-generated code do not automatically establish capability.

### P3.2 Capability depth model

Represent depth explicitly. The current domain proposal uses an ordinal model from unassessed/awareness through guided/independent/integrated/repeated evidence and production/production-like operation.

Exact UI labels may be refined from real use; do not mark a concept simply complete/not complete.

### P3.3 Capability evidence/provenance

Every personal capability claim records:

- concept;
- depth;
- evidence source/reference;
- date/freshness;
- confidence/review state;
- limitations/context;
- AI-assistance/independence context where relevant.

### P3.4 Market-to-person mapping

Map personal canonical capabilities to Phase-2 market concepts through reviewed exact/broader/narrower/partial relations.

### P3.5 Gap classes

Distinguish, at minimum:

```text
unknown evidence
knowledge gap
practice gap
depth gap
integration gap
missing production evidence
outdated evidence
presentation/evidence gap
experience-context gap
constraint mismatch
strong/adequate evidence
```

Unknown is not automatically a negative capability claim.

### P3.6 Personal comparison UI

Show the evidence behind every claimed strength/gap and allow correction.

### P3.7 Phase-3 quality gate

- no personal claim without evidence;
- depth/confidence/recency preserved;
- AI-assistance/independence context representable;
- no automatic optimism/pessimism;
- gap conclusions trace to both market evidence and personal evidence;
- backup/restore of personal evidence is proven.

## 10. Phase 4 — explainable career decisions and application readiness

Start only after Phase 3 has reviewed capability evidence.

### P4.1 Opportunity relevance

Rank/filter jobs using explainable market + personal evidence, separate from acquisition priority.

### P4.2 Fit/readiness explanation

Avoid opaque percentage scores unless a defensible calibrated method exists. Prefer explicit requirement-by-requirement/categorical breakdowns such as:

- strong evidence matches;
- partial matches;
- missing critical requirements;
- preferred-only gaps;
- unknown requirements;
- constraints;
- uncertainty.

### P4.3 Learning priorities

Prioritize gaps by:

- market demand;
- required/preferred strength;
- dependency structure;
- current personal depth;
- evidence-building value/cost where known;
- explicit target-role/scenario constraints.

Actions may include learn, practise, integrate, build evidence, document, assess, monitor or ignore for now.

### P4.4 Application priorities

Surface jobs worth considering now versus after specific evidence-building work.

### P4.5 Role/path comparison

Compare role families and career directions using actual collected market evidence and personal evidence.

### P4.6 Application-readiness artifacts

Only after the evidence model supports them, add bounded assistance such as Application Evidence Packs, tailored application checklists or evidence-constrained resume targeting. Do not automate applications.

### P4.7 Phase-4 quality gate

Every recommendation must explain:

```text
what evidence supports it
what evidence contradicts it
what is uncertain
what policy/constraint was applied
what action follows
what would change the conclusion
```

## 11. Phase 5 — sustained local product

### P5.1 Historical market trends

Track changes in demand, requirements, archetypes and source lifecycle over time without mixing old/new analysis contracts silently.

Trend claims require like-for-like snapshot scope, duplicate/lifecycle quality and visible sample size.

### P5.2 Scheduled operation

Add explicit local scheduling only after the final Phase-1 run is stable, idempotent and bounded.

### P5.3 Notifications

Notify only about meaningful completed/failed runs, new high-priority evidence, or configured conditions. Avoid noisy per-request notifications.

### P5.4 Backup/restore

Provide tested backup and restore for:

- SQLite database;
- evidence files;
- local configuration excluding secrets where appropriate;
- exports/reviewed personal evidence.

### P5.5 Durable migrations

Version and test schema migrations; old supported databases must upgrade without manual SQL.

### P5.6 Retention/storage management

Define evidence retention and optional cleanup only after real storage growth is measured. Never delete authoritative evidence silently.

### P5.7 Model/prompt regression quality

Maintain reviewed test corpora for translation and semantic analysis so model/prompt upgrades can be compared rather than guessed.

### P5.8 Performance

Optimize only measured bottlenecks: queries, pagination, inference batching, evidence I/O, startup and large-corpus views.

### P5.9 Observability and recovery UX

Expose operation health, last successful run, failure classes, retryability, migration state, current/stale derived-artifact reasons, and recovery instructions in the app.

### P5.10 Sustained-operation acceptance

Prove repeated operation over time without duplicate logical jobs, silent stale artifacts, destructive lifecycle guesses, unreported partial failures, or unrecoverable local state.

Advanced query/RAG/model-lab/provider-routing work remains trigger-based under the roadmap rather than an automatic Phase-5 requirement.

## 12. Explicitly deferred unless evidence justifies them

Do not add these merely because they are common application features or technically attractive:

- unrestricted web crawling;
- automated login/CAPTCHA bypass;
- automatic job applications or recruiter messaging;
- cloud deployment/accounts/authentication;
- mobile/native-app rewrite;
- React/Node rewrite while server-rendered Python is sufficient;
- graph database while relational traversal is sufficient;
- vector database before a measured retrieval requirement exists;
- embeddings for the entire corpus without a concrete evaluated use case;
- generic plugin framework before multiple concrete extensions require it;
- autonomous agent swarm;
- salary/hiring-probability prediction without adequate data quality/sample size;
- opaque career-fit percentages;
- personal capability assumptions from chat memory alone;
- repository dependency names treated as proficiency;
- self-training on unverified model generations.

## 13. Definition of done for every increment

An increment is accepted only when:

1. intended workflow works locally;
2. durable schema migrations are safe where relevant;
3. deterministic tests pass;
4. `ruff check .` passes;
5. `pytest -W error` passes;
6. live acceptance passes when network/model behavior matters;
7. failures are inspectable and bounded;
8. partial success is represented honestly where relevant;
9. provenance is retained;
10. browser/CLI behavior stays consistent where both expose the feature;
11. documentation matches actual behavior;
12. no unrelated future capability is claimed.

## 14. Current exact execution order

Do not add more features until this sequence completes:

```text
1. Confirm/fix legacy DB migration ordering
2. Confirm P1.6 employer-evidence boundary excludes parser metadata
3. Resolve remaining Ruff findings
4. Run full Ruff
5. Run full pytest
6. Run pytest -W error and fix residual root causes
7. Open/migrate the real database only after deterministic green
8. Repair/inspect previously corrupted v1 translations into v2
9. Repair the wider parsed corpus in bounded batches
10. Run one real P1.6 analysis and manually inspect every claim/evidence link
11. Expand to a small representative reviewed analysis batch
12. Convert repeatable source/model/semantic failure classes into regression/chaos fixtures
13. Inspect/validate the Market page including sample/concentration warning semantics
14. Harden source failure/lifecycle acceptance, especially transient 5xx/network != expiry
15. Make multi-stage operation result/partial-success semantics explicit
16. Finish remaining P1.3/P1.5 acceptance
17. Finish P1.7 final run/reporting/browser equivalent
18. Reconcile accepted-state documentation and close Phase 1
19. Only then begin Phase 2
```

The detailed working checklist for these steps is `docs/EXECUTION_TODO.md`.

## 15. Current non-claims

Until the current stabilization/live gates pass, JobHunter must not claim:

- translation-v2 quality across the full/future corpus;
- complete source lifecycle/repost resolution;
- production-quality semantic extraction across all role types;
- canonical market taxonomy;
- full-market conclusions from a small/source-biased analyzed sample;
- reviewed personal capability gaps/readiness/career recommendations;
- evidence-backed application/resume/interview readiness;
- arbitrary-web Quick Add ingestion;
- generic source-plugin support;
- final Phase-1 end-to-end reporting automation.
