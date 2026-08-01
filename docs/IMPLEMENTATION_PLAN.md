# JobHunter Implementation Plan

## 1. Purpose

This is the product-level delivery order. It is not a learning roadmap.

Detailed Phase 1 source/analysis work is controlled by
[Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## 2. Delivery rules

- Build operable vertical slices.
- Keep acquisition usable when LM Studio is unavailable.
- Preserve raw evidence before parsing, translation, or analysis.
- Keep translation derived from source versions.
- Prefer local-first providers when they satisfy the requirement.
- Keep search coverage data-driven.
- Bound pages, requests, detail checks, translation/model calls, and retries.
- Keep failures inspectable/retryable.
- Require deterministic tests before live acceptance.
- Let the web UI and CLI share application services/database rather than fork logic.
- Add product/UI complexity only where it improves repeated operation.

## 3. Product delivery overview

| Stage | Outcome | Status |
|---|---|---|
| M0 | Runnable local foundation, SQLite, LM Studio boundary, tests | Complete |
| Phase 1 | Full automation of the Jobinja workflow through analysis/reporting | Active |
| Phase 2 | Canonical career taxonomy and reliable market matrices | Deferred |
| Phase 3 | Personal capability evidence and gap analysis | Deferred |
| Phase 4 | Explainable actions and application readiness | Deferred |
| Phase 5 | Trends, backup/restore, quality and sustained operation | Deferred |

## 4. Phase 1 increments

| Increment | Outcome | Current state |
|---|---|---|
| P1.0 | Repository alignment and controlling plan | Accepted |
| P1.1 | Search acquisition and persisted Jobinja discovery | Accepted |
| P1.2 | Bounded pagination, multiple searches, repeat-safe discovery | Accepted |
| P1.3 | Detail acquisition and immutable evidence | Operational core accepted; response classification remains |
| P1.4 | Deterministic parser, multilingual handling, English projection | Parser + translation foundation live-accepted |
| P1.5 | Posting identity, versions, deduplication, lifecycle | Semantic versions/observations implemented; lifecycle/reposts remain |
| P1.6 | Evidence-backed local LLM semantic analysis | Not started |
| P1.7 | Individual outputs, combined analysis, final `jobhunter run` | Not started |

## 5. Accepted live foundation

Current evidence includes:

- repeat-safe discovery producing 79 unique jobs and one overlap;
- identical rerun producing zero new logical jobs;
- 15 structurally varied current Jobinja details;
- 15/15 source versions clean under parser-v2 structural audit;
- repeated unchanged detail checks reusing semantic versions;
- durable successful/failed fetch observations;
- refresh-due selection based on operational checks;
- data-driven Persian/English search profiles and packs;
- local LM Studio translation with structured output;
- idempotent translation-artifact reuse;
- bounded recovery from a real output-truncation failure;
- 15/15 current English artifacts;
- 15-record current English JSONL export;
- 103 deterministic tests passing at that translation acceptance point;
- successful local browser-app launch against the real corpus;
- browser rendering of discovered jobs with and without complete detail pages.

## 6. Current interface increment — guided local web application

### Goal

Make the accepted acquisition/translation foundation usable as a normal local application
without requiring the user to remember CLI commands or internal configuration terminology.

### Architecture

```text
browser UI                    CLI
     \                         /
      shared JobHunter services
                ↓
             SQLite
        + evidence files
```

The UI is server-rendered FastAPI/Jinja with packaged CSS/vanilla JavaScript. It introduces
no separate frontend database, Node toolchain, or cloud service.

### Implemented browser capabilities

```text
Overview dashboard
→ corpus counts and recent runs
→ guided bounded sync form
→ Light / Normal / Thorough visible-value presets
→ inline explanations of every sync limit
→ parser audit button
→ translate-missing button
→ English export button

Jobs
→ local text/status filtering
→ human-readable company/source-state presentation
→ stable source code labelled as Jobinja reference
→ Quick Add for one job URL, search URL, or Persian/English keyword
→ bounded Quick Add page/detail controls
→ optional translate-after-fetch
→ discovered-but-unfetched state with Fetch details action
→ original + English side-by-side detail
→ evidence identity
→ source-check timeline
→ per-job source refresh
→ per-job translation

Search plan
→ catalog version
→ profiles/packs/terms
→ current bounded generated search window

Operations
→ one-worker mutable action queue
→ live polling
→ inspectable summaries/errors

System
→ storage paths
→ LM Studio/provider/model state
→ current acquisition/translation limits
```

### Quick Add behavior

Quick Add intentionally remains inside the Jobinja source boundary.

```text
Jobinja job URL
→ validate/canonicalize
→ upsert logical job
→ fetch exact detail page
→ preserve evidence
→ parse/version/check
→ optional translation

Jobinja /jobs search URL
→ validate/canonicalize
→ bounded search-page acquisition
→ discover current-run jobs
→ fetch at most 0–20 details
→ optional translation of successful detail fetches

Persian/English phrase
→ build canonical Jobinja keyword search
→ same bounded search/discovery/detail path
```

Non-Jobinja URLs are rejected. Quick Add does not create an unrestricted crawler or mutate
the saved bilingual catalog merely because a one-off phrase was used.

### Guided sync controls

The normal form explains the operational meaning of search breadth, request budget,
missing-detail fetch limit, refresh limit, and refresh age.

Presets are convenience-only and keep the actual values visible/editable:

```text
Light      12 searches / 12 requests / 3 missing / 2 refresh / 24h
Normal     40          / 40          / 10        / 5         / 24h
Thorough   80          / 80          / 20        / 10        / 72h
```

The backend remains authoritative for hard bounds; UI presets cannot bypass them.

### Launcher

```text
jobhunter-app
```

opens the loopback browser application automatically. WSL prefers the Windows browser
opener when available instead of dumping Linux `xdg-open` failures.

Linux can install an application-menu entry with:

```text
jobhunter-app --install-desktop
```

The browser also receives an installable web-app manifest.

### Safety requirements

- loopback-only by default;
- explicit override required for LAN binding;
- CSRF token for every mutating form;
- one mutable browser operation at a time;
- restrictive CSP/frame/referrer/cache/content-type headers;
- no remote/CDN assets;
- browser actions call existing bounded/rate-limited services;
- Quick Add rejects unapproved external-source URLs;
- long UI operations never create a second hidden source lifecycle.

### Deterministic acceptance

The guided web increment must pass:

1. Ruff.
2. Full pytest suite.
3. Primary page rendering against an empty DB.
4. Packaged CSS/JS/manifest/icon availability.
5. CSRF rejection.
6. Operation queue execution/polling.
7. Safe local filtering.
8. Discovered-but-unfetched job rendering.
9. Unknown-job 404 behavior.
10. Quick Add job/search/keyword input classification.
11. Pre-network rejection of non-Jobinja URLs.
12. Human-readable company fallback and Jobinja-reference labels.
13. Guided sync/preset UI presence.

### Live acceptance

Then confirm against the real local corpus:

1. `jobhunter-app` opens/reuses the dashboard without browser-opener noise.
2. Dashboard displays the current real counts.
3. Guided sync explanations/presets render correctly.
4. Jobs page presents companies and Jobinja references clearly.
5. A known missing-detail posting shows a normal Fetch details state.
6. Quick Add a harmless one-off keyword with one search page and a small detail limit.
7. Confirm its discovered/fetched jobs appear immediately in the same Jobs catalog.
8. Quick Add one direct public Jobinja job URL and confirm one logical job/detail result.
9. Optional translation works only when deliberately selected.
10. Parser audit and English export continue to work from buttons.

Do not mark the new Quick Add/guided-controls increment live-accepted before these checks.

## 7. Next source/lifecycle work after UI acceptance

Complete remaining P1.3/P1.5 behavior:

- classify challenge/login/CAPTCHA/error/expired/inaccessible pages;
- define cautious retry/backoff from classified failures;
- expose last-successful-check and consecutive-failure summaries;
- require multiple signals for destructive lifecycle transitions;
- classify repost/duplicate content when corpus evidence justifies it.

## 8. Then P1.6 — semantic local analysis

P1.6 will transform accepted source/English representations into validated analytical
records such as responsibilities, requirements, source-explicit versus inferred concepts,
confidence, and evidence passages.

English projection may be a model convenience, but material claims must remain traceable
to original employer text.

Translation quality should later receive a reviewed Persian→English golden corpus so
provider/model changes can be compared rather than guessed.

## 9. Later phases

### Phase 2

Canonical career concepts, role archetypes, responsibility families, demand counts,
co-occurrence, and market matrices.

### Phase 3

Depth-aware personal capability evidence and gap classes.

### Phase 4

Evidence-backed career actions and application readiness.

### Phase 5

Historical trends, backup/restore, regression quality, retention, performance, and sustained
operation.

## 10. Remaining non-claims

The project must not yet claim completion of:

- full job lifecycle classification;
- repost/duplicate resolution;
- semantic responsibility extraction;
- required/preferred qualification classification;
- aggregate market conclusions;
- personal relevance or capability gaps;
- readiness scores;
- career recommendations;
- arbitrary-web Quick Add ingestion;
- final P1.7 analysis/report automation.
