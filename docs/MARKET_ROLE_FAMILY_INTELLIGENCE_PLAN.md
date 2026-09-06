# JobHunter Market and Role-Family Intelligence Plan

**Status:** OWNER-APPROVED PRODUCT DIRECTION / CONTROLLING DESIGN-AND-INVESTIGATION PLAN / IMPLEMENTATION GATED  
**Date:** 2026-09-06  
**Branch:** `main`  
**Scope:** Target-scoped market refresh → qualified evidence corpus → aggregate market/role-family intelligence → versioned report/history → later reviewed personal comparison  
**Current implementation gate:** P2.2B-B1 remains the active product frontier. This plan records and controls the future Market/role-family responsibility but does **not** authorize Market-v2 implementation while that gate remains open.

## 1. Purpose

JobHunter must let the user ask for a current view of a target job market and receive **one evidence-backed aggregate intelligence report across the relevant postings**, rather than reading or receiving one report per vacancy.

A representative user intent is:

```text
Update the market for AI Security / ML Security roles in Germany,
process the relevant current job advertisements,
and show me what this market actually asks people to know and do.
```

The system should then perform a bounded, inspectable workflow that:

1. defines the target market slice;
2. updates/discovers relevant source postings within approved source policy;
3. fetches/refreshes the required source details;
4. reuses or builds current derived artifacts as needed;
5. determines which postings genuinely belong to the requested market slice;
6. records a reproducible qualified corpus/snapshot;
7. aggregates requirements, responsibilities, skills, tools, practices, experience and other useful dimensions across that corpus;
8. synthesizes recurring work and candidate role-family/subfamily patterns without presenting inference as employer fact;
9. produces one useful **Role-Family Intelligence Report** with evidence scope, counts, warnings and drill-down provenance;
10. preserves versioned snapshots so later runs can show real market change rather than only overwrite the latest answer.

The capability directly advances JobHunter's existing product purpose:

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ ACTION
```

Job acquisition remains an input subsystem. The product value is the trustworthy synthesis of what a target market is asking for.

---

## 2. Authority and relationship to current work

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
current active focused product plan
```

Current exact product gate remains:

```text
P2.2B-B1 selective responsibility promotion
→ ta9l current English projection / P1.6 acceptance
→ final correspondence decision
→ possible one-concept/two-mapping pilot
→ B1 closure decision
```

Therefore:

- recording this plan is authorized now;
- repository orientation and plan-level architectural analysis are authorized now;
- **Market-v2 implementation is not started by this document**;
- formal implementation investigation/experiments begin only after the current P2.2B-B1 gate is closed and the owner explicitly activates this plan;
- this plan must be reconciled against whatever P2.2B/P2.2C evidence exists at activation time rather than assuming today's future dependencies remain unchanged.

The plan should not force P2.2C responsibility families or P2.2D stable role archetypes to exist before useful market interpretation can be shown. Candidate analytical groupings are allowed under the reasoning policy when clearly labeled and evidence-qualified; reusable promoted taxonomy has a stronger gate.

---

## 3. Product outcome and naming

The primary user-facing artifact should be called a:

**Role-Family Intelligence Report**

The same durable product responsibility may also be described generically as a **Market Brief** or **Target Role Profile**, but repository contracts should use one canonical name after the implementation investigation finalizes terminology.

The report is **one aggregate output for one target-market definition and one evidence snapshot**. Individual job pages remain drill-down evidence and are not the main report unit.

Example high-level output:

```text
AI / ML Security — Germany
Role-Family Intelligence Report
Generated: <timestamp>

Target corpus
- discovered candidates: ...
- fetched/current source jobs: ...
- eligible relevant jobs: ...
- analyzed jobs: ...
- distinct employers: ...
- duplicate/repost adjustments: ...
- uncertain/excluded jobs: ...
- important sampling/concentration warnings: ...

Requirements
- Python: 44 / 63 postings (70%)
  required: 31 | preferred: 8 | contextual: 5
- Cloud: ...
- Kubernetes: ...

Responsibilities
- security automation / engineering: ...
- AI/ML evaluation and monitoring: ...
- threat/vulnerability analysis: ...

Candidate role subfamilies
- AI/ML platform security
- security automation / detection engineering
- adversarial testing / AI assurance

Experience / context
...

Evidence and limitations
...
```

All example numbers and labels above are illustrative only. The implementation must calculate numeric aggregates deterministically from qualified stored evidence.

---

## 4. Permanent authority model for this capability

