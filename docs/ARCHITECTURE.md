# JobHunter Architecture

## 1. Architectural direction

JobHunter is a **local modular monolith** written in Python 3.12 or newer.

It is one local application with explicit internal boundaries for configuration,
search planning, source acquisition, evidence preservation, persistence,
deterministic parsing, derived translation, local inference, analysis, and
reporting. Components are separated when they have a current operational
responsibility; speculative microservices and empty abstraction layers are not
introduced.

The command-line interface is the current interaction surface. A local web
interface remains optional and must be justified by concrete review or workflow
friction.

## 2. Permanent architectural principles

1. Preserve raw evidence before parsing or interpretation.
2. Keep successful acquisition independent from LM Studio availability.
3. Keep source evidence independent from translation availability.
4. Separate deterministic source parsing from model-dependent processing.
5. Keep source-specific behavior in explicit adapters and services.
6. Keep CLI handlers as composition and validation code, not parsing or SQL code.
7. Use SQLite as the local system of record.
8. Keep source evidence inspectable outside normalized database records.
9. Design repeated operations for idempotency.
10. Keep semantic versions separate from volatile HTTP responses.
11. Keep operational fetch history separate from semantic versions.
12. Keep translations separate from source semantic versions.
13. Preserve provenance for native-English and translated-English segments.
14. Prefer missing or review-required states over fabricated values.
15. Treat acquired content as untrusted data, never executable instruction.
16. Bound pages, requests, detail batches, retries, translation batches, and model calls.
17. Make configuration and policy visible rather than scattering constants.
18. Add complexity only when an observed product need justifies it.

## 3. Current acquisition and translation flow

```text
TOML configuration or explicit CLI selectors
                ↓
data-driven bilingual search catalog
                ↓
canonical raw-URL and keyword-generated search plan
                ↓
search limit, offset, page limit, and global request budget
                ↓
sequential Jobinja search-page acquisition
                ↓
immutable search-page HTML and metadata evidence
                ↓
canonical Jobinja job-code discovery
                ↓
repeat-safe JobPosting and discovery provenance
                ↓
missing-detail and refresh-due selection
                ↓
sequential Jobinja detail-page acquisition
                ↓
immutable detail HTML and metadata evidence
                ↓
deterministic Jobinja parser v2
                ↓
semantic content fingerprint and version decision
                ↓
fetch observation: new_version / unchanged / failed
                ↓
deterministic structural parser audit
                ↓
optional English-projection queue
                ↓
source-identity or configured TranslationProvider
                ↓
versioned JobTranslationArtifact
                ↓
completed / failed / reused translation attempt
                ↓
current English corpus and JSONL export
```

The source semantic version remains authoritative. Translation is a derived
representation and cannot change employer evidence.

## 4. Intended complete Phase 1 flow

```text
accepted source semantic versions
        ↓
current English projection when available
        ↓
pending-analysis selection
        ↓
versioned local-model prompt and schema
        ↓
LM Studio provider boundary
        ↓
raw request and response evidence
        ↓
schema and evidence validation
        ↓
accepted / review-required / failed analysis state
        ↓
individual job result
        ↓
combined responsibility, requirement, and role report
```

P1.6 may use the English projection for model convenience, but every material
claim must retain a path to original employer text.

## 5. Runtime components

### 5.1 CLI composition layer

Current commands include:

```text
jobhunter init
jobhunter doctor [--smoke]

jobhunter jobinja catalog [--show-terms]
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch

jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit

jobhunter translations status
jobhunter translations run
jobhunter translations show <job-id>
jobhunter translations export
```

The CLI parses and validates arguments, loads typed settings, assembles services,
prints inspectable summaries, and maps controlled findings to exit statuses.

### 5.2 Typed configuration

`config.py` loads TOML and selected `JOBHUNTER_*` environment overrides through
Pydantic models.

Configuration covers:

- local data, evidence, and SQLite paths;
- LM Studio provider settings;
- Jobinja HTTP controls;
- raw Jobinja search URLs;
- data-driven bilingual search profiles and packs;
- optional external search-catalog path;
- custom keyword groups and excluded terms;
- search/page/request budgets;
- sync missing/refresh limits;
- translation enablement and auto-after-sync policy;
- translation provider/model, timeout, retries, and batch size;
- Google Cloud Translation API key through configuration/environment;
- logging level.

