# JobHunter Architecture

## 1. Architectural direction

JobHunter will begin as a **local modular monolith** written in Python.

This means one deployable local application with explicit internal module boundaries. It avoids premature microservices while preserving the option to separate components later if operational evidence requires it.

The initial interaction surface is a command-line interface. A local web interface may be added after the ingestion, extraction, persistence, and review workflows are stable.

## 2. Architectural principles

1. Raw evidence is stored before interpretation.
2. Deterministic processing is separated from model-dependent processing.
3. Network acquisition, parsing, inference, persistence, and analysis have explicit boundaries.
4. LM Studio is accessed through an internal inference-provider interface.
5. Every pipeline stage is resumable and records its outcome.
6. Source-specific behaviour lives in adapters.
7. SQLite is the initial system of record; raw source bodies remain in a content-addressed local evidence store.
8. User corrections take precedence over later automated guesses unless explicitly reconsidered.
9. Untrusted job content is data, never executable instruction.
10. Optional complexity must be justified by observed product need.

## 3. High-level flow

```text
Configured sources / pasted text / uploaded files
                    |
                    v
            Acquisition adapters
                    |
                    v
       Raw snapshot + metadata + content hash
                    |
                    v
      Cleaning / segmentation / deduplication
                    |
                    v
     LM Studio inference-provider boundary
                    |
                    v
       Schema validation and evidence checks
                    |
                    v
       Normalized job and requirement records
                    |
          +---------+----------+
          |                    |
          v                    v
  Human review queue    Aggregate analysis
                               |
                               v
                   Personal gap and action model
                               |
                               v
                         Daily report
```

## 4. Initial runtime components

### 4.1 CLI application

Responsibilities:

- initialize local configuration and storage;
- verify LM Studio connectivity;
- ingest pasted text, files, and URLs;
- run enabled sources;
- inspect run summaries;
- inspect, approve, and correct records;
- export and back up data.

Tentative command shape:

```text
jobhunter init
jobhunter doctor
jobhunter ingest text
jobhunter ingest url <url>
jobhunter run
jobhunter runs show <run-id>
jobhunter review
jobhunter report daily
```

The exact command syntax may change during implementation.

### 4.2 Configuration module

Configuration should come from a local file plus environment-variable overrides.

Initial settings include:

- database path;
- raw evidence directory;
- LM Studio base URL;
- model identifier;
- inference timeout;
- retry limits;
- maximum input size;
- enabled sources;
- user-agent string;
- per-source request limits;
- logging level.

Secrets or tokens must not be committed.

### 4.3 Source adapters

Each adapter implements a common contract such as:

```text
list_candidates() -> candidate references
fetch(candidate) -> raw acquisition result
normalize_identity(raw) -> source-specific identity hints
```

Initial adapters:

- pasted text;
- local file;
- generic permitted public URL.

Later adapters may support specific public Applicant Tracking System APIs or company career pages.

Browser automation is optional and should only be introduced for approved sources that genuinely require rendered content.

### 4.4 Evidence store

The evidence store preserves source bodies outside normalized tables.

Suggested layout:

```text
data/
  evidence/
    sha256-prefix/
      <full-sha256>.html
      <full-sha256>.json
      <full-sha256>.txt
      <full-sha256>.pdf
```

The database stores the hash, media type, relative path, retrieval time, source URL, and related acquisition record.

Identical content is stored once and can be referenced by multiple acquisition attempts.

### 4.5 Persistence layer

Initial database: SQLite.

Reasons:

- local deployment;
- transactional integrity;
- simple backup;
- sufficient scale for a personal job corpus;
- strong support from Python tooling;
- no separate service to operate.

Use schema migrations from the beginning. Database access should be isolated behind repositories or service boundaries rather than spread through command handlers.

PostgreSQL is not an initial requirement. Migration should occur only if measured concurrency, scale, or analytical needs justify it.

### 4.6 Cleaning and document preparation

This component:

- detects content type and encoding;
- removes navigation, scripts, style, cookie banners, and repeated boilerplate where safe;
- preserves headings and list structure;
- records the relationship between cleaned text and raw source;
- segments oversized documents without losing section context;
- identifies obvious acquisition failures such as login pages or bot challenges.

Cleaning must not overwrite raw evidence.

### 4.7 Duplicate and version resolver

Duplicate handling proceeds in layers:

1. exact source identifier match;
2. canonical URL match;
3. exact content-hash match;
4. normalized text fingerprint;
5. later, bounded semantic similarity for repost detection.

The resolver must preserve the distinction between repeated acquisition, edited posting, and repost.

### 4.8 Inference-provider boundary

The application calls local models through an interface similar to:

```text
extract_job(document, schema_version, prompt_version) -> extraction_result
health_check() -> provider_status
list_models() -> available_models
```

The first provider uses LM Studio through a configurable local HTTP endpoint.

Implementation requirements:

