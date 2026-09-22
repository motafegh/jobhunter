# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product and engineering priority

JobHunter is a repeated-use **local-first personal career-intelligence application**. Its primary product objective is to help the user understand jobs, the market, career requirements, gaps, and actions **faster and better than manual vacancy-by-vacancy reading** while preserving trustworthy source/state boundaries.

Optimize for **useful, decision-relevant intelligence per unit of user time**, subject to source integrity, provenance, privacy, and honest uncertainty.

Do not confuse trustworthiness with maximal determinism. Deterministic machinery protects state, provenance, bookkeeping, exact counts, currentness, and reusable authority; semantic/model reasoning is an expected product capability for interpretation, synthesis, comparison, and recommendations when correctly labeled and traceable.

The mature product is not merely a scraper, generic matcher, semantic-audit laboratory, resume generator, or autonomous application bot.

---

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
10. the current active focused/implementation plan or decision
11. `docs/EXECUTION_TODO.md`
12. `docs/WORKING_MEMORY.md`
13. task-specific decision/experiment/working-memory records, `corpus/README.md`, and selected review snapshots as needed.

For the current Market implementation stream, load at minimum after the stable documents:

```text
docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md
docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md
docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md
docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md
```

The former Market foundation entry protocol and broad research consolidation are executed/history.
Load them only when a specific accepted design decision needs its earlier evidence.

Historical phase plans remain evidence/history after their scope closes. Proposal/experiment/working-memory files do not override controlling product, domain, source, architecture, reasoning-policy, roadmap, implementation, current-state, or current focused decision owners.

The dated current-state reconciliation is a **status-only overlay**: it supersedes obsolete present-tense status wording in older master/current documents but does not replace their durable product/architecture/roadmap semantics.

Authority:

```text
product/domain/source/architecture
→ utility/epistemic reasoning policy
→ roadmap
→ implementation plan
→ current-state reconciliation for present-tense status only
→ current focused plan/decision
→ execution TODO / working memory
→ implementation/tests/live acceptance
```

If artifacts conflict, reconcile them rather than choosing the convenient instruction.

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

Fail hard for integrity defects such as wrong/stale dependency identity, corrupt persistence, fabricated employer facts, unsupported source evidence, unsafe lifecycle transitions, privacy violations, invalid canonical mutations, or incorrect deterministic denominators.

Fail soft for interpretive uncertainty such as ambiguous role family, multiple plausible archetypes, incomplete technical scope, small analytical samples, or uncertain target membership.

Preferred interpretive behavior:

```text
uncertain
→ lower confidence / show alternatives / preserve unknowns / warn
→ still provide useful bounded interpretation when possible
```

Do not convert interpretive uncertainty into an infrastructure or review blocker merely because deterministic proof is unavailable.

---

## 3. Current implementation and acceptance state

Current accepted contracts:

```text
parser:                     jobinja-detail-v2
translation provider:       lm-studio-translation-v2
English projection:         english-projection-v2

English P1.6 public:        job-analysis-english-v21 / job-analysis-v5
Original P1.6 public:       job-analysis-original-v9 / job-analysis-v4

Capability public/current:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint experimental:     role-capability-blueprint-v6 / role-capability-blueprint-v5
Canonical Registry:         jobhunter-canonical-concept-registry-v1
Job Work Intelligence:      job-work-intelligence-v2 / job-work-intelligence-v2.0
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

Those five accepted anchor artifacts remain physically v20/v5 and are accepted-only compatibility inputs under the v21 current boundary. New English P1.6 generation uses v21/v5. Pending/rejected v20 candidates never satisfy v21 currentness, and exact artifact prompt/schema identity must remain visible when compatibility reuse occurs.

Current repository-safe public corpus:

```text
known/discovered Jobinja jobs: 394
fetched/parsed detail jobs:      51
current English projections:     27
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Current phase/product state:

```text
Phase 1                         CLOSED / ACCEPTED
P2.1 Canonical Registry        CLOSED / ACCEPTED
P2.2A Job Work Intelligence    CLOSED / ACCEPTED
P2.2B-B1                       CLOSED / NO-PROMOTION / DEFER
P2.2C promoted families        NOT ACTIVE / NOT AUTHORIZED
P2.2D stable archetypes        LATER / NOT AUTHORIZED
Blueprint                      EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation investigation PASS / COMPLETE
Market first vertical slice     I1-I6 ACCEPTED / I7 EXECUTED / HOLD
Market I1-I6                    REPOSITORY ACCEPTED / CLOSED
next exact increment            I7 HOLD closure follow-up
```

B1 final evidence is retained at:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

Do not reopen B1, select another responsibility pair, or force another `ta9l` P1.6 model/prompt matrix merely to manufacture a promotion. B1 created no responsibility concept/mappings.

