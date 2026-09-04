# JobHunter Portfolio Release, CV, and Interview Package

**Status:** PR9 repository-side release candidate package  
**Date:** 2026-09-04  
**Candidate release:** `v0.1.0` / package version `0.1.0` / alpha  
**Product-development boundary:** P2.2B-B1 remains separately blocked on machine-local `ta9l` English projection/P1.6 acceptance. This portfolio package does not authorize or bypass that gate.

---

## 1. Purpose

This document is the reusable final portfolio package for JobHunter.

It provides:

- the verified release-candidate story;
- truthful release notes for the first intentional portfolio release;
- GitHub metadata recommendations;
- a CV project entry;
- a 30-second recruiter explanation;
- a 2–3 minute hiring-manager explanation;
- a 10–15 minute technical architecture walkthrough;
- interview talking points and likely technical questions;
- a transparent explanation of AI-assisted development ownership;
- an owner mastery checklist before using the project in interviews.

It is not a new product specification and does not override product/domain/source/architecture authority.

---

# Part I — Release-candidate truth

## 2. Current project identity

JobHunter is a **local-first career-intelligence system that turns real public job-posting evidence into traceable, reviewable career intelligence**.

The current application is a Python modular monolith with:

```text
bounded Jobinja acquisition
→ immutable source evidence
→ deterministic parsing / semantic job versions
→ provenance-preserving English projection
→ reviewed P1.6 factual extraction
→ parallel downstream consumers
   ├─ Capability Intelligence v9
   ├─ Job Work Intelligence v2
   ├─ reviewed Canonical Registry mappings
   └─ bounded Market/report read models
```

Browser and CLI share the same application services and SQLite runtime/history authority.

The public repository additionally contains:

- deterministic repository-safe `corpus/` projection;
- selected `review-snapshots/` acceptance evidence;
- current architecture/product/source/reasoning documentation;
- reproducible public demo walkthrough;
- fresh-clone development setup;
- CI-backed package/entrypoint/lint/test verification;
- explicit security/private-state/publication boundaries.

## 3. Current accepted public evidence baseline

```text
Known/discovered Jobinja identities: 353
Fetched/parsed job details:           43
Current English projections:          20
Accepted English P1.6 artifacts:       5
Accepted Capability artifacts:         5
```

`353` means discovered identities, not 353 fully analyzed postings.

Accepted heterogeneous P1.6 → Capability anchors include:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

The reproducible public demo uses:

- `t4qV` as a rich responsibility-heavy network/security example;
- `tmBK` as a sparse qualification-heavy Python example where responsibilities intentionally remain empty.

## 4. Current maturity

```text
Phase 1                         CLOSED
P2.1 Canonical Registry        CLOSED / ACCEPTED
P2.2A Job Work Intelligence    CLOSED / ACCEPTED
P2.2B selective responsibility promotion pilot    IN PROGRESS / LOCAL GATE
```

Blueprint v6 remains experimental/historical and non-authoritative.

Current JobHunter does **not** claim:

- semantic acceptance across every discovered job;
- complete labor-market taxonomy coverage;
- market-wide statistical representativeness from the current small accepted semantic sample;
- arbitrary-web ingestion;
- reviewed personal fit/readiness/gap scoring;
- autonomous applications or recruiter communication;
- production-scale multi-user deployment;
- an accepted/evaluated RAG or autonomous-agent platform.

## 5. Engineering differentiators

The strongest engineering story is not the number of features. It is the authority model.

JobHunter separates:

```text
SOURCE FACT
→ NORMALIZED CORRESPONDENCE
→ ANALYTICAL INTERPRETATION
→ RECOMMENDATION / DECISION SYNTHESIS
```

and independently separates:

```text
GENERATED / CANDIDATE
vs
REVIEWED / PROMOTED
```

Important implementation consequences include:

- immutable source evidence survives downstream processing;
- deterministic code owns identity, provenance, coverage, currentness, lifecycle and bookkeeping;
- model reasoning is allowed for semantic organization/interpretation but cannot manufacture employer facts;
- accepted downstream artifacts preserve exact dependency identities;
- generated semantic candidates can be rejected without overwriting history;
- strictness scales with authority and blast radius;
- uncertain interpretation can remain useful and explicitly uncertain rather than becoming fabricated certainty;
- local model use is bounded, failure-aware and subordinate to source evidence;
- repository-public projection is separate from private runtime/history state.

---

# Part II — Release readiness

## 6. Candidate version

Use:

```text
package version: 0.1.0
candidate Git tag: v0.1.0
release maturity: Alpha / portfolio release
```

Reason:

- `pyproject.toml` already declares `0.1.0`;
- the package classifier is `Development Status :: 3 - Alpha`;
- there is currently no Git tag or GitHub release;
- introducing a different portfolio-only version would add unnecessary versioning complexity.

Do not tag until the remaining release actions below are explicitly resolved.

## 7. Remaining release actions

### Owner decision — license

No repository license is currently present and GitHub reports no detected license.

The owner must explicitly decide whether third-party reuse should be granted and under what terms. Do not add a permissive license merely because portfolio repositories often have one.

Until that decision is made, do not claim that JobHunter is MIT/Apache/GPL/open-source licensed.

### GitHub repository settings

Current GitHub metadata still has:

```text
description: null
topics: []
homepage: null
```

Recommended description:

> Local-first career intelligence from real job evidence, with provenance-preserving LLM analysis, semantic review, and auditable Python workflows.

Recommended topics:

```text
python
fastapi
sqlite
llm
lm-studio
career-intelligence
job-market
provenance
local-first
pydantic
```

Recommended homepage decision:

- leave blank while there is no separate meaningful hosted destination;
- do not point it somewhere merely to fill the field.

### Real browser screenshots

`docs/demo/` intentionally contains no fabricated screenshots.

When machine-local runtime access returns:

1. launch the real application;
2. use only non-private/public-safe job state;
3. capture 2–4 representative screens;
4. inspect screenshots for local paths, private data, tokens or unrelated personal state;
5. add them to the public README/demo only after that review.

Preferred screenshots:

- dashboard/job catalog with meaningful corpus/workflow state;
- accepted job detail showing source/English/P1.6 separation;
- Capability or Work Intelligence view;
- Canonical Registry/Market view only when it communicates a current accepted boundary clearly.

### Tag/release operation

There are currently no Git tags and no GitHub releases.

After the license/metadata/screenshot decisions are complete and final CI is green:

```text
v0.1.0
```

is the intended first portfolio tag/release candidate.

---

## 8. Candidate GitHub release notes — `v0.1.0`

### JobHunter v0.1.0 — local-first career intelligence alpha

JobHunter v0.1.0 is the first intentional portfolio release of a local-first Python career-intelligence system built around traceable public job evidence rather than opaque job matching.

#### Highlights

- bounded, policy-controlled Jobinja discovery/fetch workflows;
- immutable source evidence, stable posting identity and semantic source versions;
- provenance-preserving English projection with native/translated segment tracking;
- reviewed P1.6 factual extraction for responsibilities, requirements, strength, depth and exact evidence;
- Capability Intelligence v9 with deterministic source survival and bounded model reasoning;
- Job Work Intelligence v2 with exact accepted-work injection and bounded interpretation;
- reviewed Canonical Concept Registry mappings with currentness/idempotency constraints;
- bounded Market/report read models;
- local FastAPI/Jinja2 browser plus shared CLI/application services;
- SQLite runtime/history authority;
- deterministic repository-safe public corpus and selected review snapshots;
- reproducible public demo that requires neither maintainer SQLite state nor LM Studio;
- CI-backed package installation, dependency consistency, entrypoint smoke, Ruff, pytest and warnings-as-errors;
- documented security, source-policy, provenance, privacy and public/private-state boundaries.

