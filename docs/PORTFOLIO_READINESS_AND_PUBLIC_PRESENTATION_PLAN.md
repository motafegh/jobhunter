# JobHunter Portfolio Readiness and Public Presentation Plan

**Status:** ACTIVE / PR0–PR8 COMPLETE / PR9 REPOSITORY-SIDE PACKAGE COMPLETE / RELEASE + OWNER MASTERY PENDING  
**Date:** 2026-09-04  
**Scope:** Make the public JobHunter repository professional, understandable, demonstrable, maintainable and credible as a CV/portfolio project without weakening or rewriting accepted product semantics.  
**Product-development boundary:** P2.2B-B1 remains locally blocked on `ta9l` English projection/P1.6 acceptance. Portfolio work does not authorize product-semantic changes, registry promotion or P2.2C.

---

## 0. Progress ledger

| Phase | State | Primary evidence |
| --- | --- | --- |
| PR0 — full portfolio-readiness audit | COMPLETE | `PORTFOLIO_READINESS_AUDIT_2026-09-02.md` |
| PR1 — README / public landing story | COMPLETE | root `README.md` |
| PR2 — architecture / engineering story | COMPLETE | `ARCHITECTURE.md` |
| PR3 — documentation information architecture | COMPLETE | `docs/README.md` + PR3 closure |
| PR4 — historical/versioned source disposition | COMPLETE | `CURRENT_RUNTIME_AND_VERSIONED_CODE.md` + PR4 closure |
| PR5 — current-code structure/readability | COMPLETE | bounded shared-web refactor + PR5 closure |
| PR6 — reproducible demo/public corpus | REPOSITORY-SIDE COMPLETE | `demo/README.md`; real screenshots still local-only pending |
| PR7 — installation/developer onboarding | COMPLETE | `DEVELOPMENT_AND_LOCAL_SETUP.md` + CI onboarding smoke |
| PR8 — repository/package/security hygiene | REPOSITORY-SIDE COMPLETE | `SECURITY.md`, package/config/CI cleanup + PR8 closure |
| PR9-A — final repository/public consistency audit | COMPLETE | `working-memory/2026-09-04_PR9_FINAL_PORTFOLIO_AUDIT_AND_RELEASE_READINESS.md` |
| PR9-B — owner/external release blockers | PENDING | license + GitHub metadata + real screenshots |
| PR9-C — intentional portfolio tag/release | PENDING | candidate `v0.1.0`; no tag/release yet |
| PR9-D — CV/interview package | COMPLETE | `PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md` |
| PR9-E — owner mastery | PREPARED / NOT VERIFIED | mastery route in PR9 package |

Correct current portfolio state:

> **The repository-side portfolio work is complete enough for release preparation, but PR9 is not globally closed until the intentional release state and owner mastery are actually completed.**

---

## 1. Objective

A recruiter, hiring manager, senior engineer, technical interviewer or developer should be able to understand:

1. the problem JobHunter solves;
2. what exists today versus experimental/historical/future work;
3. the architecture and major tradeoffs;
4. source truth, deterministic logic, model reasoning and review/promotion boundaries;
5. provenance, persistence, privacy and failure semantics;
6. how to inspect real output without private SQLite state or LM Studio;
7. how to install/test/run the project safely;
8. why historical/versioned implementation remains present;
9. what the owner actually learned/owns in an AI-assisted development process.

Target: **professional technical credibility**, not artificial complexity or portfolio decoration.

---

## 2. Reviewer paths

### Recruiter — 30–90 seconds

```text
README
→ product/value proposition
→ architecture at a glance
→ stack/current maturity
→ real public corpus/demo
```

### Hiring manager — 3–5 minutes

```text
README
→ current workflow/limits
→ deterministic vs model/review split
→ persistence/provenance
→ demo + tests/CI
```

### Senior engineer / interviewer — 10–30 minutes

```text
README
→ docs/README.md
→ PRODUCT_SPECIFICATION.md
→ ARCHITECTURE.md
→ CURRENT_RUNTIME_AND_VERSIONED_CODE.md
→ selected source/tests
→ deeper decisions/experiments only when useful
```

### Developer clone

```text
clone
→ Python 3.12 venv
→ pip install -e ".[dev]"
→ jobhunter init --path config/local.toml
→ pip check / entrypoint smoke
→ Ruff / pytest / pytest -W error
→ optional browser
→ optional LM Studio
→ optional bounded Jobinja acquisition
```

