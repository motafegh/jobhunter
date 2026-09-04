# JobHunter Portfolio Readiness and Public Presentation Plan

**Status:** ACTIVE / PR0–PR8 REPOSITORY-SIDE IMPLEMENTED / PR9 NEXT  
**Date:** 2026-09-04  
**Scope:** Make the public JobHunter repository professional, understandable, demonstrable, maintainable, and credible as a CV/portfolio project without weakening or rewriting accepted product semantics.  
**Relationship to product work:** P2.2B-B1 remains the current product-development gate and is locally blocked on `ta9l` English projection/P1.6 acceptance. Portfolio work may proceed independently but does not authorize new product features, semantic-contract changes, registry promotion, or reopening accepted layers.

## 0. Progress ledger

| Phase | State | Primary evidence |
| --- | --- | --- |
| PR0 — full portfolio-readiness audit | COMPLETE | `docs/PORTFOLIO_READINESS_AUDIT_2026-09-02.md` |
| PR1 — README / public landing story | COMPLETE | root `README.md`; GitHub settings remain external/manual |
| PR2 — architecture / engineering story | COMPLETE | `docs/ARCHITECTURE.md` |
| PR3 — documentation information architecture | COMPLETE | `docs/README.md`; PR3 working-memory closure |
| PR4 — historical/versioned source disposition | COMPLETE | `docs/CURRENT_RUNTIME_AND_VERSIONED_CODE.md`; PR4 working-memory closure |
| PR5 — current-code structure/readability | COMPLETE | shared `web/common.py` boundary + regression tests; PR5 closure |
| PR6 — reproducible demo/public-corpus experience | REPOSITORY-SIDE COMPLETE | `docs/demo/README.md`; real browser screenshots deferred until local runtime access |
| PR7 — installation/developer onboarding | COMPLETE | `docs/DEVELOPMENT_AND_LOCAL_SETUP.md`; clean CI onboarding smoke |
| PR8 — repository/package/security hygiene | REPOSITORY-SIDE COMPLETE | `SECURITY.md`, package/config/CI hygiene, `docs/working-memory/2026-09-04_PR8_REPOSITORY_PACKAGE_SECURITY_HYGIENE.md` |
| PR9 — portfolio release + CV/interview package | NEXT | final validation/release package not started |

Two external/owner decisions remain intentionally outside the completed repository-side PR8 work:

1. choose a license if third-party reuse should be granted;
2. apply GitHub repository description/topics/homepage through repository settings when available.

PR6 also retains one machine-local presentation item: real browser screenshots must come from the real local application when system access returns; they must not be fabricated.

---

## 1. Objective

Prepare JobHunter so a recruiter, hiring manager, senior engineer, technical interviewer, or developer can quickly understand:

1. the problem and current product value;
2. what is implemented today versus experimental/historical/future;
3. the non-trivial engineering and architecture;
4. source truth, deterministic logic, model reasoning, and reviewed authority boundaries;
5. how provenance, privacy, persistence, failure handling, and bounded acquisition work;
6. how to inspect meaningful real output without private SQLite state or LM Studio;
7. how to install, test, and run the project safely;
8. why major architectural choices were made;
9. how historical/versioned code is intentionally retained;
10. that AI-assisted implementation remained subject to explicit architecture, evidence, review, testing, and project ownership.

The target is **professional technical credibility**, not visual decoration or artificial complexity.

---

## 2. Reviewer journeys

### Recruiter / first pass — roughly 30–90 seconds

Expected path:

```text
README
→ value proposition / implemented capabilities
→ architecture at a glance
→ technology + current maturity
→ real public-corpus/demo evidence
```

### Hiring manager — roughly 3–5 minutes

They should understand the end-to-end workflow, current limits, local-first rationale, deterministic/model/review split, persistence/provenance, tests/CI, and demo path.

### Senior engineer / interviewer — roughly 10–30 minutes

Expected deeper path:

```text
README
→ docs/README.md
→ PRODUCT_SPECIFICATION.md
→ ARCHITECTURE.md
→ CURRENT_RUNTIME_AND_VERSIONED_CODE.md
→ relevant source/tests
→ decisions/experiments/working-memory only when deeper evidence is useful
```

### Developer cloning the repository

