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
9. the current active phase/focused plan
10. `docs/EXECUTION_TODO.md`
11. `docs/WORKING_MEMORY.md`
12. task-specific experiment/working-memory records, `corpus/README.md`, and selected review snapshots as needed.

Historical Phase-1 plans remain evidence/history, not automatic current execution gates after their scope is closed.

Proposal/experiment/working-memory files do not override controlling product, domain, source, architecture, reasoning-policy, roadmap, or implementation documents.

Authority:

```text
product/domain/source/architecture
→ utility/epistemic reasoning policy
→ roadmap
→ implementation plan
→ active phase/focused plan
→ execution TODO
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

Accepted/current opposite-end factual anchors:

```text
tG9K English P1.6 artifact 36 → Capability v9 artifact 11
t4jp English P1.6 artifact 37 → Capability v9 artifact 12
```

Capability v9 public promotion is closed and operationally verified. Normal public commands reuse artifacts 11/12 on P1.6 artifacts 36/37, Review Snapshot marks those chains current, and Blueprint remains non-current.

The public corpus is also operationally closed and remotely available. The accepted publication baseline is:

```text
known/discovered Jobinja jobs: 353
fetched/parsed detail jobs:      43
current English projections:     20
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Canonical Registry P2.1A deterministic persistence, P2.1B manual CLI review, P2.1C browser review, and P2.1D small real-data seed are all accepted. **P2.1 is closed.** The accepted P2.1D seed remains deliberately bounded to four concepts, one reviewed alias, five mapped decisions, and one explicit unmapped decision across the five accepted P1.6 chains. Registry publication remains unauthorized.

The 2026-08-26 governance reorientation is accepted through `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`. It preserves the strict Phase-1/P2.1 substrate while preventing future work from requiring promotion-grade proof for every low-blast-radius interpretation.

The controlling P2.2 plans are:

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md
```

P2.2A Job Work Intelligence v2 is **accepted and closed**. P2.2B-B1 is now **authorized only as a bounded responsibility-promotion evidence-selection pilot**. No responsibility promotion has occurred yet.

Current P2.2 state:

```text
P2.2A historical v1-v1.7 artifacts/attempts → preserved immutable evidence
P2.2A v2 schema                           → job-work-intelligence-v2
P2.2A v2 prompt/runtime                   → job-work-intelligence-v2.0
P2.2A representation implementation       → COMPLETE
P2.2A repository/live acceptance          → PASSED / CLOSED
P2.2B-B1                                  → EVIDENCE SELECTION / NO PROMOTION YET
```

The 2026-09-01 checkpoint verified that free-form model review did not reliably preserve action relationships across both `tG9K` and `tmyX`. Controlled v1.3-v1.7/2B/4B/12B trials remain immutable local evidence. The approved response is representation-level fact/interpretation separation, not another model-trial matrix.

Records:

```text
docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md
docs/working-memory/2026-09-01_P2_2A_V2_REPRESENTATION_IMPLEMENTATION.md
docs/working-memory/2026-09-01_P2_2A_V2_REAL_LOCAL_ACCEPTANCE.md
```

Do not reopen P1.6 v20, Capability v9, P2.1, or P2.2A merely for harmless non-authoritative wording variation. Reopen only for a repeatable material correctness/provenance/contract defect or a changed accepted dependency.

## 4. Blueprint disposition

Blueprint is implemented and inspectable but **is not an accepted Phase-1 decision layer**.

Historical v6/12B artifact 7 remains experimental evidence. Complete semantic review found assumption-bearing interpretation beyond vacancy authority even after mechanical provenance passed.

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

Phase 1, P2.1, and P2.2A are closed. P2.2B-B1 is authorized under the separate focused decision in:

```text
docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md
```

The P2.2A representation amendment remains controlling for Work Intelligence v2 behavior:

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
```

Current active gate:

```text
P2.2B-B1 selective responsibility promotion
→ focused plan APPROVED
→ evidence selection ACTIVE
→ no canonical responsibility promotion yet
→ P2.2C BLOCKED
```

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

Historical action-authority evidence:

