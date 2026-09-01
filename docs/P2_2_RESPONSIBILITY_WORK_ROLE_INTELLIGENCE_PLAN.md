# P2.2 Responsibility, Work, and Role Intelligence Plan

**Status:** APPROVED / CONTROLLING FOCUSED PLAN — P2.2A IMPLEMENTED / ACTION-AUTHORITY REPRESENTATION AMENDMENT REQUIRED
**Date:** 2026-09-01
**Scope:** P2.2 responsibility/work interpretation, selective responsibility/deliverable promotion, responsibility families, and role-archetype intelligence  
**Authority:** Subordinate to `docs/PRODUCT_SPECIFICATION.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, `docs/SOURCE_POLICY.md`, `docs/ARCHITECTURE.md`, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md` plus its 2026-08-26 amendment, and `docs/IMPLEMENTATION_PLAN.md` plus its 2026-08-26 amendment  
**Previous gate:** P2.1 Canonical Concept Registry — CLOSED / ACCEPTED  
**Current gate:** P2.2A Job Work Intelligence v1 — IMPLEMENTED / ACCEPTANCE OPEN / cross-job action-authority representation blocker verified

---

## 1. Objective

P2.2 exists to answer a practical user question:

> **What does this job actually involve, and what kind of work/role does it appear to be?**

JobHunter should answer that question substantially faster than manual vacancy-by-vacancy reading while preserving the distinction between employer facts and JobHunter interpretation.

The P2.2 backbone is:

```text
accepted/current factual job substrate
        ↓
fast job-level work interpretation
        ↓
candidate semantic structure
        ↓
selective reviewed promotion when reuse needs authority
        ↓
stable responsibility families / role archetypes where justified
```

P2.2 is **not** a program to canonicalize every responsibility before useful intelligence can exist.

---

## 2. Governing product and epistemic rules

P2.2 follows these permanent rules.

### 2.1 Optimize for user comprehension, not annotation completeness

The primary success question is:

> Does JobHunter reduce the time and cognitive effort needed to understand the work structure of a vacancy while remaining honest about evidence and uncertainty?

A larger mapping count is not success by itself.

### 2.2 Preserve four epistemic levels

```text
1. source fact
2. normalized correspondence
3. analytical interpretation
4. recommendation / decision synthesis
```

P2.2 primarily operates at levels 1-3. Personal recommendations remain outside this phase.

### 2.3 Candidate is not promoted

```text
candidate/generated interpretation
≠
reviewed/promoted reusable authority
```

A generated work theme or candidate role archetype may be shown immediately when traceable and correctly labeled. It does not silently become canonical taxonomy.

### 2.4 Fail hard for integrity, soft for interpretation

Hard failures include invalid dependencies, fabricated source references, corrupt persistence, stale-as-current state, privacy violations, and invalid canonical promotion.

Interpretive ambiguity should normally produce lower confidence, alternatives, or explicit unknowns rather than blocking useful output.

### 2.5 Determinism protects authority; it does not replace reasoning

Deterministic code owns dependency/currentness identity, source indices, exact evidence linkage, persistence invariants, review state, and promoted canonical membership.

Semantic/model reasoning may own work-theme grouping, role characterization, likely deliverables, candidate families, and candidate archetypes.

---

## 3. Exact input authority

### 3.1 P2.2A primary input

The first implementation reads **accepted/current English P1.6 v20/v5** only:

```text
job-analysis-english-v20 / job-analysis-v5
```

Primary factual fields:

- `role_purpose`;
- `responsibilities`;
- requirements only as supporting context;
- exact P1.6 claim indices/evidence;
- exact source/translation/P1.6 dependency identity already preserved by P1.6.

A P1.6 artifact must be both semantically accepted and current for its source dependency before it can produce current P2.2A intelligence.

### 3.2 Capability v9 relationship

Capability v9 remains accepted and useful, but **P2.2A does not depend on Capability v9 as an authoritative input**.

Reason:

- P2.2A should reason directly from the frozen factual P1.6 work substrate;
- this avoids unnecessary coupling to Capability grouping/prose;
- Capability v9 may later be displayed or compared as supporting context where useful;
- Capability model-owned explanatory prose never becomes P2.2 authority automatically.

P2.2A initially reuses the existing configured Capability reasoning-model fallback chain to avoid creating a new configuration surface before real usage demonstrates a need. This is model-runtime reuse only: Work Intelligence has its own prompt/schema/artifact identity and does not consume Capability artifacts as authority.

