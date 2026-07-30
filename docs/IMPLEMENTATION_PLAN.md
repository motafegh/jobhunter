# JobHunter Implementation Plan

## 1. Purpose

This plan sequences product delivery. It is not a learning roadmap and does not prescribe sessions or study milestones.

Each milestone must produce an operable increment, have explicit acceptance criteria, and stop before unrelated features are added.

## 2. Delivery rules

- Build vertical slices rather than completing speculative layers in isolation.
- Keep the application runnable after each milestone.
- Prefer one reliable path over several partial integrations.
- Do not begin aggregate career recommendations until source evidence and extraction are trustworthy.
- Add a dependency only for a current requirement.
- Record material architecture changes in the relevant existing document rather than creating excessive governance files.
- Tests must cover deterministic product behaviour; local-model quality is evaluated through a separate golden corpus.

## 3. Milestone overview

| Milestone | Outcome |
|---|---|
| M0 | Runnable local foundation and verified LM Studio connectivity |
| M1 | Pasted-text ingestion through persisted structured extraction |
| M2 | Permitted URL and file ingestion with evidence storage |
| M3 | Reliable identity, versioning, deduplication, and review workflow |
| M4 | Approved recurring sources and daily run operation |
| M5 | Canonical career taxonomy and aggregate market matrices |
| M6 | Personal capability evidence and gap analysis |
| M7 | Explainable recommendations and daily career report |
| M8 | Trend analysis, quality hardening, backup, and sustained operation |

## 4. M0 — Local application foundation and LM Studio connectivity

### Goal

Create a small, installable application that can validate local configuration and communicate with the configured LM Studio server.

### Deliverables

- Python project configuration;
- `src` package and CLI entry point;
- typed application settings;
- example configuration and environment file;
- structured logging foundation;
- LM Studio provider interface and implementation;
- `jobhunter doctor` command;
- unit tests and provider stub integration test;
- developer commands for install, test, lint, and run;
- ignored local data and secret files.

### `doctor` checks

- configuration loads;
- data directories are writable;
- SQLite can be opened or initialized;
- LM Studio base URL is reachable;
- available models can be listed;
- configured model is present or a clear warning is shown;
- a bounded structured-output smoke request can be performed optionally.

### Acceptance criteria

- a clean local checkout can be installed using documented commands;
- `jobhunter --help` runs;
- `jobhunter doctor` gives actionable pass, warning, and failure output;
- tests run without requiring a live model;
- live LM Studio testing is optional and separately marked;
- no job acquisition or analysis code is faked merely to make the milestone appear larger.

### Stop line

Do not add scraping, job schemas, dashboards, embeddings, taxonomy, or recommendation logic during M0.

## 5. M1 — Pasted-text extraction vertical slice

### Goal

Convert one pasted job description into a validated, persisted, evidence-backed local analysis.

### Deliverables

- initial versioned job-extraction schema;
- prompt template and prompt versioning;
- pasted-text ingestion command;
- raw and cleaned evidence storage;
- SQLite schema and first migration;
- extraction request to LM Studio;
- local schema validation;
- exact evidence passage requirements;
- persistence of request metadata and raw response;
- inspect command for the resulting record;
- fixtures and golden examples.

### Initial extracted fields

- source label;
- title and company when stated;
- location and work arrangement when stated;
- role purpose;
- responsibilities;
- required qualifications;
- preferred qualifications;
- technologies and tools;
- knowledge and practice expectations;
- experience and education;
- constraints;
- evidence and confidence for each material item.

### Acceptance criteria

- the same pasted content does not create uncontrolled duplicate evidence;
- invalid model output is rejected or retried within a bounded rule;
- important fields without supporting evidence enter review;
- original, cleaned, request, response, and normalized records remain inspectable;
- at least a small manually reviewed golden set passes agreed quality checks.

### Stop line

Do not add recurring crawling or personal skill recommendations until this path is trustworthy.

## 6. M2 — Public URL and local file ingestion

### Goal

Support real inputs while preserving the same extraction and evidence guarantees established in M1.

### Deliverables

- generic single public URL ingestion with allowlist and SSRF protections;
- supported local text, HTML, JSON, and PDF import;
- content-type and size validation;
- HTML cleaning with structural preservation;
- canonical URL handling;
- clear detection of login, challenge, error, and irrelevant pages;
- acquisition attempt records;
- recorded HTTP fixtures for tests.

### Acceptance criteria

- network input cannot target blocked local/private addresses by default;
- redirects are revalidated;
- raw bodies are saved before cleaning;
- extraction works consistently across pasted text and supported files;
- source failures do not corrupt existing records;
- a user can identify exactly why an input failed.

### Stop line

Do not turn the generic URL command into an unrestricted crawler.

## 7. M3 — Identity, versioning, deduplication, and review

### Goal

Make repeated operation safe and make uncertain results correctable.

### Deliverables

