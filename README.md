# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It collects approved public job-market evidence, preserves the original source, structures Jobinja postings deterministically, tracks meaningful content versions and source checks, creates a separate English projection, performs bounded evidence-backed local semantic analysis, and prepares trustworthy data for canonical market intelligence and later personal career decisions.

The browser application is the primary human interface. The CLI remains available for automation, debugging, tests and advanced workflows.

## Product direction

JobHunter is not intended to stop at scraping or generic resume/job matching. The mature product loop is:

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

The repository currently contains an accepted acquisition/parser foundation plus several newer Phase-1 capabilities that are implemented but still moving through deterministic/live acceptance.

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
→ evidence-backed P1.6 semantic analysis
→ exact original-source evidence validation
→ per-job analysis surfaces
→ first Market aggregation
→ expanded bounded browser workflow actions
```

P1.6 currently supports role purpose, responsibilities, requirements, required/preferred/contextual/inferred strength, concept type, confidence, exact original-source evidence and rationale for inferred concepts.

The exact acceptance state and execution order are controlled by [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) and [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

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
Search plan / search effectiveness
Market
Operations
System
```

The normal bounded workflow can include:

```text
run bounded sync
→ fetch priority missing details
→ repair/build current English v2
→ analyze a bounded ready set
→ inspect per-job analysis
→ inspect current Market aggregate
```

Browser and CLI paths use the same application services/database. Browser convenience state is not a second analytical truth store.

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

## Evidence-backed semantic analysis

P1.6 is a separate derived layer from source parsing and translation.

One durable analysis identity includes:

```text
source semantic version
+ exact model
+ prompt version
+ analysis schema version
```

The model receives original employer fields as authoritative evidence plus the current English projection as a comprehension aid.

Material claims must cite exact original-source excerpts. The application validates those excerpts locally. If a claim cites unsupported text, no accepted analysis artifact is created.

Current analysis distinguishes:

```text
required
preferred
contextual
inferred
```

and concept types such as tool, skill, knowledge, practice, domain, experience and education.

See [Semantic Analysis](docs/SEMANTIC_ANALYSIS.md).

## First Market layer

The current Market screen aggregates only current analysis artifacts matching the selected/current analysis contract.

It can show bounded corpus facts such as analyzed sample size, responsibility counts and concept demand with required/preferred/contextual/inferred distributions.

This is not yet a reviewed Phase-2 canonical market taxonomy. Alias consolidation, role archetypes, duplicate/repost adjustment, mature sampling controls and trend claims belong to later accepted layers.

Small/concentrated samples must be presented with explicit scope/warnings rather than as complete-market truth.

## CLI remains supported

Examples include:

```bash
jobhunter jobinja plan
jobhunter jobinja sync
jobhunter jobinja fetch --missing --limit 10
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

Additional analysis/current-workflow commands may evolve with the active Phase-1 implementation. The browser and CLI must continue to share the same underlying services and records.

## Browser security boundary

The app defaults to loopback and refuses broader network binding unless exposure is explicitly requested.

Mutating browser forms use CSRF protection. Responses use restrictive content-security/frame/referrer/content-type/cache policies. Static assets are packaged locally.

Acquired job text is untrusted data. It never receives system/tool instruction authority.

## What JobHunter does **not** claim yet

Until their respective gates pass, JobHunter does not claim:

- complete lifecycle/repost/duplicate resolution;
- production-quality translation-v2 across every future language/source case;
- production-quality semantic extraction across all role types;
- reviewed canonical market taxonomy;
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

The next building work is intentionally narrow:

1. deterministic Ruff/tests/warnings baseline;
2. migration and real-workspace safety;
3. translation-v2 repair/inspection;
4. one reviewed real P1.6 analysis;
5. representative small P1.6 review sample;
6. regression/chaos cases for source/model failure boundaries;
7. Market sampling/corpus-health truthfulness;
8. explicit partial-success operation results;
9. remaining P1.3/P1.5 acceptance;
10. final P1.7 run/report/browser equivalent;
11. Phase-1 closure;
12. only then Phase-2 canonical market intelligence and a carefully selected second source.

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
- [Acquisition Operations](docs/ACQUISITION_OPERATIONS.md)
- [Domain and Analysis Model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source Acquisition Policy](docs/SOURCE_POLICY.md)
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [Proposal Library](docs/proposals/README.md)
- [Repository Instructions](AGENTS.md)