The report must preserve JobHunter's four epistemic levels:

```text
SOURCE FACT
exact employer/source evidence

NORMALIZED CORRESPONDENCE
reviewed/deterministic concept correspondence while preserving source wording

ANALYTICAL INTERPRETATION
candidate role-family/work/responsibility synthesis with evidence and uncertainty

RECOMMENDATION / DECISION SYNTHESIS
later Market → You comparison and personal action guidance
```

### 4.1 Deterministic responsibilities

Keep deterministic where the problem is deterministic:

- target-definition identity/version;
- run/snapshot identity;
- source/job/source-version membership;
- current/stale dependency checks;
- exact counts and denominators;
- requirement-strength counts;
- distinct-employer counts;
- duplicate/repost adjustments once their rule is approved;
- sample/concentration calculations;
- artifact currentness and lineage;
- historical snapshot comparison inputs;
- source drill-down links;
- persistence/reuse/idempotency rules.

### 4.2 Semantic/model responsibilities

Semantic reasoning may be used for tasks that actually require interpretation:

- target-role relevance qualification when deterministic filters are insufficient;
- candidate responsibility/work clustering;
- candidate role-subfamily interpretation;
- comparative narrative synthesis;
- identifying meaningful combinations or unusual patterns;
- later explaining changes between snapshots.

Model output must not fabricate counts, silently create canonical concepts, silently strengthen employer claims, or become the only record of corpus membership/evidence.

### 4.3 Promotion boundary

Candidate market interpretation may be useful without canonical promotion.

However, stronger review is required before a concept becomes reusable stable authority such as:

- canonical responsibility family;
- stable role archetype;
- canonical cross-run market taxonomy;
- reusable capability relationship;
- durable personal gap/readiness decision input with high downstream impact.

---

## 5. Intended end-to-end user workflow

The mature normal browser workflow should be approximately:

```text
1. Define/select target market
        ↓
2. Preview bounded acquisition/search scope
        ↓
3. Run market refresh
        ↓
4. Discover + refresh source jobs
        ↓
5. Reuse/process missing current English/P1.6 dependencies
        ↓
6. Qualify target-market membership
        ↓
7. Freeze qualified market snapshot
        ↓
8. Build deterministic aggregate profile
        ↓
9. Build bounded candidate work/role-family synthesis
        ↓
10. Render Role-Family Intelligence Report
        ↓
11. Save versioned report/snapshot
        ↓
12. On later runs, compare like-for-like snapshots when valid
```

The CLI should expose the same services for advanced use, automation, inspection and debugging. The browser remains the normal repeated-use surface.

Partial-success semantics apply throughout. One failed source fetch, translation, P1.6 operation or semantic qualification must not erase successful durable work or turn the entire market run into a false generic success/failure.

---

## 6. Target-market definition

A durable target market must be more precise than a raw keyword string but must not become a rigid predefined career taxonomy.

The implementation investigation should determine the smallest useful `TargetMarketDefinition` contract. Candidate dimensions include:

- stable target ID and user-facing name;
- search phrases / configured search profile or pack references;
- include terms or role hints;
- explicit exclude terms where useful;
- geography/country/region/city scope;
- remote/hybrid/on-site constraints when relevant;
- seniority/experience scope;
- employment type;
- date/freshness window;
- enabled approved source(s);
- bounded request/page/detail budgets;
- optional direct approved job/search URLs;
- definition version / semantic fingerprint.

Important rule:

```text
search vocabulary
!=
target-market relevance truth
!=
canonical role taxonomy
```

Search terms exist to obtain useful recall. A posting discovered by an AI-security phrase is not automatically an AI-security role. Conversely, a relevant role may use a different title and still belong to the requested market based on its work and requirements.

The first implementation should remain Jobinja-centered. Do not build a generic source/plugin framework before a real approved second source demonstrates the abstraction need.

---

## 7. Formal investigation required before implementation

After the current P2.2B-B1 gate closes and this plan is explicitly activated, perform one bounded architecture/product investigation before writing new Market-v2 source code.

The investigation must answer the following questions and produce a dated working-memory decision record.

### 7.1 Acquisition and orchestration reuse

Inspect at minimum:

```text
src/jobhunter/search_registry.py
src/jobhunter/jobinja_discovery.py
src/jobhunter/jobinja_sync.py
src/jobhunter/jobinja_batch.py
src/jobhunter/phase1_run.py
src/jobhunter/config.py
browser operation wiring
CLI entrypoints
```

Determine:

- whether existing search profiles/packs can represent target-market acquisition cleanly;
- whether a new target-definition domain object is needed;
- how a target run should reuse existing discovery provenance instead of creating parallel source identities;
- how to update only missing/stale eligible detail data rather than refetch everything;
- how to expose request budgets and partial-success state to the user.

### 7.2 Corpus freshness and membership boundary

Define exactly which source jobs may enter one market snapshot.

Investigate:

- active/current source state;
- stale/unchecked source state;
- explicit expiry/removal;
- current semantic source version;
- failed refresh observations;
- jobs with incomplete details;
- jobs with missing/stale translation/P1.6;
- when an old accepted analysis is no longer current for the current source version.

A failed source refresh must not be interpreted as market disappearance.

### 7.3 Relevance qualification

Design a target-membership step that is stronger than keyword matching.

Candidate dispositions:

```text
core_match
adjacent_match
uncertain
excluded
```

The investigation must decide:

- which dimensions can be deterministic filters;
- when semantic/model classification is justified;
- what evidence references/reasons are stored;
- whether confidence is qualitative;
- how user correction/review works when useful;
- which dispositions enter the primary denominator;
- how adjacent/uncertain postings are displayed without contaminating core prevalence statistics.

Interpretive uncertainty should fail soft. It should not force false inclusion/exclusion.

### 7.4 P1.6 sufficiency audit

Compare the desired report fields against current accepted P1.6 output.

Confirm whether existing P1.6 already supplies enough authoritative substrate for:

- requirements;
- required/preferred/contextual/inferred strength;
- concept types;
- source-explicit depth;
- responsibilities;
- role purpose;
- exact evidence/provenance.

Do not reopen P1.6 merely because Market wants different presentation. Reopen only if a repeatable material substrate gap is proven.

### 7.5 Capability Intelligence reuse audit

Determine which market questions genuinely benefit from Capability v9 and which should aggregate directly from P1.6.

Questions include:

- capability grouping across jobs;
- source work linked to capabilities;
- source-explicit depth distribution;
- whether current Capability artifacts exist widely enough to support a market-level claim;
- whether using Capability would unnecessarily gate useful Market output.

No Market result should silently treat optional Capability model enrichment as employer truth.

### 7.6 Work Intelligence reuse audit

Determine how accepted P2.2A Work Intelligence can contribute to responsibility/work-composition synthesis.

Keep the permanent rule:

> The model may organize accepted work; accepted P1.6 statements decide what factual work is actually asserted.

Investigate whether candidate work themes can support low-blast-radius market interpretation without being promoted, while any stable cross-run family/archetype requires the proper promotion boundary.

### 7.7 Canonical Registry dependency audit

Determine which aggregates require reviewed canonical correspondence and which can remain immediately useful using bounded normalization/source concepts.

Avoid both extremes:

- **under-normalized:** `Postgres`, `PostgreSQL`, translated aliases and harmless variants split the same demand signal indefinitely;
- **over-gated:** every useful report waits for exhaustive manual canonicalization.

Use promoted registry mappings where available. Unmapped claims remain valid evidence and must not disappear.

### 7.8 Responsibility-family and role-archetype dependency audit

Reconcile the final P2.2B/P2.2C state at activation time.

Determine:

- what can be a candidate analytical family immediately;
- what requires reviewed reusable responsibility-family authority;
- how candidate role subfamilies are supported across jobs/employers;
- when a candidate archetype becomes stable enough for promotion;
- how multiple plausible subfamilies are represented without forced classification.

Titles are supporting evidence. Recurrent work/responsibilities/capability expectations should carry more semantic weight than inconsistent titles.

### 7.9 Duplicate/repost investigation

Current Market explicitly discloses that repost/cross-post near-duplicate adjustment is not implemented. Market-v2 prevalence/trend claims must address this before strong statistics are presented.

Investigate:

- same logical source job across observations;
- reposted jobs with new source IDs;
- employer/title/content near-duplicates;
- cross-source duplicates if/when a second source exists;
- whether duplicate groups should count once for prevalence while preserving all source evidence;
- how uncertain duplicate relationships are represented.

Do not solve this with opaque similarity thresholds without review evidence.

### 7.10 Sample quality and employer concentration

Reuse and extend the current Market safeguards:

- analyzed sample size;
- distinct-employer count;
- largest-employer share;
- source/filter scope;
- processing coverage;
- translation/model coverage;
- duplicate-adjustment disclosure.

Investigate stronger claims only when the sample supports them. One employer contributing many postings must not masquerade as broad market demand.

