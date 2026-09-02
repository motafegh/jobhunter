# JobHunter Portfolio Readiness and Public Presentation Plan

**Status:** ACTIVE / PR0–PR2 IMPLEMENTED / PR3 NEXT  
**Date:** 2026-09-02  
**Scope:** Make the public JobHunter repository professional, understandable, demonstrable, maintainable, and credible as a CV/portfolio project without weakening or rewriting accepted product semantics.  
**Relationship to product work:** P2.2B-B1 remains the current product-development gate and is locally blocked on `ta9l` P1.6 acceptance. Portfolio work may proceed while that local blocker exists, but it does not authorize new product features, semantic-contract changes, registry promotion, or reopening accepted layers.

## 0. Progress ledger

| Phase | State | Primary evidence |
| --- | --- | --- |
| PR0 — full portfolio-readiness audit | COMPLETE | `docs/PORTFOLIO_READINESS_AUDIT_2026-09-02.md` / commit `c7334723613e0c95b06e859222fc990d54bb905e` |
| PR1 — README / public landing story | README COMPLETE | commit `1dae378acb11941d58828c941438851985fcdfd7`; GitHub description/topics remain a later repository-settings task |
| PR2 — architecture / engineering story | IMPLEMENTED | `docs/ARCHITECTURE.md` / commit `6a2eeb9e1f2205c087c27d962b5a7a0d48432d2c` |
| PR3 — documentation information architecture | NEXT | not started |
| PR4 — historical/versioned source disposition | PENDING | not started |
| PR5 — current-code structure/readability | PENDING | not started |
| PR6 — demo/screenshots/public-corpus walkthrough | PENDING | not started |
| PR7 — installation/developer onboarding | PENDING | not started |
| PR8 — repository/package/security hygiene | PENDING | not started |
| PR9 — stable portfolio release + CV/interview package | PENDING | not started |

---

## 1. Objective

Prepare JobHunter so that a recruiter, hiring manager, senior engineer, or technical interviewer can quickly understand:

1. what problem the project solves;
2. what is implemented today;
3. what makes the engineering non-trivial;
4. how the architecture works;
5. how source truth, deterministic logic, model reasoning, and reviewed authority are separated;
6. how to run or inspect the project safely;
7. how quality, testing, provenance, privacy, and failure handling are enforced;
8. which parts are current, experimental, historical, or future work;
9. what major design decisions were made and why;
10. that the repository is intentionally engineered rather than an unstructured accumulation of generated code.

The target is **professional technical credibility**, not visual decoration or artificial complexity.

---

## 2. Reviewer journeys to optimize

### Recruiter / first-pass reviewer — about 30–90 seconds

They should immediately see:

- concise project identity/value proposition;
- major implemented capabilities;
- primary technology stack;
- one clean architecture visual;
- screenshots/product preview;
- current maturity/status;
- why this is more than a scraper or generic LLM wrapper.

### Hiring manager — about 3–5 minutes

They should understand:

- end-to-end workflow;
- current features and limitations;
- architecture/boundaries;
- local-first/privacy rationale;
- deterministic-versus-model responsibilities;
- persistence/provenance strategy;
- tests and CI;
- public-corpus/demo path.

### Senior engineer / technical interviewer — about 10–30 minutes

They should be able to inspect:

- package/module boundaries;
- important service/data flows;
- current versus historical implementations;
- failure semantics and safety boundaries;
- schema/artifact versioning rationale;
- testing strategy and representative regressions;
- source acquisition constraints;
- canonicalization/review architecture;
- design tradeoffs and known limitations.

### Developer cloning the repository

Expected route:

```text
clone
→ install
→ configure
→ inspect/demo
→ run tests
→ optionally run the local application
```

A reviewer without Jobinja acquisition access or LM Studio should still be able to inspect meaningful committed project output.

---

## 3. Permanent rules for this track

