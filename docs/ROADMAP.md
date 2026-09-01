# JobHunter Roadmap

**Status:** Current strategic roadmap  
**Date:** 2026-08-23
**Scope:** Product delivery from the current Phase-1 state through sustained personal career intelligence  
**Execution authority:** `docs/IMPLEMENTATION_PLAN.md` and active phase plans control exact implementation order and acceptance. This roadmap controls strategic sequencing and proposal disposition only when it does not conflict with those more specific execution plans.

---

## 1. Purpose

JobHunter already has a large implemented foundation and a 200-item proposal library. The purpose of this roadmap is to turn those ideas, current implementation reality, known defects, product principles, and external design lessons into one coherent delivery path.

The roadmap must prevent two failure modes:

1. **under-building** — stopping at scraping, translation, or generic job matching before JobHunter becomes a real career-intelligence system;
2. **over-building** — implementing attractive future capabilities before their data, evidence, quality, or operational prerequisites exist.

The intended mature loop is:

```text
MARKET
what employers actually ask for
    ↓
ROLE INTELLIGENCE
what work, responsibilities, requirements, technical scope, depth and capability patterns exist
    ↓
PERSONAL EVIDENCE
what the user can actually support with reviewed evidence
    ↓
GAPS / CONSTRAINTS
what is missing, shallow, stale, uncertain, blocked or merely undocumented
    ↓
LEARN / PRACTISE / BUILD / VERIFY
what action can create useful capability or evidence
    ↓
APPLICATION DECISION
which opportunities are sensible now and why
    ↓
OUTCOME
what happened and what was explicitly learned
    ↓
UPDATED EVIDENCE AND DECISIONS
    ↺
```

Job acquisition is therefore an input subsystem. Resume assistance is a downstream output. The product center is evidence-backed personal career intelligence.

---

## 2. Authority and document roles

JobHunter uses the following hierarchy:

```text
PRODUCT_SPECIFICATION.md
DOMAIN_AND_ANALYSIS_MODEL.md
SOURCE_POLICY.md
ARCHITECTURE.md
        ↓
ROADMAP.md
strategic sequencing / proposal disposition
        ↓
IMPLEMENTATION_PLAN.md
controlling delivery order and acceptance gates
        ↓
phase-specific plans
        ↓
EXECUTION_TODO.md
current operational checklist
        ↓
implementation / tests / live acceptance evidence
```

Rules:

- Product, provenance, privacy, source-policy and architectural invariants cannot be weakened by roadmap convenience.
- `IMPLEMENTATION_PLAN.md` remains the controlling exact execution order for the current active phase.
- `docs/proposals/` remains a non-controlling idea inventory. A proposal is not authorized merely because this roadmap references it.
- `EXECUTION_TODO.md` is a working checklist, not an independent source of product authority.
- If implementation reality changes, current-state documentation must be reconciled before future planning builds on a false baseline.

---

## 3. Current baseline

### 3.1 Accepted/current foundation

Current accepted/current foundations include:

- local Python modular-monolith application;
- SQLite runtime/history authority plus immutable raw evidence files;
- local browser UI and supported CLI over the same services/data;
- data-driven Persian/English Jobinja search catalog;
- bounded, repeat-safe acquisition;
- immutable search and detail evidence;
- stable logical JobPosting identity;
- semantic source versions distinct from fetch observations;
- deterministic `jobinja-detail-v2` parser and parser structural audit;
- `lm-studio-translation-v2` / `english-projection-v2` current translation boundary;
- browser Quick Add within the approved Jobinja source boundary;
- promoted/current English P1.6 `job-analysis-english-v20 / job-analysis-v5`;
- independent original-language P1.6 `job-analysis-original-v9 / job-analysis-v4`;
- promoted/current Capability Intelligence `job-capability-intelligence-v9 / job-capability-intelligence-v5`;
- Review Snapshot v1 current-chain routing;
- complete repository-safe public corpus `jobhunter-public-corpus-v1`;
- real public-corpus backfill, verification, intentional Git publication and remote inspection;
- real acquisition corpus substantially larger than the original early proof.

Accepted opposite-end semantic anchors:

```text
tG9K → P1.6 artifact 36 → Capability artifact 11
t4jp → P1.6 artifact 37 → Capability artifact 12
```

Public corpus publication baseline:

