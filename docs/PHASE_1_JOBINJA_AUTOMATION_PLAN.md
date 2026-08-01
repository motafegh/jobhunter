# Phase 1 — Jobinja Workflow Automation Plan

## 1. Status and authority

**Status:** Active implementation plan  
**Scope:** Phase 1 only  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless isolation is clearly required.

This document controls Phase 1 implementation order, boundaries, records, and
acceptance criteria. The product specification, architecture, domain model, and
source policy remain controlling at their respective levels.

## 2. Phase objective

Phase 1 must replace and improve the user's manual Jobinja process:

```text
manual keyword searches
→ open advertisements
→ copy descriptions and skills into files
→ send files to an AI assistant
→ request individual and combined analysis
```

The target system configures searches once, preserves evidence, identifies new
and changed jobs, parses explicit source fields, optionally creates a separate
English projection, runs local evidence-backed analysis, and produces inspectable
individual and combined results.

## 3. Target daily experience

The intended final Phase 1 endpoint is:

```bash
jobhunter run
```

A complete run will eventually:

1. load the effective bilingual search catalog, profiles, custom groups, and raw URLs;
2. build an inspectable bounded search plan;
3. acquire search pages sequentially and preserve evidence;
4. discover stable Jobinja job identities repeat-safely;
5. select missing and refresh-due job details;
6. preserve raw detail evidence;
7. parse explicit Jobinja fields deterministically;
8. classify semantic source content as new, unchanged, or changed;
9. retain every successful or failed fetch observation;
10. create or reuse the current English projection when configured;
11. queue new or changed versions for local analysis;
12. validate evidence-backed structured model output;
13. persist individual results and review states;
14. update a combined report;
15. print a concise actionable summary.

The system must not require manual copying of individual job URLs or text.

## 4. Phase 1 data flow

```text
Data-driven bilingual search configuration
        ↓
Search-plan expansion and bounds
        ↓
Search-page acquisition
        ↓
Raw search-page evidence
        ↓
Job identity and discovery provenance
        ↓
Missing / refresh-due selection
        ↓
Job-detail acquisition
        ↓
Raw job-page evidence
        ↓
Deterministic Jobinja parsing
        ↓
Semantic source-version decision
        ↓
Fetch observation
        ↓
Optional English projection
  ├─ native-English identity projection
  └─ configured TranslationProvider
        ↓
Versioned English artifact + translation attempt
        ↓
Local LLM structured analysis
        ↓
Validation and review state
        ↓
Individual and combined outputs
```

Acquisition remains useful when LM Studio or the external translation provider is
unavailable. Translation failure must not invalidate source evidence or semantic
versions.

## 5. Search configuration

### 5.1 Data-driven catalog

Pack/profile vocabulary is loaded from versioned TOML data:

```text
src/jobhunter/data/search_catalog.toml
```

A complete replacement catalog can be configured without Python changes:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

### 5.2 Profiles and packs

```toml
jobinja_search_profiles = ["ai-security-python"]
jobinja_search_packs = ["ai-security"]
```

### 5.3 Custom keyword groups

```toml
[[jobhunter.jobinja_keyword_groups]]
name = "My hybrid roles"
terms = [
  "مهندس امنیت هوش مصنوعی",
  "AI Security Engineer",
  "Python Security Automation",
]
enabled = true
max_pages = 1
```

### 5.4 Raw Jobinja URLs

Raw result URLs remain supported for source-owned filters.

### 5.5 Normalization, interleaving, and bounds

Term identity may normalize Unicode, Persian/Arabic character variants,
whitespace, case, and zero-width joiners while preserving the displayed source
term. Selected packs are interleaved round-robin so bounded windows represent
multiple career domains.

Search configuration supports:

- maximum pages per search;
- maximum selected searches;
- cyclic search offset;
- global search-page request budget;
- sequential request delay;
- explicit one-run selectors.

Budget exhaustion is a controlled stop, not a failure.

## 6. Source boundaries and safety

