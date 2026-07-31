# JobHunter Architecture

## 1. Architectural direction

JobHunter is a **local modular monolith** written in Python 3.12 or newer.

It is one local application with explicit internal boundaries for configuration,
search planning, source acquisition, evidence preservation, persistence,
deterministic parsing, local inference, analysis, and reporting. Components are
separated when they have a current operational responsibility; speculative
microservices and empty abstraction layers are not introduced.

The command-line interface is the current interaction surface. A local web
interface remains optional and must be justified by concrete review or workflow
friction.

## 2. Permanent architectural principles

1. Preserve raw evidence before parsing or interpretation.
2. Keep successful acquisition independent from LM Studio availability.
3. Separate deterministic processing from model-dependent processing.
4. Keep source-specific behavior in explicit adapters and services.
5. Keep CLI handlers as composition and validation code, not parsing or SQL code.
6. Use SQLite as the local system of record.
7. Keep source evidence inspectable outside normalized database records.
8. Design repeated operations for idempotency.
9. Keep semantic versions separate from volatile HTTP responses.
10. Keep operational fetch history separate from semantic versions.
11. Prefer missing or review-required states over fabricated values.
12. Treat acquired content as untrusted data, never executable instruction.
13. Bound pages, requests, detail batches, retries, and model calls.
14. Make configuration and policy visible rather than scattering constants.
15. Add complexity only when an observed product need justifies it.

## 3. Current acquisition flow

```text
TOML configuration or explicit CLI selectors
                ↓
Bilingual search registry expansion
                ↓
Canonical raw-URL and keyword-generated search plan
                ↓
Search limit, offset, page limit, and global request budget
                ↓
Sequential Jobinja search-page acquisition
                ↓
Immutable search-page HTML and metadata evidence
                ↓
Canonical Jobinja job-code discovery
                ↓
Repeat-safe JobPosting and discovery provenance
                ↓
Missing-detail and refresh-due selection
                ↓
Sequential Jobinja detail-page acquisition
                ↓
Immutable detail HTML and metadata evidence
                ↓
Deterministic Jobinja parser v2
                ↓
Semantic content fingerprint and version decision
                ↓
Fetch observation: new_version / unchanged / failed
                ↓
Deterministic structural parser audit
```

The current `jobhunter jobinja sync` command implements this acquisition-only
flow. It deliberately stops before LM Studio analysis.

## 4. Intended complete Phase 1 flow

```text
Accepted acquisition and posting versions
                ↓
Pending-analysis selection
                ↓
Versioned local-model prompt and schema
                ↓
LM Studio provider boundary
                ↓
Raw request and response evidence
                ↓
Schema and evidence validation
                ↓
Accepted / review-required / failed analysis state
                ↓
Individual job result
                ↓
Combined responsibility, requirement, and role report
```

A failure in any later stage must not invalidate evidence or records produced by
an earlier successful stage.

## 5. Runtime components

### 5.1 CLI composition layer

Current commands include:

```text
jobhunter init
jobhunter doctor [--smoke]

jobhunter jobinja catalog
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch

jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
```

The CLI:

- parses and validates arguments;
- loads typed settings;
- resolves configured or explicit search selectors;
- assembles application services;
- prints human-readable summaries;
- maps controlled findings and failures to exit statuses.

It does not contain HTML extraction or direct SQL.

### 5.2 Typed configuration

`config.py` loads TOML and selected `JOBHUNTER_*` environment overrides through
Pydantic models.

Current configuration covers:

- local data, evidence, and SQLite paths;
- LM Studio provider settings;
- Jobinja user agent, timeout, and request delay;
- raw Jobinja search URLs;
- built-in bilingual profiles and packs;
- custom bilingual keyword groups;
- excluded terms;
- default pages per generated keyword search;
- maximum expanded searches;
- global search-page request budget;
- sync missing and refresh limits;
- refresh age threshold;
- logging level.

Unknown fields are rejected. Raw search URLs are canonicalized during validation.
Pack and profile identifiers are validated before network use.

### 5.3 Bilingual search registry

`search_registry.py` owns curated search vocabulary and deterministic expansion.

Responsibilities:

- define stable built-in pack and profile identifiers;
- preserve Persian and English display terms;
- normalize term identity for deduplication;
- generate canonical Jobinja keyword-filter URLs;
- combine profiles, packs, custom groups, and one-off terms;
- apply normalized exclusions;
- produce inspectable search names containing origin, term, and stable digest;
- expose catalog and planning output.