- logical JobPosting and JobPostingVersion records;
- exact and normalized fingerprinting;
- unchanged, changed, repost, duplicate, and new classifications;
- extraction and review states;
- CLI review workflow;
- field corrections and audit history;
- approved alias mapping support;
- retry and re-extraction commands;
- extraction comparison between model or prompt versions.

### Acceptance criteria

- rerunning unchanged inputs is idempotent;
- updated content creates a version rather than overwriting history;
- user correction is retained and visible;
- a new extraction does not silently replace an accepted manual correction;
- failed and review-required items are queryable.

## 8. M4 — Approved recurring sources and daily operation

### Goal

Run JobHunter daily against explicitly approved sources.

### Deliverables

- SourceDefinition configuration;
- one high-value structured source adapter;
- one approved company or platform adapter only if justified;
- candidate discovery and pagination;
- conditional requests when supported;
- per-source rate and concurrency limits;
- run orchestration with stage isolation;
- resumable failed work;
- daily run summary;
- documented operating-system scheduling example.

### Acceptance criteria

- one source failure does not terminate unrelated source work;
- repeated daily runs remain idempotent;
- rate limits are observable and configurable;
- new, changed, unchanged, blocked, failed, and review-required counts are accurate;
- the user can disable any source without code changes.

### Stop line

Do not add many source adapters before the first recurring source proves useful and maintainable.

## 9. M5 — Taxonomy and market analysis

### Goal

Transform accepted postings into a coherent view of roles, responsibilities, and capability demand.

### Deliverables

- canonical CareerConcept model;
- original mention and alias preservation;
- concept mapping review;
- responsibility family definitions or clustering;
- initial role-archetype analysis;
- required/preferred and responsibility-linked counts;
- filters by date, role, seniority, location, company, and source;
- co-occurrence analysis;
- inspectable matrix export;
- corpus-size and uncertainty warnings.

### Acceptance criteria

- duplicate postings do not inflate market counts;
- every aggregate result can list its supporting postings;
- filters and date windows are displayed;
- tool mentions are not automatically treated as applied capabilities;
- user-approved mappings are stable and reversible.

## 10. M6 — Personal capability evidence and gap analysis

### Goal

Compare market evidence with a realistic model of the user's demonstrated capabilities.

### Deliverables

- personal capability records;
- descriptive depth scale;
- evidence references and limitations;
- recency and independence fields;
- imports or manual links to project evidence;
- knowledge, practice, depth, integration, evidence, presentation, and constraint gap classes;
- individual-role and individual-job comparisons;
- unassessed state rather than forced self-ratings.

### Acceptance criteria

- exposure is not represented as mastery;
- AI-assisted project evidence records the demonstrated capability and limitations;
- unsupported resume claims are clearly identified;
- gap conclusions display both market and personal evidence;
- unknown data remains unknown rather than defaulting to zero capability.

## 11. M7 — Explainable actions and daily report

### Goal

Convert reliable analysis into bounded actions that improve real career decisions.

### Deliverables

- action classes: learn, practise, build, improve, document, assess, monitor, ignore, investigate, prepare application evidence;
- transparent priority calculation;
- project-evidence opportunity mapping;
- individual-job readiness report;
- daily summary of meaningful changes;
- recommendation acceptance, rejection, deferment, and completion states;
- reasons and change conditions for every recommendation.

### Acceptance criteria

- a recommendation can be traced to postings and personal evidence;
- the product does not recommend a new project when documentation, assessment, or a small extension is sufficient;
- frequency alone cannot dominate priority;
- low-confidence recommendations are visibly marked;
- the daily report emphasizes decisions rather than raw counts.

## 12. M8 — Trends and operational hardening

### Goal

Make JobHunter dependable over months of daily local use.

### Deliverables

- historical trend calculations;
- source-corpus change warnings;
- extraction-quality tracking;
- prompt/model regression reports;
- backup, restore, and export commands;
- retention configuration;
- database integrity checks;
- performance profiling;
- failure recovery exercises;
- local operational documentation;
- optional local web interface if CLI review has become inefficient.

### Acceptance criteria

- historical results remain reproducible by version and corpus;
- backups restore successfully in a test;
- model replacement can be evaluated before migration;
- growth in source data does not make normal daily runs unusable;
- source and extraction failures are diagnosable from recorded evidence.

## 13. Evaluation corpus

A small manually reviewed corpus should begin during M1 and expand gradually.

It should include:

- clear and ambiguous responsibility sections;
- required versus preferred language;
- missing company or title metadata;
- duplicated and edited postings;
- multiple role families;
- misleading keyword mentions;
- security, Python, AI, machine-learning, and hybrid roles relevant to the user;
- malformed or irrelevant pages.

Evaluation should measure fields separately. A single overall score is insufficient.

## 14. Current authorized implementation

The current implementation target is **M0 — Local application foundation and LM Studio connectivity**.

The next code change should create the minimal Python application, configuration system, CLI, provider boundary, `doctor` command, and tests described by M0. It should not begin M1 extraction work in the same change.