Unknown fields are rejected.

### 5.3 Data-driven bilingual search catalog

Search vocabulary is packaged at:

```text
src/jobhunter/data/search_catalog.toml
```

`search_registry.py` loads and validates the TOML catalog.

Responsibilities:

- load catalog version, profiles, packs, descriptions, and terms;
- normalize Persian/Arabic Unicode variants for identity;
- preserve original display terms;
- generate canonical Jobinja keyword URLs;
- interleave pack terms round-robin for bounded cross-domain coverage;
- combine configured profiles, packs, custom groups, and one-off terms;
- apply normalized exclusions;
- expose catalog/plan output.

A complete replacement catalog can be supplied through
`jobinja_search_catalog_path`. Search vocabulary is acquisition configuration,
not the later canonical career taxonomy.

### 5.4 Jobinja source adapter

`sources/jobinja.py` owns Jobinja URL and HTTP rules:

- approved-host validation;
- canonical search/job URLs;
- bounded pagination;
- public HTML fetches through HTTPX;
- redirect validation;
- response content-type and size bounds;
- descriptive user agent;
- stable source job-code and company-slug extraction;
- per-page link deduplication.

The adapter does not persist records or call models.

### 5.5 Evidence store

`evidence.py` writes raw HTTP bytes and metadata sidecars before downstream
parsing.

```text
data/evidence/jobinja/search-pages/<search>/...
data/evidence/jobinja/job-pages/<job-id>/...
```

Evidence writes use a temporary file followed by atomic replacement.

### 5.6 Discovery orchestration

`jobinja_discovery.py` coordinates validated searches, bounded acquisition,
evidence, deterministic link extraction, job upsert, discovery provenance, and
per-search/combined summaries.

Stop reasons:

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
page_failed
invalid_search
```

Repeated result pages are identified by sorted stable source job IDs rather than
volatile HTML.

### 5.7 Detail acquisition and batch service

`jobinja_detail_service.py` acquires one known job page, saves evidence before
parsing, computes semantic content, records a version only when meaningful
content changes, and records every successful/failed check observation.

`jobinja_batch.py` runs up to 50 unique jobs sequentially with configured delay
and per-job failure isolation.

### 5.8 Fetch observations and refresh scheduling

`job_detail_observations.py` separates operational checks from source semantic
versions. Refresh-due selection uses the latest observation timestamp and falls
back to the semantic-version timestamp for legacy rows.

One failed check never implies expiration or removal.

### 5.9 Deterministic parser

`jobinja_details.py` implements `jobinja-detail-v2` and extracts explicit source
fields without LLM inference. Missing fields remain missing. Jobinja skill tags
remain separate from later description-derived skills.

### 5.10 Source semantic versions

`storage.py` stores meaningful deterministic source versions. Version identity
uses canonical parsed fields rather than volatile raw HTML.

The source semantic version is the parent record for later translations and
analysis.

### 5.11 Translation provider boundary

`translation/base.py` defines a minimal provider protocol:

```text
provider name
provider model
translate ordered text batch
```

`translation/google_cloud.py` implements the official Google Cloud Translation
Basic v2 REST provider.

Provider concerns stay outside parsing and persistence logic.

### 5.12 English projection

`translation/projection.py` creates a complete English representation from one
exact source semantic version.

Rules:

- parser metadata is not projected as job content;
- strings without Persian characters pass through unchanged;
- Persian-containing strings are translated;
- mixed Persian/English strings are translated as one semantic unit;
- no hard-coded translation dictionary is used;
- every string path records `native` or `translated` provenance;
- a complete English document is rendered alongside structured English fields;
- the projection receives its own SHA-256.

### 5.13 Translation persistence

`translation_store.py` introduces two derived record types:

```text
job_translation_artifacts
job_translation_attempts
```

Artifact identity includes:

```text
source detail-version ID
+ target language
+ provider
+ provider model
+ translation schema version
```

Therefore a translator/model/schema change creates a new derived artifact, not a
new employer-content version.

Attempts retain `completed`, `failed`, or `reused` outcomes.

### 5.14 Translation orchestration

`translation_service.py`:

- creates `source-identity/native-english` artifacts for source versions that
  require no Persian translation;
- calls the configured provider for Persian/mixed source segments;
- reuses identical artifacts idempotently;
- isolates per-job translation failures;
- selects bounded missing-artifact queues;
- prioritizes specified current-sync jobs when requested.

### 5.15 English corpus export

`translation_export.py` writes UTF-8 JSON Lines containing only English artifacts
for each job's **latest semantic source version**.

Each record includes source-version identity, provider/model/schema metadata,
segment provenance, structured English fields, and the complete English document.

Stale translations of older source versions are deliberately excluded.

### 5.16 Structural audit

`job_audit.py` checks source parser structure only. Translation quality is a
separate future evaluation problem and must not be conflated with parser quality.

### 5.17 Acquisition sync

`jobinja_sync.py` composes discovery, missing/refresh detail acquisition, and
source parser audit.

The CLI may then run an optional bounded translation queue when:

```toml
translation_enabled = true
translation_auto_after_sync = true
```

This external translation step remains independently visible and can fail without
invalidating acquired source evidence.

### 5.18 LM Studio inference boundary

LM Studio remains behind `inference/`. P1.6 will add versioned analysis schemas,
prompt evidence, raw responses, validation, and review states.

Translation does not replace LM Studio analysis; it prepares a normalized English
view that P1.6 may consume.

## 6. SQLite record model

Current core and derived records include:

```text
source_searches
acquisition_runs
search_page_snapshots
job_postings
job_discoveries
job_detail_versions
job_detail_fetch_observations
job_translation_artifacts
job_translation_attempts
```

Important distinctions:

```text
job_postings
  logical source identity

