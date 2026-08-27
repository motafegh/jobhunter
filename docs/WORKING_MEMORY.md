# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-27  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1 CLOSED; utility/epistemic governance REORIENTED; P2.2 plan APPROVED; P2.2A IMPLEMENTED; LIVE SEMANTIC-PRODUCT ACCEPTANCE IN PROGRESS; `tG9K` NEXT

## 1. Frozen factual substrate

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

Registry and Work Intelligence publication remain unauthorized.

## 2. Permanent governance correction

Controlling companion policy:

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

Operational model:

```text
SOURCE / STATE INTEGRITY
→ strict, provenance-preserving, deterministic where appropriate

ANALYTICAL INTERPRETATION
→ semantic/model reasoning allowed and expected
→ traceable and uncertainty-aware

PROMOTED REUSABLE AUTHORITY
→ stronger review proportional to downstream reuse/blast radius
```

Permanent distinctions:

```text
source fact ≠ normalized correspondence ≠ analytical interpretation ≠ recommendation
candidate/generated ≠ reviewed/promoted
```

Human review is mainly a promotion boundary. Do not demand market-scale proof for job-level interpretation and do not present one-job interpretation as market truth.

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

Final record: `docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md`

Do not reopen P2.1 merely because P2.2 uses candidate analytical interpretation.

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

Contract/schema:

```text
job-work-intelligence-v1
```

Current prompt identity:

```text
job-work-intelligence-v1.1
```

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
tests/test_work_intelligence_generation_schema.py
tests/test_work_intelligence_scope_guard.py
```

Integration:

```text
jobhunter-work generate <job-id>
jobhunter-work show <job-id>
python -m jobhunter.work_intelligence_cli generate <job-id>
/jobs/<job-id>/work-intelligence
```

P2.2A directly depends on accepted/current English P1.6 v20/v5. Capability v9 is not an authoritative input dependency. The runtime currently reuses the configured capability-model fallback chain only to avoid premature configuration expansion.

Candidate persistence means reproducible generated analytical state, not human acceptance, canonical taxonomy, promoted archetype, or market truth.

## 6. Live P2.2A defect history

### 6.1 First `t4qV` generation — structured provenance defect

The first live model output mentioned responsibility indices only in prose while omitting the dedicated structured arrays. Root cause: Pydantic defaults made those arrays optional in generation JSON Schema while the validator required direct work support.

Repair:

- structured responsibility/role-purpose arrays are required in generated JSON;
- validator remains strict;
- prose indices cannot masquerade as provenance;
- regression added.

Record:

`docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_LIVE_GENERATION_STRUCTURED_REFERENCE_FAILURE.md`

### 6.2 First valid `t4qV` artifact 1 — scope inflation

Artifact 1 was structurally valid and useful but repeatedly introduced unsupported `end-to-end` / `entire security stack` wording and risked transferring vendor examples from broad shared evidence into narrower responsibility claims.

General repair:

```text
prompt version: job-work-intelligence-v1.1
schema:         job-work-intelligence-v1
```

The prompt now makes the accepted responsibility/role-purpose `statement` the bounded work claim and warns that shared evidence may contain neighboring clauses/examples. A small post-validation guard rejects unsupported lifecycle/scope intensifiers while allowing source-explicit scope wording. Hyphenation variants such as `end-to-end` and `end to end` are normalized semantically.

Artifact 1 remains immutable historical evidence under the old prompt identity.

Record:

`docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_VALID_CANDIDATE_AND_SCOPE_REPAIR.md`

Repository quality gates for these repairs were green; do not ask the user to repeat already-established repository gates.

## 7. Real-local semantic/product acceptance — CURRENT STATE

### 7.1 `t4qV` — ACCEPTED candidate product anchor

Current artifact:

```text
artifact:          2
model:             gemma-4-e2b-it
P1.6 dependency:   44
prompt:            job-work-intelligence-v1.1
themes:            4
```

Useful themes:

```text
Security Architecture and Design
Firewall and Network Device Management
Secure Connectivity and Segmentation Implementation
Security Operations and Documentation
```

The previous unsupported lifecycle/scope inflation and vendor-management transfer did not survive the v1.1 rerun. The result materially reduces manual synthesis effort and is accepted as bounded candidate analytical intelligence.

Record:

`docs/working-memory/2026-08-27_P2_2A_T4QV_V11_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED.md`

### 7.2 `tmyX` — ACCEPTED candidate product anchor with recorded limitation

Current artifact:

```text
artifact:          3
model:             gemma-4-e2b-it
P1.6 dependency:   46
prompt:            job-work-intelligence-v1.1
themes:            4
```

Useful themes:

```text
Security Posture Assessment and Analysis
Security Hardening and Solution Development
Security Request Management and Response
Security Documentation and Automation
```

The grouping is useful and materially reduces manual synthesis effort.

Recorded limitation:

```text
accepted role purpose: develop and provide ... hardening solutions
candidate summary:     implementing hardening solutions
```

This strengthens the explicit action verb. It is therefore not employer truth and must not be promoted downstream as an exact work fact. Under the current governance it is recorded as a bounded candidate limitation rather than triggering another deterministic repair from one example. If similar action-verb strengthening repeats across independent jobs, reassess the need for a general semantic rule.

Record:

`docs/working-memory/2026-08-27_P2_2A_TMYX_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED_WITH_LIMITATION.md`

### 7.3 Repeated product-quality watch: all themes `primary`

Both accepted live candidate anchors so far (`t4qV` and `tmyX`) marked every work theme `primary`.

This is not an integrity failure, but if repeated it makes relative emphasis uninformative. Do not create a fixed primary-theme quota. Use `tG9K` as the third independent check; if all-primary repeats, refine the semantic meaning of `primary/supporting/uncertain` with evidence from three heterogeneous jobs.

### 7.4 Remaining anchors

```text
tG9K  industrial ML / manufacturing AI             NEXT
tmBK  requirements-only / no direct work evidence  PENDING
```

`tmBK` expected bounded result:

```text
evidence_status = limited
work_themes = []
deliverables = []
role_interpretation = null
```

No model call should be needed and qualifications must not become duties.

## 8. Remaining P2.2A acceptance work

- generate/review `tG9K`;
- decide whether all-primary emphasis is now a repeatable cross-job product weakness;
- generate/review `tmBK` limited-work boundary;
- rerun at least one unchanged current job and confirm artifact reuse;
- inspect browser Work Intelligence on real artifacts;
- verify employer/P1.6 facts versus JobHunter interpretation are visually/semantically distinct;
- close P2.2A only after the heterogeneous product/usefulness and authority-boundary evidence is sufficient.

Interpretive policy:

```text
bounded imperfection / harmless paraphrase
→ tolerate or record as candidate limitation