### 7.11 Temporal and trend model

Historical intelligence must compare comparable snapshots, not arbitrary report outputs.

Define:

- exact target-definition identity/version;
- snapshot time/window;
- source scope;
- inclusion/membership policy version;
- aggregate contract version;
- duplicate policy version;
- denominator semantics;
- minimum comparability checks.

If target definition or aggregation semantics materially change, JobHunter should display a comparability warning rather than invent a trend.

### 7.12 Persistence and artifact model

Determine the smallest durable records needed for reproducibility and repeated use.

Provisional concepts, subject to investigation:

```text
TargetMarketDefinition
MarketResearchRun
MarketJobMembership
MarketCorpusSnapshot
MarketAggregateProfile
RoleFamilyIntelligenceReport
```

Do not create separate storage systems. Reuse SQLite and existing source/derived artifact identities.

### 7.13 Browser and CLI integration

Design one coherent repeated-use workflow instead of many disconnected commands.

Browser requirements should include:

- target definition/selection;
- run preview and bounds;
- operation progress/partial-success result;
- corpus quality/scope summary;
- aggregate report;
- expandable evidence/drill-down to source jobs;
- prior snapshot comparison when comparable;
- clear candidate/promoted/uncertain labeling.

CLI should provide the same underlying service operations and deterministic inspection.

### 7.14 Performance and model-call budget

Market refresh must be incremental.

Investigate/reuse:

- current source versions;
- current English projections;
- accepted current P1.6 artifacts;
- current Capability/Work artifacts when actually required;
- missing/stale queues;
- bounded batch limits.

Do not re-run model inference across the entire corpus on every market report.

### 7.15 Publication/privacy boundary

The first report should remain local unless a separate publication decision exists.

Do not automatically add Market-v2, Work Intelligence, Canonical Registry or later personal state to `corpus/`.

Any future repository-safe projection requires a separate privacy/publication review.

### 7.16 Testing and acceptance strategy

Before implementation, define representative fixtures/cases covering:

- core relevant role;
- adjacent role;
- misleading keyword/title match;
- sparse posting;
- dense posting;
- multiple postings from one employer;
- repost/near-duplicate case;
- stale source version;
- partial translation/analysis failure;
- native-English and translated postings;
- ambiguous role-family membership;
- multiple candidate subfamilies.

Semantic tests should validate dangerous authority/boundary failures rather than require identical model prose.

---

## 8. Proposed evidence and artifact flow

The intended architecture, subject to the formal investigation, is:

```text
TargetMarketDefinition
        ↓
existing bounded search planning
        ↓
Jobinja discovery + refresh
        ↓
existing source/evidence/version/lifecycle authority
        ↓
current English projection where required
        ↓
accepted/current P1.6 factual substrate
        ↓
Target-market membership qualification
        ↓
MarketCorpusSnapshot
        │
        ├──→ deterministic requirement/context aggregation
        │
        ├──→ reviewed canonical mappings where available
        │
        ├──→ bounded Capability/Work inputs where authorized/useful
        │
        └──→ candidate cross-job semantic synthesis
                    ↓
          RoleFamilyIntelligenceReport
                    ↓
          later comparable snapshot history
                    ↓
          later reviewed Market → You comparison
```

This is an extension of the current modular monolith and current Market read-model boundary, not a new microservice, vector database, graph platform or agent framework.

---

## 9. Aggregate intelligence contract

### 9.1 Every statistic must expose its denominator

A statement such as:

```text
Python appears in 70% of jobs
```

is invalid without a defined denominator.

The report must distinguish at least where applicable:

- discovered candidate postings;
- current fetched/parsed postings;
- relevance-qualified postings;
- postings with current accepted P1.6;
- distinct employers;
- duplicate-adjusted posting units.

The primary denominator for a metric must be explicit and stable for that metric.

### 9.2 Requirement demand

For each useful normalized/canonical concept, preserve at minimum:

- posting count;
- posting share;
- distinct-employer count/share where useful;
- required count;
- preferred count;
- contextual count;
- inferred count;
- evidence/normalization status;
- source aliases/wording drill-down;
- sample/coverage warnings.

The current Market behavior of counting a source job at most once per concept/classification is a useful baseline to preserve unless the investigation proves a better contract.

### 9.3 Responsibility/work demand

Responsibility reporting must distinguish:

```text
exact accepted P1.6 responsibilities
vs
normalized/promoted responsibility correspondence
vs
candidate analytical responsibility/work family
```

