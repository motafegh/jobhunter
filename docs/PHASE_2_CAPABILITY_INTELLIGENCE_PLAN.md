# JobHunter Capability Intelligence Plan

**Status:** Bounded per-job Capability v9 promoted/current; heterogeneous non-regression active  
**Date:** 2026-08-21  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/ROADMAP.md`, `docs/DOMAIN_AND_ANALYSIS_MODEL.md`, `docs/PRODUCT_SPECIFICATION.md`, and the current Phase-1 gate  
**Scope:** Record the accepted bounded Capability Intelligence architecture and the remaining heterogeneous acceptance required before Phase-2 corpus-scale capability-profile work. Despite this file's historical `PHASE_2_...` name, it does **not** authorize corpus-wide Phase-2 rollout before Phase-1 closure.

The exact active quality sequence is defined in `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 1. Current public identities

```text
P1.6 English prompt/runtime:  job-analysis-english-v20
P1.6 English schema:          job-analysis-v5

Capability prompt/runtime:    job-capability-intelligence-v9
Capability schema:            job-capability-intelligence-v5
```

Historical Capability v7/v8 implementations/artifacts remain reproducible but are not current public contracts.

Current accepted/current anchors:

```text
tG9K → P1.6 artifact 36 → Capability artifact 11
t4jp → P1.6 artifact 37 → Capability artifact 12
```

---

## 2. Why Capability exists

P1.6 and Capability Intelligence have different uncertainty contracts.

### P1.6

P1.6 is the strict factual substrate:

- role purpose when stated;
- responsibilities;
- requirements;
- requirement strength/optionality;
- concept type;
- explicit source depth/extent;
- exact evidence/provenance.

### Capability v9

Capability organizes accepted P1.6 facts into meaningful capability areas and may add bounded technical reasoning where defensible.

The accepted architecture deliberately separates model reasoning from authoritative source bookkeeping:

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic source-link injection
→ deterministic reconciliation
→ persisted Capability v9
```

Permanent authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Do not collapse P1.6 and Capability into one prompt/artifact.

---

## 3. What v9 changed from historical v7/v8

### Historical v7

The earlier one-shot architecture produced useful bounded evidence on an older P1.6 chain, but promoted-chain dense rebuilds exposed source-link/index loss and then a stable one-profile collapse that omitted many capability requirements.

Disposition:

```text
historical / reproducible / not current
```

### Historical v8

V8 introduced staged grouping/assignment/reasoning and mechanically achieved complete dense source coverage, but semantic review still found model-owned depth, ownership/lifecycle and optionality inflation.

Disposition:

```text
historical staged proof / semantic reject / not current
```

### Accepted v9

V9 keeps staged reasoning but removes model authority over facts that JobHunter can own deterministically.

Source requirement strength, source-explicit depth, source work and source links are deterministic. Model-generated source-truth echoes are redundant and filtered. Optional enrichment may be completely empty.

---

## 4. Current v9 guarantees

A persistable/current Capability v9 artifact must satisfy:

- every capability-relevant accepted P1.6 requirement is represented;
- every accepted responsibility is represented;
- all owned indices/evidence references are valid;
- dense sources do not collapse into one catch-all group;
- source requirement strength is deterministic;
- source-explicit technical depth is deterministic and concept-specific;
- source-explicit work is deterministic;
- role-level education and duration-only experience constraints remain role-level rather than becoming capability groups;
- preferred/contextual-only facts cannot independently justify an inferred prerequisite;
- unsupported ownership/lifecycle/autonomy/architecture claims are blocked or filtered;
- optional model enrichment may be absent;
- redundant model `source_explicit` echoes are discarded;
- incomplete authoritative source truth cannot persist.

The public service facade in `src/jobhunter/capability_service.py` routes to v9/v5.

---

## 5. Evidence and dependency identity

Capability v9 depends on the exact current accepted English P1.6 chain:

```text
source detail version
+ exact English projection artifact
+ exact English P1.6 artifact
+ capability model
+ Capability prompt/runtime version
+ Capability schema version
```

A newer source/translation/P1.6 dependency makes an older downstream Capability non-current.

Capability never guesses a newer translation independently from the P1.6 artifact it consumes.

---

## 6. Model-owned surface

The group planner proposes a small coherent capability grouping. Planner prose is non-authoritative and may be normalized.

The assignment stage performs bounded group assignment of JobHunter-owned source facts. It is provenance bookkeeping, not new source extraction.

Per-group reasoning may optionally add evidence-qualified items such as:

- strongly work-implied technical decomposition;
- defensible prerequisites;
- operational practices/context;
- work-implied depth beyond already-owned source-explicit depth;
- explicit unknown scope.

These are subordinate and fail closed. Zero optional enrichment is valid.

Do not expand a group into a generic technology curriculum.

---

## 7. Accepted anchor evidence

### Dense `tG9K`

```text
P1.6 artifact:                    36
Capability artifact:              11
Capability requirements linked:   31/31
Responsibilities linked:          8/8
Capability explicit depth:        5/5
All explicit depth:               6/6
Role-level requirement indices:   [31, 32]
Disposition:                      ACCEPTED / CURRENT
```

### Sparse `t4jp`

```text
P1.6 artifact:                    37
Capability artifact:              12
Capability requirements linked:   8/8
Responsibilities linked:          0/0
Explicit depth:                   0/0
Role-level requirement indices:   []
Disposition:                      ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Normal public commands reuse artifacts 11/12 on their exact dependencies. Review Snapshot confirms both Capability chains current and Blueprint non-current.