### 3.3 Existing canonical registry relationship

P2.1 registry state may be attached opportunistically when an exact accepted/current mapping already exists, but missing canonical mappings never block P2.2A.

P2.2A must work even when zero relevant responsibility mappings have been promoted.

### 3.4 Evidence boundary for work claims

A **work theme** in v1 must own at least one accepted P1.6 responsibility or role-purpose reference.

Requirements may strengthen or contextualize a theme, but requirement-only evidence must not be converted into an employer duty.

Permanent v1 rule:

```text
qualification / technology mention alone
!=
work responsibility
```

If a job has no accepted responsibility or role-purpose evidence, P2.2A must not fabricate a work composition from qualifications. It should return a useful limitation state and preserve any requirement-side context separately.

---

## 4. P2.2A — Job Work Intelligence v1

### 4.1 Product output

For one eligible job, JobHunter should be able to show:

- concise work-character summary;
- primary work themes;
- supporting work themes;
- the exact responsibilities/role-purpose evidence supporting each theme;
- likely deliverables where supported;
- a candidate job-level role/archetype interpretation when work evidence supports one;
- alternative role interpretation where materially plausible;
- confidence and ambiguity/unknown notes;
- explicit distinction between employer facts and JobHunter interpretation.

Example shape, not exact required wording:

```text
What this job appears to involve

Primary work
- Network-security architecture and implementation
- Firewall/security-platform operation
- VPN / segmentation / availability engineering

Supporting work
- Security troubleshooting
- Security-policy implementation
- Technical documentation

Candidate role interpretation
- Network-security engineering with a strong firewall/platform-operations component

Confidence
- high

Why JobHunter thinks this
- responsibility[...]
- responsibility[...]

Unknown / ambiguous
- exact split between architecture ownership and routine operations is not stated
```

### 4.2 No fake percentages

P2.2A does not assign invented percentages such as `40% architecture / 30% operations`.

Relative emphasis uses bounded semantic classes:

```text
primary
supporting
uncertain
```

Percentages require a later defensible measurement rule and are out of scope for v1.

### 4.3 Confidence

Use simple field-specific confidence:

```text
high
medium
low
```

Confidence is interpretive support strength, not a probability calibration claim.

Low confidence does not automatically suppress an interpretation if the interpretation remains useful and clearly qualified.

### 4.4 Candidate role interpretation

A job-level candidate archetype/role characterization may be generated from one job.

It must:

- be presented as JobHunter interpretation, not employer wording;
- link to supporting work themes/evidence;
- include confidence;
- allow alternatives;
- make no market-prevalence claim;
- remain separate from any future promoted stable archetype.

### 4.5 Deliverable candidates

P2.2A may emit deliverables only with one of these evidence states:

```text
source_explicit
strongly_implied_by_work
```

Rules:

- `source_explicit` requires actual accepted work/source evidence describing the output/outcome;
- `strongly_implied_by_work` requires one or more linked responsibility references plus a rationale;
- generic tool knowledge alone cannot manufacture a deliverable;
- ambiguous deliverables may be omitted or shown with lower confidence;
- candidate deliverables are not automatically canonical registry concepts.

### 4.6 Insufficient direct work evidence

A job with no accepted responsibilities/role-purpose must not fail the entire product view.

Expected result:

```text
work evidence status: limited
work themes: none or intentionally limited
candidate archetype from work: unavailable
reason: accepted vacancy analysis contains no direct responsibility/role-purpose evidence
requirements remain inspectable through existing factual views
```

This is a successful bounded outcome, not an operation error.

`tmBK` is the first intentional negative/limited-work anchor for this behavior.

---

## 5. P2.2A persisted candidate artifact decision

### 5.1 Decision

P2.2A persists a versioned **candidate analytical artifact** rather than regenerating the same local-model interpretation every time the browser opens.

Contract name:

```text
job-work-intelligence-v1
```

Durable entity:

```text
JobWorkIntelligenceArtifact
```

Persistence means:

> reproducible generated interpretation tied to exact dependencies

Persistence does **not** mean:

> reviewed semantic truth / canonical role taxonomy

### 5.2 Why persist candidate intelligence

- local semantic reasoning can be expensive;
- repeated-use UI should reopen quickly;
- exact model/prompt/schema identity should remain inspectable;
- historical candidate interpretations are useful when contracts/models evolve;
- source/P1.6 currentness can be handled deterministically;
- reproducibility is valuable even when semantic promotion is not required.

