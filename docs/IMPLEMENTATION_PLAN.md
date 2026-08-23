# JobHunter Master Implementation Plan

**Status:** Controlling product-level implementation plan  
**Date:** 2026-08-23

## 1. Purpose and authority

This document defines JobHunter's exact product-level delivery order and acceptance gates.

It is subordinate to the product/domain/source/architecture constraints and strategic roadmap, and it controls phase-specific plans and the working checklist.

```text
PRODUCT_SPECIFICATION.md
DOMAIN_AND_ANALYSIS_MODEL.md
SOURCE_POLICY.md
ARCHITECTURE.md
        ↓
ROADMAP.md
strategic sequencing
        ↓
IMPLEMENTATION_PLAN.md
this file: controlling delivery order / gates
        ↓
PHASE_1_JOBINJA_AUTOMATION_PLAN.md
focused active plans
        ↓
EXECUTION_TODO.md
        ↓
implementation / tests / live acceptance
```

If a subordinate plan becomes stale, reconcile it. Do not silently bypass this plan.

---

## 2. Delivery rules

- Build operable vertical slices rather than disconnected framework work.
- Keep acquisition useful when LM Studio is unavailable.
- Preserve source evidence before parsing/translation/analysis.
- Keep source, English projection, factual extraction, reasoning, aggregation, and user state separate.
- Retry only explicitly retryable failure classes.
- Never equate provider/source failure with valid empty results.
- Never turn transient network/5xx/rate-limit/challenge/auth failures into destructive lifecycle conclusions.
- Require deterministic tests before live acceptance.
- Require reviewed live examples before trusting model-derived layers at scale.
- Use representative samples rather than only convenient examples.
- Keep browser and CLI on the same services/data.
- Preserve historical artifacts when contracts change.
- Keep deterministic bookkeeping/calculation deterministic.
- Prefer unknown/review states over fake precision.
- Important real incidents become regression fixtures where possible.
- Do not build future infrastructure before demonstrated need.
- Do not infer personal capability/readiness before reviewed personal evidence exists.
- Do not keep shrinking or prompt-patching a model-derived layer indefinitely when repeated bounded evidence shows it is not reliable enough for the current phase; preserve the evidence, defer the layer, and continue with accepted upstream contracts.
- Once a public semantic layer has passed bounded acceptance and promotion, reopen it only for a repeatable material correctness/provenance/contract defect or a changed accepted dependency, not cosmetic model wording variation.

---

## 3. Product stages

| Stage | Outcome | Status |
|---|---|---|
| M0 | Local Python/SQLite/LM Studio foundation | Accepted |
| Phase 1 | Trustworthy Jobinja source→English→factual-analysis→first-Market workflow | Active |
| Phase 2 | Canonical market intelligence and corpus-scale capability requirement profiles | Gated/planned |
| Phase 3 | Reviewed personal evidence and gap intelligence | Planned |
| Phase 4 | Explainable decisions/action/application readiness | Planned |
| Phase 5 | Sustained operation, trends, recovery, quality | Planned |

A bounded per-job semantic slice was intentionally implemented before Phase-1 closure to prove safe authority boundaries above P1.6. Its current dispositions are:

- English P1.6 v20/v5: promoted/current and bounded-accepted on opposite-end dense/sparse anchors;
- Capability Intelligence v9/v5: promoted/current and operationally closed on the same accepted anchors;
- Role Capability Blueprint v6/v5: implemented but Phase-1 deferred/non-authoritative after repeated semantic-boundary failures;
- heterogeneous role-family validation: closed across Python/software, network/security, and operations/platform anchors.

This does **not** authorize Phase-2 corpus-wide generation, taxonomy growth, Market-v2 aggregation, personal scoring, or authoritative Blueprint use.

---

## 4. Current accepted/strong foundation

Current strong foundations include:

- local Python modular monolith;
- SQLite structured runtime/history authority + immutable raw evidence;
- browser + CLI shared services/state;
- bounded repeat-safe bilingual Jobinja discovery;
- stable logical job identity and discovery provenance;
- deterministic `jobinja-detail-v2` parsing;
- semantic source versions separate from source checks;
- classified source outcomes and cautious lifecycle logic;
- user triage separate from source truth;
- hardened `english-projection-v2` architecture using `lm-studio-translation-v2`;
- local LM Studio structured inference boundary;
- promoted P1.6 v20/v5 factual extraction infrastructure;
- promoted Capability Intelligence v9/v5 with deterministic source truth and bounded model reasoning;
- deferred/non-authoritative Blueprint v6/v5 experimental evidence;
- first Market aggregation over accepted/current English P1.6;
- independent analysis/capability/blueprint model roles;
- Review Snapshot v1 current-chain export;
- deterministic repository-safe public corpus `jobhunter-public-corpus-v1`;
- real public-corpus backfill/publish/remote verification;
- deterministic CI gate: Ruff + full pytest + warnings-as-errors.