The committed public corpus/demo remains inspectable without Jobinja, LM Studio or maintainer SQLite state.

---

## 3. Permanent rules

1. Do not redesign architecture merely for CV appearance.
2. Do not introduce microservices, Kubernetes, React, vector databases, queues, cloud infrastructure or other fashionable technology solely for signaling.
3. Do not rewrite Git history to hide engineering evolution.
4. Do not delete historical/versioned source until runtime, compatibility, reproducibility and regression roles are proved unnecessary.
5. Do not change accepted semantic behavior as a presentation/refactor side effect.
6. Do not reopen accepted P1.6, Capability v9, P2.1 or P2.2A for harmless wording differences.
7. Do not publish private/local state.
8. Keep public documentation layered; deep engineering history may remain available without dominating entry paths.
9. Do not add ceremonial community/tooling files without demonstrated value.
10. Do not misrepresent AI-assisted development. Ownership is demonstrated through problem framing, architecture, constraints, evidence boundaries, review, validation, tradeoffs and understanding.
11. Keep implemented/current, experimental, historical, deferred and planned claims distinct.
12. Preserve one source of truth per concern.
13. Do not fabricate screenshots or machine-local acceptance.
14. Legal/owner choices such as license grants must be explicit.
15. Do not tag/release merely to satisfy a checklist when required release-state facts are unresolved.

---

# Part I — Completed portfolio engineering work

## 4. PR0–PR2 — audit, public story and architecture — COMPLETE

The PR0 audit established that JobHunter already had sufficient engineering substance for a strong portfolio project. The main weakness was public presentation/information architecture rather than lack of technical depth.

PR1 redesigned the README around product identity, current capabilities, architecture, public evidence, setup, stack, maturity and limitations.

PR2 reconciled `ARCHITECTURE.md` with the current local-first modular monolith, P1.6 fan-out, Capability v9, Work Intelligence v2, Canonical Registry, Market/report, public projections, browser/CLI and failure/security boundaries.

## 5. PR3–PR5 — information architecture and maintainability — COMPLETE

PR3 added `docs/README.md` as the professional documentation map and explicitly separated current authority/supporting docs from active plans, history, experiments, proposals and working memory without mass-moving heavily referenced files.

PR4 proved that older-looking semantic modules/tests/scripts are not uniformly dead. `CURRENT_RUNTIME_AND_VERSIONED_CODE.md` records current routing, transitive compatibility and historical/reproducibility roles; no mass deletion was authorized.

PR5 performed only a bounded measured refactor: shared web CSRF/template/redirect/operation primitives were centralized while the current modular-monolith/service boundaries were preserved.

## 6. PR6–PR7 — demonstrability and onboarding — REPOSITORY-SIDE COMPLETE

`demo/README.md` uses real committed evidence:

- `t4qV` — rich responsibility-heavy accepted chain;
- `tmBK` — sparse qualification-heavy accepted chain with intentionally empty responsibilities.

No fake demo app/data/screenshots were created.

`DEVELOPMENT_AND_LOCAL_SETUP.md` plus CI now validate the practical developer path and keep repository review, deterministic baseline, optional LM Studio and optional Jobinja acquisition separate.

Remaining PR6 local item:

```text
2–4 real browser screenshots from actual runtime
```

## 7. PR8 — repository/package/security hygiene — REPOSITORY-SIDE COMPLETE

Completed:

- package metadata/project URLs;
- explicit dev-dependency rationale;
- `python -m pip check` CI gate;
- config/example/local-state separation;
- meaningful `SECURITY.md`;
- targeted tracked-tree private/secret audit;
- minimal CI permissions;
- no unnecessary bots/templates/task-runner/container ceremony.

`httpx2` remains a justified dev/test dependency because the current Starlette TestClient path was empirically shown to require/prefer it for a clean strict-warning run.

Still owner/external:

- license decision;
- GitHub description/topics;
- optional homepage only if a meaningful external destination exists.

---

# Part II — PR9 final portfolio/release state

## 8. PR9-A — final integrated consistency audit — COMPLETE

Evidence record:

`working-memory/2026-09-04_PR9_FINAL_PORTFOLIO_AUDIT_AND_RELEASE_READINESS.md`

Verified:

- README/docs/architecture/package story is materially consistent;
- public corpus baseline/demo paths are consistent;
- current-vs-historical boundaries remain explicit;
- latest checked main CI was green;
- no tag/release currently exists;
- package version `0.1.0` naturally maps to candidate tag `v0.1.0`;
- no public claim inflation was identified in the primary reviewer path;
- private/runtime publication boundaries remain explicit.

Residual older status wording inside some large 2026-08-23 master documents is recorded as bounded documentation-consolidation debt rather than being rewritten opportunistically during PR9. Current operational status is explicit in the current governance/rolling-state surfaces.

## 9. PR9-B — owner/external release blockers — PENDING

### License

No license is currently present/detected. The owner must explicitly choose whether/how third-party reuse is granted.

### GitHub metadata

Current GitHub settings remain:

```text
description: null
topics: []
homepage: null
license: null
```

Recommended description/topics are prepared in `PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md`.

### Browser screenshots

Real screenshots remain machine-local. They must be captured from the real application and privacy-reviewed; generated/mock screenshots may not substitute.

## 10. PR9-C — intentional portfolio release — PENDING

Candidate release:

```text
package: 0.1.0
Git tag:  v0.1.0
maturity: alpha portfolio release
```

There are currently no Git tags/releases.

Release notes are prepared in `PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md`.

Do not create the tag/release until PR9-B actions are resolved and final CI is reconfirmed.

## 11. PR9-D — CV/interview package — COMPLETE

`PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md` contains:

- default and short CV entries;
- 30-second recruiter summary;
- 2–3 minute hiring-manager explanation;
- 10–15 minute technical architecture walkthrough;
- likely technical interview questions/answers;
- transparent AI-assistance ownership wording;
- exact candidate release notes and metadata recommendations.

## 12. PR9-E — owner mastery — PREPARED / NOT VERIFIED

The owner does not need to rewrite the codebase from memory.

Before using a technical claim in interviews, the owner should be able to:

```text
explain what the subsystem does
→ why it exists
→ trace the main input/output flow
→ identify authority/provenance boundaries
→ explain important failures/uncertainty
→ explain the design tradeoff
→ locate the relevant source/tests/docs for deeper detail
```

The exact must-explain/source-trace list is in the PR9 package.

PR9-E remains open until an interactive mastery pass verifies that understanding.

---

## 13. Portfolio acceptance state

### Public understanding

- [ ] GitHub description/topics applied — external settings action.
- [x] README leads with product/value rather than chronology.
- [ ] real browser screenshots present — local-runtime action.
- [x] current/experimental/future distinctions are explicit.
- [x] stack and engineering differentiators are visible without hype.

### Architecture/code

- [x] architecture matches current implementation.
- [x] authority/data-flow diagram exists.
- [x] modular-monolith/SQLite/local-first choices are explainable.
- [x] current runtime/versioned-code roles are documented.
- [x] major responsibility boundaries are defensible/test-backed.

### Documentation/demo/onboarding

- [x] external reviewer documentation path is concise.
- [x] deep history does not dominate normal navigation.
- [x] committed public corpus is inspectable without LM Studio/live acquisition.
- [x] real corpus-backed demo exists.
- [x] fresh-clone install/entrypoint/test path is CI-backed.

### Quality/hygiene

- [x] CI visible and green at latest checked baseline.
- [x] dependency/entrypoint/lint/test/warning gates are documented.
- [x] package metadata is portfolio-ready for current alpha state.
- [x] license state is truthfully explicit as undecided/no grant selected.
- [x] targeted privacy/secret audit and security boundary are documented.

### Release/CV readiness

- [x] final integrated PR9 repository audit recorded.
- [ ] intentional `v0.1.0` tag/release exists.
- [x] CV project description prepared.
- [x] recruiter/hiring-manager/technical explanations prepared.
- [ ] owner mastery pass verified.

---

## 14. Exact remaining sequence

```text
owner license-policy decision
→ GitHub description/topics update
→ machine-local real screenshots + privacy review
→ README/demo screenshot integration
→ final current-count/version check
→ final CI green
→ tag v0.1.0
→ GitHub release with prepared notes
→ verify tagged public surfaces
→ interactive owner mastery review
→ PR9 CLOSED
```

The owner mastery review can begin before machine-local access returns.

P2.2B product work remains separately paused at the existing `ta9l` P1.6 gate and must not be advanced through portfolio/release work.