1. Do not redesign architecture merely for CV appearance.
2. Do not introduce microservices, Kubernetes, React, vector databases, queues, cloud infrastructure, or other fashionable technology solely for portfolio signaling.
3. Do not rewrite Git history to hide engineering evolution.
4. Do not delete historical/versioned source modules until imports, tests, artifact compatibility, reproducibility needs, and runtime dependencies are audited.
5. Do not change accepted semantic behavior as a side effect of presentation/refactor work.
6. Do not reopen accepted P1.6, Capability v9, P2.1, or P2.2A for harmless wording/style differences.
7. Do not publish private/local state.
8. Public-facing documentation should be layered and concise; deep governance/history may remain available without dominating entry paths.
9. Do not add ceremonial files simply because other repositories have them.
10. Do not misrepresent AI-assisted development. Demonstrate project ownership through problem framing, architecture, evidence boundaries, acceptance criteria, validation, tradeoffs, and technical understanding.
11. Keep claims accurate: implemented/current, experimental, historical, deferred, and planned must remain distinct.
12. Preserve one source of truth per concern.

---

## 4. Finding classification

Every change should use one of these dispositions:

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

PR0 authorized **no removal** based only on filename/history appearance.

---

# Part I — Completed public foundation

## 5. PR0 — Full portfolio-readiness audit — COMPLETE

Deliverable:

`docs/PORTFOLIO_READINESS_AUDIT_2026-09-02.md`

Key result:

```text
KEEP core architecture + trust/provenance model
→ POLISH public story
→ reconcile current architecture
→ REORGANIZE documentation/history visibility
→ dependency-audit historical code before movement/removal
→ selectively REFACTOR only measured current problems
→ build a real corpus-backed demo
→ finish package/release/CV presentation last
```

---

## 6. PR1 — GitHub landing page and README — README COMPLETE

The root README has been redesigned around:

```text
problem / value proposition
→ current product capabilities
→ engineering differentiators
→ architecture at a glance
→ real public-corpus inspection
→ quick start
→ technology stack
→ maturity and limitations
→ project structure / docs
```

Requirements retained:

- no inflated claims;
- current vs experimental/future capabilities separated;
- Blueprint explicitly non-authoritative;
- local-first / LM Studio role explained practically;
- provenance/authority design surfaced as a differentiator;
- internal artifact chronology no longer dominates the landing page;
- CI badge linked to the real workflow;
- screenshots must later come from real application output.

Still pending outside the README:

- GitHub repository description/topics;
- optional homepage only if a meaningful destination exists;
- license decision.

Those belong to PR8 because the currently available connector does not expose repository-settings writes.

---

## 7. PR2 — Architecture and engineering story — IMPLEMENTED

`docs/ARCHITECTURE.md` now describes the current architecture including:

- modular-monolith/local-first rationale;
- current epistemic authority model;
- current end-to-end evidence/data flow;
- accepted P1.6 factual substrate as a fan-out authority boundary;
- Capability Intelligence v9;
- Job Work Intelligence v2;
- Canonical Concept Registry;
- Market/report boundaries;
- public corpus vs runtime authority;
- selected review snapshots;
- experimental Blueprint isolation;
- failure semantics;
- browser/CLI shared-service architecture;
- security/privacy boundaries;
- current contracts/acceptance anchors;
- current P2.2B boundary and planned evolution.

The architecture diagram is maintained as repository text so it remains reviewable and versionable without external diagram tooling.

No ADR bureaucracy is required yet. Add an ADR only if a major durable choice benefits from a focused decision record beyond the architecture document itself.

---

# Part II — Information architecture and source maintainability

## 8. PR3 — Documentation information architecture — NEXT

**Goal:** Keep deep engineering history while giving external readers a clean navigation path.

Before moving files, classify the documentation families:

```text
CURRENT PRODUCT / PUBLIC
ARCHITECTURE / DESIGN
DEVELOPER / OPERATIONS
DECISION RECORD
CURRENT EXECUTION PLAN
HISTORICAL PLAN
EXPERIMENT / RESEARCH
WORKING MEMORY / HANDOFF
SUPERSEDED / DUPLICATED
```

