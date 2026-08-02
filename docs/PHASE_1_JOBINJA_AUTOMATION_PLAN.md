# Phase 1 — Jobinja Workflow Automation Plan

## 1. Status and authority

**Status:** Active implementation plan  
**Scope:** Phase 1  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless isolation is clearly required.

This document is subordinate to
[JobHunter Master Implementation Plan](IMPLEMENTATION_PLAN.md) and controls detailed
Phase-1 order, records, boundaries, and acceptance.

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

The browser application is the normal human interface; CLI remains supported for advanced
operation/debugging/automation.

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
16. expose the workflow through browser UI and CLI.

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
validated analysis artifact
        ↓
per-job analysis + Market aggregation
```

Google Cloud Translation remains an optional external alternative, not a normal dependency.

## 5. Source/search boundary

Search vocabulary lives in versioned TOML data and supports profiles, packs, Persian and
English terms, custom groups, exclusions, raw Jobinja URL escape hatches, deterministic
search windows, page limits, request delays, and global request budgets.

Search vocabulary is acquisition configuration, not a career taxonomy and not proof of
personal relevance.

Use approved public Jobinja pages only. Preserve canonical URL attribution, validate hosts
and redirects, bound request/response volume, and keep requests sequential/rate-limited.

Do not automate login/applications, scrape private profiles, bypass CAPTCHA/access controls,
rotate identities/proxies to defeat limits, or create unrestricted crawling.

## 6. Durable record boundaries

Never conflate:

```text
JobPosting                    stable logical Jobinja identity
SearchPageSnapshot            exact search response evidence
JobPostingVersion             meaningful employer-content version
JobDetailFetchObservation     operational source check
JobLifecycleEvent             classified lifecycle evidence
JobTranslationArtifact        derived English view of one exact source version
JobTranslationAttempt         operational translation attempt
JobAnalysisArtifact           model-derived evidence-backed interpretation
JobAnalysisAttempt            operational semantic-analysis attempt
JobUserWorkflow               local human triage state
Browser WebOperation          ephemeral UI execution state
```

Source evidence remains authoritative over translation and model-derived records.

## 7. Parser boundary

Parser v2 extracts explicit Jobinja fields and complete source text before translation or
semantic analysis. Missing fields remain missing.

Jobinja source skill tags remain distinct from future description-derived semantic concepts.

A clean parser audit certifies known structural/parser checks only. It does not certify
translation quality or semantic-analysis quality.

## 8. Translation v2 boundary

Translation v1 is historical because real field-to-translation association corruption was
observed.

Current contracts:

```text
provider: lm-studio-translation-v2
projection: english-projection-v2
```

V2 rules:

- preserve v1 artifacts historically;
- current/exportable English must use the current v2 projection schema;
- use content-derived translation identities;
- translate one semantic segment per local LM request for the current hardened path;
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

## 9. Source response classification and lifecycle

Implemented classes include:

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
- rate limit/access/challenge/server/network errors do not become destructive lifecycle
  conclusions.

Remaining lifecycle acceptance work includes real/fixture coverage, last-successful-check
summary, consecutive-failure summary, and later repost/near-duplicate handling.

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

Missing-detail priority may use search/discovery/title signals to decide fetch order, but it
must never be described as personal fit/readiness.

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
- model request/response is retained for auditability;
- prompt/schema/model changes create distinct artifacts.

## 12. Search effectiveness and first Market aggregation

Search Plan may report:

- distinct jobs found per search;
- discovery events/runs;
- unique contributions;
- overlap/provenance.

Do not auto-prune high-overlap vocabulary.

Market currently aggregates accepted current analysis artifacts and keeps requirement strength
separate. It is not yet Phase-2 canonical taxonomy; aliases such as Postgres/PostgreSQL must
not be silently merged without reviewed canonicalization.

## 13. Browser application boundary

Current/implemented browser surfaces include:

```text
Overview
Jobs
Job detail
Search plan
Market
Operations
System
```

Normal workflow:

```text
run bounded sync
→ fetch priority missing details
→ repair/build current English v2
→ analyze small ready batch
→ inspect per-job analysis
→ inspect Market aggregate
```

Jobs UI supports filtering/triage and bounded bulk actions. Browser actions must use the same
core services and bounds as CLI paths.

The UI remains loopback-first, CSRF-protected, locally packaged, and limited to one mutable
browser operation at a time unless later concurrency is explicitly proven safe.

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
| Local browser app | Operating live; new intelligence surfaces pending acceptance |
| P1.6 evidence-backed analysis | Implemented; deterministic/live acceptance pending |
| P1.7 individual/aggregate outputs | Partial; Market/per-job surfaces implemented |

## 15. Accepted live evidence so far

Previously established:

- initial repeat-safe corpus of 79 unique jobs;
- identical rerun creating zero new logical jobs;
- later browser sync: 40/40 search requests, 273 unique postings, 241 new, 32 known,
  zero search failures;
- 10/10 selected details fetched successfully in that run;
- 26/26 current parsed jobs structurally clean at that point;
- semantic versions protected from volatile raw HTML;
- fetch observations and refresh-due selection;
- local LM Studio translation and idempotent reuse;
- bounded recovery from a real translation output truncation;
- browser app/Quick Add/guided sync/missing-detail backlog functioning.

Historical translation-v1 success is not sufficient to certify current English quality
because later real field-association corruption was discovered.

## 16. Current exact acceptance sequence

Do not add new Phase-1 features until this sequence completes:

1. confirm/fix legacy DB migration ordering;
2. exclude parser metadata from P1.6 employer evidence;
3. resolve Ruff findings;
4. run full Ruff;
5. run full pytest;
6. run `pytest -W error` and fix residual root causes;
7. open/migrate the real database only after deterministic green;
8. repair one previously corrupted v1 translation to v2 and inspect it;
9. repair a second affected job and inspect it;
10. repair the wider parsed corpus in bounded batches;
11. run one real P1.6 analysis and inspect every source evidence excerpt;
12. rerun that job and confirm reuse;
13. analyze a small reviewed batch, default 5;
14. inspect the Market page;
15. accept/revise P1.6 before scaling analysis.

## 17. Remaining Phase-1 work after current acceptance

- broader real/fixture coverage for expired/challenge/access/rate-limit conditions;
- more visible last-successful/consecutive-failure lifecycle summaries;
- repost/near-duplicate classification when corpus evidence justifies it;
- reviewed translation golden corpus/model comparison;
- analysis review/correction workflow only if live quality demonstrates the need;
- pagination/operation-result links where corpus scale requires them;
- complete combined current-corpus reporting;
- final bounded `jobhunter run` orchestration and browser equivalent;
- end-to-end Phase-1 live acceptance.

## 18. Explicit non-claims

Phase 1 is not complete. JobHunter must not yet claim:

- translation-v2 quality across the full corpus;
- complete lifecycle/repost resolution;
- production-quality semantic extraction across all roles;
- canonical market taxonomy;
- full-market conclusions from a small analyzed sample;
- personal relevance/capability gaps/readiness;
- career recommendations;
- arbitrary-web Quick Add ingestion;
- final Phase-1 combined report/run automation.
