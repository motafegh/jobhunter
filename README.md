# JobHunter

JobHunter is a local-first personal career-intelligence application.

Its purpose is not merely to scrape job advertisements. It collects job postings from user-approved sources, preserves the original evidence, extracts structured responsibilities and requirements with a local Large Language Model (LLM), identifies recurring role and skill patterns, compares those patterns with the user's demonstrated capabilities, and produces practical career decisions.

## Product identity

JobHunter is a **utility-first personal application**, not a learning curriculum or a portfolio exercise whose main purpose is technology practice. Engineering choices therefore favour reliability, inspectability, maintainability, and daily usefulness.

## Intended daily workflow

1. Run JobHunter locally.
2. Check configured and approved job sources for new or changed postings.
3. Save immutable source snapshots and acquisition metadata.
4. Remove duplicates and identify changed versions.
5. Use a locally served model through LM Studio to extract structured responsibilities, requirements, skills, experience expectations, and supporting evidence.
6. Normalize extracted concepts into a career taxonomy.
7. Update role, responsibility, skill-demand, and personal-gap analyses.
8. Review the daily report and correct uncertain extractions when necessary.

## Permanent product principles

- **Local-first:** personal profile, analysis, and model inference remain local by default.
- **Evidence-first:** every extracted or inferred claim must be traceable to source text.
- **User-controlled acquisition:** only explicitly configured and permitted sources are collected.
- **Model-replaceable:** LM Studio is the default local inference provider, not a hard dependency throughout the codebase.
- **Idempotent daily runs:** rerunning the same acquisition period must not create uncontrolled duplicates.
- **Human-correctable:** uncertain extraction and normalization decisions must be reviewable and repairable.
- **Depth-aware:** skills are not binary; exposure, understanding, guided practice, independent execution, integration, and production evidence remain distinct.
- **Utility over ceremony:** documentation and architecture exist to support a working personal product.

## Initial product boundary

The first usable extraction slice will:

- accept pasted job text and a permitted public job URL;
- preserve the original content and metadata;
- send cleaned content to LM Studio;
- require schema-conforming structured output;
- extract responsibilities, required and preferred qualifications, technologies, experience expectations, and evidence passages;
- store results locally;
- display an inspectable result that the user can approve or correct.

Automated recurring source discovery, skill matrices, personal capability comparison, trend analysis, and dashboards follow only after this extraction path is reliable.

## M0 local foundation

The current implementation provides:

- an installable Python package and `jobhunter` command;
- validated TOML configuration with environment-variable overrides;
- local data, evidence, and SQLite initialization;
- an isolated LM Studio inference-provider client;
- model discovery through LM Studio's OpenAI-compatible API;
- an optional JSON-Schema structured-output smoke test;
- deterministic tests that do not require a live model.

## Local setup

Requires Python 3.12 or newer.

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Activate the virtual environment before running commands. On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Create local configuration and storage:

```bash
jobhunter init
```

Start LM Studio's local API server, then run:

```bash
jobhunter doctor
```

To also verify an actual schema-conforming model response:

```bash
jobhunter doctor --smoke
```

Set `lm_studio_model` in `jobhunter.toml` to an exact model identifier shown by the server, or leave it unset and the smoke test will use the first visible model.

Run development checks:

```bash
pytest
ruff check .
```

## Configuration

Use `jobhunter.toml.example` as the reference. The real `jobhunter.toml`, runtime database, evidence, logs, exports, backups, and model files are excluded from Git.

Environment variables use the `JOBHUNTER_` prefix. See `.env.example` for the available M0 overrides. JobHunter does not automatically load `.env`; it documents conventional environment names for shells or external environment loaders.

## Documentation

- [Product specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Domain and analysis model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source acquisition policy](docs/SOURCE_POLICY.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [AI-assisted repository instructions](AGENTS.md)

## Current status

M0 provides the local application foundation and LM Studio connectivity. The next product milestone is **M1 — pasted-text extraction through persisted, evidence-backed structured analysis**. M1 should begin only after M0 validation is accepted.