Validated route:

```text
clone
→ Python 3.12 virtual environment
→ pip install -e ".[dev]"
→ jobhunter init --path config/local.toml
→ pip check / offline entrypoint smoke
→ Ruff / pytest / pytest -W error
→ optional browser
→ optional LM Studio
→ optional bounded Jobinja acquisition
```

A reviewer without Jobinja or LM Studio can still inspect the committed public corpus and demo.

---

## 3. Permanent rules

1. Do not redesign architecture merely for CV appearance.
2. Do not introduce microservices, Kubernetes, React, vector databases, queues, cloud infrastructure, or fashionable technology solely for portfolio signaling.
3. Do not rewrite Git history to hide engineering evolution.
4. Do not delete historical/versioned source until imports, tests, artifact compatibility, reproducibility, and runtime dependencies are proved unnecessary.
5. Do not change accepted semantic behavior as a presentation/refactor side effect.
6. Do not reopen accepted P1.6, Capability v9, P2.1, or P2.2A for harmless wording/style differences.
7. Do not publish private/local state.
8. Keep public documentation layered and concise; retain deep governance/history without making it the entry path.
9. Do not add ceremonial files, bots, badges, templates, or tooling simply because other repositories have them.
10. Do not misrepresent AI-assisted development. Demonstrate ownership through framing, architecture, evidence boundaries, review, validation, tradeoffs, and technical understanding.
11. Keep implemented/current, experimental, historical, deferred, and planned claims distinct.
12. Preserve one source of truth per concern.
13. Do not fabricate screenshots/demo state or claim machine-local acceptance that has not occurred.
14. Legal/repository-owner choices such as license grants must be explicit rather than inferred for portfolio polish.

---

## 4. Finding classification

Use:

```text
KEEP        already professional and appropriate
POLISH      correct substance, weak wording/presentation/discoverability
REORGANIZE  useful content/code, poor grouping/location
REFACTOR    real current maintainability/readability problem
ARCHIVE     historical/research material worth retaining but not presenting as current
REMOVE      proven obsolete/redundant material with no remaining value
ADD         missing artifact/capability justified by reviewer/developer usability
```

`REMOVE` requires stronger evidence than `ARCHIVE` or `REORGANIZE`.

---

# Part I — Completed foundation

## 5. PR0–PR2 — Audit, README, and architecture — COMPLETE

### PR0

The full audit established that JobHunter already had sufficient engineering substance for a strong portfolio project. The principal weakness was public presentation/information architecture, not technical depth.

Core disposition:

```text
KEEP architecture/trust model
→ POLISH public story
→ reconcile architecture
→ organize documentation/history
→ dependency-audit versioned code
→ selectively refactor measured current problems
→ real corpus-backed demo
→ onboarding/hygiene
→ release/CV package last
```

### PR1

The README now leads with product identity, implemented capabilities, engineering differentiators, current architecture, real public corpus, setup, stack, maturity, limits, and documentation entry points.

### PR2

`docs/ARCHITECTURE.md` now matches the current modular-monolith/local-first implementation, fan-out from accepted P1.6 authority, Capability v9, Work Intelligence v2, Canonical Registry, Market/report boundaries, public corpus/runtime separation, browser/CLI shared services, failure semantics, and experimental Blueprint isolation.

---

# Part II — Information architecture and maintainability — COMPLETE

## 6. PR3 — Documentation information architecture — COMPLETE

Result:

- `docs/README.md` is the professional documentation map;
- stable governance-critical paths were preserved instead of mass-moving files;
- current/supporting/active/closed/historical/proposal/working-memory lifecycles are explicit;
- public Review Snapshot wording/baseline was reconciled;
- deep history remains available without dominating external navigation.

## 7. PR4 — Historical/versioned source disposition — COMPLETE

`docs/CURRENT_RUNTIME_AND_VERSIONED_CODE.md` records the evidence-backed runtime/dependency roles.

The audit proved that older-looking modules are not uniformly dead. Current paths transitively reuse earlier P1.6/Capability components, and experimental Blueprint retains a historical Capability compatibility boundary. No mass deletion or relocation was authorized.

## 8. PR5 — Current-code structure/readability — COMPLETE

