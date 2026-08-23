# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-23
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`

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
- [x] durable English P1.6 `pending`/`accepted` review state plus explicit status/accept/reject CLI and browser actions.
- [x] pending P1.6 excluded from Capability, Market, accepted browser counts, and public corpus; rejected candidates archived locally and rebuildable.
- [x] v20 depth registry isolated from historical validator modules.
- [x] P1.6 v20 implementation/calibration stack consolidated into `main`.
- [x] Capability v9 public/current facade and promotion.
- [x] version-controlled public corpus projection `jobhunter-public-corpus-v1`.

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
- [x] operational P1.6 v20 promotion complete.

Promoted does not mean unchangeable implementation code: heterogeneous review may still expose repeatable deterministic defects. Fix those with regression tests without inventing a new public contract unless the contract itself changes materially.

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
- [x] dense artifact 11 accepted/current on P1.6 artifact 36.
- [x] sparse artifact 12 accepted/current on P1.6 artifact 37.
- [x] neutral/current `capability_service.py` promotes v9/v5.
- [x] CLI/browser/Review Snapshot follow the neutral current facade.
- [x] Blueprint v6 pinned to historical Capability v7 constants.
- [x] promotion CI and docs gates PASS.
- [x] normal Capability commands reused artifacts 11/12.
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

### B5 — Complete versioned public corpus — OPERATIONALLY CLOSED

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

Implementation/acceptance:

- [x] deterministic `src/jobhunter/public_corpus.py` exporter.
- [x] `corpus/manifest.json` whole-corpus index.
- [x] one UTF-8 job directory per known Jobinja identity.
- [x] `source.json` preserves current public parsed Persian/English vacancy fields when detail exists.
- [x] discovery-only identities use `current_detail: null`.
- [x] current English projection/P1.6/Capability stage exports.
- [x] exact artifact/dependency/model/prompt/schema identities preserved.
- [x] only semantically accepted English P1.6 and its exact Capability chain are projected.
- [x] raw model protocol, raw HTML, machine-local paths, secrets/logs/config/private state excluded.
- [x] stale downstream files removed after source changes until rebuilt.
- [x] exact DB↔corpus deterministic verification.
- [x] `jobhunter-corpus export`, `verify`, and `status` commands.
- [x] normal mutating CLI and completed browser operations refresh local corpus after durable work.
- [x] corpus failure surfaces without rolling back SQLite.
- [x] no automatic Git commit/push.
- [x] deterministic tests cover Unicode, privacy, dependencies, stale cleanup, tampering, routing, browser hook, and coverage terminology.
- [x] real DB backfill completed and current `jobhunter-corpus verify` passed for 353 known jobs.
- [x] exact publication baseline recorded:

```text
Known/discovered jobs:       353
Fetched/parsed job details:   43
Current English projections:  20
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
Per-job stage files:         383
Corpus size:                ~3.7 MiB
```

- [x] public-data safety scan clean.
- [x] accepted tG9K chain: detail 40 → translation 33 → P1.6 36 → Capability 11.
- [x] accepted t4jp chain: detail 41 → translation 34 → P1.6 37 → Capability 12.
- [x] accepted heterogeneous chains published: tmBK P1.6 39 → Capability 13; t4qV 44 → 14; tmyX 46 → 15.
- [x] full corpus committed/pushed in `15dbfa3636bbf7118de79683beec3e7ac4a6359d`.
- [x] remote manifest/job directories and accepted anchors verified.
- [x] publication CI 902 PASS.
- [x] coverage terminology hardened: known/discovered jobs distinguished from fetched/parsed details.
- [x] public-corpus operational availability CLOSED.

Permanent interpretation:

```text
353 known/discovered jobs != 353 fully fetched advertisements
```

Only jobs with a non-null current fetched/parsed detail are eligible downstream semantic-review anchors.

### B6 — Heterogeneous live review — CLOSED

Order:

- [x] Python/software role — `tmBK` accepted on P1.6 39 → Capability 13.
- [x] network/security role — `t4qV` accepted on P1.6 44 → Capability 14.
- [x] operations/platform role — `tmyX` accepted on P1.6 46 → Capability 15.
- [x] promoted P1.6 + Capability heterogeneous gate closed; proceed to remaining Phase-1 acceptance.

#### B6A — Python/software `tmBK`

Current upstream:

```text
job:                       tmBK — Python Developer
source detail:             44
English projection:        38
P1.6 contract:             job-analysis-english-v20 / job-analysis-v5
analysis model:            gemma-4-e4b-it-ud
```

Selection/source checks:

- [x] selected from fetched/parsed corpus rather than discovery-only titles.
- [x] materially different from dense industrial-ML and sparse content anchors.
- [x] source contains real backend/software skills and multiple explicit depth levels.
- [x] source contains no genuine explicit responsibility section; qualification-vs-duty restraint is therefore a key test.
- [x] separate candidate `tI1n` blocked before P1.6 because its English projection materially mistranslated source meaning.

Deterministic defects already found/fixed:

- [x] accept exact `Sufficient knowledge` as employer depth while plain `knowledge` remains non-depth.
- [x] regression test for the boundary above.
- [!] first persisted `tmBK` P1.6 artifact 38 semantically rejected: multi-signal evidence incorrectly propagated `Mastery` to `Familiarity`/`Sufficient knowledge` concepts.
- [x] v20 now preserves item-specific supplied depth rather than the first marker in the evidence block.
- [x] v20 fails closed when multi-level evidence has no item-specific depth signal.
- [x] exact tmBK-style multi-signal regression coverage added; CI 911 PASS.
- [x] `Ability to effectively use AI ...` recognized as application wording, not technical depth, when evidence contains no genuine depth marker.
- [x] fail-closed behavior retained if real depth appears in the same evidence.
- [x] regression coverage added; CI 914 PASS.
- [x] redundant coverage exclusion removed only when the same reference is positively represented.
- [x] genuine exclusions preserved.
- [x] regression coverage added; CI 916 PASS.

Artifact/current state:

- [x] rejected P1.6 artifact 38 must not feed Capability.
- [x] no Capability artifact was created from rejected artifact 38.
- [x] failed later rebuild attempt persisted no new P1.6 artifact.
- [x] accepted rebuild persisted as P1.6 artifact 39.

Exact next steps:

- [x] all tmBK depth, AI non-depth, qualification-vs-duty, structured-skill, and coverage checks passed.
- [x] P1.6 artifact 39 explicitly accepted with durable review note.
- [x] Capability artifact 13 complete source coverage/provenance and semantic review passed.
- [x] Python/software anchor closed.

#### B6B — network/security `t4qV`

- [x] selected fetched/parsed `t4qV` (detail 30, English projection 20).
- [x] source→English quality reviewed before P1.6.
- [x] artifacts 40-43 rejected with durable notes; no Capability run.
- [x] general evidence-boundary defects converted to regression tests.
- [!] artifact 43 certification ontology rejected: named credentials persisted as skills and would cross the role-level/Capability boundary.
- [x] general credential classification guidance added without vendor-specific acronyms.
- [x] P1.6 artifact 44 accepted; Capability artifact 14 passed 9/9 requirements, 10/10 duties and role-level credential separation.

#### B6C — operations/platform/DevOps

- [x] blocked `t49N` before P1.6 for a material English field-association defect.
- [x] selected/reviewed `tmyX` (detail 35, English projection 24; IT/DevOps/Server).
- [x] fixed generic-heading false splits, explicit pre-heading role-duty coverage, and non-depth `Ability to` / `Skill in` wording with regressions.
- [x] rejected/archived artifact 45 for omitted opening role actions.
- [x] P1.6 artifact 46 accepted; Capability artifact 15 passed 11/11 requirements, 5/5 duties and 6/6 depth facts.

Per-role permanent checks:

- [x] P1.6 factual coverage/provenance.
- [x] required/preferred/contextual optionality.
- [x] concept-specific explicit depth.
- [x] role-level constraints.
- [x] no fabricated responsibilities.
- [x] Capability complete requirement/responsibility coverage and provenance.
- [x] no fabricated prerequisites, ownership, lifecycle, architecture, autonomy, or mandatory strength.
- [x] deterministic defect vs acceptable model variation/local-model limitation distinguished.
- [x] repeatable deterministic defects converted into fixtures.
- [x] no contract change for harmless non-authoritative wording differences.

## C. Phase-1 closure after heterogeneous semantic acceptance

### C1 — Market truthfulness

- [x] analyzed-current sample size visible.
- [x] source/filter/contract scope recoverable.
- [x] small-sample/concentration warnings.
- [x] coverage metrics separate from semantic certification.
- [x] posting-level strength columns documented as non-exclusive.
- [x] repost/cross-post near-duplicate adjustment explicitly reported as not implemented.

### C2 — Source/lifecycle

- [x] network/429/5xx/challenge/auth failure != expired/removed.
- [x] cautious 404/410/repeated-missing lifecycle handling.
- [x] last-successful / consecutive-failure summaries accepted.

### C3 — Partial-success truthfulness

- [x] expose requested / attempted / completed / reused / skipped / failed / remaining eligible.
- [x] browser/CLI complete-workflow summaries use the same service and formatter.
- [x] earlier durable success survives later failure and still refreshes the public projection.
- [x] no-eligible-work != attempted-and-failed.
- [x] Quick Add propagates mixed detail/translation/analysis outcomes as partial success.

### C4 — P1.7 final workflow

- [x] final per-job report/provenance.
- [x] ready-job queue.
- [x] combined current-corpus report.
- [x] `jobhunter run` deterministic acceptance.
- [x] browser equivalent acceptance.
- [x] rerun/idempotency proof.
- [x] bounded live end-to-end Phase-1 acceptance.

### C5 — Phase-1 closure

- [x] acceptance summary with exact corpus/sample/contracts/bounds.
- [x] reconcile final accepted docs.
- [x] freeze accepted P1.6 + Capability starting contract for Phase 2.
- [x] keep Blueprint deferred/non-authoritative unless later evidence reopens it.

## D. Phase 2 — gated

Phase-1 closure passed on 2026-08-23. Begin only through the focused P2.1 plan:

```text
docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md
```

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

### D1 — P2.1A registry foundation — ACCEPTED

- [x] versioned typed concept/category/status contract.
- [x] SQLite concepts, aliases, and job-claim mappings.
- [x] stable-ID, normalization, collision, supersession, and provenance invariants.
- [x] explicit mapped/unmapped/rejected decisions.
- [x] current accepted P1.6 dependency boundary.
- [x] deterministic offline tests and migration proof.

### D2 — P2.1B manual CLI workflow — ACCEPTED

- [x] list/show/add/deprecate concepts.
- [x] add reviewed aliases with provenance.
- [x] list accepted-current P1.6 claims and mapping state.
- [x] record mapped/unmapped/rejected decisions with meaningful review notes.
- [x] preserve idempotency and immutable prior decisions.
- [x] complete local `ruff check .`, `pytest`, and `pytest -W error` acceptance gate passed on 2026-08-23.

### D3 — P2.1C read-only and review browser surfaces — ACCEPTED

- [x] registry overview and filters.
- [x] concept detail with aliases and source-backed job mappings.
- [x] accepted-current pending/unmapped review queue.
- [x] CSRF-protected bounded manual concept/alias/mapping decisions.
- [x] structured links for registry review navigation where useful.
- [x] CLI/browser review mutations share the same canonical-registry service contract.
- [x] registry review writes do not trigger public-corpus refresh side effects.
- [x] deterministic browser/service tests plus local `ruff check .`, `pytest`, and `pytest -W error` acceptance passed on 2026-08-23.

### D4 — P2.1D small seed and P2.1 acceptance — ACTIVE NEXT

- [ ] deliberately small cross-role seed from the five accepted chains.
- [ ] include at least one alias, one ambiguous/unmapped case, one responsibility, and one education/credential or experience signal.
- [ ] inspect every seed decision against exact accepted P1.6 evidence.
- [ ] verify rerun/idempotency and stale-dependency behavior on the accepted seed.
- [ ] decide separately whether any repository-safe registry projection is warranted after privacy/source review.
- [ ] close P2.1 only when every focused-plan acceptance criterion is satisfied.
