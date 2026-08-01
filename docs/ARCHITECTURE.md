# JobHunter Architecture

## 1. Architectural direction

JobHunter is a **local Python modular monolith**.

One application owns configuration, Jobinja acquisition, evidence preservation, SQLite
persistence, deterministic parsing, translation, future local inference/analysis, and two
interaction surfaces:

```text
Browser UI       normal repeated human use
CLI              automation, debugging, tests, advanced operation
        \         /
         application services
                ↓
             SQLite
        + raw evidence files
```

The browser is not a separate frontend product with its own API/data model. It is a thin
server-rendered interface over the same application services and records used by the CLI.

## 2. Permanent principles

1. Preserve raw source evidence before parsing, translation, or interpretation.
2. Keep successful acquisition independent from LM Studio availability.
3. Keep source evidence independent from translation availability.
4. Separate deterministic source parsing from model-dependent processing.
5. Keep source-specific behavior behind explicit adapters/services.
6. Keep browser/CLI handlers as composition and validation code, not source parsing logic.
7. Use SQLite as the local system of record.
8. Keep source evidence inspectable outside normalized records.
9. Design repeated operations for idempotency.
10. Separate semantic versions from volatile HTTP responses.
11. Separate operational fetch history from semantic versions.
12. Separate translation artifacts from authoritative source versions.
13. Preserve native-versus-translated provenance.
14. Prefer missing/review-required states over fabricated values.
15. Treat acquired content as untrusted data, never executable instruction.
16. Bound pages, requests, detail batches, translation batches, retries, and model calls.
17. Keep configuration/policy visible instead of scattering constants.
18. Keep the local web application loopback-first and CSRF-protected.
19. Add complexity only for an observed product need.

## 3. Current end-to-end flow

```text
TOML configuration
        ↓
data-driven bilingual search catalog
        ↓
inspectable bounded search plan
        ↓
sequential Jobinja search acquisition
        ↓
immutable search evidence
        ↓
stable JobPosting identities + discovery provenance
        ↓
missing / refresh-due detail selection
        ↓
sequential detail acquisition
        ↓
immutable detail evidence
        ↓
Jobinja parser v2
        ↓
semantic source version
        ↓
fetch observation
        ↓
structural parser audit
        ↓
optional English-projection queue
        ↓
source identity OR TranslationProvider
        ├─ LM Studio local structured translation (default)
        └─ Google Cloud Translation (optional external)
        ↓
versioned English artifact + translation attempt
        ↓
current English JSONL corpus
```

P1.6 will extend the accepted source/English corpus into evidence-backed semantic analysis.

## 4. Interaction surfaces

### 4.1 Local web application

`jobhunter.web` contains the browser application.

Technology:

```text
FastAPI
Uvicorn
Jinja2
packaged CSS
small vanilla JavaScript
```

There is no Node/npm build system and no CDN dependency.

Primary routes:

```text
/                     dashboard and bounded sync controls
/jobs                 filterable local job catalog
/jobs/{job-id}        source + English detail, evidence, checks, actions
/searches              catalog/profile/pack/effective-plan inspection
/operations            browser operation history
/operations/{id}       live local operation status/output
/system                runtime/configuration visibility
```

Mutating routes cover bounded sync, audit, missing translation, export, per-job source
check, and per-job translation.

Long operations are submitted to one in-process `ThreadPoolExecutor(max_workers=1)`.
This prevents overlapping mutable browser workflows and keeps the initial HTTP response
fast. Durable source/translation history remains in SQLite; the browser operation cards
are intentionally ephemeral runtime state.

### 4.2 Web security boundary

The launcher defaults to `127.0.0.1` and refuses non-loopback binding unless the operator
explicitly chooses network exposure.

The web layer additionally uses:

- a process-local CSRF token on every mutating form;
- restrictive Content Security Policy;
- `X-Frame-Options: DENY`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- no Swagger/OpenAPI UI endpoints;
- no remote static assets.

Browser controls do not bypass source request limits or access policy; they invoke the same
bounded services as the CLI.

### 4.3 CLI

The `jobhunter` CLI remains supported for scriptability, local debugging, explicit batch
operation, and deterministic acceptance work.

The `jobhunter-app` executable starts the local Uvicorn application and opens the default
browser. `jobhunter-app --install-desktop` installs a Linux application-menu entry.

