# Phase 1 — Jobinja Workflow Automation Plan

## 1. Status and authority

**Status:** Active implementation plan  
**Scope:** Phase 1  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless isolation is clearly required.

This document controls Phase 1 order, records, boundaries, and acceptance.

## 2. Objective

Replace and improve the former manual workflow:

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
→ repeat-safe acquisition
→ immutable evidence
→ deterministic structured source data
→ semantic version/check history
→ local English projection
→ evidence-backed local semantic analysis
→ inspectable individual/combined results
```

The browser application should be the normal human interface; CLI remains supported.

## 3. Final intended Phase 1 run

A complete final run will eventually:

1. load the bilingual search catalog/profiles/custom groups/raw URLs;
2. construct a bounded plan;
3. acquire search pages and preserve evidence;
4. discover stable Jobinja identities repeat-safely;
5. select missing/refresh-due details;
6. preserve detail evidence;
7. parse source-explicit fields deterministically;
8. classify source content as new/unchanged/changed;
9. retain every source check;
10. create/reuse current English projection when configured;
11. select new/changed versions for local semantic analysis;
12. validate structured evidence-backed model output;
13. persist review states/results;
14. update combined reporting;
15. expose the result through browser UI and CLI.

Manual copying of individual jobs should not be required.

## 4. Current accepted flow

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
missing / refresh-due selection
        ↓
detail acquisition
        ↓
raw detail evidence
        ↓
Jobinja parser v2
        ↓
semantic source version
        ↓
fetch observation
        ↓
structural parser audit
        ↓
current English projection
  ├─ source identity for native English
  └─ local LM Studio structured translation
        ↓
versioned English artifact + attempt
        ↓
current English JSONL corpus
```

Google Cloud Translation remains an optional external alternative, not a normal dependency.

## 5. Search configuration

Search vocabulary lives in versioned TOML data. It supports profiles, packs, Persian and
English terms, custom groups, exclusions, raw Jobinja URL escape hatches, deterministic
search windows, page limits, request delays, and global request budgets.

Normalized identity may harmonize Persian/Arabic character variants, case, whitespace, and
zero-width characters without changing the displayed search term.

Search vocabulary is acquisition configuration, not a career taxonomy.

## 6. Source safety

Use approved public Jobinja pages only. Preserve canonical URL attribution, validate hosts
and redirects, bound response/request volume, and keep requests sequential/rate-limited.

Do not automate login/applications, scrape private profiles, bypass CAPTCHA/access controls,
rotate identities/proxies to defeat limits, or create unrestricted crawling.

## 7. Source identity and records

### JobPosting

Stable logical source identity keyed by Jobinja source job code.

### SearchPageSnapshot

One exact search response with evidence hash/path and discovery count.

### JobPostingVersion

One meaningful deterministic employer-content version. Raw HTML volatility alone must not
create a new semantic version.

### JobDetailFetchObservation

One successful/failed source check, independent from semantic history.

### JobTranslationArtifact

One derived English projection of one exact source semantic version under one target
language/provider/model/schema identity.

### JobTranslationAttempt

One `completed`, `failed`, or `reused` translation operation.

### AnalysisRun / DailyReport

Future P1.6/P1.7 records for versioned model analysis and combined reporting.

## 8. Parser boundary

Parser v2 extracts explicit Jobinja fields and complete source text before translation or
semantic analysis. Missing fields remain missing. Jobinja source skill tags remain distinct
from future description-derived career concepts.

A clean structural audit means no known parser-shape/contamination issue was detected. It
does not certify semantic interpretation.

## 9. Translation boundary

Source evidence is authoritative. English is derived convenience data.

Native-English strings pass through without translation calls. Persian-containing strings
translate as semantic units and retain `native`/`translated` provenance.

Normal provider:

```toml
translation_provider = "lm-studio"
```

Model-selection priority:

```text
translation_lm_studio_model
→ lm_studio_model
→ exactly-one-visible-model auto-selection
```

Ambiguous selection fails closed.

LM Studio translation uses JSON-schema structured output and rejects missing/extra/duplicate
IDs, count mismatches, empty translations, or malformed responses.

