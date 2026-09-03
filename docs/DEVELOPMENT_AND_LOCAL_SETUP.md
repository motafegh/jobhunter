# JobHunter Development and Local Setup

**Status:** Current developer onboarding / local setup guide  
**Scope:** Fresh-clone setup, repository-safe inspection, local runtime configuration, optional LM Studio, optional Jobinja acquisition, and local-state boundaries.

This guide is for developers or technical reviewers who want to go beyond the repository-only demo and run JobHunter locally.

JobHunter is intentionally local-first. A useful fresh-clone experience does **not** require LM Studio or live Jobinja access. Those are optional capabilities layered on top of the deterministic local application and committed public corpus.

## 1. Choose the setup depth you need

### A. Repository review only

Use this when you only want to inspect real accepted project output.

Requirements:

- GitHub access, or a cloned repository;
- no SQLite database from the maintainer;
- no LM Studio;
- no Jobinja network access.

Start with:

- [`../README.md`](../README.md)
- [`demo/README.md`](demo/README.md)
- [`../corpus/README.md`](../corpus/README.md)

The committed corpus is a repository-safe projection, not the operational SQLite database.

### B. Developer baseline

Use this to run tests, CLI read/planning commands, and the browser against your own local state.

Requirements:

- Git;
- Python 3.12+.

LM Studio and Jobinja access are not required for this baseline.

### C. Full local intelligence workflow

Add these only when you need them:

- LM Studio for translation and local semantic/reasoning workflows;
- live Jobinja access for bounded public-source acquisition.

Keep these optional components separate from basic installation so failures in an external/model service do not look like Python/package setup failures.

---

## 2. Clone and create an isolated Python environment

```bash
git clone https://github.com/motafegh/jobhunter.git
cd jobhunter
python -m venv .venv
```

Activate the environment.

Linux/macOS/WSL:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

`.venv/` is ignored by Git.

The repository CI performs the same editable development install on Python 3.12 before running the quality gates.

---

## 3. Create your own local configuration

Do not depend on another machine's LM Studio model identifiers or runtime choices.

Create an ignored developer configuration:

```bash
jobhunter init --path config/local.toml
```

`config/local.*` is intentionally ignored by Git. The generated configuration starts with conservative defaults, including translation disabled.

Use it explicitly:

```bash
jobhunter --config config/local.toml jobinja plan
jobhunter-app --config config/local.toml
```

Or set the configuration path in your shell for the current session.

Linux/macOS/WSL:

```bash
export JOBHUNTER_CONFIG=config/local.toml
```

Windows PowerShell:

```powershell
$env:JOBHUNTER_CONFIG = "config/local.toml"
```

After that, commands that load normal settings may omit `--config`.

### About the root configuration files

- `jobhunter.toml.example` is the portable documented example.
- the repository may retain a maintainer-oriented root `jobhunter.toml` while configuration hygiene is being handled separately;
- new developers should use their own ignored `config/local.toml` rather than inheriting machine-specific model selections.

### About `.env.example`

`.env.example` documents supported environment-variable names. JobHunter does not silently require a dotenv file for normal operation. If you use environment overrides, export them through your shell/process environment and keep real secrets in ignored local state.

---

## 4. Verify the deterministic baseline

These commands require no live Jobinja request and no model call:

```bash
jobhunter --version
jobhunter --config config/local.toml jobinja plan
jobhunter-corpus status
ruff check .
pytest
pytest -W error
```

`jobhunter-corpus status` reads the committed repository manifest and does not query your SQLite database.

The expected current public-corpus shape is documented in [`demo/README.md`](demo/README.md). Corpus counts will naturally change as accepted public project state evolves.

### Why both `pytest` and `pytest -W error`?

The normal test run protects behavior. The strict run also treats Python warnings as failures so dependency/API deprecations cannot silently accumulate. CI executes both.

---

## 5. Launch the browser without LM Studio

```bash
jobhunter-app --config config/local.toml
```

Default address:

```text
http://127.0.0.1:8765/
```

The launcher binds to loopback by default and refuses non-loopback binding unless `--allow-network` is explicitly supplied.

A new local database may be empty. That is valid: the browser can render its primary local pages against newly initialized local SQLite state. The committed `corpus/` is **not** silently imported into runtime SQLite.

Useful launcher options:

```bash
jobhunter-app --help
jobhunter-app --config config/local.toml --no-browser
```

Linux desktop integration is optional:

```bash
jobhunter-app --config config/local.toml --install-desktop
```

See [`LOCAL_WEB_APP.md`](LOCAL_WEB_APP.md) for the browser architecture, security boundary, and screen behavior.

---

## 6. Local runtime files and Git boundaries

Normal local operation creates machine-local state under the configured data paths, typically:

```text
data/
├── jobhunter.sqlite3
├── jobhunter.sqlite3-wal / -shm   # SQLite may create these
└── evidence/
```

The repository ignores:

- `data/`;
- SQLite/database files and WAL/SHM companions;
- `.env` and local environment files;
- `config/local.*`;
- virtual environments;
- logs, exports, backups, local models, and common temporary/editor files.

Do not commit private/personal runtime data, credentials, raw model protocol history, or machine-local evidence paths.

### Important: public-corpus synchronization

