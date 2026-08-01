# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It collects approved public job-market data, preserves original evidence, structures
Jobinja advertisements deterministically, tracks meaningful content versions and source
checks, creates a separate English representation through local LM Studio, and prepares
trustworthy data for later evidence-backed career analysis.

The browser application is now the primary human interface. The CLI remains available for
automation, debugging, tests, and advanced workflows.

## Current accepted data pipeline

```text
data-driven Persian + English search catalog
→ bounded/repeat-safe Jobinja discovery
→ immutable search-page evidence
→ missing + refresh-due detail selection
→ immutable detail evidence
→ deterministic Jobinja parser v2
→ semantic source versions
→ fetch-observation history
→ structural parser audit
→ local LM Studio English projection
→ versioned English artifacts
→ current English JSONL corpus
```

Live acceptance currently includes:

- 103 deterministic tests passing before the web-app increment;
- 79 unique discovered Jobinja identities in the initial repeat-safe live corpus;
- zero new logical jobs on the identical discovery rerun;
- 15 structurally varied complete Jobinja advertisements;
- 15/15 current source versions passing structural parser audit;
- repeated unchanged checks without false semantic versions;
- refresh-due selection using fetch-observation history;
- 15/15 current English artifacts using local LM Studio;
- successful bounded recovery from one real `finish_reason="length"` translation;
- a 15-record current English JSONL export.

The local web interface is implemented but requires its own local acceptance run before it
is marked live-accepted.

## Start the application

After pulling changes, install/update dependencies:

```bash
python3 -m pip install -e ".[dev]"
```

Launch the UI:

```bash
jobhunter-app
```

It opens automatically at:

```text
http://127.0.0.1:8765/
```

### Linux desktop launcher

Install once:

```bash
jobhunter-app --install-desktop
```

After that JobHunter can be started from the Linux application menu without opening a
terminal.

The browser manifest also supports standalone installation in browsers that expose local
web-app installation.

See [Local Web Application](docs/LOCAL_WEB_APP.md).

## Browser experience

### Overview

The dashboard provides:

- discovered/detail/English-corpus counts;
- missing detail and translation counts;
- fetch-observation count;
- recent acquisition runs;
- recent browser operations;
- one bounded sync form;
- one-click parser audit;
- one-click missing translation;
- one-click English-corpus export.

### Jobs

Browse the local corpus without network requests and filter by:

- title/company/location/job ID;
- detail availability;
- current English availability;
- lifecycle state.

One job page shows original employer data and the derived English representation side by
side, plus source checks, evidence identity, parser state, and per-job refresh/translation
buttons.

### Search plan

Inspect the versioned bilingual vocabulary, profiles, packs, generated search sequence,
and request bounds without remembering CLI syntax.

### Operations

Long sync/translation work runs through a one-worker local queue. The browser redirects to
a live operation page that polls local status and displays the same service summaries used
by the CLI. Overlapping mutable browser operations are rejected deliberately.

### System

Inspect local database/evidence/export paths, LM Studio/provider configuration, translation
coverage, and acquisition limits.

## Data-driven bilingual search catalog

Search words are **data, not Python logic**.

The packaged catalog lives at:

```text
src/jobhunter/data/search_catalog.toml
```

The broad profile:

```toml
jobinja_search_profiles = ["ai-security-python"]
```

combines:

```text
ai-ml
llm-applications
python-data
defensive-security
ai-security
network-platform
```

It includes Persian and English terminology for AI/ML, LLM/RAG/agents, Python/data,
defensive security, AI security, Linux/networking/platform/DevOps, and related roles.

A complete replacement catalog can be configured with:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

Small personal additions can remain TOML keyword groups. No Python change is required.

See [Search Configuration](docs/SEARCH_CONFIGURATION.md).

## Source evidence and semantic versions

JobHunter distinguishes:

```text
JobPosting
  logical Jobinja identity

Raw evidence
  one exact HTTP response

JobPostingVersion
  meaningful deterministic employer-content version

JobDetailFetchObservation
  one successful or failed source check
```

