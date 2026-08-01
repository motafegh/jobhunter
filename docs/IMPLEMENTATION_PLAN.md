# JobHunter Implementation Plan

## 1. Purpose

This document defines the product-level delivery order. It is not a learning
roadmap and does not prescribe study sessions.

Detailed Phase 1 execution is controlled by
[Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## 2. Delivery rules

- Build operable vertical slices.
- Keep successful acquisition independent from local-model availability.
- Preserve raw evidence before parsing, translation, or analysis.
- Keep translation derived from source versions rather than mixed into source evidence.
- Prefer one reliable source adapter over several incomplete integrations.
- Make source coverage data-driven rather than scattering search constants.
- Bound pages, requests, detail checks, translation batches, retries, and model calls.
- Add dependencies only for active requirements.
- Keep failures inspectable and retryable.
- Require deterministic tests for configuration, acquisition, identity, parsing,
  translation, persistence, export, and orchestration.
- Evaluate translation and model quality separately on manually reviewed corpora.
- Do not add architecture or governance artifacts that do not improve operation.

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

M0 established the package, CLI, typed TOML configuration, SQLite foundation,
local evidence directories, LM Studio provider boundary, smoke testing, linting,
and deterministic test foundation.

M0 is complete. Local-model availability must never block source acquisition.

## 5. Phase 1 — Jobinja workflow automation

### Goal

Replace and improve the manual process of searching Jobinja, opening jobs,
copying fields into files, and sending those files to an AI assistant.

### Required result

```text
saved bilingual Jobinja search configuration
→ repeat-safe job discovery
→ immutable raw evidence
→ new / unchanged / changed / failed classification
→ deterministic source-field parsing
→ optional versioned English projection
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
| P1.4 | Deterministic Jobinja parsing, multilingual normalization, and derived English projection |
| P1.5 | Posting identity, versions, deduplication, and lifecycle |
| P1.6 | Evidence-backed local LLM analysis and review states |
| P1.7 | Individual outputs, combined analysis, and `jobhunter run` |

## 6. Phase 2 — Career taxonomy and market intelligence

After Phase 1 produces a trustworthy accepted corpus, Phase 2 will add canonical
career concepts, role archetypes, responsibility families, requirement-linked
counts, filters, co-occurrence analysis, and evidence-backed matrices.

Source language and English projection provenance must remain available as corpus
filters so translated content can be evaluated separately from native-English
content.

## 7. Phase 3 — Personal capability evidence and gap analysis

Phase 3 will add depth-aware personal capability evidence, gap classes, recency,
independence, evidence quality, and job/role comparisons. Exposure must never be
represented as mastery.

## 8. Phase 4 — Explainable career actions

Recommendations will remain evidence-backed and bounded to actions such as learn,
practise, build, improve, document, assess, monitor, investigate, ignore for now,
or prepare application evidence.

## 9. Phase 5 — Trends and operational hardening

Phase 5 will add historical trends, regression evaluation, extraction/translation
quality tracking, backup/restore, retention, performance testing, and sustained
operation hardening.

## 10. Accepted implementation

Accepted on `main` before the current translation increment:

- M0 local foundation;
- P1.1 discovery foundation;
- P1.2 repeat-safe bounded pagination and multi-search discovery;
- operational detail acquisition for explicit, missing-only, and refresh-due jobs;
- immutable raw search/detail evidence;
- parser-v2 deterministic Jobinja extraction;
- semantic content versioning;
- persistent successful/failed fetch observations;
- local job, check-history, and parser-audit inspection.

Live evidence includes:

- two two-page searches producing 79 unique jobs and one cross-search overlap;
- zero new jobs on the identical discovery rerun;
- fifteen structurally varied complete Jobinja advertisements;
- fifteen of fifteen latest versions passing structural audit;
- unchanged refresh checks producing observations without false semantic versions.

## 11. Current authorized implementation

The current authorized increment combines **data-driven bilingual acquisition
configuration** with the **derived English corpus foundation**.

### Search path

```text
packaged or user-supplied TOML search catalog
+ custom Persian/English groups
+ optional raw Jobinja URLs
→ normalized identity and URL deduplication
→ inspectable search plan
→ search/page/request bounds
→ repeat-safe discovery
```

### Source path

```text
discovery
→ bounded missing/refresh detail selection
→ immutable evidence
→ deterministic parser-v2 source fields
→ semantic source version
→ fetch observation
→ structural parser audit
```

### Translation path

```text
latest semantic source version
→ Persian-content detection
→ native-English identity projection OR TranslationProvider
→ versioned English fields + complete English document
→ native/translated segment provenance
→ translation artifact + attempt history
→ current English JSONL corpus
```

Active commands:

```text
jobhunter jobinja catalog [--show-terms]
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch
jobhunter jobs list
jobhunter jobs show
jobhunter jobs checks
jobhunter jobs audit
jobhunter translations status
jobhunter translations run
jobhunter translations show
jobhunter translations export
```

Acceptance requires:

- search words are loaded from versioned TOML data rather than Python tuples;
- a complete custom search catalog can replace the packaged vocabulary;
- Persian/Arabic spelling variants deduplicate predictably;
- original display terms remain visible;
- bounded search windows cover all selected packs round-robin;
- source acquisition remains idempotent and bounded;
- translation is disabled by default;
- native-English source fields create identity artifacts without external calls;
- Persian/mixed source fields use an isolated provider;
- the Google provider uses official Cloud Translation Basic v2 semantics;
- translation artifacts are keyed by source version/provider/model/schema;
- repeated identical translation reuses the existing artifact;
- a newer source semantic version invalidates the old artifact as current corpus data;
- translated versus native string provenance is retained;
- only current-source-version artifacts are exported;
- translation failure never alters source evidence or semantic history;
- automatic translation after sync is explicit, bounded, and opt-in;
- no translation artifact is treated as stronger employer evidence than source text.

## 12. Immediate acceptance work

Before moving on, validate:

1. Ruff and the complete deterministic pytest suite.
2. Search-catalog loading and the effective bilingual plan.
3. Existing source acquisition still works unchanged when translation is disabled.
4. One native-English projection produces no Google request.
5. One Persian/mixed real Jobinja posting translates successfully through Google
   Cloud when explicitly enabled.
6. Repeating the same translation reports `reused`.
7. `translations show` displays the current English projection.
8. `translations export` produces a valid current-version JSONL corpus.
9. Automatic translation after a deliberately bounded sync works when enabled.

Translation quality acceptance must examine actual terminology and requirement
strength; transport success alone is insufficient.

## 13. Next implementation after acceptance

Then complete remaining P1.3/P1.5 source/lifecycle behavior:

- challenge/login/error-page detection;
- cautious expired/inaccessible classification;
- retry/backoff rules based on classified failures;
- last-successful-fetch and consecutive-failure summaries;
- lifecycle transitions requiring more than one weak signal;
- duplicate/repost classification when corpus evidence justifies it.

In parallel with P1.6 preparation, create a small manually reviewed
Persian→English translation golden corpus to compare Google NMT and any later
translation provider/model.

P1.6 local analysis must preserve original evidence links even when it consumes
English projected text.

## 14. Remaining outside current scope

The current increment must not claim completion of:

- translation quality evaluation across a reviewed golden corpus;
- terminology glossary locking or custom Google glossary support;
- challenge/login/expired-page classification;
- complete lifecycle policy;
- repost similarity and duplicate-content resolution;
- local-model responsibility and requirement interpretation;
- required-versus-preferred classification;
- combined market reports;
- personal relevance and capability gaps;
- career recommendations;
- final `jobhunter run` orchestration including analysis and reporting.