A candidate cluster must never be displayed as though every employer used that wording.

Useful aggregate dimensions may include:

- supporting posting count;
- distinct employers;
- exact supporting responsibility claims;
- candidate/promoted status;
- representative source wording;
- confidence/ambiguity;
- source-specific details intentionally not normalized away.

### 9.4 Skills, tools, practices, knowledge and domains

The report should separate concept types where useful instead of flattening every concept into a single skill list.

Potential sections include:

- programming languages;
- frameworks/libraries;
- platforms/tools;
- security/engineering practices;
- knowledge areas;
- domain knowledge;
- interpersonal/professional capabilities;
- language/legal/location constraints.

A tool mention is not automatically an applied capability.

### 9.5 Experience, seniority and education

Aggregate explicit signals separately:

- years/duration requirements;
- seniority wording;
- education requirements/preferences;
- credentials/certifications;
- prior-domain experience;
- leadership/ownership expectations only when source/work evidence supports them.

Do not convert years mechanically into technical depth.

### 9.6 Work arrangement and market context

Where the source supports it, aggregate:

- geography;
- remote/hybrid/on-site arrangement;
- employment type;
- language expectations;
- salary/compensation only if source quality/coverage is sufficient and the contract is explicitly designed for it.

Missing data must not be interpreted as negative evidence.

### 9.7 Co-occurrence and capability bundles

Co-occurrence can reveal useful market bundles, but it must remain distinct from prerequisite logic.

Example:

```text
Docker + Kubernetes frequently co-occur
```

must not become:

```text
Kubernetes is a prerequisite for Docker
```

unless separate evidence supports that relationship.

---

## 10. Demand bands and report interpretation

The report may eventually use human-readable demand bands such as:

```text
core
common
specialized
```

but the first accepted implementation should not hide raw counts/shares behind arbitrary labels.

Before demand bands become durable semantics, investigate and document:

- denominator;
- threshold rule;
- minimum sample size;
- employer concentration effect;
- whether the threshold is global or target-specific;
- whether the classification remains stable enough to be useful.

### 10.1 `Emerging` has a stricter meaning

`Emerging` must **not** mean simply low-frequency or unusual.

It requires longitudinal evidence such as:

- materially increasing prevalence across comparable snapshots;
- increasing distinct-employer support;
- repeated new appearance across successive valid windows;
- appropriate sample/comparability warnings.

Until trend history exists, use terms such as `niche`, `less common`, `limited-sample signal`, or simply show the count.

---

## 11. Role-family and subfamily synthesis

The report should aim to answer:

> What kinds of work actually make up this target market, independent of inconsistent job titles?

Candidate subfamily inference may use:

- accepted responsibilities;
- role purpose;
- Work Intelligence themes where valid;
- canonical responsibility mappings/families when available;
- capability/requirement patterns;
- deliverables where evidence is authorized;
- titles only as supporting context.

Example candidate output:

```text
Target: AI Security

Candidate subfamilies:
1. AI/ML platform security
2. security automation and detection engineering
3. adversarial testing / AI assurance
```

For each candidate subfamily, retain:

- supporting jobs;
- distinct employers;
- representative exact responsibilities;
- differentiating requirements/capabilities;
- overlap with other subfamilies;
- confidence/uncertainty;
- candidate versus promoted status.

Do not force every job into exactly one subfamily. Multiple membership or unresolved classification can be correct.

Stable reusable role archetypes require stronger cross-job/employer evidence and explicit promotion.

---

## 12. Role-Family Intelligence Report structure

The first complete report should be designed around fast comprehension with inspectable depth.

Recommended sections:

### 12.1 Header and target identity

- target name;
- target definition/version;
- geography/seniority/source/time scope;
- generated timestamp;
- report/snapshot contract identity.

### 12.2 Corpus and evidence quality

- discovered candidates;
- fetched/current details;
- relevance-qualified jobs;
- analyzed/current jobs;
- distinct employers;
- duplicate/repost adjustment;
- native/translated coverage where relevant;
- excluded/adjacent/uncertain counts;
- source/model partial failures;
- sample/concentration/comparability warnings.

### 12.3 Executive market summary

A concise bounded interpretation of what this market appears to value and do, clearly separated from employer-authored facts.

### 12.4 Role-family landscape

- candidate/promoted subfamilies;
- supporting jobs/employers;
- overlaps/uncertainty;
- representative responsibilities.

### 12.5 Responsibilities and work patterns

