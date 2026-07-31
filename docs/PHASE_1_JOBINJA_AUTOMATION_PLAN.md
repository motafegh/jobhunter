# Phase 1 — Jobinja Workflow Automation Plan

## 1. Status and authority

**Status:** Active implementation plan  
**Scope:** Phase 1 only  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Repository branch policy for this phase:** Work directly on `main` unless a later change creates a clear need for isolation.

This document controls the implementation sequence and completion criteria for Phase 1. The broader product direction remains defined by the product specification, architecture, domain model, and source policy.

## 2. Phase objective

Phase 1 must replace and improve the user's current manual Jobinja workflow.

Today the user:

1. opens Jobinja;
2. searches for keywords or exact positions;
3. reviews the result list;
4. opens relevant advertisements;
5. copies skills, responsibilities, and related sections;
6. places one or several advertisements into files;
7. sends those files to an AI assistant;
8. requests individual and combined career analysis.

At the end of Phase 1, JobHunter must automate that flow for configured Jobinja searches while preserving source evidence and keeping the user able to inspect and correct results.

## 3. Target daily experience

The intended final Phase 1 command is:

```bash
jobhunter run
```

A successful run will:

1. load enabled Jobinja search definitions;
2. execute each search and follow its bounded pagination;
3. discover matching job advertisements;
4. identify new, unchanged, changed, inaccessible, and expired candidates;
5. fetch new or refresh-due job pages;
6. preserve raw search and job-detail HTML plus acquisition metadata;
7. deterministically extract Jobinja's known fields;
8. preserve Persian, English, and mixed-language source text;
9. queue new or changed postings for local analysis;
10. obtain evidence-backed structured analysis through the configured local model;
11. persist individual results and failure states;
12. update a combined Phase 1 career report;
13. print a concise run summary with actionable failures.

The system must not require manual copying of individual job URLs or advertisement text.

## 4. Phase 1 data flow

```text
Saved Jobinja searches
        ↓
Search-page acquisition
        ↓
Raw search-page evidence
        ↓
Result-link discovery and canonicalization
        ↓
Job identity and discovery persistence
        ↓
New / known / refresh-due decision
        ↓
Job-detail acquisition
        ↓
Raw job-page evidence
        ↓
Deterministic Jobinja field extraction
        ↓
Original-language normalized job document
        ↓
New / unchanged / changed version decision
        ↓
Local LLM structured analysis
        ↓
Validation and review state
        ↓
Individual job result
        ↓
Combined responsibility, skill, and role analysis
        ↓
Daily report and exports
```

Acquisition must continue to work when LM Studio is unavailable. Such postings remain safely stored in `pending_analysis` or `analysis_failed` state and can be processed later.

## 5. Source configuration

A Jobinja search is configured once, not once per job.

The first supported configuration form is a saved Jobinja result URL:

```toml
[[jobhunter.jobinja_searches]]
name = "Artificial intelligence roles"
url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
enabled = true
max_pages = 3
```

JobHunter then discovers all individual advertisement links from the result pages automatically.

A later Phase 1 increment may allow keywords and filters to be entered directly in JobHunter and converted into a Jobinja search URL. Saved result URLs remain the initial reliable interface because they preserve Jobinja's own filter semantics.

## 6. Source boundaries and safety

Phase 1 will:

- use only public Jobinja search and job-detail pages;
- operate for personal, local use;
- preserve Jobinja attribution and canonical source URLs;
- use a descriptive user agent;
- use sequential, rate-limited requests by default;
- enforce configurable page and request limits;
- validate redirects and remain on approved Jobinja hosts;
- stop and report access-denial, challenge, CAPTCHA, or login pages;
- retain raw evidence locally;
- support disabling any search without code changes.

Phase 1 will not:

- automate login;
- automate job applications;
- scrape private profiles or resumes;
- bypass CAPTCHA, blocking, authentication, or access controls;
- create an unrestricted generic crawler;
- redistribute collected advertisements publicly;
- add another job platform before the Jobinja workflow is useful and stable.

## 7. Source-specific identity rules

Observed Jobinja job URLs follow this shape:

```text
/companies/{company-slug}/jobs/{job-code}/{title-slug}
```

The source job code is the primary external identity for Phase 1.

Canonicalization must:

- normalize the host to `jobinja.ir`;
- prefer HTTPS;
- remove query parameters such as `_ref` and `_t`;
- remove fragments;
- preserve the meaningful job path;
- extract `company_slug` and `source_job_code`;
- reject non-Jobinja and non-job URLs.

The title slug is descriptive and must not be treated as the stable identity.

## 8. Language handling

Jobinja advertisements may be Persian, English, or mixed.

Phase 1 must preserve:

- the exact original text as evidence;
- the detected language classification;
- a normalized analysis copy;
- any later translation as a separately labelled derived artifact.

Normalization may standardize Persian and Arabic character variants, digits, whitespace, and zero-width characters for matching. It must never overwrite the original evidence.

English technical terms embedded in Persian text must remain intact.

## 9. Deterministic extraction boundary

Jobinja's explicitly labelled fields must be extracted by normal code whenever present, including:

