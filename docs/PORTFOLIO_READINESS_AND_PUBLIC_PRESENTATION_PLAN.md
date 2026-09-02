# JobHunter Portfolio Readiness and Public Presentation Plan

**Status:** APPROVED / CONTROLLING TEMPORARY REPOSITORY-QUALITY TRACK — PLAN ONLY / NO CLEANUP IMPLEMENTATION YET  
**Date:** 2026-09-02  
**Scope:** Make the public JobHunter repository professional, understandable, demonstrable, maintainable, and credible as a CV/portfolio project without weakening or rewriting accepted product semantics.  
**Relationship to product work:** P2.2B-B1 remains the current product-development gate and is locally blocked on `ta9l` P1.6 acceptance. This portfolio-readiness track may proceed while that local blocker exists, but it does not authorize new product features, semantic-contract changes, registry promotion, or reopening accepted layers.

---

## 1. Objective

Prepare JobHunter so that a recruiter, hiring manager, senior engineer, or technical interviewer can open the GitHub repository and quickly understand:

1. what problem the project solves;
2. what is actually implemented today;
3. what makes the engineering non-trivial;
4. how the architecture works;
5. how source truth, LLM reasoning, and reviewed authority are separated;
6. how to run or inspect the project safely;
7. how quality, testing, provenance, privacy, and failure handling are enforced;
8. which parts are current, experimental, historical, or future work;
9. what design decisions were made and why;
10. that the repository is intentionally engineered rather than an unstructured accumulation of AI-generated code.

The target is **professional technical credibility**, not visual decoration or artificial complexity.

---

## 2. Reviewer journeys to optimize

The repository must work for four different review depths.

### 2.1 Recruiter / first-pass reviewer — about 30–90 seconds

They should immediately see:

- a concise project identity and value proposition;
- major implemented capabilities;
- primary technology stack;
- one clean architecture visual;
- screenshots or a visual product preview;
- current maturity/status;
- how the project differs from a simple scraper or generic LLM wrapper.

They should not need to understand internal artifact IDs, historical prompt generations, working-memory files, or experimental chronology first.

### 2.2 Hiring manager — about 3–5 minutes

They should be able to understand:

- the end-to-end product workflow;
- current features and limitations;
- architecture and major boundaries;
- local-first/privacy rationale;
- deterministic-versus-model responsibilities;
- persistence/provenance strategy;
- tests and CI;
- public-corpus/demo path.

### 2.3 Senior engineer / technical interviewer — about 10–30 minutes

They should be able to inspect:

- package/module boundaries;
- important service/data flows;
- current versus historical implementations;
- failure semantics and safety boundaries;
- schema/artifact versioning rationale;
- testing strategy and representative regression coverage;
- source acquisition constraints;
- canonicalization/review architecture;
- design tradeoffs and known limitations.

### 2.4 Developer cloning the repository

They should have a reliable route from:

```text
clone
→ install
→ configure
→ inspect/demo
→ run tests
→ optionally run the local application
```

A reviewer who does not have Jobinja acquisition access or LM Studio configured should still be able to understand and inspect meaningful committed project output where practical.

---

## 3. Permanent rules for this track