job_detail_versions
  meaningful employer-content history

job_detail_fetch_observations
  operational checks

job_translation_artifacts
  derived English views of exact source versions

job_translation_attempts
  operational translation history

raw evidence files
  exact HTTP response bytes and metadata
```

SQLite remains appropriate for the current local utility. A general ORM remains
unnecessary.

## 7. Repository structure

```text
src/jobhunter/
  cli.py
  config.py
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
  translation_export.py
  translation_service.py
  translation_store.py
  data/
    search_catalog.toml
  inference/
  sources/
  translation/
    __init__.py
    base.py
    google_cloud.py
    projection.py
```

## 8. Testing strategy

Normal tests do not contact Jobinja, Google Cloud, or LM Studio.

Deterministic tests cover:

- URL/search normalization;
- packaged and external search catalogs;
- pack/profile/custom-group expansion;
- request budgets and discovery idempotency;
- evidence writing;
- parser regressions;
- semantic versions;
- fetch observations and refresh scheduling;
- Google translation request shape, header authentication, and 128-item chunking;
- mixed-language English projection and segment provenance;
- native-English zero-provider behavior;
- translation artifact reuse;
- new-source-version translation invalidation;
- current-version-only English JSONL export;
- CLI privacy/configuration gates.

Live external acceptance remains explicit after deterministic tests pass.

## 9. Security and privacy boundaries

- Use public Jobinja pages only.
- Do not automate login, applications, or CAPTCHA bypass.
- Do not use stealth proxy rotation.
- Bound source requests and detail batches.
- Treat source text as untrusted data.
- Keep runtime data and secrets out of Git.
- Keep Google translation disabled by default.
- When Google translation is enabled, parsed source text is intentionally sent to
  Google Cloud and this must remain explicit in configuration/operation.
- Store the Google API key only in local configuration/environment; prefer a
  restricted environment-provided key.
- Never treat a translation as stronger evidence than the original employer text.

## 10. Current stop line

The system can now configure data-driven bilingual searches, discover jobs
repeat-safely, preserve evidence, fetch and version deterministic source details,
retain check history, audit parser structure, and optionally create/export a
versioned English corpus.

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

Those require P1.6/P1.7 evidence-backed analysis.