Search vocabulary is source acquisition configuration. It must not be confused
with a later canonical career taxonomy.

### 5.4 Search-plan controls

The CLI applies deterministic controls after expansion:

- canonical URL deduplication;
- optional page override;
- cyclic search offset;
- maximum selected searches;
- global request budget.

`--search-offset` and `--search-limit` allow a large catalog to be covered in
stable windows. The global request budget is enforced again in the discovery
service so CLI mistakes cannot create unbounded requests.

### 5.5 Jobinja source adapter

`sources/jobinja.py` owns Jobinja URL and HTTP rules.

Responsibilities:

- validate approved Jobinja hosts;
- canonicalize search and job URLs;
- generate bounded pagination URLs;
- fetch public search and job pages with HTTPX;
- follow redirects while validating final host and path;
- enforce supported content type and response-size bounds;
- use a descriptive user agent and Persian/English accept language;
- extract stable source job codes and company slugs;
- deduplicate repeated links within a search page.

The adapter does not write evidence, persist records, or invoke a model.

### 5.6 Evidence store

`evidence.py` writes raw response bytes and metadata sidecars before downstream
parsing.

Current layouts:

```text
data/evidence/jobinja/search-pages/<search>/...
data/evidence/jobinja/job-pages/<job-id>/...
```

Metadata includes:

- source and evidence kind;
- search or job identity;
- requested and final URLs;
- capture time;
- selected HTTP headers;
- status code;
- SHA-256 content hash;
- byte count;
- raw content path.

Writes use temporary files followed by atomic replacement. Partial evidence
pairs are not silently retained.

### 5.7 Discovery orchestration

`jobinja_discovery.py` coordinates:

```text
validated searches
→ sequential bounded fetch
→ evidence write
→ deterministic link extraction
→ job upsert
→ discovery provenance
→ per-search and combined summary
```

Stop reasons are explicit:

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
page_failed
invalid_search
```

Repeated result pages are identified by sorted stable source job IDs rather than
volatile HTML. One search failure does not discard successful searches.

### 5.8 Detail acquisition service

`jobinja_detail_service.py` owns one-job detail acquisition.

Responsibilities:

- resolve an existing JobPosting;
- acquire the public detail page;
- write immutable evidence before parsing;
- parse deterministic source fields;
- calculate a semantic fingerprint;
- insert a semantic version only when content changed;
- record every successful or expected failed fetch observation;
- return an inspectable summary.

The detail service does not perform relevance or career analysis.

### 5.9 Bounded batch acquisition

`jobinja_batch.py` performs sequential detail checks for up to 50 unique job IDs.

It:

- preserves input order;
- removes duplicate IDs;
- applies the configured delay between requests;
- isolates expected failures by job;
- reports new semantic versions, unchanged checks, and failures;
- exposes version and observation IDs.

### 5.10 Fetch observations and refresh scheduling

`job_detail_observations.py` stores operational detail-check history separately
from versions.

A successful observation can reference:

- check timestamp;
- new-version or unchanged outcome;
- requested and final URLs;
- HTTP status;
- exact raw-response hash;
- semantic hash and version ID;
- parser version and parse status;
- evidence paths.

A failed observation stores the timestamp, requested URL, error type, and error
message without deleting earlier successful data.

Refresh-due selection:

1. considers only jobs with a local semantic detail version;
2. uses the latest fetch-observation timestamp;
3. falls back to the latest version timestamp for legacy data;
4. applies a configurable age threshold;
5. returns a bounded ordered selection.

No single failed check changes lifecycle state.

### 5.11 Deterministic Jobinja parser

`jobinja_details.py` implements parser version `jobinja-detail-v2`.

It extracts explicit Jobinja fields and structured `JobPosting` metadata while
preferring visible source labels where they are more useful.

Current fields include:

- title;
- company;
- category;
- location;
- employment type;
- minimum experience;
- education;
- salary display;
- gender;
- military-service requirement;
- source skill tags;
- complete job description;
- company description;
- publication and validity dates;
- language classification.

Missing fields remain missing. Dedicated Jobinja skill tags remain separate from
skills later inferred from description text.

### 5.12 Semantic versions

`storage.py` stores semantic detail versions in SQLite.

Version identity is based on canonical JSON of deterministic source fields,
excluding parser-only metadata such as language classification and parser
version. This prevents volatile HTML tokens or rendering changes from creating
false content versions.

Each semantic version retains the raw evidence that first defined it. Later
unchanged checks receive their own raw snapshots and observations.

### 5.13 Local catalog and inspection

`job_catalog.py` provides read-only listing and missing-detail selection.

`jobs show` displays the latest semantic version and its version-defining
evidence. `jobs checks` displays operational fetch history. These views are
intentionally separate.

### 5.14 Structural parser audit

`job_audit.py` checks latest local semantic versions without network or model
calls.

It detects known structural risks such as:

- missing required title or description;
- partial or failed parse status;
- outdated parser version;
- non-scalar values in scalar fields;
- obvious page-interface contamination;
- mapping representations accidentally stored as text;
- implausibly long scalar values or skill tags.

Optional-field absence is reported as coverage, not automatically as failure.
The audit does not claim semantic interpretation correctness.

### 5.15 Acquisition sync

`jobinja_sync.py` composes accepted acquisition services:

```text
discovery
→ bounded missing-detail selection
→ bounded refresh-due selection
→ one sequential detail batch
→ latest-corpus parser audit
```

The combined missing and refresh limits may not exceed 50. The sync returns an
attention-required status when discovery or detail failures occur, or when the
audit finds structural issues.

### 5.16 Inference-provider boundary

LM Studio remains behind `inference/`.

Provider responsibilities include:

- connectivity and model discovery;
- bounded timeout and retries;
- structured-output requests;
- response diagnostics;
- exact model identity reporting.

No acquisition component imports or calls LM Studio. P1.6 will add versioned
analysis schemas, prompt evidence, raw responses, local validation, and review
states.

## 6. SQLite record model

Current records include:

```text
source_searches
acquisition_runs
search_page_snapshots
job_postings
job_discoveries
job_detail_versions
job_detail_fetch_observations
```

Important distinctions:

```text
job_postings
  logical source identity