1. **Do not redesign architecture merely for CV appearance.** The local Python modular monolith + SQLite + FastAPI/browser + CLI architecture remains valid unless a measured product or maintainability problem justifies change.
2. **Do not introduce microservices, Kubernetes, React, vector databases, queues, cloud infrastructure, or other fashionable technology solely for portfolio signaling.**
3. **Do not hide important engineering history by rewriting Git history.** Use organization, documentation, archival boundaries, and Git history appropriately.
4. **Do not delete historical/versioned source modules until references, imports, tests, reproducibility needs, artifact compatibility, and runtime dependencies are audited.**
5. **Do not change accepted semantic behavior as a side effect of cleanup.** A presentation/refactor task that exposes a material semantic defect must stop and route that defect through the normal product governance.
6. **Do not reopen P1.6, Capability v9, P2.1, or P2.2A for harmless wording/style differences.**
7. **Do not publish private/local state.** SQLite runtime data, raw local evidence paths, secrets, private personal evidence, model raw protocol history, or other excluded state remains outside repository publication.
8. **Do not over-document.** Public-facing documentation should be concise and layered; deep governance/history remains available without dominating the entry path.
9. **Do not add ceremonial files simply because popular repositories have them.** Every new file must serve a real reviewer, contributor, security, licensing, or operational need.
10. **Do not misrepresent AI-assisted development.** The repository should demonstrate human project ownership through problem framing, architecture, evidence boundaries, acceptance criteria, validation, design decisions, and technical understanding rather than pretending AI assistance did not occur.
11. **Keep claims accurate.** README, CV copy, diagrams, screenshots, release notes, and repository metadata must distinguish implemented/current, experimental, deferred, and planned capabilities.
12. **Preserve one source of truth per concern.** Public summaries may link to deeper documents but should not create conflicting parallel specifications.

---

## 4. Finding classification

Every portfolio-readiness finding must be classified before action:

```text
KEEP
already professional and appropriate

POLISH
content is fundamentally correct but wording/presentation/discoverability needs improvement

REORGANIZE
content/code is useful but located or grouped poorly for public understanding

REFACTOR
current code structure creates a real maintainability/readability problem

ARCHIVE
historical/research material is worth retaining but should not look current

REMOVE
provably obsolete/redundant repository content with no current or reproducibility value

ADD
a missing artifact or capability is justified by portfolio/developer usability
```

`REMOVE` requires stronger evidence than `ARCHIVE` or `REORGANIZE`.

---

## 5. Current known portfolio-readiness issues

These are initial evidence-backed findings, not yet permission to change each item.

### 5.1 GitHub repository landing metadata

Current GitHub metadata lacks a repository description, topics, homepage, and license declaration.

Needed review:

- concise GitHub description;
- useful topics/tags;
- license decision based on actual intended sharing/reuse policy;
- optional homepage only if a meaningful destination later exists;
- repository feature settings only where they improve public use.

### 5.2 README is technically strong but not optimized as a portfolio landing page

Current README accurately exposes deep internal contract/state detail, but the first reviewer path should prioritize:

```text
problem
→ product
→ features
→ screenshots/demo
→ architecture
→ engineering highlights
→ quick start
→ current status/limitations
→ deeper documentation
```

Internal prompt/schema/artifact identities remain valuable in deeper technical sections/docs, but should not dominate the first-screen narrative.

### 5.3 Architecture documentation is behind current implementation

`docs/ARCHITECTURE.md` predates accepted Canonical Registry and Job Work Intelligence work and therefore no longer describes the complete current system.

It must eventually include, at minimum:

- Canonical Concept Registry;
- Job Work Intelligence v2;
- current review/promotion boundaries;
- current public/private projection boundaries;
- accurate current end-to-end flow;
- current versus experimental/deferred layers.

### 5.4 Public documentation hierarchy is too dense for external readers

The `docs/` root contains current product specifications, plans, amendments, experiments, acceptance plans, operational documents, and historical evolution material in one highly visible namespace.

The information is valuable, but reviewer navigation needs a clearer hierarchy such as:

```text
public/current product docs
architecture/design
operations/development
engineering decisions
internal execution plans/history
experiments/working memory
```

Any move/reorganization must preserve links or update references systematically.

### 5.5 Historical/versioned implementation accumulation is highly visible

The current source package contains many historical implementations, including multiple `analysis_runtime_v*` generations and related versioned modules/tests.

This history may be necessary for reproducibility and historical artifact support, but currently it makes the package appear less intentionally organized.

Before any action, each versioned module must be classified as:

```text
CURRENT RUNTIME
CURRENT COMPATIBILITY / HISTORICAL ARTIFACT SUPPORT
TEST / REGRESSION SUPPORT
EXPERIMENTAL / RESEARCH
DEAD / UNREFERENCED
```