Do not regenerate or reopen the accepted v20/v5 P1.6 anchor artifacts merely because v21 is now current; their accepted-only compatibility is intentional. Do not reopen Capability v9, P2.1, or P2.2A for harmless non-authoritative wording variation. Reopen only for a repeatable material correctness/provenance/contract defect or a changed accepted dependency.

---

## 4. Blueprint disposition

Blueprint is implemented and inspectable but **is not an accepted decision layer**.

Historical v6/12B evidence remains experimental. Complete semantic review found assumption-bearing interpretation beyond vacancy authority even after mechanical provenance passed.

Do not:

- create Blueprint v7 merely because later Market work needs interpretation;
- weaken Blueprint validators;
- add vacancy/domain-specific prompt patches merely to obtain a passing artifact;
- use Blueprint as Market, personal-readiness, automatic-recommendation, or other authoritative input;
- silently rebase historical Blueprint artifacts onto current Capability semantics.

Decision record:

`docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md`

This does **not** prohibit new bounded analytical interpretation under a new explicit contract.

---

## 5. Current exact next-work rule — Market first vertical slice

Formal foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Authorized first slice:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

Implementation order:

```text
I1  domain models + SQLite persistence          ACCEPTED
I2  target-scoped source eligibility / affected-work planning  ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate profile             ACCEPTED
I6  browser + CLI thin workflow                 ACCEPTED
I7  bounded local real acceptance + reuse rerun EXECUTED / HOLD
```

### 5.1 I7 exact boundary

I1-I6 have passed repository acceptance. Latest accepted implementation record:

`docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

I7 protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

I7 execution result:

`docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

I7 real-local execution has now occurred. The evidence supports the I1-I6 architecture, bounded
partial-success behavior, target-scoped progression/reuse, membership, privacy, and browser workflow,
but the acceptance outcome is **HOLD** rather than PASS. The live snapshots did not yet contain an
accepted-semantic core posting, so accepted P1.6 requirement/responsibility drill-down was not exercised
end to end. The 2026-09-19 follow-up recovered snapshot/profile 2, verified snapshot-1
historical immutability and SQLite integrity, and repaired rejection of pending P1.6 referenced
by a historical snapshot. Artifact 48 was reviewed and rejected for material semantic defects; historical
snapshot evidence was preserved. Continue only the bounded I7 closure follow-up recorded in the result file. Do not broaden
product scope or weaken semantic review to manufacture PASS.

The selected `tvMm` generation was executed once on 2026-09-20 local time and failed
validation (attempt 106); no candidate was persisted. A general v20 structured-skill
prompt/payload ownership contradiction was repaired with 639 passing tests and green
CI, but post-repair real-model acceptance is unproven. Before further generation,
follow the bounded evaluation decision boundary in
`docs/working-memory/2026-09-20_MARKET_I7_TVMM_BOUNDED_CLOSURE.md` rather than repeating
the historical selected-case command. I7 remains HOLD.

The bounded post-repair `tvMm` attempt 107 produced artifact 49, which was reviewed
and rejected for borrowed familiarity depth and candidate-versus-AI-system subject
misattribution. V20 now fails closed when multiple identical depth markers appear
in one broad evidence span. The 2026-09-20 closure record has the current evidence
and stop line; do not infer that the repair authorizes automatic acceptance or
unbounded model retries.

The remaining artifact-49 subject error was investigated across the 27 current
English projections. Four broad requirement coverage spans in two jobs cross
company-goal/application text, but the model-facing coverage already permits
exclusion and no safe universal cutoff was established. Keep I7 HOLD pending
representative source-backed section/subject design evidence or naturally available
valid accepted-semantic core evidence; do not select a substitute vacancy merely
to obtain PASS.

A bounded general evidence-span repair now keeps dependent `; to ...` wording
with its subject and ends requirement scope at an explicit `How to Apply:`
heading. All five accepted anchor plans were unchanged. This does not resolve
the model's full subject-attribution reliability or change I7 HOLD.

One bounded post-span-repair `tvMm` generation (attempt 108) failed after its
allowed retry on mixed-depth broad evidence citations. No candidate was created. The
depth guard was preserved, all Market tables matched the pre-run backup, and
SQLite integrity/foreign-key checks passed. This check is closed; do not repeat
`tvMm` or switch vacancy/model to force I7 PASS. Continue only from independent
evidence for a generalizable improvement or naturally available valid accepted-
current core semantic evidence. I7 remains HOLD.

The 27-projection offline audit and exact attempt-108 replay now show that v20's
broad coverage reference conflates omitted applicable familiarity with correct
null depth on neighboring experience claims; shared preferred wording is also
lost by naive item splitting. A separate explicit repeated-marker validator gap
was repaired with 642 passing strict-warning tests and read-only validation of
all five accepted anchors. The next general implementation is a versioned
candidate with separate exact item excerpts and parent coverage/obligation
context. That investigation produced v21, which is now the public/current English generation contract.
Keep the accepted v20/v5 artifacts as accepted-only compatibility inputs, preserve semantic review
and Market history, and keep I7 HOLD until the live accepted-semantic closure path passes.

