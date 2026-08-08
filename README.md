# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It collects approved public job-market evidence, preserves authoritative source data, structures Jobinja postings deterministically, tracks meaningful source versions/checks, creates a separate hardened English projection, performs strict evidence-backed factual extraction, and provides bounded per-job reasoning layers for capability interpretation and professional role understanding.

The browser application is the primary human interface. The CLI remains supported for automation, debugging, tests, and advanced workflows.

---

## Product direction

JobHunter is not intended to stop at scraping, keyword matching, or resume generation.

The mature loop is:

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Every consequential conclusion should remain traceable to source and/or reviewed personal evidence.

Strategic sequencing: [Roadmap](docs/ROADMAP.md)  
Current working checklist: [Execution TODO](docs/EXECUTION_TODO.md)  
Current semantic-quality plan: [Semantic Quality Acceptance Plan](docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md)  
Rolling handoff: `docs/WORKING_MEMORY.md` once present/current.

---

## Current implementation state

JobHunter has a mature Phase-1 foundation plus a bounded semantic-reasoning slice that is currently under representative quality acceptance.

### Accepted/strong foundation

```text
data-driven Persian + English Jobinja search catalog
→ bounded repeat-safe discovery
→ immutable search/detail evidence
→ stable logical job identities
→ semantic source versions
→ fetch/check observations
→ deterministic jobinja-detail-v2 parsing
→ local browser application + CLI
→ hardened english-projection-v2 architecture
```

Historical translation-v1 artifacts remain preserved but are not treated as the current trusted English contract after a real field-association defect was found.

### Current semantic stack

```text
Jobinja source
        ↓
english-projection-v2
        ↓
P1.6 strict factual extraction
  English:  job-analysis-english-v4
  Original: job-analysis-original-v4
  schema:   job-analysis-v2
        ↓
Capability Intelligence
  prompt:   job-capability-intelligence-v4
  schema:   job-capability-intelligence-v2
        ↓
Role Capability Blueprint
  prompt:   role-capability-blueprint-v2
  schema:   role-capability-blueprint-v1
        ↓
Review Snapshot
  schema:   job-review-snapshot-v1
```

These newer layers are implemented but **semantic-quality acceptance is still active**. Code existing does not automatically mean the layer is accepted across all role types.

---

## What each semantic layer does

### P1.6 — strict factual extraction

P1.6 establishes a conservative factual substrate:

- role purpose;
- responsibilities;
- requirements;
- requirement obligation/strength;
- concept type;
- confidence;
- exact evidence from the selected representation;
- rationale where inference is allowed by contract.

Production v4 uses deterministic evidence references, heading-aware long-description segments, clause references for mixed-strength lines, rich-source non-empty guards, and exact source-text resolution before persistence.

P1.6 is intentionally **not** the human-facing expert explanation layer.

See [Semantic Analysis](docs/SEMANTIC_ANALYSIS.md).

### Capability Intelligence — auditable machine reasoning

Capability Intelligence reasons above accepted English P1.6:

- role interpretation;
- work activities;
- depth signals;
- sub-capabilities;
- underlying knowledge/prerequisites;
- operational practices;
- independence/ownership;
- operational context;
- explicit unknown/unsupported scope.

Expectation provenance is kept distinct:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

Model-generated evidence references are resolved back to exact source text before persistence.

See [Capability Intelligence Plan](docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md).

### Role Capability Blueprint — human-facing professional interpretation

Blueprint is intentionally freer than the audit/reasoning layers. It explains what the position probably requires in practice from the perspective of an experienced practitioner in the relevant domain.

It may provide:

- likely practical depth;
- likely subskills;
- source-named / likely / possible tool examples;
- work products;
- operational concerns/failure modes;
- plausible end-to-end scenarios;
- hidden prerequisites;
- probable non-requirements;
- important unknowns.

It must preserve uncertainty and must not present one plausible technology architecture as employer fact.

See [Role Capability Blueprint Plan](docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md).

---

## Current quality-acceptance evidence

Two live examples currently anchor semantic acceptance:

```text
t4jp  sparse/ambiguous AI-content posting
tG9K  rich semiconductor/industrial-ML posting
```

`t4jp` tests whether intelligence stays conservative when source evidence is weak.

`tG9K` tests long/dense technical extraction and deeper reasoning. Its current complete review chain is committed at:

```text
review-snapshots/jobs/tG9K.json
```

The `tG9K` chain now runs end to end, but its first reviewed snapshot still identified remaining quality work around factual requirement recall, stack optionality/depth, Capability calibration, Blueprint architecture over-inference, and expert-model adequacy.

The exact next sequence is [Semantic Quality Acceptance Plan](docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md).

---

## Review Snapshots — no more manual giant copy/paste

The live SQLite database remains local and ignored.

For selected review jobs:

```bash
jobhunter jobs snapshot tG9K
```

Default output:

```text
review-snapshots/jobs/tG9K.json
```

Then intentionally review and publish:

```bash
git diff -- review-snapshots/jobs/tG9K.json
git add review-snapshots/jobs/tG9K.json
git commit -m "review: update tG9K intelligence snapshot"
git push origin main
```

A reviewer/AI can then inspect the complete selected source→English→P1.6→Capability→Blueprint chain directly from GitHub.

Snapshots exclude raw model responses/prompts, SQLite/WAL/SHM, raw HTML contents, secrets, logs, and future private user state.

See [Review Snapshot README](review-snapshots/README.md).

### Known snapshot issue before model comparison

The standalone snapshot exporter uses the configured effective model roles correctly. The normal integrated `jobhunter jobs snapshot` command currently does not pass those role-model arguments into the exporter, so the first `tG9K` snapshot reports null `configured_models` even though each artifact records its actual model.

This is the **first code task** in the current TODO because it must be fixed before controlled multi-model comparisons.