```text
Known/discovered jobs:       353
Fetched/parsed job details:   43
Current English projections:  20
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

### 3.2 Accepted Phase-1 implementation

The repository already contains, but must not over-claim before the remaining gates pass:

- classified source response/failure states;
- cautious lifecycle transitions;
- user triage and deterministic acquisition priority;
- first Market aggregation over accepted/current English P1.6;
- expanded bounded browser workflow actions;
- final run/reporting pieces;
- heterogeneous role-family non-regression for promoted P1.6 + Capability.

Blueprint v6/v5 is implemented for research/inspection but is **deferred and non-authoritative**, not merely acceptance-pending.

### 3.3 Current semantic-quality position

P1.6 v20/v5 and Capability v9/v5 are promoted/current on dense+sparse opposite-end anchors. Heterogeneous role-family validation is active before those promoted contracts are frozen as Phase-2 input.

Current order:

```text
1. Python/software          ← accepted: tmBK P1.6 39 → Capability 13
2. network/security         ← accepted: t4qV P1.6 44 → Capability 14
3. operations/platform      ← accepted: tmyX P1.6 46 → Capability 15
```

The first Python/software anchor `tmBK` has already exposed useful repeatable deterministic P1.6 edge cases around:

- recognizing `Sufficient knowledge` as explicit employer depth while plain `knowledge` remains non-depth;
- preserving item-specific depth inside a single multi-level evidence segment;
- failing closed rather than borrowing depth when multi-level evidence lacks item-specific scope;
- treating `Ability to effectively use AI ...` as application wording rather than technical depth;
- filtering only redundant coverage exclusions that contradict positive extraction of the same reference.

The first persisted `tmBK` P1.6 artifact 38 was semantically rejected and never fed Capability. Rebuilt P1.6 artifact 39 was explicitly accepted after complete source/depth review, and Capability artifact 13 then passed complete coverage and source-truth review. Python/software is closed.

Network/security `t4qV` is accepted on P1.6 44 → Capability 14 after a general certification/credential ontology clarification; artifacts 40-43 remain rejected/archived evidence. Operations/platform `tmyX` is accepted on P1.6 46 → Capability 15 after general heading-boundary, pre-heading duty-coverage, and non-depth ability/skill fixes. Heterogeneous validation, Market truthfulness, source/lifecycle, partial-success semantics, and P1.7 report/run/browser acceptance are closed. Phase 1 and P2.1 are accepted; P2.2A Job Work Intelligence semantic/product acceptance is active.

### 3.4 Current governance state

The repository has a 200-item candidate proposal library organized into fourteen families. These proposals are deliberately non-controlling and must be promoted only through explicit product/implementation decisions.

### 3.5 External reference lesson: career-ops

The career-ops project was reviewed as an external design reference. It does not become a dependency or architectural template for JobHunter. The main lessons incorporated into this roadmap are:

- broad provider/source coverage is valuable only after source contracts are reliable;
- `empty result` must never be conflated with `provider/acquisition failure`;
- transient server/network errors must never become destructive lifecycle conclusions;
- user-owned and system-owned data need explicit boundaries;
- critical safety/data-integrity invariants should be enforced in code/tests, not only duplicated prompts;
- partial-success semantics matter for long workflows;
- liveness checks should precede expensive inference when possible;
- application outcome tracking is useful, but causal claims require explicit evidence;
- application/resume/interview workflows have real user value but belong downstream of trustworthy personal evidence;
- high feature velocity without strong regression contracts creates semantic/data-integrity debt.

JobHunter deliberately does **not** adopt career-ops's file-as-primary-database model or holistic opaque fit score.

---

## 4. Permanent product and engineering rules

These rules apply across every roadmap stage.

1. Preserve source evidence before derived processing.
2. Keep source truth, translation, model interpretation, market aggregation, user workflow state and personal evidence separate.
3. Treat acquired content as untrusted data.
4. Keep deterministic calculations deterministic.
5. Prefer explicit missing/uncertain/review states over guessed certainty.
6. Version durable derived contracts and preserve historical artifacts.
7. Make consequential conclusions traceable to evidence.
8. Keep browser and CLI on one service/data model.
9. Keep acquisition independently useful when AI/model providers are unavailable.
10. Keep local-first operation as the default.
11. Keep SQLite and the modular monolith until measured limitations justify replacement.
12. Do not build a generic plugin system before at least two concrete implementations prove the abstraction.
13. Do not create a vector/RAG platform before real structured/keyword queries prove insufficient.
14. Do not derive personal capability from chat memory, repository keywords, course completion or AI-generated code without reviewed evidence.
15. Do not convert one application outcome into an invented causal explanation.
16. Do not automate application submission.
17. Do not interpret roadmap/proposal breadth as permission to implement everything.
18. Every new capability must have bounded acceptance criteria and explicit non-goals.
19. Do not replace vague employer wording with fake technical precision. Job-specific capability depth may only be as detailed as source/work evidence supports, and unknown scope remains explicit.
20. Once a semantic layer is promoted, reopen it only for repeatable material correctness/provenance/contract defects or changed dependencies, not harmless model prose variation.

---

# Part I — Immediate current work

## 5. Stage R0 — Reconcile, stabilize and finish Phase 1

**Objective:** Establish one trustworthy, accepted end-to-end Jobinja source-to-market pipeline before expanding the product surface.

**Status:** Active now.

### 5.1 Documentation/state reconciliation

Current-state documents must agree on:

```text
P1.6 English public:        v20/v5
Capability public/current:  v9/v5
Blueprint:                  deferred / non-authoritative / historical-v7-pinned
Public corpus:              operationally closed / remotely available
Heterogeneous review:       active
Phase 2:                    blocked
```

Historical experiment/incident files remain historical and must not be rewritten as though they were current contracts.

### 5.2 Current controlling Phase-1 sequence

The exact execution order is controlled by `docs/IMPLEMENTATION_PLAN.md`, `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`, and `docs/EXECUTION_TODO.md`.

Current high-level sequence:

```text
rebuild/review tmBK P1.6
→ if accepted, review tmBK Capability v9
→ close Python/software heterogeneous anchor
→ network/security heterogeneous anchor
→ operations/platform/DevOps heterogeneous anchor
→ freeze promoted P1.6 + Capability as Phase-2 input if stable
→ Market truthfulness acceptance
→ source/lifecycle acceptance
→ partial-success acceptance closed
→ P1.7 final run/report/browser acceptance closed
→ Phase-1 closure accepted
→ P2.1 canonical concept registry
```

### 5.3 Promote selected proposal safeguards into current acceptance

These proposals remain useful **now as engineering/acceptance requirements**, not as large new product subsystems:

- **B087 — Corpus health summary**: expose layer-specific coverage where operationally useful;
- **B102 — Rich operation results**: show requested/attempted/completed/reused/failed/remaining work;
- **B104 — Partial-success semantics**: avoid generic success when a multi-stage run partially failed;
- **B118 — Regression corpus**: every important real defect becomes a durable offline test fixture;
- **B120 — Fault simulation**: test 429/5xx/timeout/challenge/provider/model failure boundaries;
- **B121 — Model chaos testing**: test structurally plausible but dangerous model output;
- **B178/B179 — untrusted-content / evidence-poisoning tests**: source text never receives instruction authority;
- **B187 — Representative review sampling**: the reviewed sample intentionally varies across role/company/language/length/requirement density where the corpus permits;
- **B190 — Sampling warnings**: the Market UI must qualify small or concentrated analyzed subsets.

### 5.4 External failure classes to encode as JobHunter regression scenarios

JobHunter must explicitly protect these invariants:

```text
source/provider failure != legitimate empty result
500/502/503/504 != expired/removed
challenge/auth/access failure != vacancy gone
rate limit != vacancy unavailable
Unicode normalization must not collapse distinct identities
partial persistence != operation success
new lower/worse analysis must not be silently ignored merely because an older result looked better
prompt wording alone must not be the only enforcement of a critical invariant
one source depth marker must not spread to neighboring concepts
non-depth application/scope wording must not become technical depth
```

### 5.5 Phase-1 definition of done

R0/Phase 1 is complete only when:

- deterministic checks are green;
- current source/translation/migration behavior is explainable and non-destructive;
- promoted P1.6 + Capability pass the bounded heterogeneous representative sample;
- unsupported model evidence is rejected reliably;
- lifecycle failure classes do not create destructive conclusions;
- Market outputs show exact sample scope and warning state;
- browser and CLI expose the same underlying result semantics;
- the final bounded Phase-1 run/report path exists and is live-accepted;
- documentation reflects actual accepted and non-accepted state;
- the accepted P1.6 + Capability starting contract for Phase 2 is explicitly frozen.

**Gate:** No corpus-wide Phase-2 semantic/taxonomy or multi-source expansion becomes controlling work until this stage passes.

---

# Part II — Core career-intelligence construction

## 6. Stage R1 — Canonical semantic market model (Phase 2 core)

**Objective:** Convert accepted job-level semantic claims into reviewed reusable market concepts and job-specific capability requirement profiles without flattening the market into keyword frequencies or vague depth adjectives.

### 6.1 Canonical concept registry

Build the smallest useful reviewed taxonomy for:

- tools/platforms/frameworks/languages;
- applied skills;
- knowledge areas;
- practices;
- domains;
- experience signals;
- education/credential signals;
- responsibilities;
- deliverables.

Primary proposal inputs: B013, B014, B015, B020, B021, B022, B028, B029.

### 6.2 Alias and mapping review

Support reviewed mappings such as:

```text
Postgres -> PostgreSQL
K8s -> Kubernetes
LLM -> Large Language Model
```

Preserve source wording and mapping provenance. Do not silently mutate taxonomy from model proposals.

Primary proposal inputs: B029, B030, B160.

### 6.3 Responsibility families and role archetypes

Build upward from actual accepted responsibilities:

```text
source responsibility
→ canonical responsibility
→ responsibility family
→ evidence-derived role archetype
```

Do not force every job into a predeclared role taxonomy.

Primary proposal inputs: B016, B017, B018, B019, B023.

### 6.4 Technology/capability relationships

Add only relations that support real decisions:

- co-occurrence;
- capability bundles;
- broad-to-narrow capability/sub-capability relations;
- prerequisite knowledge relations;
- substitution/family relations;
- tool-versus-underlying-capability relations;
- responsibility/deliverable-to-capability relations.

Keep prerequisite relations distinct from market co-occurrence. A common association such as Docker + Kubernetes must never imply Kubernetes is part of every Docker requirement.

Primary proposal inputs: B024-B028.

### 6.5 Job capability requirement and depth intelligence

Build a first-class **JobCapabilityRequirementProfile** for material capabilities in a vacancy.

The goal is not merely:

```text
Docker -> required -> advanced
```

The goal is to answer:

```text
What must the employee know?
What must the employee understand?
What must the employee be able to do?
Which parts/sub-capabilities of the broad technology are supported?
In what work context?
With what independence/ownership?
At what operational complexity?
What is explicit, strongly work-implied, inferred, or unknown?
Why do we believe each part?
```

#### Inputs

Use the complete accepted evidence set available for the job, including:

- P1.6 responsibilities;
- explicit requirements and strength;
- deliverables;
- source-explicit experience/seniority wording;
- deterministic job context;
- canonical concept mappings;
- responsibility/deliverable-to-capability relations;
- supported company/product/team context when available;
- bounded lessons from accepted Capability v9 grouping/source-truth behavior where they remain evidence-qualified.

Company context is supporting evidence only. Do not manufacture requirements from stereotypes such as `startup means broad ownership` or `enterprise means narrow specialization`.

#### Required profile dimensions

For each material capability preserve where evidence supports it:

```text
canonical capability
exact employer wording
employer requirement strength
employer-stated depth wording
expected work activities
expected deliverables
technical scope / sub-capabilities
underlying knowledge / practices
expected independence / ownership
complexity / production context
explicit duration/experience signals
responsibility links
deliverable links
supported company/product/team context
source-explicit evidence
inference rationale
confidence
unknown / unsupported scope
review state
contract version
```

#### Evidence status per expectation

Fine-grained expectations must distinguish at minimum:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

An inferred prerequisite must carry rationale and provenance. It must never be shown as employer-explicit wording.

#### Depth model

Do **not** make a single beginner/intermediate/advanced/expert number the primary model.

Keep these signals separate:

1. employer-stated depth wording;
2. work-implied depth/scope;
3. technical sub-capability coverage;
4. expected independence/ownership;
5. complexity/operational/production context;
6. confidence and unknown scope.

Only introduce a summary job-depth category after reviewed examples show that it is stable and decision-useful. The multidimensional profile remains the authoritative derived representation.

#### Example behavior

If a posting only says `Docker required`, the correct profile may be:

```text
Docker is explicitly required.
Specific technical scope: insufficient evidence.
Unknown: Compose, networking depth, registries, security hardening, orchestration, internals.
```

If responsibilities also say `containerize services`, `maintain CI/CD pipelines` and `troubleshoot production deployments`, the profile may support narrower expectations such as Dockerfile/image work, container runtime configuration, deployment integration and troubleshooting—each with evidence status and confidence.

Likewise, `expert Python` must be interpreted through the actual work. A role centered on async APIs, tests and production debugging should produce a different Python capability profile from a role centered on scientific numerical computing or ML experimentation.

#### Acceptance

Do not scale this layer until reviewed examples across broad and narrow capabilities demonstrate that:

- sub-capabilities are supported by evidence rather than generic model knowledge;
- vague adjectives do not create fake technical precision;
- responsibilities/deliverables materially improve interpretation;
- explicit vs implied vs inferred vs unknown remains correct;
- unsupported sub-capabilities are omitted or marked unknown;
- profile changes are versioned and reversible;
- a reviewer can trace every material expectation back to job evidence and reasoning.

Primary proposal inputs: B013-B030, especially B020-B028.

### 6.6 Market aggregation v2

Every market aggregate must expose:

- posting count;
- distinct employer count where available;
- required/preferred/contextual/inferred distribution;
- role/archetype scope;
- source scope;
- sample size;
- current analysis/taxonomy/capability-profile contract;
- duplicate/repost adjustment state;
- warning when claims exceed evidence quality.

Where capability-depth profiles are aggregated, keep employer-explicit signals separate from work-implied/model-inferred signals and expose support counts before presenting a technical scope pattern as market-wide.

Primary proposal inputs: B031, B086-B089, B188-B195.

### 6.7 Review and reversibility

Introduce claim/taxonomy/capability-profile review only where real P1.6/Phase-2 errors justify it. Corrections append/supersede; they do not destroy original model history.

Review must allow individual sub-capability, evidence-status, independence/context and work-link corrections without rewriting original employer/P1.6 evidence.

Primary proposal inputs: B007-B010, B184.

### 6.8 Phase-2 core gate

Do not advance to personal gap intelligence until:

- canonical mappings are reviewable;
- responsibility families/archetypes have representative reviewed examples;
- job capability requirement profiles have representative reviewed examples across multiple broad/narrow capability types;
- fine-grained technical expectations preserve explicit/implied/inferred/unknown boundaries;
- unsupported scope remains unknown rather than model-filled;
- aggregate counts reproduce from accepted claims;
- duplicate aliases do not inflate demand;
- sample scope is visible;
- every aggregate can drill back to job-level evidence;
- the job-side requirement model is stable enough to compare against future personal evidence without pretending it is the personal 0–7 scale.

---

## 7. Stage R2 — Multi-source acquisition and longitudinal source intelligence

**Objective:** Expand market coverage without weakening source-policy, evidence or lifecycle guarantees.

This stage may begin after Phase 1 acceptance and can overlap bounded Phase-2 semantic work when the downstream contracts are stable enough.

### 7.1 Select exactly one second source

Choose a source because it adds repeated-use market value, not because a provider list looks impressive.

Preference order remains:

1. official public API/feed;
2. public ATS endpoint;
3. embedded structured data;
4. static public HTML;
5. rendered public page only when explicitly approved and necessary.

### 7.2 Implement source-specific behavior first

For the second source define explicitly:

- stable identity;
- discovery;
- detail retrieval;
- evidence preservation;
- response classification;
- lifecycle semantics;
- rate/bounds policy;
- field normalization;
- tests;
- live acceptance.

### 7.3 Extract a minimal SourceAdapter contract only after two real sources

Possible capability-oriented operations:

```text
discover()
fetch_detail()
classify_response()
canonicalize_identity()
source_capabilities()
```

Avoid dynamic third-party plugin loading initially.

Primary proposal inputs: B002, B170.

### 7.4 Search/source effectiveness intelligence

Track:

```text
search/source
→ discoveries
→ unique contribution
→ duplicates/overlap
→ successful detail acquisition
→ accepted semantic analysis
→ later reviewed target/opportunity value
```

Recommendations to alter search coverage remain human-approved.

Primary proposal inputs: B003, B158, B161.

### 7.5 Duplicate/repost and richer lifecycle

Build duplicate/repost relations as derived evidence without deleting source postings.

Distinguish:

- exact duplicate;
- probable repost;
- similar recurring vacancy;
- changed semantic version;
- unavailable/removed/returned states.

Primary proposal inputs: B004-B006, B192.

### 7.6 Multi-source gate

Do not scale to many sources until:

- the second adapter passes policy and live acceptance;
- downstream analysis remains source-agnostic where appropriate;
- source-specific semantics are not erased by normalization;
- failure and empty-result states remain distinguishable;
- duplicate/repost logic has an explicit confidence/review path.

---

## 8. Stage R3 — Personal Evidence Platform (Phase 3)

**Objective:** Model the user through inspectable evidence rather than resume keywords, chat memory or optimistic self-assessment.

### 8.1 Data ownership/privacy contract before personal evidence

Formalize data classes:

```text
system/application data
public market evidence
public derived intelligence
user workflow state
personal capability evidence
private notes
secrets
rebuildable exports/indexes
```

For each class define:

- canonical store;
- backup/restore behavior;
- export policy;
- AI processing policy;
- remote-processing eligibility;
- deletion/retention behavior.

Primary proposal inputs: B108-B113, B176, B183.

### 8.2 Personal Evidence Ledger

Create the smallest credible schema:

```text
PersonalCapability
- canonical concept/activity
- depth
- confidence
- recency
- limitations
- review state