```text
t4qV artifact 2
→ v1.1 candidate grouping useful and bounded

tmyX artifact 3
→ grouping useful
→ free-form summary strengthened `develop/provide hardening solutions` to `implementing`

tG9K artifact 4
→ useful industrial-ML grouping
→ 3 primary + 1 supporting
→ free-form action wording strengthened `move models toward production` to direct `deploying`

tG9K artifact 5
→ v1.2 remained useful
→ direct `deploying` persisted despite prompt-level authority refinement

artifacts 6-11
→ controlled v1.3-v1.7 model/protocol evidence
→ stronger/larger/free-form review still did not reliably preserve action relationship
```

Current exact next action:

```text
bounded local scan for one clean repeated accepted responsibility
→ prefer already-available current English evidence
→ if necessary, accept at most one additional evidence-bearing P1.6 job for this concrete recurrence question
→ present the exact two responsibility claims + proposed responsibility:<slug>
→ semantic review before any canonical mutation
→ only then apply one concept + two mappings
→ rerun/idempotency + CLI/browser/currentness/publication-boundary inspection
→ B1 PASS or evidence-based NO-PROMOTION / DEFER decision
```

The initially considered documentation pair is explicitly **not approved** for promotion because `t4qV` responsibility[9] is equipment-specific technical documentation while `tmyX` responsibility[3] is compound checklists + technical documentation + security reports. Do not normalize partial overlap into whole-claim equivalence merely to produce a promotion.

`tG9K`/`tmyX` already establish the P2.2A action-authority design defect. Do not run another prompt/model trial matrix merely to prove the same point.

P2.2 must **not** require manual canonicalization of every responsibility before useful role/work intelligence is shown.

During P2.2B-B1:

- do not bulk-map the remaining accepted P1.6 claim corpus;
- do not broaden the canonical ontology merely to eliminate unmapped cases;
- do not normalize partial semantic overlaps as whole-claim equivalence;
- do not broaden a concept merely to absorb compound claims;
- do not auto-promote P2.2A theme or deliverable labels;
- do not add deliverable mapping schema without concrete repeated-value evidence;
- do not publish canonical-registry or P2.2 state;
- do not start Market v2;
- do not add personal evidence/readiness/scoring/recommendations;
- do not create responsibility families/archetypes yet;
- do not make stable market-archetype claims from insufficient cross-job/employer evidence;
- do not add deterministic action-verb equivalence machinery;
- do not restore the v1.3 second semantic authority-review pass;
- do not impose a fixed quota of primary themes;
- do not ask the owner to rerun already-proven repository quality gates without new evidence requiring them.

Accepted P2.1D seed:

```text
canonical concepts: 4
reviewed aliases:   1
claim decisions:    6
  mapped:           5
  unmapped:         1
accepted chains:    5
```

P2.1 acceptance record:

```text
docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md
```

Current accepted heterogeneous factual order remains:

```text
1. Python/software             → tmBK P1.6 39 / Capability 13 ACCEPTED
2. network/security            → t4qV P1.6 44 / Capability 14 ACCEPTED
3. operations/platform/DevOps  → tmyX P1.6 46 / Capability 15 ACCEPTED
```

The accepted Python/software anchor is:

```text
tmBK — Python Developer
source detail version:       44
English projection artifact: 38
P1.6 contract:               job-analysis-english-v20 / job-analysis-v5
accepted P1.6 artifact:      39
accepted Capability artifact: 13
```

`tmBK` is closed and accepted after complete P1.6 and Capability review. Artifact 39 has 16 requirements, 0 responsibilities, correct 7/7 explicit depth facts, and accepted semantic-review state. Capability 13 covers 16/16 requirements and 7/7 explicit depth facts with no fabricated duties or role-level inflation.

The network/security anchor `t4qV` (detail 30, English projection 20) is accepted on P1.6 artifact 44 and Capability artifact 14. P1.6 artifacts 40-43 remain rejected/archived evidence. General deterministic fixes from those reviews cover:

