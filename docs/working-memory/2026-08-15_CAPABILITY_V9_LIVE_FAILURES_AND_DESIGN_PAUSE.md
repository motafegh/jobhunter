# Capability v9 Live Failures and Design Pause

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** implementation paused by explicit user decision; design discussion required before any further code or live rerun

## Purpose

This checkpoint records the exact Capability state after two failed dense `tG9K` v9 live runs.
It is intentionally documentary only. No further implementation is authorized at this point.

## Stable upstream state

English P1.6 is already promoted and closed:

```text
Dense job:                 tG9K
Accepted English P1.6:     artifact 36
Contract:                  job-analysis-english-v20 / job-analysis-v5
Requirements:              33
Responsibilities:          8
Public runtime proof:      reused through normal `jobhunter jobs analyze tG9K`
```

Sparse `t4jp` artifact 37 is also accepted/current under the same English v20/v5 contract.
The current Capability problem is therefore downstream of accepted P1.6, not a P1.6 regression.

## Capability history leading to v9

### Public/historical v7

`job-capability-intelligence-v7 / job-capability-intelligence-v4` remains the public accepted
Capability route, but its historical dense artifact 9 depends on old P1.6 artifact 29 and is no
longer current-chain.

Two attempts to rebuild v7 against P1.6 artifact 36 failed before persistence. The dense one-shot
architecture repeatedly lost source-link coverage and collapsed evidence into one oversized profile.
That path was rejected rather than weakening coverage validation or increasing retries.

### Candidate v8

V8 introduced source-led staged reasoning:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation/source truth
```

Dense `tG9K` completed mechanically with:

```text
31/31 capability-relevant requirements linked
8/8 responsibilities linked
4 capability profiles
role-level requirement indices [31, 32]
```

This proved the staged architecture solved the v7 dense coverage failure.

V8 was nevertheless semantically rejected because model-owned prose inflated depth, obligation,
ownership/lifecycle scope, and preferred/contextual facts.

### Candidate v9

V9 kept the successful v8 staged architecture and introduced semantic guardrails plus corrected
capability-vs-role-level depth accounting under a new identity:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

No v9 artifact has ever persisted as of this checkpoint.

## Live v9 failure 1 — semantic guardrail granularity

The first dense v9 live run reached bounded profile reasoning but failed before persistence.

Generation 1 used unsupported technical-depth language in the profile summary (`expertise`). That
was correctly treated as a hard semantic failure.

The bounded repair corrected the summary, but optional derived depth items then used obligation or
necessity language such as:

```text
necessary
prerequisite
must
necessitates
```

Because those optional items were validated at whole-profile level, one unsafe inference caused the
entire bounded profile to fail.

Diagnosis at that point:

- summary/group semantic inflation should remain hard-fail;
- optional derived expectations should fail closed individually instead of forcing whole-profile
  regeneration;
- deterministic P1.6 strength/depth/work/source truth must remain authoritative.

A filtering correction was implemented and deterministic CI 838 passed Ruff, full pytest, and
warnings-as-errors.

## Live v9 failure 2 — inherited "must add derived reasoning" invariant

The second dense v9 live run also failed before persistence.

Both generations returned a bounded MLOps/production profile containing a summary and an empty
`depth_signals` list, with no additional derived sections. The surfaced validation error was:

```text
Capability profile reasoning must add derived reasoning or an explicit unknown boundary
```

This comes from the inherited Capability v8 `CapabilityProfileReasoningV8` contract. V8 requires at
least one derived expectation or one explicit unknown-scope item.

This exposes an unresolved design contradiction in v9:

```text
v9 semantic policy:
  do not force unsupported extra reasoning;
  unsafe optional derived expectations may be discarded;
  deterministic P1.6 facts may be sufficient for a bounded profile.

inherited v8 schema invariant:
  every profile must still add derived reasoning or explicit unknown scope.
```

Therefore the previous documentation statement that a v9 profile was "allowed to contribute no safe
model-derived expectations after filtering" was an intended design property but was not actually
effective in the live runtime because the inherited v8 validator executes that non-empty-derived
requirement.

The second live result also shows that the model can deliberately choose not to manufacture extra
depth reasoning when the evidence does not justify it. Under the current inherited contract, that
restraint itself becomes a validation failure.

Generation 2 additionally put `requires` into its summary. The surfaced failure occurred at the
inherited v8 non-empty-derived validator before a successful v9 artifact could exist, so this run
must not be interpreted as proving the summary would otherwise have passed all v9 semantic guards.

## What is proven vs unresolved

### Proven

- P1.6 v20/v5 is accepted/current and is not the source of this failure.
- v7 one-shot dense Capability generation is not reliable enough for promoted artifact 36.
- v8 source-led staging solves dense source-coverage/linkage mechanically.
- v8 semantics are too permissive and must not be promoted.
- v9 semantic guardrails correctly identify real downstream authority inflation.
- no invalid v9 artifact persisted in either live attempt.
- public Capability routing remains v7 and has not been silently changed.

### Unresolved

The correct semantic contract for model-owned Capability reasoning is not settled.
In particular, we must decide whether a bounded profile should:

1. be valid with only a neutral capability summary plus deterministic source truth;
2. require at least one genuinely derived analytical statement;
3. require an explicit unknown boundary when no safe derived statement exists;
4. distinguish mandatory analytical sections from optional enrichment sections in a new contract;
5. reduce or remove model-owned `depth_signals` now that source-explicit depth is deterministic;
6. change the role of Capability itself so it does not reward speculative elaboration.

These are design questions, not implementation details.

## Current artifact/contract state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT
Capability v8 dense candidate       PERSISTED / MECHANICAL PASS / SEMANTIC REJECT
Capability v9 artifact              NONE PERSISTED
Capability public route             still v7/v4
Capability v9 candidate             IMPLEMENTED BUT LIVE-UNACCEPTED
Blueprint                           DEFERRED / NON-AUTHORITATIVE
Phase 2                             BLOCKED
```

## Explicit pause decision

Per user instruction on 2026-08-15:

```text
STOP implementation for now.
Do not patch v9 again.
Do not create v10.
Do not rerun Capability live generation.
Document the complete state, then discuss the design together.
```

Accordingly, no further Capability code change, schema change, prompt change, retry-policy change,
or live LM Studio run should occur until a new design decision is made explicitly.

## Next action

Discussion/design review only.

The next conversation should start from the contradiction above and decide what Capability is
supposed to add beyond accepted P1.6 source truth, what model-owned reasoning is actually valuable,
and which outputs are mandatory versus optional. Only after that decision should implementation
resume.
