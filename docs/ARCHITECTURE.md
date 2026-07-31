# JobHunter Architecture

## 1. Architectural direction

JobHunter is a **local modular monolith** written in Python.

It is one local application with explicit internal boundaries for acquisition, evidence, persistence, inference, parsing, analysis, and reporting. Components should be separated only when the code has a real current responsibility; empty speculative packages are not created to imitate a future architecture diagram.

The initial interaction surface is a command-line interface. A local web interface may be added only when CLI inspection and review become inefficient.

## 2. Architectural principles

1. Raw evidence is stored before parsing or interpretation.
2. Successful acquisition does not depend on LM Studio availability.
3. Deterministic processing is separated from model-dependent processing.
4. Source-specific behaviour lives in explicit adapters.
5. Network acquisition, evidence writing, persistence, inference, and analysis have clear boundaries.
6. SQLite is the initial system of record.
7. Local source files remain inspectable outside normalized database records.
8. Every repeated operation is designed for idempotency.
9. User corrections will take precedence over later automated guesses.
10. Acquired content is untrusted data, never executable instruction.
11. Optional complexity must be justified by observed product need.

## 3. High-level flow

```text
Configured source searches
          ↓
Source-specific acquisition
          ↓
Raw page + acquisition metadata
          ↓
Candidate identity discovery
          ↓
Repeat-safe SQLite records
          ↓
Job-detail acquisition
          ↓
Deterministic source-field parsing
          ↓
Original + normalized job document
          ↓
Local inference-provider boundary
          ↓
Schema and evidence validation
          ↓
Individual and combined analysis
          ↓
Daily report and review
```

Each completed stage remains valid if a later stage fails. For example, an acquired posting remains stored in `pending_analysis` when LM Studio is unavailable.

## 4. Current runtime components

### 4.1 CLI

Current commands:

```text
jobhunter init
jobhunter doctor
jobhunter doctor --smoke
jobhunter jobinja discover
```

The intended Phase 1 endpoint is:

```text
jobhunter run
```

Command handlers assemble application services. They should not contain source parsing, direct SQL, or model-specific protocol logic.

### 4.2 Typed configuration

Configuration is loaded from a local TOML file with selected environment-variable overrides.

Current settings include:

- database path;
- evidence directory;
- LM Studio base URL and model;
- inference timeout and retry limits;
- Jobinja user agent;
- Jobinja request timeout and delay;
- enabled Jobinja search definitions;
- maximum pages per search;
- logging level.

The real local configuration and secrets remain outside Git.

### 4.3 Jobinja source adapter

The first source adapter is Jobinja-specific.

Its current responsibilities are:

- validate public Jobinja search URLs;
- normalize search pagination;
- fetch pages with bounded sequential HTTP requests;
- validate final redirect hosts and paths;
- reject unsupported response types;
- identify Jobinja job links;
- remove tracking query parameters;
- extract the source job code and company slug;
- deduplicate repeated links on one page.

The adapter uses HTTPX and Python's standard `HTMLParser` for P1.1. A focused external HTML parser should be added only when job-detail field extraction demonstrates that the standard parser is insufficient.

Browser automation remains a fallback only for approved content that ordinary HTTP acquisition cannot retrieve.

### 4.4 Evidence store

The evidence store writes raw response bytes before downstream parsing.

Current layout:

```text
data/
  evidence/
    jobinja/
      search-pages/
        <search-name-and-hash>/
          <timestamp>_p<page>_<hash>.html
          <timestamp>_p<page>_<hash>.json
```

The JSON sidecar records:

- source and evidence kind;
- search name and page;
- requested and final URLs;
- retrieval time;
- selected HTTP headers;
- status code;
- SHA-256 content hash;
- byte count;
- raw content path.

Writes use a temporary file followed by atomic replacement. A failed metadata write removes the associated raw file rather than leaving an ambiguous partial snapshot.

Later content-addressed deduplication may reduce repeated raw storage after actual corpus growth justifies it.

### 4.5 SQLite persistence

SQLite is accessed through a small repository boundary using Python's standard `sqlite3` module.

Current P1.1 tables represent:

- configured source searches;
- acquisition runs;
- search-page snapshots;
- logical job postings;
- search/page discoveries.

This direct approach avoids introducing an Object-Relational Mapper and migration framework before schema evolution requires them.

Schema migration tooling must be introduced before incompatible production schema changes, not merely because it may be useful later.

### 4.6 Discovery orchestration

The Jobinja discovery service coordinates:

