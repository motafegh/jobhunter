# Market / Role-Family Foundation Investigation Decision

**Date:** 2026-09-14  
**Status:** FOUNDATION INVESTIGATION PASS / FIRST VERTICAL SLICE AUTHORIZED  
**Branch:** `main`  
**Controlling parent:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Entry protocol:** `docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`  
**Research consolidation:** `docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`  
**B1 input:** `docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

## 1. Decision

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

The first implementation slice is deliberately narrow:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow over the same services/state
```

This decision authorizes implementation of that slice only.

It does **not** authorize:

- a model-generated/persisted Role-Family Intelligence Report yet;
- candidate role-subfamily synthesis in the first slice;
- promoted P2.2C responsibility families or P2.2D stable archetypes;
- automatic repost/new-ID collapsing;
- trend, `emerging`, forecasting, or longitudinal claims;
- personal `Market → You` readiness/gap/scoring;
- Market state publication into `corpus/`;
- a new workflow/orchestration framework, vector store, graph store, or generic source plugin system.

The implementation must remain a bounded extension of JobHunter's existing local modular monolith and SQLite authority model.

---

## 2. Exact first-slice product question

For one user-defined target market, JobHunter should be able to answer:

> Which currently evidenced Jobinja postings genuinely belong to this target, what trustworthy source/accepted-semantic evidence is available for them, and what recurring requirements and factual work can be aggregated across that qualified corpus without hiding missing analysis coverage or overstating the sample?

The first slice is successful when the user can define/select a target, run or refresh it incrementally, inspect the qualified corpus and processing ledger, receive a deterministic aggregate profile with explicit denominators/warnings, and drill down to the underlying jobs/evidence.

This is online-job-ad intelligence from a bounded evidence corpus, not a claim to represent the complete labour market.

---

## 3. Evidence boundary of this investigation

This decision uses:

- the current repository architecture and tests;
- the versioned public Jobinja corpus;
- the five accepted heterogeneous P1.6 anchors;
- the completed B1 `ta9l` local execution/recovery evidence;
- the existing search/config, acquisition, lifecycle, translation, P1.6, Work, Registry, current Market and browser-operation owners;
- the six completed Market research passes and their consolidation ledger.

No new live Jobinja acquisition run was performed by this investigation session. Therefore this record does **not** claim an optimized search-recall policy or a measured real repost/new-ID classifier. Those two items are deliberately bounded below rather than guessed.

B1 is particularly important evidence for first-slice design: `ta9l` is clearly source-level relevant to an applied-AI market and has a reviewed current English projection, while accepted-current P1.6 remains unavailable after bounded failures/rejection. Therefore source-level market membership and strong P1.6-backed semantic prevalence must be separate denominators.

---

# 4. Q1–Q12 decisions

## Q1 — Smallest target-definition contract

### Decision

Use two identities:

```text
TargetMarket
→ stable user-recognizable target identity

TargetMarketDefinitionVersion
→ immutable exact meaning/acquisition definition used by a run/snapshot
```

### `TargetMarket` minimum responsibility

Store only stable logical identity and ordinary lifecycle/display information:

```text
id / stable slug
name
description or short user-facing intent
created_at
optional archived/active state if later needed
```

Do not place mutable search details directly on the stable target row.

### `TargetMarketDefinitionVersion` first-slice fields

The immutable definition should represent:

```text
target_market_id
definition version / semantic fingerprint
human-readable membership intent
approved source: Jobinja
search-catalog version
selected search profile references
selected search pack references
bounded custom/extra search terms when used
bounded raw approved search definitions/URLs when used
include work/role hints
exclude work/role hints
geography scope when specified
work-arrangement scope when specified
seniority/experience scope when specified
employment-type scope when specified
freshness/time-window rule
created_at
```

Search vocabulary remains an acquisition envelope, not membership truth.

### Run controls, not target semantic identity

Keep these as exact `MarketResearchRun` inputs rather than definition meaning:

```text
request/page budget
detail missing/refresh budget
refresh-after threshold
translation batch budget
P1.6 batch budget
provider/model selections actually used
```

They must be recorded for reproducibility, but changing an operational budget must not silently create a different logical market definition.

If future evidence proves a particular acquisition bound materially changes the intended semantic scope, version the target definition explicitly rather than inferring that from a generic run budget.

---

## Q2 — Target-run orchestration and reuse

### Decision

Add one thin target-aware coordinator, provisionally `MarketResearchService`, that composes existing owners.

Preferred flow:

