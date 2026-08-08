# JobHunter Architecture

**Status:** Current architecture  
**Date:** 2026-08-08

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
- bounded human-facing Role Capability Blueprint;
- first deterministic Market read models;
- review-snapshot export;
- browser and CLI interaction surfaces.

```text
Browser UI                 CLI
normal human use      automation/debug
        \                /
         application services
                 ↓
              SQLite
        + raw evidence files
                 ↓
       optional review exports
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
8. Use SQLite as the canonical local structured state until measured limits justify replacement.
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
P1.6 strict English v4 factual extraction
        ↓
first Market aggregation

bounded reviewed reasoning branch:
accepted English P1.6
        ↓
Capability Intelligence v4
        ↓
Role Capability Blueprint v2
        ↓
Review Snapshot v1
```

The bounded reasoning branch is currently per-job/manual and is not part of automatic corpus-wide Market aggregation.

---

## 4. Current active contract identities

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:            english-projection-v2

English P1.6 prompt/runtime:   job-analysis-english-v4
Original P1.6 prompt/runtime:  job-analysis-original-v4
P1.6 persisted schema:         job-analysis-v2

Capability prompt/runtime:     job-capability-intelligence-v4
Capability persisted schema:   job-capability-intelligence-v2

Blueprint prompt/runtime:      role-capability-blueprint-v2
Blueprint persisted schema:    role-capability-blueprint-v1

Review Snapshot schema:        job-review-snapshot-v1
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
Blueprint artifact              human-facing interpretation above Capability
Blueprint attempt               operational Blueprint history
Market aggregate                deterministic aggregate of accepted current P1.6
User workflow state             local human triage/preference
Browser WebOperation            ephemeral UI execution state
Review Snapshot                 generated repository-review export only
```

Authority hierarchy:

```text
original employer/source evidence    authoritative
        ↓
deterministic parsed fields           source-derived
        ↓
English projection                    derived convenience
        ↓
P1.6 factual semantic extraction      strict model-derived facts
        ↓
Capability Intelligence               auditable derived reasoning
        ↓
Role Capability Blueprint             freer human-facing interpretation
```

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

Current browser domains include:

```text
Overview
Jobs
Job detail
Capability Intelligence
Role Capability Blueprint
Search plan / search effectiveness
Market
Operations
System
```

### CLI

CLI remains supported for automation/debugging/acceptance.

Important current commands include:

```bash
jobhunter run
jobhunter jobs health <id>
jobhunter jobs capability <id>
jobhunter jobs blueprint <id>
jobhunter jobs snapshot <id>
```

Both surfaces must use the same source, translation, analysis, reasoning and persistence services.

---

## 7. Browser security boundary

The app is loopback-first.

Protections include:

- CSRF validation on mutating forms;
- restrictive Content Security Policy;
- frame/content-type/referrer/cache protections;
- packaged local static assets;
- one mutable browser workflow at a time unless concurrency is proven safe;
- acquired job text rendered as data, never instruction/tool authority.

---

## 8. Configuration and independent model roles

Configuration is typed TOML plus selected `JOBHUNTER_*` environment overrides. Unknown configuration fails closed.

Current model roles:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Effective fallback:

```text
Analysis
→ dedicated analysis
→ general LM Studio model
→ explicit translation model

Capability
→ dedicated capability
→ effective analysis

