# JobHunter Architecture

**Status:** Current architecture  
**Date:** 2026-09-02

JobHunter is a **local-first Python modular monolith** for turning public job-market evidence into traceable career intelligence.

This document describes the current implemented system and its authority boundaries. Product meaning is defined more fully in `docs/PRODUCT_SPECIFICATION.md`; source/evidence rules remain controlled by `docs/SOURCE_POLICY.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, and `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`.

---

## 1. Architectural direction

One application owns:

- typed configuration;
- bounded approved-source acquisition;
- immutable source evidence;
- deterministic Jobinja parsing and source-version identity;
- fetch/check/lifecycle state;
- SQLite persistence and migrations;
- provenance-preserving English projection;
- reviewed P1.6 factual semantic extraction;
- Capability Intelligence;
- Job Work Intelligence;
- reviewed Canonical Concept Registry mappings;
- bounded Market/report read models;
- experimental historical Role Capability Blueprint research;
- repository-safe public-corpus projection;
- selected review-snapshot export;
- browser and CLI interaction surfaces.

The current deployment target is one local application/process and one local SQLite database. The browser is a server-rendered interface over the same services and durable records used by the CLI; it is not a separate frontend product with a second analytical data model.

```text
                         JobHunter local application

 Browser UI                                                 CLI
 normal repeated use                              automation / review / debug
      \                                                       /
       \                                                     /
        └──────────── shared application services ──────────┘
                              │
                              ▼
                           SQLite
                     structured runtime/history
                              +
                     immutable raw evidence
                              │
                              ▼
                 deterministic repository projections
                     ┌───────────────┴──────────────┐
                     ▼                              ▼
                  corpus/                    review-snapshots/
          complete repository-safe          selected semantic-review
          current public projection          / acceptance evidence
```

SQLite and raw evidence remain runtime/history authority. Repository projections are inspectable outputs, not runtime write authorities.

---

## 2. Why a modular monolith

The current architecture deliberately favors a modular monolith over microservices or distributed infrastructure.

Reasons:

- JobHunter is a local repeated-use utility, not a multi-tenant hosted platform;
- acquisition, semantic processing, review, persistence, and UI all benefit from one explicit local transaction/history boundary;
- SQLite is sufficient for current scale and offers simple durable inspection and migration;
- browser and CLI can share the same services without duplicate APIs or state models;
- local LM Studio inference fits the privacy and offline-first product direction;
- distributed queues, service discovery, orchestration, Kubernetes, a separate SPA, or cloud databases would add operational complexity without a demonstrated product need.

This is not a permanent ban on decomposition. A domain should split into another process/repository only when measured scale, isolation, deployment, ownership, or reliability requirements justify that cost.

---

## 3. Permanent architectural principles

1. Preserve source evidence before parsing, translation, or interpretation.
2. Keep source acquisition useful when LM Studio is unavailable.
3. Keep source fact, English projection, factual extraction, normalization/correspondence, interpretation, aggregation, and future personal evidence distinct.
4. Deterministic parsing, identity, provenance, counts, lifecycle, coverage, currentness, and bookkeeping remain deterministic.
5. Treat acquired content as untrusted data, never instructions.
6. Keep source-specific behavior explicit and bounded.
7. Keep browser and CLI on the same services and durable state.
8. Use SQLite as canonical local structured runtime/history state until measured limits justify replacement.
9. Keep raw evidence independently inspectable.
10. Separate semantic source versions from volatile HTTP/fetch observations.
11. Separate operational attempts from successful semantic/derived artifacts.
12. Preserve native-versus-translated provenance.
13. Preserve exact source/model/prompt/schema/dependency identity for durable derived artifacts.
14. Prefer missing, unknown, limited, or review-required over fabricated certainty.
15. Bound requests, pages, batches, retries, model calls, validation retries, and output size where applicable.
16. Deterministic bookkeeping repairs belong in code, not repeated model calls.
17. Models may organize and interpret accepted evidence; they do not manufacture source truth.
18. Generated/candidate state is distinct from reviewed/promoted state.
19. Add complexity only for observed product need.
20. Keep local-first privacy and network boundaries explicit.
21. Historical artifacts remain historical when contracts change.
22. Coverage and semantic quality are different properties.
23. Runtime persistence and repository projections have different authority.
24. Public-data projection never authorizes future private/personal state for publication.
25. Downstream interpretation must never silently strengthen upstream evidence.

---

## 4. Epistemic authority model

The system uses four conceptual authority levels:

```text
SOURCE FACT
    ↓
