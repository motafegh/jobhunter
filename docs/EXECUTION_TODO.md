# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-14  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

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
- [x] targeted `jobhunter jobs analyze <id>` command for one explicit public P1.6 job.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] `jobhunter jobs snapshot <id>` preserves effective model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**Public/accepted P1.6 remains v9/schema v4. Dense `tG9K` v9 artifact 29 remains authoritative. Active candidate is v18/schema-v5 on `agent/p16-v18-deterministic-structured-requirements`. V18 deterministic CI passes; dense live `tG9K` is the next gate.**

#### Accepted dense v9 baseline — `tG9K`

- [x] 27 requirements / 7 responsibilities retained.
- [x] deterministic coverage accounting accepted.
- [x] optionality preserved.
- [x] `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` preserved.
- [x] MATLAB/C++ remain preferred.
- [x] contextual stack remains contextual.
- [x] Master's degree and 3–6 years professional experience preserved.

#### Sparse calibration baseline — `t4jp`

- [x] v16 artifact `35`: bounded sparse mechanical + semantic PASS.
- [x] 8 requirements / 0 responsibilities / 0 role purpose.
- [x] structured required skills 3/3.
- [x] qualification items 4/4.
- [x] residual decisions 4/4.
- [x] no fabricated duty/purpose.

Earlier v9→v15 sparse failures remain preserved in dated working-memory and are not reopened unless new evidence requires it.

#### Permanent semantic boundaries inherited by v18

- [x] exact source evidence/provenance.
- [x] no unsupported/invented career claims.
- [x] required/preferred/contextual strength kept distinct.
- [x] depth kept separate from obligation and normalized concept.
- [x] structured `skills[]` cannot silently disappear.
- [x] exact qualification-list item evidence.
- [x] deterministic coarse-span decomposition bookkeeping.
- [x] complete residual sentence accounting.
- [x] qualification-vs-responsibility protection.
- [x] schedule wording cannot become capability depth.
- [x] clean reusable concepts; no punctuation debris.
- [x] ontology: skill/tool/knowledge/practice/domain/experience/education/other.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] one bounded correction; fail closed after exhaustion.

#### Dense v16 defect — source-led capacity

- [x] v16 `tG9K` failed twice at exactly 32 requirements.
- [x] education/minimum-experience oscillated across the old 32-slot boundary.
- [x] inherited 32-requirement ceiling confirmed in typed model, JSON schema, and final guard.
- [x] no product/domain rule justifies that ceiling.
- [x] isolated v17/schema-v5 removed the arbitrary requirement cap without mutating accepted v9/v4.

Detailed record:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

#### V17 correction 1 — source-led requirement capacity

- [x] `job-analysis-english-v17` / `job-analysis-v5` created.
- [x] requirements no longer capped at 32 in candidate typed/schema path.
- [x] item 33+ receives strict evidence/depth validation.
- [x] duplicate and invented-evidence guards remain effective beyond item 32.

Record:

```text
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
```

#### V17 correction 2 — aggregate dense coverage feedback

First v17 dense run:

- [!] failed before persistence.
- [x] did not hit 32; first generation had 15 requirements, retry 16.
- [!] first generation omitted minimum experience and one duty surface.
- [!] one-error-at-a-time coverage feedback caused retry to fix minimum experience, then discover education after retry exhaustion.

Correction:

- [x] requirement + responsibility coverage defects now aggregate into one retry message.
- [x] one bounded retry retained; retry count not increased.
- [x] regression test proves minimum experience + education + another missing requirement + missing responsibility can be reported together.
- [x] deterministic CI passed.

Record:

```text
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
```

#### Second v17 dense run — unnecessary model ownership exposed

- [!] no v17 artifact persisted.
- [x] generation 1 represented all seven duty surfaces.
- [x] aggregate feedback correctly reported both `field:minimum_experience` and `field:education` together.
- [x] generation 2 added both structured facts.
- [!] retry represented minimum experience as `Professional experience of three to six years` while also using `three to six years` as `depth_signal`.
- [x] strict depth-neutral concept validator correctly rejected that representation.
- [x] failure classified as unnecessary model authority over mechanically known structured facts, not as a reason to weaken validation.

#### V18 — deterministic structured-fact ownership

Candidate:

```text
English P1.6: job-analysis-english-v18
schema shape: job-analysis-v5
branch: agent/p16-v18-deterministic-structured-requirements
stacked draft PR: #6
base candidate: agent/p16-v17-source-led-capacity / PR #5
```

- [x] parseable structured `minimum_experience` is removed from model-facing evidence and deterministically materialized as:
  - `Professional experience`
  - exact years `depth_signal`
  - required / experience
  - exact structured-field evidence.
