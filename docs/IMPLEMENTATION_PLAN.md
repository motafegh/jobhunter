# JobHunter Implementation Plan

## 1. Purpose

This document defines the product-level delivery order. It is not a learning roadmap and does not prescribe study sessions.

Detailed Phase 1 execution is controlled by [Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## 2. Delivery rules

- Build operable vertical slices.
- Keep successful acquisition independent from local-model availability.
- Preserve raw evidence before parsing or analysis.
- Prefer one reliable source adapter over several incomplete integrations.
- Add dependencies only for active requirements.
- Keep failures inspectable and retryable.
- Require deterministic tests for acquisition, identity, parsing, and persistence.
- Evaluate model quality separately on a manually reviewed corpus.
- Do not add architecture or governance artifacts that do not improve implementation or operation.

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

M0 is complete. Local structured-output capability remains model-specific and must not block acquisition.

## 5. Phase 1 — Jobinja workflow automation

### Goal

Replace and improve the user's manual process of searching Jobinja, opening jobs, copying relevant fields into files, and sending those files to an AI assistant.

### Required result

A local run must:

```text
saved Jobinja searches
→ discover job advertisements
→ preserve raw evidence
→ identify new and changed postings
→ parse known Jobinja fields
→ analyse new or changed content locally
→ produce individual and combined results
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

All requirements, stop lines, records, and acceptance criteria are defined in the Phase 1 plan.

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
- knowledge, practice, depth, integration, evidence, presentation, and constraint gap classes;
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

Every recommendation must show supporting postings, personal evidence, uncertainty, and the condition that would change it.

## 9. Phase 5 — Trends and operational hardening

Phase 5 will add:

- historical trend calculations;
- model and prompt regression evaluation;
- extraction-quality tracking;
- backup, restore, retention, and export;
- database integrity checks;
- performance and failure-recovery testing;
- optional local interface only if CLI operation becomes inefficient.

## 10. Current authorized implementation

M0, P1.1, and P1.2 are accepted. Repeat-safe discovery was validated live across two two-page searches with 79 combined unique jobs, one cross-search overlap, and zero new jobs on the identical rerun.

A bounded parser-v2 slice across P1.3 and P1.4 is also accepted against fifteen structurally varied live Jobinja advertisements. All fifteen latest semantic versions pass the deterministic local structural audit.

The current implementation and live acceptance target is the operational core of **P1.3 — job-detail acquisition and immutable evidence**:

```text
explicit, missing-only, or refresh-due bounded selection
→ sequential rate-limited detail requests
→ immutable raw detail HTML and metadata
→ deterministic parser-v2 fields
→ semantic new / unchanged decision
→ persistent successful or failed fetch observation
→ inspectable check history
→ bounded refresh scheduling
```

The active commands are:

```text
jobhunter jobinja fetch <job-id> [<job-id> ...]
jobhunter jobinja fetch --missing --limit <count>
jobhunter jobinja fetch --refresh-due --older-than-hours <hours> --limit <count>
jobhunter jobs checks <job-id> [--limit <count>]
jobhunter jobs list
jobhunter jobs audit
jobhunter jobs show <job-id>
```

This increment must keep three records distinct:

- semantic versions describe meaningful advertisement content;
- raw evidence identifies one exact HTTP response;
- fetch observations record when a check happened, whether it changed, or why it failed.

Refresh-due selection must use the latest fetch observation and fall back to a semantic-version timestamp for legacy data. It must remain bounded, sequential, user-controlled, and independent from LM Studio.

Challenge/login classification, retry-backoff refinement, expiration/removal decisions, repost and duplicate-content classification, and full lifecycle transitions remain incomplete. P1.4 still requires broader language and expired-page fixtures before completion. Local model interpretation, responsibility classification, personal relevance, gap analysis, career recommendations, aggregate reports, and `jobhunter run` remain outside the active increment.