- exact structured-skill tags materialized deterministically rather than model-restated;
- composite preferred headings retain their optionality in exact evidence;
- explicit experience lower bounds such as `more than six years` remain intact;
- explicit `position/role ... responsible for` clauses enter responsibility coverage;
- explicit pre-heading `we are looking/seeking ... with experience in ...` clauses enter requirement coverage.

The operations/platform anchor `tmyX` (detail 35, English projection 24) is accepted on P1.6 artifact 46 and Capability artifact 15. Artifact 45 was rejected for missing the explicit opening role actions. Its reviews additionally fixed:

```text
generic heading words inside ordinary sentences no longer split evidence
explicit pre-heading candidate duty clauses enter responsibility coverage
Ability to / Skill in application wording stays non-depth without real depth markers
```

Fresh English v20 artifacts are `pending` by default. Pending artifacts remain excluded from authoritative Capability/Market/accepted dashboard/public-corpus flows under the accepted Phase-1 contract. That strict promotion rule protects the reusable factual substrate; it must not be generalized into a rule that every future analytical view requires human acceptance first.

Do not rerun accepted factual anchors merely for wording variation. Phase-2 work must preserve the frozen P1.6 v20/v5 and Capability v9/v5 source-truth input contracts.

Convert repeatable deterministic defects into tests. Record bounded model limitations separately. Do not patch one vacancy at a time.

Accepted progression to the current point:

```text
Phase-1 closure accepted
→ P2.1 canonical concept registry accepted / closed
→ utility/epistemic reasoning governance corrected
→ P2.2 focused responsibility/work/role-intelligence plan approved
→ P2.2A Job Work Intelligence v1 implemented
→ t4qV/tmyX/tG9K live candidate evidence established
→ v1.2/v1.3 prompt/review refinements proved insufficient for action authority
→ v1.3-v1.7 cross-model/protocol trials preserved as local evidence
→ tG9K/tmyX cross-job free-form action-authority reliability blocker verified
→ P2.2A representation amendment approved
→ job-work-intelligence-v2 / v2.0 implemented
→ exact accepted P1.6 work injection + candidate interpretation separation implemented
→ second authority-review model pass removed
→ repository Ruff/full pytest/warnings-as-errors GREEN
→ t4qV/tmBK/reuse/browser/CLI real-local v2 acceptance PASSED
→ P2.2A CLOSED
→ P2.2B-B1 focused responsibility-promotion plan APPROVED
→ initial documentation pair REJECTED as lossy normalization
→ bounded evidence selection ACTIVE
```

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

Blueprint is experimental professional interpretation above historical accepted source truth. Its generated prose is not Phase-1 authority.

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
- project current successful English projection, P1.6, and Capability artifacts with exact dependency/contract identities;
- support remote AI review, heterogeneous selection, reproducibility, Market work, and later Phase-2 analysis without direct access to local SQLite.

The public corpus is a deterministic projection, **not** a runtime input and **not** a replacement database.

Current layout:

```text
corpus/manifest.json
corpus/jobs/<job-id>/source.json
corpus/jobs/<job-id>/english-projection.json
corpus/jobs/<job-id>/p16-english.json
corpus/jobs/<job-id>/p16-original.json
corpus/jobs/<job-id>/capability.json
```

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

The public corpus contains only public job-domain facts and repository-safe derived intelligence. Any future schema expansion must explicitly review this privacy/public boundary before adding fields.

Normal mutating CLI workflows and completed web background operations synchronize the local `corpus/` projection **after** durable SQLite work. Projection failure must be surfaced but must never roll back durable SQLite success.

JobHunter does **not** automatically Git commit or push. Publishing remains intentional:

```bash
jobhunter-corpus verify
git diff -- corpus/
git add corpus/
git commit -m "data: update JobHunter public corpus"
git push origin main
```

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

Snapshots are generated review artifacts, not runtime inputs. Commit selected public review examples intentionally. Dependency-current flags remain distinct from the explicit P1.6 semantic-review status/time/note.

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

Current Market aggregates accepted/current English P1.6 only. Preserve sample size, source/filter scope, requirement-strength semantics, contract identity, and concentration/small-sample warnings.

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