job_discoveries
  where and when that identity appeared

job_detail_versions
  meaningful deterministic content history

job_detail_fetch_observations
  every successful or failed operational check

raw evidence files
  exact HTTP response bytes and metadata
```

SQLite is accessed through focused repository boundaries using the standard
`sqlite3` module. A general Object-Relational Mapper remains unnecessary.
Migration tooling must be introduced before an incompatible production schema
change, not merely because more tables now exist.

## 7. Current repository structure

```text
src/jobhunter/
  cli.py
  config.py
  doctor.py
  evidence.py
  job_audit.py
  job_catalog.py
  job_detail_observations.py
  jobinja_batch.py
  jobinja_detail_service.py
  jobinja_details.py
  jobinja_discovery.py
  jobinja_sync.py
  search_registry.py
  storage.py
  inference/
  sources/
    jobinja.py
```

The structure expands by active responsibility rather than by speculative
future layers.

## 8. Testing strategy

Normal tests do not contact Jobinja or require LM Studio.

Deterministic coverage includes:

- URL validation and canonicalization;
- bilingual term normalization and deduplication;
- profile, pack, group, exclusion, and URL expansion;
- configuration validation;
- search-plan limits and CLI validation;
- global request-budget behavior;
- repeated-page and empty-page stopping;
- cross-search identity overlap;
- raw evidence writing;
- repeat-safe job identity;
- parser extraction and contamination regression cases;
- semantic version identity;
- unchanged-check observations;
- failure observations;
- refresh-due selection and legacy fallback;
- batch isolation;
- acquisition-sync composition;
- local structural audit.

Live Jobinja runs remain explicit acceptance probes after deterministic tests
pass.

## 9. Security boundaries

- Use public Jobinja pages only.
- Do not automate login or applications.
- Do not store Jobinja credentials or cookies.
- Do not bypass CAPTCHA, blocking, authentication, or access controls.
- Do not use stealth proxy rotation.
- Validate final redirect hosts and paths.
- Enforce page, request, response-size, batch, timeout, and delay bounds.
- Never execute acquired scripts.
- Treat all page content as untrusted prompt data.
- Do not grant the future extraction model shell, filesystem, browser, or
  unrestricted network tools.
- Keep local runtime data, evidence, personal data, and model files outside Git.

## 10. Current architectural stop line

The current system can configure broad bilingual searches, plan them, discover
jobs repeat-safely, preserve evidence, fetch missing or refresh-due details,
parse source fields, version meaningful changes, retain every check, and audit
structural quality.

It must not yet infer or claim:

- role purpose;
- responsibilities;
- required versus preferred qualifications;
- description-derived skills;
- personal relevance;
- capability gaps;
- application readiness;
- career recommendations;
- aggregate market conclusions.

Those require the versioned, evidence-backed local analysis boundary defined for
P1.6 and P1.7.
