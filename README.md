# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It collects approved public job-market evidence, preserves the original source, structures Jobinja postings deterministically, tracks meaningful content versions and source checks, creates a separate hardened English projection, performs bounded evidence-backed semantic extraction, and now includes a bounded per-job **Capability Intelligence** layer for richer role reasoning before later canonical market and personal-career layers.

The browser application is the primary human interface. The CLI remains available for automation, debugging, tests and advanced workflows.

## Product direction

JobHunter is not intended to stop at scraping, text extraction or generic resume/job matching. The mature product loop is:

```text
market evidence
→ role / requirement intelligence
→ reviewed personal evidence
→ gaps / constraints
→ learn / practise / build / verify
→ application decision
→ outcome
→ updated evidence and decisions
```

Every consequential conclusion should remain traceable to market and/or personal evidence.

See [Roadmap](docs/ROADMAP.md) and [Execution TODO](docs/EXECUTION_TODO.md).

## Current implementation state

The repository contains an accepted acquisition/parser foundation plus newer Phase-1 and bounded capability-intelligence capabilities that are still moving through deterministic/live acceptance.

### Accepted foundation

```text
data-driven Persian + English search catalog
→ bounded/repeat-safe Jobinja discovery
→ immutable search-page evidence
→ missing + refresh-due detail selection
→ immutable detail evidence
→ deterministic Jobinja parser v2
→ semantic source versions
→ fetch-observation history
→ structural parser audit
→ local-first English projection architecture
```

Previously established live evidence includes repeat-safe discovery, a later 40/40-search browser run with 273 unique postings and zero search failures, successful bounded detail acquisition, structurally clean parsed samples, source-version/check separation, and functioning local browser workflows.

Historical translation-v1 artifacts remain preserved but are not treated as the trusted current English contract after a real field-association defect was discovered.

### Implemented / acceptance pending

The current codebase additionally contains:

```text
classified source failures + cautious lifecycle rules
→ user triage / deterministic acquisition priority
→ hardened english-projection-v2
→ translation-integrity validation
→ separate English / Original P1.6 semantic extraction
→ Instructor + Pydantic structured validation
→ exact selected-representation evidence validation
→ per-job analysis surfaces
→ bounded per-job Capability Intelligence reasoning
→ first Market aggregation from English P1.6 only
→ expanded bounded browser workflow actions
→ shared bounded Phase-1 run orchestration
→ concise per-job source-health summaries
```

P1.6 is intentionally a **strict factual extraction layer**. It records role purpose, responsibilities and requirements with required/preferred/contextual/inferred strength, concept type, confidence and exact evidence from the selected representation.

Capability Intelligence is intentionally separate. It reasons above the accepted English extraction to connect responsibilities, explicit requirements, experience signals, skill tags and supported company/product context into job-local capability profiles with explicit/implied/inferred/unknown distinctions. It is currently a manually reviewed per-job slice, not yet the corpus-wide Phase-2 canonical Market layer.

The shared Phase-1 runner composes acquisition, detail refresh/audit, current English-v2 repair/build, a bounded analysis-ready queue, English semantic extraction and the current Market summary while preserving successful durable work when a later stage has failures. Its CLI surface is `jobhunter run`.

Source-health summaries expose current lifecycle state, last check, last successful check, consecutive operational failures, latest failure and recent lifecycle-signal state through `jobhunter jobs health <job-id>`.

These newer capabilities are **implemented but not automatically accepted merely because code exists**. The exact acceptance state and execution order are controlled by [Implementation Plan](docs/IMPLEMENTATION_PLAN.md), [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md), and the bounded [Capability Intelligence Implementation Plan](docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md).

## Start the application

Requires Python 3.12 or newer.

```bash
python3 -m pip install -e ".[dev]"
```

Launch the browser UI:

```bash
jobhunter-app
```

It opens locally at:

```text
http://127.0.0.1:8765/
```

### Linux desktop launcher

```bash
jobhunter-app --install-desktop
```

The application remains a local Python/FastAPI/Jinja system; there is no Node/npm runtime requirement or CDN dependency.

## Browser experience

Current/implemented browser domains include:

```text
Overview
Jobs
Job detail
Per-job Capability Intelligence review
Search plan / search effectiveness
Market
Operations
System
```

The normal bounded Phase-1 workflow can include:

```text
run bounded sync
→ fetch priority missing details
→ repair/build current English v2
→ analyze a bounded English-ready set
→ inspect per-job strict analyses
→ inspect current Market aggregate
```

For a reviewed job with a current accepted English analysis, the job page also exposes **Capability Intelligence**. That action is deliberately per-job and opt-in while the reasoning quality is reviewed. It is not part of the automatic full-market workflow yet.

Browser and CLI paths operate on the same durable application data/services. Browser convenience state is not a second analytical truth store.

## Quick Add

Quick Add currently accepts only approved Jobinja inputs:

- one public Jobinja job URL;
- one public Jobinja `/jobs` search URL;
- one Persian/English keyword phrase interpreted as a bounded Jobinja search.

It is not an arbitrary-web ingestion escape hatch. Additional websites require explicit source adapters and source-policy review.

## Data-driven bilingual search catalog

Search vocabulary is **data, not Python logic**.

The packaged catalog lives at:

```text
src/jobhunter/data/search_catalog.toml
```

Profiles/packs can combine Persian and English terminology for AI/ML, LLM/RAG/agents, Python/data, defensive security, AI security, Linux/networking/platform/DevOps and related roles.

Search vocabulary is acquisition recall. It is not career taxonomy or proof of personal relevance.

See [Search Configuration](docs/SEARCH_CONFIGURATION.md).

## Source evidence and semantic versions

JobHunter distinguishes:

```text
JobPosting
  stable logical source identity

Raw evidence
  one exact acquired source response

JobPostingVersion
  meaningful deterministic employer-content version

JobDetailFetchObservation
  one operational source check
```

A volatile HTML change therefore does not manufacture a logical semantic job change.

Source failure/lifecycle logic must remain conservative. In particular:

```text
network / 5xx / rate-limit / challenge failure
!=
expired or removed vacancy
```

For concise operational inspection, `jobhunter jobs health <job-id>` summarizes the latest source/lifecycle state. `jobhunter jobs checks <job-id>` remains the more detailed historical timeline.

## Deterministic Jobinja parsing

Parser v2 extracts explicit source fields such as title, company, category, location, employment type, experience, salary, Jobinja tags, gender, military-service requirement, education, posting/expiration dates, complete job description, company description and source-language classification.

Missing source values remain missing. The parser does not ask an LLM to infer employer intent.

A structural parser audit checks parser structure/contamination only; it does not certify translation or semantic interpretation quality.

## English projection v2

JobHunter keeps source and English representation separate:

```text
original Persian / English / mixed employer text
        ↓ authoritative
English projection
        ↓ derived convenience
```

The current hardened design uses `english-projection-v2` with local LM Studio as the normal translator.

Native-English strings pass through without model translation. Persian-containing semantic units are translated through bounded structured requests, then deterministic source/English integrity checks run before a current artifact can be persisted.

Historical v1 artifacts remain historical; they are not silently relabeled or overwritten.

Google Cloud Translation remains an optional external provider, not a normal requirement.

See [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md).

## Strict evidence-backed semantic extraction

P1.6 is a separate derived layer from source parsing and translation, and it now has **two independent analysis products**:

```text
English projection v2
→ Analyze English
→ English statements + English evidence
→ job-analysis-english-v2

original employer/source fields
→ Analyze Original
→ original-language statements + original-language evidence
→ job-analysis-original-v2
```

The two modes do not mix source representations or satisfy/reuse each other.

One durable analysis identity includes:

```text
source semantic version
+ exact model
+ prompt version
+ analysis schema version
```

Structured extraction uses local LM Studio through Instructor/Pydantic. Runtime validation keeps evidence grounded in the selected representation, rejects unsupported evidence, preserves required/preferred/contextual/inferred semantics and performs only mechanically safe canonicalization such as exact duplicate collapse or exact field-value/source-span recovery.

This layer is intentionally conservative. Its job is to establish trustworthy structured facts, not to generate a complete technical curriculum or personal career recommendation.

See [Semantic Analysis](docs/SEMANTIC_ANALYSIS.md).

## Per-job Capability Intelligence

The bounded capability layer exists because **strict extraction and useful career intelligence are different uncertainty contracts**.

```text
current source
→ exact English projection used by P1.6
→ accepted English P1.6 factual extraction
→ Capability Intelligence
```

The capability artifact can synthesize new analytical statements while keeping evidence anchors exact. Fine-grained expectations use:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

A capability profile can reason about:

```text
role interpretation
work activities
employer-stated depth
technical sub-capabilities
underlying knowledge / prerequisites
operational practices
independence / ownership
operational context
unknown / unsupported scope
```

The model is explicitly told not to dump a generic technology curriculum from a keyword. Responsibilities and deliverables carry more interpretive weight than isolated skill tags. Company context may support reasoning only when actual source text makes it relevant.

The current artifact identity includes:

```text
current source version
+ exact English projection artifact
+ exact accepted English P1.6 artifact
+ capability model
+ capability prompt/schema versions
```

A changed factual dependency therefore prevents silent reuse of stale reasoning.

Current review surfaces:

```bash
jobhunter jobs capability <job-id>
```

and, after English analysis exists, the **Capability Intelligence** link on the browser job page.

This slice does **not** yet populate the canonical Market taxonomy, score the user, generate readiness/gaps, or run automatically across the corpus. Those remain gated until reviewed real-job quality supports promotion.

See [Capability Intelligence Implementation Plan](docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md).

## First Market layer

The current Market screen aggregates only current **English P1.6** analysis artifacts matching the selected/current analysis contract.

