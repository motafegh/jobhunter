# P2.3A Technical Feasibility and Reuse Audit — 2026-10-17

**Status:** PRE-AUTHORIZATION TECHNICAL AUDIT / NO P2.3 IMPLEMENTATION AUTHORIZED  
**Date:** 2026-10-17  
**Depends on:** `2026-10-17_POST_B2_P2_2C_VS_P2_3_READINESS_PREDECISION.md`  
**Current controlling gate remains:** P2.2B-B2 local R3-R6 Registry application, verification, and closure.

This audit answers a narrower question: if B2 closes cleanly and the post-B2 direction decision selects P2.3A, what existing architecture should P2.3A reuse, and what must still be proven before adding a new durable profile subsystem?

It does not authorize P2.3A and does not change the current B2 state.

---

## 1. Main finding

The repository already contains most of the **epistemic and multidimensional capability-profile machinery** that P2.3 needs. The missing capability is not another generic capability-inference stack.

Current Capability v9 already models, validates, persists, and renders job-local capability interpretation with:

- exact P1.6 requirement/responsibility references;
- requirement strength;
- employer-stated depth;
- expected work activities and deliverables;
- technical sub-capabilities;
- underlying knowledge;
- operational practices/context;
- independence expectations;
- complexity signals;
- explicit unknown scope;
- evidence statuses separating `source_explicit`, `strongly_implied_by_work`, `model_inferred_prerequisite`, and `unknown_or_unsupported`.

The Canonical Registry already owns reviewed reusable concept identity and immutable exact claim mappings/currentness.

Therefore a future P2.3A should **compose these accepted responsibilities rather than fork them**.

---

## 2. Capability-v9 reuse boundary

Relevant accepted code owners:

```text
src/jobhunter/capability_models.py
src/jobhunter/capability_v9_models_core.py
src/jobhunter/capability_service_v9.py
src/jobhunter/capability_store.py
src/jobhunter/web/capability.py
src/jobhunter/web/templates/capability_intelligence.html
```

### What Capability v9 already owns well

`CapabilityProfile` already has the dimensional shape that the roadmap expects from a useful job capability profile. The v9 contract further enforces source-link validity and proportional semantic reasoning.

Its evidence-status vocabulary is already the correct one:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

The v9 builder separates:

```text
accepted P1.6 source truth
→ semantic group planning
→ exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic reconciliation
```

and deterministic code retains ownership of source links, requirement strength, source-explicit depth, and accepted responsibilities.

The browser already exposes these dimensions and drills back to source evidence.

### What Capability v9 does not solve for P2.3

Capability-v9 `capability_label` is **job-local semantic organization**, not reviewed reusable canonical identity. An accepted artifact can therefore be rich and useful while still lacking the stable cross-job concept identity needed for later comparison/aggregation.

Also, only five accepted/current Capability artifacts currently exist, from the older heterogeneous Phase-1 anchor set. The six snapshot-15 Market postings used for the proposed P2.3A acceptance frame do not all have accepted Capability-v9 artifacts.

Therefore:

```text
Capability v9 MUST NOT become a mandatory upstream artifact for every P2.3 profile.
Capability v9 MUST NOT be retroactively mutated to carry canonical identities.
Capability v9 MAY be reused as design code, optional accepted enrichment, or an experimental grouping baseline.
```

---

## 3. Canonical Registry reuse boundary

Relevant owner code:

```text
src/jobhunter/canonical_registry.py
src/jobhunter/canonical_registry_review.py
```

`CanonicalRegistryReviewReader` already provides the correct currentness/provenance seam over exact accepted/current P1.6 claims and reviewed mappings.

P2.3A should reuse that seam rather than implement another mapping/currentness system.

Registry authority remains narrow:

```text
reviewed source/canonical correspondence only
```

It must not receive:

- work-implied expectations;
- model-inferred prerequisites;
- local semantic grouping merely because a model used the same label twice;
- temporary P2.3 profile organization;
- inferred depth or ownership.

Those remain profile interpretation, not reusable canonical truth.

---

## 4. P2.1 seed coverage is intentionally insufficient for direct P2.3 projection

P2.1 final acceptance deliberately closed with only four canonical concepts:

```text
platform:linux
tool:powershell
education_credential:ccnp-security
responsibility:manage-next-generation-firewalls
```

and six reviewed claim decisions:

```text
5 mapped
1 explicitly unmapped
```

This is a feature of the accepted design, not a defect. P2.1 explicitly did not authorize bulk ontology expansion.

The representative P2.3A capabilities under consideration—RAG, Tool/Function Calling, Python, MCP, speech/PyTorch, backend/API/service integration—therefore cannot assume existing canonical requirement mappings.

Consequences:

1. **Unmapped must remain first-class.** A useful job capability profile cannot disappear merely because no canonical concept exists yet.
2. **P2.3A must not begin with bulk canonicalization of 140 requirements.**
3. **Canonical identity should enrich/anchor a profile where reviewed mappings exist, not gate profile usefulness.**
4. **Minimum new canonical reviews should be driven by representative acceptance needs, not a coverage quota.**

---

## 5. Do not prematurely choose a zero-model or new-model architecture

A purely deterministic projection from P1.6 + Registry is attractive because it introduces little new authority. However, with intentionally sparse canonical coverage it may produce many exact but fragmented source-local requirement entries rather than a useful per-capability profile.

A brand-new P2.3 semantic model/prompt is also premature because Capability v9 already performs job-local semantic grouping and bounded reasoning.

