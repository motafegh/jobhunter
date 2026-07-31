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

The current target is **P1.1 — Jobinja discovery foundation**.

The active code increment must support:

```text
one configured or command-line Jobinja search URL
→ bounded HTTP fetch
→ raw search-page evidence
→ job-link canonicalization
→ repeat-safe SQLite discovery records
→ concise CLI summary
```

It must not require LM Studio and must stop before full job-detail parsing or analysis.