### 5.2 First-slice settled rules

Permanent for this slice unless implementation evidence exposes a concrete contradiction:

```text
search/acquisition envelope
!= target membership truth
!= canonical role taxonomy
```

- reuse existing Jobinja source identity/provenance/lifecycle/observation machinery;
- reuse existing translation/P1.6 identities and currentness; no second cache/invalidation stack;
- target-run affected-work queues must be target-scoped rather than spending remaining bounded budgets on unrelated global backlog;
- source-level membership dispositions are `core_match / adjacent_match / uncertain / excluded`;
- current parsed source + title/English evidence may establish target membership before accepted P1.6 exists;
- accepted-current P1.6 is the authority boundary for strong P1.6-backed semantic prevalence, not a prerequisite for source-level membership;
- pending/missing/failed/rejected P1.6 must remain visible and never become zero demand;
- Capability and Work Intelligence are not mandatory first-slice dependencies;
- reviewed Registry mappings may enrich where available; unmapped facts remain valid;
- first-slice automatic repost/new-ID collapse is deliberately deferred for lack of defensible real evidence;
- call the denominator `qualified source postings`, not `unique demand units`;
- point-in-time snapshots are immutable historical authority;
- exact counts/shares/employer concentration/denominators are deterministic application responsibilities;
- Market state remains local/private by default.

### 5.3 First-slice stop lines

Do not during this slice:

- reopen B1 or force `ta9l` through another P1.6 matrix;
- auto-accept P1.6;
- make Capability/Work mandatory gates;
- implement automatic repost/new-ID collapse without real evidence;
- claim deduplicated `unique demand`;
- add model-generated/persisted Role-Family Intelligence Report yet;
- add semantic role-subfamily synthesis yet;
- start promoted P2.2C/P2.2D taxonomy;
- add trend / `emerging` / forecasting;
- add personal Market → You readiness/gap/scoring/recommendations;
- publish Market tables/profile into `corpus/`;
- add graph/vector/RAG/autonomous-agent orchestration or generic source/plugin infrastructure without demonstrated need.

Implementation completion is not pre-accepted. I7 must prove one bounded real target workflow after I1–I6 exist.

---

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

Recent B1 repairs strengthened source coverage/depth handling but do not authorize regeneration of accepted anchors without a real defect.

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

Permanent rules include:

- every capability-relevant accepted P1.6 requirement and responsibility must be covered;
- source indices/evidence must be valid and grounded;
- dense sources cannot collapse into one catch-all group;
- source requirement strength, source-explicit depth, and source work remain deterministic;
- role-level education/duration-only experience stay separate;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture claims are blocked/filtered;
- zero optional model enrichment is valid;
- deterministic reconciliation remains authority.

Capability model prose is not automatically downstream authority.

### Job Work Intelligence v2

Permanent authority rule:

> The model decides how accepted work is usefully organized; accepted P1.6 statements decide what factual work is actually asserted.

- accepted/current English P1.6 is factual authority;
- requirements may support interpretation but cannot manufacture duties;
- exact accepted work statements are deterministically injected;
- candidate themes/deliverables/role labels remain interpretation;
- no dedicated second semantic authority-review model pass;
- requirement-only jobs use the deterministic limited path;
- Work state remains local unless separately published.

### Analytical interpretation

Permitted when explicitly bounded:

- target-market semantic membership;
- job work-composition summaries;
- candidate cross-job work/responsibility groupings;
- candidate role archetypes/subfamilies;
- semantic comparisons and later recommendations after prerequisite evidence exists.

Never present interpretation as employer wording. Retain traceability and uncertainty where consequential. Promote to reusable authority only through the stronger applicable boundary.

---

## 7. Versioned public-corpus rules

Runtime authority remains local SQLite:

```text
data/jobhunter.sqlite3
```

Repository-safe public projection:

```text
corpus/
contract: jobhunter-public-corpus-v1
```

The public corpus is a deterministic projection, not a runtime input or replacement database.

It may contain public source jobs and explicitly approved current derived public artifacts. Optional stage files exist only when current for their source dependency.

Never export into `corpus/`:

- SQLite/WAL/SHM;
- machine-local evidence paths;
- raw HTML evidence;
- LM Studio request bodies/raw protocol responses;
- prompts/secrets/API credentials;
- logs/debug histories;
- local configuration;
- Market target/membership/snapshot/profile state under the current first-slice decision;
- future private/personal evidence, applications, notes, profiles, or outcomes.

