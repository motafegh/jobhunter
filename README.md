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

## Fetch and inspect complete jobs locally

After discovery, fetch one complete advertisement page by stable Jobinja ID:

```bash
jobhunter jobinja fetch tpLF
```

Fetch a deliberate validation set in one bounded sequential batch:

```bash
jobhunter jobinja fetch tmW1 tmkE tmNr tpBO
```

Each batch:

- removes duplicate IDs while preserving order;
- performs requests sequentially;
- uses `jobinja_request_delay_seconds` between requests;
- isolates one job's failure without discarding successful jobs;
- accepts no more than 50 jobs;
- reports new semantic versions, unchanged content, and failures.

List locally known jobs and their detail status:

```bash
jobhunter jobs list
jobhunter jobs list --details missing
jobhunter jobs list --details available
```

Audit the latest locally parsed details without network access or LM Studio:

```bash
jobhunter jobs audit
jobhunter jobs audit tmW1 tmkE tmNr tpBO
jobhunter jobs audit --only-issues
```

The audit reports parser version, description length, explicit-field coverage, source skill-tag count, and structural findings. It flags missing title or description, non-scalar values, obvious page-interface contamination, implausibly long scalar fields, malformed skill tags, and outdated parser versions. Missing optional fields such as salary or education are shown as coverage gaps rather than automatically treated as parser failures.

Once representative layouts have been reviewed, fetch a bounded number of jobs that have no local detail version:

```bash
jobhunter jobinja fetch --missing --limit 5
```

`--missing` does not refresh already acquired jobs. It selects the oldest discovered jobs with no detail content and defaults to five jobs. Explicit IDs and `--missing` cannot be combined.

Inspect the latest locally stored semantic detail without another network request:

```bash
jobhunter jobs show tpLF
```

Detail acquisition:

- loads the canonical URL from SQLite;
- downloads the public job page;
- validates redirects, content type, and response size;
- saves raw HTML and metadata before parsing;
- extracts explicit source fields from Jobinja labels and embedded `JobPosting` metadata;
- stores semantic versions separately from volatile raw-HTML snapshots;
- recognizes unchanged job content even when Jobinja's surrounding HTML changes.

The output can include title, company, category, location, cooperation type, experience, education, salary, gender, military-service requirement, skill tags, complete description, source URL, retrieval time, semantic hash, raw hash, and evidence paths. Missing fields are displayed as unavailable rather than guessed.

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

M0 and P1.1 are complete on `main`. Complete-job acquisition, immutable raw evidence, parser-v2 deterministic extraction, semantic versioning, local inspection, bounded explicit batches, missing-detail selection, local catalog listing, and deterministic local parser auditing are implemented. Representative live Jobinja layouts still control parser acceptance before unrestricted routine acquisition is considered reliable.
