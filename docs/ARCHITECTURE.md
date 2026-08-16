# JobHunter Architecture

**Status:** Current architecture  
**Date:** 2026-08-16

## 1. Architectural direction

JobHunter is a **local Python modular monolith**.

One application owns:

- typed configuration;
- approved-source acquisition;
- immutable evidence preservation;
- SQLite persistence/migrations;
- deterministic Jobinja parsing;
- source version/check/lifecycle state;
- hardened English projection;
- strict factual semantic extraction;
- bounded per-job Capability Intelligence;
- experimental Role Capability Blueprint;
- first deterministic Market read models;
- complete repository-safe public-corpus projection;
- selected review-snapshot export;
- browser and CLI interaction surfaces.

```text
Browser UI                 CLI
normal human use      automation/debug
        \                /
         application services
                 ↓
              SQLite
        + raw evidence files
       runtime/history authority
                 ↓
       deterministic projections
          /               \
     corpus/         review-snapshots/
 complete public      selected review
 current dataset         evidence
```

The browser is not a separate frontend product with a second analytical data model. It is a thin server-rendered interface over the same services and durable records used by the CLI.

The deployment target remains one local process/application. Future domains may add focused modules/repositories without becoming microservices.

---

## 2. Permanent principles

1. Preserve source evidence before parsing, translation, or interpretation.
2. Keep source acquisition useful when LM Studio is unavailable.
3. Keep source truth, English projection, factual extraction, reasoning, aggregation, and user state distinct.
4. Deterministic parsing/identity/counts/lifecycle logic remain deterministic.
5. Treat acquired content as untrusted data, never instructions.
6. Keep source-specific behavior explicit and bounded.
7. Keep browser and CLI on the same services/data.
8. Use SQLite as the canonical local structured/runtime state until measured limits justify replacement.
9. Keep raw evidence independently inspectable.
10. Separate semantic source versions from volatile HTTP/fetch observations.
11. Separate operational attempts from successful semantic/derived artifacts.
12. Preserve native-versus-translated provenance.
13. Preserve exact model/prompt/schema/dependency identity for durable derived artifacts.
14. Prefer missing/unknown/review-required over fabricated certainty.
15. Bound requests/pages/detail batches/model calls/output tokens/retries where applicable.
16. Do not impose arbitrary local-generation read deadlines merely to force responsiveness when a valid long model call is progressing.
17. Deterministic bookkeeping repairs belong in code, not repeated LLM calls.
18. Models may reason; they do not manufacture source truth.
19. Add complexity only for observed product need.
20. Keep local-first privacy/network boundaries explicit.
21. Do not build generic plugin/vector/agent infrastructure before demonstrated need.
22. Historical artifacts remain historical when contracts change.
23. Coverage and semantic quality are different metrics.
24. A technology list is not an architecture specification.
25. Keep runtime persistence separate from repository projections.
26. A public-data projection never implicitly authorizes future private/personal state for publication.

---

## 3. Current end-to-end flow

```text
TOML configuration
        ↓
data-driven bilingual Jobinja search catalog
        ↓
bounded deterministic search plan
        ↓
sequential Jobinja search acquisition
        ↓
immutable search evidence
        ↓
stable JobPosting identity + discovery provenance
        ↓
missing / refresh-due detail selection
        ↓
classified bounded detail acquisition
        ↓
immutable valid detail evidence
        ↓
jobinja-detail-v2 parser
        ↓
semantic source version
        ↓
fetch observation + lifecycle evidence
        ↓
current English projection v2
        ↓
P1.6 strict factual extraction
        ↓
Capability Intelligence v9
        ↓
first Market aggregation from accepted English P1.6

repository projections:
current durable public state
        ↓
jobhunter-public-corpus-v1

selected acceptance evidence
        ↓
job-review-snapshot-v1

experimental branch only:
historical Blueprint-compatible accepted chain
        ↓
Role Capability Blueprint v6
```

Capability v9 is an accepted/current Phase-1 layer. Blueprint remains experimental/non-authoritative and is not on the Phase-1 critical path.

---

## 4. Current active contract identities

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6 prompt/runtime:   job-analysis-english-v20
English P1.6 schema:           job-analysis-v5
Original P1.6 prompt/runtime:  job-analysis-original-v9
Original P1.6 schema:          job-analysis-v4