Only after this dependency audit may we decide whether to keep in place, isolate under an explicit historical/compatibility package, archive, or remove.

### 5.6 Some modules may have grown beyond clear responsibility boundaries

Examples requiring evidence-based review include large orchestration modules such as `src/jobhunter/web/app.py` and other large registry/workflow/CLI modules.

The goal is not arbitrary file-size reduction. Refactor only where there is a natural responsibility boundary that improves:

- readability;
- testability;
- dependency direction;
- discoverability;
- developer comprehension;
- change isolation.

### 5.7 Visual/demo presentation is weak relative to actual product capability

The project has a real browser UI and committed public corpus, but the repository does not currently make that visible enough to an external reviewer.

Potential justified outputs:

- 2–4 representative screenshots;
- one architecture diagram;
- one end-to-end example walkthrough using a committed public job;
- a demo/read-only path that does not require live acquisition or local LLM inference where feasible;
- sample CLI output only when it adds value.

### 5.8 Developer onboarding needs a dedicated audit

Review the complete fresh-clone experience:

- Python version;
- installation command;
- configuration setup;
- optional LM Studio dependency;
- what works without LM Studio;
- how to run tests;
- how to launch browser/CLI;
- how to inspect the public corpus;
- expected local-only files;
- troubleshooting for common setup boundaries.

### 5.9 Package metadata and release surface are incomplete

Audit:

- `pyproject.toml` project metadata;
- package/project description;
- authorship fields only if useful and accurate;
- license metadata after license decision;
- project URLs if justified;
- dependency grouping;
- script discoverability;
- version/release policy;
- first intentional portfolio release/tag after readiness work is accepted.

### 5.10 Quality/security strengths are not sufficiently surfaced

Existing strengths include CI, Ruff, pytest, warnings-as-errors, source allowlisting, bounded acquisition, provenance, CSRF/security headers, public/private projection boundaries, and fail-closed semantic promotion.

These should be visible as engineering highlights without turning the README into a security specification.

---

# Part I — Audit before changes

## 6. PR0 — Full portfolio-readiness audit

**Goal:** Build one evidence-backed issue inventory before structural cleanup.

### 6.1 Repository surface audit

Inspect:

- GitHub repository metadata/settings visible to public reviewers;
- root files;
- `.github/` workflows;
- `README.md`;
- package metadata/config examples;
- `src/`;
- `tests/`;
- `docs/`;
- `corpus/`;
- `review-snapshots/`;
- scripts/tools;
- ignored/local-only boundaries;
- current release/tag state.

### 6.2 Source dependency/structure audit

Produce an explicit inventory of:

- current public entrypoints;
- runtime modules;
- compatibility/history modules;
- versioned semantic implementations;
- experimental code;
- large/high-coupling modules;
- circular or awkward dependency risks if any;
- dead/unreferenced modules if any;
- duplicate responsibilities if any.

Do not infer dead code from filenames alone.

### 6.3 Documentation audit

For every significant documentation family classify:

- current controlling/public;
- developer/operations;
- decision record;
- historical plan;
- experiment;
- working memory;
- obsolete/duplicated.

Identify stale statements and broken navigation.

### 6.4 Public claims audit

Cross-check README, architecture, product specification, roadmap, package metadata, and GitHub metadata against actual code/current acceptance.

Every public claim must be one of:

```text
implemented/current
implemented/experimental
implemented/deferred
planned
historical
```

### 6.5 Fresh-clone and demo-path audit

Determine exactly what an external developer can do:

- with only Python + repository;
- with committed public corpus but no LM Studio;
- with LM Studio configured;
- with live Jobinja acquisition enabled.

This audit defines the future Quick Start and demo story.

### PR0 deliverable

Create one portfolio-readiness audit record containing:

```text
finding
category: KEEP/POLISH/REORGANIZE/REFACTOR/ARCHIVE/REMOVE/ADD
severity: critical/high/medium/low
reviewer impact
technical evidence
recommended action
risk if changed
validation required
proposed phase
```

No broad cleanup should precede this inventory.

---

# Part II — Public-facing professional presentation

## 7. PR1 — GitHub landing page and README

**Goal:** Make the repository understandable and compelling within the first few minutes.

Expected README structure:

```text
JobHunter
short value proposition
visual preview / screenshots
what it does today
why it is technically interesting
architecture at a glance
major features
engineering/trustworthiness highlights
technology stack
quick start / demo
current maturity and limitations
project structure
testing
documentation map
roadmap direction
license
```

Requirements:

- no inflated claims;
- current features separated from future roadmap;
- experimental Blueprint clearly labeled;
- local-first and LM Studio role explained in practical language;
- provenance/authority design summarized as a differentiator;
- internal contract IDs moved below the main product story or into technical docs where appropriate;
- CI badge only after confirmed workflow/status reliability;
- screenshots added only from real application output.

Also update GitHub description/topics once the wording is final.

---

## 8. PR2 — Architecture and engineering story

**Goal:** Present one accurate current-system model suitable for a technical reviewer/interview.

Required outputs:

1. reconcile `docs/ARCHITECTURE.md` with current implementation;
2. add one clean architecture diagram maintained as repository text/source where practical;
3. document current data/authority flow including:

```text
Jobinja source
→ immutable evidence / source version
→ English projection
→ accepted P1.6 factual substrate
→ Capability Intelligence
→ Job Work Intelligence
→ reviewed Canonical Registry mappings
→ later market/personal intelligence
```

4. distinguish runtime authority from repository-safe projections;
5. distinguish deterministic logic from model reasoning;
6. explain why modular monolith + SQLite + server-rendered FastAPI UI are intentional current choices;
7. document meaningful design tradeoffs rather than listing technologies;
8. link deeper source-policy/domain/governance documents without duplicating them.

Potential ADRs (Architecture Decision Records) should be introduced only if they improve understanding of a small number of major durable choices. Do not create ADR bureaucracy retroactively for every historical decision.

---

## 9. PR3 — Documentation information architecture

**Goal:** Keep deep engineering history while giving external readers a clean path.

Design a documentation hierarchy before moving files.

Possible target families:

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

The exact structure must be chosen from the audit rather than copied mechanically.

Requirements:

- add a concise documentation index/map;
- make current controlling documents obvious;
- make historical plans visibly historical;
- preserve working-memory/experiment evidence without placing it on the normal reviewer path;
- update all internal references if files move;
- verify no broken repository links;
- avoid duplicate current-state documents.

---

# Part III — Source structure and maintainability

## 10. PR4 — Historical/versioned source disposition

**Goal:** Make the current implementation obvious without sacrificing reproducibility.

For every versioned semantic source/test family:

1. build import/reference map;
2. identify runtime and historical artifact dependencies;
3. identify compatibility/replay needs;
4. classify tests using each implementation;
5. identify truly unreferenced code;
6. choose one disposition:

```text
KEEP IN PLACE
ISOLATE AS HISTORICAL/COMPATIBILITY
ARCHIVE OUTSIDE CURRENT RUNTIME PACKAGE
REMOVE AFTER PROOF
```

Desired end state:

- current runtime paths are obvious;
- historical implementations remain intentionally discoverable when necessary;
- names/directories communicate status;
- old files do not look accidentally abandoned;
- tests preserve relevant regression/reproducibility contracts.

No mass deletion.

---

## 11. PR5 — Current-code structure and readability

**Goal:** Make important current code understandable to another engineer without over-engineering.

Audit and selectively improve:

- module responsibility boundaries;
- large route/orchestration files;
- CLI command organization;
- service construction/dependency wiring;
- registry/work-intelligence boundaries;
- type annotations;
- names and public interfaces;
- docstrings/comments for non-obvious invariants and cross-file data flow;
- removal of genuinely redundant wrappers/helpers;
- test organization around current public behavior.