#### Current public corpus baseline

```text
353 discovered identities
43 fetched/parsed detail jobs
20 current English projections
5 accepted English P1.6 artifacts
5 accepted Capability artifacts
```

These counts describe the committed evidence state, not production-scale market coverage.

#### Design principles

- source evidence before interpretation;
- deterministic bookkeeping/provenance, semantic reasoning where appropriate;
- generated candidates separated from reviewed/promoted authority;
- unknown/unresolved preferred over fabricated certainty;
- local-first inference and persistence;
- bounded requests, retries and model calls;
- public repository projection separated from private runtime state.

#### Current limitations

- Jobinja is the only approved recurring public source adapter;
- accepted semantic evidence is intentionally bounded rather than corpus-wide;
- Work Intelligence and Canonical Registry runtime state are not currently published into `corpus/`;
- Blueprint remains experimental/non-authoritative;
- personal capability evidence, gap/readiness scoring and application decisions are future product layers;
- no autonomous job application or recruiter messaging;
- no production multi-user deployment claim;
- no accepted RAG/agent platform.

---

# Part III — CV package

## 9. Default CV project entry

**JobHunter — Local-first Career Intelligence Platform**  
*Python, FastAPI, SQLite, Pydantic/JSON Schema, LM Studio/LLMs, Jinja2, pytest, Ruff, GitHub Actions*

- Designed and built a provenance-preserving pipeline that converts bounded public job-posting evidence into reviewed factual, capability and work intelligence while keeping employer source truth separate from LLM interpretation.
- Implemented deterministic artifact/version lineage, semantic review/promotion gates, bounded local-model workflows, canonical claim mappings, failure-aware acquisition and a repository-safe public corpus over local SQLite runtime history.
- Built shared browser/CLI workflows plus broad CI-backed regression coverage across acquisition, parsing, translation, LLM contracts, lifecycle/currentness, Capability/Work Intelligence, Registry behavior and public export.

### Shorter one-bullet version

Built a local-first Python/FastAPI career-intelligence system that turns real job postings into provenance-traceable factual, capability and work intelligence using deterministic evidence/version controls, reviewed LLM outputs, SQLite history, and CI-backed browser/CLI workflows.

### What not to put on the CV yet

Do not claim:

- production users or production scale;
- 353 fully analyzed jobs;
- market-wide accuracy metrics;
- automated job applications;
- personal fit scoring;
- a production RAG/agent architecture;
- independent ownership of every manually typed line of code.

---

# Part IV — Spoken explanations

## 10. 30-second recruiter summary

> JobHunter is a local-first Python career-intelligence application I built to turn real job postings into structured, traceable evidence instead of manually reading vacancies or trusting opaque LLM summaries. It uses bounded acquisition, SQLite history, provenance-preserving translation, reviewed factual extraction, capability and work intelligence, and a local FastAPI browser/CLI. The main engineering focus is making LLM reasoning useful without letting it overwrite source truth.

## 11. 2–3 minute hiring-manager explanation

> The problem I wanted to solve was that job-market research becomes repetitive and unreliable if every vacancy is read manually or summarized independently by an LLM. JobHunter creates a durable evidence pipeline instead.
>
> It starts with bounded Jobinja acquisition. Every successful source fetch is preserved before interpretation, then deterministic parsing creates stable job identity and semantic source versions. If needed, the system builds an English projection while retaining the original employer text as authority and recording which segments were native or translated.
>
> Above that I have a reviewed factual layer called P1.6. It extracts responsibilities, requirements, requirement strength, explicit depth and exact supporting evidence. Fresh model output is a candidate until it passes the semantic review boundary. Accepted P1.6 then fans out to different consumers rather than becoming one monolithic LLM result: Capability Intelligence groups supported capability areas, Work Intelligence organizes accepted work, the Canonical Registry stores reviewed cross-job correspondences, and Market/report views aggregate bounded accepted evidence.
>
> The design is intentionally a Python modular monolith with SQLite. Browser and CLI use the same services and durable state. I chose that instead of microservices or a separate SPA because this is currently a local single-user application and the extra operational complexity is not justified.
>
> A major project theme is separating deterministic responsibilities from semantic reasoning. IDs, provenance, dependency currentness, source coverage and lifecycle bookkeeping are deterministic. Models are used where semantic interpretation adds value, but model wording cannot become employer fact merely because it sounds plausible.
>
> The repository also contains a deterministic public corpus and demo, so reviewers can inspect real accepted chains without my private SQLite database, LM Studio or live Jobinja access. The CI pipeline verifies installation, dependencies, entrypoints, linting, the test suite and warnings-as-errors.