CapabilityEvidence
- evidence type
- source/reference
- date
- demonstrated behavior
- AI-assistance / independence context
- strength and limitations
```

Primary proposal inputs: B041-B047.

### 8.3 Depth, confidence and recency remain separate

Use an ordinal depth scale instead of `knows/doesn't know`. A current proposed model is:

```text
0 Unassessed
1 Awareness
2 Introductory understanding
3 Guided practice
4 Independent bounded execution
5 Integrated application
6 Repeated independent evidence
7 Production / production-like operation
```

Confidence in an assessment must not be confused with depth itself.

This personal scale describes evidence about the user. It is intentionally distinct from the multidimensional job-side capability requirement profile built in Phase 2.

### 8.4 Manual evidence workflow first

Before automatic importers:

- create/inspect evidence manually;
- review capability interpretation;
- correct depth/limitations;
- prove versioning/history;
- prove privacy/backup behavior.

Only then consider GitHub/project evidence import as **candidate evidence generation**, never automatic proficiency.

Primary proposal inputs: B043, B054.

### 8.5 Market-to-person mapping

Map reviewed personal capabilities to canonical market concepts and job-required activities/sub-capabilities with explicit relations such as exact, broader, narrower or partial.

Semantic similarity may propose a mapping but cannot silently declare equivalence.

