# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product and engineering priority

JobHunter is a repeated-use **local-first personal career-intelligence application**. Its primary product objective is to help the user understand jobs, the market, career requirements, gaps, and actions **faster and better than manual vacancy-by-vacancy reading** while preserving trustworthy source/state boundaries.

Optimize for **useful, decision-relevant intelligence per unit of user time**, subject to source integrity, provenance, privacy, and honest uncertainty.

Do not confuse trustworthiness with maximal determinism. Deterministic machinery protects state, provenance, bookkeeping, and reusable authority; semantic/model reasoning is an expected product capability for interpretation, synthesis, comparison, and recommendations when correctly labeled and traceable.

The mature product is not merely a scraper, generic matcher, semantic-audit laboratory, resume generator, or autonomous application bot.

## 2. Required reading order and authority

Before material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
5. `docs/SOURCE_POLICY.md`
6. `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`
7. `docs/ROADMAP.md`
8. `docs/IMPLEMENTATION_PLAN.md`
9. `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`
10. the current active phase/focused plan
11. `docs/EXECUTION_TODO.md`
12. `docs/WORKING_MEMORY.md`
13. task-specific experiment/working-memory records, `corpus/README.md`, and selected review snapshots as needed.

Historical Phase-1 plans remain evidence/history, not automatic current execution gates after their scope is closed.

Proposal/experiment/working-memory files do not override controlling product, domain, source, architecture, reasoning-policy, roadmap, implementation, or active focused-plan documents.

The dated current-state reconciliation is a **status-only overlay**: it supersedes obsolete present-tense status wording in older master/current documents but does not replace their durable product/architecture/roadmap semantics.

Authority:

```text
product/domain/source/architecture
→ utility/epistemic reasoning policy
→ roadmap
→ implementation plan
→ current-state reconciliation for present-tense status only
→ active phase/focused plan
→ execution TODO / working memory
→ implementation/tests/live acceptance
```

The reasoning policy operationalizes existing product/domain/architecture principles; it does not authorize violations of higher source/privacy/meaning constraints. If artifacts conflict, reconcile them rather than choosing the convenient instruction.

### 2.1 Permanent epistemic/promotion rule

Always distinguish:

```text
SOURCE FACT
strict source/provenance integrity

NORMALIZED CORRESPONDENCE
reviewed/deterministic mapping while preserving source wording

ANALYTICAL INTERPRETATION
model/semantic reasoning allowed; confidence/evidence/uncertainty as appropriate

RECOMMENDATION / DECISION SYNTHESIS
explainable reasoning over qualified inputs
```

Also distinguish:

```text
GENERATED / CANDIDATE
useful immediately when transparently inferred and bounded

REVIEWED / PROMOTED
reusable durable authority with stronger validation
```

Human review is primarily a **promotion boundary**, not a prerequisite for every useful interpretation.

Strictness must scale with authority and blast radius. Do not demand market-scale proof for a job-level interpretation, and do not present one-job interpretation as market truth.

### 2.2 Hard-failure versus soft-uncertainty rule

Fail hard for integrity defects such as wrong/stale dependency identity, corrupt persistence, fabricated employer facts, unsupported source evidence, unsafe lifecycle transitions, privacy violations, or invalid canonical mutations.

Fail soft for interpretive uncertainty such as ambiguous role family, multiple plausible archetypes, incomplete technical scope, small analytical samples, or uncertain responsibility grouping.

Preferred interpretive behavior:

```text
uncertain
→ lower confidence / show alternatives / preserve unknowns / warn
→ still provide useful bounded interpretation when possible
```

Do not convert interpretive uncertainty into a blocker merely because deterministic proof is unavailable.

## 3. Current implementation and acceptance state

```text
parser:                     jobinja-detail-v2
translation provider:       lm-studio-translation-v2
English projection:         english-projection-v2

English P1.6 public:        job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:       job-analysis-original-v9 / job-analysis-v4

Capability public/current:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Capability v7:              historical
Capability v8:              historical / semantic reject

Blueprint experimental:     role-capability-blueprint-v6 / role-capability-blueprint-v5
Canonical Registry:         jobhunter-canonical-concept-registry-v1
Job Work Intelligence:      job-work-intelligence-v2 / prompt-pipeline job-work-intelligence-v2.0
Review Snapshot:            job-review-snapshot-v1
Public Corpus:              jobhunter-public-corpus-v1
```

Accepted/current factual chains:

```text
tG9K English P1.6 artifact 36 → Capability v9 artifact 11
t4jp English P1.6 artifact 37 → Capability v9 artifact 12
tmBK English P1.6 artifact 39 → Capability v9 artifact 13
t4qV English P1.6 artifact 44 → Capability v9 artifact 14
tmyX English P1.6 artifact 46 → Capability v9 artifact 15
```

Capability v9 public promotion is closed and operationally verified. Blueprint remains non-current/non-authoritative.

The public corpus is operationally closed and remotely available. The accepted publication baseline is:

```text
known/discovered Jobinja jobs: 353
fetched/parsed detail jobs:      43
current English projections:     20
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Canonical Registry P2.1A deterministic persistence, P2.1B manual CLI review, P2.1C browser review, and P2.1D small real-data seed are all accepted. **P2.1 is closed.** Registry publication remains unauthorized.

The 2026-08-26 governance reorientation is accepted through `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`. It preserves the strict Phase-1/P2.1 substrate while preventing future work from requiring promotion-grade proof for every low-blast-radius interpretation.

The controlling P2.2 documents are:

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md
```

P2.2A Job Work Intelligence v2 is **accepted and closed**. P2.2B-B1 is the active bounded responsibility-promotion pilot. Repository-side evidence selection and preflight are complete; no responsibility promotion has occurred yet.

Current P2.2 state:

```text
P2.2A historical v1-v1.7 artifacts/attempts → preserved immutable evidence
P2.2A v2 schema                           → job-work-intelligence-v2
P2.2A v2 prompt/runtime                   → job-work-intelligence-v2.0
P2.2A repository/live acceptance          → PASSED / CLOSED
P2.2B-B1 repo evidence selection          → COMPLETE
P2.2B-B1 selected candidate               → ta9l
P2.2B-B1 current gate                     → ta9l local English + P1.6 semantic authority
P2.2B-B1 canonical promotion              → NOT YET AUTHORIZED
P2.2C                                     → BLOCKED
```

The 2026-09-01 P2.2A checkpoint verified that free-form model review did not reliably preserve action relationships across heterogeneous jobs. Controlled historical trials remain immutable evidence. The accepted response is representation-level fact/interpretation separation, not another model-trial matrix.

Do not reopen P1.6 v20, Capability v9, P2.1, or P2.2A merely for harmless non-authoritative wording variation. Reopen only for a repeatable material correctness/provenance/contract defect or a changed accepted dependency.

## 4. Blueprint disposition

Blueprint is implemented and inspectable but **is not an accepted decision layer**.

Historical v6/12B evidence remains experimental. Complete semantic review found assumption-bearing interpretation beyond vacancy authority even after mechanical provenance passed.

During P2.2B-B1:

- do not create Blueprint v7;
- do not weaken Blueprint validators;
- do not add vacancy/domain-specific prompt patches merely to obtain a passing artifact;
- do not use Blueprint for Market, personal readiness, automatic recommendations, or other authoritative decisions;
- keep Blueprint v6 pinned to historical Capability v7 dependency semantics until an explicit evidence-backed reopening decision.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

This does **not** mean Phase-2 interpretation in general is prohibited. New bounded analytical interpretation may be designed under the reasoning policy without promoting Blueprint or treating model prose as employer truth.

## 5. Current exact next-work rule

Phase 1, P2.1, and P2.2A are closed. The exact current product gate is P2.2B-B1 under:

```text
docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md
```

Current active gate:

```text
P2.2B-B1 selective responsibility promotion
→ focused plan APPROVED
→ bounded repository evidence scan COMPLETE
→ ta9l selected
→ repository-side local-runtime preflight COMPLETE
→ ta9l current English projection + P1.6 v20/v5 semantic review NEXT
→ no canonical responsibility promotion yet
→ P2.2C BLOCKED
```

Selected evidence:

```text
accepted anchor:
tG9K P1.6 artifact 36 responsibility[5]
Design rigorous validation and monitoring for models running in an industrial setting.

selected ta9l source duty:
Create evaluation, testing, and observability frameworks for LLM and agent performance.

tentative identity, NOT PROMOTED:
responsibility:design-ai-evaluation-monitoring
```

Local execution packet:

```text
docs/working-memory/2026-09-06_P2_2B_B1_TA9L_LOCAL_RUNTIME_PREFLIGHT.md
```

Current exact next action:

```text
local doctor / translation-provider status
→ ta9l current English projection
→ inspect current English projection
→ ta9l English P1.6 v20/v5 generation
→ inspect complete review-analysis state
→ semantic accept or reject on whole-artifact quality
→ if accepted, report exact artifact ID + responsibility index + statement + evidence
→ compare exact accepted ta9l claim with tG9K P1.6 36 responsibility[5]
→ final non-lossy correspondence review
→ only if still aligned: one concept + two mappings
→ idempotency + CLI/browser/currentness/publication-boundary verification
→ B1 PASS or evidence-based NO-PROMOTION / DEFER
```

Do **not** repeat the already-completed repository scan before testing `ta9l`. Do not accept a second additional job unless `ta9l` is explicitly rejected and a new focused decision authorizes continued evidence search. Do not accept an otherwise defective P1.6 artifact merely because one selected responsibility is convenient for B1.

The P2.2A direct-work flow remains permanently accepted:

```text
accepted/current English P1.6 factual work substrate
→ typed CandidateJobWorkIntelligence generation
→ deterministic dependency/reference/coverage/scope validation
→ one bounded regeneration only if those post-generation guards reject the candidate
→ deterministic injection of exact accepted P1.6 direct-work statements
→ assembled-artifact exact dependency validation
→ persisted generated/candidate artifact for repeated-use UX
```

Core P2.2A decisions remain:

- accepted/current English P1.6 v20/v5 is the primary authoritative input;
- Capability v9 is not an authoritative dependency for P2.2A;
- existing registry mappings may enrich but never gate generation;
- every candidate work theme must own at least one accepted responsibility or role-purpose reference;
- requirements may support a theme but may not independently manufacture duties or strengthen factual action/ownership/lifecycle scope;
- candidate artifacts persist for reproducibility/reuse but persistence does not mean promotion;
- candidate output does not require human approval merely because a model generated it;
- relative emphasis is `primary` / `supporting` / `uncertain`, not fake percentages;
- confidence is qualitative and does not claim calibrated probability;
- deliverables may be `source_explicit` or `strongly_implied_by_work` with required accepted-work support;
- candidate role/archetype interpretation is allowed at job level without becoming stable market taxonomy;
- exact accepted P1.6 statements carry factual action authority inside v2 themes/deliverables;
- theme labels, rationales, deliverable labels/rationales, and role labels remain JobHunter interpretation;
- there is **no dedicated second semantic authority-review model pass** in v2;
- semantic action relationships must not be replaced by a deterministic verb-equivalence table merely for testability;
- browser is the normal user surface; CLI is secondary generation/inspection/debugging;
- P2.2 state remains local unless a separate publication decision authorizes otherwise.

During P2.2B-B1:

- do not bulk-map the remaining accepted P1.6 claim corpus;
- do not broaden the canonical ontology merely to eliminate unmapped cases;
- do not normalize partial semantic overlaps as whole-claim equivalence;
- do not broaden a concept merely to absorb compound claims;
- do not auto-promote P2.2A theme or deliverable labels;
- do not add deliverable mapping schema without concrete repeated-value evidence;
- do not publish canonical-registry or P2.2 state;
- do not start P2.2C/P2.2D promoted family/archetype work;
- do not add personal evidence/readiness/scoring/recommendations;
- do not add deterministic action-verb equivalence machinery;
- do not restore the P2.2A second semantic authority-review pass;
- do not impose a fixed quota of primary themes;
- do not ask the owner to rerun already-proven repository quality gates without new evidence requiring them.

## 6. Permanent semantic boundaries

### P1.6

P1.6 is the strict factual substrate:

- preserve explicit source facts and exact evidence;
- account for meaningful requirements on dense postings;
- remain restrained on sparse postings;
- keep obligation strength and technical depth separate;
- never spread one depth adjective across neighboring technologies;
- preserve optional/contextual wording;
- uncertain source claims remain contextual/unknown rather than forced;
- structured source skills cannot silently disappear;
- qualification wording must not fabricate job duties.

These strict rules protect factual substrate authority. They do not prohibit later analytical interpretation from making explicitly inferred, confidence-qualified conclusions above that substrate.

### Capability Intelligence v9

Current accepted architecture:

```text
accepted P1.6 source truth
→ compact semantic group plan
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

Permanent v9 rules:

- every capability-relevant accepted P1.6 requirement must be covered;
- every accepted responsibility must be covered;
- source indices/evidence must be valid and grounded;
- dense sources cannot collapse into one catch-all group;
- source requirement strength, source-explicit depth, and source work are deterministic;
- role-level education/duration-only experience stay separate;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture claims are blocked or filtered;
- zero optional model enrichment is valid;
- redundant model `source_explicit` echoes are discarded; deterministic reconciliation remains authority;
- incomplete authoritative source truth cannot persist.

Important downstream lesson: **Capability grouping and deterministic source truth may flow downstream; model-owned explanatory prose is not automatically authoritative.** It may still be used as candidate/analytical reasoning when a later contract explicitly labels and bounds it rather than promoting it as source truth.

### Blueprint

Blueprint is experimental professional interpretation above historical accepted source truth. Its generated prose is not current authority.

No downstream layer replaces upstream authority. Mechanical linkage never certifies semantic truth.

### Analytical interpretation above the strict substrate

For Phase 2 and later, analytical interpretation is a first-class product capability.

Permitted examples include:

- job work-composition summaries;
- candidate responsibility-family assignments;
- candidate role archetypes;
- cross-job semantic comparisons;
- strongly work-implied capability expectations;
- explainable recommendations when their prerequisite personal-evidence policy exists.

Requirements:

- never present inference as employer wording;
- retain traceability to supporting facts where consequential;
- communicate material uncertainty/confidence;
- promote to reusable canonical authority only through the applicable stronger review boundary.

## 7. Versioned public-corpus rules

The local SQLite database remains the operational/runtime authority:

```text
data/jobhunter.sqlite3
```

The repository-safe public projection is:

```text
corpus/
```

Contract:

```text
jobhunter-public-corpus-v1
```

Purpose:

- make every known public Jobinja job remotely inspectable;
- preserve original Persian/English parsed vacancy content as UTF-8 JSON;
- project current successful English projection, accepted P1.6, and Capability artifacts with exact dependency/contract identities;
- support remote AI review, heterogeneous selection, reproducibility, and bounded analysis without direct access to local SQLite.

The public corpus is a deterministic projection, **not** a runtime input and **not** a replacement database.

Optional stage files exist only when that stage is current for the current source dependency. If the source changes, stale downstream files must disappear until rebuilt. Git history preserves previously published states.

Never export into `corpus/`:

- SQLite/WAL/SHM files;
- machine-local evidence paths;
- raw HTML evidence;
- LM Studio request bodies/raw protocol responses;
- prompts/secrets/API credentials;
- logs/debug histories;
- local configuration;
- future private/personal evidence, applications, notes, profiles, or outcomes.

Any future schema expansion must explicitly review the privacy/publication boundary before adding fields.

Normal mutating CLI workflows and completed web background operations synchronize the local `corpus/` projection **after** durable SQLite work where currently designed. Projection failure must be surfaced but must never roll back durable SQLite success.

JobHunter does **not** automatically Git commit or push. Publishing remains intentional.

Detailed format and command rules live in `corpus/README.md`.

## 8. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

`review-snapshots/` and `corpus/` are distinct:

```text
corpus/           complete current public dataset
review-snapshots/ selected semantic-review evidence
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally. Dependency-current flags remain distinct from explicit semantic-review state.

Never commit SQLite/WAL/SHM, raw model responses/prompts, secrets, logs, raw HTML contents, or future private user state.

The tracked `jobhunter.toml` is public project configuration. Never place actual API tokens/passwords/keys in it; use an ignored local secret mechanism.

## 9. Record boundaries

Never conflate:

```text
JobPosting
SearchPageSnapshot
JobPostingVersion
JobDetailFetchObservation
JobLifecycle state/event
JobTranslationArtifact
JobAnalysisArtifact
Capability artifact
Role Blueprint artifact
JobUserWorkflow
Market aggregate
Canonical Concept Registry
JobWorkIntelligenceArtifact
candidate analytical interpretation
promoted reusable semantic knowledge
Public Corpus projection
Review Snapshot
Raw evidence
```

Preserve provenance and dependency identity across every derived layer.

## 10. Interaction, security, and source rules

```text
local browser UI   normal repeated human use
CLI                automation/debug/advanced operation
```

Permanent constraints:

- loopback-first browser binding;
- CSRF on mutating forms;
- restrictive security headers and local static assets;
- acquired content is untrusted data;
- one mutable browser operation at a time unless concurrency is proven safe;
- no application/login automation, CAPTCHA/access bypass, proxy rotation, or autonomous recruiter messages;
- network/429/5xx/challenge/auth failures are **not** equivalent to an expired/removed vacancy;
- bounded sequential/rate-limited acquisition;
- raw valid evidence before downstream processing;
- search vocabulary is TOML data, not hard-coded career taxonomy.