### 5.3 Artifact identity

Artifact identity includes:

```text
source job identity
exact accepted P1.6 artifact ID
P1.6 prompt/schema dependency identity
work-intelligence model
work-intelligence prompt version
work-intelligence schema version
```

Changing the source/P1.6 dependency makes an older candidate historical/non-current.

Changing the work-intelligence prompt/model/schema may produce a distinct candidate artifact without rewriting history.

### 5.4 Candidate artifact review state

P2.2A artifacts do **not** default to `pending human acceptance` merely because a model generated them.

Semantic state:

```text
generated / candidate
```

Currentness and candidate status remain separate concepts.

A later promoted responsibility family or stable archetype uses its own explicit review/promotion state.

---

## 6. P2.2A v1 domain shape

### 6.1 WorkTheme

```text
local theme identity within artifact
label
summary
relative_emphasis: primary | supporting | uncertain
confidence: high | medium | low
responsibility_indices[]
role_purpose_indices[]
optional supporting_requirement_indices[]
reason/rationale
```

Rules:

- at least one responsibility or role-purpose reference is required;
- requirement references are supporting only;
- no cross-job canonical identity is implied by the theme label.

### 6.2 DeliverableCandidate

```text
label
summary
status: source_explicit | strongly_implied_by_work
confidence
responsibility_indices[] / role_purpose_indices[]
rationale when implied
```

### 6.3 CandidateRoleInterpretation

```text
label
summary
confidence
supporting_theme_ids[]
optional alternatives[]
limitations[]
```

This is a job-level analytical interpretation, not a promoted `RoleArchetype` entity.

### 6.4 WorkIntelligenceArtifact content

At minimum:

```text
artifact identity / created_at
source_job_id
source detail dependency identity
translation dependency identity where recoverable through P1.6
P1.6 artifact/prompt/schema identity
work-intelligence model/prompt/schema identity
work_evidence_status
concise work summary
work themes[]
deliverable candidates[]
optional candidate role interpretation
ambiguities / unknowns[]
source-reference coverage metadata
```

---

## 7. P2.2A reasoning architecture

Implemented v1 flow:

```text
accepted/current P1.6
        ↓
deterministic compact factual input
        ↓
bounded local semantic reasoning
        ↓
structured candidate response
        ↓
deterministic reference/invariant validation
        ↓
persist JobWorkIntelligenceArtifact
        ↓
browser-first work-intelligence view
```

### 7.1 Deterministic pre-processing

Code prepares compact factual input with exact indices rather than asking the model to rediscover source identity.

The model receives:

- role purpose;
- responsibilities;
- selected requirements/context useful for interpretation;
- explicit instructions distinguishing facts from inference.

### 7.2 Model responsibilities

The model may:

- group work into coherent themes;
- judge primary/supporting emphasis semantically;
- infer bounded deliverables from work evidence;
- synthesize candidate role interpretation;
- identify ambiguity/unknowns.

### 7.3 Deterministic post-validation

Code rejects structurally invalid candidate output when:

- referenced responsibility/role-purpose/requirement indices do not exist;
- a work theme owns no direct work reference;
- accepted responsibilities or role-purpose items are omitted from all themes;
- a deliverable owns no direct work reference;
- candidate role interpretation references unknown theme IDs;
- required fields/schema are invalid;
- dependency identity is inconsistent.

Do not deterministically rewrite valid semantic wording merely to force a preferred phrase.

### 7.4 Model failure semantics

Model/provider failure:

```text
!= source/P1.6 failure
!= empty work truth
```

Earlier durable work remains valid.

Failed generation records bounded operational failure without manufacturing a successful artifact.

---

## 8. P2.2A interaction surfaces

### 8.1 Browser-first

Normal route:

```text
/jobs/<job-id>/work-intelligence
```

Accepted English-analysis job-detail pages link directly to Work Intelligence.

The view optimizes for fast comprehension first, with exact P1.6 reference indices inspectable.

### 8.2 Required visual distinction

The view makes these categories recoverable:

```text
Employer/P1.6 factual work
JobHunter interpretation
Unknown / ambiguous
```

Avoid provenance-heavy clutter in the default view, but do not hide the basis of consequential interpretations.

### 8.3 CLI

CLI entrypoint:

```text
jobhunter-work generate <job-id>
jobhunter-work show <job-id>
```

CLI remains secondary for generation/inspection/debugging rather than becoming a manual review system for candidate output.

### 8.4 Publication side effect

