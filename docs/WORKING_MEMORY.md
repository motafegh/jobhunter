# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-26  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1 CLOSED; utility/epistemic governance REORIENTED; P2.2 plan APPROVED; P2.2A IMPLEMENTED / CI GREEN / REAL-LOCAL SEMANTIC ACCEPTANCE NEXT

## 1. Exact current point

The accepted factual Phase-2 substrate remains frozen:

```text
English P1.6 public/current:  job-analysis-english-v20 / job-analysis-v5
Capability public/current:    job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint:                    deferred / non-current / historical
Canonical Registry:           jobhunter-canonical-concept-registry-v1 / P2.1 CLOSED
Public Corpus:                jobhunter-public-corpus-v1 / operationally closed
```

Accepted/current real chains:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

Public-corpus baseline remains:

```text
known/discovered Jobinja jobs: 353
fetched/parsed detail jobs:      43
current English projections:     20
accepted/current English P1.6:    5
accepted/current Capability:      5
```

Registry publication remains unauthorized.

## 2. Permanent governance correction

The controlling companion policy is:

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

Operational model:

```text
SOURCE / STATE INTEGRITY
→ strict, provenance-preserving, deterministic where appropriate

ANALYTICAL INTERPRETATION
→ semantic/model reasoning allowed and expected
→ traceable, confidence/uncertainty aware

PROMOTED REUSABLE AUTHORITY
→ stronger review proportional to downstream reuse/blast radius
```

Permanent distinctions:

```text
source fact
≠ normalized correspondence
≠ analytical interpretation
≠ recommendation

candidate/generated
≠ reviewed/promoted
```

Human review is mainly a promotion boundary. Interpretive uncertainty should normally reduce confidence, show alternatives, or preserve unknowns rather than block useful job-level intelligence.

Do not demand market-scale evidence for a one-job interpretation and do not present a one-job interpretation as market truth.

## 3. P2.1 closure

P2.1 Canonical Concept Registry is accepted and closed.

Accepted seed:

```text
concepts:          4
reviewed aliases:  1
claim decisions:   6
  mapped:          5
  unmapped:        1
```

Final record:

`docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md`

Do not reopen P2.1 merely because P2.2 needs analytical interpretation. Candidate Work Intelligence is deliberately separate from promoted registry authority.

## 4. P2.2 focused plan

Controlling plan:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

Approved sequence:

```text
P2.2A Job Work Intelligence v1
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

P2.2 asks:

> What does this job actually involve, and what kind of work/role does it appear to be?

Useful candidate interpretation must not wait for exhaustive canonical mapping.

## 5. P2.2A implementation — COMPLETE / ACCEPTANCE OPEN

Working contract:

`job-work-intelligence-v1`

Implementation record:

`docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md`

Implemented vertical slice:

```text
accepted/current English P1.6
→ compact indexed work payload
→ bounded typed LM Studio reasoning when direct work exists
→ deterministic source-reference + full-work-coverage validation
→ immutable candidate artifact
→ CLI/browser inspection
```

Core files:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_store.py
src/jobhunter/work_intelligence_inference.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_cli.py
src/jobhunter/web/work_intelligence.py
src/jobhunter/web/templates/work_intelligence.html
tests/test_work_intelligence.py
```

Integration:

```text
jobhunter-work generate <job-id>
jobhunter-work show <job-id>
/jobs/<job-id>/work-intelligence
```

Accepted job-detail pages now link to Work Intelligence.

### Authority boundary

P2.2A depends directly on accepted/current English P1.6 v20/v5.

Capability v9 is **not** an authoritative input dependency. The initial Work Intelligence runtime merely reuses the existing configured capability-model fallback chain to avoid premature configuration expansion; Work Intelligence has its own prompt/schema/artifact identity.

Existing canonical registry mappings may later enrich P2.2 but missing mappings cannot block P2.2A.

### Candidate persistence

`JobWorkIntelligenceArtifact` is persisted for reproducibility and repeated local UX.

Persistence means:

```text
generated candidate analytical state
```

It does not mean:

```text
human accepted
canonical responsibility family
promoted role archetype
market truth
```

### No-direct-work boundary

If accepted P1.6 has requirements but no responsibilities/role purpose:

```text
evidence_status = limited
work_themes = []
deliverables = []
role_interpretation = null
```

No model call is required and qualifications are not converted into duties.

`tmBK` is the real acceptance anchor for this boundary.

### Deterministic integrity after reasoning

JobHunter validates:

- every referenced responsibility/role-purpose/requirement index exists;
- every accepted responsibility appears in at least one work theme;
- every accepted role-purpose item appears in at least one work theme;
- candidate role interpretation references only generated themes.

Semantic grouping remains model-owned; JobHunter does not demand deterministic wording/group identity.

### Browser/publication boundary

The P2.2A browser POST is CSRF protected but intentionally outside `WebOperationManager` because that manager synchronizes the public corpus after successful mutations.

Therefore:

```text
local Work Intelligence persistence  AUTHORIZED
browser/CLI local use                AUTHORIZED
public-corpus Work Intelligence      NOT AUTHORIZED
```

## 6. Repository quality evidence

CI run:

```text
32996495178
head c77635c63ec3140146315980fb0c80522b03d0cf
```

Observed:

```text
Ruff                         PASS
full pytest                  PASS
pytest warnings-as-errors    PASS
overall quality job          PASS
```

No exact test count was retrieved from the CI response; do not invent one.

## 7. Exact next action — real-local semantic/product acceptance

The repository implementation is mechanically green. The next work is **not more architecture or P2.2B**.

Use the owner's real local database/model on:

```text
tG9K  industrial ML / manufacturing AI, 8 responsibilities
t4qV  network/security, 10 responsibilities
tmyX  security infrastructure / Microsoft services, 5 responsibilities
tmBK  accepted requirements, no direct responsibilities
```

Review each against the actual product goal:

1. Is the Work Intelligence view materially faster/easier to understand than manually reading the vacancy responsibilities?
2. Are all accepted work facts represented without one-item-per-theme mechanical output?
3. Are theme labels/summaries useful, restrained, and clearly JobHunter interpretation?
4. Are deliverables actually source-explicit or strongly work-implied?
5. Is candidate role interpretation helpful without pretending to be promoted taxonomy?
6. Are confidence/alternatives/limitations calibrated rather than blocker-like?
7. Does `tmBK` remain explicitly limited without invented duties?
8. Does an unchanged rerun reuse the same artifact?
9. Does the browser make employer/P1.6 facts versus JobHunter interpretation clear?

If a model output is imperfect but bounded/candidate, record the limitation rather than automatically treating wording variation as an integrity defect. Fix deterministic code only for repeatable contract/integrity problems.

## 8. Do not start yet

Until P2.2A real-local semantic/product acceptance is decided:

- do not start P2.2B;
- do not promote responsibility families/archetypes;
- do not bulk-map remaining claims for completeness;
- do not broaden ontology merely to eliminate unresolved cases;
- do not publish Work Intelligence or registry state;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not revive Blueprint as authority.

## 9. Key current records

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
docs/ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md
docs/IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md
docs/working-memory/2026-08-26_UTILITY_EPISTEMIC_GOVERNANCE_REORIENTATION.md
docs/working-memory/2026-08-26_P2_2_FOCUSED_PLAN_APPROVED.md
docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md
docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md
corpus/README.md
```