The prompt/provider contract is versioned independently from source parsing. Current
contract: `lm-studio-translation-v1`.

Explicit output truncation uses bounded recovery:

```text
multi-segment truncation → split recursively
single-segment truncation → double output budget up to 32,768
```

Source text is never shortened to satisfy translation limits.

## 10. Browser UI boundary

The browser app is a second interface over the same services/database.

Current screens:

```text
Overview
Jobs
Job detail
Search plan
Operations
System
```

Browser mutation actions cover bounded sync, audit, missing translation, export, per-job
source check, and per-job translation.

The UI must remain loopback-first, CSRF-protected, self-contained (no CDN assets), and
limited to one mutable browser operation at a time unless future concurrency is proven safe.

Browser runtime operation cards are ephemeral; durable source/translation history remains
in SQLite.

## 11. Delivery state

### P1.0 — Repository alignment

Accepted.

### P1.1 — Discovery foundation

Accepted.

### P1.2 — Pagination and repeat-safe discovery

Accepted through live repeated multi-search validation.

### P1.3 — Detail acquisition and evidence

Operational core accepted. Remaining:

- challenge/login/CAPTCHA/error/expired/irrelevant classification;
- classified retry/backoff policy.

### P1.4 — Parser, multilingual handling, English projection

Live-accepted foundation:

- parser v2 clean across 15 varied advertisements;
- 15/15 current English artifacts through local LM Studio;
- translation reuse/idempotency;
- real output-truncation recovery;
- current 15-record JSONL export.

Translation quality is useful but still requires a future reviewed Persian→English golden
corpus before treating any model as a permanent quality standard.

### P1.5 — Identity, versions, lifecycle

Implemented:

- stable Jobinja identity;
- semantic versions;
- raw evidence separation;
- fetch observations;
- refresh-due selection.

Remaining:

- cautious active/expired/inaccessible transitions;
- consecutive-failure/lifecycle summaries;
- repost/duplicate classification.

### Local browser interface

Implementation complete; deterministic/live acceptance pending.

### P1.6 — Evidence-backed local semantic analysis

Not started. It will add versioned prompts/schemas, responsibilities, requirements,
source-explicit versus inferred concepts, evidence passages, confidence, validation, and
review states.

### P1.7 — Individual/combined semantic outputs

Not started.

## 12. Accepted live evidence

Current accepted foundation includes:

- 79 unique initial discovered jobs;
- one cross-search overlap;
- zero new jobs on identical discovery rerun;
- 15 current complete parser-v2 advertisements;
- 15/15 structurally clean audits;
- repeated unchanged source checks without false semantic versions;
- bounded refresh-due behavior;
- local LM Studio translation selected explicitly;
- 15/15 current English artifacts;
- 15-record English JSONL export;
- bounded successful recovery from `finish_reason="length"`;
- 103 deterministic tests passing before the browser increment.

## 13. Browser acceptance target

Deterministic acceptance:

1. Ruff passes.
2. Full pytest suite passes.
3. Primary pages render locally.
4. Packaged CSS/JS/icon/manifest load.
5. Security headers are present.
6. Invalid CSRF is rejected.
7. Browser operations execute/poll correctly.
8. Empty/local filtering is safe.

Live acceptance against the real corpus:

1. dashboard shows correct real counts;
2. jobs page shows discovered corpus;
3. `tpLF` shows original + English current artifact;
4. search plan shows configured bilingual coverage;
5. parser audit completes from browser;
6. one bounded sync completes from browser;
7. export button produces the current corpus;
8. desktop launcher works when installed.

## 14. Next work after browser acceptance

Complete remaining P1.3/P1.5 response/lifecycle classification, then begin P1.6 semantic
analysis.

P1.6 may use English projection for model convenience, but every material claim must retain
a path to original employer evidence.

## 15. Explicit non-claims

Phase 1 is not complete. JobHunter must not yet claim full lifecycle classification,
repost resolution, responsibility extraction, required/preferred qualification analysis,
aggregate market intelligence, personal relevance/gaps, career recommendations, or the
final combined Phase 1 report workflow.
