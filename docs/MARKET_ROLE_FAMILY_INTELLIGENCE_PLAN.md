# JobHunter Market and Role-Family Intelligence Plan

**Status:** CURRENT / CONTROLLING PRODUCT PLAN — FOUNDATION PASS / I1-I6 REPOSITORY ACCEPTED / I7 LOCAL ACCEPTANCE OPEN
**Original date:** 2026-09-06  
**Last reconciled:** 2026-09-18
**Branch:** `main`  
**Scope:** Target-scoped market refresh → qualified evidence corpus → deterministic aggregate intelligence → later bounded semantic role-family synthesis/history → later reviewed personal comparison

## 1. Current execution decision

The former P2.2B-B1 gate is closed as **NO-PROMOTION / DEFER**. The formal Market foundation investigation has been executed and passed.

Final foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Research consolidation:

`docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Current implementation order:

```text
I1  domain models + SQLite persistence          ACCEPTED
I2  target-scoped source eligibility / affected-work planning  ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate profile             ACCEPTED
I6  browser + CLI thin workflow                 ACCEPTED
I7  bounded local real acceptance + reuse rerun ← NEXT
```

This plan controls the long-term Market direction and the first vertical slice. I1-I6 are repository-accepted, but end-to-end first-slice completion remains **not accepted** until I7 real local evidence passes. The prepared I7 protocol is `docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`.

---

## 2. Product purpose

JobHunter must let the user ask for a current view of a target job market and receive **one evidence-backed aggregate intelligence view across the relevant postings**, rather than manually reading or receiving one report per vacancy.

Representative intent:

```text
Update the market for AI Security / ML Security roles,
process the relevant current advertisements,
and show what this market actually asks people to know and do.
```

The mature capability should eventually:

1. define/version the target market;
2. discover/refresh relevant approved-source postings;
3. reuse/build required current derived artifacts;
4. qualify which postings genuinely belong;
5. freeze a reproducible qualified corpus snapshot;
6. aggregate requirements, responsibilities, tools, knowledge, practices, experience and context;
7. optionally synthesize bounded candidate work/role subfamilies without presenting inference as employer fact;
8. render one Role-Family Intelligence Report;
9. preserve comparable versioned history;
10. later compare objective Market evidence with reviewed personal evidence.

Long-term product chain:

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ ACTION
```

Job acquisition is an input subsystem. The value is trustworthy synthesis.

---

## 3. Authority model

This plan is subordinate to:

```text
docs/PRODUCT_SPECIFICATION.md
docs/DOMAIN_AND_ANALYSIS_MODEL.md
docs/SOURCE_POLICY.md
docs/ARCHITECTURE.md
        ↓
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
        ↓
docs/ROADMAP.md
docs/IMPLEMENTATION_PLAN.md
        ↓
docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md
        ↓
this plan + current foundation decision
```

Preserve JobHunter's four epistemic levels:

```text
SOURCE FACT
exact employer/source evidence

NORMALIZED CORRESPONDENCE
reviewed/deterministic mapping while preserving source wording

ANALYTICAL INTERPRETATION
candidate relevance/work/role-family synthesis with evidence and uncertainty

RECOMMENDATION / DECISION SYNTHESIS
later Market → You comparison/action guidance
```

### Deterministic responsibilities

Keep deterministic where the problem is deterministic:

- target/definition identity and versioning;
- run/snapshot identity;
- exact source/source-version membership dependencies;
- current/stale dependency checks;
- exact counts and denominators;
- requirement-strength counts;
- distinct-employer counts/concentration;
- approved duplicate adjustments if/when a future rule exists;
- sample/coverage warnings;
- persistence/reuse/idempotency/history;
- evidence drill-down links.

### Semantic responsibilities

Semantic/model reasoning may be used for:

- target-role relevance when deterministic filters are insufficient;
- later candidate responsibility/work grouping;
- later candidate role-subfamily interpretation;
- later bounded narrative/comparative synthesis.

Models must not fabricate counts, silently create canonical concepts, strengthen employer claims, or become the only record of corpus membership/evidence.

### Promotion boundary

Candidate Market interpretation may be useful without canonical promotion.

