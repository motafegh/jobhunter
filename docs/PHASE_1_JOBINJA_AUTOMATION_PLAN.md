# Phase 1 — Jobinja Workflow Automation Plan

## 1. Status and authority

**Status:** Active implementation plan  
**Scope:** Phase 1  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless isolation is clearly required.

This document is subordinate to:

1. product/domain/source/architecture constraints;
2. [JobHunter Roadmap](ROADMAP.md) for strategic sequencing;
3. [JobHunter Master Implementation Plan](IMPLEMENTATION_PLAN.md) for exact product-level delivery order.

[JobHunter Execution TODO](EXECUTION_TODO.md) is the working checklist for this plan and cannot override it.

This document controls detailed Phase-1 order, records, boundaries and acceptance.

## 2. Objective

Replace the former manual workflow:

```text
manual keyword search
→ open advertisements
→ copy text into files
→ send files to an AI assistant
→ request individual/combined analysis
```

with:

```text
configured bilingual search coverage
→ repeat-safe bounded acquisition
→ immutable evidence
→ deterministic structured source data
→ semantic version/check history
→ hardened local English projection
→ evidence-backed local semantic analysis
→ inspectable individual/aggregate results
```

The browser application is the normal human interface; CLI remains supported for advanced operation/debugging/automation.

## 3. Final intended Phase-1 run

A complete Phase-1 run will:

1. load configured bilingual search coverage;
2. construct a bounded request plan;
3. acquire search pages and preserve evidence;
4. discover stable Jobinja identities repeat-safely;
5. select priority missing and refresh-due details;
6. acquire/classify detail responses and preserve valid source evidence;
7. parse source-explicit fields deterministically;
8. classify semantic content as new/unchanged/changed;
9. retain source-check/lifecycle evidence;
10. create/reuse current hardened English v2 projection;
11. select analysis-ready new/changed current versions;
12. run bounded evidence-backed local semantic analysis;
13. validate every material claim against original employer text;
14. persist derived artifacts/attempts/review state;
15. update individual and aggregate Market outputs;
16. expose the workflow through browser UI and CLI;
17. report requested/attempted/completed/reused/skipped/failed/remaining work without hiding partial failure.

Manual copying of individual jobs should not be required.

## 4. Current dependency flow

```text
bilingual TOML search catalog
        ↓
bounded search plan
        ↓
Jobinja search acquisition
        ↓
raw search evidence
        ↓
logical JobPosting + discovery provenance
        ↓
priority missing / refresh-due selection
        ↓
detail response classification
        ↓
raw valid detail evidence
        ↓
Jobinja parser v2
        ↓
semantic source version
        ↓
fetch observation + lifecycle evidence
        ↓
structural parser audit
        ↓
current English projection v2
  ├─ source identity for native English
  └─ local LM Studio translation
        ↓
translation integrity gate
        ↓
current English artifact
        ↓
evidence-backed P1.6 analysis
        ↓
original-source evidence validation
        ↓
validated analysis artifact
        ↓
per-job analysis + Market aggregation
```

Google Cloud Translation remains an optional external alternative, not a normal dependency.

## 5. Source/search boundary

Search vocabulary lives in versioned TOML data and supports profiles, packs, Persian and English terms, custom groups, exclusions, raw Jobinja URL escape hatches, deterministic search windows, page limits, request delays and global request budgets.

Search vocabulary is acquisition configuration, not a career taxonomy and not proof of personal relevance.

Use approved public Jobinja pages only. Preserve canonical URL attribution, validate hosts and redirects, bound request/response volume, and keep requests sequential/rate-limited.

Do not automate login/applications, scrape private profiles, bypass CAPTCHA/access controls, rotate identities/proxies to defeat limits, or create unrestricted crawling.

Critical failure distinction:

```text
source/provider failure
!=
valid search with zero results
```

## 6. Durable record boundaries

Never conflate:

```text
JobPosting                    stable logical Jobinja identity
SearchPageSnapshot            exact search response evidence
JobPostingVersion             meaningful employer-content history
JobDetailFetchObservation     operational source check
JobLifecycleEvent/state       classified lifecycle evidence
JobTranslationArtifact        derived English view of one source version
JobTranslationAttempt         operational translation history
JobAnalysisArtifact           model-derived evidence-backed interpretation
JobAnalysisAttempt            operational semantic-analysis history
JobUserWorkflow               local human triage state
Browser WebOperation          ephemeral UI execution state
```

Source evidence remains authoritative over translation and model-derived records.

## 7. Parser boundary

Parser v2 extracts explicit Jobinja fields and complete source text before translation or semantic analysis. Missing fields remain missing.

Jobinja source skill tags remain distinct from future description-derived semantic concepts.

Parser metadata such as `language` and `parser_version` is not employer evidence.

A clean parser audit certifies known structural/parser checks only. It does not certify translation quality or semantic-analysis quality.