P2.2A browser generation intentionally stays outside the existing `WebOperationManager` because successful operation-manager mutations refresh the public corpus.

Work Intelligence publication is not authorized in P2.2A.

---

## 9. P2.2A initial real-job acceptance set

Use the existing heterogeneous accepted factual anchors rather than requiring corpus expansion first.

### 9.1 `tG9K` — industrial ML / manufacturing AI

Accepted work evidence includes eight responsibilities spanning:

- ML/AI model building and validation;
- yield/process/fault/anomaly work;
- high-dimensional industrial data handling;
- robust pipelines;
- problem framing;
- model validation/monitoring;
- movement toward production;
- traceability/reproducibility/governance.

Purpose: prove dense technical work composition without collapsing into one generic `Machine Learning` theme.

### 9.2 `t4qV` — network/security

Accepted work evidence includes ten responsibilities spanning:

- security solution design/execution;
- NGFW management;
- security policy implementation;
- network-security architecture;
- VPNs;
- high availability;
- troubleshooting;
- Zero Trust/segmentation;
- technical documentation.

Purpose: prove architecture/operations/troubleshooting/documentation can coexist without false single-role simplification.

### 9.3 `tmyX` — security infrastructure / Microsoft services

Accepted work evidence includes five responsibilities spanning:

- vulnerability/configuration investigation;
- security-request/ticket response;
- access-control/GPO review;
- security documentation/reporting;
- PowerShell assessment/audit automation.

Purpose: prove a mixed assessment/hardening/automation interpretation.

### 9.4 `tmBK` — limited direct work evidence

Accepted P1.6 has requirements but no responsibilities/role purpose suitable for direct work composition.

Purpose: prove P2.2A does not fabricate duties from qualifications and returns a useful limited-evidence state instead of failing.

### 9.5 Additional jobs

Do not add jobs merely to reach a quota.

Add a new accepted job only when a concrete P2.2 question needs evidence, such as:

- family boundary case;
- repeated cross-job responsibility pattern;
- deliverable ambiguity;
- title/work mismatch candidate;
- promoted archetype support;
- cross-employer recurrence.

---

## 10. P2.2A acceptance tiers

### Tier A — integrity/persistence

Repository implementation currently proves:

- [x] migration/persistence correctness through focused tests;
- [x] exact P1.6 dependency identity;
- [x] only accepted/current P1.6 can produce current Work Intelligence;
- [x] stale upstream dependency makes candidate artifact non-current without rewriting history;
- [x] rerun/reuse behavior is idempotent for the same identity;
- [x] invalid source references cannot persist;
- [x] omitted accepted work evidence cannot persist as successful sufficient Work Intelligence;
- [x] browser mutation does not publish Work Intelligence into `corpus/`;
- [x] model failure path cannot manufacture a successful artifact by contract.

CI implementation head `c77635c63ec3140146315980fb0c80522b03d0cf`, run `32996495178`:

```text
Ruff                       PASS
full pytest                PASS
pytest warnings-as-errors  PASS
```

The retrieved CI evidence did not include an exact test count; do not invent one.

### Tier C — bounded analytical usefulness — OPEN

Must still prove on real heterogeneous jobs:

- [ ] work themes are useful and materially reduce manual synthesis effort;
- [ ] employer facts and JobHunter interpretation remain distinguishable;
- [ ] dense work does not collapse into an unhelpful generic theme;
- [ ] multiple plausible work areas may coexist;
- [ ] ambiguous cases can lower confidence/show alternatives;
- [ ] likely deliverables are properly labeled explicit versus work-implied;
- [ ] limited-work jobs do not fabricate responsibilities;
- [ ] no exact wording match is required from semantic reasoning;
- [ ] harmless phrasing variation is not treated as a contract failure.

P2.2A does **not** require Tier B promotion-grade human acceptance for every generated artifact.

### Product utility acceptance

For at least `tG9K`, `t4qV`, and `tmyX`, manual review must answer yes to:

> Is the Work Intelligence view a faster and clearer way to understand the job's actual work than reading and mentally grouping the full vacancy responsibilities oneself?

This is a product-quality judgment, not a deterministic text assertion.

`tmBK` must additionally prove the limited-work boundary without invented duties.

---

## 11. P2.2B — Selective responsibility and deliverable normalization

P2.2B begins only after P2.2A reveals which reusable semantic correspondences actually create downstream value.

### 11.1 Objective