## 12. 10–15 minute technical architecture walkthrough

Use this order rather than narrating repository chronology.

### 1. Product problem — 1 minute

Explain:

- vacancy-by-vacancy reading does not scale well for personal career research;
- generic LLM summaries lose provenance and blur source fact with interpretation;
- JobHunter's goal is useful career intelligence with recoverable evidence.

### 2. Source/acquisition boundary — 1–2 minutes

Explain:

- Jobinja is the current approved recurring source;
- acquisition is bounded by hosts/paths/pages/request budgets/retries;
- CAPTCHA/auth/access-control bypass is explicitly prohibited;
- source responses are classified rather than treated as one generic failure;
- transient network/server failures cannot become destructive lifecycle conclusions.

### 3. Evidence, identity and versions — 1–2 minutes

Explain the difference between:

```text
raw evidence
JobPosting logical identity
JobPostingVersion semantic employer-content version
fetch/check observation
lifecycle interpretation
```

Explain why model/provider changes do not create new source semantic versions.

### 4. English projection — about 1 minute

Explain:

- original source remains authority;
- English is a derived convenience projection;
- native vs translated segments retain provenance;
- provider/model/schema/source identity remains attached.

### 5. P1.6 factual authority — 2 minutes

Explain:

- responsibilities must not be manufactured from qualifications;
- exact evidence is locally validated;
- strength and technical depth are separate dimensions;
- fresh candidate artifacts require explicit semantic review before promotion;
- rejected candidates remain historical evidence rather than being silently overwritten.

Use `tmBK` as the simple example of why an empty responsibilities list can be correct.

### 6. Downstream fan-out — 2 minutes

Explain that accepted P1.6 is the factual substrate for separate consumers:

```text
Capability Intelligence
Work Intelligence
Canonical Registry
Market/report
```

Capability:
- groups supported capability areas;
- source facts/strength/depth/work links remain deterministic;
- optional model enrichment stays subordinate.

Work Intelligence:
- model proposes useful work organization;
- accepted P1.6 statements decide factual work;
- exact accepted work is injected deterministically;
- requirement-only jobs use a limited deterministic path.

Registry:
- stable reviewed concepts/aliases/mappings;
- mapping is correspondence, not source rewriting;
- no silent automatic taxonomy promotion.

### 7. Persistence and projections — 1–2 minutes

Explain:

- SQLite is runtime/history authority;
- raw evidence is independently inspectable;
- `corpus/` is deterministic public projection, not an import database;
- `review-snapshots/` are selected acceptance evidence, not the full current public corpus;
- private/personal future state is not automatically publishable.

### 8. Failure semantics and quality — 1 minute

Explain:

- hard fail for integrity/provenance/privacy/persistence defects;
- soft uncertainty for ambiguous semantic interpretation;
- partial success prevents one failed item from invalidating already durable work;
- CI: install → `pip check` → entrypoint smoke → Ruff → pytest → pytest warnings-as-errors.

### 9. Tradeoffs and future triggers — 1 minute

Explain why JobHunter currently avoids:

- microservices;
- Kubernetes;
- separate SPA state;
- vector/RAG infrastructure;
- generic plugin framework;
- multi-model voting.

