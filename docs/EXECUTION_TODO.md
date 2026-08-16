# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-16  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

Repository workflow rule:

```text
All current and next JobHunter implementation work proceeds directly on main.
Do not create a new working branch unless the user explicitly changes this rule.
```

Status vocabulary:

```text
[ ] not started
[~] in progress / implemented but acceptance incomplete
[x] completed/accepted for the stated bounded scope
[!] rejected / blocking defect for the stated candidate
[-] deliberately deferred
```

## A. Accepted foundation

- [x] Jobinja acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2`.
- [x] `english-projection-v2` / `lm-studio-translation-v2`.
- [x] local browser + CLI shared services.
- [x] independent analysis/capability/blueprint model roles.
- [x] Review Snapshot v1 and current-chain routing.
- [x] deterministic CI gate: Ruff + full pytest + warnings-as-errors.
- [x] targeted `jobhunter jobs analyze <id>` command.
- [x] P1.6 v20 implementation/calibration stack consolidated into `main`.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing — COMPLETE

- [x] current-chain snapshot routing preserves model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.
- [x] public Review Snapshot distinguishes English v20/v5 from original v9/v4.
- [x] Review Snapshot selects Capability v9/v5 artifacts 11/12 as current on P1.6 artifacts 36/37.
- [x] `blueprint_current=False` for both accepted anchors after Capability promotion.

### B2 — P1.6 factual extraction — PROMOTED / CLOSED

Public-current contracts:

```text
English:  job-analysis-english-v20 / job-analysis-v5
Original: job-analysis-original-v9 / job-analysis-v4
```

- [x] dense `tG9K` artifact 36: 33 requirements / 8 responsibilities / 0 role purpose.
- [x] dense mechanical audit PASS.
- [x] dense semantic review PASS WITH ACCEPTABLE DIFFERENCE.
- [x] sparse `t4jp` artifact 37: 8 requirements / 0 responsibilities / 0 role purpose.
- [x] sparse mechanical audit PASS.
- [x] sparse semantic non-regression PASS.
- [x] exact source evidence/provenance and complete source accounting.
- [x] required/preferred/contextual strength distinct from depth.
- [x] structured skills cannot silently disappear.
- [x] qualification-vs-duty protection.
- [x] schedule wording cannot become capability depth.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] public English routing aligned across CLI, batch, browser, Market, Review Snapshot and Capability dependency selection.
- [x] public original-language path remains v9/v4.
- [x] normal `jobhunter jobs analyze tG9K` reuses artifact 36.
- [x] normal `jobhunter jobs analyze t4jp` reuses artifact 37.
- [x] normal Review Snapshot selects artifacts 36/37 with matching projection dependencies.
- [x] operational P1.6 v20 promotion complete.

### B3 — Capability Intelligence v9 — PROMOTED / CLOSED

Current public contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Historical evidence:

- [x] Capability v7 artifact 9 preserved as historical evidence tied to old P1.6 artifact 29.
- [!] v7 promoted-chain dense rebuild rejected: source-link/index loss then stable one-profile collapse.
- [x] do not reopen the v7 one-shot architecture.
- [x] Capability v8 staging mechanically proved 31/31 dense requirement coverage and 8/8 responsibilities.
- [!] v8 semantic candidate rejected for depth/ownership/lifecycle and optionality inflation.
- [x] historical v7/v8 modules/artifacts remain preserved.

Accepted v9 policy:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

- [x] complete capability-relevant requirement coverage.
- [x] complete responsibility coverage.
- [x] valid owned indices and grounded evidence.
- [x] dense anti-collapse protection.
- [x] role-level education/duration-only experience separation.
- [x] deterministic source requirement strength/depth/work.
- [x] preferred/contextual-only facts cannot independently justify inferred prerequisites.
- [x] unsupported ownership/lifecycle/autonomy/architecture analytical claims are blocked/filtered.
- [x] zero optional model enrichment is valid.
- [x] redundant model `source_explicit` echoes are filtered; deterministic reconciliation remains authority.
- [x] incomplete authoritative source truth cannot persist.

Dense v9 acceptance:

- [x] artifact 11 depends on P1.6 artifact 36.
- [x] 31/31 capability requirements linked.
- [x] 8/8 responsibilities linked.
- [x] capability explicit depth 5/5; all explicit depth 6/6.
- [x] role-level indices `[31, 32]` separate.
- [x] semantic review PASS.

Sparse v9 acceptance:

- [x] artifact 12 depends on P1.6 artifact 37.
- [x] 8/8 requirements linked; 0/0 responsibilities; 0/0 explicit depth.
- [x] no fabricated role purpose, role-level constraints, duties, prerequisites, or depth.
- [x] semantic disposition PASS WITH ACCEPTABLE DIFFERENCES.

Promotion/operation:

- [x] neutral/current `capability_service.py` promotes v9/v5.
- [x] CLI/browser/Review Snapshot follow the neutral current facade.
- [x] Blueprint v6 pinned to historical Capability v7 constants.
- [x] CI 874 promotion code gate PASS.
- [x] governing docs reconciliation PASS.
- [x] normal Capability commands reused artifacts 11/12.
- [x] no new Capability generation occurred for accepted dependencies.
- [x] snapshots marked artifacts 11/12 current on analyses 36/37.
- [x] both snapshots report `blueprint_current=False`.
- [x] Capability v9 public promotion operationally CLOSED.

Do not reopen Capability v9 calibration for harmless non-authoritative wording variation.

### B4 — Role Capability Blueprint experiment — DEFERRED

- [x] historical v6/12B artifact 7 remains experimental evidence.
- [!] semantic review found unsupported assumptions.
- [x] Blueprint v6 remains pinned to historical v7.
- [x] post-promotion snapshots confirm Blueprint is not current on accepted v9 chains.
- [-] do not resume Blueprint tuning during current Phase-1 gates.

### B5 — Complete versioned public corpus — IMPLEMENTED / OPERATIONAL BACKFILL ACTIVE

Contract:

```text
jobhunter-public-corpus-v1
```

Architecture:

```text
local SQLite                 runtime/history authority
corpus/                      complete current public Git projection
review-snapshots/            curated semantic-review evidence
```

Implementation:

- [x] deterministic `src/jobhunter/public_corpus.py` exporter.
- [x] `corpus/manifest.json` whole-corpus index.
- [x] one UTF-8 job directory per Jobinja identity.
- [x] `source.json` preserves current public parsed Persian/English vacancy fields.
- [x] current `english-projection.json` export.
- [x] current `p16-english.json` and `p16-original.json` exports.
- [x] current public `capability.json` export.
- [x] artifact/dependency/model/prompt/schema identities preserved.
- [x] raw model request/response protocol excluded.
- [x] raw HTML/local evidence paths/secrets/logs/config/private state excluded.
- [x] stale downstream files removed after a source-version change until rebuilt.
- [x] stale job directories prunable on full export.
- [x] exact DB↔corpus deterministic verification.
- [x] `jobhunter-corpus export` command.
- [x] `jobhunter-corpus verify` command.
- [x] `jobhunter-corpus status` command.
- [x] normal mutating CLI commands refresh corpus after durable local work.
- [x] browser background operations refresh corpus through shared post-success hook.
- [x] corpus failure surfaces without rolling back SQLite.
- [x] no automatic Git commit/push.
- [x] regression coverage for UTF-8, privacy exclusions, dependencies, stale cleanup, tampering, CLI routing, and browser hook.
- [x] CI 893 Ruff PASS.
- [x] CI 893 full pytest PASS.
- [x] CI 893 warnings-as-errors PASS.

Operational backfill/publish:

- [ ] pull latest `main` locally.
- [ ] reinstall editable package once so new `jobhunter` wrapper and `jobhunter-corpus` entrypoint are registered.
- [ ] `jobhunter-corpus export` against real `data/jobhunter.sqlite3`.
- [ ] `jobhunter-corpus verify` PASS.
- [ ] inspect `jobhunter-corpus status` counts.
- [ ] inspect `git diff -- corpus/` for expected public-only data.
- [ ] commit/push full current corpus.
- [ ] remotely verify `corpus/manifest.json` and job directories from GitHub.
- [ ] only then mark public-corpus operational availability CLOSED.

Exact local commands:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python -m pip install -e '.[dev]'

jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status

git status --short
git diff -- corpus/
```