Promote a bounded set of canonical responsibilities/deliverables where reuse is justified by real jobs or planned family/aggregate queries.

### 11.2 Selection rule

Prioritize cases such as:

- obvious near-equivalent responsibility wording across jobs;
- recurring responsibilities needed for family membership;
- deliverables required for P2.3 capability profiles;
- ambiguity that cannot be handled well by job-local candidate themes alone.

Do not normalize every responsibility merely because it exists.

### 11.3 Existing registry reuse

Reuse the P2.1 canonical-registry concept categories:

```text
responsibility
deliverable
```

where their existing contract is sufficient.

Do not create a parallel canonical concept system.

### 11.4 Promotion

Canonical responsibility/deliverable creation and claim mapping are Tier A/B reusable-authority operations and keep explicit review/provenance.

Candidate P2.2A theme labels never auto-promote themselves.

---

## 12. P2.2C — Responsibility-family intelligence

### 12.1 Candidate family

A candidate family may be generated/used analytically before promotion.

It may:

- have a semantic label/description;
- own multiple responsibility/theme references;
- be one-to-many;
- carry confidence;
- remain local to one analytical result or exploratory comparison.

Candidate-family generation must not automatically create global durable authority.

### 12.2 Promoted ResponsibilityFamily

A stable reusable family requires Tier B promotion.

Expected durable properties:

```text
stable family ID
preferred label
definition
boundary / exclusion notes
active/deprecated status
review note/time
representative responsibility concepts/jobs
reviewed family memberships
```

Membership may be many-to-many where justified.

### 12.3 Promotion evidence

No universal numeric quota is required.

Promotion requires enough evidence for the specific reuse claim:

- more than one supporting responsibility pattern where possible;
- cross-job support for a supposedly recurring family;
- cross-employer support when the family is intended to represent broader market structure;
- clear definition/boundaries;
- explicit handling of hybrid/unmapped cases.

---

## 13. P2.2D — Role-archetype intelligence

### 13.1 Job-level candidate archetype

May exist from one job when work composition supports it.

It is an interpretation, not market taxonomy.

### 13.2 Cross-job candidate archetype

A few jobs may justify a tentative recurring pattern when labeled as such and linked to supporting jobs.

### 13.3 Promoted RoleArchetype

A stable reusable archetype requires stronger Tier B evidence:

```text
stable ID
preferred label
definition and boundaries
representative jobs
responsibility-family/work composition
supporting employers/jobs appropriate to the claim
hybrid/unmapped policy
review/promotion decision
```

Do not treat titles as archetype truth.
Do not treat one clustering/model result as promotion evidence by itself.

### 13.4 Title-versus-work observations

P2.2D may add bounded title-alignment/mismatch observations when work evidence is strong.

They must be presented as JobHunter analysis, not as a claim that the employer used an incorrect title.

---

## 14. Promotion-state architecture

P2.2 uses this permanent separation:

```text
JobWorkIntelligenceArtifact
→ generated candidate job-level interpretation
→ versioned/reusable for UX
→ not canonical authority

Canonical responsibility / deliverable
→ reviewed reusable concept via registry

ResponsibilityFamily
→ candidate analytically OR promoted durable family

RoleArchetype
→ candidate analytically OR promoted durable archetype
```

Do not infer authority merely from persistence.

---

## 15. Public-corpus and privacy boundary

P2.2 implementation does **not** automatically authorize exporting Work Intelligence artifacts, candidate families, promoted families, or archetypes into `corpus/`.

Default:

```text
local SQLite/runtime state
→ allowed when implemented

repository public corpus
→ unchanged until separate explicit publication/privacy/source review
```

This preserves the P2.1 registry-publication boundary.

---

## 16. Quality and testing strategy

### 16.1 Test strongly where semantics are deterministic

Focus deterministic tests on:

- migrations;
- dependency/currentness;
- reference validity;
- complete direct-work coverage;
- artifact identity/reuse;
- review/promotion invariants;
- invalid-state rejection;
- browser/CLI service consistency;
- publication/privacy non-side-effects.

### 16.2 Test semantic reasoning appropriately

For model-owned interpretation:

- validate schema and evidence-reference ownership;
- use representative real/regression fixtures;
- assert prohibited authority confusion/fabrication;
- avoid brittle exact prose assertions;
- do not force one exact theme wording when multiple semantically valid descriptions exist.

### 16.3 Regression rule

Convert repeatable material integrity defects into regression tests.

Record harmless model wording variation or non-repeatable low-impact differences as model behavior, not automatic reasons for contract churn.