- recurring direct work;
- supporting counts;
- employer diversity;
- exact evidence drill-down;
- candidate family/grouping status.

### 12.6 Requirements and capabilities

- core/common/specialized only if accepted band semantics exist;
- otherwise sorted raw prevalence;
- required/preferred/contextual/inferred distribution;
- distinct-employer support;
- tools versus applied capabilities kept distinguishable.

### 12.7 Technology/tool landscape

- languages;
- frameworks/libraries;
- platforms;
- infrastructure/security/ML tooling;
- co-occurrence where meaningful.

### 12.8 Knowledge/practice/domain expectations

- engineering practices;
- security/ML/domain knowledge;
- quality/reliability/operations practices;
- professional/interpersonal expectations.

### 12.9 Experience/seniority/education/context

- explicit experience patterns;
- seniority distribution;
- education/credentials;
- location/arrangement/language patterns.

### 12.10 Market change since prior comparable snapshot

Later history stage only:

- increased/decreased prevalence;
- newly recurring patterns;
- disappearing patterns;
- employer-diversity changes;
- explicit comparability limitations.

### 12.11 Evidence and limitations

Always expose:

- exact scope;
- important missing coverage;
- duplicate policy;
- model/translation dependencies;
- sample warnings;
- uncertainty;
- what the report is **not** claiming.

### 12.12 Evidence drill-down

The user must be able to inspect supporting postings/claims from an aggregate item without turning the entire report into one summary per vacancy.

---

## 13. Historical market intelligence

Every accepted report run should preserve enough state to compare future runs safely.

The goal is to answer questions such as:

```text
Python demand: 68% → 73%
Kubernetes: 29% → 37%
LLM security responsibilities: 11% → 26%
```

only when the underlying snapshots are sufficiently comparable.

Historical storage should support:

- exact target definition/version;
- source scope;
- snapshot timestamp/window;
- job/source-version membership;
- aggregate contract version;
- duplicate policy;
- role-family interpretation contract/version if persisted;
- prior report reference.

A trend is an analytical conclusion over deterministic snapshot measurements. The measurements should be deterministic; the narrative explanation may be semantic and uncertainty-aware.

---

## 14. Later Market → You layer

The objective market report must be built first and remain independently inspectable.

Only after JobHunter has an accepted reviewed personal-evidence layer should a later workflow compare:

```text
qualified market / role-family requirements
        ↕
reviewed personal capability evidence
```

Potential output:

```text
Market priority / recurring expectation
→ current personal evidence
→ exact gap class
→ recommended learn / practise / build / document / assess action
```

Permanent boundaries:

- do not infer personal capability from chat memory, repository keywords, course completion or AI-generated code alone;
- do not contaminate the objective market aggregate with the user's current skills;
- do not create a fake single readiness percentage;
- do not rank personal action solely by keyword frequency;
- preserve knowledge/practice/depth/integration/evidence/recency/context/presentation gap distinctions.

This is a later product stage, not part of the first Market/role-family implementation.

---

## 15. Delivery sequence

Implementation should proceed as bounded vertical slices after activation.

### Foundation investigation and design

**Outcome:** exact reuse/new-contract decision before code.

- perform Section 7 investigation;
- inspect current source/tests/services only as needed;
- document decisions in a dated working-memory record;
- amend this plan if evidence changes architecture or ordering;
- define first acceptance corpus/cases;
- explicitly authorize the first implementation slice.

**Stop line:** no speculative framework/database/agent/taxonomy build during investigation.

### Target definition and scoped refresh

**Outcome:** one target market can drive the existing bounded acquisition/update pipeline reproducibly.

- target definition contract;
- target-run identity;
- search-plan integration;
- incremental discovery/detail refresh;
- explicit bounds;
- partial-success operation result;
- browser/CLI parity.

**Acceptance:** a repeated target run reuses existing source identities and does not broaden source policy.

### Qualified market snapshot

**Outcome:** one run produces an inspectable target-market membership snapshot.

- relevance membership contract;
- core/adjacent/uncertain/excluded dispositions;
- currentness/dependency rules;
- exact job/source-version membership;
- corpus quality metrics;
- representative semantic review.

**Acceptance:** inclusion/exclusion is explainable and uncertain cases do not silently contaminate the primary denominator.

### Deterministic aggregate profile

**Outcome:** trustworthy requirements/context statistics over the qualified snapshot.

- posting + employer prevalence;
- strength distributions;
- type-aware concept groups;
- sample/concentration disclosures;
- duplicate policy appropriate to claim strength;
- source drill-down;
- no model-generated numeric statistics.