```text
definition version
→ expand bounded configured Jobinja searches
→ discovery using existing source identity/provenance
→ derive target candidate source_job_ids
→ target-scoped missing/refresh detail selection
→ existing detail fetch/version/lifecycle/observation machinery
→ target-scoped translation affected-work selection
→ target-scoped P1.6 affected-work selection
→ membership qualification
→ snapshot
→ deterministic aggregate profile
```

Do not create a second acquisition stack, artifact cache, invalidation engine, or workflow framework.

### Important difference from `Phase1RunService`

`Phase1RunService` is a strong composition precedent, but its missing/refresh/model queues are global with preferred IDs. For Market, preferred target IDs are not enough: a bounded target run must not spend its remaining budget on unrelated global missing jobs.

Therefore the first slice needs target-scoped selection at the coordinator/store-query boundary. Reuse the underlying services and identities; do not reuse global queue semantics where that would violate target scope.

### Partial success

Persist/expose a run ledger that can distinguish at least:

```text
requested / candidate
eligible
attempted
completed
reused
failed
pending-review
remaining
```

One failed fetch, translation, P1.6 generation or semantic classification does not erase successful durable work.

---

## Q3 — Source-level snapshot eligibility

### Decision

A posting may enter source-level market membership evaluation only when it has a current successfully parsed source detail version. Missing-detail discoveries remain candidates/backlog, not qualified snapshot members.

Lifecycle handling for an active-market snapshot:

```text
active
→ eligible subject to target freshness/membership

possibly_unavailable
→ may remain eligible with an explicit availability/freshness warning when a sufficiently recent valid parsed source version exists

expired
→ exclude from the current-active primary corpus; preserve historical evidence

removed
→ exclude from the current-active primary corpus; preserve historical evidence

rate_limited / access_denied / challenge / auth_required /
server_error / network_error / unexpected_page / unknown_error
→ a failed/retryable refresh is not disappearance; retain prior valid evidence subject to freshness policy and expose the warning
```

This directly preserves the existing lifecycle rule that weak fetch failure cannot become vacancy disappearance.

### Source-version change

A new semantic source version invalidates reuse of membership decisions whose dependency identity names the prior version. It does not mutate old snapshots.

### Freshness

The first implementation must define one deterministic freshness rule from available posting/source timestamps and the definition's requested window. Do not invent a trend model. Snapshot metadata must expose the effective rule.

---

## Q4 — Target-market membership evidence

### Decision

Use staged membership:

```text
1. deterministic eligibility
2. bounded semantic role/work relevance when necessary
```

First-slice dispositions are confirmed as:

```text
core_match
adjacent_match
uncertain
excluded
```

### Lowest sufficient evidence

The first-slice semantic membership boundary is:

```text
current parsed source detail + title
+ current English projection when source language/semantic reasoning needs it
+ accepted-current P1.6 opportunistically when available
```

Accepted P1.6 is **not** a prerequisite for source-level membership.

Capability and Work Intelligence are not required membership dependencies in v1.

### Membership artifact identity

A reusable semantic membership decision must record/identify:

```text
target definition version
source job identity
exact source detail version
membership classifier contract/version
model/prompt/schema identity when a model is used
exact English/P1.6 artifact IDs actually consumed, if any
disposition
short reason / evidence references
qualitative confidence if the contract uses it
created/reviewed/corrected state as applicable
```

Do not imply that absence of P1.6 means weak source-level relevance.

### Primary corpus rule

The primary target corpus is `core_match` only.

`adjacent_match` and `uncertain` remain visible separately. `excluded` remains traceable but outside the primary denominator.

---

## Q5 — P1.6 acceptance coverage at Market scale

### Decision

One immutable snapshot preserves the qualified source-level corpus and exact processing state. Do not create separate snapshots merely because semantic processing is incomplete.

Every report/profile must expose, for the primary core corpus:

```text
core source postings
core + accepted-current P1.6
core + pending P1.6
core + missing/no-current P1.6
core + failed/rejected current processing where applicable
```

### Denominator rules

```text
source-level corpus / employer / geography / lifecycle facts
→ denominator = qualified core source postings with the required exact source field

P1.6 requirement/responsibility prevalence
→ denominator = qualified core postings with accepted-current P1.6 under the declared contract
```

Pending/missing/failed P1.6 cannot enter the accepted semantic denominator.

A missing or failed P1.6 artifact must never be treated as `zero requirements` or `zero responsibilities`.

### Throughput policy