Stable reusable responsibility families, role archetypes, cross-run taxonomy, capability relationships, or high-impact personal decisions require their stronger review/promotion boundary.

---

## 4. Permanent target-market distinction

A target market must separate:

```text
ACQUISITION ENVELOPE
How do we obtain useful candidate recall?

MEMBERSHIP INTENT
What role/work actually belongs?
```

Permanent rule:

```text
search vocabulary
!= target-market relevance truth
!= canonical role taxonomy
```

Search terms are recall machinery. A job found through an AI-security term is not automatically an AI-security role. A relevant role may use a different title and still belong because of its actual work/requirements.

External standards such as ESCO/O*NET may later support optional crosswalk/validation, but they do not silently decide JobHunter membership.

---

# 5. Authorized first vertical slice

The first slice deliberately stops before semantic report/subfamily synthesis.

Authorized responsibility:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ MarketResearchRun
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow
```

## 5.1 `TargetMarket`

Stable user-recognizable target identity.

Minimum responsibility:

```text
stable target ID/slug
name
short description/intent
created_at
ordinary active/archive lifecycle only if needed
```

Do not mutate target meaning directly on this stable row.

## 5.2 `TargetMarketDefinitionVersion`

Immutable exact definition used by runs/snapshots.

First-slice semantic content may include:

```text
target_market_id
version / semantic fingerprint
membership intent
Jobinja source scope
search-catalog version
selected profile/pack references
bounded custom/extra terms/raw approved searches
include/exclude role/work hints
geography
work arrangement when material
seniority/experience scope when material
employment type when material
freshness/time-window rule
created_at
```

Operational request/detail/model budgets belong to the run and must not silently redefine market meaning.

## 5.3 `MarketResearchRun`

Operational attempt, not market semantic authority.

Record:

- exact definition version;
- exact acquisition/detail/model budgets/settings used;
- start/end/terminal status;
- requested/eligible/attempted/completed/reused/failed/pending/remaining stage ledger;
- snapshot/profile references when created;
- bounded failure summary.

Partial success is first-class.

## 5.4 `MarketJobMembership`

Target-specific semantic decision; never a global property of a job.

Confirmed first-slice dispositions:

```text
core_match
adjacent_match
uncertain
excluded
```

Membership identity must preserve:

```text
target definition version
source_job_id
exact source detail version
classifier contract/version
model/prompt/schema if semantic model used
exact English/P1.6 artifacts actually consumed, if any
disposition
reason/evidence refs
qualitative confidence if used
review/correction state as applicable
```

`uncertain` is a valid successful result.

## 5.5 `MarketCorpusSnapshot`

Point-in-time historical Market authority.

A snapshot must freeze:

- exact target definition version;
- exact member source/source-version identities;
- effective membership decisions/dispositions;
- exact accepted/pending/missing semantic coverage state used by the report;
- applicable lifecycle/freshness state/warnings;
- denominator semantics;
- duplicate/repost policy identity/disclosure;
- aggregate contract input identity.

Old snapshots remain immutable after source/target/contract changes.

## 5.6 `MarketAggregateProfile`

Deterministic immutable derivative of one exact snapshot + aggregate contract.

It is the first-slice user intelligence artifact. A separate model-generated report artifact is not required yet.

---

## 6. Acquisition and orchestration reuse

Reuse existing JobHunter owners:

```text
search_registry / config
Jobinja discovery
Jobinja sync/detail fetch
source identity/version/evidence
fetch observations
lifecycle
translation
P1.6
existing browser operation model
CLI
SQLite
```

Use one thin target-aware coordinator rather than a workflow framework.

### Important first-slice rule: target-scoped affected work

Existing Phase-1 orchestration is a useful composition precedent, but global missing/refresh queues that merely prioritize target IDs may spill remaining bounded budget into unrelated jobs.

A Market run must select affected work from the target candidate set for:

- detail missing/refresh;
- translation missing/stale;
- P1.6 missing/stale/review backlog.

Do not create parallel source identities or derived-artifact caches.

### Reuse/invalidation

```text
source semantic version changes
→ recompute affected translation/P1.6 per their existing contracts
→ membership for that source/version becomes stale
→ old snapshots remain unchanged