Projection failure must be surfaced but must not roll back durable SQLite success.

JobHunter does not automatically Git commit/push. Publishing remains intentional.

Detailed rules: `corpus/README.md`.

---

## 8. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

```text
corpus/           complete current public dataset
review-snapshots/ selected semantic-review evidence
```

Snapshots are generated review artifacts, not runtime inputs. Commit selected public examples intentionally.

Never commit SQLite/WAL/SHM, raw model protocol/prompts, secrets, logs, raw HTML contents, or future private user state.

The tracked `jobhunter.toml` is public project configuration. Never place actual tokens/passwords/keys in it.

---

## 9. Record boundaries

Never conflate:

```text
JobPosting
SearchPageSnapshot
JobPostingVersion / job detail semantic version
JobDetailFetchObservation
JobLifecycle state/event
JobTranslationArtifact
JobAnalysisArtifact
Capability artifact
Role Blueprint artifact
JobUserWorkflow
Canonical Concept Registry
JobWorkIntelligenceArtifact
TargetMarket
TargetMarketDefinitionVersion
MarketResearchRun
MarketJobMembership
MarketCorpusSnapshot
MarketAggregateProfile
candidate analytical interpretation
promoted reusable semantic knowledge
Public Corpus projection
Review Snapshot
Raw evidence
```

Preserve provenance and exact dependency identity across every derived layer.

---

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
- network/429/5xx/challenge/auth failures are **not** equivalent to expired/removed vacancy;
- bounded sequential/rate-limited acquisition;
- raw valid evidence before downstream processing;
- search vocabulary is TOML data, not hard-coded career taxonomy.

---

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

Independent model roles are supported. No multi-model voting unless measured evidence justifies it.

Models may reason, synthesize, compare, classify, and recommend within the applicable contract. They must not manufacture source truth or deterministic counts. Do not demand deterministic semantic equivalence solely for test convenience.

---

## 12. Market and personal-evidence boundaries

The old global `MarketInsights` remains a bounded deterministic read model over accepted/current English P1.6 and is useful implementation precedent; it is not the final target-scoped Market contract.

The target-scoped Market first slice is now authorized. Its formal decision is the 2026-09-14 foundation record.

Core denominator separation:

```text
qualified core source postings
!=
qualified core postings with accepted-current P1.6
```

Use source-level facts only where the exact source denominator supports them. Use P1.6 requirement/responsibility statistics only over the accepted-current semantic sub-denominator. Expose missing/pending/failed coverage.

Small samples may support bounded hypotheses or job-level interpretations with warnings. They do not support unqualified broad-market claims.

Do not implement durable personal readiness/gap/recommendation claims until a reviewed personal-evidence schema exists with depth, confidence, recency, evidence references, limitations, and AI-assistance/independence context.

Personal/private state must never enter the public corpus merely because it lives in the same local database.

---

## 13. Architecture-evolution discipline

- preserve the local modular monolith;
- keep SQLite until measured limits justify replacement;
- keep runtime authority separate from the versioned public corpus projection;
- implement a real second source before a generic source/plugin abstraction;
- use structured/keyword retrieval before embeddings/RAG;
- no graph/vector DB or autonomous-agent orchestration without demonstrated product/query need and explicit privacy/provenance/budget controls;
- prefer a thin target-aware coordinator over a workflow framework;
- extract neutral shared helpers from versioned modules only when a concrete maintenance/replay need justifies it, not as unrelated cleanup during Market implementation.

---

## 14. Development and definition of done

- build coherent vertical increments;
- separate deterministic logic from network/model/provider calls;
- keep handlers thin and SQL focused;
- use typed config and versioned contracts;
- preserve historical artifacts;
- reconcile current-state docs when behavior materially changes;
- normal tests never contact Jobinja/Google/LM Studio;
- convert repeatable deterministic incidents into fixtures when practical;
- test high-blast-radius authority/persistence invariants strongly;
- do not overfit tests by forcing semantic/model outputs to become deterministic when the product question is inherently interpretive;
- avoid duplicate/manual validation that does not materially increase confidence in a consequential boundary.

An increment is done only when:

1. the intended workflow works;
2. applicable engineering quality gates pass;
3. source/state/privacy/provenance invariants hold;
4. analytical outputs communicate authority/uncertainty honestly;
5. live behavior is reviewed when scope/impact justifies it;
6. failures remain bounded/inspectable;
7. docs match behavior;
8. no unrelated future scope is claimed; and
9. **the increment materially reduces user effort or improves the speed/quality of a real career-intelligence task.**

Do not ask the owner to rerun a completed gate merely because a transcript excerpt is incomplete when the owner has explicitly and credibly confirmed that gate passed. Record the evidence boundary accurately and continue.

Work directly on `main` unless the repository owner explicitly requests isolation or a concrete isolation need is agreed first.