## 5. Runtime components

### Configuration

`config.py` loads typed TOML plus selected `JOBHUNTER_*` environment overrides through
Pydantic. Unknown fields fail closed.

### Search registry

`search_registry.py` loads versioned Persian/English profiles and packs from
`data/search_catalog.toml`, normalizes identity variants, preserves display terms,
interleaves packs for bounded coverage, and builds canonical Jobinja keyword URLs.

### Jobinja source adapter

`sources/jobinja.py` owns public Jobinja URL validation, canonical identities, HTTP bounds,
redirect checks, response-size/content-type checks, and link extraction.

### Evidence store

`evidence.py` writes exact HTTP bytes plus metadata sidecars before downstream parsing.

### Discovery

`jobinja_discovery.py` records search snapshots, stable job identities, discovery
provenance, per-search stop reasons, cross-search overlap, and repeat-safe acquisition
runs.

### Detail acquisition

`jobinja_detail_service.py` preserves one detail response, parses it, computes semantic
content identity, records/reuses the semantic version, and records the source check.

`jobinja_batch.py` adds bounded sequential batch acquisition with per-job failure isolation.

### Fetch observations

`job_detail_observations.py` stores successful/failed checks independently from semantic
versions and drives refresh-due selection.

### Deterministic parser

`jobinja_details.py` implements `jobinja-detail-v2`. It extracts source-explicit fields and
complete description text without LLM inference.

### Structural audit

`job_audit.py` checks parser structure/contamination only. A clean audit does not claim
semantic employer interpretation or translation quality.

### Translation boundary

`translation/base.py` defines the provider protocol.

Current implementations:

```text
translation/lm_studio.py     local-first structured translator
translation/google_cloud.py  optional external provider
```

LM Studio translation validates JSON-schema output, exact IDs/counts, and bounded output.
Explicit `finish_reason="length"` recovery splits multi-segment batches and can increase a
single long segment's output budget up to a hard 32,768-token cap without shortening source
text.

### English projection and persistence

`translation/projection.py` constructs structured English fields, a canonical English
document, per-string native/translated provenance, and a projection hash.

`translation_store.py` persists:

```text
job_translation_artifacts
job_translation_attempts
```

Artifact uniqueness includes source version, target language, provider, model, and
translation schema. Current export/use never silently falls back to an older source
version.

### English export

`translation_export.py` writes current English artifacts as UTF-8 JSON Lines for future
LLM/ML workflows.

### Web read models

`web/queries.py` owns focused read-only dashboard/job-list queries. It is deliberately not a
second persistence layer.

### Web operation manager

`web/operations.py` owns ephemeral browser action state. It does not replace durable
acquisition runs, fetch observations, or translation attempts.

## 6. SQLite record model

Current durable records include:

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

Important distinction:

```text
job_postings                    logical source identity
job_detail_versions             meaningful employer-content history
job_detail_fetch_observations   operational source checks
job_translation_artifacts       derived English views
job_translation_attempts        operational translation history
raw evidence files              exact HTTP response bytes + metadata
```

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
  web/
    app.py
    launcher.py
    operations.py
    queries.py
    templates/
    static/
```

## 8. Testing

Normal tests never contact Jobinja, LM Studio, or Google Cloud.

Deterministic coverage includes acquisition identity/versioning, parsing, observations,
refresh selection, translation/provider behavior, English export, search planning, and the
local web application.

Web tests cover primary route rendering, packaged static assets, browser security headers,
CSRF rejection, local operation execution/polling, and safe empty-corpus filtering.

## 9. Accepted and incomplete boundaries

Accepted through live validation before the web increment:

- M0 foundation;
- P1.1/P1.2 discovery;
- bounded detail acquisition and refresh observations;
- parser v2 across 15 structurally varied live advertisements;
- semantic source versioning;
- 15/15 current LM Studio English artifacts;
- 15-record current English JSONL corpus;
- bounded real truncation recovery.

The new local web application is implemented but must still receive local browser/live
acceptance.

Still incomplete:

- challenge/login/CAPTCHA/error/expired-page classification;
- complete lifecycle/repost/duplicate policy;
- P1.6 responsibility/requirement interpretation;
- aggregate role/market intelligence;
- personal capability comparison and gap analysis;
- final P1.7 combined analysis/report workflow.
