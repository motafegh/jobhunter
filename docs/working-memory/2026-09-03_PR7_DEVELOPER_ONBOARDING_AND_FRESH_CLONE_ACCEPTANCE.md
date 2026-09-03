# PR7 — Developer Onboarding and Fresh-Clone Acceptance

**Date:** 2026-09-03  
**Status:** PR7 COMPLETE / ACCEPTED  
**Track:** Portfolio readiness / developer experience  
**Product-semantic impact:** none

## Objective

Make a fresh clone understandable and runnable without implying that LM Studio, live Jobinja acquisition, or the maintainer's SQLite state are prerequisites for basic development or review.

## Accepted onboarding model

JobHunter now distinguishes three setup depths:

```text
repository review only
→ committed corpus/demo; no SQLite/LM Studio/Jobinja required

developer baseline
→ Python 3.12 + editable install + isolated local config + local SQLite/tests/browser

full local intelligence
→ optional LM Studio + optional bounded live Jobinja acquisition
```

This separation is intentional. External/model/network readiness must not be conflated with Python/package installation readiness.

## Implemented changes

### 1. Dedicated developer setup guide

Added:

`docs/DEVELOPMENT_AND_LOCAL_SETUP.md`

It covers:

- clone and `.venv` setup;
- Python 3.12+ requirement;
- editable development install;
- isolated local configuration through `config/local.toml`;
- repository-only/public-corpus inspection;
- deterministic baseline checks;
- browser launch against a fresh/empty local database;
- local runtime/Git boundaries;
- optional LM Studio setup and `doctor` semantics;
- optional bounded Jobinja acquisition;
- useful CLI entrypoints;
- troubleshooting by layer;
- normal quality gates.

### 2. Isolated local configuration is the recommended fresh-clone route

Documented bootstrap:

```bash
jobhunter init --path config/local.toml
```

`config/local.*` is already ignored by `.gitignore`.

Developers may use:

```bash
jobhunter --config config/local.toml ...
jobhunter-app --config config/local.toml
```

or set `JOBHUNTER_CONFIG=config/local.toml` in the process environment.

This avoids silently coupling a new machine to maintainer-specific model selections.

### 3. Root README quick start aligned

The root README now recommends:

```text
clone
→ venv
→ editable install
→ ignored local config
→ offline plan/public-corpus status
→ Ruff/pytest/warnings-as-errors
→ local browser
```

It links the full setup guide rather than overloading the landing page with operational detail.

### 4. Documentation map aligned

`docs/README.md` now lists `DEVELOPMENT_AND_LOCAL_SETUP.md` as the primary developer setup reference and includes it in the deeper reviewer/developer route.

### 5. Environment-override example reconciled

`.env.example` now reflects the current supported settings roles more accurately, including:

- local runtime paths;
- general LM Studio settings;
- analysis/capability/Blueprint model roles;
- analysis bounds;
- Jobinja retry/budget settings;
- translation settings;
- optional Google translation credentials;
- log level.

It also explicitly states that JobHunter reads process environment variables and does not automatically load a dotenv file.

### 6. CI now protects onboarding entrypoints

The CI clean runner now validates after editable installation:

```bash
jobhunter --version
jobhunter-corpus status
jobhunter init --path /tmp/jobhunter-local.toml
jobhunter --config /tmp/jobhunter-local.toml jobinja plan
jobhunter --config jobhunter.toml.example jobinja plan
jobhunter-app --help
```

The smoke intentionally requires no live Jobinja request and no model call.

CI then continues to run:

```bash
ruff check .
pytest
pytest -W error
```

## Acceptance evidence

Final PR7 CI:

- workflow run: `1083`
- run ID: `33776557385`
- head commit: `ff829a0f5e859b67269e56bbda9cafc0dc9a0c08`
- result: SUCCESS

Successful steps include:

- Python 3.12 setup;
- editable `.[dev]` installation;
- installed public-entrypoint smoke;
- isolated config bootstrap;
- offline search-plan resolution;
- committed public-corpus status;
- browser launcher help/import path;
- Ruff;
- normal pytest;
- pytest with warnings as errors.

The existing web tests also establish that primary browser pages render against temporary fresh local SQLite state with translation disabled; a maintainer database is not required for the browser architecture itself.

## Important local/public boundary

A fresh clone does not include:

- maintainer SQLite history;
- raw local evidence;
- local model files;
- private/personal career state;
- local secrets;
- uncommitted local logs/notes.

It does include current source/tests/docs, public corpus, review snapshots, configuration examples, and CI.

Mutating installed CLI/browser workflows may refresh the tracked public `corpus/` projection after durable local work. Developers are instructed to inspect `git status --short` and publish corpus changes only intentionally.

## Explicit non-changes

PR7 did not:

- require Docker;
- add a Makefile/task runner;
- add `CONTRIBUTING.md` without demonstrated need;
- add Node/npm/frontend tooling;
- require LM Studio for baseline development;
- require Jobinja network access for baseline development;
- auto-import committed corpus into SQLite;
- change semantic contracts or accepted product behavior.

## Deferred to PR8

The repository still tracks a maintainer-oriented root `jobhunter.toml` containing specific local LM Studio model identifiers/port choices. It contains no identified secret, but it is not the preferred portable developer configuration.

PR7 intentionally did **not** delete or rewrite it because doing so could disrupt the maintainer's current local workflow. PR8 repository/configuration hygiene should decide the safe long-term disposition, including any migration needed before making the root config untracked or fully portable.

Also still outside PR7:

- GitHub description/topics;
- license decision;
- package/project URL metadata;
- dependency-hygiene audit;
- broader secret/privacy/repository hygiene audit;
- real browser screenshots, which remain deferred until maintainer local runtime access returns.

## Decision

PR7 is accepted and closed.

Next portfolio phase:

`PR8 — repository / package / security / configuration hygiene`
