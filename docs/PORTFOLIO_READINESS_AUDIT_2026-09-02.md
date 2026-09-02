# JobHunter Portfolio Readiness Audit

**Status:** PR0 COMPLETE / EVIDENCE-BACKED AUDIT / NO CLEANUP IMPLEMENTED  
**Date:** 2026-09-02  
**Controlling track:** `docs/PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md`  
**Product-work boundary:** P2.2B-B1 remains paused at the machine-local `ta9l` P1.6 acceptance gate. This audit does not change semantic contracts, accepted artifacts, registry authority, or product behavior.

---

## 1. Executive verdict

JobHunter already has enough engineering substance to be a strong portfolio project. The primary portfolio problem is **presentation and information architecture, not lack of technical depth**.

The current repository demonstrates:

- a coherent local-first Python modular-monolith architecture;
- SQLite runtime/history authority plus immutable source evidence;
- bounded public Jobinja acquisition with explicit failure/lifecycle semantics;
- a local LM Studio translation and structured-inference boundary;
- strict factual P1.6 extraction with semantic review;
- accepted Capability Intelligence;
- accepted Job Work Intelligence v2;
- a reviewed Canonical Concept Registry;
- browser and CLI surfaces over shared services/state;
- a deterministic repository-safe public corpus;
- curated review snapshots;
- substantial regression tests;
- CI running Ruff, pytest, and pytest with warnings treated as errors;
- deliberate privacy, provenance, security, and public/private-state boundaries.

The repository therefore should **not** be redesigned into microservices, cloud services, a SPA, Kubernetes, a vector platform, or other portfolio-driven infrastructure.

The current weakness is that an external reviewer sees too much internal development chronology before the clean current product story. Current implementation, historical semantic generations, experiments, governance, plans, and acceptance records are all valuable, but their presentation is not yet layered by audience.

### PR0 decision

```text
KEEP the architecture and trust/provenance model
→ POLISH the GitHub/README public story first
→ reconcile current architecture documentation
→ REORGANIZE documentation/history visibility
→ dependency-audit historical code/scripts/tests before moving anything
→ selectively REFACTOR only real current maintainability problems
→ build a real corpus-backed demo and screenshots
→ finish package/release/CV presentation last
```

No `REMOVE` action is authorized by PR0. The audit found visible historical accumulation, but not enough dependency evidence to prove any historical source, test, or script is safely disposable.

---

## 2. Portfolio scorecard

| Area | Current judgment | Primary disposition |
| --- | --- | --- |
| Product substance | Strong | KEEP / POLISH presentation |
| Core architecture | Strong and defensible | KEEP |
| Evidence/provenance model | Distinctive strength | KEEP / POLISH visibility |
| LLM/deterministic authority boundaries | Distinctive strength | KEEP / POLISH visibility |
| Browser + CLI product surfaces | Strong | KEEP / ADD visual demonstration |
| Testing and CI | Strong | KEEP / POLISH visibility |
| Source/security/privacy boundaries | Strong | KEEP / POLISH visibility |
| README / first-pass reviewer experience | Weak relative to implementation | POLISH |
| Architecture-document currentness | Stale relative to current main | POLISH |
| Documentation navigation | Too internally dense | REORGANIZE |
| Current-vs-historical source discoverability | Weak | REORGANIZE / ARCHIVE candidate after dependency audit |
| Current code responsibility boundaries | Mostly defensible; selected large modules need review | REFACTOR candidate |
| Demoability without local runtime | Strong latent capability, weak presentation | ADD / POLISH |
| Fresh-clone onboarding | Functional basics exist, but path is fragmented | POLISH / ADD |
| GitHub metadata | Incomplete | POLISH / ADD |
| Package/release metadata | Minimal | POLISH / ADD |
| Stable portfolio release | Missing | ADD later |
| CV/interview narrative | Strong raw material, not packaged | ADD later |

---

## 3. Findings by priority

### F01 — GitHub landing metadata is incomplete

**Category:** POLISH / ADD  
**Severity:** HIGH  
**Reviewer impact:** Immediate. This is visible before a reviewer opens any file.

**Evidence:** Public repository metadata currently has no description, no topics, no homepage, and no declared license.

**Recommended action:**