A broad personal concept match does not automatically satisfy every job-specific technical activity under that concept.

Primary proposal input: B048.

### 8.6 Phase-3 gate

No readiness/gap recommendation becomes authoritative until:

- every personal claim has reviewed evidence;
- depth/confidence/recency/limitations are preserved;
- AI-assisted work can be represented honestly;
- personal data processing/export policy is explicit;
- backup/restore protects irreplaceable evidence;
- market↔personal mappings are inspectable and correctable;
- job-required activities/sub-capabilities can be compared to personal evidence without collapsing them into concept-name equality.

---

## 9. Stage R4 — Gap, readiness and action intelligence (Phase 4)

**Objective:** Explain what differs between target-market expectations and personal evidence, then choose useful actions without fake precision.

### 9.1 Gap taxonomy

Distinguish at minimum:

```text
knowledge
practice
depth
integration
production evidence
recency
presentation/evidence
experience context
credential
constraint mismatch
unknown evidence
```

Unknown is not automatically a negative capability claim.

Primary proposal inputs: B049-B050.

### 9.2 Requirement-by-requirement comparison

Prefer inspectable comparison over one global score. Where Phase-2 capability profiles exist, compare at activity/sub-capability level rather than concept name alone:

```text
Requirement | Job scope/activity              | Personal evidence      | Assessment
Python      | async API implementation        | repeated evidence      | strong
Docker      | production troubleshooting      | guided/basic evidence  | partial
Kubernetes  | preferred deployment context    | introductory           | weak
SOC ops     | incident workflow ownership     | no reviewed proof      | unknown/major gap by policy
```