**Acceptance:** same snapshot + same aggregate contract yields the same numeric result.

### Responsibility/work and candidate role-family synthesis

**Outcome:** useful cross-job work interpretation above deterministic facts.

- accepted responsibilities remain factual anchors;
- reuse reviewed mappings/families where available;
- candidate analytical grouping where promotion is unnecessary;
- candidate subfamily support/overlap/confidence;
- no forced stable archetypes.

**Acceptance:** candidate synthesis reduces manual reading while exact supporting claims remain recoverable and no interpretation is presented as employer wording.

### Report and repeated-use browser workflow

**Outcome:** one normal browser flow produces the Role-Family Intelligence Report.

- report UI;
- operation progress/result;
- scope/warnings first-class;
- drill-down evidence;
- saved report/snapshot;
- CLI equivalent service operations.

**Acceptance:** the user can understand the target market without opening every vacancy, while still being able to inspect evidence on demand.

### Historical snapshot and trend comparison

**Outcome:** comparable prior/current market snapshots show evidence-backed change.

- comparability contract;
- trend calculations;
- employer-diversity checks;
- emerging/declining signals;
- explicit warnings for incompatible snapshots.

**Acceptance:** no trend is asserted from incompatible or insufficient evidence.

### Later reviewed personal comparison

**Outcome:** objective Market → You gap/action layer after personal-evidence prerequisites are accepted.

This remains separately gated and must not be pulled into earlier Market implementation for convenience.

---

## 16. Acceptance criteria for the complete capability

The complete first-generation Market/role-family capability is acceptable only when all applicable criteria below pass.

### Integrity

- every included posting is linked to an exact source identity/version;
- stale derived artifacts do not silently feed current reports;
- every numeric aggregate is deterministically reproducible from the recorded snapshot;
- every material semantic interpretation has recoverable supporting evidence;
- source failures are not treated as zero-market evidence;
- duplicate/repost policy is disclosed and appropriate to the claim;
- no model output manufactures numeric prevalence;
- no candidate interpretation becomes source fact;
- no private/personal data enters public projections without separate authorization.

### Scope honesty

- target definition is explicit;
- report denominator(s) are explicit;
- distinct employer support is available for broad claims;
- small/concentrated samples produce warnings;
- incomplete translation/analysis coverage is visible;
- uncertain relevance cases remain visible;
- missing employer information is not interpreted as absence of a requirement.

### Utility

- one report materially reduces vacancy-by-vacancy reading;
- recurring requirements and responsibilities are easy to identify;
- requirement strength is visible;
- tools are not flattened into capabilities blindly;
- candidate role subfamilies explain actual work differences better than titles alone;
- evidence drill-down is available without overwhelming the summary;
- later repeated runs can reuse prior work and show comparable changes.

### Operational quality

- bounded source requests and model calls;
- incremental/reuse behavior;
- explicit partial success;
- browser/CLI share services/state;
- deterministic tests green;
- representative semantic acceptance performed for new model-derived responsibilities;
- important repeatable defects become regression tests.

---

## 17. Explicit non-goals and stop lines

This plan does **not** authorize:

- Market-v2 implementation before the current P2.2B-B1 gate closes and owner activation occurs;
- unrestricted web crawling;
- authenticated LinkedIn automation or access-control bypass;
- a generic source/plugin framework before a real second source;
- exhaustive canonicalization merely to make a report look complete;
- automatic canonical taxonomy growth from model output;
- Blueprint v6 as Market authority;
- opaque model-generated market percentages;
- a single generic `market demand score` hiding real dimensions;
- arbitrary `core/common/emerging` labels without explicit accepted semantics;
- calling a low-frequency concept `emerging` without longitudinal evidence;
- forced one-role-per-job classification;
- fake prerequisite relations from co-occurrence;
- a vector database, graph database, RAG platform or agent framework without demonstrated need;
- microservices/distributed queues for the current local workload;
- personal readiness/gap scoring before reviewed personal evidence exists;
- autonomous applications or recruiter communication;
- automatic publication of Market/Work/Registry/personal state.

---

## 18. Documentation and progressive memory protocol

This responsibility is large enough that decisions must be recorded progressively rather than reconstructed at the end.

Use the following documentation pattern:

### 18.1 This plan

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Controls the feature's design/investigation/delivery intent once activated. Update it only when durable scope, ordering, acceptance or architecture decisions change.

### 18.2 Rolling working memory