- add a concise product description after README wording is finalized;
- add a small set of accurate topics such as Python, FastAPI, local-first, LLM, career-intelligence, SQLite, provenance;
- make an explicit license decision rather than copying a license by convention;
- leave homepage empty unless a real useful destination exists.

**Risk if changed:** Incorrect license or inflated metadata can create legal/credibility problems.

**Validation:** Cross-check wording with current implemented features and chosen license intent.

**Phase:** PR1 for description/topics; PR8 for license/package metadata.

---

### F02 — README is internal-state-first rather than portfolio-first

**Category:** POLISH  
**Severity:** HIGH

**Reviewer impact:** A recruiter or hiring manager must process internal contract IDs, artifact numbers, Phase/P1.6 terminology, acceptance chronology, and governance links before seeing the simplest product story.

**Evidence:** The README begins correctly with `local-first personal career-intelligence application`, but its primary technical narrative rapidly moves into semantic contract identities and accepted artifact anchors. Its suggested starting documents include `AGENTS.md`, execution TODOs, semantic acceptance plans, and working memory. The current near-term sequence is also written in internal phase language.

**Recommended action:** Rewrite README around:

```text
problem / value
→ what works today
→ visual preview
→ architecture at a glance
→ key engineering decisions
→ technology stack
→ quick inspect/run path
→ testing
→ current limitations
→ deeper documentation
```

Keep exact contract/version detail in deeper technical documentation and a compact current-status section.

**Risk if changed:** Oversimplifying could erase the project's strongest engineering differentiators.

**Validation:** Every public claim must map to current code/governance and keep experimental/deferred status explicit.

**Phase:** PR1.

---

### F03 — README is stale relative to current accepted implementation

**Category:** POLISH  
**Severity:** HIGH

**Reviewer impact:** The project appears less capable than it is and gives an incomplete architecture picture.

**Evidence:** The visible accepted-stack narrative stops at P1.6 → Capability and the near-term sequence ends around the Canonical Registry. Current main additionally contains accepted P2.1 Canonical Registry and accepted P2.2A Job Work Intelligence v2, with browser/CLI surfaces for both.

**Recommended action:** Reconcile current feature/status summary with current main while keeping P2.2B and later work clearly unfinished.

**Risk if changed:** Accidentally presenting candidate/promotion work as completed.

**Validation:** Compare with `AGENTS.md`, `EXECUTION_TODO.md`, `WORKING_MEMORY.md`, and accepted implementation/tests.

**Phase:** PR1.

---

### F04 — Architecture document is substantively good but materially stale

**Category:** POLISH  
**Severity:** HIGH

**Reviewer impact:** Senior reviewers receive an outdated end-to-end model.

**Evidence:** `docs/ARCHITECTURE.md` is dated 2026-08-16 and currently describes the main analytical flow through P1.6 → Capability → first Market, plus experimental Blueprint. It predates the accepted Canonical Registry and Job Work Intelligence v2 layers.

**Recommended action:** Preserve the modular-monolith design and permanent principles, but update:

- current end-to-end flow;
- Work Intelligence;
- Canonical Registry;
- candidate vs promoted authority;
- current browser/CLI surfaces;
- current vs experimental/deferred layers;
- repository-safe projections;
- one clean reviewer-facing architecture diagram.

**Risk if changed:** Duplicating product/domain policy or turning architecture into another history log.

**Validation:** Cross-check actual current modules and accepted state.

**Phase:** PR2.

---

### F05 — Documentation currentness drift is already observable

**Category:** POLISH / REORGANIZE  
**Severity:** HIGH

**Reviewer impact:** Conflicting numbers/statuses reduce trust in otherwise rigorous documentation.

**Evidence:** Current README/governance report 353 discovered jobs and 20 current English projections. `review-snapshots/README.md` still reports an older publication baseline of 344 discovered jobs and 33 English projections. The difference is historical/currentness drift, not merely wording preference.

**Recommended action:** During PR2/PR3, identify which docs are current reference docs versus historical acceptance records. Current-facing docs should use one authoritative baseline or explicitly date/freeze the figure. Historical records should be visibly historical rather than silently updated to simulate history.

**Risk if changed:** Rewriting historical evidence instead of preserving it.

**Validation:** Current counts come from the current public corpus/governance; historical records retain their original dated values when intentionally historical.

**Phase:** PR2/PR3.

---