## 8. Translation v2 boundary

Translation v1 is historical because real field-to-translation association corruption was observed.

Current contracts:

```text
provider: lm-studio-translation-v2
projection: english-projection-v2
```

V2 rules:

- preserve v1 artifacts historically;
- current/exportable English must use the current v2 projection schema;
- use content-derived translation identities;
- translate one semantic source segment per LM Studio request for the current hardened path;
- reject malformed/missing/extra output;
- run deterministic source/English integrity checks before persistence;
- reject suspicious scalar expansion/shape/date corruption;
- never shorten employer source text to satisfy batching;
- native-English jobs use source-identity artifacts without model calls;
- translation failure never changes source evidence/history.

Model-selection priority:

```text
translation_lm_studio_model
→ lm_studio_model
→ exactly-one-visible-model auto-selection
```

Output truncation recovery remains bounded up to the configured hard token cap.

A reviewed Persian/mixed-language golden set should be introduced when permanent translation model/contract quality is being compared, not merely because one fluent output looks good.

## 9. Source response classification and lifecycle

Implemented/current classes include:

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

Retry policy:

- transient network failure: bounded retry;
- 429: bounded retry/backoff;
- selected 5xx: bounded retry/backoff;
- challenge/auth/access/not-found/gone: no blind automatic hammering.

Lifecycle policy:

- successful normal detail -> active;
- explicit source expiry -> expired;
- first 404/410 -> possibly_unavailable;
- repeated 404/410 evidence may -> removed;
- rate limit/access/challenge/server/network errors do not become destructive lifecycle conclusions.

Required regression invariants:

```text
500/502/503/504 != expired/removed
network failure   != expired/removed
rate limit        != expired/removed
challenge/auth    != vacancy gone
source exception  != valid empty result
```

Remaining lifecycle acceptance work includes real/fixture coverage, last-successful-check summary, consecutive-failure summary, stronger lifecycle UI and later repost/near-duplicate handling.

## 10. User triage and priority

User state is local derived workflow metadata, not employer/source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Jobs marked not relevant remain preserved historically.

Missing-detail priority may use search/discovery/title signals to decide fetch order, but it must never be described as personal fit/readiness or market importance.

## 11. P1.6 semantic-analysis boundary

P1.6 is implemented but not live-accepted yet.

Artifact identity includes:

```text
source detail version
+ current hardened English artifact
+ exact LM Studio model
+ prompt version
+ analysis schema version
```

The current schema supports:

- role purpose;
- responsibilities;
- requirements;
- required / preferred / contextual / inferred distinction;
- concept type;
- confidence;
- exact original-source evidence excerpt;
- rationale for inferred concepts.

Rules:

- original employer/job fields are authoritative;
- English v2 is comprehension aid only;
- parser metadata (`language`, `parser_version`) is excluded from employer evidence;
- every material claim must cite an excerpt located in authoritative source fields;
- hallucinated/unsupported evidence rejects the artifact;
- source-explicit requirement strength must not be inflated;
- inferred concepts require rationale plus source evidence;
- model request/response is retained for auditability;
- prompt/schema/model changes create distinct artifacts;
- acquired job text remains untrusted data even when it contains instruction-like strings;
- critical invariants must be enforced by application validation/tests rather than prompt wording alone.

### Model-chaos / untrusted-content acceptance

Deterministic tests should cover at least:

- valid JSON with fabricated evidence -> reject;
- parser metadata used as evidence -> reject;
- inferred concept without rationale -> reject;
- malformed/extra structured fields -> reject;
- truncated/invalid structured output -> no partial artifact;
- prompt-injection-like strings in employer text -> inert data;
- source content instructing the model to mark a candidate qualified -> no personal/readiness state is created.

## 12. Search effectiveness and first Market aggregation

Search Plan may report:

- distinct jobs found per search;
- discovery events/runs;
- unique contributions;
- overlap/provenance.

Do not auto-prune high-overlap vocabulary.

Market currently aggregates accepted current analysis artifacts and keeps requirement strength separate. It is not yet Phase-2 canonical taxonomy; aliases such as Postgres/PostgreSQL must not be silently merged without reviewed canonicalization.

Before Phase-1 Market acceptance:

- exact analyzed-current sample size must be visible;
- filtered/source scope must remain recoverable;
- broad market conclusions from tiny/concentrated samples must produce explicit warnings;
- requirement prevalence counts must be by posting when the metric claims job demand, not duplicate claim count;
- `analyzed count` must not be presented as semantic-quality certification.

A compact corpus-health summary may show distinct layer coverage such as discovered/detail/parsed/current-English/current-analysis, but coverage and quality remain separate concepts.

## 13. Browser application boundary

Current/implemented browser surfaces include:

```text
Overview
Jobs
Job detail
Search plan / search effectiveness
Market
Operations
System
```

