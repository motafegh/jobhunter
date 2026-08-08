# JobHunter Master Implementation Plan

**Status:** Controlling product-level implementation plan  
**Date:** 2026-08-08

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

A **bounded per-job Capability/Blueprint slice** is implemented before Phase-1 closure solely to evaluate whether P1.6 is a useful substrate and to establish the later capability contract. This does **not** authorize Phase-2 corpus-wide generation, taxonomy growth, Market-v2 aggregation, or personal scoring.

---

## 4. Current accepted/strong foundation

Current strong foundations include:

- local Python modular monolith;
- SQLite structured state + immutable raw evidence;
- browser + CLI shared services/state;
- bounded repeat-safe bilingual Jobinja discovery;
- stable logical job identity and discovery provenance;
- deterministic `jobinja-detail-v2` parsing;
- semantic source versions separate from source checks;
- classified source outcomes and cautious lifecycle logic;
- user triage separate from source truth;
- hardened `english-projection-v2` architecture;
- local LM Studio structured inference boundary;
- P1.6 Instructor/Pydantic factual extraction infrastructure;
- first Market aggregation over accepted/current English P1.6;
- bounded per-job Capability Intelligence persistence/surface;
- bounded Role Capability Blueprint persistence/surface;
- independent analysis/capability/blueprint model roles;
- repository Review Snapshot export.

Historical translation-v1 remains preserved but non-current.

Phase 1 is not closed until the remaining acceptance gates below pass.

---

## 5. Current active contract identities

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6 prompt/runtime:  job-analysis-english-v4
Original P1.6 prompt/runtime: job-analysis-original-v4
P1.6 schema:                  job-analysis-v2

Capability prompt/runtime:    job-capability-intelligence-v4
Capability schema:            job-capability-intelligence-v2

Blueprint prompt/runtime:     role-capability-blueprint-v2
Blueprint schema:             role-capability-blueprint-v1

Review Snapshot:              job-review-snapshot-v1
```

Historical prompt/runtime identities remain historical.

---

# Part I — Finish Phase 1

## 6. Gate P1-A — Semantic-quality acceptance (active now)

This is the immediate current gate.

Detailed plan:

```text
docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
```

Operational checklist:

```text
docs/EXECUTION_TODO.md
```

### P1-A0 — Review Snapshot correctness

First code task:

- integrated `jobhunter jobs snapshot` must pass effective analysis/capability/blueprint model roles into the exporter;
- snapshot chain selection must remain dependency-correct under multiple current model artifacts;
- regenerate `tG9K` and confirm explicit configured model identities.

Do this before controlled model comparison.

### P1-A1 — P1.6 factual coverage / optionality / depth

P1.6 is the factual substrate and must be corrected before downstream tuning.

Acceptance requires representative reviewed examples to show:

- responsibilities are not confused with candidate qualifications;
- meaningful explicit requirements on dense postings are not silently omitted;
- evidence is exact selected-representation source text;
- employer optionality is preserved;
- explicit technical depth is preserved separately from obligation strength;
- one depth adjective does not spread to neighboring technologies;
- structured experience/education signals are not lost merely because a long description is dense;
- unsupported facts remain omitted/rejected.

Current key rich example: `tG9K`.

The current four-way P1.6 requirement enum (`required`, `preferred`, `contextual`, `inferred`) may be revised only if reviewed evidence demonstrates that mixed/unspecified employer wording cannot be represented truthfully.

### P1-A2 — Capability Intelligence calibration

Capability must add useful auditable reasoning without amplifying factual mistakes.

Acceptance requires:

- explicit/implied/inferred/unknown remain distinct;
- `depth_signals` are used when material evidence exists;
- requirement strength is not systematically inflated;
- optional deployment/context wording stays appropriately uncertain;
- capability grouping remains coherent;
- invalid-only supported evidence fails closed;
- invalid-only unknown evidence may normalize to empty;
- deterministic bookkeeping failures do not consume arbitrary repeated LLM repairs.

### P1-A3 — Role Capability Blueprint calibration

Blueprint must remain useful human interpretation, not source restatement.

Acceptance requires:

- professional frame matches the actual role;
- source optionality/unknowns survive downstream;
- technology lists are not automatically turned into architecture specifications;
- `highly_likely` does not contradict explicit unknowns;
- likely/possible examples remain examples;
- technical/domain terms are used correctly;
- scenario detail scales with source evidence density;
- output avoids generic curriculum dumping.

### P1-A4 — Controlled model-role comparison

After deterministic contract fixes, compare a stronger local reasoning model if current Gemma still shows expert-judgment limitations.

Keep fixed:

```text
source semantic version
English projection
accepted P1.6 artifact
prompt/schema contract
review rubric
```

Change only the relevant Capability/Blueprint model.

Do not build multi-model voting.

### P1-A5 — Representative CI-3 sample

Use at least five materially different jobs where possible:

```text
t4jp  sparse/ambiguous
tG9K  rich AI/ML industrial
+ Python/software
+ network/security
+ operations/platform
```

Review the complete chain through repository snapshots.

Repeatable deterministic failures become tests. Model limitations are documented separately.

**P1-A done when:** the bounded semantic stack is good enough to freeze/promote as Phase-2 input, or one final clearly justified contract/model revision remains.

---

## 7. Gate P1-B — Market truthfulness

After P1-A is acceptable:

- exact analyzed-current sample size visible;
- source/filter scope recoverable;
- current analysis contract recoverable;
- requirement-strength semantics remain honest;
- per-job prevalence does not inflate from duplicate claims;
- small-sample warning;
- employer/role concentration warning where appropriate;
- coverage and semantic quality remain separate concepts.

Capability/Blueprint do not enter Market yet.

---

## 8. Gate P1-C — Source/lifecycle acceptance

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

---

## 9. Gate P1-D — Partial-success operation semantics

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

---

## 10. Gate P1-E — Finish P1.7 run/reporting

Complete/accept:

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

## 11. Phase-1 closure

Phase 1 closes only when:

- deterministic Ruff/pytest/warnings gates are green on the accepted head;
- current migration/source/translation behavior is explainable/non-destructive;
- semantic-quality representative sample is accepted;
- source/lifecycle failure classes are safe;
- Market scope/warnings are truthful;
- partial-success semantics are honest;
- final run/report/browser paths are accepted;
- current documentation matches actual accepted state;
- accepted P1.6 contract is explicitly identified as Phase-2 input.

No corpus-wide Phase-2 work before closure.

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

Promote the bounded per-job Capability contract into reviewed canonical market relationships.

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
- autonomous application workflows.

---

## 21. Current plan links

```text
ROADMAP.md
→ strategic direction

PHASE_1_JOBINJA_AUTOMATION_PLAN.md
→ active Phase-1 detail

SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
→ current semantic-quality sub-gate

EXECUTION_TODO.md
→ exact current operational checklist

WORKING_MEMORY.md
→ rolling handoff/current state, non-authoritative
```