A person may have strong general evidence for Docker while lacking the exact networking/troubleshooting/CI activity required by one vacancy.

Primary proposal inputs: B051-B053, B135-B136.

### 9.3 Explainable categorical readiness

Candidate outputs:

- apply now;
- reasonable to apply;
- targeted preparation recommended;
- major required gaps;
- insufficient evidence.

Every result must show supporting evidence, blockers, uncertainty and applied policy.

Do not introduce an opaque `83% fit` score unless a future calibrated method proves meaningful.

### 9.4 Learning/action priority

Prioritize using transparent factors:

- target-role relevance;
- requirement strength;
- job-specific activity/sub-capability gaps;
- market prevalence;
- dependency/prerequisite structure;
- personal depth gap;
- evidence-building value;
- current constraints.

Outputs may include:

```text
learn
practise
integrate
build evidence
document existing work
assess current capability
monitor
ignore for now
```

Recommendations should target the missing activity when possible rather than telling the user to relearn an entire broad technology.

Primary proposal inputs: B061-B067, B134.

### 9.5 Career scenarios and constraints

Represent target roles, adjacent roles, geography/work-mode constraints and preference strength separately from capability evidence.

Support multiple scenarios over one shared market/evidence base.

Primary proposal inputs: B137-B141.

### 9.6 Challenge and counterfactual analysis