Normal workflow:

```text
run bounded sync
→ fetch priority missing details
→ repair/build current English v2
→ analyze a small ready batch
→ inspect per-job analysis
→ inspect Market aggregate
```

Jobs UI supports filtering/triage and bounded bulk actions. Browser actions must use the same core services and bounds as CLI paths.

The UI remains loopback-first, CSRF-protected, locally packaged, and limited to one mutable browser operation at a time unless later concurrency is explicitly proven safe.

### Operation result semantics

For multi-stage work, normal user-facing summaries should distinguish where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

Do not display a generic success state when meaningful sub-work failed. Valid durable work from earlier stages remains preserved if a later stage fails.

## 14. Delivery state

| Increment | State |
|---|---|
| P1.0 repository alignment | Accepted |
| P1.1 discovery foundation | Accepted |
| P1.2 bounded repeat-safe discovery | Accepted |
| P1.3 detail acquisition | Operational core accepted; classification/retry pending acceptance |
| P1.4 parser | Accepted foundation |
| P1.4 translation v2 | Implemented; migration/live acceptance pending |
| P1.5 semantic versions/observations | Accepted foundation |
| P1.5 lifecycle/triage/priority | Implemented; acceptance pending |
| Local browser app | Operating live; newer intelligence/workflow surfaces pending acceptance |
| P1.6 evidence-backed analysis | Implemented; deterministic/live acceptance pending |
| P1.7 individual/aggregate outputs | Partial; Market/per-job surfaces implemented |

## 15. Accepted live evidence so far

Previously established:

- initial repeat-safe corpus of 79 unique jobs;
- identical rerun creating zero new logical jobs;
- later browser sync: 40/40 search requests, 273 unique postings, 241 new, 32 known, zero search failures;
- 10/10 selected details fetched successfully in that run;
- 26/26 current parsed jobs structurally clean at that point;
- semantic versions protected from volatile raw HTML;
- fetch observations and refresh-due selection;
- local LM Studio translation and idempotent reuse;
- bounded recovery from a real translation output truncation;
- browser app/Quick Add/guided sync/missing-detail backlog functioning.

Historical translation-v1 success is not sufficient to certify current English quality because later real field-association corruption was discovered.

## 16. Current exact acceptance sequence

Do not add new Phase-1 features until this sequence completes:

1. confirm/fix legacy DB migration ordering;
2. confirm parser metadata is excluded from P1.6 employer evidence;
3. resolve Ruff findings;
4. run full Ruff;
5. run full pytest;
6. run `pytest -W error` and fix residual root causes;
7. back up and open/migrate the real database only after deterministic green;
8. repair one previously corrupted v1 translation to v2 and inspect it;
9. repair a second affected/different job and inspect it;
10. repair the wider parsed corpus in bounded batches;
11. run one real P1.6 analysis and inspect every source evidence excerpt/strength classification;
12. rerun that job and confirm reuse;
13. select a small **representative** review batch, default around 5, varying available company/title/role/language/length/requirement-density dimensions;
14. analyze and review that batch, recording semantic/model failure classes;
15. convert repeatable source/model/semantic failure classes into regression/chaos fixtures;
16. inspect the Market page and validate sample/concentration warning semantics;
17. finish source-response/lifecycle acceptance, especially transient 5xx/network != expiry;
18. make partial-success operation result semantics explicit;
19. accept/revise P1.6 before scaling analysis;
20. finish remaining P1.3/P1.5 acceptance;
21. finish P1.7 final run/report/browser equivalent;
22. reconcile accepted-state documentation and close Phase 1.

## 17. Remaining Phase-1 work after current semantic acceptance

- broader real/fixture coverage for expired/challenge/access/rate-limit/server/network conditions;
- more visible last-successful/consecutive-failure lifecycle summaries;
- repost/near-duplicate classification only when corpus evidence justifies it;
- reviewed translation golden corpus/model comparison when permanent model quality is being selected;
- analysis review/correction workflow only if live quality demonstrates recurring correction need;
- pagination/operation-result links where corpus scale requires them;
- corpus-health and Market sampling truthfulness;
- complete combined current-corpus reporting;
- final bounded `jobhunter run` orchestration and browser equivalent;
- end-to-end Phase-1 live acceptance.

## 18. Explicit non-claims

Phase 1 is not complete. JobHunter must not yet claim:

- translation-v2 quality across the full/future corpus;
- complete lifecycle/repost resolution;
- production-quality semantic extraction across all roles;
- canonical market taxonomy;
- full-market conclusions from a small/source-biased analyzed sample;
- personal relevance/capability gaps/readiness;
- career recommendations;
- evidence-backed application/resume/interview readiness;
- arbitrary-web Quick Add ingestion;
- generic source-plugin support;
- final Phase-1 combined report/run automation.