A volatile HTML change therefore does not manufacture a logical job change.

Every successful or failed detail check is retained operationally, so refresh scheduling
can use the latest actual observation rather than guessing from semantic-version time.

## Deterministic Jobinja parsing

Parser v2 currently extracts explicit source fields such as:

- title;
- company;
- category;
- location;
- employment type;
- minimum experience;
- salary;
- Jobinja skill tags;
- gender;
- military-service requirement;
- education;
- posting/expiration dates;
- complete job description;
- company description;
- source-language classification.

Missing source values remain missing. The parser does not ask an LLM to infer employer
intent.

## Local English corpus

JobHunter keeps source and translation separate:

```text
original Persian / English / mixed employer text
        ↓ authoritative

English projection
        ↓ derived convenience representation
```

The default translator is local LM Studio:

```toml
translation_enabled = true
translation_provider = "lm-studio"
translation_lm_studio_model = "gemma-4-e2b-it"
```

Translation uses structured JSON-schema output and validates exact result IDs/counts before
an artifact can be persisted. Native English strings pass through without model calls;
Persian-containing strings are labelled `translated` in segment provenance.

A real long-output failure led to bounded recovery:

```text
truncated multi-segment response
→ recursively split requests

single segment still truncated
→ 4096 → 8192 → 16384 → 32768 output-token cap
```

The original source text is never shortened to make translation fit.

Google Cloud Translation remains an optional external provider, but normal operation does
not require a Google account, API key, or billing account.

See [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md).

## Current English export

```bash
jobhunter translations export
```

writes:

```text
data/exports/job_english_corpus.jsonl
```

Each current record contains source identity/version metadata, source language,
provider/model/schema identity, native-versus-translated provenance, structured English
fields, and a canonical English document.

This representation is ready for later embeddings, NLP/ML experiments, clustering,
retrieval, or P1.6 local LLM analysis while preserving a path back to original evidence.

## CLI remains supported

Examples:

```bash
jobhunter jobinja plan
jobhunter jobinja sync
jobhunter jobinja fetch --missing --limit 10
jobhunter jobs list
jobhunter jobs show tpLF
jobhunter jobs checks tpLF
jobhunter jobs audit
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

These commands and the browser use the same underlying SQLite records/services.

## Browser security boundary

The app defaults to loopback and refuses non-loopback binding unless network exposure is
explicitly requested.

Mutating browser forms use a process-local CSRF token. Responses also set restrictive
CSP, frame, referrer, content-type, and cache headers. Static CSS/JS/icons are packaged
locally; the UI does not depend on CDN resources.

## What JobHunter does **not** do yet

The current system prepares trustworthy job data. It does not yet perform the core
semantic career-intelligence stage.

Incomplete areas include:

- challenge/login/CAPTCHA/error/expired-page classification;
- cautious full posting lifecycle policy;
- repost/duplicate-content classification;
- responsibility extraction;
- required-versus-preferred requirement classification;
- description-derived canonical skills;
- aggregate role/market conclusions;
- personal capability comparison;
- readiness/gap analysis;
- career recommendations;
- final combined `jobhunter run` analysis/report workflow.

Those belong to the remaining P1.5/P1.6/P1.7 and later phases. Translation output is
useful but is still derived data; important later conclusions must remain traceable to the
original employer text.

## Development validation

```bash
ruff check .
pytest
```

Normal deterministic tests do not contact Jobinja, Google Cloud, or LM Studio. Network and
model behavior are represented with controlled mock transports.

## Documentation

- [Product Specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Local Web Application](docs/LOCAL_WEB_APP.md)
- [Search Configuration](docs/SEARCH_CONFIGURATION.md)
- [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md)
- [Acquisition Operations](docs/ACQUISITION_OPERATIONS.md)
- [Domain and Analysis Model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source Acquisition Policy](docs/SOURCE_POLICY.md)
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [Repository Instructions](AGENTS.md)