`docs/WORKING_MEMORY.md`

At meaningful gate transitions, keep a concise pointer to:

- current status;
- latest accepted decision;
- exact next action;
- current stop lines;
- latest dated working-memory record.

Do not turn the rolling file into a full historical transcript.

### 18.3 Execution checklist

`docs/EXECUTION_TODO.md`

Keep the current product frontier unchanged while this plan is gated. Once activated, add only the exact currently authorized slice and its acceptance tasks; do not pre-mark future implementation as active.

### 18.4 Dated working-memory records

Create a new record under `docs/working-memory/` for every meaningful investigation/implementation/acceptance transition, especially:

- plan creation / owner intent;
- formal foundation investigation;
- target-definition contract decision;
- relevance/membership design decision;
- duplicate/repost decision;
- aggregate contract decision;
- role-family semantic experiment/acceptance;
- browser/live acceptance;
- trend-comparability decision;
- eventual Market → You prerequisite/activation decision.

Each record should state:

```text
what was attempted
what evidence was inspected
what changed
what did not change
accepted/rejected/deferred decisions
exact current state
exact next action
stop lines / unresolved risks
```

### 18.5 Experiments

Use `docs/experiments/` only for bounded model/semantic/relevance/cluster experiments whose evidence needs preservation. Experiments do not become controlling authority merely by existing.

### 18.6 Master product/architecture/domain docs

Do not broad-rewrite `PRODUCT_SPECIFICATION.md`, `ARCHITECTURE.md`, `DOMAIN_AND_ANALYSIS_MODEL.md`, `ROADMAP.md` or `IMPLEMENTATION_PLAN.md` merely because this plan exists.

Update/amend them only when an implemented/accepted durable contract changes their product meaning or architecture. If old present-tense status becomes misleading, use the repository's existing reconciliation/amendment practice rather than rewriting historical chronology.

### 18.7 Tests and regression memory

A repeatable deterministic or authority-boundary defect found during implementation should become a test when practical. One-off model wording variation should be recorded as bounded semantic evidence rather than forcing endless contract churn.

---

## 19. Initial repository mapping already established during planning

The plan was created only after confirming that the desired capability fits the current architecture rather than requiring a parallel subsystem.

Existing reusable foundations include:

```text
Acquisition
- search_registry.py
- jobinja_discovery.py
- jobinja_sync.py
- jobinja_batch.py
- phase1_run.py

Factual substrate
- current English projection
- accepted English P1.6 v20/v5
- AnalysisStore / currentness semantics

Per-job interpretation
- Capability Intelligence v9
- Job Work Intelligence v2

Reviewed normalization
- Canonical Registry v1

Current aggregate/read model
- market_insights.py
- phase1_report.py
- browser /market and report surfaces

Durable/runtime foundation
- SQLite
- source evidence/version/lifecycle model
- browser + CLI shared services
```

Current `MarketInsights` already provides a useful v1 baseline:

- deterministic aggregation over accepted current P1.6;
- requirement prevalence by distinct posting;
- required/preferred/contextual/inferred counts;
- analyzed sample size;
- distinct-employer concentration warning;
- source/filter/duplicate-policy disclosure.

The desired feature should therefore evolve JobHunter toward **target-scoped, snapshot-based Market/role-family intelligence** rather than replace this foundation.

Known gap already identified for later investigation:

```text
current Market has no repost/cross-post near-duplicate adjustment
```

Known governance boundary already identified:

```text
current Market does not silently consume Capability, Work Intelligence,
Blueprint, or speculative canonical relationships
```

Any broader use of those layers must be explicitly designed and evidence-qualified.

---

## 20. Exact next action

### Current product track — unchanged

```text
ta9l current English projection
→ ta9l English P1.6 v20 generation + semantic acceptance review
→ exact responsibility-shape report
→ final correspondence review against tG9K P1.6 36 responsibility[5]
→ possible one-concept/two-mapping B1 mutation
→ B1 closure decision
```

### Market/role-family track — plan recorded, implementation gated

```text
owner-approved feature intent recorded
→ focused plan recorded
→ rolling memory/TODO pointer recorded
→ WAIT while P2.2B-B1 remains current product gate
→ after B1 closure + explicit owner activation:
   perform Section 7 foundation investigation
→ write dated investigation record
→ reconcile/amend this plan if evidence changes the design
→ authorize the first bounded implementation slice
```

Do not begin Market-v2 source implementation, role-family promotion, personal scoring or speculative infrastructure merely because this plan now exists.