Add only after normal gap decisions are stable:

- challenge overly optimistic or negative recommendations;
- show what evidence would change the conclusion;
- simulate hypothetical capability improvements without pretending they already exist;
- compare path/project opportunity cost transparently.

Primary proposal inputs: B130-B133, B142-B144.

### 9.7 Phase-4 gate

Every consequential recommendation must answer:

```text
what evidence supports it?
what evidence contradicts it?
what is uncertain?
what policy was applied?
what action follows?
what would change the conclusion?
```

---

# Part III — Opportunity workflow and sustained operation

## 10. Stage R5 — Application, interview and opportunity workspace

**Objective:** Use the evidence system to help pursue real opportunities without fabricating claims or automating submission.

### 10.1 Application Evidence Pack first

For one selected opportunity produce a versioned package containing:

- employer responsibilities/requirements;
- job-specific capability scope/depth where available;
- strongest matching personal evidence;
- partial/critical gaps;
- constraints/unknowns;
- relevant projects;
- interview-preparation domains;
- exact provenance and artifact versions.

Primary proposal input: B071.

### 10.2 Evidence-constrained resume targeting

Generated wording must trace to approved evidence. Never invent:

- years;
- titles;
- metrics;
- production scale;
- ownership;
- technologies;
- independence.

Primary proposal input: B072.

### 10.3 Interview preparation

Build from employer evidence, job capability profiles and personal evidence:

```text
requirement / required activity
→ concepts to explain
→ strongest real example
→ missing preparation
→ synthetic self-test questions
```

Primary proposal inputs: B068-B070.

### 10.4 Application tracking

Separate a neutral workflow tracker from later outcome intelligence.

Neutral application state may include:

```text
considering
preparing
applied
screening
technical_interview
final_interview
rejected
withdrawn
offer
closed_unknown
```

This state is user-owned and distinct from source lifecycle.

Primary proposal input: B073.

### 10.5 Outcome learning with causal restraint

Store:

```text
outcome
explicit feedback if any
reason unknown when no reason is supplied
```

Never infer `rejected because X` merely because X was a known gap.

Primary proposal inputs: B074-B075.

### 10.6 Opportunity watch

Only after target roles, repeated acquisition and job-level comparison are mature, surface meaningful new/changed opportunities with explicit reasons.

Primary proposal input: B076.

### 10.7 Permanent boundary

No autonomous application submission or recruiter messaging.

---

## 11. Stage R6 — Longitudinal intelligence and sustained operation

**Objective:** Make JobHunter useful repeatedly over months/years without fragile manual maintenance.

### 11.1 Durable workflow history and partial success

Add lightweight durable workflow/run records only when current operation history becomes insufficient.

Primary proposal inputs: B103-B105.

### 11.2 Reproducible market snapshots

Freeze analytical manifests containing:

- eligible job/source versions;
- source/filter scope;
- analysis contract;
- taxonomy/capability-profile version;
- creation time.

Primary proposal input: B114.

### 11.3 Market trends and drift

Only after longitudinal data and duplicate/lifecycle quality are adequate:

- period-over-period market change;
- emerging capability detection;
- stability classification;
- company/role/geographic change;
- changes in recurring required activities/sub-capabilities where evidence coverage is sufficient;
- career-market drift relative to personal evidence.

Primary proposal inputs: B032-B040, B159-B163.

### 11.4 Scheduling

Schedule only workflows already proven bounded, idempotent and safe manually.

Primary proposal input: B106.

### 11.5 Notifications/change summaries

Prefer meaningful in-app change summaries over high-frequency noise.

Primary proposal inputs: B077, B098, B107.