Historical translation-v1, P1.6 contracts, Capability v7/v8, and Blueprint experiment artifacts remain preserved for reproducibility but are not current public contracts.

Phase 1 closed on 2026-08-23 after all acceptance gates below passed. Historical artifacts remain reproducible but non-current.

---

## 5. Current contract identities

Accepted/current Phase-1 contracts:

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6 prompt/runtime:  job-analysis-english-v20
English P1.6 schema:          job-analysis-v5
Original P1.6 prompt/runtime: job-analysis-original-v9
Original P1.6 schema:         job-analysis-v4

Capability prompt/runtime:    job-capability-intelligence-v9
Capability schema:            job-capability-intelligence-v5

Review Snapshot:              job-review-snapshot-v1
Public Corpus:                jobhunter-public-corpus-v1
```

Experimental/non-authoritative Blueprint contract:

```text
Blueprint prompt/runtime:     role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
```

Blueprint remains pinned to historical Capability v7 dependency semantics and is not current on accepted Capability v9 chains.

Accepted/current opposite-end anchors:

```text
tG9K: P1.6 artifact 36 → Capability artifact 11
t4jp: P1.6 artifact 37 → Capability artifact 12
```

Historical prompt/runtime identities remain historical and must not be reused for material redesigns.

---

# Part I — Finish Phase 1

## 6. Gate P1-A — Semantic-quality acceptance (active now)

Detailed plan:

```text
docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
```

Operational checklist:

```text
docs/EXECUTION_TODO.md
```

### P1-A0 — Review Snapshot correctness — accepted

Accepted behavior:

- integrated `jobhunter jobs snapshot` preserves effective model/dependency identities;
- deterministic routing tests cover analysis/capability/blueprint roles;
- dependency-current status is represented explicitly;
- current-chain status is not treated as semantic acceptance;
- accepted dense/sparse anchors resolve Capability artifacts 11/12 against P1.6 artifacts 36/37;
- Blueprint remains non-current on those accepted v9 chains.

### P1-A1 — P1.6 factual coverage / optionality / depth — promoted / closed

P1.6 is the strict factual substrate.

Accepted public contract:

```text
English:  job-analysis-english-v20 / job-analysis-v5
Original: job-analysis-original-v9 / job-analysis-v4
```

Bounded acceptance anchors:

```text
tG9K — dense
P1.6 artifact 36
33 requirements
8 responsibilities
0 role purpose
semantic disposition: PASS WITH ACCEPTABLE DIFFERENCE

