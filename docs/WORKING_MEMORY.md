# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-27  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1 CLOSED; utility/epistemic governance REORIENTED; P2.2 plan APPROVED; P2.2A IMPLEMENTED; LIVE SEMANTIC-PRODUCT ACCEPTANCE IN PROGRESS; fresh `tG9K` v1.3 generation NEXT

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

Public-corpus baseline remains 353 known/discovered jobs, 43 fetched/parsed details, 20 current English projections, 5 accepted/current English P1.6 artifacts, and 5 accepted/current Capability artifacts. Registry and Work Intelligence publication remain unauthorized.

## 2. Permanent governance model

Controlling companion:

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

Operational rule:

```text
SOURCE / STATE INTEGRITY
→ strict provenance/currentness/persistence boundaries

ANALYTICAL INTERPRETATION
→ semantic/model reasoning is allowed and expected
→ traceable, uncertainty-aware, candidate by default

PROMOTED REUSABLE AUTHORITY
→ stronger review proportional to reuse/blast radius
```

Never collapse these distinctions:

```text
source fact ≠ normalized correspondence ≠ analytical interpretation ≠ recommendation
candidate/generated ≠ reviewed/promoted
```

Semantic relationship problems should normally be solved semantically, not by inventing brittle deterministic vocabularies.

## 3. P2.1 closure

P2.1 Canonical Concept Registry is accepted and closed. Accepted seed remains four concepts, one reviewed alias, five mapped decisions, and one explicit unmapped decision. Do not reopen P2.1 merely because P2.2 uses candidate analytical interpretation.

Final record:

`docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md`

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

P2.2A answers the practical user question: **What does this job actually involve?** Useful job-level interpretation must not wait for exhaustive canonical mapping.

## 5. P2.2A implementation — COMPLETE / ACCEPTANCE OPEN

Contract/schema:

```text
job-work-intelligence-v1
```

Current prompt/pipeline identity:

```text
job-work-intelligence-v1.3
```

Current direct-work pipeline:

```text
accepted/current English P1.6
→ compact indexed work payload
→ typed local-model Work Intelligence generation
→ deterministic reference/coverage/scope validation
→ one bounded regeneration if those post-generation guards reject the draft
→ final semantic authority review against accepted direct-work statements
→ deterministic reference/coverage/scope validation again
→ immutable candidate artifact
→ CLI/browser inspection
```

Requirement-only jobs use the deterministic `limited` path and do not call the model or turn qualifications into duties.

The final semantic authority review is deliberately model-semantic. It focuses on action strength, ownership relationship, lifecycle scope, and unsupported transfer from requirements/shared evidence. It is instructed to preserve theme grouping, IDs, emphasis, confidence, and structured references by default and prefer minimal prose corrections.

Do **not** replace this with a deterministic action-verb equivalence table.