### 11.6 Backup, restore, portability and packaging

Before JobHunter contains years of irreplaceable personal evidence, provide tested backup/restore. Later add workspace portability and packaging when repeated-use friction justifies them.

Primary proposal inputs: B112-B113, B174-B176.

### 11.7 Sustained-operation gate

Prove repeated operation without:

- duplicate logical jobs;
- silent stale derived artifacts;
- destructive lifecycle guesses;
- unreported partial failures;
- unrecoverable migrations;
- irreplaceable unbacked-up personal evidence.

---

# Part IV — Advanced intelligence only when justified

## 12. Stage R7 — Evaluation Lab, retrieval, assistant and bounded AI workers

**Objective:** Add advanced AI infrastructure only after structured JobHunter knowledge is strong enough to evaluate whether it helps.

### 12.1 Evaluation foundation before model proliferation

Start small with:

- translation golden examples;
- representative P1.6 gold jobs;
- reviewed job capability requirement/depth examples once Phase 2 begins;
- regression fixtures;
- human annotations for high-value cases;
- exact contract identity;
- candidate-versus-baseline evaluation.

Primary proposal inputs: B011-B012, B116, B159, B167-B169, B185-B187.

### 12.2 Multi-provider/task-specific routing

Introduce additional inference providers only when there is a measured quality, privacy, latency or cost reason.

Different tasks may eventually use different models, but the single-model/local configuration must remain valid.

Primary proposal inputs: B123-B125, B171.

### 12.3 Structured query before RAG

For natural-language questions:

```text
question
→ bounded intent/query plan
→ approved structured/keyword query
→ deterministic result
→ optional grounded synthesis
```

Primary proposal inputs: B093-B095.

### 12.4 Semantic retrieval only after demonstrated need

Add embeddings/retrieval when reviewed real queries cannot be served well by structured/keyword search. Version embedding/chunking/retrieval contracts and keep indexes derived/rebuildable.

Primary proposal inputs: B126-B129.

### 12.5 Evidence-backed assistant

A future assistant may retrieve JobHunter market/personal evidence and explain it conversationally, but conversational memory never becomes durable personal truth.

Primary proposal inputs: B094-B098.

### 12.6 Bounded specialist workers

If specialist AI workers are introduced, each must have:

- narrow inputs;
- narrow tools;
- explicit model/provider route;
- versioned prompt/schema;
- deterministic validation where possible;
- budgets;
- review requirements;
- no unrestricted shell/filesystem/browser/network access.

### 12.7 Explicitly deferred infrastructure

Do not introduce merely for sophistication:

- autonomous agent swarms;
- vector database before a measured need;
- graph database when relational traversal suffices;
- distributed services/message brokers;
- generic workflow DSL;
- self-training on unverified model generations.

---

# Part V — Product experience across stages

## 13. UX evolution

The browser remains the normal user interface. Add product domains only when underlying capability exists.

Likely mature information architecture:

```text
Market
Jobs
Roles
Me
Gaps
Learning
Applications
Research
System
```

Do not create empty future navigation.

Useful UX proposals by maturity:

### Near term

- rich operation results;
- corpus-health view;
- sampling/uncertainty labels;
- operation links to affected jobs;
- clearer stale/current states.

### Mid term

- per-job capability requirement/depth profile showing required activities, sub-capabilities, evidence status and unknown scope;
- saved views;
- multi-job comparison;
- role/company comparisons;
- unified review inbox when at least three real review workflows exist;
- job timeline / lineage trace.

### Later

- market heatmaps;
- co-occurrence network visualization;
- role-family maps;
- Personal Career Cockpit;
- generated charts/reports.

Primary proposal inputs: B077-B085, B099-B102.

---

## 14. Cross-cutting architecture and developer knowledge

JobHunter should remain understandable as it grows.

Promote lightweight engineering knowledge where it prevents recurring mistakes:

- trace one job end-to-end from acquisition to current derived output;
- focused architecture diagnostics;
- concise comments/docstrings around non-obvious invariants;
- lightweight ADRs only for major cross-cutting decisions;
- incident notes only for failures that change contracts/architecture or create reusable lessons.

Keep these as support capabilities, not a second product.

Primary proposal inputs: B148-B154.

Logical knowledge-graph thinking is useful, but relational tables/foreign keys remain the implementation default. Primary proposal inputs: B145-B146, B173.

---

# Part VI — Proposal disposition

## 15. How the 200 proposals map into roadmap capability programs

The proposal IDs remain stable traceability references. They should not become 200 implementation tickets.

### Program A — Product identity and decision loop

B001, B137-B147, B200.

### Program B — Acquisition/source intelligence

B002-B006, B158, B161, B170.

### Program C — Evidence, provenance, review and trust

B007-B010, B086-B092, B145, B184.

### Program D — AI evaluation and experimentation

B011-B012, B116, B121, B123-B129, B159-B160, B167-B169, B185-B187.

### Program E — Semantic role/taxonomy/requirement model

B013-B030.

This program includes the job capability requirement/depth intelligence layer: broad concepts, work activities, sub-capabilities, prerequisites, tool-versus-underlying-capability relations, experience/depth signals and reviewed evidence boundaries.