### F06 — `docs/` exposes too much execution chronology at one level

**Category:** REORGANIZE  
**Severity:** HIGH

**Reviewer impact:** The repository looks harder to understand than the actual architecture.

**Evidence:** Top-level `docs/` mixes current product specification, architecture, domain model, source policy, roadmap, implementation plan, operational docs, P1/P2 focused plans, amendments, proposals, experiments, TODO, and working-memory history.

**Recommended action:** Design a documentation map before moving anything. Likely public paths should separate:

- product/current architecture;
- development/operations;
- durable design decisions;
- plans/history;
- experiments;
- working memory.

Add one external-reader index. Keep governance depth available but off the default reviewer path.

**Risk if changed:** Broken internal links and governance routing.

**Validation:** Repository-wide reference/link audit before/after moves.

**Phase:** PR3.

---

### F07 — Historical semantic implementations are interleaved with current runtime code

**Category:** REORGANIZE / ARCHIVE CANDIDATE  
**Severity:** HIGH

**Reviewer impact:** A developer opening `src/jobhunter/` encounters many `analysis_runtime_v10.py` through `analysis_runtime_v20.py` and corresponding historical service families before understanding which path is current.

**Evidence:** `analysis_current.py` deliberately routes the current public contract to original-language v9 and English v20. It directly imports `analysis_runtime_v20` and the historical/base v9 runtime. This proves at least some versioned modules are still active compatibility/current dependencies. Therefore filenames alone cannot justify deletion.

**Recommended action:** Build a dependency/reference matrix for each versioned source family and classify each as:

```text
CURRENT_RUNTIME
COMPATIBILITY_REQUIRED
HISTORICAL_REPRODUCIBILITY
EXPERIMENTAL
DEAD/UNREFERENCED
```

Only then choose keep-in-place, isolate under explicit compatibility/history, archive, or remove.

**Risk if changed:** Breaking accepted artifact compatibility, replay/review behavior, imports, or regression evidence.

**Validation:** Import/reference search, targeted tests, full CI, and historical artifact requirements.

**Phase:** PR4.

---

### F08 — Historical test generations are valuable but visually noisy

**Category:** REORGANIZE / ARCHIVE CANDIDATE  
**Severity:** MEDIUM

**Reviewer impact:** The extensive test suite is a strength, but dozens of version-numbered candidate/regression tests make it difficult to identify tests for current public behavior.

**Evidence:** `tests/` includes current runtime/service/semantic-review tests alongside `test_analysis_v10_candidate.py`, `v11`, `v12`, ... `v20`, plus historical regression families.

**Recommended action:** Do not reduce coverage merely for aesthetics. After PR4 source classification, organize tests so current-contract tests are immediately discoverable and historical contract/reproduction tests are explicitly grouped.

**Risk if changed:** Losing regression evidence that explains why the current contract exists.

**Validation:** Full test collection/count comparison and CI.

**Phase:** PR4/PR5.

---

### F09 — `scripts/` also contains substantial historical audit generations

**Category:** REORGANIZE / ARCHIVE CANDIDATE  
**Severity:** MEDIUM

**Reviewer impact:** The repository exposes many one-generation audit scripts (`audit_blueprint_v3/v4/v5/v6`, multiple P1.6 candidate audits, Capability audits, etc.) without an obvious current-vs-historical navigation boundary.

**Recommended action:** Classify scripts by current operational need, historical acceptance/reproduction value, or dead/unreferenced state. Historical scripts may belong under a clearly labeled historical/verification area rather than the default operational script surface.

**Risk if changed:** Losing reproducibility of accepted/rejected semantic experiments.

**Validation:** Search docs/tests for script references and preserve unique decision evidence.

**Phase:** PR4.

---

### F10 — Current public entrypoints are actually clear and should be preserved

**Category:** KEEP  
**Severity:** LOW / POSITIVE

**Reviewer impact:** Strong developer-facing signal.

**Evidence:** `pyproject.toml` exposes explicit installed commands for the main app, browser app, review snapshots, public corpus, Canonical Registry, and Work Intelligence.

**Recommended action:** Keep the entrypoint model. Improve README discoverability instead of inventing a new command framework.

**Risk if changed:** Unnecessary CLI churn.

**Validation:** Existing entrypoint tests/install behavior.

**Phase:** PR1/PR7 presentation only.