```text
validated searches
→ bounded fetch
→ evidence write
→ deterministic link extraction
→ job upsert
→ discovery record
→ run summary
```

It receives its HTTP client, evidence store, database store, clock, and sleep function through explicit constructor arguments. This keeps network, time, and delay behaviour testable without contacting Jobinja.

### 4.7 Job-detail acquisition

P1.3 will add a separate detail-acquisition path. It will select new or refresh-due postings, preserve raw detail HTML, and classify challenge, login, invalid, expired, and inaccessible pages.

Search discovery must not become responsible for parsing complete job descriptions.

### 4.8 Deterministic Jobinja parser

P1.4 will extract Jobinja's explicitly labelled fields using deterministic code. It will preserve:

- original field text;
- complete description content;
- dedicated source skill tags;
- Persian, English, and mixed language;
- a separate normalized analysis copy.

It will exclude navigation, similar-job cards, account controls, and footer content.

### 4.9 Identity and versions

Identity resolution proceeds in layers:

1. Jobinja source job code;
2. canonical source URL;
3. raw content hash;
4. normalized content fingerprint;
5. later, bounded repost similarity when justified.

Repeated acquisition, edited posting, cross-search discovery, and reposting remain distinct concepts.

### 4.10 Inference-provider boundary

LM Studio remains behind the internal inference-provider interface.

Provider responsibilities include:

- connectivity and model discovery;
- bounded timeout and retries;
- structured-output requests;
- response diagnostics;
- model identity reporting.

No acquisition component imports or calls LM Studio.

P1.6 will add real job-analysis requests with versioned prompts and schemas, raw request/response evidence, local validation, and source-evidence requirements.

### 4.11 Analysis and reporting

Analysis operates only on validated posting versions explicitly included in a corpus.

Phase 1 reporting will provide:

- individual job analysis;
- repeated responsibilities and skills;
- required versus preferred distinctions;
- role-family patterns;
- filters by search, date, language, company, location, and state;
- links back to posting and evidence records.

Personal capability comparison remains a later product phase.

## 5. Current repository structure

```text
jobhunter/
  pyproject.toml
  README.md
  AGENTS.md
  docs/
  src/
    jobhunter/
      __init__.py
      cli.py
      config.py
      doctor.py
      evidence.py
      jobinja_discovery.py
      storage.py
      inference/
      sources/
        jobinja.py
  tests/
  data/                 # ignored local runtime data
```

The tree expands only when active responsibilities require it.

## 6. Current technology choices

- Python 3.12 or newer;
- Pydantic for typed configuration and later schemas;
- HTTPX for bounded HTTP access and test transports;
- standard-library `HTMLParser` for initial search-link extraction;
- standard-library `sqlite3` for current persistence;
- `argparse` for the current CLI;
- pytest for tests;
- Ruff for linting;
- structured standard-library logging.

Not currently required:

- SQLAlchemy or Alembic;
- Typer;
- browser automation;
- asynchronous task queues;
- web frameworks;
- embeddings libraries;
- vector databases;
- frontend frameworks.

## 7. Security boundaries

- Use public Jobinja pages only.
- Do not automate login or applications.
- Do not store platform credentials or cookies.
- Do not bypass CAPTCHA, access controls, or blocking.
- Validate final redirect hosts.
- Use bounded pages, timeouts, and delays.
- Never execute acquired scripts.
- Treat page text as untrusted prompt data.
- Do not grant the extraction model shell, filesystem, browser, or unrestricted network tools.
- Keep local runtime data and personal evidence outside version control.

## 8. Testing strategy

### Deterministic unit and service tests

- Jobinja URL validation and canonicalization;
- pagination query preservation;
- job-link extraction and deduplication;
- raw evidence writing;
- SQLite identity idempotency;
- cross-run new versus known classification;
- configuration validation;
- source and provider failure reporting.

### Network tests

Normal tests use HTTPX mock transports or recorded fixtures. They do not contact Jobinja or require LM Studio.

A live Jobinja probe and a live LM Studio smoke test remain explicit local operations.

### Later golden analysis tests

Real Persian, English, and mixed Jobinja examples will form a manually reviewed corpus for field parsing and model extraction evaluation.

## 9. Current architecture decision

The active complete slice is:

```text
Jobinja search URL
→ raw search-page evidence
→ canonical job identities
→ repeat-safe SQLite discovery
→ CLI summary
```

The next slice extends stored identities into raw job-detail evidence. Full LLM analysis begins only after acquisition and deterministic source parsing work against real Jobinja pages.