If correct:

```bash
git add corpus/
git commit -m "data: publish JobHunter public corpus"
git push origin main
```

Record:

```text
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
corpus/README.md
```

### B6 — Heterogeneous live review — NEXT AFTER PUBLIC-CORPUS PUBLISH PROOF

Use the complete remote corpus to choose materially different current jobs:

- [ ] Python/software role.
- [ ] network/security role.
- [ ] operations/platform/DevOps role.
- [ ] for each role, verify current P1.6 dependency/source truth first.
- [ ] verify Capability complete source coverage/provenance.
- [ ] review required/preferred/contextual optionality and explicit depth calibration.
- [ ] verify no fabricated responsibilities, role constraints, prerequisites, ownership, lifecycle, architecture, or autonomy.
- [ ] distinguish deterministic defects from acceptable model variation/local-model limitations.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] avoid contract changes for harmless non-authoritative wording differences.
- [ ] decide whether promoted P1.6 + Capability are stable enough to freeze as Phase-2 input.

## C. Phase-1 closure after heterogeneous semantic acceptance

### C1 — Market truthfulness

- [ ] analyzed-current sample size visible.
- [ ] source/filter/contract scope recoverable.
- [ ] small-sample/concentration warnings.
- [ ] coverage metrics separate from semantic certification.

### C2 — Source/lifecycle

- [ ] network/429/5xx/challenge/auth failure != expired/removed.
- [ ] cautious 404/410/repeated-missing lifecycle handling.
- [ ] last-successful / consecutive-failure summaries accepted.

### C3 — Partial-success truthfulness

- [ ] expose requested / attempted / completed / reused / skipped / failed / remaining eligible.
- [ ] browser/CLI summaries agree.
- [ ] earlier durable success survives later failure.
- [ ] no-eligible-work != attempted-and-failed.

### C4 — P1.7 final workflow

- [ ] final per-job report/provenance.
- [ ] ready-job queue.
- [ ] combined current-corpus report.
- [ ] `jobhunter run` deterministic acceptance.
- [ ] browser equivalent acceptance.
- [ ] rerun/idempotency proof.
- [ ] bounded live end-to-end Phase-1 acceptance.

### C5 — Phase-1 closure

- [ ] acceptance summary with exact corpus/sample/contracts/bounds.
- [ ] reconcile final accepted docs.
- [ ] freeze accepted P1.6 + Capability starting contract for Phase 2.
- [ ] keep Blueprint deferred/non-authoritative unless later evidence reopens it.

## D. Phase 2 — gated

Do not begin until Phase-1 closure.

```text
canonical concept registry
→ reviewed aliases/mappings
→ responsibilities/deliverables
→ corpus-scale capability requirement profiles
→ role archetypes
→ Market v2
→ later personal evidence/gap intelligence
```

Still deferred: automatic taxonomy growth, corpus-wide Blueprint generation, personal readiness scoring, learning-plan generation, application ranking, autonomous applications, vector/RAG infrastructure, generic plugin framework, and multi-model voting.
