# JobHunter Architecture

## 1. Architectural direction

JobHunter is a **local Python modular monolith**.

One application owns configuration, approved-source acquisition, evidence preservation, SQLite persistence, deterministic parsing, translation, evidence-backed semantic analysis, market read models, and two interaction surfaces:

```text
Browser UI       normal repeated human use
CLI              automation, debugging, tests, advanced operation
        \         /
         application services
                ↓
             SQLite
        + raw evidence files
```

The browser is not a separate frontend product with its own API/data model. It is a thin server-rendered interface over the same application services and durable records used by the CLI.

The architectural target remains one local process/deployment. Future product domains may gain focused modules/repositories, but they do not become microservices merely because the feature set grows.

## 2. Permanent principles

1. Preserve raw source evidence before parsing, translation or interpretation.
2. Keep successful acquisition independent from LM Studio/model availability.
3. Keep source evidence independent from translation availability.
4. Separate deterministic source parsing from model-dependent processing.
5. Keep source-specific behavior behind explicit source modules/adapters.
6. Keep browser/CLI handlers as composition/validation code, not source parsing or analytical truth logic.
7. Use SQLite as the local structured system of record.
8. Keep raw source evidence inspectable outside normalized records.
9. Design repeated operations for idempotency.
10. Separate semantic source versions from volatile HTTP responses.
11. Separate operational fetch/check history from semantic source versions.
12. Separate translation artifacts from authoritative source versions.
13. Separate semantic-analysis artifacts from source and translation artifacts.
14. Preserve native-versus-translated provenance.
15. Prefer missing/review-required/uncertain states over fabricated values.
16. Treat acquired content as untrusted data, never executable instruction.
17. Bound pages, requests, detail batches, translation batches, retries and model calls.
18. Keep configuration/policy visible instead of scattering constants.
19. Keep the local web application loopback-first and CSRF-protected.
20. Keep browser and CLI on the same underlying durable state.
21. Version material model/prompt/schema contracts and preserve historical artifacts.
22. Deterministic calculations remain deterministic; models interpret but do not manufacture counts, identity or lifecycle truth.
23. Add complexity only for an observed product need.
24. Keep SQLite and the modular monolith until measured evidence requires replacement.

## 3. Current end-to-end flow

The implemented Phase-1 path is now conceptually:

```text
TOML configuration
        ↓
data-driven bilingual search catalog
        ↓
inspectable bounded search plan
        ↓
sequential Jobinja search acquisition
        ↓
immutable search evidence
        ↓
stable JobPosting identities + discovery provenance
        ↓
missing / refresh-due / priority detail selection
        ↓
sequential detail acquisition
        ↓
classified response / retryability
        ↓
immutable valid detail evidence
        ↓
Jobinja parser v2
        ↓
semantic source version
        ↓
fetch observation + cautious lifecycle evidence
        ↓
structural parser audit
        ↓
current English projection v2
  ├─ source identity for native English
  └─ local LM Studio translation by default
        ↓
translation integrity gate
        ↓
versioned current English artifact
        ↓
evidence-backed P1.6 analysis
        ↓
original-source evidence validation
        ↓
versioned current analysis artifact
        ↓
per-job analysis + first Market aggregation
```

Some of the newer layers above are **implemented but still pending deterministic/live acceptance** under `docs/IMPLEMENTATION_PLAN.md` and the Phase-1 plan. Architecture documentation describes implementation structure; it does not upgrade acceptance state by itself.

## 4. Authority boundaries

Never conflate:

```text
Raw source evidence              exact acquired source bytes/metadata
JobPosting                       stable logical source identity
JobPostingVersion                meaningful employer-content version
Fetch/check observation          one operational source check
Lifecycle interpretation         cautious derived state from source observations
Translation artifact             derived English representation
Translation attempt              operational translation history
Analysis artifact                model-derived interpretation of one exact source version
Analysis attempt                 operational semantic-analysis history
Market aggregate                 deterministic aggregate of accepted current analyses
User workflow state              local human triage/preference state
Browser WebOperation             ephemeral UI execution state
```

Authority hierarchy:

```text
original employer/source evidence    authoritative
        ↓
deterministic parsed fields           source-derived
        ↓
English projection                    derived convenience
        ↓
semantic analysis                     model-derived interpretation
        ↓
current market aggregation            deterministic aggregate of accepted analysis
        ↓
future canonical taxonomy             reviewed/derived mapping
        ↓
future personal evidence              reviewed user-evidence layer
        ↓
future gap/recommendation              explainable system-derived decision
```

A derived layer may depend on an upstream layer but does not replace its authority.

## 5. Interaction surfaces

### 5.1 Local web application

`jobhunter.web` contains the browser application.

Technology remains deliberately small:

```text
FastAPI
Uvicorn
Jinja2
packaged CSS
small vanilla JavaScript
```