---

## 17. P2.2 delivery increments and stop lines

### P2.2A — Job Work Intelligence v1 — IMPLEMENTED / REAL-LOCAL ACCEPTANCE NEXT

Implemented scope:

- [x] typed candidate Work Intelligence contract;
- [x] deterministic persistence/currentness identity;
- [x] bounded reasoning service over accepted/current P1.6;
- [x] evidence-reference validation;
- [x] complete accepted direct-work coverage validation;
- [x] one-job CLI generate/show path;
- [x] browser-first job Work Intelligence surface;
- [x] targeted deterministic/browser tests;
- [x] progressive implementation working-memory documentation;
- [x] repository Ruff/full-pytest/warnings CI gates.

Acceptance still open:

- [ ] live semantic/product review on `tG9K`;
- [ ] live semantic/product review on `t4qV`;
- [ ] live semantic/product review on `tmyX`;
- [ ] live limited-evidence review on `tmBK`;
- [ ] unchanged rerun/reuse proof on at least one real job;
- [ ] browser usability/authority-boundary review on real artifacts;
- [ ] final P2.2A acceptance decision and documentation.

Stop line:

- do not create global responsibility families/archetypes merely to finish P2.2A;
- do not bulk-map responsibilities;
- do not publish P2.2 state;
- do not start P2.3/Market v2/personal intelligence.

### P2.2B — Selective responsibility/deliverable promotion — LATER

Start only after P2.2A shows concrete reusable correspondences worth promoting.

### P2.2C — Responsibility families — LATER

Start only with evidence and downstream use from P2.2A/B.

### P2.2D — Role archetype intelligence — LATER

Candidate job-level role interpretation already exists in P2.2A; durable cross-job archetype promotion remains later.

---

## 18. Definition of done for P2.2 overall

P2.2 closes only when the product can demonstrate both useful analytical speed and correct authority boundaries.

Required overall outcomes:

- [ ] real jobs produce useful job-level Work Intelligence;
- [ ] candidate interpretation is available before exhaustive canonicalization;
- [ ] employer facts / normalized mappings / JobHunter inference remain distinguishable;
- [ ] ambiguity and limited evidence degrade confidence/detail rather than fabricating certainty;
- [ ] candidate persistence does not imply promotion;
- [ ] selective canonical responsibility/deliverable promotion is proven where useful;
- [ ] responsibility-family candidate vs promoted state is proven;
- [ ] role-archetype candidate vs promoted state is proven or stable promotion is explicitly deferred for insufficient reuse evidence;
- [ ] promoted reusable semantics retain provenance/review/currentness;
- [ ] normal browser UX materially reduces manual responsibility synthesis effort;
- [ ] implementation/integrity quality gates pass without demanding deterministic model wording;
- [ ] P2.3 and Market v2 remain outside P2.2 until their own focused gates.

A valid P2.2 closure may explicitly defer stable archetype promotion if the evidence/reuse need is not yet sufficient. That does not invalidate successful job-level role intelligence.

---

## 19. Non-goals

P2.2 does not authorize:

- bulk canonicalization for completeness;
- automatic model-generated canonical concept/family/archetype promotion;
- fixed title-first role taxonomy;
- arbitrary corpus-size quotas;
- market prevalence claims from one/few jobs;
- exact percentage Role DNA without a defensible measurement rule;
- P2.3 fine-grained capability requirement profiles;
- Market v2 stable canonical aggregation;
- personal evidence/readiness/gap/recommendation/scoring;
- resume/application/interview automation;
- registry/P2.2 public-corpus publication;
- vector DB, graph DB, RAG, generic agent infrastructure, or multi-model voting without a separate demonstrated need.

---

## 20. Exact next action

P2.2A implementation and repository mechanical quality are complete.

Do **not** start P2.2B yet.

Verified checkpoint:

`docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md`

Next plan decision:

```text
retain model candidate grouping and relative emphasis
→ deterministically inject exact accepted P1.6 direct-work statements within each theme
→ keep free-form candidate interpretation optional and visually/structurally separate
→ define which existing free-form action-bearing fields are removed, demoted, or retained
→ preserve currentness/reference/coverage validation and immutable candidate history
→ approve the bounded representation amendment before implementation
```

The current implementation record is:

`docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md`

The cross-job `tG9K`/`tmyX` evidence is the material design evidence required to amend this plan.
Do not continue prompt/model retries or start P2.2B before the representation decision.