t4jp — sparse
P1.6 artifact 37
8 requirements
0 responsibilities
0 role purpose
semantic disposition: PASS
```

Permanent P1.6 invariants include:

- responsibilities are not confused with candidate qualifications;
- meaningful explicit requirements on dense postings are not silently omitted;
- sparse postings remain restrained;
- evidence/provenance is exact and source-grounded;
- employer optionality is preserved;
- obligation strength remains separate from technical depth;
- one depth adjective cannot spread to neighboring concepts;
- structured skills cannot silently disappear;
- structured experience/education constraints are retained;
- unsupported facts remain omitted/rejected;
- deterministic coverage/reconciliation may correct bookkeeping, but must not invent source semantics.

The public contract remains promoted while heterogeneous validation probes for repeatable material defects. A defect found during heterogeneous review is fixed in the current v20 implementation with regression coverage; this does not automatically imply a new public prompt/schema version when the public semantic contract itself is unchanged.

### P1-A2 — Capability Intelligence v9 — promoted / operationally closed

Accepted public contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Accepted dense anchor (`tG9K`, artifact 11 on P1.6 36):

- 31/31 capability-relevant requirements linked;
- 8/8 responsibilities linked;
- 5/5 capability-explicit depth represented;
- 6/6 all explicit depth represented;
- role-level indices `[31, 32]` retained separately;
- semantic disposition accepted/current.

Accepted sparse anchor (`t4jp`, artifact 12 on P1.6 37):

- 8/8 capability-relevant requirements linked;
- 0/0 responsibilities;
- no fabricated explicit depth;
- role-level indices empty;
- semantic disposition accepted with acceptable differences/current.

Historical v7 remains reproducible but its promoted-chain rebuild was rejected. Historical v8 staging proved better coverage mechanics but was semantically rejected for depth/ownership/lifecycle/optionality inflation. Do not reopen either architecture as the current public path.

Capability v9 remains promoted while heterogeneous role-family review checks that the same source-truth and reasoning boundaries hold outside the original two anchors.

### P1-A3 — Role Capability Blueprint — experiment concluded / Phase-1 deferred

Blueprint must not be accepted merely because provenance or JSON validation succeeds.

The bounded v3→v6/model experiment demonstrated that deterministic provenance can be made safe, but the remaining professional interpretation still introduced unsupported assumptions beyond vacancy authority.

Therefore:

- Blueprint is **not accepted as a Phase-1 decision layer**;
- its implementation and historical artifacts remain inspectable experimental evidence;
- no Blueprint v7, nearby model shopping, validator weakening, or vacancy-specific prompt patching is authorized during Phase 1;
- Blueprint does not feed Market, personal readiness, recommendations, or other authoritative Phase-1 outputs;
- Blueprint v6 remains pinned to historical Capability v7 dependency semantics;
- it may be revisited only after a materially different grounding approach or demonstrated product-value gap changes the problem.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

### P1-A4 — Public corpus — operationally closed

Runtime/history authority remains local SQLite. The repository-safe current public projection is:

```text
jobhunter-public-corpus-v1
```

Accepted publication baseline:

```text
Known/discovered jobs:       353
Fetched/parsed job details:   43
Current English projections:  20
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

Important interpretation:

```text
353 known/discovered jobs != 353 complete advertisements
```

The corpus was backfilled from the real local DB, verified, safety-scanned, intentionally committed/pushed, remotely inspected, and its coverage terminology was hardened to distinguish known/discovered jobs from fetched/parsed details. The public corpus is now available for remote heterogeneous anchor selection and later public-data analysis.

Git publication remains intentional; runtime correctness never depends on GitHub/network availability.

### P1-A5 — Representative heterogeneous semantic review — closed

Use materially different fetched/parsed jobs:

```text
accepted baselines:
t4jp  sparse/ambiguous
tG9K  rich AI/ML industrial

accepted families:
1. Python/software — tmBK P1.6 39 → Capability 13
2. network/security — t4qV P1.6 44 → Capability 14
3. operations/platform — tmyX P1.6 46 → Capability 15
```

The first Python/software anchor is:

```text
tmBK — Python Developer
source detail version:       44
English projection artifact: 38
P1.6 public contract:        v20/v5
```

`tmBK` has already exposed several repeatable deterministic P1.6 edge cases:

1. `Sufficient knowledge` was initially missing from accepted explicit employer depth vocabulary while plain `knowledge` correctly remains non-depth.
2. A multi-level evidence segment (`Mastery`, `Familiarity`, `Sufficient knowledge`) was incorrectly canonicalized to the first marker; v20 now preserves the item-specific supplied source depth and fails closed if multi-level evidence lacks item-specific depth.
3. `Ability to effectively use AI ...` was model-supplied as depth even though it expresses application/manner rather than proficiency; v20 now clears that exact non-depth signal only when the evidence contains no real depth marker.
4. The model could positively extract a coverage reference while also redundantly excluding the same reference; v20 now removes only that contradictory redundant exclusion.

The first persisted `tmBK` P1.6 artifact 38 is **semantically rejected** and must not feed Capability. It was not published as an accepted corpus artifact and no Capability downstream was created.

Acceptance is now an enforced state transition: fresh English v20 artifacts persist as `pending`; explicit review acceptance records time/note; rejection archives the complete local artifact and releases the current contract identity for rebuild. Capability, Market, browser accepted counts, and public-corpus export select accepted artifacts only. V20-specific depth phrases are held in a copied registry so current imports cannot alter historical validator behavior.

Current live result:

```text
tmBK P1.6 artifact 39 accepted → Capability 13 accepted → Python/software closed
→ t4qV artifacts 40-43 rejected; general defects fixed
→ P1.6 44 accepted → Capability 14 accepted → network/security closed
→ tmyX artifact 45 rejected; heading/duty/depth defects fixed
→ P1.6 46 accepted → Capability 15 accepted → operations/platform closed
→ Market truthfulness and sampling accepted
```