- no LM Studio-specific calls outside the provider module;
- configurable model and base URL;
- bounded timeout and retries;
- structured-output request using a JSON Schema where supported;
- validation with local application models after receipt;
- storage of model identifier, parameters, schema version, prompt version, request timing, and raw response;
- no automatic trust in schema-conforming content without evidence checks.

### 4.9 Extraction pipeline

Recommended initial stages:

1. deterministic metadata extraction from URL or embedded structured data;
2. document cleaning;
3. section detection;
4. LLM extraction into a versioned schema;
5. local schema validation;
6. evidence-span verification;
7. normalization preparation;
8. persistence;
9. review classification.

A record enters automatic acceptance only when required fields validate and important claims have evidence. Otherwise it enters review.

### 4.10 Taxonomy and normalization

The taxonomy layer stores:

- canonical concept;
- concept type;
- aliases;
- broader and narrower relationships;
- related concepts;
- external taxonomy identifiers when useful;
- user-approved mappings;
- mapping confidence and provenance.

The original employer wording is always retained.

### 4.11 Analysis engine

The analysis engine operates only on accepted or explicitly included records.

It will eventually calculate:

- posting and responsibility counts;
- required/preferred distributions;
- role and seniority distributions;
- concept co-occurrence;
- expected-depth signals;
- trends over defined time windows;
- personal capability gaps;
- recommendation priorities.

Derived results must record the dataset filter and calculation version used.

### 4.12 Review interface

The initial review interface may be CLI-based. It must support:

- viewing original evidence beside extraction;
- approving or rejecting a field;
- correcting text or classification;
- merging aliases;
- mapping to a different canonical concept;
- marking a source document invalid;
- recording the reason for a correction.

A local browser-based review UI may replace or supplement the CLI later.

## 5. Proposed repository structure

```text
jobhunter/
  pyproject.toml
  README.md
  docs/
  src/
    jobhunter/
      __init__.py
      cli.py
      config.py
      domain/
      application/
      acquisition/
        adapters/
      evidence/
      inference/
        providers/
      extraction/
      normalization/
      analysis/
      review/
      persistence/
      reporting/
  tests/
    unit/
    integration/
    fixtures/
  data/                 # ignored local runtime data
  config/               # example configuration only
```

The exact folder tree should emerge with implementation. Empty speculative packages should not be created merely to mirror this diagram.

## 6. Initial technology direction

The first implementation should use a compact Python stack:

- Python;
- `uv` or another single project/dependency manager;
- Pydantic for configuration and schema validation;
- SQLAlchemy with Alembic for SQLite persistence and migrations;
- HTTPX for HTTP access;
- a focused HTML parser;
- Typer or equivalent for the CLI;
- pytest for tests;
- Ruff for formatting and linting;
- structured local logging.

A browser engine, embeddings library, vector database, task queue, web framework, or frontend framework is added only when a vertical slice requires it.

## 7. Scheduling

The application should first support a reliable manual `jobhunter run` command.

After manual runs are stable, daily execution can be scheduled through the operating system:

- Windows Task Scheduler;
- cron;
- systemd timer;
- another local scheduler selected by the user.

Scheduling remains outside the core acquisition logic. The command itself must be safe to rerun.

## 8. Security boundaries

- Bind LM Studio to localhost by default.
- Treat retrieved content as untrusted input.
- Never execute scripts from acquired pages.
- Never pass page text as system or developer instructions.
- Escape or isolate source text inside prompts.
- Do not expose filesystem, shell, browser, or network tools to the extraction model.
- Enforce maximum response and input sizes.
- Store no platform passwords, cookies, or session tokens for initial sources.
- Prevent URLs from targeting local services or private network ranges unless explicitly approved.
- Keep runtime data and personal capability evidence out of version control.

## 9. Observability

Each run should emit structured events containing:

- run identifier;
- stage;
- source identifier;
- posting identifier when known;
- duration;
- outcome;
- retry count;
- error class;
- model and schema version for inference;
- counts of new, changed, unchanged, failed, accepted, and review-required records.

Logs should aid diagnosis without duplicating entire personal records or confidential configuration.

## 10. Testing strategy

### Unit tests

- canonical URL handling;
- hashing and evidence storage;
- deduplication rules;
- schema validation;
- confidence and review rules;
- taxonomy mapping;
- priority calculations.

### Integration tests

- SQLite migrations;
- evidence store plus database transaction flow;
- HTTP adapter against recorded fixtures;
- LM Studio provider against a stub server;
- optional live LM Studio smoke test marked separately.

### Golden extraction tests

A small manually reviewed corpus should compare expected versus actual extraction fields. Model changes must not be accepted solely because output appears plausible.

## 11. Current architecture decision

Build the smallest complete local pipeline first:

```text
input -> raw evidence -> cleaning -> LM Studio -> schema validation -> SQLite -> inspectable result
```

No aggregate career recommendation is trustworthy until this path is repeatable and auditable.