There is no Node/npm build system and no runtime CDN dependency.

Current browser domains include:

```text
Overview
Jobs
Job detail
Search plan / search effectiveness
Market
Operations
System
```

Implemented browser actions include bounded acquisition/sync work, Quick Add within the approved Jobinja boundary, detail/backlog work, translation-v2 work, semantic-analysis work and other guided Phase-1 operations exposed by the shared application services.

The UI should expose user-relevant source/English/analysis/current/stale/failure states without becoming a second persistence layer.

### 5.2 Web security boundary

The launcher defaults to `127.0.0.1` and refuses broader binding unless explicitly requested.

The web layer uses protections including:

- CSRF validation on mutating forms;
- restrictive Content Security Policy;
- `X-Frame-Options: DENY`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- no runtime remote static assets.

Acquired job content is rendered as data and must never gain script/tool authority.

### 5.3 Browser operation execution

Long browser operations use bounded in-process execution rather than spawning a separate distributed workflow system.

Current design intentionally avoids overlapping mutable browser workflows until concurrency is explicitly proven safe.

Durable domain results live in source/translation/analysis stores. Browser operation cards are execution-state convenience and do not replace durable domain history.

Future durable `WorkflowRun` records should be introduced only if cross-restart orchestration history becomes a real requirement.

### 5.4 CLI

The `jobhunter` CLI remains supported for scriptability, debugging, explicit batch operation and deterministic/live acceptance work.

Browser and CLI actions must invoke the same underlying source, translation, analysis and persistence contracts.

## 6. Current runtime components

### 6.1 Configuration

Typed TOML plus selected `JOBHUNTER_*` environment overrides. Unknown configuration fields fail closed.

### 6.2 Search registry/planning

Versioned Persian/English profiles and packs live as data rather than Python search-word constants. Planning normalizes identity where required, preserves display terms, builds deterministic bounded search windows and exposes request limits.

Search vocabulary is acquisition recall, not career taxonomy or personal relevance.

### 6.3 Jobinja source boundary

The Jobinja source implementation owns:

- approved-host/path validation;
- canonical source identity;
- request/response bounds;
- redirect validation;
- content-type/size checks;
- discovery-link extraction;
- source-specific parsing behavior.

Source acquisition remains sequential/rate-limited under explicit configuration.

### 6.4 Evidence store

Exact acquired bytes plus metadata sidecars are written before downstream deterministic/model processing where the source response is valid for preservation.

Derived representations never overwrite raw evidence.

### 6.5 Discovery and acquisition state

Discovery persists:

- source searches;
- bounded acquisition runs;
- search-page snapshots;
- stable job identities;
- discovery provenance;
- search contribution/overlap data.

Detail acquisition preserves valid detail evidence, parses it, computes semantic identity and records/reuses the meaningful source version.

### 6.6 Source observations, classification and lifecycle

Operational source checks remain separate from semantic versions.

Current classification/lifecycle work distinguishes transient operational failures from evidence that a vacancy has actually expired/disappeared.

Critical invariant:

```text
network/server/rate-limit/challenge/auth failure
        !=
expired/removed job
```

A first strong missing/gone response is treated cautiously; destructive lifecycle state requires the defined evidence policy.

### 6.7 Deterministic parser

`jobinja-detail-v2` extracts source-explicit fields and complete relevant description text without LLM inference.

Missing values remain missing. Parser metadata is not employer evidence.

Structural parser audit verifies parser structure/contamination checks only; it is not semantic-quality certification.

### 6.8 Translation boundary

Translation is a separate derived layer.

Current trusted path is the hardened v2 architecture:

```text
current parsed source version
→ collect semantic source segments
→ native-English identity OR bounded local translation
→ structured response validation
→ source/English integrity checks
→ persist current English v2 artifact only when clean
```

Historical v1 artifacts remain historical and must not be silently relabeled.

LM Studio is the normal local provider; Google Cloud Translation remains optional external processing.

### 6.9 Semantic-analysis boundary

`analysis_service.py` performs evidence-constrained local semantic analysis.

Current artifact identity includes:

```text
source detail version
+ exact model
+ prompt version
+ analysis schema version
```

The analysis contract currently supports:

- role purpose;
- responsibilities;
- requirements;
- required/preferred/contextual/inferred classification;
- concept type;
- confidence;
- exact original-source evidence;
- rationale for inferred concepts.

Application-side validation verifies material evidence excerpts against authoritative source fields. Parser metadata such as `language` and `parser_version` is excluded from employer-evidence candidates.

A structurally valid model response with unsupported evidence is a failed analysis attempt, not an accepted artifact.

`analysis_store.py` persists immutable/versioned analysis artifacts and separate completed/failed/reused attempt history.

### 6.10 Market read models

The current Market layer reads accepted/current analysis artifacts under the selected analysis contract and computes first deterministic aggregates such as concept demand and requirement-strength counts.