Target definition changes
→ new definition version
→ membership/snapshot/profile recompute
→ generic source/translation/P1.6 stay valid

membership classifier contract changes
→ membership/snapshot/profile recompute
→ upstream source/translation/P1.6 stay valid

aggregate contract changes
→ snapshot stays valid
→ new aggregate profile
```

---

## 7. Source eligibility and lifecycle

A posting must have a current successfully parsed source detail version before it can become a qualified source-level snapshot member.

Active-market handling:

```text
active
→ eligible subject to target freshness/membership

possibly_unavailable
→ may remain eligible with explicit warning when prior valid source evidence is fresh enough

expired / removed
→ outside active primary corpus; preserved historically

rate_limited / access_denied / challenge / auth_required /
server_error / network_error / unexpected_page / unknown_error
→ weak/retryable failure is not disappearance; preserve prior valid evidence subject to freshness policy
```

Permanent rule:

```text
failed refresh != market disappearance
```

Missing-detail discoveries remain candidates/backlog, not qualified snapshot members.

---

## 8. Membership evidence and denominator policy

First-slice staged membership:

```text
deterministic source/target eligibility
→ bounded semantic role/work relevance when necessary
```

Lowest sufficient semantic evidence:

```text
current parsed source detail + title
+ current English projection when needed
+ accepted-current P1.6 opportunistically when available
```

Accepted P1.6 is **not** required for source-level target membership.

Capability and Work Intelligence are not first-slice membership dependencies.

### Primary target corpus

```text
primary corpus = core_match
adjacent_match = visible separately
uncertain = visible separately
excluded = traceable / outside primary denominator
```

### P1.6 semantic coverage

Always distinguish within the core source corpus:

```text
core source postings
core + accepted-current P1.6
core + pending P1.6
core + missing/no-current P1.6
core + failed/rejected current processing where relevant
```

Source-level metrics use their exact source denominator.

Requirement/responsibility prevalence uses only core postings with accepted-current P1.6 under the declared semantic contract.

Pending/missing/failed P1.6 must never be interpreted as zero requirements or zero work.

B1 `ta9l` is a concrete proof of this boundary: source-level relevance can be clear while accepted P1.6 remains unavailable.

---

## 9. Repost / duplicate policy for first slice

Stable repeated observation of one `source_job_id` is already one logical source posting.

Automatic repost/new-source-ID collapsing is deliberately **not implemented in the first slice** because the formal investigation did not establish a defensible real Jobinja pair set for an authority rule.

Therefore first-slice denominator language is:

```text
qualified source postings
```

not:

```text
unique demand units
```

Profiles must disclose that repost/new-ID adjustment is not implemented.

Keep employer concentration visible and avoid strong deduplicated-demand, trend, or `emerging` claims.

All source advertisements must remain preserved if a later explicit duplicate/repost policy is introduced.

---

## 10. Deterministic first aggregate profile

The first `MarketAggregateProfile` should contain only evidence-backed deterministic values.

### Evidence/corpus-quality header

Include:

- target + definition version;
- run/snapshot identity/time;
- source/search scope;
- candidate/source-eligible counts;
- core/adjacent/uncertain/excluded counts;
- qualified core source postings;
- accepted/pending/missing-or-failed P1.6 coverage;
- raw source-posting count;
- repost-adjustment disclosure;
- distinct employers;
- largest-employer contribution/share;
- freshness/lifecycle warnings;
- processing failures/backlog.

### Requirement rows

For accepted-current P1.6 core members:

- concept;
- concept type;
- supporting-posting count/share with explicit denominator;
- required/preferred/contextual/inferred support;
- distinct-employer support;
- source-explicit depth distribution where useful;
- exact job/artifact/claim/evidence drill-down.

One posting supports one concept at most once in the concept-support count.

Strength columns may remain non-exclusive where one posting genuinely states the same normalized concept at multiple strengths; disclose that behavior.

### Responsibilities/work

Expose accepted responsibility/work evidence/counts/drill-down without inventing cross-job family equivalence.

Reviewed Registry mappings may enrich normalization where available. Unmapped accepted facts remain visible.

### Source-level context

Aggregate geography/employment/experience/education/context only where exact field/normalization/denominator semantics are explicit.

### Excluded from v1

- model-generated numeric statistics;
- opaque importance scores;
- fixed `core/common/specialized` bands;
- semantic subfamily prevalence;
- trends/`emerging`/forecasting.

---

## 11. Capability, Work and Registry reuse

### Capability

Not a mandatory first-slice dependency. Current coverage and model dependency would unnecessarily reduce Market coverage for basic factual aggregation.

### Work Intelligence

Not a mandatory first-slice dependency. P1.6 already owns factual responsibilities/role purpose. Work may later add useful candidate organization after first-slice product value is proven.

### Canonical Registry

Use reviewed mappings opportunistically when available.

Avoid both extremes:

```text
under-normalization
→ harmless variants split every signal forever