Capability prompt/runtime:     job-capability-intelligence-v9
Capability persisted schema:   job-capability-intelligence-v5

Blueprint experimental:        role-capability-blueprint-v6
Blueprint schema:              role-capability-blueprint-v5

Review Snapshot schema:        job-review-snapshot-v1
Public Corpus schema:          jobhunter-public-corpus-v1
```

Current accepted opposite-end anchors:

```text
tG9K P1.6 artifact 36 → Capability artifact 11
t4jp P1.6 artifact 37 → Capability artifact 12
```

Prompt/runtime version changes intentionally produce distinct current/historical artifacts even when a persisted schema remains unchanged.

---

## 5. Authority boundaries

Never conflate:

```text
Raw evidence                    exact acquired source bytes/metadata
JobPosting                      stable logical source identity
JobPostingVersion               meaningful employer-content version
Fetch/check observation         one operational source check
Lifecycle state/event           cautious derived source availability
Translation artifact            derived English representation
Translation attempt             operational translation history
P1.6 analysis artifact          strict model-derived factual interpretation
P1.6 analysis attempt           operational analysis history
Capability artifact             evidence-qualified reasoning above P1.6
Capability attempt              operational Capability history
Blueprint artifact              experimental human-facing interpretation
Blueprint attempt               operational Blueprint history
Market aggregate                deterministic aggregate of accepted current P1.6
User workflow state             local human triage/preference
Browser WebOperation            ephemeral UI execution state
Public Corpus                   deterministic repository-safe public projection
Review Snapshot                 selected repository-review export
```

Authority hierarchy:

```text
original employer/source evidence     authoritative
        ↓
deterministic parsed fields            source-derived
        ↓
English projection                     derived convenience
        ↓
P1.6 factual semantic extraction       strict factual substrate
        ↓
Capability v9 deterministic source truth + bounded grouping/reasoning
```

Blueprint sits outside this accepted authority chain during Phase 1.

The Market layer currently aggregates accepted English P1.6, not Capability/Blueprint.

A downstream layer never upgrades an upstream error into source truth.

---

## 6. Interaction surfaces

### Browser

Current stack:

```text
FastAPI
Uvicorn
Jinja2
packaged CSS
small vanilla JavaScript
```

No Node/npm build and no runtime CDN dependency.

Current browser domains include Overview, Jobs, Job detail, Capability Intelligence, experimental Blueprint review, Search plan/effectiveness, Market, Operations, and System.

### CLI

CLI remains supported for automation/debugging/acceptance.

Important current commands include:

```bash
jobhunter run
jobhunter jobs health <id>
jobhunter jobs analyze <id>
jobhunter jobs capability <id>
jobhunter jobs snapshot <id>
jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

Both surfaces must use the same source, translation, analysis, reasoning, and persistence services.

---

## 7. Browser security and operation boundary

The app is loopback-first.

Protections include:

- CSRF validation on mutating forms;
- restrictive Content Security Policy;
- frame/content-type/referrer/cache protections;
- packaged local static assets;
- one mutable browser workflow at a time unless concurrency is proven safe;
- acquired job text rendered as data, never instruction/tool authority.

All background browser operations share `WebOperationManager`. The runtime installs a post-success public-corpus projection hook on this manager. Durable service work completes first; the projection runs afterward.

If projection fails, durable SQLite state is preserved and the web operation visibly reports the projection failure.

---

## 8. Configuration and independent model roles

Configuration is typed TOML plus selected `JOBHUNTER_*` environment overrides. Unknown configuration fails closed.

Current model roles:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Effective role selection is explicit in the corresponding service builders. The best factual extractor is not assumed to be the best reasoning model.

Use controlled same-job comparison when model adequacy is genuinely the variable. Do not change evidence, contract, and model simultaneously.

---

## 9. Source registry/acquisition boundary

The Jobinja implementation owns:

- approved URL/host/path validation;
- canonical source identity;
- bounded sequential requests;
- redirect/content-type/size validation;
- search/detail acquisition;
- classified failures/retryability;
- source-specific deterministic parsing.

Critical invariant:

```text
network / 429 / 5xx / challenge / auth / access failure
!=
expired or removed job
```

Provider/source failure is not a valid empty result.

---

## 10. Evidence and source-version model

Exact acquired bytes + metadata are preserved independently from normalized records.

Source versioning distinguishes:

```text
logical job identity
raw observation
meaningful semantic content version
operational source check
lifecycle interpretation
```

Volatile HTML changes must not manufacture logical semantic changes.

`jobinja-detail-v2` extracts explicit public fields including title, company, category, location, employment type, minimum experience, salary, description, skills, gender, military service, education, company description, source dates, language, and parser version where available.

Missing source values stay missing. Parser metadata is not employer evidence. Structural parser audit is not semantic-quality certification.

---

## 11. Translation boundary

Current trusted English path:

```text
current parsed source version
→ semantic source segments
→ native-English identity OR bounded local translation
→ structured response validation
→ deterministic integrity checks
→ english-projection-v2 artifact
```

Historical translation artifacts remain preserved but non-current when contracts/source dependencies change.

LM Studio is the normal local translation provider. Optional external translation remains deliberate/policy-controlled.

---

## 12. P1.6 factual semantic boundary

P1.6 uses Instructor + Pydantic over LM Studio for structured factual extraction plus independent deterministic reconciliation/validation.

Current English v20/v5 behavior preserves:

- exact source evidence/provenance;
- complete meaningful requirement accounting on rich sources;
- structured source skills;
- required/preferred/contextual strength;
- concept-specific explicit depth;
- education and experience constraints;
- qualification-vs-duty separation;
- conservative handling of sparse/ambiguous sources.

P1.6 remains factual substrate. It does not produce full technical curricula or personal recommendations.

See `docs/SEMANTIC_ANALYSIS.md` and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 13. Capability Intelligence v9 boundary

Capability v9 reasons above accepted English P1.6 while making source survival deterministic.

Architecture:

```text
accepted P1.6 source truth
→ compact semantic capability-group plan
→ bounded exact source-fact assignment partitions
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

Artifact identity includes source detail version, exact translation artifact, exact accepted English P1.6 artifact, model, prompt, and schema.

Complete source coverage/provenance is mandatory. Source strength/depth/work are deterministic. Role-level education/duration-only experience remain separate. Unsupported ownership/lifecycle/autonomy/architecture and optionality inflation are blocked/filtered. Zero optional enrichment is valid.

Historical v7/v8 modules/artifacts remain reproducible but non-current.

---

## 14. Role Capability Blueprint boundary

Blueprint v6 is implemented for research/inspection but remains **deferred and non-authoritative** in Phase 1.

It is pinned to historical Capability v7 dependency semantics so Capability v9 promotion does not silently rebase it.

Historical mechanically valid Blueprint evidence still failed complete semantic acceptance because professional interpretation could introduce unsupported assumptions about architecture, topology, automation, platforms, or ownership.

Do not route Blueprint into Market, personal readiness, recommendations, or other authoritative Phase-1 decisions.

---

## 15. Public Corpus architecture

The live SQLite database remains local and ignored. The complete repository-safe current public dataset lives in:

```text
corpus/
```

Contract:

```text
jobhunter-public-corpus-v1
```

Layout:

```text
corpus/manifest.json
corpus/jobs/<job-id>/source.json
corpus/jobs/<job-id>/english-projection.json
corpus/jobs/<job-id>/p16-english.json
corpus/jobs/<job-id>/p16-original.json
corpus/jobs/<job-id>/capability.json
```

Properties:

- deterministic sorted UTF-8 JSON;
- atomic file replacement;
- every known Jobinja identity represented in the manifest;
- original parsed Persian/English public vacancy content preserved;
- current derived stage files retain exact artifact/dependency/model/prompt/schema identities;
- stale downstream files disappear when source dependency changes until rebuilt;
- DB↔corpus verification is deterministic;
- no network/model calls during export/verification.

Excluded from the public corpus:

- SQLite/WAL/SHM;
- raw HTML evidence;
- machine-local evidence paths;
- raw model request/response protocol;
- prompts/secrets/logs/local config;
- future personal/private evidence, applications, notes, profiles, or outcomes.

Normal mutating CLI workflows and completed browser background operations project current durable state after SQLite work. Projection failure never rolls back SQLite but is surfaced.

Git commit/push is intentionally manual; runtime correctness never depends on GitHub/network availability.

See `corpus/README.md` and `docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md`.

---

## 16. Review Snapshot architecture

Review workflow:

```bash
jobhunter jobs snapshot <job-id>
```

Output:

```text
review-snapshots/jobs/<job-id>.json
```

Review Snapshots are **selected** semantic-review/acceptance artifacts. They are not the complete public corpus and are not runtime inputs.

The integrated command records configured model roles and exact current-chain dependencies while excluding raw model protocol, SQLite, secrets, logs, raw HTML, and future private state.

Current-chain flags prove dependency currentness, not semantic acceptance.

---

## 17. Market read model

Current Market reads accepted/current English P1.6 artifacts under the selected analysis contract.

It is not yet Phase-2 canonical market intelligence.

Keep visible/recoverable analyzed sample size, source/filter scope, requirement-strength semantics, contract identity, and sampling/concentration warning state.

Capability/Blueprint are not mixed into Market yet.

---

## 18. User workflow and future private state

Local triage remains independent of employer/source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Acquisition priority must not be presented as personal fit/readiness.

Personal capability evidence remains a future separate reviewed domain. Future private/personal state may coexist in SQLite but must never enter `corpus/` without an explicit public/privacy boundary change—which is not currently authorized.

---

## 19. Persistence model

SQLite remains the canonical structured application/runtime/history state.

Current durable concerns include separate tables/repositories for source/search/discovery/version records, fetch observations/lifecycle, translation artifacts/attempts, P1.6 artifacts/attempts, Capability artifacts/attempts, Blueprint artifacts/attempts, and user workflow state.

Schema migration is application-owned, deterministic, and regression-tested.

Repository projections (`corpus/`, `review-snapshots/`) do not replace SQLite tables or become runtime write authorities.

---

## 20. Runtime model-call policy

For long local semantic reasoning:

```text
connection establishment bounded
read timeout after connection none
transport replay disabled
output tokens bounded
validation retry bounded separately
```

A local generation that has connected and is legitimately reasoning should not be terminated solely by an arbitrary short read deadline.

---

## 21. Failure semantics

Keep distinct:

```text
no eligible work           != operation failure
zero source results        != provider/source failure
stale artifact             != failed artifact
transient source failure   != vacancy removed
translation failure        != source failure
P1.6 failure               != translation/source failure
Capability failure         != P1.6 failure
Blueprint failure          != Capability failure
corpus projection failure  != rollback of durable SQLite success
partial workflow success   != complete success
```

Valid earlier durable work remains preserved when a later stage fails.

---

## 22. Testing and acceptance strategy

Normal deterministic tests do not contact Jobinja, LM Studio, or Google Cloud.

Important real failures become fixtures.

Current acceptance distinguishes deterministic contract defect, source ambiguity/low evidence density, model-quality limitation, domain/technical correctness issue, bookkeeping/provenance issue, and repository-projection drift.

The focused acceptance sequence is `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 23. Current gate and future evolution

Current mini-gate:

```text
public corpus implementation complete
→ local full SQLite backfill
→ DB↔corpus verify
→ intentional Git publish
→ remote corpus proof
→ heterogeneous semantic review
```

Heterogeneous review families:

```text
Python/software
network/security
operations/platform/DevOps
```

After remaining Phase-1 gates close:

1. reviewed canonical concept registry;
2. alias/mapping provenance;
3. responsibility/deliverable families;
4. corpus-scale capability requirement profiles;
5. role archetypes / Market v2;
6. reviewed personal evidence;
7. explainable gap/action/readiness;
8. later application workspace;
9. retrieval/advanced AI only after measured need.

Implement one real second source before extracting a generic source-adapter abstraction.

---

## 24. Architectural non-goals

Do not introduce without demonstrated need:

- microservices;
- Redis/message broker/API gateway;
- Kubernetes;
- React/Node rewrite;
- graph/vector database;
- generic plugin runtime;
- autonomous agent swarm;
- multi-model voting system;
- separate browser analytical database;
- cloud-first personal-data architecture;
- live SQLite committed to Git as the public dataset.

---

## 25. Current plan relationship

```text
docs/ROADMAP.md
→ strategic direction

docs/IMPLEMENTATION_PLAN.md
→ controlling product-level order

docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md
→ detailed active Phase-1 order

docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
→ focused current semantic/public-corpus acceptance sequence

docs/EXECUTION_TODO.md
→ current operational checklist

docs/WORKING_MEMORY.md
→ rolling non-authoritative handoff/current-session memory
```