---

## 8. Product surfaces

Current surfaces include:

```bash
jobhunter jobs capability <job-id>
```

and the browser **Capability Intelligence** view.

Review Snapshots can export selected current-chain Capability evidence. The complete routine public current dataset is separately projected through `corpus/`.

Capability remains bounded per-job intelligence during Phase 1 and is **not** currently aggregated into Market.

---

## 9. Runtime policy

Capability inference uses local LM Studio through Instructor/Pydantic and the configured dedicated capability model when present.

Runtime policy:

```text
connection establishment: bounded
read timeout after connection: none
transport replay: disabled
max output tokens: bounded
validation retry: bounded
```

A legitimate local generation is not killed by an arbitrary read deadline after connection.

---

## 10. Heterogeneous non-regression — active

Public promotion is closed, but the stack is not yet frozen as Phase-2 input. It must survive materially different role families.

Current order:

```text
1. Python/software          ← tmBK active at P1.6 gate
2. network/security
3. operations/platform/DevOps
```

For each role:

1. inspect source and English projection quality;
2. run/reuse public English P1.6;
3. manually accept P1.6 before Capability;
4. run/reuse public Capability v9;
5. verify complete requirement/responsibility coverage and provenance;
6. verify source strength/depth/work remain correct;
7. inspect grouping coherence;
8. reject fabricated prerequisites, ownership, lifecycle, architecture, autonomy or mandatory strength;
9. classify any problem as deterministic defect, model limitation, or harmless non-authoritative variation;
10. convert repeatable deterministic defects into regression tests.

### Current `tmBK` position

`tmBK` is not yet at the Capability stage. Its first persisted P1.6 artifact 38 was semantically rejected for deterministic multi-signal depth propagation and must not feed Capability. Current v20 fixes the defect and adjacent depth/coverage cases; a clean P1.6 rebuild/review is required first.

Do **not** run `jobhunter jobs capability tmBK` until its rebuilt P1.6 artifact is manually accepted.

---

## 11. Promotion/freeze decision

Capability v9 is already the **promoted current public contract**. The remaining decision is not whether to return to v7/v8 or invent v10 for cosmetic prose differences.

After Python/software, network/security and operations/platform/DevOps pass without unresolved repeatable material defects:

```text
P1.6 v20 + Capability v9
→ freeze as accepted Phase-2 starting input
```

If heterogeneous evidence reveals a repeatable material correctness/provenance defect, fix the smallest correct deterministic/contract boundary and regression-test it. Do not vacancy-patch model prose.

---

## 12. Phase-2 boundary

Only after full Phase-1 closure may JobHunter scale into canonical market intelligence:

```text
canonical concept registry
→ reviewed aliases/mappings
→ responsibility/deliverable families
→ evidence-derived role archetypes
→ corpus-scale JobCapabilityRequirementProfile
→ Market v2
```

Capability v9 grouping and deterministic source truth may inform that design. Model-owned explanatory prose is not automatically canonical Phase-2 authority.

Blueprint output is not automatically promoted into the canonical layer.

---

## 13. Known technical debt / explicit limits

- The promoted bounded Capability layer is not a universal technology curriculum generator.
- It is not yet corpus-wide canonical taxonomy.
- It is not personal readiness/gap scoring.
- It is not application ranking or learning-plan generation.
- It does not make Blueprint authoritative.
- Current Market still aggregates accepted/current English P1.6, not Capability.
- Heterogeneous semantic stability is still under active review.

Do not add vector/RAG infrastructure, agent orchestration, multi-model voting or corpus-wide generative profiles merely because Capability exists.