over-gating
→ useful report waits for exhaustive manual canonicalization
```

Unmapped claims remain valid evidence and must not disappear.

---

## 12. Browser and CLI first-slice workflow

### Browser — primary

Target repeated-use flow:

```text
Targets
→ create/select target
→ create immutable definition version when meaning changes
→ preview acquisition scope + run budgets
→ run/refresh using existing one-mutable-operation pattern
→ inspect partial-success ledger
→ inspect membership/evidence/uncertainty
→ inspect frozen snapshot + deterministic profile
→ drill down to source/semantic evidence
→ inspect run/snapshot history
```

Market runtime state stays local.

Existing public-corpus synchronization may continue publishing only upstream repository-safe artifacts already governed for publication. Market target/membership/snapshot/profile tables are not automatically exported.

### CLI — secondary

Expose the same underlying services for advanced use, automation and debugging. Exact command names are implementation details; responsibilities include target/version, run, membership, snapshot and profile inspection.

No CLI-only semantic path.

---

## 13. First-slice testing and acceptance

Use the accepted three-tier philosophy:

```text
Tier 1: compact synthetic deterministic mini-market
Tier 2: curated repository-safe semantic boundary cases
Tier 3: bounded real local target run
```

### Mandatory invariants

- stable target vs immutable definition version;
- target-definition change does not invalidate generic source/translation/P1.6;
- unchanged rerun reuses upstream work;
- target run does not spend budgets on unrelated global backlog;
- failed refresh != disappearance;
- expired/removed does not mutate old snapshots;
- `adjacent_match` / `uncertain` / `excluded` never enter core prevalence silently;
- `uncertain` is a valid semantic result;
- missing/pending/failed P1.6 is visible, not zero demand;
- only accepted-current P1.6 enters strong semantic statistics;
- one posting max once per concept support count;
- every share has recoverable denominator semantics;
- employer breadth/concentration is deterministic;
- snapshot/member dependencies are exact and immutable;
- aggregate profile references exact snapshot + contract;
- no first-slice `unique demand` claim;
- partial success preserves successful durable work;
- browser/CLI share services/state;
- normal CI uses deterministic fixtures/fakes and never requires Jobinja/LM Studio;
- Market state remains local/private by default.

### Real local acceptance

I7 must run one representative target and verify:

- bounded acquisition scope/noise is visible;
- source/detail/model reuse on rerun;
- membership inspection;
- honest P1.6 coverage;
- denominator/warnings;
- evidence drill-down;
- partial-success behavior;
- browser/CLI shared state.

Do not call the first slice closed before this passes.

---

# 14. Later Market responsibilities — separately gated

The long-term product direction remains broader than the first slice.

## 14.1 Candidate responsibility/work + role-subfamily synthesis

After deterministic target/profile acceptance, investigate/add one bounded **report-level** semantic synthesis if it materially reduces manual interpretation.

Preferred evidence order:

```text
accepted recurring responsibilities/work
→ requirement/capability bundles
→ tools/knowledge/context
→ titles as supporting evidence
```

Candidate subfamilies remain analytical interpretation. Do not force every job into exactly one family.

Do not generate per-job semantic narratives merely to summarize them upward.

## 14.2 Role-Family Intelligence Report

Once semantic synthesis exists and exact nondeterministic output must be recoverable, persist a versioned user-facing `RoleFamilyIntelligenceReport` referencing the exact snapshot/profile and model/prompt/schema contract.

Numeric values must be injected from deterministic profile data rather than authored by the model.

Recommended mature reading order:

```text
Target + Evidence Quality
→ Executive Market Summary
→ Market Shape
→ Responsibilities / Work
→ Technologies / Tools
→ Applied Skills / Capabilities
→ Knowledge / Practices
→ Professional / Transversal Capabilities
→ Experience / Seniority / Education / Credentials
→ Work Context / Geography / Arrangement
→ Useful Co-occurrence / Bundles
→ Candidate Role Subfamilies
→ Changes Since Comparable Snapshot
→ Evidence Drill-down + Method / Limitations
```

## 14.3 Repost/new-ID adjustment

Reopen only with real bounded Jobinja evidence. Preserve every source advertisement and represent `same demand / separate / uncertain` explicitly before any unique-demand denominator becomes authoritative.

## 14.4 Historical comparison / trends

Only after comparable immutable snapshots exist.

Comparability must account for:

- same logical target;
- compatible target-definition semantics;
- source/search scope;
- membership policy;
- duplicate policy;
- aggregate contract;
- denominator semantics;
- sufficient support.

Materially incompatible snapshots must display `NOT DIRECTLY COMPARABLE` rather than invent a trend.

`emerging` requires sustained comparable evidence and employer breadth; rare != emerging.

## 14.5 Later Market → You

Objective Market intelligence must remain independently inspectable.

Personal comparison requires a separately accepted reviewed personal-evidence schema. Do not infer personal capability from chat memory, repository keywords, course completion, or AI-generated code alone.

No fake single readiness percentage.

---

## 15. Architecture discipline

Keep this capability inside the current local modular monolith and SQLite history model.

Do not introduce without demonstrated need:

- microservices/distributed queues;
- vector database;
- graph database;
- generic RAG platform;
- agent/workflow framework;
- generic source/plugin layer before a real second approved source;
- exhaustive canonicalization.

Prefer existing versioned service/store patterns and typed contracts.

---

## 16. Publication / privacy

The first Market slice remains local/private.

Do not automatically publish:

```text
Market target definitions
membership decisions
snapshots
aggregate profiles
Work Intelligence
Canonical Registry
future personal evidence
```

into `corpus/`.

Any future repository-safe Market projection requires a separate privacy/publication review and explicit authorization.

---

## 17. Documentation / progressive memory

Use:

### Current plan

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Update only when durable Market scope/order/acceptance/architecture changes.

### Rolling state

`docs/WORKING_MEMORY.md`

Keep current status, accepted decision, next action, stop lines and latest record; do not turn it into a transcript.

### Execution checklist

`docs/EXECUTION_TODO.md`

Keep only authorized increments active.

### Dated records

Use `docs/working-memory/` for meaningful design/implementation/acceptance transitions.

The foundation protocol is now closed:

`docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`

The final foundation decision is current implementation input:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Repeatable deterministic/authority defects should become tests when practical. One-off model prose variation should not force endless contract churn.

---

## 18. Definition of done for the first slice

The first Market vertical slice is done only when:

1. I1–I6 implement the authorized responsibilities without later-scope leakage;
2. deterministic/store/service/browser/CLI tests pass;
3. source/state/privacy/provenance invariants hold;
4. target/source/P1.6 denominators are explicit and correct;
5. partial failures are inspectable without erasing durable success;
6. one bounded real local target run passes I7;
7. unchanged rerun proves useful reuse;
8. evidence drill-down is usable;
9. docs match behavior;
10. the workflow materially reduces target-market vacancy-by-vacancy reading.

---

## 19. Current exact next action

```text
I1-I6 repository acceptance complete
→ I7 real-local execution complete / HOLD
→ complete only the bounded HOLD closure checks
→ review pending P1.6 normally; never auto-accept
→ verify live accepted-semantic drill-down + rerun snapshot immutability + post-run SQLite integrity
→ record PASS only if those remaining checks succeed
→ close the first slice only after PASS
```

Latest repository-accepted implementation increment: `docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`.

I7 protocol: `docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`.

I7 execution result: `docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`.

Do not restart B1/foundation investigation or add report/subfamily/trend/personal scope while I7 remains HOLD.
