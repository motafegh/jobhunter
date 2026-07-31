# JobHunter Implementation Plan

## 1. Purpose

This document defines the product-level delivery order. It is not a learning
roadmap and does not prescribe study sessions.

Detailed Phase 1 execution is controlled by
[Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## 2. Delivery rules

- Build operable vertical slices.
- Keep successful acquisition independent from local-model availability.
- Preserve raw evidence before parsing or analysis.
- Prefer one reliable source adapter over several incomplete integrations.
- Make source coverage configurable rather than scattering search constants.
- Bound pages, requests, detail checks, retries, and model calls.
- Add dependencies only for active requirements.
- Keep failures inspectable and retryable.
- Require deterministic tests for configuration, acquisition, identity, parsing,
  persistence, and orchestration.
- Evaluate model quality separately on a manually reviewed corpus.
- Do not add architecture or governance artifacts that do not improve
  implementation or operation.

## 3. Product delivery overview

| Stage | Outcome | Status |
|---|---|---|
| M0 | Runnable local foundation, SQLite checks, and LM Studio provider boundary | Complete |
| Phase 1 | Full automation of the user's current Jobinja workflow | Active |
| Phase 2 | Canonical career taxonomy and reliable market matrices | Deferred until Phase 1 evidence is trustworthy |
| Phase 3 | Personal capability evidence and gap analysis | Deferred |
| Phase 4 | Explainable actions, application readiness, and daily career decisions | Deferred |
| Phase 5 | Trends, quality hardening, backup, restore, and sustained operation | Deferred |

## 4. M0 — Local application foundation

M0 established:

- installable Python package and CLI;
- typed TOML configuration;
- local data and evidence directories;
- SQLite health validation;
- isolated LM Studio provider;
- model discovery and optional structured inference smoke testing;
- deterministic tests and lint configuration;
- protected local runtime data and secrets.

M0 is complete. Local structured-output capability remains model-specific and
must not block acquisition.

## 5. Phase 1 — Jobinja workflow automation

### Goal

Replace and improve the user's manual process of searching Jobinja, opening
jobs, copying relevant fields into files, and sending those files to an AI
assistant.

### Required result

A local run must eventually provide:

```text
saved bilingual Jobinja search configuration
→ repeat-safe job discovery
→ immutable raw evidence
→ new / unchanged / changed / failed classification
→ deterministic source-field parsing
→ local evidence-backed analysis
→ individual and combined results
```

### Delivery increments

| Increment | Outcome |
|---|---|
| P1.0 | Repository alignment and controlling Phase 1 plan |
| P1.1 | Search-page acquisition and persisted Jobinja job discovery |
| P1.2 | Bounded pagination, multiple searches, and repeat-safe daily discovery |
| P1.3 | Job-detail acquisition and immutable raw evidence |
| P1.4 | Deterministic Jobinja field parsing and multilingual normalization |
| P1.5 | Posting identity, versions, deduplication, and lifecycle |
| P1.6 | Evidence-backed local LLM analysis and review states |
| P1.7 | Individual outputs, combined analysis, and `jobhunter run` |

All requirements, stop lines, records, and acceptance criteria are defined in
the Phase 1 plan.

## 6. Phase 2 — Career taxonomy and market intelligence

After Phase 1 produces a trustworthy accepted corpus, Phase 2 will add:

- canonical role, responsibility, skill, tool, knowledge, and practice concepts;
- original phrase and alias preservation;
- required/preferred and responsibility-linked counts;
- role-archetype and responsibility-family analysis;
- filters by date, role, seniority, language, location, company, and search;
- co-occurrence analysis;
- evidence-backed matrix exports;
- corpus-size and uncertainty warnings.

Duplicate and unchanged postings must not inflate market counts.

## 7. Phase 3 — Personal capability evidence and gap analysis

Phase 3 will add:

- depth-aware personal capability records;
- project and assessment evidence;
- recency, independence, and evidence-quality fields;
- knowledge, practice, depth, integration, evidence, presentation, and
  constraint gap classes;
- job-level and role-level comparisons;
- explicit unknown and unassessed states.

Exposure must never be represented as mastery.

## 8. Phase 4 — Explainable career actions

Phase 4 will convert reliable market and personal evidence into bounded actions:

- learn;
- practise;
- build;
- improve an existing project;
- document;
- assess;
- monitor;
- ignore for now;
- investigate;
- prepare application evidence.

Every recommendation must show supporting postings, personal evidence,
uncertainty, and the condition that would change it.

## 9. Phase 5 — Trends and operational hardening

Phase 5 will add:

- historical trend calculations;
- model and prompt regression evaluation;
- extraction-quality tracking;
- backup, restore, retention, and export;
- database integrity checks;
- performance and failure-recovery testing;
- optional local interface only if CLI operation becomes inefficient.

## 10. Accepted implementation

The following are accepted on `main`:

- M0 local foundation;
- P1.1 discovery foundation;
- P1.2 bounded pagination, multiple searches, cross-search deduplication, and
  repeat-safe discovery;
- operational detail acquisition for explicit, missing-only, and refresh-due
  selections;
- immutable raw search and detail evidence;
- parser-v2 deterministic Jobinja extraction;
- semantic content versioning;
- persistent successful and failed fetch observations;
- local job, check-history, and parser-audit inspection.

Live evidence currently includes:

- two two-page searches producing 79 unique jobs and one cross-search overlap;
- zero new jobs on the identical discovery rerun;
- fifteen structurally varied complete Jobinja advertisements;
- fifteen of fifteen latest versions passing the deterministic structural audit;
- unchanged refresh checks producing new observations without false versions.

## 11. Current authorized implementation

The current authorized increment is **configurable bilingual acquisition
planning and acquisition-only synchronization**.

The active path is:

```text
built-in profiles and packs
+ custom Persian/English keyword groups
+ optional raw Jobinja URLs
→ normalized term and URL deduplication
→ explicit search plan
→ search limit, cyclic offset, page limit, and global request budget
→ repeat-safe discovery
→ bounded missing and refresh-due detail selection
→ immutable evidence
→ deterministic parsing and semantic versioning
→ fetch observations
→ structural parser audit
→ one acquisition-only sync summary
```

Active commands:

```text
jobhunter jobinja catalog
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch
jobhunter jobs list
jobhunter jobs show
jobhunter jobs checks
jobhunter jobs audit
```

Acceptance requires:

- built-in profile and pack identifiers are validated;
- Persian/Arabic variants and zero-width joiners deduplicate predictably;
- original display terms remain visible;
- custom groups and exclusions require no code changes;
- keyword terms generate canonical Jobinja search URLs;
- raw URLs remain supported for source-owned filters;
- one-run selectors do not silently mix configured searches;
- search windows are stable under the same configuration and version;
- the global request budget is enforced inside discovery;
- budget exhaustion sends no additional request and is not treated as failure;
- `sync` remains bounded to 50 combined detail checks;
- `sync` preserves successful earlier stages when later stages need attention;
- no acquisition command invokes LM Studio.

## 12. Immediate next implementation after acceptance

After local lint, tests, search-plan inspection, and a bounded live sync validate
this increment, the next target is completing remaining P1.3/P1.5 source and
lifecycle states:

- challenge and login-page detection;
- explicit irrelevant-page detection;
- cautious expired/inaccessible classification;
- retry timing and backoff policy;
- last-successful-fetch and consecutive-failure summaries;
- lifecycle transitions that require more than one weak signal;
- duplicate and repost classification only after corpus evidence justifies it.

P1.6 local analysis must not begin until acquisition failures and source-page
classifications are inspectable enough to protect the analysis corpus.

## 13. Remaining outside current scope

The current increment must not claim completion of:

- challenge/login/expired-page classification;
- refined retry and lifecycle policy;
- repost similarity and duplicate-content resolution;
- local model responsibility and requirement interpretation;
- required-versus-preferred classification;
- combined market reports;
- personal relevance and capability gaps;
- career recommendations;
- final `jobhunter run` orchestration including analysis and reporting.
