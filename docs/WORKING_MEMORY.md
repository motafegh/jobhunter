# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-01  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1 CLOSED; P2.2A IMPLEMENTED v1 / ACCEPTANCE OPEN; v2 representation amendment APPROVED; v2 implementation NEXT

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

Registry and Work Intelligence publication remain unauthorized. Do not reopen accepted P1.6/Capability contracts merely for harmless downstream candidate wording variation.

## 2. Permanent governance model

Controlling reasoning companion:

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

Operational distinction:

```text
SOURCE / STATE INTEGRITY
→ strict provenance/currentness/persistence boundaries

ANALYTICAL INTERPRETATION
→ semantic/model reasoning allowed and expected
→ traceable, uncertainty-aware, candidate by default

PROMOTED REUSABLE AUTHORITY
→ stronger review proportional to reuse/blast radius
```

Never collapse:

```text
source fact ≠ normalized correspondence ≠ analytical interpretation ≠ recommendation
candidate/generated ≠ reviewed/promoted
```

## 3. P2.2 controlling plan and approved amendment

Base focused plan:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

Approved controlling companion amendment:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`

Evidence checkpoint that triggered the amendment:

`docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md`

The amendment is more specific and controls where it changes the base P2.2A representation/pipeline decision.

## 4. Why the representation changed

Real `tG9K` and `tmyX` evidence established that model reasoning remains useful for grouping and emphasis, but free-form model prose is not reliable enough to carry factual action authority.

Known examples:

```text
tG9K accepted work:
Partner with the semiconductor technical lead and engineering to move models toward production.

Model variants repeatedly strengthened that relationship toward direct deployment / into production.


tmyX accepted role purpose:
...develop and provide security requirements, Best Practices, and hardening solutions.

Model variants strengthened this toward direct hardening execution.
```

Controlled v1.3-v1.7 trials across 2B/4B/12B and multiple review protocols are complete historical evidence. Do **not** run another prompt/model action-authority trial matrix.

## 5. Approved v2 representation

The key authority rule is now:

> The model decides how accepted work is usefully organized; accepted P1.6 statements decide what factual work is actually asserted.

Approved flow:

```text
accepted/current English P1.6 direct work
→ compact indexed factual input
→ model candidate grouping / emphasis / bounded interpretation
→ deterministic reference + coverage validation
→ deterministic injection of exact accepted P1.6 work statements
→ persist assembled candidate artifact
→ browser / CLI
```

New identities to implement:

```text
persisted Work Intelligence schema/contract: job-work-intelligence-v2
prompt/runtime identity:                     job-work-intelligence-v2.0
```

Historical v1 artifacts 2-11 and attempt history remain immutable.

## 6. Field ownership

Model candidate owns:

```text
theme IDs / labels
relative emphasis
confidence
source indices used for grouping
supporting requirement references
optional interpretation / rationale
candidate deliverables
candidate role label / alternatives / limitations
unknowns / limitations
```

Application code owns factual assembly:

```text
AcceptedWorkItem
- kind: responsibility | role_purpose
- index
- exact accepted P1.6 statement
- copied P1.6 confidence when available
```

Each persisted theme contains exact accepted work items rather than relying on a model-written theme summary plus raw indices.

Current action-bearing free-form fields are intentionally reduced in v2:

```text
work_summary                     → remove
WorkTheme.summary                → remove as factual description
CandidateRoleInterpretation.summary → remove from required v2 shape
DeliverableCandidate.summary     → remove from required v2 shape
```

Optional interpretation/rationale may remain only when structurally and visually labeled as JobHunter candidate interpretation.

## 7. Pipeline change

Normal v2 direct-work path:

```text
one model candidate generation
→ deterministic validation
→ optional one bounded regeneration only after deterministic candidate rejection
→ deterministic exact-work assembly
→ persistence
```

Remove the dedicated second model semantic authority-review call from the active successful path. The completed trials showed that another free-form model review cannot reliably establish factual action authority and increases repeated-use latency.

Do not replace it with:

- deterministic verb-equivalence tables;
- 12B authority review;
- multi-model voting;
- another prompt-only trial series.

Keep deterministic dependency/currentness/reference/coverage/schema/publication protections. The existing small unsupported scope-intensifier guard may remain for clearly misleading candidate interpretation but must not expand into semantic paraphrase machinery.

## 8. Browser / CLI target

Themes should present authority at the point of use:

```text
Candidate theme label
PRIMARY / SUPPORTING / UNCERTAIN · confidence

Accepted P1.6 work
- exact accepted statement
- exact accepted statement

JobHunter interpretation
- optional rationale / explanation
```

Raw source indices alone are not sufficient factual presentation.

Do not label translated/derived English P1.6 statements as literal employer-authored English. Underlying original source evidence remains recoverable through P1.6 provenance.

Browser and CLI must render the same assembled artifact semantics.

## 9. Expected implementation surface

Start with the smallest bounded set:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_inference.py        # only where new candidate model / review removal requires it
src/jobhunter/web/work_intelligence.py              # only if context assembly changes
src/jobhunter/web/templates/work_intelligence.html
src/jobhunter/work_intelligence_cli.py              # formatter/rendering as needed
focused Work Intelligence tests
```

`work_intelligence_store.py` should remain structurally unchanged unless implementation finds a real table-level need. Do not create a migration ceremonially.

Do not modify P1.6, Capability v9, Blueprint, Registry, Market, or public-corpus publication as part of this repair.

## 10. Required deterministic regression evidence

At minimum prove:

- exact P1.6 direct-work statements survive unchanged into final theme work items;
- kind/index/statement correspondence cannot drift;
- model candidate wording cannot replace factual action wording;
- all accepted direct work remains covered;
- invalid references still fail;
- requirement-only `tmBK` remains deterministic limited/no-model;
- valid normal generation no longer performs a second authority-review model call;
- bounded regeneration remains bounded;
- historical v1 artifacts remain historical and are not reused as current v2;
- v2 reuse remains idempotent;
- browser/CLI visibly separate accepted work from interpretation;
- Work Intelligence remains excluded from public-corpus publication.

## 11. Post-implementation real acceptance

Do not repeat the completed `tG9K`/`tmyX` action-authority model experiments.

After v2 deterministic quality is green:

```text
1. t4qV — generate/review redesigned direct-work artifact
2. tmBK — verify deterministic limited behavior
3. unchanged current v2 job — verify reuse
4. browser — inspect authority separation + comprehension
5. CLI — confirm same representation semantics
6. decide P2.2A acceptance
7. only then decide P2.2B
```

## 12. Exact next action

```text
implement job-work-intelligence-v2 candidate-vs-assembled representation
→ remove dedicated second model authority-review call
→ deterministically inject exact accepted P1.6 direct-work statements
→ update browser/CLI authority presentation
→ add focused v2 regression coverage
→ run focused repository quality gates
→ resume t4qV / tmBK / reuse / browser acceptance
→ P2.2A close/acceptance decision
→ only then P2.2B decision
```

## 13. Do not start yet

Until P2.2A closes:

- do not start P2.2B/C/D implementation;
- do not bulk canonicalize responsibilities;
- do not broaden ontology for completeness;
- do not publish Work Intelligence/registry state;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not revive Blueprint as authority;
- do not add deterministic action-verb equivalence;
- do not add a fixed primary-theme quota;
- do not rerun the completed action-authority model trial matrix.

## 14. Key records

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md
docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md
```