### Program F — Market/company/geography/measurement intelligence

B031-B040, B155-B157, B162-B163, B188-B196.

### Program G — Personal evidence and portfolio intelligence

B041-B048, B054, B164-B166, B177, B197-B199.

### Program H — Gap/readiness/learning/project prioritization

B049-B053, B055-B067, B130-B136.

### Program I — Application/interview/opportunity workflow

B068-B076.

### Program J — Product UX/review/visualization

B077-B085, B099-B102.

### Program K — Query/reporting/career assistant

B093-B098.

### Program L — Operations/reliability/testing/observability

B103-B107, B114-B115, B117-B120, B122.

### Program M — Privacy/security/backup/portability

B108-B113, B174-B176, B178-B183.

### Program N — Architecture/developer knowledge

B146, B148-B154, B171-B173.

No proposal is implemented merely by being listed here. Promotion happens through the current implementation plan and active phase plan.

---

## 16. Current proposal disposition

### Promote into current hardening/acceptance

```text
B087 Corpus health summary
B102 Rich operation results
B104 Partial-success semantics
B118 Regression corpus
B120 Fault simulation
B121 Model chaos testing
B178 Red-team untrusted acquired content
B179 Evidence-poisoning tests
B187 Representative review sampling
B190 Sampling warnings
```

These should normally be implemented as bounded acceptance/reliability improvements, not separate platforms.

### Selected direction after Phase 1

```text
B002 Multi-source acquisition
B003 Search effectiveness
B004 Repost/near-duplicate identity
B006 Rich lifecycle
B013-B030 Semantic/taxonomy backbone, including job-specific capability scope/depth intelligence
B031 Market Snapshot
B086-B089 Trust/quality surfaces
B114 Reproducible snapshots
B117 Artifact-staleness explanation
B158 Source/parser drift
B160 Taxonomy drift
B161 Search drift
B170 Source adapter contract
B188-B195 Market quality/statistics controls
```

### Phase-3 foundation

```text
B041-B048 Personal evidence model
B054 Evidence portability
B108-B113 Privacy/data/backup boundaries
B164-B166 Longitudinal evidence/progress safeguards
```

### Phase-4 decision/action foundation

```text
B049-B053 Gap/readiness comparison
B055-B067 Learning/evidence actions
B130-B145 Counterfactual/decision/scenario capabilities
```

### Phase-5 opportunity workflow

```text
B068-B076 Application/interview/outcome workflow
```

### Deliberately wait for demonstrated need

```text
large RAG/agent infrastructure
semantic vector retrieval
multi-provider routing beyond current need
graph database
complex visualization infrastructure
high-frequency scheduling/notifications
advanced ROI simulators
Career Digital Twin as a technical subsystem
```

---

# Part VII — Stop lines and success criteria

## 17. Stop lines

Stop and repair rather than continuing when any of these occur:

- source/provider failure is being represented as valid empty data;
- transient failures are changing lifecycle state destructively;
- accepted model artifacts cannot trace material claims to evidence;
- a job capability profile expands a broad technology into unsupported sub-capabilities or presents model knowledge as vacancy evidence;
- a vague employer adjective is being converted into fake exact depth without responsibility/deliverable/context support;
- explicit, work-implied, inferred and unknown capability expectations are being collapsed together;
- one depth adjective is being spread across neighboring concepts;
- non-depth scope/application wording is being persisted as technical depth;
- a mechanically completed artifact is being treated as semantically accepted without review where the active gate requires review;
- a rejected upstream artifact is allowed to feed a downstream authority layer;
- a new contract silently reuses incompatible historical artifacts;
- browser and CLI mutate different durable state;
- personal evidence is being inferred without user-reviewed provenance;
- market claims hide denominator/source/sample scope;
- a proposal requires an abstraction whose second concrete use does not exist;
- a new AI layer cannot be evaluated against representative evidence;
- automation can perform more work than the user-configured bounds imply;
- an application/resume feature can create claims that cannot be mapped to personal evidence;
- a roadmap item expands implementation scope before its prerequisite gate passes.

---

## 18. Product-level success standard

JobHunter is not successful because it has many sources, many models, many agents, many charts or a large database.

The mature system succeeds when it can repeatedly answer, with inspectable evidence:

1. What does the selected market actually ask people to do?
2. For important capabilities in a specific job, what technical activities/sub-capabilities, independence and operational depth does the evidence actually support, and what remains unknown?
3. Which responsibilities, requirements and capability bundles are stable or changing?
4. Which role families are real in the observed corpus despite inconsistent titles?
5. What reviewed evidence does the user have for those capabilities and activities, and at what depth?
6. Which differences are knowledge gaps, practice gaps, depth gaps, evidence gaps, experience-context gaps, stale evidence, constraints or unknowns?
7. Which next action has the strongest evidence-based rationale?
8. Which opportunities are reasonable now, which need preparation, and why?
9. What explicitly changed after learning, building, applying or receiving real feedback?
10. Can every consequential conclusion be traced back through the relevant market and personal evidence?

That is the target against which roadmap proposals should be accepted, deferred, merged or rejected.