Then state the trigger: adopt additional complexity only when measured scale, isolation, retrieval, provider or product requirements justify it.

---

# Part V — Interview questions and concise answers

## 13. Why SQLite instead of PostgreSQL?

Current product scope is local/single-user. SQLite gives durable transactions, schema migrations, inspectability and one simple runtime/history boundary without a server dependency. PostgreSQL becomes justified if concurrency, remote multi-user deployment or operational scale creates a real requirement.

## 14. Why a modular monolith instead of microservices?

Acquisition, analysis, review, browser and CLI currently belong to one local product and benefit from one data/history boundary. Splitting them would introduce deployment/network/observability complexity without an isolation or scale requirement. The architecture keeps domain modules explicit so future decomposition remains possible when evidence justifies it.

## 15. How do you reduce LLM hallucination risk?

Not by pretending LLM reasoning can be eliminated. JobHunter constrains where model output is authoritative:

- source evidence is preserved first;
- factual claims need exact evidence;
- evidence references are validated locally;
- deterministic code owns coverage/provenance/currentness;
- model outputs are typed and bounded;
- generated candidates are separate from reviewed/promoted authority;
- downstream layers cannot silently strengthen upstream evidence;
- uncertainty can remain unresolved instead of being guessed.

## 16. Why local LM Studio?

It fits a local-first/private workflow, avoids making cloud inference mandatory, allows explicit model-role selection and keeps source acquisition useful even when model inference is unavailable. The provider boundary remains versioned so another provider can be introduced deliberately later.

## 17. Why not use RAG/vector search yet?

Current core questions are largely structured: exact evidence, requirements, responsibilities, dependency identity, currentness and bounded aggregates. Structured/keyword access remains sufficient. A vector/RAG layer would be justified only by an evaluated retrieval use case where current structured access demonstrably fails.

## 18. What was a difficult design lesson?

A recurring lesson was that stronger prompts or larger/free-form review do not automatically preserve factual action relationships. Work Intelligence trials showed model prose could strengthen actions such as `move toward production` into `deploying`. The accepted v2 design therefore separates model-owned organization from exact accepted P1.6 work and injects the factual statements deterministically instead of trying to prompt the problem away indefinitely.

## 19. Give an example of evidence discipline.

The accepted `tmBK` Python Developer vacancy has many requirements but no explicit duties. P1.6 keeps `responsibilities: []`, and downstream capability work activities remain empty. JobHunter does not infer generic backend duties merely from the job title and technology list.

## 20. How do you handle evolving models/prompts/contracts?

Durable artifacts carry source/model/prompt/schema/dependency identities. Historical artifacts remain historical when contracts change. Currentness is checked explicitly rather than overwriting old artifacts. Rejected candidates can be preserved for reproducibility/regression evidence while a later accepted artifact becomes current.

## 21. What would make you split the architecture?

Measured requirements such as multi-user remote deployment, independent scaling/failure isolation, separate ownership/deployment cycles, or sustained database/concurrency limits. File size or portfolio fashion is not enough.

## 22. What is currently the biggest product limitation?

The system has a strong market/job evidence substrate, but the future personal half is not implemented yet: reviewed personal evidence, gap/readiness analysis, personalized learning/action planning and application-decision intelligence remain later stages. Current semantic acceptance is also intentionally bounded rather than market-wide.

---

# Part VI — AI-assisted development ownership

## 23. Recommended interview answer

> I used AI coding assistants extensively during the project, including for implementation, refactoring, tests and documentation. I do not present every line as manually typed by me. My ownership is in defining the product problem, engineering constraints, source/provenance and authority model, architecture, acceptance criteria, review decisions, debugging direction, regression requirements and the iterative decisions about what to keep, reject, defer or redesign. I also use the project as a learning-by-building system, so before representing an area in an interview I make sure I can explain its data flow, tradeoffs and failure modes.

This is stronger and more credible than either hiding AI assistance or claiming that directing an AI assistant removes the need to understand the resulting system.

