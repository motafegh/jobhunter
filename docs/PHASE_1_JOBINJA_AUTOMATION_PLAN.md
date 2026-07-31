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
→ open individual advertisements
→ copy descriptions and skills into files
→ send files to an AI assistant
→ request individual and combined analysis
```

The target system must configure searches once, preserve evidence, identify new
and changed jobs, parse explicit source fields, run local evidence-backed
analysis, and produce inspectable individual and combined results.

## 3. Target daily experience

The intended final Phase 1 endpoint is:

```bash
jobhunter run
```

A complete run will eventually:

1. load enabled bilingual profiles, packs, custom groups, and raw URLs;
2. build an inspectable bounded search plan;
3. acquire search pages sequentially and preserve evidence;
4. discover stable Jobinja job identities repeat-safely;
5. select missing and refresh-due job details;
6. preserve raw detail evidence;
7. parse explicit Jobinja fields deterministically;
8. classify semantic content as new, unchanged, or changed;
9. retain every successful or failed fetch observation;
10. queue new or changed versions for local analysis;
11. validate evidence-backed structured model output;
12. persist individual results and review states;
13. update a combined report;
14. print a concise actionable summary.

The system must not require manual copying of individual job URLs or text.

## 4. Phase 1 data flow

```text
Bilingual search configuration
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
Semantic version decision
        ↓
Fetch observation
        ↓
Local LLM structured analysis
        ↓
Validation and review state
        ↓