---

### F11 — `web/app.py` is a legitimate selective-refactor candidate, not an emergency defect

**Category:** REFACTOR CANDIDATE  
**Severity:** MEDIUM

**Reviewer impact:** A technical reviewer sees a roughly 45 KB application module combining service factories, security helpers, operation orchestration, and many FastAPI routes.

**Evidence:** The web package already has useful focused modules (`capability.py`, `registry.py`, `work_intelligence.py`, `operations.py`, `queries.py`, etc.), so there are natural existing boundaries that could support further routing/assembly cleanup.

**Recommended action:** In PR5, map route groups and construction responsibilities. Split only where a coherent domain/router boundary improves comprehension and tests. Do not refactor by arbitrary line-count targets.

**Risk if changed:** Route/security/operation regressions and unnecessary abstraction.

**Validation:** targeted web tests + full CI; local browser acceptance only if behavior touched cannot be proven remotely.

**Phase:** PR5.

---

### F12 — Local-first modular monolith + SQLite is a portfolio strength

**Category:** KEEP  
**Severity:** LOW / POSITIVE

**Reviewer impact:** Demonstrates restraint and architecture tradeoff awareness.

**Evidence:** Architecture intentionally keeps browser and CLI over shared services/state, uses SQLite as canonical local structured/runtime state, retains raw evidence separately, and explicitly rejects premature microservices/vector/agent infrastructure.

**Recommended action:** Keep this architecture. Explain why it fits the product: one-user local utility, privacy, inspectability, transactional state, low operational burden, and measurable upgrade triggers.

**Risk if changed:** CV-driven overengineering would make the project less credible.

**Validation:** None beyond current accepted architecture.

**Phase:** PR2 presentation.

---

### F13 — Provenance and epistemic authority model is a major differentiator

**Category:** KEEP / POLISH  
**Severity:** LOW / POSITIVE

**Reviewer impact:** This distinguishes JobHunter from a generic scraper + LLM wrapper.

**Evidence:** Source evidence, deterministic parsing, English projection, strict factual extraction, analytical interpretation, candidate/promoted authority, exact dependencies/currentness, and reviewed canonical mappings are explicitly separated.

**Recommended action:** Surface this in plain engineering language in README and architecture. Do not expose the entire governance taxonomy in the first screen.

**Risk if changed:** Simplifying the story into “AI analyzes jobs” would erase technical depth.

**Validation:** Cross-check public explanation against domain/reasoning policy.

**Phase:** PR1/PR2.

---

### F14 — Public corpus is an unusually strong demo/reproducibility asset but is buried

**Category:** KEEP / POLISH / ADD  
**Severity:** HIGH

**Reviewer impact:** Reviewers currently may assume they need the owner's SQLite database, Jobinja network access, and LM Studio to see useful results.

**Evidence:** `corpus/` is a deterministic repository-safe projection of public Jobinja state and successful processing stages. It intentionally excludes SQLite, raw local evidence paths, prompts, model protocol responses, secrets, logs, and future private/personal state.

**Recommended action:** Make corpus inspection a first-class README/demo path. Select one or two representative accepted jobs and create a concise source → English → P1.6 → Capability walkthrough. Where Work Intelligence/Registry are not yet published in corpus, state that boundary honestly rather than fabricating demo artifacts.

**Risk if changed:** Accidentally publishing local/private or unpromoted state.

**Validation:** corpus contract/verify rules and public-state exclusions.

**Phase:** PR1 narrative; PR6 full demo.

---

### F15 — No visual product preview is available in the repository

**Category:** ADD  
**Severity:** HIGH

**Reviewer impact:** A working browser application is effectively invisible on the GitHub landing page.

**Evidence:** Repository inventory contains browser templates/static assets but no committed project screenshots/portfolio preview images were found.

**Recommended action:** When machine access returns, capture 2–4 real screenshots covering dashboard/jobs, accepted factual analysis/Capability, Work Intelligence, and Registry/review where useful. Avoid mockups presented as product output.

**Risk if changed:** Screenshots can leak source/private/local information or become stale.

**Validation:** use public-safe data, visually inspect redaction/currentness, and label experimental surfaces.

**Phase:** PR6; README can reserve the structure earlier without fake images.

---

### F16 — Fresh-clone setup exists but is not yet a clean layered onboarding journey