Core files:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_store.py
src/jobhunter/work_intelligence_inference.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_cli.py
src/jobhunter/web/work_intelligence.py
src/jobhunter/web/templates/work_intelligence.html
```

Core regressions now include generation schema, scope guard, empty-section reference normalization, bounded semantic repair, and semantic authority review.

Current repository-quality evidence on the v1.3 code/test pipeline:

```text
Ruff                         PASS
full pytest                  PASS — 530 tests
pytest warnings-as-errors    PASS
overall CI quality job       PASS
```

Do not ask the user to repeat these repository gates locally.

## 6. Live P2.2A history that matters

### `t4qV`

First generation exposed missing structured provenance fields. That was fixed by making structured reference arrays required.

First structurally valid artifact 1 then exposed unsupported `end-to-end` / `entire security stack` scope inflation and shared-evidence transfer risk. v1.1 strengthened the prompt and added a bounded scope-intensifier guard.

Artifact 2 under v1.1 became a useful network/security candidate anchor with four coherent themes and no repeated unsupported lifecycle inflation. It is historical under current v1.3 identity.

### `tmyX`

Artifact 3 under v1.1 gave useful security-assessment/hardening/request/documentation/automation grouping, but its summary strengthened accepted `develop and provide ... hardening solutions` into `implementing hardening solutions`.

That was initially recorded as a bounded candidate limitation. Once a similar pattern appeared independently on `tG9K`, it became evidence for a general semantic action-authority refinement.

### `tG9K`

The first attempt exposed an impossible `role_purpose[1]` reference while the accepted role-purpose section was empty. JobHunter now deterministically removes references into structurally empty sections only; invalid references into non-empty sections still fail.

Artifact 4 under v1.1 produced useful industrial-ML grouping and proved emphasis does not always collapse to all-primary: it had `3 primary + 1 supporting`. Therefore do not add a fixed primary-theme quota.

Artifact 4 also strengthened `partner ... to move models toward production` into direct `deploying` language. Together with `tmyX`, this justified v1.2 prompt-level action-authority refinement.

The first v1.2 generation then hit unsupported `entire lifecycle`; that revealed a runtime UX problem, so JobHunter gained one bounded post-validation semantic-repair retry.

Artifact 5 under v1.2 successfully persisted after those changes and remained useful, but still said `building, validating, and deploying Machine Learning/AI models`. Therefore prompt-only action-authority refinement was proven insufficient.

Current response: v1.3 adds a dedicated final semantic authority-review pass before persistence. Artifact 5 remains immutable historical v1.2 evidence and is not current under v1.3.

## 7. Current artifact state

```text
artifact 2  t4qV  v1.1  useful accepted candidate anchor; historical under v1.3
artifact 3  tmyX  v1.1  useful candidate with action-strengthening limitation; historical
artifact 4  tG9K  v1.1  useful grouping; supporting emphasis demonstrated; historical
artifact 5  tG9K  v1.2  useful grouping but direct-deployment wording remained; historical
```

No current v1.3 direct-work artifact has yet been live-reviewed.

## 8. Exact next action

On the user's real local environment:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

This must create a fresh v1.3 artifact rather than reuse artifact 5.

Review specifically whether:

1. the industrial-ML grouping remains useful;
2. the final persisted/output wording preserves collaborative production-readiness (`move models toward production`) rather than direct deployment ownership;
3. unsupported lifecycle/scope language does not survive;
4. the result still materially reduces manual synthesis effort.

If `tG9K` v1.3 succeeds:

```text
→ regenerate/review tmyX under v1.3 against the earlier develop/provide → implementing case
→ regenerate/review t4qV under v1.3 for current identity
→ test tmBK deterministic limited-work behavior
→ prove unchanged current-artifact reuse
→ inspect browser UX + employer-fact / JobHunter-interpretation distinction
→ decide P2.2A closure
→ only then decide P2.2B
```

## 9. Do not start yet

Until P2.2A closes:

- do not start P2.2B;
- do not promote responsibility families/archetypes;
- do not bulk-map remaining claims merely for completeness;
- do not broaden ontology just to eliminate unresolved cases;
- do not publish Work Intelligence or registry state;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not revive Blueprint as authority;
- do not add a deterministic action-verb equivalence system;
- do not add a fixed primary-theme quota.

## 10. Key current records

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_LIVE_GENERATION_STRUCTURED_REFERENCE_FAILURE.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_VALID_CANDIDATE_AND_SCOPE_REPAIR.md
docs/working-memory/2026-08-27_P2_2A_T4QV_V11_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED.md
docs/working-memory/2026-08-27_P2_2A_TMYX_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED_WITH_LIMITATION.md
docs/working-memory/2026-08-27_P2_2A_TG9K_EMPTY_ROLE_PURPOSE_REFERENCE_FAILURE_AND_REPAIR.md
docs/working-memory/2026-08-27_P2_2A_TG9K_USEFUL_CANDIDATE_AND_ACTION_AUTHORITY_V12_REFINEMENT.md
docs/working-memory/2026-08-27_P2_2A_V12_SCOPE_FAILURE_AND_BOUNDED_SEMANTIC_REPAIR_RETRY.md
docs/working-memory/2026-08-27_P2_2A_TG9K_V12_PERSISTED_ACTION_INFLATION_AND_V13_AUTHORITY_REVIEW.md
```