For every heterogeneous role review:

- factual coverage and exact evidence;
- required/preferred/contextual strength;
- concept-specific explicit depth;
- role-level constraints;
- qualification-vs-duty separation;
- Capability complete requirement/responsibility coverage and provenance;
- grouping coherence without catch-all collapse;
- no fabricated prerequisites, responsibilities, ownership, lifecycle, architecture, autonomy, or mandatory strength;
- deterministic defect vs local-model limitation vs harmless non-authoritative variation.

Repeatable deterministic failures become regression tests. Harmless model wording variation does not justify a contract change.

**P1-A is done when:** promoted P1.6 v20 + Capability v9 remain semantically acceptable across the bounded heterogeneous sample with no unresolved repeatable material correctness defect. Blueprint is explicitly excluded from this Phase-1 acceptance requirement.

---

## 7. Gate P1-B — Market truthfulness — closed

After P1-A is acceptable:

- exact analyzed-current sample size visible;
- source/filter scope recoverable;
- current analysis contract recoverable;
- requirement-strength semantics remain honest;
- per-job prevalence does not inflate from duplicate claims;
- small-sample warning;
- employer/role concentration warning where appropriate;
- coverage and semantic quality remain separate concepts.

Capability and Blueprint do not enter current Market aggregation yet.

Accepted live state: five accepted/current English P1.6 jobs across five employers. The surface exposes 5/43/353 analyzed/parsed/discovered coverage, exact model/prompt/schema identity, source and filter scope, posting-level non-exclusive strength semantics, the absence of repost/near-duplicate adjustment, a small-sample warning, and a clear boundary between per-posting semantic acceptance and market representativeness.

---

## 8. Gate P1-C — Source/lifecycle acceptance — closed

Deterministic/live acceptance must protect:

```text
network failure != expired/removed
429             != empty/removed
500/502/503/504 != expired
challenge/auth  != missing vacancy
provider error  != valid zero-result search
```

First 404/410 remains cautious. Destructive removal follows the defined stronger/repeated evidence rule.

Complete/accept:

- source classification fixtures;
- last-successful-check summary;
- consecutive-failure summary;
- lifecycle UI;
- source truth vs user triage boundary.

Focused deterministic acceptance covers network failures, 429, 5xx, challenge/auth responses, explicit expiry, cautious repeated 404/410 removal, recovery to active, and last-success/consecutive-failure health summaries. Real accepted-anchor health output remains active and inspectable.

---

## 9. Gate P1-D — Partial-success operation semantics — closed

Multi-stage workflows expose where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

Requirements:

- valid earlier durable work survives later failure;
- mixed success is not presented as simple success;
- no-eligible-work != attempt-failed;
- browser and CLI semantics agree;
- affected/failed jobs are inspectable where practical.

Accepted implementation uses one `Phase1RunService` and one formatter for CLI and browser full workflows. Its outcome ledger reports requested limits/selections, attempted, completed, reused/unchanged, failed, intentionally skipped, and remaining eligible work. Translation backlog size is calculated independently of the batch limit. Quick Add propagates detail/translation/analysis failures as `completed_with_failures`; clean no-work and operator-not-requested paths remain successful intentional skips. Completed durable work still triggers the public-corpus projection hook even when a later stage fails.

---

## 10. Gate P1-E — P1.7 run/reporting — closed

Accepted:

- per-job analysis/report provenance surface;
- operation result links;
- bounded ready-job analysis queue;
- combined current-corpus report;
- final bounded `jobhunter run` orchestration;
- browser equivalent using the same services;
- honest partial failures;
- rerun/idempotency behavior;
- deterministic end-to-end acceptance;
- bounded live end-to-end acceptance.

---

## 11. Phase-1 closure — accepted

Phase 1 closes only when:

- deterministic Ruff/pytest/warnings gates are green on the accepted head;
- current migration/source/translation behavior is explainable/non-destructive;
- P1.6 + Capability semantic-quality representative sample is accepted;
- Blueprint remains explicitly non-authoritative/deferred unless later evidence formally reopens it;
- source/lifecycle failure classes are safe;
- Market scope/warnings are truthful;
- partial-success semantics are honest;
- final run/report/browser paths are accepted;
- current documentation matches actual accepted state;
- accepted P1.6 + Capability contract is explicitly identified/frozen as Phase-2 input.