repeatable material source/authority defect
→ smallest general repair + regression

repeated product-quality weakness
→ gather cross-job evidence first, then refine semantics if justified
```

## 9. Exact next action

On the user's real local environment:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Review `tG9K` for:

1. useful compression of its eight industrial-ML responsibilities;
2. sensible distinction among model development, industrial data/pipelines, validation/monitoring, and production/governance;
3. no unsupported ownership/lifecycle/action strengthening;
4. whether all generated themes are again `primary`;
5. optional deliverables/role interpretation only when genuinely useful;
6. whether the view is materially faster/easier than manually synthesizing the eight responsibilities.

## 10. Do not start yet

Until P2.2A closes:

- do not start P2.2B;
- do not promote responsibility families/archetypes;
- do not bulk-map remaining claims for completeness;
- do not broaden ontology merely to eliminate unresolved cases;
- do not publish Work Intelligence or registry state;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not revive Blueprint as authority;
- do not add a deterministic action-verb equivalence system from the single `tmyX` limitation;
- do not add a fixed quota of primary themes.

## 11. Key current records

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_LIVE_GENERATION_STRUCTURED_REFERENCE_FAILURE.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_VALID_CANDIDATE_AND_SCOPE_REPAIR.md
docs/working-memory/2026-08-27_P2_2A_T4QV_V11_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED.md
docs/working-memory/2026-08-27_P2_2A_TMYX_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED_WITH_LIMITATION.md
docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md
corpus/README.md
```