The bounded refactor centralized shared web CSRF/template/redirect/operation primitives in `web/common.py` and migrated specialized route modules to that boundary with focused tests.

CLI, Work Intelligence service decomposition, Registry persistence/domain structure, and the modular monolith were kept. `web/app.py` remains a future candidate only if a concrete maintenance/reuse problem justifies a split; file size alone is not authorization.

---

# Part III — Demonstrability and developer experience

## 9. PR6 — Reproducible demo / public-corpus experience — REPOSITORY-SIDE COMPLETE

`docs/demo/README.md` provides a real committed-evidence walkthrough:

- `t4qV` demonstrates a rich accepted source → English → P1.6 → Capability chain;
- `tmBK` demonstrates a sparse/qualification-heavy case where accepted responsibilities remain empty rather than being invented.

No fake demo app or fabricated data was added.

Remaining machine-local item:

```text
2–4 real browser screenshots from the actual local application
```

This remains deferred until local runtime access returns.

## 10. PR7 — Installation/developer onboarding — COMPLETE

`docs/DEVELOPMENT_AND_LOCAL_SETUP.md` now separates:

```text
repository review only
developer deterministic baseline
optional LM Studio intelligence workflow
optional live Jobinja acquisition
```

CI validates the actual fresh-install entrypoints and isolated config bootstrap. The recommended developer config is ignored `config/local.toml`, not the maintainer-specific tracked root runtime reference.

---

# Part IV — Repository quality and release

## 11. PR8 — Repository/package/security hygiene — REPOSITORY-SIDE COMPLETE

Implemented:

- polished `pyproject.toml` package metadata and project URLs;
- explicit evidence-backed dev dependency rationale;
- `python -m pip check` in CI/developer verification;
- aligned tracked maintainer config, portable example, and environment-example boundaries;
- `SECURITY.md` with meaningful local-first/privacy/reporting scope;
- targeted tracked-tree secret/private-artifact review;
- retained minimal CI repository permissions;
- no unnecessary bots/templates/task runners/container infrastructure.

Important dependency evidence:

- removing `httpx2` was tested rather than assumed;
- current Starlette 1.6 TestClient explicitly requires/prefers it and strict CI failed without it;
- `httpx2` is therefore retained as a justified dev/test dependency;
- the AnyIO `<4.15` cap remains a separate strict-warning compatibility boundary until independently disproved.

Still external/owner-controlled:

- **license:** explicit owner choice required before adding a legal reuse grant;
- **GitHub description/topics/homepage:** settings update required; current connector cannot write repository settings.

PR8 closure: `docs/working-memory/2026-09-04_PR8_REPOSITORY_PACKAGE_SECURITY_HYGIENE.md`.

---

## 12. PR9 — Portfolio release and CV/interview package — NEXT

PR9 should perform the final integrated portfolio acceptance rather than starting new product work.

### PR9-A — final repository/public consistency audit

Verify:

- README ↔ docs ↔ architecture ↔ package metadata consistency;
- current public-corpus baseline/demo paths;
- documentation links and current/historical labels;
- latest CI quality result;
- release version/tag readiness;
- no unresolved portfolio claim inflation;
- no accidental private/runtime publication.

Do not reopen accepted product semantics during this audit.

### PR9-B — resolve owner/external release blockers

Before an intentional public portfolio release:

1. owner chooses license policy (if any);
2. apply GitHub description/topics and optional homepage through repository settings;
3. capture real browser screenshots when local runtime access is available.

Do not substitute generated/fake screenshots.

### PR9-C — intentional portfolio release

After the final state is accepted:

1. choose an intentional release label/version;
2. ensure package/version/release notes are consistent;
3. create the Git tag/GitHub release with truthful release notes;
4. ensure README/architecture/demo accurately describe that release.

Do not claim production scale, a production user base, accuracy levels, or capabilities not demonstrated by evidence.

### PR9-D — CV/interview package

Prepare truthful reusable material:

```text
CV project entry
30-second recruiter summary
2–3 minute hiring-manager explanation
10–15 minute technical architecture walkthrough
```

Cover:

- problem/product motivation;
- local-first rationale;
- source/provenance model;
- deterministic vs LLM responsibilities;
- semantic review/promotion boundary;
- SQLite/artifact/versioning strategy;
- bounded acquisition and failure handling;
- public-corpus design;
- tests/CI and important regressions;
- current limitations/tradeoffs and future scale triggers;
- how AI assistance was directed, reviewed, tested, and incorporated into project ownership.

### PR9-E — owner mastery check

Before using the project in interviews, ensure the owner can explain the major architecture/data flows and tradeoffs at the depth claimed in the CV package. This is a learning/review responsibility, not a requirement to manually rewrite AI-assisted code from scratch.

---

## 13. Validation rules

### Documentation/presentation-only

Require:

- factual current-state cross-check;
- link/path verification;
- no overclaiming;
- consistency with controlling product/governance documents.

### File moves/reorganization

Require:

- all references updated;
- imports unaffected or intentionally changed;
- documentation links verified;
- tests/CI when executable paths are touched.

### Runtime/package/dependency change

Require as applicable:

```bash
python -m pip check
ruff check .
pytest
pytest -W error
```

Also require targeted regression or clean-install/entrypoint validation when the changed boundary demands it.

No persisted-contract/currentness changes unless separately authorized. Local/live acceptance is required only where behavior cannot be validated remotely.

### Removal

Require proof of:

- no current imports/references;
- no runtime compatibility role;
- no accepted historical-artifact reproducibility requirement;
- no unique regression value;
- Git history sufficient for discarded material.

---

## 14. Portfolio-readiness acceptance criteria

### Public understanding

- [ ] GitHub description/topics are professional and accurate — external settings action remains.
- [x] README explains the product before implementation chronology.
- [ ] real browser screenshots/visual product evidence exist — local-runtime deferred.
- [x] current, experimental, limited, and future capabilities are separated.
- [x] technology stack and engineering differentiators are visible without hype.

### Architecture

- [x] architecture documentation matches current implementation.
- [x] architecture/data-authority diagram exists in repository-maintained text.
- [x] modular-monolith/SQLite/local-first choices are explainable.
- [x] deterministic/model/review authority boundaries are explicit.

### Code

- [x] current runtime paths are documented for a new engineer.
- [x] historical/versioned code has an intentional documented disposition.
- [x] retained historical/current source clutter has an evidence-backed reason or bounded future trigger.
- [x] major current modules have defensible responsibility boundaries.
- [x] important invariants/data flows are documented and test-backed.

### Documentation

- [x] external-reader documentation path is concise.
- [x] deep governance/history does not dominate normal navigation.
- [x] known stale current-state public documentation from the audit has been reconciled.
- [x] no mass reorganization introduced known broken-path churn.

### Demo / onboarding

- [x] committed public corpus can be inspected without live acquisition/LM Studio.
- [x] README states LM Studio/local-runtime boundaries.
- [x] fresh-clone install/test/entrypoint path has clean CI verification.
- [x] real corpus-backed demo walkthrough exists.
- [ ] real browser screenshots are present.

### Quality / hygiene

- [x] CI is visible in README.
- [x] install/dependency/entrypoint/lint/test/warnings gates are documented and CI-backed.
- [x] package metadata is portfolio-ready for the current alpha state.
- [x] license status is explicit: no license grant has been chosen; owner decision remains before any permissive reuse claim.
- [x] targeted tracked-tree privacy/secret exposure audit is recorded with its limits.
- [x] meaningful security/private-state/public-corpus boundaries are documented.

### CV readiness

- [ ] final integrated PR9 audit is accepted.
- [ ] intentional tagged portfolio release exists.
- [ ] CV project description is finalized.
- [ ] short, medium, and deep interview explanations are prepared.
- [ ] owner learning/mastery pass covers the architecture/tradeoffs represented in the CV package.

---

## 15. Exact next action

Proceed with **PR9 final portfolio validation and release/CV package**, beginning with an integrated consistency audit rather than immediately tagging a release.

```text
final public/repository consistency audit
→ identify only true remaining release blockers
→ resolve owner/settings items where possible
→ real screenshots when local access permits
→ intentional release/tag
→ CV + recruiter/hiring-manager/interview package
→ owner mastery review
```

P2.2B product work remains paused at the existing machine-local `ta9l` P1.6 gate until system access returns. PR9 must not bypass or alter that product gate.