- [x] structured `education` is removed from model-facing evidence and deterministically materialized as required education with exact evidence.
- [x] unparseable minimum-experience wording stays model-owned/fail-closed; code does not guess.
- [x] structured `skills[]` remain model-visible for semantic concept-type classification.
- [x] every structured skill gets explicit non-excludable coverage so all omissions are reported together.
- [x] deterministic requirements are combined before the existing semantic/persistence/final-validation chain; no guard is bypassed.
- [x] materialization is idempotent.
- [x] regression tests cover deterministic partition, conservative fallback, structured-skill coverage, aggregate missing-skill feedback, strict final validation, and idempotence.
- [x] CI run 731 passed Ruff, full pytest, and warnings-as-errors before docs reconciliation.

Record:

```text
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
```

#### Current dense v18 live gate — `tG9K`

Run:

```bash
git fetch origin
git switch agent/p16-v18-deterministic-structured-requirements
git pull --ff-only origin agent/p16-v18-deterministic-structured-requirements
python scripts/run_p16_v18_candidate.py --job-id tG9K
```

- [~] run dense v18 locally against configured LM Studio/current database.
- [ ] confirm one v18 artifact persists.
- [ ] confirm `Master's degree` is present as required education.
- [ ] confirm `Professional experience` + exact `three to six years` depth coexist correctly.
- [ ] confirm all six structured `skills[]` surfaces are represented.
- [ ] confirm all seven dense duty surfaces are represented.
- [ ] compare dense factual coverage against accepted v9 artifact 29; no silent fact loss.
- [ ] inspect `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` depth attachment.
- [ ] verify MATLAB/C++ remain preferred.
- [ ] verify contextual stack remains contextual where source wording requires it.
- [ ] preserve provenance distinction between structured Python and prose `Python (expert)`.
- [ ] review concept-type differences only after mechanical validity.

If v18 fails, classify the new concrete failure. Do not increase retries or weaken semantic validation by default.

#### Sparse v18 non-regression — only after dense PASS

```bash
python scripts/run_p16_v18_candidate.py --job-id t4jp
```

- [ ] compare with accepted sparse v16 artifact 35.
- [ ] ensure deterministic structured ownership does not create sparse over-extraction.
- [ ] retain structured skills, qualification/residual accounting, and zero fabricated duties/purpose.

#### Current B2 decision boundary

- [x] public v9/schema v4 stays authoritative.
- [x] sparse v16 acceptance remains valid.
- [x] v17 capacity correction deterministic gate passed.
- [x] v17 aggregate feedback correction deterministic gate passed.
- [x] v18 deterministic structured ownership implementation gate passed.
- [!] v18 public promotion blocked until dense semantic PASS + sparse non-regression PASS.
- [!] Capability v7 rebuild above v18 blocked until P1.6 promotion.
- [!] heterogeneous-role progression blocked until the dense/sparse v18 decision.

### B3 — Capability Intelligence

**Accepted only for bounded `tG9K` on Capability artifact 9 tied to accepted P1.6 v9 artifact 29.**

- [x] `job-capability-intelligence-v7` / schema v4 accepted for bounded tG9K.
- [x] complete deterministic source truth.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 accepted requirements retained in source truth.
- [x] all six accepted explicit-depth facts retained.
- [x] two coherent capability profiles.

Freeze v7 unless heterogeneous evidence reveals a repeatable correctness defect. After eventual P1.6 promotion, rebuild Capability v7 against the promoted analysis artifact rather than reusing artifact 9 as though it were current-chain.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred.**

- [x] provenance/index failure class identified and mechanically fixed.
- [x] v6/12B artifact 7 passed mechanical audit and CI.
- [!] semantic review still found unsupported automated-feedback/platform/implementation assumptions.
- [x] do not create Blueprint v7, weaken validators, or resume nearby model shopping during this gate.

### B5 — CI-3 heterogeneous live review

Permanent workflow:

```text
snapshot current local state first
→ run matching mechanical audit
→ inspect source/projection/P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
```

Current targets:

- [x] sparse `t4jp` — v16 bounded acceptance.
- [x] rich AI/ML `tG9K` — accepted v9/v7 baseline retained.
- [~] dense `tG9K` v18 — live gate next.
- [ ] sparse `t4jp` v18 non-regression after dense PASS.
- [ ] Python/software role — gated on v18 decision.
- [ ] network/security role — gated on v18 decision.
- [ ] operations/platform/DevOps role — gated on v18 decision.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] record model limitations separately from deterministic defects.
- [ ] decide whether P1.6 + Capability v7 is good enough to freeze as Phase-2 input.

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