The first post-authorization responsibility should therefore be an **architecture experiment**, not immediate durable profile persistence.

---

## 6. Recommended P2.3A-0 architecture experiment

If P2.3A is formally selected after B2 closure, begin with:

```text
P2.3A-0 — capability-profile composition/reuse experiment
```

No production schema/table or corpus-wide generation should be committed before this comparison.

Compare three strategies on a small heterogeneous evidence set.

### Strategy A — deterministic P1.6 + Registry projection

Inputs:

```text
accepted/current P1.6 requirements/responsibilities
+ CanonicalRegistryReviewReader mapping state
```

Behavior:

- preserve exact requirement/responsibility claims;
- attach reviewed canonical identity where available;
- keep explicit unmapped state otherwise;
- group only where deterministic/reviewed identity justifies it;
- no LM call.

Question:

> Is the result already useful enough, or too fragmented to answer the roadmap’s per-capability questions?

### Strategy B — reuse Capability-v9 job-local grouping as optional composition input

Inputs:

```text
Strategy A inputs
+ accepted/current Capability-v9 artifact where one already exists
```

Behavior:

- do not treat the v9 label as canonical authority;
- use accepted v9 organization/dimensions only as job-local interpretation;
- overlay reviewed Registry identities where exact source claims map;
- preserve conflicts/unmapped state rather than forcing correspondence.

Question:

> Does existing accepted Capability-v9 organization materially improve usability without creating a second authority or requiring regeneration?

### Strategy C — bounded reuse of Capability-v9 grouping machinery over current P1.6

Only if A is too fragmented and B cannot cover the representative jobs:

- reuse/extract the smallest neutral semantic grouping responsibilities from Capability v9;
- keep the same evidence-status and source-grounding discipline;
- do not copy the entire Capability-v9 artifact contract merely to rename it;
- do not introduce a second model-review loop;
- compare the incremental value against A/B.

Question:

> Is dedicated semantic grouping genuinely necessary for P2.3, and if so what is the minimum new contract responsibility?

---

## 7. Experimental evidence frame

Use heterogeneous cases, not six near-identical AI-agent examples.

Recommended representative checks:

```text
RAG / Tool Calling     — direct work + explicit requirements across tvMm/tNVe and requirement-only evidence elsewhere
Python                 — same broad capability with materially different depth/context across postings
MCP                    — narrow requirement contrast, including t7Ay specialization
Speech / PyTorch       — t7ck requirement-only narrow technical domain
Backend/API integration — cross-role context with direct work in some postings and qualification-only evidence in others
```

At minimum include:

- one dense direct-work posting;
- one adjacent/broader direct-work posting;
- `t7ck` requirement-only speech role;
- `t7Ay` requirement-only LLM/RAG/MCP role.

Requirement-only cases are mandatory boundary evidence: no strategy may fabricate work activities when P1.6 contains zero responsibilities.

---

## 8. Experiment evaluation rubric

For each strategy evaluate:

```text
source coverage completeness
exact evidence recoverability
canonical identity correctness
unmapped/unknown preservation
requirement-strength correctness
source-explicit depth preservation
work-activity fabrication risk
technical-scope precision
semantic duplication / fragmentation
cross-job comparability
browser readability / user effort
new model-call cost
new persistence complexity
new authority blast radius
```

Prefer the least complex strategy that materially improves the user’s ability to answer:

> What exactly does this job require me to know or do with this capability, how deep is the explicit requirement, what work supports that interpretation, and what remains unknown?

---

## 9. Likely implementation direction if the experiment supports it

The current code audit makes the following architecture **provisional**, not yet authorized:

```text
accepted/current P1.6
        │
        ├── exact requirements/responsibilities/currentness
        │
CanonicalRegistryReviewReader
        │
        ├── reviewed canonical identity where available
        └── explicit pending/unmapped state otherwise
        │
optional accepted Capability-v9/local grouping semantics
        │
        ▼
JobCapabilityRequirementProfile read model / candidate contract
        │
        ├── exact source truth
        ├── canonical identity status
        ├── multidimensional requirement/work context
        ├── evidence-status separation
        └── unknowns
```

The first useful browser surface should emphasize requirement understanding and comparison, not taxonomy maintenance.

If the read-model experiment proves stable and repeatedly useful, then define a **separate versioned immutable P2.3 profile artifact** with explicit dependencies/currentness rather than mutating Capability-v9 persistence in place.

Persistence should be earned by demonstrated reuse/history needs, not created merely because the roadmap names a future entity.

---

## 10. Explicit non-decisions

This audit does not decide that:

- P2.3A is authorized now;
- Capability v9 must be regenerated for snapshot 15;
- P2.3 can never use an LM;
- P2.3 should share Capability-v9 storage;
- all requirement concepts need canonical mappings;
- P2.2C is rejected;
- candidate profile output is durable authority before review;
- one scalar depth score should exist.

---

## 11. Trigger after B2 closure

After the local R3-R6 Registry batch is proven and B2 is formally closed:

```text
reconcile proven B2 state
→ re-evaluate the post-B2 pre-decision for contradictions
→ if P2.3A is selected:
     authorize P2.3A-0 composition/reuse experiment first
     compare Strategy A / B / conditional C
     choose the profile ownership boundary from evidence
     then write the durable P2.3A implementation/acceptance plan
→ only then implement persistent production profile state
```

This sequence deliberately turns existing accepted architecture into evidence before creating another semantic subsystem.