It is not yet the Phase-2 reviewed canonical taxonomy. Alias consolidation, role archetypes, duplicate adjustment and mature sampling/statistical treatment belong to later accepted layers.

### 6.11 User workflow state

Local triage such as interested/review-later/reviewed/not-relevant remains user workflow metadata. It never mutates employer evidence or proves personal fit/readiness.

## 7. Persistence model

### 7.1 Current durable source records

The core source store includes durable records for concepts such as:

```text
source searches
acquisition runs
search-page snapshots
job postings
job discoveries
job detail/source versions
```

`JobHunterStore.initialize()` owns creation/migration of the core Phase-1 schema and must run before dependent stores query newer source columns/tables.

### 7.2 Separate operational/derived stores

Additional repositories/tables preserve separate concerns including:

```text
fetch/check observations
translation artifacts
translation attempts
analysis artifacts
analysis attempts
lifecycle/user-workflow state where implemented
```

This separation is intentional. Do not merge operational attempt history into semantic source versions or derived analytical artifacts.

### 7.3 SQLite migration rule

Schema migration is application-owned, deterministic and regression-tested. Existing source/history rows are not destructively rewritten to make a new contract appear current.

Keep SQLite until measured query, locking, portability or workload constraints demonstrate a real replacement need.

## 8. Current source-of-truth choice

JobHunter intentionally does **not** use editable Markdown/TSV files as the canonical analytical database.

```text
SQLite                    canonical structured application state
raw evidence files         canonical acquired bytes/metadata
versioned exports/reports  derived/portable representations
browser/CLI                interaction surfaces
```

Human-readable exports are valuable, but durable analytical identity, relationships, migrations and provenance remain in structured stores.

## 9. Failure semantics

Important failure distinctions are architectural contracts:

```text
no eligible work          != operation failure
zero source results       != source/provider failure
stale artifact            != failed artifact
transient source failure  != vacancy removed
translation failure       != source-version failure
analysis failure          != source/translation failure
partial workflow success  != complete success
```

Future full-workflow summaries should expose requested/attempted/completed/reused/skipped/failed/remaining counts rather than a single ambiguous success flag.

## 10. Testing and regression strategy

Normal deterministic tests do not contact Jobinja, LM Studio or Google Cloud.

Coverage should protect:

- source URL/identity/versioning;
- bounded acquisition/retry classification;
- parser structure;
- fetch observations/lifecycle rules;
- migration compatibility;
- translation provider/integrity behavior;
- analysis evidence validation and artifact reuse;
- Market aggregation contract selection;
- browser security and shared-service behavior;
- partial-success result semantics;
- real historical failure classes.

Important real incidents become regression fixtures.

Current/near-term adversarial tests should include:

- transient 5xx not becoming expiry/removal;
- provider failure not becoming a legitimate empty result;
- non-Latin/Unicode normalization edge cases;
- fabricated model evidence;
- parser metadata offered as employer evidence;
- prompt-injection-like strings inside acquired job text;
- valid-looking but unsupported model output.

## 11. Future architecture evolution

### 11.1 Phase 2

Add reviewed canonical concepts, responsibility families, role archetypes, market matrices and lineage/review relationships while retaining original P1.6 claims.

### 11.2 Second source

Implement one real second source vertically first. Only then extract a minimal source-adapter protocol from Jobinja plus that source. Do not build a generic plugin platform in advance.

### 11.3 Phase 3 personal evidence

Before personal evidence, define explicit system/public/personal/secret data boundaries and tested backup/restore. Personal capability becomes its own evidence-backed domain, not a field on a job or hidden AI memory.

### 11.4 Phase 4 decisions

Gap/readiness/action logic should be explainable relational/domain logic over accepted market and personal evidence. Avoid opaque global fit scores.

### 11.5 Application workspace

Application tracking is user-owned state. Resume/interview generation consumes reviewed evidence packs and cannot invent user claims.

### 11.6 Retrieval/AI platform

Structured query and deterministic read models come before embeddings/RAG. Advanced provider routing, semantic retrieval and specialist AI workers are added only after measured need and evaluated benefit.

## 12. Architectural non-goals

Do not introduce without demonstrated need:

- microservices;
- message brokers;
- Redis;
- API gateway;
- Kubernetes;
- distributed tracing platform;
- React/Node rewrite;
- graph database;
- vector database;
- generic plugin runtime;
- autonomous agent swarm;
- separate browser analytical database;
- cloud-first personal-data architecture.

## 13. Current roadmap relationship

`docs/ROADMAP.md` defines how the current architecture should grow across Phase 1 completion, canonical market intelligence, multi-source acquisition, personal evidence, gap/action intelligence, application workflows, sustained operation and advanced evaluated AI.

`docs/IMPLEMENTATION_PLAN.md` remains the controlling exact delivery/acceptance sequence for the active implementation stage.
