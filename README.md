# JobHunter

JobHunter is a local-first personal career-intelligence application.

Its purpose is not merely to scrape job advertisements. It collects postings from user-approved sources, preserves original evidence, extracts structured responsibilities and requirements with a local Large Language Model (LLM), identifies recurring role and skill patterns, compares those patterns with the user's demonstrated capabilities, and supports practical career decisions.

## Product identity

JobHunter is a **utility-first personal application**, not a learning curriculum or a portfolio exercise whose main purpose is technology practice. Engineering choices favour reliability, inspectability, maintainability, and daily usefulness.

## Intended daily workflow

```text
configured job searches
→ new and changed job discovery
→ immutable raw evidence
→ deterministic source-field parsing
→ local structured analysis
→ individual and combined results
→ practical career report
```

Acquisition is independent from LM Studio. If the model is unavailable or an analysis fails, successfully acquired postings remain stored for later processing.

## Permanent product principles

- **Local-first:** personal profile, analysis, and model inference remain local by default.
- **Evidence-first:** every extracted or inferred claim must be traceable to source text.
- **User-controlled acquisition:** only explicitly configured and permitted sources are collected.
- **Model-replaceable:** LM Studio is the default local inference provider, not a dependency spread throughout the codebase.
- **Idempotent daily runs:** rerunning must not create uncontrolled duplicates.
- **Human-correctable:** uncertain extraction and normalization decisions must be reviewable and repairable.
- **Depth-aware:** exposure, understanding, guided practice, independent execution, integration, and production evidence remain distinct.
- **Utility over ceremony:** documentation and architecture exist to support a working personal product.

## Current Phase 1

Phase 1 automates the user's existing Jobinja workflow:

1. configure each Jobinja search once;
2. discover individual advertisements automatically;
3. follow bounded result pagination;
4. preserve raw search and job-detail pages;
5. identify new, unchanged, changed, and failed items;
6. extract Jobinja's known fields deterministically;
7. preserve Persian, English, and mixed-language source content;
8. analyse new or changed postings through the configured local model;
9. produce individual and combined career results.

See [Phase 1 — Jobinja Workflow Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## Jobinja discovery

Run a one-off search:

```bash
jobhunter jobinja discover \
  --url 'https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=...' \
  --pages 1 \
  --show-jobs
```

The URL represents one search, not one job. JobHunter discovers individual advertisement URLs automatically, stores stable Jobinja job IDs, preserves the raw search page, and recognizes known jobs on later runs.

A reusable search can be configured in `jobhunter.toml`:

```toml
[[jobhunter.jobinja_searches]]
name = "Artificial intelligence roles"
url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
enabled = true
max_pages = 3
```

Then run:

```bash
jobhunter jobinja discover --show-jobs
```

## Fetch and inspect a complete job locally

After discovery, fetch one or more complete advertisement pages by stable Jobinja ID:

```bash
jobhunter jobinja fetch tpLF
```

This command:

- loads the canonical URL from SQLite;
- downloads the public job page;
- validates redirects and content type;
- saves raw HTML and metadata before parsing;
- extracts explicit source fields from embedded `JobPosting` metadata and Jobinja labels;
- stores a content-addressed detail version;
- recognizes unchanged content on a repeated fetch.

Inspect the latest locally stored detail without another network request:

```bash
jobhunter jobs show tpLF
```

The output can include title, company, category, location, cooperation type, experience, education, salary, gender, military-service requirement, skill tags, complete description, source URL, retrieval time, content hash, and evidence paths. Missing fields are displayed as unavailable rather than guessed.

Raw detail evidence is stored under:

```text
data/evidence/jobinja/job-pages/
```

This deterministic detail extraction does not invoke LM Studio. Responsibility and requirement interpretation remains a later Phase 1 increment.

## Existing M0 foundation

The repository also provides:

- an installable Python package and `jobhunter` command;
- validated TOML configuration with environment-variable overrides;
- local data, evidence, and SQLite initialization;
- an isolated LM Studio inference provider;
- model discovery through LM Studio's OpenAI-compatible API;
- optional structured-output smoke testing;
- deterministic tests that do not require a live model or Jobinja.

## Local setup

Requires Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

Create local configuration and storage:

```bash
jobhunter init
```

Start LM Studio's local server, configure an exact model identifier in `jobhunter.toml`, and run:

```bash
jobhunter doctor
jobhunter doctor --smoke
```

Run development checks:

```bash
pytest
ruff check .
```

## Configuration

Use `jobhunter.toml.example` as the reference. The real `jobhunter.toml`, runtime database, evidence, logs, exports, backups, and model files are excluded from Git.

Environment variables use the `JOBHUNTER_` prefix. JobHunter does not automatically load `.env`; `.env.example` documents conventional names for shells or external environment loaders.

## Documentation

- [Product specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Domain and analysis model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source acquisition policy](docs/SOURCE_POLICY.md)
- [Product implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 — Jobinja workflow automation](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [AI-assisted repository instructions](AGENTS.md)

## Current status

M0 and P1.1 are complete on `main`. The first complete-job vertical slice is implemented: a discovered Jobinja job can be fetched, preserved, parsed deterministically, versioned, and inspected locally. Live validation against representative Jobinja pages controls the next parser refinements and batch-fetch work.