Blueprint
→ dedicated Blueprint
→ effective Capability
```

This enables controlled same-job model comparison without changing source/translation/P1.6 evidence.

The best factual extractor is not assumed to be the best expert-reasoning model.

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

Current critical invariant:

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

---

## 11. Deterministic parser

`jobinja-detail-v2` extracts explicit source fields and relevant full source text without LLM inference.

Missing source values stay missing.

Parser metadata such as `language` and `parser_version` is not employer evidence.

Structural parser audit is not semantic-quality certification.

---

## 12. Translation boundary

Current trusted English path:

```text
current parsed source version
→ semantic source segments
→ native-English identity OR bounded local translation
→ structured response validation
→ deterministic integrity checks
→ english-projection-v2 artifact
```

Historical translation-v1 artifacts remain preserved but non-current.

LM Studio is the normal local translation provider. Optional external translation remains deliberate/policy-controlled.

---

## 13. P1.6 factual semantic boundary

P1.6 uses Instructor + Pydantic over LM Studio for structured factual extraction.

V4 adds:

- evidence-reference IDs;
- heading-aware long-description segmentation;
- clause-level evidence addressing;
- exact source resolution before persistence;
- rich-source empty-analysis guard;
- mixed-strength atomicity rules;
- preference-wording validation;
- obligation/depth separation;
- no arbitrary model read deadline after connection;
- bounded correction retry;
- independent final JobHunter validation.

P1.6 remains conservative factual substrate. It does not produce full technical curricula or personal recommendations.

See `docs/SEMANTIC_ANALYSIS.md`.

---

## 14. Capability Intelligence boundary

Capability Intelligence reasons above accepted English P1.6 while retaining evidence status and exact upstream dependency identity.

Artifact identity includes:

```text
source detail version
+ exact translation artifact
+ exact accepted English P1.6 artifact
+ capability model
+ capability prompt/schema
```

Generation uses JobHunter evidence references. Persisted evidence is exact resolved source text.

Supported status classes:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

Deterministic evidence resilience:

- valid grounding + bad extra reference → keep valid grounding;
- supported invalid-only grounding → fail closed;
- unknown invalid-only grounding → normalize to empty evidence.

See `docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`.

---

## 15. Role Capability Blueprint boundary

Blueprint is the intentionally freer human-facing expert layer.

Artifact identity includes exact source/translation/P1.6/Capability/model/prompt/schema dependencies.

It may use professional knowledge to suggest practical scope, examples, work products, failure modes and scenarios, but it must distinguish:

```text
highly_likely
plausible
speculative
```

and tool relationships:

```text
source_named
likely_example
possible_example
```

It must not transform a stack list into employer architecture truth.

See `docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md`.

---

## 16. Review Snapshot architecture

The live SQLite database remains local/ignored.

Review workflow:

```bash
jobhunter jobs snapshot <job-id>
```

Output:

```text
review-snapshots/jobs/<job-id>.json
```

A snapshot may contain public source fields plus current translation/P1.6/Capability/Blueprint outputs and dependency identities.

Excluded:

- SQLite/WAL/SHM;
- raw HTML contents;
- raw model responses;
- prompts/request bodies;
- secrets/configuration;
- private candidate/user state.

Snapshots are review artifacts, not runtime inputs.

### Current known defect

The integrated `jobhunter jobs snapshot` command does not yet pass the effective analysis/capability/blueprint model roles into `write_review_snapshot()`. Fix this before multi-model comparison so the snapshot selects and records the configured chain deterministically.

---

## 17. Market read model

Current Market reads accepted/current English P1.6 artifacts under the selected analysis contract.

It is not yet Phase-2 canonical market intelligence.

Keep visible/recoverable:

- analyzed sample size;
- source/filter scope;
- requirement-strength semantics;
- contract identity;
- sampling/concentration warning state.

Capability/Blueprint are not mixed into Market yet.

---

## 18. User workflow state

Local triage remains independent of employer/source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Acquisition priority must not be presented as personal fit/readiness.

Personal capability evidence remains a future separate reviewed domain.

---

## 19. Persistence model

SQLite remains the canonical structured application state.

Current durable concerns include separate tables/repositories for:

```text
source/search/discovery/version records
fetch observations/lifecycle
translation artifacts/attempts
P1.6 artifacts/attempts
Capability artifacts/attempts
Blueprint artifacts/attempts
user workflow state
```

Schema migration is application-owned, deterministic and regression-tested.

Known debt: P1.6 artifact uniqueness does not directly include `translation_artifact_id`; downstream Capability/Blueprint follow the exact translation ID stored on the accepted P1.6 artifact. Any future identity migration must be explicit and tested.

---

## 20. Runtime model-call policy

For long local P1.6/Capability/Blueprint reasoning:

```text
connection establishment bounded
read timeout after connection none
transport replay disabled
output tokens bounded
validation retry bounded separately
```

This is intentional. A local generation that has connected and is legitimately reasoning should not be terminated solely by an arbitrary 30/120-second read deadline.

---

## 21. Failure semantics

Keep distinct:

```text
no eligible work          != operation failure
zero source results       != provider/source failure
stale artifact            != failed artifact
transient source failure  != vacancy removed
translation failure       != source failure
P1.6 failure               != translation/source failure
Capability failure         != P1.6 failure
Blueprint failure          != Capability failure
partial workflow success  != complete success
```

Valid earlier durable work remains preserved when a later stage fails.

---

## 22. Testing and acceptance strategy

Normal deterministic tests do not contact Jobinja, LM Studio or Google Cloud.

Important real failures become fixtures.

Current semantic acceptance must distinguish:

- deterministic contract defect;
- source ambiguity/low evidence density;
- model-quality limitation;
- domain/technical correctness issue;
- bookkeeping/provenance issue.

The current detailed semantic-quality sequence is `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 23. Future architecture evolution

After Phase-1 closure:

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
- cloud-first personal-data architecture.

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
→ focused current P1.6/Capability/Blueprint acceptance sequence

docs/EXECUTION_TODO.md
→ current operational checklist

docs/WORKING_MEMORY.md
→ rolling non-authoritative handoff/current-session memory
```