**Category:** POLISH / ADD  
**Severity:** MEDIUM

**Reviewer impact:** New developers must infer what can be done with only Python, what requires configuration, and what requires LM Studio/live acquisition.

**Evidence:** README provides Python 3.12+, editable install, `jobhunter-app`, CLI commands, and test commands. `jobhunter.toml.example` is detailed and useful, but model roles, search/acquisition settings, and translation options create substantial configuration surface.

**Recommended action:** Document four explicit modes:

```text
1. inspect repository/public corpus only
2. install + run deterministic tests
3. launch local app with local state/config
4. enable LM Studio and/or bounded live Jobinja acquisition
```

Avoid forcing full model/acquisition setup before a reviewer can inspect the project.

**Risk if changed:** Promising a read-only app mode that does not actually exist.

**Validation:** fresh-clone verification when local system access returns.

**Phase:** PR7, with concise PR1 Quick Start.

---

### F17 — CI is real, recent, and should be surfaced

**Category:** KEEP / POLISH  
**Severity:** LOW / POSITIVE

**Reviewer impact:** Strong credibility signal currently underused.

**Evidence:** GitHub CI runs on push to `main` and pull requests, installs Python 3.12 + dev dependencies, runs Ruff, pytest, and pytest with warnings as errors. The portfolio-plan commit `0b16ad5...` completed CI successfully on 2026-09-02.

**Recommended action:** Add a CI badge in PR1 after choosing final README layout. Keep validation commands visible.

**Risk if changed:** Badge becomes misleading if workflow is renamed/disabled.

**Validation:** confirmed successful workflow URL/status.

**Phase:** PR1.

---

### F18 — Security/privacy engineering is stronger than the public story suggests

**Category:** KEEP / POLISH  
**Severity:** MEDIUM / POSITIVE

**Reviewer impact:** Particularly valuable for security/AI-engineering roles.

**Evidence:** Current implementation/policy includes bounded source allowlisting, no authenticated-platform bypass behavior, retry classification, immutable evidence, untrusted-content treatment, CSRF checks, safe return paths, no-store, CSP, frame denial, no-referrer, content-type protection, ignored SQLite/evidence/log/secret paths, and repository-safe corpus exclusions.

**Recommended action:** Add a concise “trust & safety / engineering boundaries” section to README and link deeper source/security policy. Do not market the local app as internet-hardened multi-user software.

**Risk if changed:** Overclaiming security guarantees.

**Validation:** wording stays within implemented local-first threat model.

**Phase:** PR1/PR2/PR8.

---

### F19 — `.gitignore` and public/private runtime separation are appropriate

**Category:** KEEP  
**Severity:** LOW / POSITIVE

**Reviewer impact:** Shows deliberate repository hygiene.

**Evidence:** Local SQLite/WAL/SHM, evidence, logs, env/secrets, generated local exports, caches, and virtual environments are excluded; public corpus/review snapshots are intentionally distinct committed projections.

**Recommended action:** Keep. Re-audit before final release for accidental leakage, but do not replace with a complex secret-management system merely for appearance.

**Risk if changed:** Accidental local-state publication.

**Validation:** final PR8 secret/privacy scan and corpus contract verification.

**Phase:** PR8 verification.

---

### F20 — Package metadata is functional but minimal

**Category:** POLISH  
**Severity:** MEDIUM

**Reviewer impact:** `pyproject.toml` looks like an internal/local package rather than an intentionally presented public project.

**Evidence:** Package is `jobhunter-local`, version `0.1.0`, with description, dependencies, dev extras, scripts, pytest and Ruff configuration. It does not currently present richer project URLs/license metadata, and repository metadata has no license.

**Recommended action:** Keep distribution scope honest. Add only useful metadata after README/license decisions. Do not publish to PyPI merely to gain a badge.

**Risk if changed:** Inconsistent version/license/project-name claims.

**Validation:** editable install, entrypoints, tests, metadata consistency.

**Phase:** PR8.

---

### F21 — No intentional portfolio release exists yet

**Category:** ADD  
**Severity:** MEDIUM

**Reviewer impact:** CV link points to a moving `main` rather than a named stable portfolio checkpoint.

**Evidence:** GitHub releases currently return an empty set. Package version is `0.1.0` but there is no corresponding portfolio release surfaced.