Rules:

- split by responsibility, not arbitrary line counts;
- prefer explicit modules over generic abstractions;
- preserve current external behavior and persisted contracts;
- avoid dependency-injection frameworks or architectural layers without demonstrated value;
- any runtime refactor requires targeted regression tests plus normal repository quality gates.

---

# Part IV — Demonstrability and developer experience

## 12. PR6 — Reproducible demo / public-corpus experience

**Goal:** Let an external reviewer experience meaningful JobHunter output with minimal setup.

Audit and implement the smallest useful demo path from committed public data.

Preferred approach:

- reuse `corpus/` rather than fabricate sample results;
- select one or two representative jobs;
- show source → English → factual analysis → Capability → Work Intelligence/registry where repository-safe data exists;
- avoid requiring live scraping merely to understand the product;
- avoid requiring a local LLM for read-only inspection when committed artifacts can demonstrate the feature;
- clearly state which operations require LM Studio or local runtime state.

Potential outputs:

- `docs/demo/` walkthrough;
- simple read-only command/script only if existing CLI/corpus commands cannot provide a good experience;
- representative screenshots;
- concise expected-output examples.

Do not build a separate fake demo application.

---

## 13. PR7 — Installation and developer onboarding

**Goal:** Make a clean clone understandable and runnable.

Validate and document:

```text
Python 3.12+
installation
configuration
public-corpus inspection
browser launch
CLI entrypoints
optional LM Studio setup
optional live acquisition
running tests
linting
warnings-as-errors
local files that must stay uncommitted
```

Decide whether a dedicated `CONTRIBUTING.md` is useful based on actual content. For a solo portfolio project it should be added only if it materially improves developer onboarding beyond README/development docs.

Avoid adding Makefiles/task runners merely to wrap already-simple commands unless audit evidence shows command discoverability is a real problem.

---

# Part V — Repository quality, security, and release

## 14. PR8 — Open-source/repository hygiene

**Goal:** Remove avoidable credibility gaps in the public repository surface.

Audit and address where justified:

- license decision and file;
- `pyproject.toml` metadata;
- GitHub description/topics;
- project URLs;
- environment/config examples;
- `.gitignore` completeness;
- accidental secret/private-data risk;
- public-corpus privacy boundary;
- dependency pin/range rationale;
- CI reliability and badge;
- optional dependency/security update automation only if maintainable;
- `SECURITY.md` only if it can state a meaningful vulnerability-reporting/security model;
- stale/broken links;
- dead scripts or temporary development artifacts;
- repository naming/terminology consistency.

Do not add badges, bots, templates, CODEOWNERS, issue forms, or community files purely as decoration.

---

## 15. PR9 — Portfolio release and CV/interview package

**Goal:** Produce a stable point that can be linked from a CV.

Only after PR0–PR8 acceptance:

1. establish an intentional project version/release label;
2. create a GitHub release/tag with concise real release notes;
3. ensure screenshots/README/architecture reflect that release;
4. write a truthful CV project description;
5. prepare 3 levels of explanation:

```text
30-second recruiter summary
2–3 minute hiring-manager explanation
10–15 minute technical-interview architecture walkthrough
```

6. prepare technical talking points covering:

- problem and product motivation;
- local-first rationale;
- source/provenance model;
- deterministic vs LLM reasoning boundary;
- structured inference and semantic-review boundary;
- SQLite/artifact/versioning strategy;
- acquisition safety/failure handling;
- public-corpus design;
- tests/CI and key regressions;
- tradeoffs and what would change at larger scale;
- how AI assistance was directed, validated, and incorporated into engineering ownership.

Do not claim a production user base, scale, accuracy level, or automation capability that has not been demonstrated.

---

## 16. Execution order

Follow this order unless an audit finding proves a dependency requires adjustment:

```text
PR0  full readiness audit
 ↓
PR1  README + GitHub landing story
 ↓
PR2  architecture story/currentness
 ↓
PR3  documentation hierarchy
 ↓
PR4  historical/versioned source disposition
 ↓
PR5  current-code structure/readability
 ↓
PR6  demo + screenshots/public-corpus walkthrough
 ↓
PR7  installation/developer onboarding
 ↓
PR8  repository/security/package hygiene
 ↓
PR9  stable portfolio release + CV/interview package
```

Presentation/docs are intentionally addressed before invasive source cleanup so the desired public architecture/current-state story is explicit before code is reorganized.

PR4 and PR5 may be skipped or narrowed if PR0 demonstrates that current source structure is defensible and cleanup would create more risk than value.

---

## 17. Validation by change type

### Documentation/presentation-only

Require:

- factual current-state cross-check;
- link/path verification;
- no overclaiming;
- consistency with controlling product/governance docs.

### Repository metadata/package metadata

Require:

- install/build metadata remains valid;
- no accidental license/authorship/URL claims;
- current CLI entrypoints remain accurate.

### File moves/reorganization

Require:

- all references updated;
- imports unaffected or intentionally changed;
- documentation links verified;
- tests/CI where code paths are touched.

### Runtime refactor

Require:

- targeted tests for affected behavior;
- full Ruff + pytest + warnings-as-errors;
- no persisted-contract/currentness changes unless separately authorized;
- local/live acceptance only when the refactor touches behavior that cannot be validated remotely.

### Removal

Require proof of:

- no current imports/references;
- no runtime compatibility role;
- no accepted historical-artifact reproducibility requirement;
- no unique regression value;
- Git history sufficient for intentionally discarded material.

---

## 18. Portfolio-readiness acceptance criteria

The track is complete only when all of the following are true:

### Public understanding

- [ ] GitHub landing metadata is professional and accurate.
- [ ] README explains the product before internal implementation chronology.
- [ ] screenshots/visuals demonstrate real current behavior.
- [ ] current features, experimental features, limitations, and roadmap are clearly separated.
- [ ] technology stack and engineering differentiators are visible without hype.

### Architecture

- [ ] architecture documentation matches current implementation.
- [ ] one clean architecture/data-authority diagram exists.
- [ ] modular-monolith/SQLite/local-first choices are explainable.
- [ ] deterministic/model/review authority boundaries are clear.

### Code

- [ ] current runtime paths are obvious.
- [ ] historical/versioned code has an intentional documented disposition.
- [ ] no known dead/temporary source clutter remains without reason.
- [ ] major modules have defensible responsibility boundaries.
- [ ] important non-obvious invariants/data flows are understandable.

### Documentation

- [ ] external-reader documentation path is concise.
- [ ] deep governance/history remains available but does not dominate navigation.
- [ ] stale current-state documentation is reconciled.
- [ ] repository links are valid.

### Demo / onboarding

- [ ] a reviewer can inspect meaningful committed output without live acquisition.
- [ ] requirements for LM Studio/local runtime are explicit.
- [ ] fresh-clone install/test/run instructions are verified.

### Quality / hygiene

- [ ] CI is visible and reliable.
- [ ] tests/linting instructions are clear.
- [ ] package metadata is complete enough for the project’s actual distribution model.
- [ ] license status is intentional.
- [ ] repository contains no known private/local-only leakage.

### CV readiness

- [ ] one stable tagged portfolio release exists.
- [ ] CV project description is accurate and technically strong.
- [ ] short, medium, and deep interview explanations are prepared.
- [ ] the owner can explain major architectural tradeoffs and important code/data flows.

---

## 19. Exact next action

Do **not** begin random cleanup.

Next:

```text
execute PR0 full portfolio-readiness audit
→ produce one classified issue inventory
→ review the findings and proposed dispositions
→ then begin PR1 one bounded increment at a time
```

P2.2B product work remains paused at the existing local `ta9l` P1.6 gate until machine access returns. Portfolio work must not bypass that product gate.