Allow target-aware prioritization of generation/review backlog, but do not auto-accept P1.6 to increase sample size.

The `ta9l` B1 result is the concrete boundary case: source-level membership can be clear while accepted-semantic coverage remains incomplete.

---

## Q6 — Jobinja repost/new-ID policy

### Decision for first slice

Automatic repost/new-source-ID collapsing is **deferred** because this investigation does not have a defensible bounded real Jobinja pair set from which to establish an authority rule.

Do not invent a similarity threshold.

What is already safe:

- repeated observations of the same stable `source_job_id` remain one source posting;
- all source advertisements remain preserved;
- employer breadth/concentration remains visible.

### First-slice denominator language

Use:

```text
qualified source postings
```

Do **not** call the first-slice denominator `unique demand units`.

Every profile must state that repost/new-ID adjustment is not implemented. Therefore the first slice must avoid strong deduplicated-demand or longitudinal claims.

A later bounded repost investigation may introduce explicit `same_demand / separate / uncertain` relationships after real evidence exists.

No global duplicate ontology is justified now.

---

## Q7 — Minimum persistence model

### Decision

First-slice runtime persistence should use SQLite and the following conceptual tables/owners:

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

No `role_family_intelligence_reports` table is required until nondeterministic semantic report synthesis is introduced.

### Mutability/history

```text
Market target
→ stable identity; ordinary display/lifecycle metadata may evolve

Target definition version
→ immutable

Research run
→ operational record: running → terminal; never semantic authority

Membership
→ immutable/reusable semantic decision keyed by exact dependencies; correction creates a new effective decision/history rather than silently rewriting old snapshots

Snapshot + members
→ immutable historical authority

Aggregate profile
→ immutable deterministic derivative of one exact snapshot + aggregate contract
```

### Minimum dependency walk

**Unchanged rerun**  
Reuse current source/translation/P1.6 and exact membership decisions where dependencies match; create a new run and, when requested, a new point-in-time snapshot/profile without re-inference merely for repetition.

**New source semantic version**  
Keep old snapshot; recompute membership for the changed source version; upstream translation/P1.6 follow their existing currentness identities.

**New target definition version**  
Do not invalidate source/translation/P1.6. Recompute membership/snapshot/profile for the new target meaning.

**New membership contract/model**  
Source/translation/P1.6 remain valid; create/recompute membership and downstream snapshot/profile.

**New aggregate contract**  
Snapshot remains valid; create a new aggregate profile over the exact snapshot.

### Storage rule

Store exact foreign/dependency identities, not copied source/P1.6 payloads.

---

## Q8 — First deterministic aggregate profile

### Decision

The first `MarketAggregateProfile` should contain only deterministic values that are already justified by source/snapshot/P1.6 authority.

### Evidence-quality/header section

Include:

```text
target + definition version
snapshot/run identity and time
source/search scope
candidate/source-eligible counts
core / adjacent / uncertain / excluded counts
qualified core source postings
accepted / pending / missing-or-failed P1.6 coverage
raw source posting count
repost adjustment status
number of distinct employers
largest-employer contribution/share
freshness/lifecycle warnings
processing failures/backlog
```

### P1.6-backed requirement rows

For accepted-current P1.6 core members:

```text
concept
concept_type
supporting posting count
share with explicit denominator
required / preferred / contextual / inferred support counts
distinct employer support
source-explicit depth-signal distribution where useful
evidence/job/artifact drill-down references
```

One posting may support one concept at most once in the concept-support count. Strength columns may remain non-exclusive when one posting genuinely states the same normalized concept at different strengths, with the disclosure preserved.

### Work/responsibility section

Expose accepted responsibility/work evidence and counts/drill-down without inventing cross-job family equivalence.

Reviewed Canonical Registry mappings may enrich/merge a concept where available. Unmapped evidence remains visible.

Do not introduce a model-generated clustering layer merely to make a cleaner first report.

### Source-level context

Aggregate exact normalized source facts such as geography, employment type, experience and education only where denominator/normalization semantics are explicit.

### Explicitly excluded from v1 profile

- opaque importance scores;
- `core/common/specialized` bands;
- emerging/trend labels;
- forecast values;
- model-authored counts;
- candidate subfamily prevalence presented as fact.

---

## Q9 — Capability / Work Intelligence dependency

### Decision

Neither Capability Intelligence nor Work Intelligence is a mandatory first-slice dependency.

Reason:

- accepted P1.6 is already the factual substrate for strong requirement/responsibility statistics;
- current Capability/Work coverage is much smaller than the full source corpus;
- making either layer mandatory would unnecessarily reduce usable Market coverage and add model cost/currentness dependencies.