The installed `jobhunter` command intentionally refreshes the tracked `corpus/` projection after supported durable mutations. Browser mutations use the same post-success projection idea.

Therefore, after live/local mutating work, check:

```bash
git status --short
```

A changed `corpus/` is not automatically an error. It means your durable public-domain JobHunter state produced a different repository-safe projection. Commit those changes only when publishing that public project state is intentional.

The runtime SQLite database remains the operational authority; `corpus/` remains a deterministic public projection.

---

## 7. Optional LM Studio setup

LM Studio is needed only for local model-backed workflows such as translation and semantic/reasoning generation.

1. Start LM Studio's OpenAI-compatible local server.
2. Load the model(s) you intend to use.
3. Edit `config/local.toml` with the actual local URL/model identifiers.
4. Keep the URL on loopback for normal local use.

Typical local endpoint:

```text
http://127.0.0.1:1234/v1
```

Inspect exact visible model identifiers:

```bash
jobhunter --config config/local.toml translations models
```

Run environment/model health checks:

```bash
jobhunter --config config/local.toml doctor
```

When you deliberately want a small structured-inference check:

```bash
jobhunter --config config/local.toml doctor --smoke
```

`doctor` is an LM Studio-aware preflight, so an unavailable LM Studio server is expected to fail that check. It is **not** required for the deterministic developer baseline.

For translation, set appropriate model configuration and enable it intentionally:

```toml
translation_enabled = true
translation_provider = "lm-studio"
```

Do not enable automatic translation-after-sync merely to make setup look complete. Validate a small real translation sample first.

See [`TRANSLATION_AND_ENGLISH_CORPUS.md`](TRANSLATION_AND_ENGLISH_CORPUS.md) for model selection, translation authority, integrity checks, and recovery behavior.

---

## 8. Optional live Jobinja acquisition

Search planning is offline:

```bash
jobhunter --config config/local.toml jobinja catalog
jobhunter --config config/local.toml jobinja plan
```

Live acquisition begins only when you run acquisition commands such as:

```bash
jobhunter --config config/local.toml jobinja discover
jobhunter --config config/local.toml jobinja sync
jobhunter --config config/local.toml jobinja fetch <job-id>
```

For a first live experiment, keep bounds small and inspect the plan before acquisition. The configured request/page/batch limits exist to prevent unbounded source access.

Source acquisition remains useful independently of LM Studio. A network/model failure must not be interpreted as a package-installation failure.

See [`ACQUISITION_OPERATIONS.md`](ACQUISITION_OPERATIONS.md) for the full bounded operational workflow and failure semantics.

---

## 9. Useful command map

Repository/public inspection:

```bash
jobhunter-corpus status
python -m json.tool corpus/jobs/t4qV/p16-english.json
```

Local source/job inspection:

```bash
jobhunter --config config/local.toml jobs list
jobhunter --config config/local.toml jobs show <job-id>
jobhunter --config config/local.toml jobs audit
```

Model/translation inspection:

```bash
jobhunter --config config/local.toml translations status
jobhunter --config config/local.toml translations models
```

Semantic/reasoning work is intentionally explicit:

```bash
jobhunter --config config/local.toml jobs analyze <job-id>
jobhunter --config config/local.toml jobs review-analysis <job-id> status
jobhunter --config config/local.toml jobs capability <job-id>
jobhunter-work --help
jobhunter-registry --help
```

Use `--help` on an entrypoint/subcommand before assuming options from older project history.

---

## 10. What a fresh clone does not contain

A clone does not contain the maintainer's operational state:

- local SQLite history;
- raw local evidence files;
- LM Studio models;
- private/personal career evidence;
- local secrets or tokens;
- uncommitted review notes/logs.

It **does** contain:

- application source and tests;
- current public documentation;
- deterministic public corpus projection;
- selected repository-safe review snapshots;
- configuration examples;
- CI definition and engineering history.

This distinction is intentional. Reproducibility does not mean publishing private runtime state.

---

## 11. Troubleshooting by layer

### Install/import failure

Check:

```bash
python --version
python -m pip install -e ".[dev]"
```

JobHunter requires Python 3.12+.

### Configuration failure

Use an explicit known local config:

```bash
jobhunter --config config/local.toml jobinja plan
```

Do not diagnose model/network services until settings load cleanly.

### Empty browser/catalog

A fresh local SQLite database is expected to be empty until you acquire jobs. Use the committed [`demo/`](demo/README.md) / [`corpus/`](../corpus/README.md) for repository-backed examples.

### LM Studio failure

Verify the server and exact model IDs:

```bash
jobhunter --config config/local.toml translations models
jobhunter --config config/local.toml doctor
```

### Jobinja failure

First confirm that offline planning works, then use the bounded acquisition runbook. Keep access/challenge/network failures distinct from legitimate vacancy state.

---

## 12. Development quality gate

Before sharing a code change:

```bash
ruff check .
pytest
pytest -W error
```

For changes that affect installed CLI/browser onboarding, also exercise the relevant installed entrypoint or rely on the equivalent CI smoke when it covers the exact path.

Do not add a task runner, container stack, frontend build system, or service orchestration layer merely to wrap these already-short commands. Add infrastructure only when the project has a demonstrated need for it.