**Recommended action:** Do not release now. After PR1–PR8, create one intentional tagged release whose README, screenshots, architecture, tests, and release notes agree.

**Risk if changed:** Freezing a release before the presentation cleanup is complete.

**Validation:** final readiness checklist + CI + current local acceptance where required.

**Phase:** PR9.

---

### F22 — Experimental Blueprint is correctly bounded internally but needs simpler public labeling

**Category:** POLISH  
**Severity:** MEDIUM

**Reviewer impact:** A reviewer can mistake implemented experimental code for a production decision layer.

**Evidence:** Governance and README repeatedly mark Blueprint v6 as experimental/deferred/non-authoritative. Browser/source support remains intentionally inspectable.

**Recommended action:** Keep the experimental implementation/history, but public surfaces should label it once, clearly, and avoid making it appear equal to accepted P1.6/Capability/Work Intelligence.

**Risk if changed:** Hiding real research work or, conversely, overclaiming it.

**Validation:** status wording matches governance.

**Phase:** PR1/PR2/PR3.

---

### F23 — Current Work Intelligence and Registry browser modules improve architecture clarity

**Category:** KEEP  
**Severity:** LOW / POSITIVE

**Reviewer impact:** Shows the web package is already evolving toward domain-specific presentation modules rather than one monolithic UI file.

**Evidence:** Dedicated web modules exist for Capability, Registry, and Work Intelligence alongside the central app/router assembly.

**Recommended action:** Preserve these boundaries and use them as evidence when deciding whether `web/app.py` should delegate additional route groups in PR5.

**Risk if changed:** Over-fragmenting routes into trivial files.

**Validation:** dependency/route map.

**Phase:** PR5 if needed.

---

### F24 — AI-assisted development should be presented through ownership and validation, not hidden or foregrounded as a gimmick

**Category:** POLISH  
**Severity:** MEDIUM

**Reviewer impact:** The repository contains extensive AI-agent governance/history. Without context, a reviewer may see generation chronology rather than engineering ownership.

**Recommended action:** Keep `AGENTS.md` and governance because they are real project controls, but stop sending first-pass readers there as the primary project introduction. In CV/interviews, explain AI assistance through requirements, architecture decisions, bounded authority, tests, semantic review, regression evidence, and human ownership.

**Risk if changed:** Misrepresenting authorship/engineering process or deleting useful governance.

**Validation:** truthful wording; no claim that all code was manually authored.

**Phase:** PR1/PR3/PR9.

---

## 4. Explicit KEEP decisions

PR0 finds **no evidence-based reason to replace** the following:

1. local-first product posture;
2. Python modular monolith;
3. SQLite as current runtime authority;
4. FastAPI + Jinja2 + small vanilla JS browser architecture;
5. shared browser/CLI application services and state;
6. immutable source evidence + semantic source-version model;
7. deterministic vs LLM authority separation;
8. semantic review as a promotion boundary;
9. explicit artifact/dependency/currentness tracking;
10. bounded Jobinja acquisition/source policy;
11. public corpus vs local SQLite separation;
12. review snapshots as selected acceptance evidence;
13. Ruff + pytest + warnings-as-errors CI;
14. explicit current/experimental distinction;
15. historical evidence/reproducibility as an engineering goal.

These are portfolio assets, not liabilities.

---

## 5. Items that require deeper dependency audit before disposition

PR0 intentionally does **not** decide to remove or move these yet:

```text
analysis_runtime_v*
analysis_service_v*
other versioned P1.6/Capability/Blueprint implementation families
historical version-specific tests
historical audit scripts
accepted/rejected semantic experiment helpers
```

Known fact: current `analysis_current.py` still imports current English v20 plus original-language v9 paths. Therefore the historical/versioned tree cannot be treated as dead code wholesale.

PR4 must produce the exact import/reference/reproducibility matrix before file movement.

---

## 6. Public-claims reconciliation matrix