Then design the smallest useful target hierarchy. Candidate families may include:

```text
docs/product/
docs/architecture/
docs/development/
docs/operations/
docs/decisions/
docs/plans/
docs/experiments/
docs/working-memory/
```

Do not adopt that structure mechanically. The audit must determine which boundaries are worth the move.

Required outputs:

- concise `docs/README.md` or equivalent documentation map;
- current controlling/product docs immediately discoverable;
- internal/historical material clearly separated from normal reviewer navigation;
- stale current-state statements identified and reconciled;
- broken links/references prevented;
- no duplicate current source of truth.

If large-scale file movement creates more churn than value, prefer a strong index + explicit historical/current labeling over mass relocation.

---

## 9. PR4 — Historical/versioned source disposition

**Goal:** Make current runtime paths obvious without sacrificing reproducibility.

For each versioned source/test/script family:

1. build import/reference map;
2. identify current runtime dependencies;
3. identify historical-artifact compatibility/replay needs;
4. identify regression-test dependencies;
5. identify research-only code;
6. prove any genuinely unreferenced code;
7. choose:

```text
KEEP IN PLACE
ISOLATE AS HISTORICAL/COMPATIBILITY
ARCHIVE OUTSIDE CURRENT RUNTIME PACKAGE
REMOVE AFTER PROOF
```

No mass deletion.

---

## 10. PR5 — Current-code structure and readability

**Goal:** Make important current code understandable to another engineer without over-engineering.

Audit and selectively improve:

- module responsibility boundaries;
- large web route/orchestration files;
- CLI command organization;
- service construction/dependency wiring;
- Registry/Work Intelligence boundaries;
- names/public interfaces;
- type annotations;
- comments/docstrings for important invariants and cross-file data flow;
- genuinely redundant wrappers/helpers;
- test organization around current public behavior.

Rules:

- split by responsibility, not arbitrary line counts;
- prefer explicit modules over generic frameworks;
- preserve current behavior and persisted contracts;
- no dependency-injection framework without demonstrated need;
- runtime changes require targeted regression plus normal quality gates.

---

# Part III — Demonstrability and developer experience

## 11. PR6 — Reproducible demo / public-corpus experience

**Goal:** Let an external reviewer experience meaningful JobHunter output with minimal setup.

Preferred path:

- reuse committed `corpus/` rather than fabricate data;
- select one or two representative accepted jobs;
- demonstrate source → English projection → P1.6 → Capability, plus Work Intelligence/Registry where repository-safe evidence is available;
- avoid requiring live acquisition merely to understand the product;
- avoid requiring LM Studio for read-only committed-output inspection;
- state clearly which workflows do require SQLite/local runtime/LM Studio.

Potential justified outputs:

- `docs/demo/` walkthrough;
- 2–4 real browser screenshots;
- concise expected CLI/corpus output;
- a tiny read-only helper only if existing commands/files cannot provide an adequate experience.

Do not create a separate fake demo application.

---

## 12. PR7 — Installation and developer onboarding

Validate and document:

```text
Python 3.12+
installation
configuration
public-corpus inspection
browser launch
CLI entrypoints
optional LM Studio setup
optional live Jobinja acquisition
running tests
linting
warnings-as-errors
expected local-only files
common setup boundaries
```

Add `CONTRIBUTING.md` only if it provides real value beyond README/development documentation.

Avoid Makefiles/task runners that only wrap already-simple commands.

---

# Part IV — Repository quality and release

## 13. PR8 — Open-source/repository hygiene

Audit and address where justified:

- license decision/file;
- `pyproject.toml` metadata;
- GitHub description/topics;
- project URLs;
- configuration examples;
- `.gitignore` completeness;
- accidental secret/private-data risk;
- public-corpus privacy boundary;
- dependency ranges/rationale;
- CI reliability/badge;
- optional dependency/security automation only if maintainable;
- `SECURITY.md` only if it can state a meaningful reporting/security model;
- stale/broken links;
- dead scripts/temporary artifacts only after proof;
- repository terminology consistency.