## 24. Ownership evidence visible in the repository

Examples include:

- explicit product/source/domain/architecture governance;
- accepted/rejected semantic artifacts and working-memory decisions;
- multiple redesigns after evidence showed prompt-only fixes were inadequate;
- reproducible regression tests from real failures;
- documented stop lines against overengineering and unsupported feature growth;
- explicit historical/current boundaries instead of deleting unsuccessful work;
- bounded portfolio refactors that preserved semantic behavior;
- current-vs-future claims narrower than the full roadmap.

---

# Part VII — Owner mastery check

## 25. Mastery rule

The interview requirement is **not** to rewrite the entire codebase from memory.

Before making a technical claim, the owner should be able to:

```text
explain what the subsystem does
→ explain why it exists
→ trace its main input/output path
→ identify which facts are authoritative
→ identify important failure/uncertainty behavior
→ explain the main design tradeoff
→ locate the relevant source/tests/docs when deeper detail is needed
```

## 26. Must explain comfortably

1. JobHunter's product problem and current non-goals.
2. Why the architecture is local-first and a modular monolith.
3. Why SQLite is appropriate now and what would trigger replacement.
4. Raw evidence vs JobPosting vs JobPostingVersion vs fetch observation.
5. Source fact vs English projection vs factual extraction vs interpretation.
6. The four-level epistemic authority ladder.
7. Candidate/generated vs reviewed/promoted.
8. P1.6 responsibilities vs requirements and why qualifications cannot manufacture duties.
9. Capability Intelligence's deterministic/model split.
10. Work Intelligence v2's exact-work injection design.
11. Canonical Registry correspondence and why it is not automatic taxonomy growth.
12. Runtime SQLite vs public corpus vs review snapshots.
13. Bounded acquisition/retry/lifecycle safety.
14. Hard integrity failure vs soft interpretive uncertainty.
15. Why Blueprint is non-authoritative.
16. Why RAG/microservices/extra infrastructure are deferred.
17. Current P2.2B local gate and why portfolio work does not bypass it.
18. One real failure/redesign story from the project.
19. CI/test strategy and what warnings-as-errors adds.
20. How AI assistance was used and what project ownership means.

## 27. Must be able to trace in source when asked

- CLI/browser → shared services → SQLite;
- Jobinja acquisition → evidence → parser → semantic version;
- translation artifact currentness;
- P1.6 current routing/review state;
- Capability current entrypoint and source-survival path;
- Work Intelligence generation/validation/exact-work injection;
- Registry persistence/mapping/currentness;
- public corpus exporter/manifest/status path;
- one representative browser route/service path;
- one representative regression test from a real semantic or dependency incident.

## 28. Useful deeper topics, not required to memorize first

- every historical P1.6 prompt version;
- every experiment artifact ID;
- every SQL migration statement;
- every Jinja template detail;
- all CLI argument syntax;
- every historical Blueprint/Capability implementation;
- dependency internals unrelated to a project decision.

Know how to locate these. Do not spend interview-preparation time memorizing them without a concrete reason.

## 29. Owner mastery acceptance

PR9 owner mastery is complete only after an interactive review confirms the owner can explain the **must-explain** topics above at the level claimed in the CV/interview package.

Until then, the package is prepared but owner mastery remains **not yet verified**.

---

# Part VIII — Exact final release sequence

When the remaining owner/local actions are available:

```text
1. choose explicit license policy
2. set GitHub description/topics (homepage only if meaningful)
3. capture and privacy-review 2–4 real browser screenshots
4. update README/demo with those real screenshots
5. recheck repository/current public counts and package version
6. confirm latest CI is green
7. tag v0.1.0
8. create GitHub release using the release notes in this document
9. verify the tagged README/architecture/demo match the release
10. complete the interactive owner mastery pass
11. use the finalized CV entry/interview narratives
```

Do not advance P2.2B product semantics as part of this release sequence.