Phase 1 will:

- use public Jobinja search and detail pages only;
- preserve source attribution and canonical URLs;
- use sequential bounded acquisition;
- validate redirects and approved hosts;
- retain raw evidence locally;
- report access denial, challenge, CAPTCHA, login, or unsupported pages.

Phase 1 will not:

- automate login or applications;
- scrape private profiles or resumes;
- bypass CAPTCHA, blocking, authentication, or access controls;
- use stealth proxy rotation;
- create an unrestricted crawler;
- redistribute collected advertisements publicly.

Google Cloud Translation is not a source-acquisition adapter. When explicitly
enabled it transmits already-parsed job text to a translation service and must be
treated as a separate external-data boundary.

## 7. Source-specific identity

The Jobinja source job code remains the primary external identity. The title slug
is descriptive and not stable identity.

## 8. Language and translation handling

Jobinja advertisements may be Persian, English, or mixed.

Phase 1 preserves:

- exact original raw evidence;
- deterministic original-language parsed fields;
- source language classification;
- native English technical terms embedded in Persian text;
- any translation as a separately versioned derived artifact;
- per-segment `native` or `translated` provenance in the English projection.

Translation must never overwrite raw evidence or source semantic fields.

### 8.1 Native English

If projected source fields contain no Persian text, JobHunter creates a
`source-identity / native-english` English artifact without an external provider
request.

### 8.2 Persian or mixed content

Persian-containing strings are translated through the configured
`TranslationProvider`. Mixed Persian/English strings are translated as semantic
units rather than by replacing hard-coded words.

### 8.3 Translation identity

A derived artifact is identified by:

```text
source semantic-version ID
+ target language
+ provider
+ provider model
+ translation schema version
```

Changing the translator/model/schema creates a different derived artifact. It
does not create a new employer-content semantic version.

## 9. Deterministic extraction boundary

Explicit Jobinja fields are extracted by deterministic code before translation
or LLM interpretation. Missing fields remain missing. Source skill tags remain
separate from later description-derived skills.

## 10. Phase 1 records

### SearchDefinition

- source;
- stable name;
- canonical URL;
- origin profile, pack, group, term, or raw URL when available;
- enabled state;
- page limit;
- created and updated timestamps.

### AcquisitionRun

- run identifier;
- start and completion timestamps;
- status;
- search, request, page, job, overlap, and failure counts;
- failure summary.

### SearchPageSnapshot

- run/search/page;
- requested and final URLs;
- retrieval time;
- HTTP status;
- content hash;
- evidence paths;
- discovered count.

### JobPosting

- source and source job code;
- canonical URL and company slug;
- first and last seen times;
- lifecycle state.

### JobDiscovery

- run;
- search/page;
- job posting;
- timestamp.

### JobPostingVersion

- posting reference;
- retrieval time;
- version-defining raw evidence;
- deterministic source fields;
- semantic fingerprint;
- parser/language metadata.

### JobDetailFetchObservation

- source posting;
- check timestamp;
- new-version, unchanged, or failed outcome;
- URLs/status/hashes when available;
- version reference;
- evidence paths;
- error details.

### JobTranslationArtifact

- exact source detail-version reference;
- source semantic SHA-256;
- source and target languages;
- provider and model;
- translation schema version;
- structured English fields;
- complete English document;
- per-segment provenance;
- native/translated counts;
- projection SHA-256;
- creation timestamp.

### JobTranslationAttempt

- exact source detail-version reference;
- attempt timestamp;
- provider/model/schema;
- `completed`, `failed`, or `reused` outcome;
- artifact reference when available;
- failure type/message when applicable.

### AnalysisRun

- source posting version;
- English artifact reference when used;
- model, prompt, and schema versions;
- request/response evidence;
- validated result;
- success/failure/review state;
- original source evidence references for material claims.

### DailyReport

- run and corpus window;
- source, translation, analysis, and review counts;
- conclusions and uncertainty notes.

## 11. Processing states

Source progression:

```text
discovered
→ acquired
→ parsed
→ pending_analysis
→ analysed
→ review_required or accepted
```

Translation is parallel derived state, not a source lifecycle transition:

```text
translation_missing
translation_completed
translation_failed
translation_reused
```

A later-stage failure must not delete earlier successful evidence.

## 12. Delivery increments

### P1.0 — Repository alignment

Accepted.

### P1.1 — Discovery foundation

Accepted.

### P1.2 — Pagination and repeat-safe discovery

Accepted through live repeated two-search/two-page validation.

### P1.3 — Detail acquisition and evidence

Operational core accepted. Challenge/login/error/expired/irrelevant page
classification and refined retry policy remain incomplete.

### P1.4 — Deterministic parser, language normalization, and English projection

Deliverables:

- source-specific parser;
- complete original description preservation;
- Persian/Arabic normalization for matching without overwriting source text;
- language classification;
- structural parser audit;
- isolated translation-provider boundary;
- native-English identity projection;
- Persian/mixed English projection;
- provider/model/schema versioned translation artifacts;
- translation attempt history;
- per-segment native/translated provenance;
- current English-corpus JSONL export;
- representative parser and translation fixtures.

Parser v2 is live-accepted against fifteen varied advertisements. The English
projection implementation is complete but requires local deterministic and live
Google acceptance before this translation portion is accepted.

Translation acceptance requires:

- source fields/evidence remain unchanged;
- native-English source requires no external call;
- Persian/mixed translation produces complete English fields/document;
- repeating an identical translation reuses the artifact;
- source semantic changes require a new artifact;
- provider/model/schema identity is retained;
- failures remain independent from source acquisition;
- export includes only each job's current source-version artifact;
- a real Persian/mixed sample is manually checked for requirement-strength and
  technical-term fidelity.

### P1.5 — Identity, versions, and lifecycle

Semantic versions and fetch observations are implemented. Repost, duplicate,
and lifecycle classification remain incomplete.

### P1.6 — Evidence-backed local analysis

P1.6 may use current English projection text for model convenience, but every
material claim must remain traceable to original employer text. Translation alone
cannot establish requirement strength.

Deliverables remain versioned analysis schema, evidence passages, Persian/English
handling, validated structured output, bounded retries, review states, reanalysis,
and a manually reviewed golden corpus.

### P1.7 — Individual outputs and combined report

Remains future work.

## 13. Phase completion criteria

Phase 1 is complete only when:

1. searches are configured once;
2. normal runs discover jobs automatically;
3. acquisition is bounded and observable;
4. new/changed jobs preserve immutable source evidence;
5. explicit Jobinja fields parse deterministically;
6. Persian, English, and mixed source text remain intact;
7. an English derived representation is available when configured without losing
   original-language provenance;
8. local analysis produces evidence-backed structured results;
9. failures remain inspectable/retryable;
10. individual and combined reports exist;
11. reruns do not inflate unchanged data;
12. no access-control bypass or application automation is required.

## 14. Deferred work

Outside Phase 1 unless required:

- other job platforms;
- generic crawling;
- automated applications/messages;
- full personal capability graph;
- long-term trend analysis;
- salary/hiring-probability prediction;
- distributed services;
- model fine-tuning;
- vector databases without demonstrated need.

## 15. Current authorized implementation

Accepted source evidence:

- M0, P1.1, and P1.2;
- 79 unique jobs across two two-page searches with one overlap;
- zero new jobs on identical discovery rerun;
- fifteen complete parser-v2 advertisements;
- fifteen of fifteen latest versions structurally clean;
- unchanged checks creating observations without false versions;
- bounded refresh-due selection.

Current target: **data-driven bilingual search configuration plus versioned English
projection acceptance**.

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

After this increment passes deterministic and bounded live validation, the next
source target is challenge/login/irrelevant/expired-page classification, retry
policy, and cautious lifecycle transitions. P1.6 semantic analysis must retain
original-source evidence even when consuming English projection text.