---

## Independent local model roles

JobHunter can configure strict extraction, Capability, and Blueprint models independently:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

The best factual extractor is not assumed to be the best professional reasoning model.

Current plan: fix snapshot model routing, harden deterministic factual/certainty contracts, then compare a stronger dedicated local reasoning model only if current Gemma reasoning remains inadequate.

---

## Start the application

Requires Python 3.12+.

```bash
python3 -m pip install -e ".[dev]"
```

Launch:

```bash
jobhunter-app
```

Default local URL:

```text
http://127.0.0.1:8765/
```

Linux desktop launcher:

```bash
jobhunter-app --install-desktop
```

The browser remains a FastAPI/Uvicorn/Jinja/local-static application. No Node/npm runtime or CDN is required.

---

## Browser experience

Current browser domains include:

```text
Overview
Jobs
Job detail
Capability Intelligence
Role Capability Blueprint
Search plan / effectiveness
Market
Operations
System
```

Typical bounded flow:

```text
sync / acquire
→ fetch/refresh details
→ build/repair English v2
→ Analyze English
→ inspect P1.6
→ optionally build Capability
→ optionally build Blueprint
→ optionally export a review snapshot
```

Capability/Blueprint are still reviewed per job; they are not automatically generated across the corpus.

---

## Quick Add

Quick Add accepts only approved Jobinja inputs:

- one public Jobinja job URL;
- one public Jobinja `/jobs` search URL;
- one Persian/English keyword phrase interpreted as a bounded Jobinja search.

It is not an arbitrary-web ingestion escape hatch.

---

## Search/acquisition principles

Search vocabulary is data, not Python career logic.

Packaged catalog:

```text
src/jobhunter/data/search_catalog.toml
```

Search terms support acquisition recall. They are not canonical career taxonomy or personal relevance proof.

Critical source invariant:

```text
network / 429 / 5xx / challenge / auth failure
!=
expired or removed vacancy
```

Provider/source failure is not a valid empty result.

---

## Source evidence and versions

JobHunter distinguishes:

```text
JobPosting                 stable source identity
Raw evidence               exact acquired response
JobPostingVersion          meaningful employer-content version
Fetch observation          operational source check
Lifecycle state            cautious interpretation of checks
```

Volatile HTML changes do not automatically manufacture a semantic job change.

---

## English projection v2

Source and English remain separate:

```text
original source text    authoritative
        ↓
English projection      derived convenience
```

Native-English strings are identity-projected. Persian-containing semantic units are translated through bounded structured LM Studio requests and deterministic integrity checks.

Google Cloud Translation remains optional external processing, not a normal dependency.

---

## First Market layer

Current Market aggregates accepted/current **English P1.6** artifacts only.

It does not yet aggregate Capability or Blueprint.

It is not yet a canonical Phase-2 taxonomy. Small/concentrated analyzed samples must remain explicitly scoped/warned.

---

## CLI

Important current commands:

```bash
jobhunter run
jobhunter jobinja plan
jobhunter jobinja sync
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs health <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter jobs capability <job-id>
jobhunter jobs blueprint <job-id>
jobhunter jobs snapshot <job-id>
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

Browser and CLI share underlying services/state.

---

## Local/security boundary

- loopback-first browser binding;
- CSRF validation on mutating forms;
- restrictive browser security headers;
- packaged local static assets;
- acquired job text is untrusted data;
- no application/login automation;
- no CAPTCHA/access-control bypass;
- no autonomous recruiter/application messaging.

---

## Current near-term execution

Continue from the current repository state; do not restart the old August-3 checklist.

```text
1. fix integrated Review Snapshot effective-model routing
2. deterministic Ruff / pytest / warnings gate
3. harden P1.6 factual coverage / optionality / explicit depth on tG9K
4. rebuild/review tG9K P1.6
5. calibrate Capability
6. calibrate Blueprint
7. compare stronger dedicated reasoning model if needed
8. complete CI-3 with materially different real jobs using snapshots
9. stop expanding the semantic slice once accepted
10. finish Market/source/lifecycle/partial-success/P1.7 acceptance
11. close Phase 1
12. only then begin corpus-wide Phase 2
```

See [Execution TODO](docs/EXECUTION_TODO.md).

---

## What JobHunter does not claim yet

JobHunter does **not** yet claim:

- Phase 1 fully closed/accepted;
- perfect translation/semantic reasoning across every role/language;
- production-quality Capability/Blueprint across all roles;
- complete lifecycle/repost resolution;
- canonical Phase-2 market taxonomy;
- corpus-wide inferred-capability aggregation;
- complete-market conclusions from bounded Jobinja evidence;
- reviewed personal capability state;
- readiness/gap/career recommendations;
- evidence-backed resume/interview/application claims;
- autonomous applications;
- arbitrary-web ingestion;
- generic source-plugin platform;
- evaluated RAG/agent authority.

---

## Development validation

```bash
ruff check .
pytest
pytest -W error
```

Normal deterministic tests do not contact Jobinja, Google Cloud, or LM Studio. Live model/source validation is separate and bounded.

---

## Documentation

Required/current entry points:

- [Product Specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Domain and Analysis Model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source Policy](docs/SOURCE_POLICY.md)
- [Roadmap](docs/ROADMAP.md)
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [Execution TODO](docs/EXECUTION_TODO.md)
- [Semantic Analysis](docs/SEMANTIC_ANALYSIS.md)
- [Semantic Quality Acceptance Plan](docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md)
- [Capability Intelligence Plan](docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md)
- [Role Capability Blueprint Plan](docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md)
- [Review Snapshots](review-snapshots/README.md)
- `docs/WORKING_MEMORY.md` — rolling current handoff when present
- [Repository Instructions](AGENTS.md)