NORMALIZED CORRESPONDENCE
    ↓
ANALYTICAL INTERPRETATION
    ↓
RECOMMENDATION / DECISION SYNTHESIS
```

Current JobHunter is strongest in the first three levels. Personal recommendation/decision synthesis remains future work.

The practical rule is:

> A downstream layer may organize, normalize, or interpret evidence only within its authorized scope; it never upgrades unsupported meaning into source fact.

Never conflate:

```text
Raw evidence                 exact acquired source bytes + metadata
JobPosting                   stable logical source identity
JobPostingVersion            meaningful employer-content version
Fetch/check observation      one operational source check
Lifecycle state/event        cautious source-availability interpretation
Translation artifact         derived English representation
P1.6 artifact                reviewed factual semantic substrate
Capability artifact          bounded capability-level organization/reasoning
Work Intelligence artifact   bounded work organization/interpretation
Canonical concept            reviewed reusable correspondence identity
Canonical claim mapping      reviewed exact P1.6 claim → concept decision
Market/report aggregate      bounded read model over accepted evidence
Blueprint artifact           experimental historical interpretation
User workflow state          local human triage, not employer truth
Public Corpus                repository-safe current public projection
Review Snapshot              selected semantic-review evidence
```

---

## 5. Current end-to-end data and authority flow

```text
TOML configuration
        ↓
data-driven bilingual Jobinja search catalog
        ↓
bounded deterministic search plan
        ↓
Jobinja acquisition
        ↓
immutable source evidence
        ↓
stable JobPosting identity + discovery provenance
        ↓
classified detail fetch / refresh observations
        ↓
jobinja-detail-v2 deterministic parsing
        ↓
semantic JobPostingVersion
        ↓
current English projection v2
        ↓
English P1.6 candidate
        ↓
explicit semantic review
        ↓
ACCEPTED/CURRENT P1.6 FACTUAL SUBSTRATE
        │
        ├────────→ Capability Intelligence v9
        │            bounded capability grouping/reasoning
        │            exact source survival remains deterministic
        │
        ├────────→ Job Work Intelligence v2
        │            bounded work grouping/interpretation
        │            exact accepted work is injected deterministically
        │
        ├────────→ Canonical Concept Registry
        │            reviewed exact requirement/responsibility mappings
        │            no automatic ontology promotion
        │
        └────────→ Market / report read models
                     bounded aggregates over accepted evidence
```

This fan-out is important. Capability, Work Intelligence, Canonical Registry, and Market are different consumers of accepted P1.6. None is allowed to rewrite P1.6 source truth.

The current P2.2B pilot is testing selective reviewed responsibility correspondence through the existing Canonical Registry. Responsibility families/archetypes and broader Market v2 remain later work.

---

## 6. Current contract identities

```text
Source parser
  jobinja-detail-v2

Translation
  provider/runtime: lm-studio-translation-v2
  projection:       english-projection-v2

P1.6 factual extraction
  English runtime:  job-analysis-english-v20
  English schema:   job-analysis-v5
  Original runtime: job-analysis-original-v9
  Original schema:  job-analysis-v4

Capability Intelligence
  runtime:           job-capability-intelligence-v9
  schema:            job-capability-intelligence-v5

Job Work Intelligence
  contract/schema:   job-work-intelligence-v2
  runtime/prompt:    job-work-intelligence-v2.0
  deterministic limited path:
                     jobhunter-deterministic-limited-work-v2

Canonical Registry
  jobhunter-canonical-concept-registry-v1

Experimental Blueprint
  runtime:           role-capability-blueprint-v6
  schema:            role-capability-blueprint-v5

Review Snapshot
  job-review-snapshot-v1

Public Corpus
  jobhunter-public-corpus-v1