| Surface | Current status | Audit result |
| --- | --- | --- |
| GitHub metadata | missing description/topics/license | incomplete |
| README product identity | broadly correct | keep core wording, restructure |
| README semantic stack | behind current main | update |
| README corpus baseline | current 353 / 43 / 20 / 5 / 5 | keep as current reference until refreshed |
| Architecture end-to-end flow | behind Registry/Work Intelligence | update |
| Product specification | strong, detailed | retain as deep product authority |
| Domain model | strong provenance/entity foundation | retain; later reconcile new current entities if needed |
| Source policy | strong and appropriate | retain |
| Reasoning policy | strong differentiator | retain as deep authority, summarize publicly |
| Review snapshots README | contains older corpus baseline | mark/reconcile current-vs-historical meaning |
| Blueprint | implemented but non-authoritative | keep clearly experimental |
| Canonical Registry | implemented/accepted P2.1 | add to current product story |
| Job Work Intelligence v2 | implemented/accepted P2.2A | add to current product story |
| P2.2B responsibility promotion | incomplete/local-blocked | do not present as implemented feature |
| personal evidence/readiness/gap intelligence | planned | do not present as implemented |
| automated applications/recruiter communication | not authorized | do not claim |

---

## 7. Fresh-clone / demo capability matrix

### A. Repository only, no installation

A reviewer can already inspect:

- README/docs;
- public corpus source and accepted artifacts;
- review snapshots;
- source/tests;
- CI history.

**Problem:** This route is not presented as a first-class demo.

### B. Python 3.12 + install, no LM Studio

Expected useful activities include deterministic tests and non-model code paths. The exact clean-fresh-clone behavior still requires local verification during PR7.

### C. Local app/runtime state, no LM Studio

Acquisition/source browsing remains designed to be useful independently of model availability, but a fresh external user does not inherit the owner's SQLite state. The README must not imply that cloning automatically reconstructs the live app from `corpus/`.

### D. LM Studio configured

Translation/analysis/reasoning workflows become available according to configured model roles and accepted contracts.

### E. Live Jobinja acquisition

Bounded approved-source discovery/fetch/sync is available under source-policy restrictions.

### Demo decision

PR6 should **not build a fake standalone demo**. The smallest credible portfolio demonstration is:

```text
committed public corpus + curated walkthrough
+ real browser screenshots
+ optional local runtime instructions
```

A corpus-import/read-only app mode should be considered only if later evidence shows it materially improves reviewer usability; it is not authorized merely for portfolio polish.

---

## 8. Ranked execution after PR0

### PR1 — immediate next bounded slice

PR1 should focus only on public landing/presentation:

1. rewrite README around the current product rather than internal chronology;
2. add current features including Work Intelligence + Canonical Registry with accurate acceptance labels;
3. add architecture-at-a-glance text/diagram source placeholder only if it can be accurate without local screenshots;
4. add concise technology and engineering-highlights sections;
5. make public-corpus inspection a first-class no-model review path;
6. simplify Quick Start into staged levels;
7. expose CI/test quality and add a validated CI badge;
8. clearly separate current / experimental / planned capabilities;
9. define final GitHub description/topics wording.

**Not PR1:** license decision, file moves, historical-code cleanup, screenshots fabricated without machine access, runtime refactors.

### PR2

Reconcile architecture and current engineering story, including Work Intelligence/Registry and current authority flow.

### PR3

Design and execute documentation information architecture with link/reference verification.

### PR4

Build exact source/test/script historical dependency matrix and choose disposition.

### PR5

Only then selectively refactor current code where evidence shows real maintainability benefit.

### PR6–PR9

Demo/screenshots → onboarding → repository/package hygiene → stable release/CV/interview package.

---

## 9. PR0 acceptance decision

PR0 passes.

Evidence gathered covers:

- public GitHub metadata;
- root repository surface;
- README;
- current governance/product/architecture/domain/source/reasoning boundaries;
- package metadata and installed entrypoints;
- CI configuration and recent successful run;
- `src/jobhunter` current/historical structure;
- web package structure and large-module candidate;
- tests historical/current mixture;
- scripts historical audit mixture;
- `docs/` density/currentness;
- public corpus;
- review snapshots;
- configuration example;
- ignored/private runtime boundaries;
- release state;
- local-model/live-acquisition onboarding boundaries.

No cleanup implementation was mixed into this audit.

## 10. Exact next action

```text
PR1 — professional GitHub landing + README redesign
→ preserve current semantics
→ no file-tree cleanup yet
→ no code refactor yet
→ no fake screenshots/demo artifacts
```

P2.2B product work remains paused at the existing local `ta9l` P1.6 acceptance gate.