Individual and combined outputs
```

Acquisition must remain useful when LM Studio is unavailable.

## 5. Source configuration

### 5.1 Built-in profiles and packs

JobHunter supports version-controlled bilingual search vocabulary:

```toml
jobinja_search_profiles = ["ai-security-python"]
jobinja_search_packs = ["ai-security"]
```

Built-in vocabulary is a starting point, not hidden relevance policy.

### 5.2 Custom keyword groups

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

### 5.3 Raw Jobinja URLs

Raw result URLs remain supported for source-owned filters:

```toml
[[jobhunter.jobinja_searches]]
name = "Remote AI roles"
url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
enabled = true
max_pages = 2
```

### 5.4 Normalization and exclusions

Term comparison may normalize Unicode, Persian/Arabic character variants,
whitespace, case, and zero-width joiners. The displayed original term remains
visible. Exclusions apply after normalization.

### 5.5 Bounds

Search configuration must support:

- maximum pages per search;
- maximum selected searches;
- cyclic search offset;
- global search-page request budget;
- sequential request delay;
- explicit one-run CLI selectors.

Budget exhaustion is a controlled stop, not a failure.

## 6. Source boundaries and safety

Phase 1 will:

- use public Jobinja search and detail pages only;
- operate for personal local use;
- preserve source attribution and canonical URLs;
- use a descriptive user agent;
- use sequential rate-limited requests;
- enforce page, request, response-size, and batch limits;
- validate redirects and approved hosts;
- retain raw evidence locally;
- report access denial, challenge, CAPTCHA, login, or unsupported pages.

Phase 1 will not:

- automate login or applications;
- scrape private profiles or resumes;
- bypass CAPTCHA, blocking, authentication, or access controls;
- use stealth proxy rotation;
- create an unrestricted generic crawler;
- redistribute collected advertisements publicly;
- add another platform before Jobinja is stable and useful.

## 7. Source-specific identity

Observed job URLs follow:

```text
/companies/{company-slug}/jobs/{job-code}/{title-slug}
```

The source job code is the primary external identity. Canonicalization must:

- normalize host to `jobinja.ir`;
- prefer HTTPS;
- remove tracking query parameters and fragments;
- preserve the meaningful job path;
- extract company slug and source job code;
- reject unsupported hosts and paths.

The title slug is descriptive, not stable identity.

## 8. Language handling

Jobinja advertisements may be Persian, English, or mixed.

Phase 1 must preserve:

- exact original evidence;
- detected language classification;
- normalized analysis text;
- English technical terms embedded in Persian text;
- any translation as a separately labelled derived artifact.

Normalization must never overwrite raw evidence.

## 9. Deterministic extraction boundary

Explicit Jobinja fields should be extracted by deterministic code when present:

- title;
- company;
- category;
- location;
- employment type;
- minimum experience;
- salary display;
- source skill tags;
- education;
- gender;
- military-service requirement;
- publication and validity indicators;
- company metadata;
- complete job description.

The LLM interprets free text. It must not rediscover fields already labelled by
Jobinja. Source skill tags remain separate from description-derived skills.

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

- run, search, and page;
- requested and final URLs;
- retrieval time;
- HTTP status and selected headers;
- content hash;
- evidence paths;
- discovered count.

### JobPosting

- source and source job code;
- canonical URL and company slug;
- first and last seen times;
- lifecycle state;
- latest known version reference.

### JobDiscovery

- run;
- search and page;
- job posting;
- discovery timestamp.

### JobPostingVersion

- posting reference;
- retrieval time;
- version-defining evidence;
- deterministic fields;
- semantic fingerprint;
- parser and language metadata.

### JobDetailFetchObservation

- posting reference;
- check timestamp;
- new-version, unchanged, or failed outcome;
- requested and final URLs when available;
- HTTP status and raw-response hash when available;
- semantic hash and version reference when available;
- parser version and parse status when available;
- evidence paths for successful checks;
- error type and message for failures.

Fetch observations are operational history and remain separate from semantic
versions and raw snapshots.

### AnalysisRun

- posting version;
- model, prompt, and schema versions;
- request and raw response evidence;
- validated structured result;
- success, failure, or review state.

### DailyReport

- run and corpus window;
- new, changed, unchanged, failed, and analysed counts;
- relevant jobs requiring attention;
- repeated responsibilities and skills;
- conclusions and uncertainty notes.

## 11. Processing states

Successful progression:

```text
discovered
→ acquired
→ parsed
→ pending_analysis
→ analysed
→ review_required or accepted
```

Failure and lifecycle states remain explicit:

```text
acquisition_failed
parse_failed
analysis_failed
inaccessible
expired
removed
unknown
```

A later-stage failure must not delete earlier successful evidence.

## 12. Delivery increments

### P1.0 — Repository alignment

Accepted when the controlling documents and implementation live on `main` and
the next target is unambiguous.

### P1.1 — Discovery foundation

Deliverables:

- validated search URL configuration;
- Jobinja URL canonicalization;
- sequential search-page fetcher;
- raw search-page evidence;
- link extraction and deduplication;
- initial SQLite records;
- `jobhunter jobinja discover`.

Accepted.

### P1.2 — Pagination and repeat-safe discovery

Deliverables:

- bounded pagination;
- empty, repeated, invalid, budget, and maximum stop conditions;
- multiple searches;
- cross-search deduplication and provenance;
- per-search summaries;
- repeat-safe runs.

Accepted through live repeated two-search, two-page validation.

### P1.3 — Detail acquisition and evidence

Deliverables:

- bounded explicit, missing, and refresh-due queues;
- raw detail evidence;
- persistent successful and failed observations;
- challenge, login, error, expired, and irrelevant-page detection;
- retry rules;
- inspectable check history.

Operational core accepted. Source-page classification and refined retry policy
remain incomplete.

### P1.4 — Deterministic parser and normalization

Deliverables:

- source-specific parser;
- complete description preservation;
- original and normalized text;
- Persian/Arabic normalization;
- language classification;
- structural validation report;
- Persian, English, mixed, active, and expired fixtures.

Parser v2 is accepted against fifteen varied live advertisements. Expired and
special-page fixtures remain incomplete.

### P1.5 — Identity, versions, and lifecycle

Deliverables:

- semantic fingerprints;
- new, unchanged, changed, reposted, and duplicate classifications;
- version persistence;
- first-seen, last-seen, last-checked, and last-successful-fetch tracking;
- cautious expiration/removal detection;
- inspection commands.

Semantic versions and fetch observations are implemented. Repost, duplicate,
and lifecycle classification remain incomplete.

### P1.6 — Evidence-backed local analysis

Deliverables:

- versioned analysis schema;
- role purpose, responsibilities, required and preferred qualifications, tools,
  knowledge, experience, constraints, and evidence passages;
- Persian, English, and mixed prompt handling;
- validated structured output;
- bounded retries and diagnostics;
- pending, failed, review-required, and accepted states;
- reanalysis by model or prompt version;
- manually reviewed golden corpus.

Acceptance requires evidence for every material claim and measured model quality.

### P1.7 — Individual outputs and combined report

Deliverables:

- inspectable individual report;
- Markdown and JSON exports;
- combined responsibility, skill, role, experience, and requirement counts;
- required-versus-preferred separation;
- filters;
- initial relevance classification;
- concise daily report;
- final `jobhunter run` orchestration.

## 13. Phase completion criteria

Phase 1 is complete only when:

1. searches are configured once;
2. a normal run discovers jobs automatically;
3. pagination and budgets are bounded and observable;
4. new and changed jobs preserve immutable evidence;
5. explicit Jobinja fields parse deterministically;
6. Persian, English, and mixed content remain intact;
7. local analysis produces evidence-backed structured results;
8. model and parser failures remain inspectable and retryable;
9. individual and combined reports exist;
10. reruns do not duplicate unchanged jobs or inflate analysis;
11. no access-control bypass or application automation is required;
12. the result is materially more useful than the manual workflow.

## 14. Deferred work

Outside Phase 1 unless required for completion:

- other job platforms;
- generic crawling;
- automated applications and recruiter messaging;
- resume tailoring and submission;
- full personal capability graph;
- long-term trend analysis;
- salary or hiring-probability prediction;
- mobile or browser-extension interfaces;
- distributed services;
- model fine-tuning;
- vector databases without demonstrated need.

## 15. Current authorized implementation

Accepted evidence:

- M0, P1.1, and P1.2;
- 79 unique jobs across two two-page searches with one overlap;
- zero new jobs on the identical discovery rerun;
- fifteen complete parser-v2 advertisements;
- fifteen of fifteen latest versions structurally clean;
- unchanged checks creating observations without false versions;
- bounded refresh-due selection.

Current target: **configurable bilingual search planning and acquisition-only
synchronization**.

```text
profiles + packs + custom Persian/English groups + raw URLs
→ normalized deduplication and exclusions
→ inspectable plan
→ search limit + offset + pages + global request budget
→ repeat-safe discovery
→ bounded missing and refresh-due details
→ evidence + parsing + semantic versioning + observations
→ structural audit
→ acquisition sync summary
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

Acceptance requires deterministic tests and bounded live validation. Acquisition
must remain independent from LM Studio.

After acceptance, the next target is challenge/login/irrelevant/expired-page
classification, retry policy, and cautious lifecycle transitions. P1.6 must not
begin until acquisition failures are sufficiently classified to protect the
analysis corpus.
