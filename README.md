# JobHunter

[![CI](https://github.com/motafegh/jobhunter/actions/workflows/ci.yml/badge.svg)](https://github.com/motafegh/jobhunter/actions/workflows/ci.yml)

**JobHunter is a local-first career-intelligence system that turns real job postings into traceable, reviewable evidence for career decisions.**

It is designed as more than a scraper or generic LLM wrapper. JobHunter combines bounded public-source acquisition, immutable evidence, deterministic parsing, local model inference, strict factual extraction, explicit semantic review, capability/work intelligence, reviewed canonical mappings, and durable provenance.

The browser application is the primary repeated-use interface. The CLI exposes the same services and durable state for automation, debugging, review, and advanced workflows.

## What JobHunter does today

JobHunter currently supports an end-to-end Jobinja-centered workflow:

- discover and refresh public jobs through bounded, configurable search plans;
- preserve immutable source evidence and semantic job versions before interpretation;
- build a provenance-preserving English projection without replacing the employer's original text;
- extract conservative responsibilities, requirements, strength, explicit depth, and exact evidence through accepted P1.6 contracts;
- keep fresh semantic artifacts in a review gate before they can feed higher-authority layers;
- build Capability Intelligence above accepted factual claims while preserving complete source coverage;
- organize accepted work through Job Work Intelligence v2 without letting model prose replace source truth;
- maintain reviewed canonical concepts and exact claim mappings in the Canonical Registry;
- expose bounded Market/report read models from accepted evidence;
- inspect the same durable state through a local browser UI and CLI;
- export a deterministic repository-safe public corpus for remote inspection and reproducibility;
- preserve selected semantic-review evidence as curated review snapshots.

## Why the engineering is non-trivial

The central design problem is not "call an LLM on a job description." It is deciding **what may become authoritative, what remains interpretation, and how every important claim stays recoverable to evidence**.

JobHunter uses an explicit authority ladder:

```text
SOURCE FACT
    ↓
NORMALIZED CORRESPONDENCE
    ↓
ANALYTICAL INTERPRETATION
    ↓
RECOMMENDATION / DECISION SYNTHESIS
```

Important boundaries include:

- **source truth before reasoning** — acquired employer evidence is preserved before parsing, translation, or model interpretation;
- **deterministic vs model responsibilities** — identity, provenance, coverage, currentness, lifecycle, counts, and source bookkeeping stay deterministic;
- **reviewed promotion** — generated semantic candidates are not automatically treated as accepted truth;
- **exact lineage** — durable derived artifacts retain model, prompt, schema, source, and dependency identity;
- **local-first inference** — LM Studio is the primary local model boundary for translation and semantic reasoning;
- **partial-success semantics** — one failed fetch, translation, analysis, or downstream operation does not invalidate already successful durable work;
- **public/private separation** — runtime SQLite/history authority is local while only deliberately repository-safe projections are committed;
- **bounded acquisition** — source access, pages, retries, batches, and model calls are intentionally constrained.

## Architecture at a glance

JobHunter is intentionally a **Python modular monolith** with SQLite as the local runtime/history authority.

```text
Public Jobinja source
        ↓
immutable evidence + source observations
        ↓
jobinja-detail-v2 deterministic parsing
        ↓
semantic JobPosting version
        ↓
English projection v2
        ↓
reviewed P1.6 factual substrate
        ├──→ Capability Intelligence v9
        ├──→ Job Work Intelligence v2
        ├──→ reviewed Canonical Registry mappings
        └──→ bounded Market / report read models

Browser UI ─┐
            ├──→ shared application services ──→ SQLite
CLI ────────┘                                  runtime/history authority
                                                     ↓
                                      deterministic repository projections
                                         ├── corpus/
                                         └── review-snapshots/
```

The browser is server-rendered and intentionally shares the same service/data model as the CLI. There is no separate SPA data model, Node runtime, or distributed-service layer.

### Current semantic boundaries

Current accepted/public contracts include:

- English P1.6: `job-analysis-english-v20 / job-analysis-v5`;
- original-language P1.6: `job-analysis-original-v9 / job-analysis-v4`;
- Capability Intelligence: `job-capability-intelligence-v9 / job-capability-intelligence-v5`;
- Job Work Intelligence: `job-work-intelligence-v2 / v2.0`;
- Canonical Registry: `jobhunter-canonical-concept-registry-v1`;
- Public Corpus: `jobhunter-public-corpus-v1`.

Role Capability Blueprint v6 remains implemented as **experimental/historical research**, not an accepted current decision layer.

## Public corpus: inspect real output without LM Studio

The operational database remains local at runtime, but the repository includes a deterministic public projection under [`corpus/`](corpus/README.md).

Current committed baseline:

| Public corpus state | Count |
| --- | ---: |
| Known/discovered jobs | 353 |
| Fetched/parsed job details | 43 |
| Current English projections | 20 |
| Accepted English P1.6 artifacts | 5 |
| Accepted Capability artifacts | 5 |

`353` means known/discovered job identities, not 353 complete advertisements.

A fresh clone can inspect the committed corpus without SQLite, Jobinja access, or LM Studio:

```bash
python -m pip install -e ".[dev]"
jobhunter-corpus status
```

For a concrete accepted example, inspect the committed `t4qV` chain:

```bash
python -m json.tool corpus/jobs/t4qV/source.json
python -m json.tool corpus/jobs/t4qV/english-projection.json
python -m json.tool corpus/jobs/t4qV/p16-english.json
python -m json.tool corpus/jobs/t4qV/capability.json
```

For a guided two-case walkthrough—including lineage checks and a sparse listing where JobHunter deliberately keeps accepted responsibilities empty—see [`docs/demo/README.md`](docs/demo/README.md).

The corpus intentionally excludes SQLite files, raw HTML evidence, machine-local paths, raw model protocol history, prompts, secrets, logs, local configuration, and future personal/private evidence.

## Quick start

### Requirements

- Git
- Python 3.12+
- LM Studio only for local translation/semantic-generation workflows
- network access to Jobinja only for live acquisition workflows

### Install an isolated developer environment

```bash
git clone https://github.com/motafegh/jobhunter.git
cd jobhunter
python -m venv .venv
source .venv/bin/activate       # Linux/macOS/WSL
python -m pip install -e ".[dev]"
jobhunter init --path config/local.toml
```

On Windows PowerShell, activate with:

```powershell
.\.venv\Scripts\Activate.ps1
```

`config/local.toml` is ignored by Git and is the recommended fresh-clone configuration path. It avoids coupling a developer setup to maintainer-specific local model identifiers.

Verify the deterministic baseline:

```bash
jobhunter --config config/local.toml jobinja plan
jobhunter-corpus status
ruff check .
pytest
pytest -W error
```

Normal deterministic tests and offline search planning do not contact Jobinja or LM Studio.

### Launch the local application

```bash
jobhunter-app --config config/local.toml
```

Default URL:

```text
http://127.0.0.1:8765/
```

A fresh local database may be empty; that is valid. The committed `corpus/` is a repository-safe projection for inspection and reproducibility and is not silently imported into local SQLite.

For the complete setup path—including local-state boundaries, optional LM Studio, optional live acquisition, WSL/Windows notes, and troubleshooting—see [`docs/DEVELOPMENT_AND_LOCAL_SETUP.md`](docs/DEVELOPMENT_AND_LOCAL_SETUP.md).

### Selected CLI entry points

```bash
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs analyze <job-id>
jobhunter jobs review-analysis <job-id> status
jobhunter jobs capability <job-id>

jobhunter-work <...>
jobhunter-registry <...>

jobhunter translations status
jobhunter-corpus status
```

Use `--config config/local.toml` (or set `JOBHUNTER_CONFIG`) for local commands that load runtime settings. Run each command with `--help` for the exact subcommands/options supported by the installed version.

## Technology stack

| Concern | Current choice |
| --- | --- |
| Language/runtime | Python 3.12+ |
| Web application | FastAPI, Uvicorn, Jinja2 |
| Persistence | SQLite |
| Typed validation/contracts | Pydantic, JSON Schema |
| HTTP/source access | HTTPX |
| Local structured inference | LM Studio through OpenAI-compatible APIs + Instructor |
| Testing | pytest |
| Lint/static quality | Ruff |
| CI | GitHub Actions |
| UI model | server-rendered browser UI + shared CLI services |

The architecture deliberately avoids microservices, Kubernetes, a separate SPA, vector infrastructure, queues, or cloud dependencies until a measured product need justifies them.

## Current maturity

Accepted/current foundation:

```text
Phase 1                         CLOSED
P2.1 Canonical Registry        CLOSED
P2.2A Job Work Intelligence    ACCEPTED / CLOSED
P2.2B selective responsibility promotion pilot    IN PROGRESS
```

Five heterogeneous accepted P1.6 → Capability chains currently serve as semantic anchors across AI/ML, sparse listings, Python/software, network/security, and operations/platform role shapes.

JobHunter does **not** currently claim:

- semantic acceptance across every discovered job;
- a complete canonical labor-market taxonomy;
- arbitrary-web ingestion;
- reviewed personal capability/gap scoring;
- autonomous job applications;
- production-scale multi-user deployment;
- an evaluated RAG/agent platform.

Those boundaries are intentional: current claims stay narrower than the evidence.

## Project structure

```text
src/jobhunter/        application, domain, persistence, inference, CLI and web modules
tests/                deterministic unit/integration/regression coverage
corpus/               complete current repository-safe public projection
review-snapshots/     selected semantic-review and acceptance evidence
docs/                 product, architecture, policies, plans and engineering history
scripts/              bounded audits and historical/verification utilities
.github/workflows/    CI quality gates
```

Historical/versioned semantic implementations are currently retained for reproducibility and compatibility. They are not all current runtime paths; their eventual disposition is being handled conservatively rather than by mass deletion.

## Documentation

Useful entry points:

- [`docs/PRODUCT_SPECIFICATION.md`](docs/PRODUCT_SPECIFICATION.md) — product purpose, current capabilities, outputs, and boundaries;
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — core architecture, authority, persistence, and runtime design;
- [`docs/DEVELOPMENT_AND_LOCAL_SETUP.md`](docs/DEVELOPMENT_AND_LOCAL_SETUP.md) — fresh-clone development setup and optional local services;
- [`docs/DOMAIN_AND_ANALYSIS_MODEL.md`](docs/DOMAIN_AND_ANALYSIS_MODEL.md) — domain/analysis semantics;
- [`docs/SOURCE_POLICY.md`](docs/SOURCE_POLICY.md) — acquisition and source-authority rules;
- [`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`](docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md) — epistemic/decision authority;
- [`docs/demo/README.md`](docs/demo/README.md) — guided reproducible public-corpus demo using real accepted artifacts;
- [`corpus/README.md`](corpus/README.md) — public corpus contract and usage;
- [`review-snapshots/README.md`](review-snapshots/README.md) — curated semantic-review evidence.

The repository also retains detailed plans, experiments, working memory, and historical acceptance records for engineering traceability. They are deeper implementation history, not the intended first-pass product narrative.

## Quality and trustworthiness

CI runs the repository's normal deterministic gates on every push to `main` and on pull requests:

```bash
ruff check .
pytest
pytest -W error
```

CI also smoke-checks the installed public entrypoints and offline public/demo paths so package installation can succeed while onboarding commands are broken only with a visible failure.

Beyond ordinary tests, the project has regression coverage around source parsing, translation integrity, P1.6 factual contracts, semantic review, Capability reconciliation, lifecycle/source truth, public-corpus projection, Canonical Registry behavior, Work Intelligence, CLI behavior, and browser workflows.

The design prefers **unknown / unresolved / review-required** over fabricated certainty and treats provenance or authority violations as correctness failures rather than presentation details.

## Product direction

The long-term loop remains:

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Current development is still building the reviewed market/work/canonical substrate needed before personal scoring or recommendation layers can be trusted.