- title;
- company;
- job category;
- location;
- employment/cooperation type;
- minimum experience;
- salary display;
- required-skill tags;
- education;
- gender requirement;
- military-service requirement;
- publication/expiration indicators;
- company metadata;
- complete free-text job description.

The LLM is responsible for interpreting the free-text content, not for rediscovering fields already labelled by Jobinja.

Dedicated Jobinja skill tags and skills inferred from the description must remain separate source categories.

## 10. Phase 1 records

The implementation should introduce only the records needed for this workflow.

### SearchDefinition

- source;
- user-defined name;
- search URL;
- enabled state;
- maximum pages;
- request delay or inherited default;
- created and updated timestamps.

### AcquisitionRun

- run identifier;
- start and completion timestamps;
- status;
- configured searches;
- page, job, and error counts;
- failure summary.

### SearchPageSnapshot

- search and page number;
- requested and final URLs;
- retrieval time;
- HTTP status and selected headers;
- content hash;
- raw evidence path;
- discovered job count.

### JobPosting

- source and source job code;
- canonical URL;
- company slug;
- first and last seen times;
- current lifecycle state;
- latest known version reference.

### JobPostingVersion

- posting reference;
- retrieval time;
- raw evidence reference;
- deterministic fields;
- normalized content hash;
- version classification;
- language metadata.

### JobDetailFetchObservation

- posting reference;
- check timestamp;
- new-version, unchanged, or failed outcome;
- requested and final URLs when available;
- HTTP status and exact raw-response hash when available;
- semantic hash and semantic-version reference when available;
- parser version and parse status when available;
- raw evidence paths for successful checks;
- error type and message for failed checks.

A fetch observation is operational history. It must remain separate from semantic versions and raw snapshots so repeated unchanged checks are visible without creating false content versions.

### AnalysisRun

- posting version;
- model and prompt versions;
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

A posting may move through these states:

```text
discovered
→ acquired
→ parsed
→ pending_analysis
→ analysed
→ review_required
→ accepted
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

A failure in a later stage must not delete or invalidate evidence from an earlier successful stage.

## 12. Delivery increments

### P1.0 — Repository alignment and controlling plan

Deliverables:

- M0 consolidated into `main`;
- this Phase 1 plan;
- repository entry points updated;
- acquisition-first implementation order established.

Acceptance:

- `main` contains the complete current implementation;
- no active implementation depends on the temporary M0 branch;
- the next build target is unambiguous.

### P1.1 — Jobinja discovery foundation

Goal: turn one configured or command-line Jobinja search URL into persisted discovered job identities.

Deliverables:

- validated Jobinja search configuration;
- source-specific URL canonicalization;
- sequential HTTP search-page fetcher;
- raw search-page HTML and metadata evidence;
- extraction and deduplication of job links;
- initial SQLite acquisition and discovery tables;
- `jobhunter jobinja discover` command;
- bounded page count and request delay;
- deterministic fixtures and tests.

Acceptance:

- one search URL is fetched without LM Studio;
- job codes and canonical URLs are discovered automatically;
- duplicate links on a page produce one source identity;
- raw HTML is saved before parsing;
- rerunning records known jobs without creating duplicate JobPosting rows;
- non-Jobinja URLs and off-domain redirects are rejected;
- command output reports searches, pages, unique jobs, new jobs, known jobs, and failures.

Stop line:

- do not fetch every job-detail page or invoke the LLM during P1.1.

### P1.2 — Pagination and repeat-safe daily discovery

Deliverables:

- automatic bounded pagination;
- stop conditions for empty, repeated, invalid, or maximum pages;
- multiple enabled saved searches;
- cross-search discovery deduplication;
- acquisition-run completion and failure recording;
- search disablement through configuration;
- clear per-search summaries.

Acceptance:

- one job found by several searches remains one JobPosting;
- all matching searches are retained as discovery evidence;
- one search failure does not discard successful searches;
- repeated runs are idempotent.

### P1.3 — Job-detail acquisition and immutable evidence

Deliverables:

- bounded job-detail fetch queue;
- new and refresh-due selection;
- raw detail HTML and metadata snapshots;
- persistent observation of every successful or expected failed check;
- challenge, login, error, expired, and irrelevant page detection;
- acquisition retry rules;
- inspectable evidence and check-history paths;
- detail-acquisition CLI support.

Acceptance:

- newly discovered jobs can be fetched automatically;
- raw content is written before parsing;
- unchanged semantic content does not create false versions;
- unchanged checks still create inspectable operational observations;
- refresh-due selection uses the latest known check and remains bounded;
- failures remain retryable without losing discovery or earlier detail data.

### P1.4 — Jobinja field parser and language normalization

Deliverables:

- source-specific field parser;
- complete description preservation;
- original and normalized text;
- Persian/Arabic character normalization;
- language classification;
- deterministic field-validation report;
- representative Persian, English, mixed, active, and expired fixtures.

Acceptance:

- known labelled fields are extracted without LLM inference;
- similar-job cards, navigation, login prompts, and footer content are excluded;
- missing fields remain missing rather than guessed;
- source text is never overwritten by normalized or translated text.

### P1.5 — Posting identity, versions, and lifecycle

Deliverables:

- normalized content fingerprints;
- new, unchanged, changed, reposted, and duplicate classifications;
- JobPostingVersion persistence;
- first-seen, last-seen, last-checked, and last-successful-fetch tracking;
- cautious expiration/removal detection;
- inspection commands.

Acceptance:

- changed advertisements create versions instead of overwriting history;
- disappearance from one search is not sufficient to mark a job expired;
- duplicate postings do not inflate later analysis.

### P1.6 — Evidence-backed local analysis

Deliverables:

- versioned job-analysis schema;
- local-model extraction of role purpose, responsibilities, required and preferred qualifications, tools, knowledge, experience, constraints, and evidence passages;
- Persian, English, and mixed-language prompt handling;
- validated structured output;
- bounded retries and diagnostic evidence;
- pending, failed, review-required, and accepted states;
- reanalysis by model or prompt version;
- initial manually reviewed golden corpus.

Acceptance:

- every material extracted claim includes source evidence;
- explicit requirements remain distinct from preferred and inferred capabilities;
- malformed output does not corrupt accepted data;
- acquisition continues when the model is unavailable;
- model quality is measured on real Jobinja examples.

### P1.7 — Individual outputs and combined Phase 1 report

Deliverables:

- inspectable individual job report;
- Markdown and JSON exports;
- combined counts for responsibilities, skills, role families, experience, and requirements;
- required versus preferred separation;
- filters by search, date, language, company, location, and status;
- initial user relevance classification;
- concise daily run report;
- `jobhunter run` orchestration.

Acceptance:

- the user no longer manually copies job advertisements into files for analysis;
- every aggregate conclusion can list supporting postings;
- unchanged and duplicate postings do not inflate counts;
- individual and combined results preserve links to original evidence;
- the daily report identifies jobs and analysis failures that require attention.

## 13. Phase completion criteria

Phase 1 is complete only when all of the following are true:

1. The user configures Jobinja searches once.
2. A normal run discovers individual advertisements automatically.
3. Pagination is bounded, observable, and repeat-safe.
4. New and changed advertisements are preserved as immutable evidence.
5. Jobinja's known fields are parsed deterministically.
6. Persian, English, and mixed text are preserved correctly.
7. Local analysis produces evidence-backed structured results.
8. Model or parser failures remain inspectable and retryable.
9. Individual job reports and a combined report are produced.
10. Rerunning does not duplicate unchanged jobs or inflate analysis.
11. No login, CAPTCHA bypass, private-data scraping, or application automation is required.
12. The automated result is materially more useful than the previous manual file-and-AI workflow.

## 14. Deferred work

The following remain outside Phase 1 unless strictly necessary to complete the workflow:

- other job platforms;
- generic crawling;
- automated applications;
- resume tailoring and submission;
- full personal capability evidence graph;
- deep roadmap modification;
- market trend analysis over long periods;
- salary prediction;
- hiring-probability prediction;
- mobile or browser-extension interfaces;
- distributed services;
- model fine-tuning;
- embeddings or vector databases without demonstrated need.

## 15. Current authorized implementation

M0, P1.1, and P1.2 are accepted. Repeat-safe discovery was validated live across two two-page Jobinja searches with 79 unique jobs, one cross-search overlap, and zero new jobs on the identical rerun.

A bounded parser-v2 slice spanning parts of P1.3 and P1.4 is accepted against fifteen structurally varied live Jobinja advertisements. All fifteen latest semantic versions pass the deterministic local structural audit.

The current implementation and live acceptance target is the operational core of **P1.3 — job-detail acquisition and immutable evidence**.

The active P1.3 path is:

```text
explicit, missing-only, or refresh-due bounded selection
→ sequential rate-limited detail requests
→ immutable raw detail evidence
→ deterministic parser-v2 extraction
→ semantic new / unchanged decision
→ persistent successful or failed fetch observation
→ inspectable per-job check history
→ bounded refresh scheduling
```

P1.3 must:

- preserve semantic versions, raw HTTP snapshots, and fetch observations as distinct records;
- record every successful check even when content is unchanged;
- record expected acquisition and evidence-write failures without deleting prior data;
- select refresh-due jobs only when a local detail version exists;
- use the latest observation timestamp and a semantic-version fallback for legacy data;
- remain sequential, bounded to 50 jobs, user-controlled, and independent from LM Studio;
- avoid lifecycle conclusions from one failure or one search disappearance.

The active commands are:

```text
jobhunter jobinja fetch <job-id> [<job-id> ...]
jobhunter jobinja fetch --missing --limit <count>
jobhunter jobinja fetch --refresh-due --older-than-hours <hours> --limit <count>
jobhunter jobs checks <job-id> [--limit <count>]
```

Challenge/login classification, retry-backoff refinement, expired and irrelevant page classification, and full lifecycle decisions remain incomplete. Local LLM interpretation, individual analysis, combined reports, personal relevance, career recommendations, and `jobhunter run` remain outside the active increment.