Use reviewed Canonical Registry mappings opportunistically when they exist.

Capability and Work may become optional enrichments in a later slice if a measured product question demonstrates value.

---

## Q10 — Semantic role-subfamily synthesis placement

### Decision

Defer semantic role-subfamily synthesis from the first implementation slice.

The deterministic first profile already provides useful product value:

- explicit target corpus;
- honest processing coverage;
- recurring requirement demand over accepted P1.6;
- factual responsibilities/work drill-down;
- employer breadth/concentration;
- transparent missing evidence.

After the deterministic slice is accepted on a bounded real target run, add one bounded **report-level** semantic synthesis only if user value requires it.

When introduced later, candidate subfamily reasoning should be based primarily on recurring accepted work/responsibilities and requirement/capability bundles, with titles as supporting evidence. It remains candidate interpretation, not P2.2C/P2.2D promotion.

Do not generate one semantic narrative per job and then summarize those narratives.

---

## Q11 — Smallest coherent browser/CLI workflow

### Browser — primary

Use shared services for a workflow approximately:

```text
Targets
→ create/select target
→ create a new immutable definition version when meaning changes
→ preview acquisition scope and run budgets
→ run/refresh in the existing single-mutable-operation model
→ inspect run partial-success ledger
→ inspect membership breakdown / evidence / uncertainty
→ inspect frozen snapshot + deterministic aggregate profile
→ drill down to source job / exact semantic evidence
→ inspect prior target runs/snapshots
```

A target definition edit must create a new version rather than silently changing historical meaning.

The existing web operation manager is the correct concurrency shape: one mutable operation at a time, terminal `completed` / `completed_with_failures`, with inspectable summaries/links.

Market state remains local. Existing public-corpus synchronization may continue to publish only upstream repository-safe artifacts already governed for publication; Market target/membership/snapshot/profile tables must not be exported by default.

### CLI — secondary

Expose the same underlying services for inspection/automation/debugging. Exact command spelling is an implementation detail, but responsibilities should cover:

```text
target list/show/create-version
market run/refresh
run show
membership/snapshot/profile inspection
```

Do not create a second CLI-only behavior path.

---

## Q12 — First-slice implementation acceptance gate

Implementation is accepted only after all applicable deterministic/service/browser/CLI tests pass and one small real local target run validates the product path.

Minimum invariants:

1. `TargetMarket` identity remains stable while changed meaning creates a new immutable definition version.
2. Changing only target meaning never invalidates generic source/translation/P1.6 artifacts.
3. Re-running unchanged upstream dependencies reuses them rather than rebuilding the corpus.
4. Target-scoped runs do not spend bounded detail/model budgets on unrelated global backlog.
5. Failed refresh is never interpreted as disappearance.
6. Removed/expired state does not mutate historical snapshots.
7. `excluded`, `adjacent_match` and `uncertain` cannot silently enter the core denominator.
8. `uncertain` is a valid successful semantic disposition.
9. Missing/pending/failed P1.6 is exposed and cannot be counted as zero semantic demand.
10. Only accepted-current P1.6 contributes to P1.6-backed semantic statistics.
11. One qualified posting contributes at most once to one concept-support count.
12. Every reported share exposes/recoverably identifies its denominator.
13. Employer breadth/concentration is deterministic and warned appropriately.
14. Snapshot members reference exact source/membership/semantic dependency identities.
15. A snapshot remains immutable after source, target or contract changes.
16. Aggregate profile references one exact snapshot and deterministic contract version.
17. No first-slice metric claims repost-adjusted `unique demand` while new-ID dedup is deferred.
18. One stage failure produces a bounded partial-success result rather than erasing prior durable success.
19. Browser and CLI operate over the same service/state owners.
20. Ordinary CI uses deterministic fixtures/fake providers and never requires Jobinja or LM Studio.
21. A very small local real target smoke is required before implementation acceptance, specifically to verify acquisition bounds, reuse, membership inspection, denominator display and evidence drill-down.
22. Market state remains local/private unless a separate publication decision is made.

The real local smoke is an implementation acceptance requirement, not a reason to block source implementation now.

---

# 5. Bounded investigation experiments / evidence results

## E1 — Target/search contract

**Result: sufficient to authorize the contract; live recall optimization deferred to implementation acceptance.**