All listed conditions passed on 2026-08-23. The accepted evidence is recorded in `docs/working-memory/2026-08-23_P1_7_AND_PHASE_1_CLOSURE.md`. Phase 2 may proceed through focused, reviewed increments; corpus-wide generation remains gated by the P2.1 registry contract.

---

# Part II — Phase 2: canonical market intelligence

## 12. P2.1 Canonical concept registry

After Phase-1 closure, build the smallest useful reviewed registry for:

```text
tools/platforms/frameworks/languages
skills
knowledge areas
practices
domains
experience signals
education/credentials
responsibilities
deliverables
```

Requirements:

- stable IDs;
- reviewable aliases;
- mapping provenance;
- historical/supersession behavior;
- explicit unknown/unmapped state.

Do not auto-grow taxonomy from model output without review.

---

## 13. P2.2 Responsibilities/deliverables and role families

Build upward from accepted source claims:

```text
source responsibility
→ canonical responsibility
→ responsibility family
→ evidence-derived role archetype
```

Do not force titles into a predeclared role taxonomy.

---

## 14. P2.3 Corpus-scale capability requirement profiles

Promote the accepted factual substrate and bounded Capability grouping/source-truth lessons into reviewed canonical market relationships.

For material capabilities preserve where supported:

- canonical capability;
- exact employer wording;
- employer obligation/strength;
- employer-stated depth;
- expected work activities;
- deliverables;
- technical scope/sub-capabilities;
- underlying knowledge/practices;
- independence/ownership;
- operational/production context;
- explicit experience signals;
- exact evidence/provenance;
- confidence/unknown scope;
- contract/review state.

Do not reduce this to one beginner/intermediate/advanced number.

Capability v9 grouping and deterministic source truth may inform Phase-2 design, but model-owned explanatory prose is not automatically canonical authority. Blueprint-generated interpretation is not automatically promoted into this layer. Any later professional interpretation requires its own reviewed grounding contract.

---

## 15. P2.4 Market v2

Aggregate only reviewed/current canonical mappings/profiles.

Expose:

- posting count;
- distinct-employer count;
- requirement-strength distribution;
- explicit vs implied/inferred support;
- role/archetype/source scope;
- sample size;
- contract/taxonomy identity;
- duplicate/repost adjustment state;
- uncertainty/warning state.

---

# Part III — Phase 3: reviewed personal evidence

## 16. Personal evidence before personal scoring

Define a separate reviewed personal-evidence domain with:

- capability;
- depth dimensions;
- confidence;
- recency;
- evidence reference/type;
- limitations;
- AI-assistance/independence context;
- review state.

Do not infer mastery from chat memory, dependency files, project completion, or repository keywords.

Backup/restore/privacy boundaries must exist before irreplaceable personal state becomes central.

---

# Part IV — Phase 4: explainable gaps/actions/applications

## 17. Gap/readiness/action layer

Compare canonical job requirement profiles against reviewed personal evidence.

Expose reasons and uncertainty rather than opaque global fit scores.

Distinguish knowledge, practice, depth, integration, evidence, recency, experience-context, presentation, and external constraints where supported.

---

## 18. Application preparation

Resume/interview/application assistance may use only reviewed personal evidence for material user claims.

User remains final approver.

No autonomous applications or recruiter messages.

---

# Part V — Phase 5: sustained operation

## 19. Longitudinal market/outcome intelligence

Add trends, recovery/backup, reviewed outcome learning, and maintenance only after upstream data/quality boundaries are stable.

Do not infer causal rejection reasons from outcomes without explicit evidence.

---

## 20. Deferred advanced programs

Require explicit promotion/evidence before implementation:

- generic source-plugin framework;
- multi-source abstraction before a real second source exists;
- vector/RAG platform;
- graph database;
- specialist agent orchestration;
- multi-model voting;
- cloud-first personal data;
- autonomous application workflows;
- corpus-wide Blueprint generation or authoritative Blueprint use before a materially stronger grounding contract exists.

---

## 21. Current plan links

```text
ROADMAP.md
→ strategic direction

PHASE_1_JOBINJA_AUTOMATION_PLAN.md
→ active Phase-1 detail

SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
→ active heterogeneous semantic-quality sub-gate

EXECUTION_TODO.md
→ exact current operational checklist

WORKING_MEMORY.md
→ rolling handoff/current state, non-authoritative
```