```

Prompt/runtime changes intentionally create distinct current/historical artifacts even when a persisted schema remains compatible.

Current accepted heterogeneous P1.6 → Capability anchors are:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

These are acceptance anchors, not a claim that every discovered job has been semantically analyzed.

---

## 7. Source registry and acquisition boundary

The Jobinja acquisition subsystem owns:

- approved host/path/URL validation;
- canonical source identity;
- bilingual configurable search planning;
- bounded sequential requests;
- redirect/content-type/response-size validation;
- search and detail acquisition;
- classified failure/retryability state;
- deterministic source-specific parsing;
- discovery provenance;
- refresh selection;
- lifecycle evidence.

Critical invariant:

```text
network / 429 / 5xx / challenge / auth / access failure
!=
expired or removed vacancy
```

Provider/source failure is never treated as a valid empty result.

---

## 8. Evidence and source-version model

Exact acquired evidence is preserved independently from normalized records.

The system distinguishes:

```text
logical job identity
raw observation
meaningful semantic content version
operational source check
lifecycle interpretation
```

Volatile HTML changes must not manufacture a semantic job version.

`jobinja-detail-v2` extracts explicit public fields such as title, company, category, location, employment type, minimum experience, salary, description, skills, gender, military-service requirement, education, company description, source dates, language, and parser version where supplied.

Missing employer values stay missing. Parser metadata is not employer evidence. Structural parser correctness is not semantic-quality certification.

---

## 9. Persistence and operational-history model

SQLite is canonical structured runtime/history state.

Durable domains include separate records for:

- searches and discovery provenance;
- source evidence/version state;
- fetch/check/lifecycle observations;
- translation artifacts and attempts;
- P1.6 artifacts, attempts, and semantic-review state;
- Capability artifacts and attempts;
- Work Intelligence artifacts;
- Canonical Registry concepts, aliases, and claim mappings;
- experimental Blueprint artifacts/attempts;
- user workflow state;
- application/report support state where applicable.

Schema migration is application-owned, deterministic, and regression-tested.

An operational failure does not erase already committed successful work from earlier pipeline stages.

---

## 10. Translation boundary

Current English flow:

```text
current parsed source version
→ semantic source segments
→ native-English identity OR bounded translation
→ structured response validation
→ deterministic integrity checks
→ english-projection-v2
```

The original employer source remains authoritative. English projection is derived convenience data with segment provenance and exact source dependency.

LM Studio is the normal local translation provider. Optional external translation is deliberate and policy-controlled rather than an implicit fallback.

---

## 11. P1.6 factual semantic boundary

P1.6 is the reviewed factual substrate used by higher layers.

It extracts conservative employer-supported information including:

- role purpose when explicitly supported;
- responsibilities;
- requirements;
- required/preferred/contextual/inferred strength where authorized;
- concept type;
- source-explicit concept-scoped depth;
- confidence;
- exact evidence/provenance.

Important invariants:

- qualifications do not become duties;
- contextual tools do not become required expertise without evidence;
- one adjective/depth statement is not spread across neighboring concepts;
- unsupported role purpose is omitted;
- evidence must validate against authoritative employer fields;
- fresh English v20 artifacts remain `pending` until explicit semantic review;
- pending candidates are inspectable but excluded from accepted downstream layers;
- rejection archives local candidate evidence and removes the rejected artifact from current runtime state so the same contract can be rebuilt.

`src/jobhunter/analysis_current.py` is the current public routing boundary: English uses v20/v5 while original-language P1.6 remains on independently validated v9/v4.

---

## 12. Capability Intelligence boundary

Capability Intelligence v9 consumes accepted/current English P1.6 and organizes source truth into coherent capability areas.

```text
accepted P1.6 source truth
→ compact capability-group plan
→ bounded exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic source-link injection
→ deterministic reconciliation
→ persisted Capability
```

Authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Complete source coverage/provenance is mandatory. Requirement strength, source-explicit depth, and source work activities are deterministic. Unsupported ownership, lifecycle, autonomy, architecture, or optionality inflation is blocked or filtered. Zero optional enrichment is valid.

Historical v7/v8 implementations remain historical/reproducibility material rather than current public contracts.

---

## 13. Job Work Intelligence v2 boundary

Job Work Intelligence addresses a different question from Capability Intelligence: **how is the accepted direct work of this job usefully organized?**

Permanent authority rule:

> The model decides how accepted work is usefully organized; accepted P1.6 statements decide what factual work is actually asserted.

Current flow:

```text
accepted/current English P1.6
→ typed candidate work interpretation
→ deterministic source-reference / coverage / scope validation
→ at most one bounded regeneration after deterministic rejection
→ deterministic injection of exact accepted P1.6 work statements
→ exact dependency validation
→ persisted Work Intelligence artifact
```

The model may propose:

- work themes;
- relative primary/supporting/uncertain emphasis;
- bounded deliverable candidates;
- tentative role interpretation;
- limitations/uncertainty.

The model may **not** replace accepted factual work statements or turn requirements into duties.

Scope inflation such as unsupported `end-to-end`, `full lifecycle`, ownership, autonomy, or deployment responsibility is rejected/controlled.

For requirement-only jobs with no accepted direct responsibility/role-purpose evidence, JobHunter takes a deterministic `limited` path and does not call the model to invent work.

Work Intelligence is accepted P2.2A functionality. Its interpretive themes/deliverables are not automatically promoted into the Canonical Registry or Market taxonomy.

---

## 14. Canonical Concept Registry boundary

The Canonical Registry provides **reviewed reusable correspondence identities** across exact accepted P1.6 claims.

Current contract:

```text
jobhunter-canonical-concept-registry-v1
```

It stores:

- stable explicit `category:slug` concept IDs;
- preferred labels;
- reviewed aliases with provenance;
- concept status/deprecation relationships;
- immutable reviewed exact-claim mapping decisions;
- exact P1.6/source/translation dependency identity;
- mapped / unmapped / rejected dispositions.

Current claim mappings operate on accepted/current P1.6:

```text
requirement
responsibility
```

A `deliverable` concept category exists, but candidate Work Intelligence deliverables do not currently have an authorized automatic mapping path.

The Registry is deliberately human-reviewed. Similar words, shared domains, or partial semantic overlap do not prove canonical equivalence. No model is allowed to silently create or accept canonical concepts/aliases/mappings.

The current P2.2B-B1 pilot is a selective responsibility-promotion proof, not a completeness-driven taxonomy build.

---

## 15. Market and report read-model boundary

Current Market/report surfaces aggregate bounded accepted/current evidence for inspection and operational understanding.

They may expose:

- analyzed sample size;
- responsibility/requirement counts;
- requirement-strength prevalence;
- source/search effectiveness/provenance views;
- current pipeline/artifact counts and queues;
- lineage/currentness information.

Current Market is not yet a reviewed corpus-wide canonical role taxonomy or Market v2.

Capability, Work Intelligence themes, Blueprint interpretations, and speculative canonical relationships are not silently mixed into Market truth.

---

## 16. Browser and CLI interaction surfaces

### Browser

Current web stack:

```text
FastAPI
Uvicorn
Jinja2
packaged CSS
small vanilla JavaScript
```

No Node/npm build or runtime CDN is required.

The browser covers repeated-use workflows across overview/reporting, job inspection, source/translation/analysis state, semantic review, Capability Intelligence, Work Intelligence, Canonical Registry review, acquisition/search operations, and experimental Blueprint inspection where explicitly labeled.

### CLI

The CLI remains a first-class technical surface for automation, debugging, acceptance, inspection, and advanced workflows.

Representative entry points:

```bash
jobhunter ...
jobhunter-work ...
jobhunter-registry ...
jobhunter-corpus ...
```

Both browser and CLI use shared application services and the same durable state.

---

## 17. Browser security and operation boundary

The browser is loopback-first.

Protections include:

- CSRF validation for mutating forms;
- restrictive Content Security Policy;
- frame/content-type/referrer/cache protections;
- packaged local static assets;
- acquired job text rendered as data, never instruction/tool authority;
- bounded background-operation coordination;
- durable service work committed before repository projection hooks run.

If a post-success public-corpus projection fails, durable SQLite state remains preserved and the operation reports the projection failure rather than silently diverging.

---

## 18. Configuration and model-role boundary

Configuration is typed TOML plus selected `JOBHUNTER_*` environment overrides. Unknown configuration fails closed.

Semantic roles may use independent local models:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

The best factual extractor is not assumed to be the best higher-level reasoning model.

Model adequacy is evaluated with controlled evidence/contract/model comparisons. Evidence, contract, and model should not all change simultaneously when diagnosing one variable.

---

## 19. Public Corpus architecture

The runtime database remains local and ignored. The complete repository-safe current public projection lives under:

```text
corpus/
```

Current contract:

```text
jobhunter-public-corpus-v1
```

Current job layout:

```text
corpus/jobs/<job-id>/source.json
corpus/jobs/<job-id>/english-projection.json
corpus/jobs/<job-id>/p16-english.json
corpus/jobs/<job-id>/p16-original.json
corpus/jobs/<job-id>/capability.json
```

The current public-corpus contract deliberately does **not** project Work Intelligence, Canonical Registry state, experimental Blueprint state, raw model protocol, SQLite, or future personal evidence.

Properties:

- deterministic sorted UTF-8 JSON;
- atomic file replacement;
- every known Jobinja identity represented by the manifest;
- exact current source/derived dependency identities;
- stale downstream stage files removed when source/dependency currentness changes;
- deterministic DB↔corpus verification;
- no network/model calls during export or verification.

Excluded:

- SQLite/WAL/SHM;
- raw HTML evidence;
- machine-local evidence paths;
- raw model request/response protocol;
- prompts, secrets, logs, and local config;
- future personal/private evidence, applications, notes, profiles, or outcomes.

Git commit/push is intentionally manual. Runtime correctness never depends on GitHub availability.

---

## 20. Review Snapshot architecture

`review-snapshots/` stores deliberately selected repository-safe semantic-review/acceptance evidence.

```text
corpus/           complete current public projection
review-snapshots/ selected review / regression evidence
```

Snapshots may preserve current/historical compatible semantic chains and model/config identities needed for inspection, while excluding raw model protocol, SQLite, secrets, logs, machine-local evidence, and future private state.

Current-chain flags prove dependency currentness. They do not themselves prove semantic acceptance.

---

## 21. Experimental Blueprint boundary

Role Capability Blueprint v6 remains implemented for historical research/inspection but is **not an accepted current decision layer**.

It is pinned to historical Capability v7 dependency semantics and is intentionally not silently rebased onto Capability v9.

Blueprint must not feed current Market truth, personal readiness, recommendations, canonical promotion, or other authoritative decisions unless separately redesigned and accepted later.

---

## 22. Future private/personal state

Current workflow triage remains local human state and is not employer truth.

Personal capability evidence, readiness, gaps, constraints, applications, outcomes, and strategy remain later product domains.

When implemented, personal evidence must have an explicit reviewed/private authority model separate from public market evidence. Coexistence in SQLite would not authorize publication into `corpus/`.

---

## 23. Runtime model-call policy

For long local semantic generation, JobHunter distinguishes connection establishment from legitimate post-connection reasoning.

Current principle:

```text
connection establishment bounded
transport retries bounded/explicit
output tokens bounded
structured validation retries bounded
legitimate local generation not killed only by an arbitrary short read deadline
```

This policy is local-runtime specific and does not weaken bounded acquisition or validation controls.

---

## 24. Failure semantics

Keep these states distinct:

```text
no eligible work              != operation failure
zero source results           != provider/source failure
stale artifact                != failed artifact
transient source failure      != vacancy removed
translation failure           != source failure
P1.6 failure                  != translation/source failure
semantic rejection            != transport failure
Capability failure            != P1.6 failure
Work Intelligence failure     != P1.6 failure
Registry unmapped/rejected    != registry corruption
Blueprint failure             != Capability failure
corpus projection failure     != rollback of durable SQLite success
partial workflow success      != complete success
```

Earlier valid durable work remains preserved when a later stage fails.

---

## 25. Testing and acceptance strategy

Normal deterministic tests do not contact Jobinja, LM Studio, or Google Cloud.

CI currently runs:

```bash
ruff check .
pytest
pytest -W error
```

Important real failures become deterministic fixtures where possible.

Acceptance distinguishes at least:

- deterministic contract defects;
- source ambiguity or weak evidence density;
- model-quality limitations;
- domain/technical correctness issues;
- bookkeeping/provenance/currentness defects;
- repository-projection drift;
- UI/CLI representation defects.

Accepted semantic layers are not reopened for harmless non-authoritative wording variation.

---

## 26. Current architectural state

```text
Phase 1                         CLOSED
P2.1 Canonical Registry        CLOSED
P2.2A Job Work Intelligence    ACCEPTED / CLOSED
P2.2B selective responsibility promotion pilot    IN PROGRESS
```

Current P2.2B-B1 is deliberately narrow: prove or reject one reviewed reusable responsibility correspondence using exact accepted/current P1.6 evidence. It does not authorize responsibility families, broad ontology construction, deliverable promotion, Market v2, or personal scoring.

The machine-local next gate for that product work remains `ta9l` English projection → P1.6 v20/v5 generation → semantic review → final correspondence evaluation.

Portfolio/documentation work may proceed independently but must not bypass that product gate or change accepted semantics.

---

## 27. Planned architectural evolution

The intended direction remains:

```text
MARKET EVIDENCE
→ reviewed reusable concepts / responsibility correspondence
→ responsibility families / role intelligence when justified
→ REVIEWED PERSONAL EVIDENCE
→ gaps / constraints / readiness
→ learn / practise / build / verify actions
→ application decision
→ outcome
→ updated evidence and decisions
↺
```

Future additions should preserve the same architecture discipline:

- explicit evidence authority;
- review where authority increases;
- deterministic provenance/currentness;
- bounded model reasoning;
- local-first privacy;
- no generic retrieval/agent/vector/distributed infrastructure until a measured need proves its value.