The packaged search catalog already provides bilingual, versioned profiles/packs for AI/ML, LLM applications, security and platform roles. `Settings` already supports profiles, packs, custom keyword groups, raw approved URLs, exclusions and request/page budgets.

Representative first implementation target for acceptance may use an **Applied AI / ML Engineering** or similarly coherent AI target with the existing `ai-focused` acquisition envelope. The product/domain contract does not require creating a new hard-coded career taxonomy.

No claim is made that one current profile has optimal recall. The local real acceptance run must expose discovered candidates/noise and validate the run bounds.

## E2 — Membership boundary set

Repository-safe cases demonstrate why membership must use actual work/evidence rather than title equality:

| Job | Evidence shape | Applied AI / ML Engineering disposition for the representative case | Why |
| --- | --- | --- | --- |
| `ta9l` | Senior Applied AI Engineer; semantic/RAG/agents/retrieval/evaluation/text-to-SQL | `core_match` | Direct AI system engineering work; accepted P1.6 unavailable but source evidence is strong. |
| `tG9K` | AI/ML semiconductor models, pipelines, validation/monitoring, production/governance | `core_match` | Clear applied ML engineering; accepted P1.6 strengthens downstream statistics. |
| `tGM0` | Python/backend engineer in AI team; LLM/agent integration and AI workflow infrastructure | `adjacent_match` | Genuine AI-adjacent platform/backend work, but role center is backend infrastructure for this target definition. |
| `t4jp` | Title says AI specialist; actual evidence is AI-assisted content/video/social/web work | `excluded` | Concrete title-keyword false positive; title alone would be unsafe. |
| `tmBK` | Python/Django/FastAPI role; AI appears as a software-development usage qualification | `excluded` | AI usage requirement does not make the job an AI engineering role. |
| `t4qV` | Senior network security architecture/firewall/VPN/Zero Trust work | `excluded` | Security engineering, not the representative applied-AI target. |
| `tmyX` | Microsoft infrastructure hardening/security/PowerShell work | `excluded` | Infrastructure security, not applied AI/ML engineering. |

This is a boundary-evidence set, not a statistical accuracy benchmark.

It confirms:

- title-only membership is unsafe;
- source work can establish clear membership before accepted P1.6 exists;
- accepted P1.6 is valuable for strong semantic aggregation but should not gate source-level membership;
- `adjacent_match` is useful for genuine neighboring work without contaminating the core denominator.

## E3 — Repost/new-ID evidence

**Result: insufficient real evidence for an authority rule; explicitly deferred.**

No credible bounded repo-safe Jobinja pair was established during this investigation. The correct outcome under the entry protocol is therefore no automatic new-ID collapse in v1, explicit disclosure, and conservative claims.

## E4 — P1.6 coverage/backlog boundary

**Result: directly evidenced by current stores and B1.**

The existing analysis store already represents completed/failed/reused attempts, pending/accepted artifacts and rejected archives. B1 adds a real target-relevant case with reviewed source/English evidence but no accepted P1.6 after bounded failures.

Therefore the first slice must preserve useful source-level intelligence while separately reporting accepted-semantic coverage. No auto-acceptance mechanism is justified.

## E5 — Minimal schema/dependency walk

**Result: relational shape above is sufficient for the first slice.**

Existing SQLite owners already use stable source identities, immutable semantic versions, operational runs, exact foreign dependencies, currentness checks and append/preserve history. The proposed seven Market table responsibilities fit that model without a new persistence system.

The dependency walk in Q7 proves that target changes do not require rebuilding unrelated upstream artifacts and historical snapshots need never be rewritten.

## E6 — First deterministic report/read-model

**Result: sufficient product basis to authorize implementation; real repeated-use acceptance still required.**

Current `MarketInsights` already demonstrates deterministic concept counts, requirement strength separation, discovered/parsed/analyzed coverage, distinct-employer concentration warnings and explicit duplicate limitations. The first target-scoped profile extends those proven responsibilities with exact target/snapshot membership and per-section denominators rather than replacing them.

This is enough to establish that a deterministic profile can answer useful first questions before semantic role-subfamily narrative exists.

The bounded real implementation acceptance run must still confirm that the complete target workflow is useful and inspectable in the browser.

---

# 6. First implementation order

Implement as bounded increments inside the authorized slice:

```text
I1  domain models + SQLite persistence
    TargetMarket / DefinitionVersion / Run / Membership / Snapshot / Profile

I2  target-scoped source eligibility + affected-work planning
    reuse existing discovery/detail/translation/P1.6 owners

I3  membership qualification contract/service
    deterministic eligibility + bounded semantic relevance

I4  immutable snapshot construction
    exact member/dependency identities + processing coverage

I5  deterministic target aggregate profile
    explicit denominators / employer breadth / requirement strength / drill-down

I6  browser + CLI thin workflow
    same services/state; operation ledger + evidence navigation

I7  bounded local real acceptance
    one representative target + reuse rerun + failure/coverage inspection
```

Do not collapse these into one large speculative implementation if smaller vertical increments can remain usable and testable.

---

# 7. Implementation-specific test matrix

## Deterministic/store tests

Cover at minimum:

- target/definition uniqueness and immutability;
- definition semantic fingerprint stability;
- run terminal states/ledger counts;
- exact membership dependency identity and reuse;
- source-version invalidation of membership only where appropriate;
- target-version change without upstream invalidation;
- snapshot immutability and exact member identities;
- aggregate exact snapshot dependency;
- one-posting-per-concept support counts;
- core/adjacent/uncertain/excluded denominator isolation;
- employer concentration;
- missing/pending/accepted semantic coverage;
- no repost-adjusted claim in v1.

## Service integration tests with temporary SQLite

Cover:

- unchanged rerun reuse;
- changed source semantic version;
- failed refresh with prior valid evidence;
- explicit removal/expiry;
- translation missing/failure/reuse;
- P1.6 accepted/pending/missing/failure;
- one unrelated global-backlog item proving target run does not consume its budget;
- partial-success snapshot/profile construction when integrity permits it.

## Semantic membership boundary tests

Use fake/fixture outputs and representative evidence shapes. Protect:

- clear core;
- non-obvious core;
- adjacent;
- misleading title/keyword exclusion;
- hybrid;
- sparse/uncertain;
- no false certainty from missing P1.6.

Do not assert exact prose labels beyond the typed/disposition/evidence contract.

## Browser/CLI

Verify:

- target definition/version display;
- run start/busy/terminal state;
- partial-success ledger;
- membership breakdown;
- aggregate denominator/warnings;
- evidence drill-down;
- rerun/reuse visibility;
- no Market publication side effect.

---

# 8. Stop lines for implementation

During the authorized first slice:

- do not reopen B1 or search for another responsibility pair;
- do not force `ta9l` through another P1.6 model/prompt matrix;
- do not make Capability/Work mandatory Market prerequisites;
- do not auto-accept P1.6;
- do not introduce automatic repost/new-ID collapsing;
- do not call the source-posting denominator `unique demand`;
- do not add trend/emerging/forecast logic;
- do not add stable subfamily/archetype promotion;
- do not add personal evidence/readiness/scoring;
- do not publish Market tables/profile to the repository-safe corpus;
- do not add graph/vector/RAG/agent orchestration infrastructure;
- do not add a generic second-source abstraction before a real approved second source exists;
- do not broaden the first slice merely because the future plan contains later responsibilities.

---

# 9. Consequence of B1 NO-PROMOTION / DEFER

B1 closure does not block Market work.

The first Market slice deliberately does not require promoted cross-job responsibility families. It may aggregate exact accepted P1.6 facts and reviewed Registry mappings where available while keeping unmapped facts visible.

The B1 result instead strengthens two first-slice requirements:

1. source-level target membership must remain useful when accepted P1.6 is unavailable;
2. semantic coverage/backlog must be visible so missing analysis is never misreported as absence of demand/work.

No canonical `responsibility:design-ai-evaluation-monitoring` concept was created by B1, and this Market authorization does not create or imply one.

---

# 10. Final authorization

The foundation integrity questions needed to begin implementation are resolved strongly enough:

- source identity/provenance remain existing authority;
- target meaning/version boundaries are explicit;
- affected-work reuse/invalidation is explicit;
- source eligibility and failure semantics are explicit;
- membership semantics and denominator isolation are explicit;
- P1.6 accepted/pending/missing boundaries are explicit;
- repost adjustment is honestly deferred rather than guessed;
- the minimal SQLite persistence model is bounded;
- deterministic profile ownership/denominators are explicit;
- Capability/Work and semantic synthesis are intentionally not first-slice gates;
- browser/CLI share one service/state path;
- acceptance and publication boundaries are explicit.

Therefore:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
NEXT PRODUCT ACTION: IMPLEMENT I1, THEN CONTINUE THE AUTHORIZED SLICE IN BOUNDED INCREMENTS
```

Implementation completion is not pre-accepted. The real local target run and full first-slice acceptance matrix remain required before the slice can be called closed.