Do not add badges, bots, templates, CODEOWNERS, issue forms, or community files purely as decoration.

---

## 14. PR9 — Portfolio release and CV/interview package

Only after PR0–PR8 acceptance:

1. establish an intentional project version/release label;
2. create a GitHub release/tag with truthful release notes;
3. ensure README/screenshots/architecture match that release;
4. prepare truthful CV project wording;
5. prepare:

```text
30-second recruiter summary
2–3 minute hiring-manager explanation
10–15 minute technical architecture walkthrough
```

6. prepare talking points for:

- problem/product motivation;
- local-first rationale;
- source/provenance model;
- deterministic vs LLM reasoning;
- semantic-review boundary;
- SQLite/artifact/versioning strategy;
- acquisition safety/failure handling;
- public-corpus design;
- tests/CI and important regressions;
- tradeoffs and future scale changes;
- how AI assistance was directed, reviewed, validated, and incorporated into project ownership.

Do not claim a production user base, scale, accuracy level, or automation capability that has not been demonstrated.

---

## 15. Validation rules

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

### Runtime refactor

Require:

- targeted tests;
- `ruff check .`;
- `pytest`;
- `pytest -W error`;
- no persisted-contract/currentness changes unless separately authorized;
- local/live acceptance only when behavior cannot be validated remotely.

### Removal

Require proof of:

- no current imports/references;
- no runtime compatibility role;
- no accepted historical-artifact reproducibility requirement;
- no unique regression value;
- Git history sufficient for discarded material.

---

## 16. Portfolio-readiness acceptance criteria

### Public understanding

- [ ] GitHub metadata professional and accurate.
- [x] README explains the product before implementation chronology.
- [ ] real screenshots/visual product evidence exist.
- [x] current, experimental, limited, and future capabilities are separated.
- [x] technology stack and engineering differentiators are visible without hype.

### Architecture

- [x] architecture documentation matches current implementation.
- [x] architecture/data-authority diagram exists in repository-maintained text.
- [x] modular-monolith/SQLite/local-first choices are explainable.
- [x] deterministic/model/review authority boundaries are explicit.

### Code

- [ ] current runtime paths are obvious to a new engineer.
- [ ] historical/versioned code has intentional documented disposition.
- [ ] no known dead/temporary source clutter remains without reason.
- [ ] major modules have defensible responsibility boundaries.
- [ ] important invariants/data flows are understandable.

### Documentation

- [ ] external-reader documentation path is concise.
- [ ] deep governance/history does not dominate normal navigation.
- [ ] stale current-state documentation is reconciled.
- [ ] repository links are valid after any reorganization.

### Demo / onboarding

- [x] committed public corpus can be inspected without live acquisition/LM Studio.
- [x] README states LM Studio/local-runtime boundaries at a high level.
- [ ] fresh-clone install/test/run path receives dedicated final verification.
- [ ] real demo walkthrough/screenshots are present.

### Quality / hygiene

- [x] CI is visible in README.
- [x] tests/linting commands are visible.
- [ ] package metadata is portfolio-ready.
- [ ] license status is intentional.
- [ ] final privacy/secret exposure audit is complete.

### CV readiness

- [ ] stable tagged portfolio release exists.
- [ ] CV project description is finalized.
- [ ] short, medium, and deep interview explanations are prepared.
- [ ] owner learning/mastery pass covers major architectural tradeoffs and important code/data flows.

---

## 17. Exact next action

Do not begin source-code cleanup yet.

Next:

```text
PR3 documentation information-architecture audit
→ classify current/public vs internal/history document families
→ design the smallest useful navigation/hierarchy change
→ add a professional docs entry path
→ move files only when the benefit clearly exceeds reference churn
```

P2.2B product work remains paused at the existing machine-local `ta9l` P1.6 gate until system access returns. Portfolio work must not bypass that product gate.