## 11. Translation and inference rules

Trusted translation contracts:

```text
lm-studio-translation-v2
english-projection-v2
```

Source remains authoritative; English is derived.

For local long reasoning:

```text
connect timeout: bounded
read timeout after connection: none
write/pool: bounded
transport replay: disabled
max tokens: bounded
validation retries: bounded separately
```

Independent model roles are supported. The current experimental Blueprint model does not make Blueprint accepted.

Use controlled same-job comparison when model adequacy is genuinely the variable. Do not change evidence, contract, and model simultaneously. No multi-model voting unless future measured evidence justifies it.

Models may reason, synthesize, compare, classify, and recommend within the applicable contract. They must not manufacture source truth. Do not require deterministic equivalence for intrinsically semantic output solely to simplify testing.

## 12. Market and personal-evidence boundaries

The current implemented Market read model remains a bounded deterministic aggregate over accepted/current English P1.6. Preserve sample size, source/filter scope, requirement-strength semantics, contract identity, and concentration/small-sample warnings.

The future target-scoped Market / Role-Family responsibility is owner-approved but **not yet an active implementation stream**.

Current Market state:

```text
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
→ owner-approved direction / implementation gated

six bounded remote research passes
→ COMPLETE ENOUGH

docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md
→ research consolidated into DECIDED / PROVISIONAL / OPEN / DEFERRED

docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md
→ formal post-B1 Q1-Q12 investigation protocol PREPARED

formal foundation investigation
→ NOT STARTED / BLOCKED BY OPEN B1

Market-v2 implementation
→ NOT AUTHORIZED
```

While B1 remains open, do not start the formal Market foundation investigation or source implementation. The already-completed research/preparation records are design input only.

After B1 closes by PASS or evidence-based NO-PROMOTION / DEFER:

```text
load final B1 decision
→ load Market consolidation ledger
→ execute prepared Q1-Q12 foundation investigation
→ write one dated foundation decision
→ implement only if it explicitly states:
   FOUNDATION INVESTIGATION: PASS
   FIRST VERTICAL SLICE: AUTHORIZED
```

No second owner activation is required merely to start that already-approved post-B1 investigation.

Candidate Market subfamilies may be useful analytical interpretation without prior P2.2C/P2.2D promotion; stable reusable families/archetypes require their stronger promotion boundary.

Small samples may support bounded hypotheses or job-level interpretations with warnings. They do not support unqualified broad-market claims.

Do not implement durable personal readiness/gap/recommendation claims until a reviewed personal-evidence schema exists with depth, confidence, recency, evidence references, limitations, and AI-assistance/independence context.

Personal/private state must never be added to the public corpus merely because it lives in the same local database in a future phase.

## 13. Architecture-evolution discipline

- preserve the local modular monolith;
- keep SQLite until measured limits justify replacement;
- keep runtime authority separate from the versioned public corpus projection;
- implement a real second source before a generic source/plugin abstraction;
- use structured/keyword retrieval before embeddings/RAG;
- no graph/vector DB or autonomous agent orchestration without demonstrated query/product need and explicit privacy/provenance/budget controls.

## 14. Development and definition of done

- build coherent vertical increments;
- separate deterministic logic from network/model/provider calls;
- keep handlers thin and SQL focused;
- use typed config and versioned contracts;
- preserve historical artifacts;
- reconcile current-state docs when behavior materially changes;
- normal tests never contact Jobinja/Google/LM Studio;
- convert repeatable deterministic incidents into fixtures when possible;
- test high-blast-radius authority/persistence invariants strongly;
- do not overfit tests by forcing semantic/model outputs to become deterministic when the product question is inherently interpretive;
- avoid duplicate/manual validation that does not materially increase confidence in a consequential boundary.

An increment is done only when:

1. the intended workflow works;
2. applicable engineering quality gates pass;
3. source/state/privacy/provenance invariants hold;
4. analytical outputs communicate authority/uncertainty honestly;
5. live behavior is reviewed when the scope/impact justifies it;
6. failures remain bounded/inspectable;
7. docs match behavior;
8. no unrelated future scope is claimed; and
9. **the increment materially reduces user effort or improves the speed/quality of a real career-intelligence task.**

Do not ask the repository owner to rerun a completed gate merely because a transcript excerpt is incomplete when the owner has explicitly and credibly confirmed that gate passed. Record the evidence boundary accurately and continue.

Work directly on `main` unless the repository owner explicitly requests isolation or a concrete isolation need is agreed first.