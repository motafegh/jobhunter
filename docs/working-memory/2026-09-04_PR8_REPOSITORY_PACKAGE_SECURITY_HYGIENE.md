# PR8 — Repository, Package, Security, and Configuration Hygiene Closure

**Date:** 2026-09-04  
**State:** COMPLETE for repository-side technical hygiene; owner/settings decisions explicitly deferred  
**Portfolio phase:** PR8

## Purpose

PR8 audited and improved repository/package/security/configuration hygiene without changing accepted JobHunter product semantics or introducing portfolio-only infrastructure.

## Implemented dispositions

### Package metadata — POLISH

`pyproject.toml` now carries a stronger package description, author, keywords, classifiers, and project/documentation/issues URLs while keeping the existing package identity and `0.1.0` development version.

No license metadata was invented because a license is a legal reuse grant and remains an explicit repository-owner decision.

### Development dependencies — KEEP, with evidence

The initial audit found no JobHunter source import of `httpx2`, so PR8 temporarily removed it to test whether it was obsolete.

A clean CI resolver installed FastAPI 0.141.1 / Starlette 1.6.0. Starlette's current TestClient explicitly attempts `import httpx2 as httpx`; without `httpx2` it falls back to `httpx` and emits `StarletteDeprecationWarning`. That made the strict `pytest -W error` gate fail during web-test collection.

Therefore:

- `httpx2>=2.7,<3` is **KEEP** as an explicit development/test dependency while current Starlette TestClient requires/prefers it;
- `httpx>=0.28,<1` remains the application HTTP dependency;
- `anyio>=4,<4.15` remains the separate PR6 strict-warning compatibility cap until a later clean dependency experiment proves that AnyIO 4.15+ is warning-free for the effective stack.

This disposition is based on clean-environment behavior, not package-name inference.

### Dependency consistency — ADD

CI and the developer-quality route now include:

```bash
python -m pip check
```

This validates the installed dependency graph in addition to Ruff, normal pytest, and warnings-as-errors pytest.

### Configuration boundary — POLISH / KEEP

The tracked root `jobhunter.toml` is preserved because it records current maintainer runtime/model selections and removing or replacing it while local machine access is unavailable could create unnecessary operational churn.

It is now explicitly labeled as a **maintainer runtime/reproducibility reference**, not the portable fresh-clone setup, and must not contain secrets.

Portable developer configuration remains:

```text
jobhunter init --path config/local.toml
```

with `config/local.*` ignored by Git.

`jobhunter.toml.example`, `.env.example`, README, and the development setup guide now consistently explain this boundary.

### Security policy — ADD

`SECURITY.md` now documents JobHunter's actual security model rather than generic hosted-service boilerplate:

- local-first/loopback browser boundary;
- local SQLite/evidence/private-state boundary;
- optional LM Studio and live Jobinja boundaries;
- secret/private-data handling;
- public-corpus privacy boundary;
- vulnerability-reporting guidance;
- non-loopback binding risk.

### Privacy / tracked-tree posture — KEEP

The targeted tracked-tree audit found no committed SQLite/database files, key/certificate files, or obvious credential artifacts. `.gitignore` already excludes local databases/WAL/SHM files, `.env` files, `config/local.*`, models, logs, exports, backups, and runtime data.

The public-corpus exporter remains an allowlisted deterministic projection of approved public-domain/current artifacts rather than a database dump. Its privacy boundary remains a portfolio strength.

This was a GitHub-tree and targeted source audit; it is not represented as an exhaustive secret-scanning product.

### CI permissions/infrastructure — KEEP

The CI workflow keeps repository permission at `contents: read` and now validates:

```text
editable dev install
→ pip check
→ installed entrypoint/onboarding smoke
→ Ruff
→ pytest
→ pytest -W error
```

No Dependabot, CODEOWNERS, issue-template suite, task runner, container stack, or additional bot/ceremony was added without a demonstrated project need.

## Explicitly deferred owner/settings decisions

### License — OWNER DECISION REQUIRED

The public repository still has no license. PR8 deliberately did not choose MIT, Apache-2.0, or another license on the owner's behalf because that changes third-party reuse rights.

If permissive public reuse is desired, MIT is a reasonable simple candidate, but the repository owner must choose before a `LICENSE` file/project license metadata is added.

### GitHub repository metadata — SETTINGS ACTION REQUIRED

The repository still has no GitHub description/homepage/topics configured. The available GitHub connector does not expose repository-settings writes, so PR8 could not apply them directly.

Recommended description:

> Local-first career intelligence from real job evidence, with provenance-preserving LLM analysis, semantic review, and auditable Python workflows.

Recommended topics:

```text
python
fastapi
sqlite
llm
lm-studio
career-intelligence
job-market
provenance
local-first
pydantic
```

A homepage should remain unset unless a meaningful destination exists.

## Validation

Clean GitHub Actions run `1093` (`33893216022`) after restoring the evidence-backed TestClient dependency passed:

- package/dev installation;
- `python -m pip check`;
- installed public-entrypoint/onboarding smoke;
- Ruff;
- all 540 normal tests;
- all tests with warnings treated as errors.

No accepted semantic contract, persisted schema, source-policy rule, public-corpus authority boundary, or product runtime behavior was intentionally changed by PR8.

## Handoff

PR8 repository-side technical hygiene is complete.

PR9 may now perform final portfolio validation and release/CV/interview packaging, while preserving these unresolved external/owner items:

1. real browser screenshots remain deferred until local runtime access returns;
2. license choice requires explicit owner selection;
3. GitHub description/topics/homepage require repository-settings access/manual owner action.
