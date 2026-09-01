# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-01  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1 CLOSED; P2.2A v2 IMPLEMENTED / REPOSITORY QUALITY GREEN / REAL-LOCAL ACCEPTANCE NEXT

## 1. Frozen accepted substrate

```text
English P1.6 public/current:  job-analysis-english-v20 / job-analysis-v5
Capability public/current:    job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint:                    deferred / non-current / historical
Canonical Registry:           jobhunter-canonical-concept-registry-v1 / P2.1 CLOSED
Public Corpus:                jobhunter-public-corpus-v1 / operationally closed
```

Accepted/current factual chains:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
tmBK → P1.6 39 → Capability 13
t4qV → P1.6 44 → Capability 14
tmyX → P1.6 46 → Capability 15
```

Do not reopen P1.6, Capability v9, P2.1, or Blueprint merely for harmless candidate wording variation.

## 2. Controlling P2.2 documents

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
```

The amendment resolved the cross-job action-authority representation blocker and is controlling where more specific than the base plan.

Implementation checkpoint:

```text
docs/working-memory/2026-09-01_P2_2A_V2_REPRESENTATION_IMPLEMENTATION.md
```

## 3. Current P2.2A identities

```text
persisted schema:       job-work-intelligence-v2
prompt/runtime:         job-work-intelligence-v2.0
limited deterministic: jobhunter-deterministic-limited-work-v2
```

Historical v1/v1.1-v1.7 artifacts and attempts remain immutable evidence. They are not reused as current v2 artifacts.

## 4. Current authority architecture

Permanent v2 rule:

> The model decides how accepted work is usefully organized; accepted P1.6 statements decide what factual work is actually asserted.

Current direct-work flow:

```text
accepted/current English P1.6
→ compact indexed factual input
→ one typed CandidateJobWorkIntelligence model call
→ deterministic reference / coverage / scope validation
→ at most one bounded regeneration if those guards reject
→ deterministic exact P1.6 work injection
→ assembled-artifact exact dependency validation
→ immutable candidate artifact
→ browser + CLI
```

There is **no dedicated second semantic authority-review model pass** in v2.

Normal valid direct-work generation uses one model call. The bounded repair path uses at most two candidate-generation calls.

Requirement-only jobs use the deterministic `limited` path and make no model call.

## 5. Candidate versus factual representation

Model candidate owns:

```text
theme label / grouping
relative emphasis
confidence
supporting requirement refs
optional rationale
candidate deliverables
candidate role label / alternatives / limitations
```

Persisted factual work item:

```text
kind: responsibility | role_purpose
index: exact accepted P1.6 index
statement: exact accepted P1.6 statement
confidence: copied accepted P1.6 confidence when available
```

Removed from v2 persisted representation:

```text
work_summary
WorkTheme.summary
DeliverableCandidate.summary
CandidateRoleInterpretation.summary
```

The browser/CLI show exact accepted work separately from JobHunter interpretation.

## 6. Integrity/reuse hardening

Current/reused v2 artifacts are checked again against their accepted/current P1.6 dependency before display/reuse.

A persisted accepted work item must have a consistent:

```text
kind
index
exact statement
copied confidence
```

Every accepted responsibility/role-purpose item must remain covered by a theme. Supporting requirement indices must remain valid.

A structurally valid but factually mismatched artifact fails rather than being shown.

## 7. Repository quality evidence

Implementation head before documentation reconciliation:

```text
d8e7f5d0a064dcec5e662101eac67d624ff925b1
```

CI:

```text
run 33548003449
quality: SUCCESS
Ruff: PASS
full pytest: PASS
pytest warnings-as-errors: PASS
```

Do not confuse this with real-local semantic/product acceptance. No live LM Studio generation was performed in this remote session.

## 8. Why v2 exists

Historical evidence remains:

```text
t4qV artifact 2  v1.1  useful candidate anchor
tmyX artifact 3  v1.1  useful grouping + action strengthening
tG9K artifact 4  v1.1  useful grouping; 3 primary + 1 supporting + action strengthening
tG9K artifact 5  v1.2  useful grouping; direct deployment wording remained
artifacts 6-11          controlled v1.3-v1.7 action-authority/model/protocol evidence
```

Key facts that drove redesign:

```text
tG9K:
Partner with the semiconductor technical lead and engineering to move models toward production.

tmyX role purpose:
Assess security posture of servers and Microsoft services and to develop and provide security
requirements, Best Practices, and hardening solutions.
```

Free-form model review repeatedly strengthened those action relationships. The response is now representation-level separation, not another prompt/model trial.

## 9. Exact next action

Real-local acceptance sequence:

```text
1. t4qV
   → generate current v2 on accepted P1.6 44
   → review grouping usefulness + exact accepted-work presentation

2. tmBK
   → verify deterministic limited result
   → zero invented duties

3. reuse
   → rerun one unchanged v2 job
   → confirm same artifact is reused

4. browser
   → inspect same real artifacts
   → confirm factual work and interpretation are immediately distinguishable

5. CLI
   → confirm same assembled semantics

6. decide P2.2A acceptance

7. only then decide P2.2B
```

`tG9K`/`tmyX` already established the action-authority design defect. Do not repeat the model-trial matrix.

## 10. Stop lines

Until P2.2A closes:

- do not start P2.2B;
- do not bulk-map responsibilities;
- do not broaden ontology merely to eliminate unresolved cases;
- do not create global responsibility families/archetypes merely to finish P2.2A;
- do not add a deterministic action-verb equivalence system;
- do not restore the second semantic authority-review pass;
- do not impose a fixed primary-theme quota;
- do not publish Work Intelligence or registry state;
- do not start Market v2;
- do not add personal readiness/gap/scoring/recommendations;
- do not revive Blueprint as authority.

## 11. Key current records

```text
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md
docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md
docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md
docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md
docs/working-memory/2026-09-01_P2_2A_V2_REPRESENTATION_IMPLEMENTATION.md
```