It can show bounded corpus facts such as analyzed sample size, responsibility counts and concept demand with required/preferred/contextual/inferred distributions.

Capability Intelligence is not yet mixed into these aggregates.

This is not yet a reviewed Phase-2 canonical market taxonomy. Alias consolidation, role archetypes, duplicate/repost adjustment, mature sampling controls and trend claims belong to later accepted layers.

Small/concentrated samples must be presented with explicit scope/warnings rather than as complete-market truth.

## CLI remains supported

The bounded Phase-1 orchestration is available as an **implementation-pending-acceptance** command:

```bash
jobhunter run
jobhunter run --help
```

It performs, within configured/explicit limits:

```text
Jobinja discovery
→ missing/refresh-due detail acquisition
→ parser audit
→ current English-v2 repair/build
→ bounded analysis-ready selection
→ strict English P1.6 analysis
→ current Market summary
```

A partial later-stage failure does not roll back valid earlier durable work; the command exits non-zero and reports the attention-required stage rather than presenting a false simple success.

Other CLI examples include:

```bash
jobhunter jobinja plan
jobhunter jobinja sync
jobhunter jobinja fetch --missing --limit 10
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs health <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter jobs capability <job-id>
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

Existing commands remain supported through the same console entrypoint. Some older individual CLI source factories still require final convergence with the newer shared dependency graph; the complete `jobhunter run` path already uses configured Jobinja retry bounds plus lifecycle persistence.

## Browser security boundary

The app defaults to loopback and refuses broader network binding unless exposure is explicitly requested.

Mutating browser forms use CSRF protection. Responses use restrictive content-security/frame/referrer/content-type/cache policies. Static assets are packaged locally.

Acquired job text is untrusted data. It never receives system/tool instruction authority.

## What JobHunter does **not** claim yet

Until their respective gates pass, JobHunter does not claim:

- complete lifecycle/repost/duplicate resolution;
- production-quality translation-v2 across every future language/source case;
- production-quality semantic extraction across all role types;
- production-quality capability/depth reasoning across all role types;
- accepted final Phase-1 end-to-end operation merely because `jobhunter run` is implemented;
- reviewed canonical market taxonomy;
- corpus-wide aggregation of inferred capability profiles;
- complete-market conclusions from the bounded/source-biased corpus;
- reviewed personal capability state;
- personal readiness/gap/career recommendations;
- evidence-backed learning/project prioritization;
- evidence-backed resume/interview assistance;
- autonomous job applications;
- mature longitudinal market trends;
- arbitrary-web ingestion;
- generic source-plugin support;
- evaluated RAG/career assistant authority.

## Near-term execution

The near-term acceptance work remains deliberately bounded:

1. keep deterministic Ruff/tests/warnings gates green after each tranche;
2. finish remaining Phase-1 migration/source/lifecycle/live orchestration acceptance;
3. review representative strict English P1.6 outputs as factual extraction artifacts;
4. review the bounded per-job Capability Intelligence slice on materially different real jobs;
5. turn repeatable extraction/reasoning failures into fixtures or documented model limitations;
6. compare a stronger dedicated capability model only if the current model's reasoning remains inadequate under the correct contract;
7. keep Capability Intelligence out of automatic Market aggregation until reviewed quality is sufficient;
8. close Phase 1;
9. then promote the reviewed capability contract into Phase-2 canonical mapping/Market-v2 work and add a carefully selected second source;
10. only later connect canonical job requirements to reviewed personal evidence for readiness/gap/learning decisions.

The bounded capability slice is being reviewed now because it is necessary to determine whether our current factual extraction provides a useful substrate. This does **not** waive the gate on corpus-wide Phase-2 promotion.

See [Execution TODO](docs/EXECUTION_TODO.md) for the complete checklist.

## Development validation

```bash
ruff check .
pytest
pytest -W error
```

Normal deterministic tests do not contact Jobinja, Google Cloud or LM Studio. Network/model behavior should be represented with controlled transports/fixtures in normal tests; live validation is a separate bounded acceptance step.

## Documentation

- [Product Specification](docs/PRODUCT_SPECIFICATION.md)
- [Roadmap](docs/ROADMAP.md)
- [Execution TODO](docs/EXECUTION_TODO.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Local Web Application](docs/LOCAL_WEB_APP.md)
- [Search Configuration](docs/SEARCH_CONFIGURATION.md)
- [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md)
- [Semantic Analysis](docs/SEMANTIC_ANALYSIS.md)
- [Capability Intelligence Implementation Plan](docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md)
- [Semantic Analysis Engineering Lessons](docs/SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md)
- [Acquisition Operations](docs/ACQUISITION_OPERATIONS.md)
- [Domain and Analysis Model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source Acquisition Policy](docs/SOURCE_POLICY.md)
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [Proposal Library](docs/proposals/README.md)
- [Repository Instructions](AGENTS.md)
