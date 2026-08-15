# Capability v8 source-led partitioning

**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Branch:** `main`  
**Status:** Candidate implemented; deterministic CI PASS; dense live acceptance pending

## Why v8 exists

Promoted English P1.6 v20/v5 is accepted and operationally current. Dense `tG9K` uses P1.6 artifact 36 with 33 requirements and 8 responsibilities.

Capability v7 remains the historical accepted bounded baseline through artifact 9, but that artifact depends on historical P1.6 artifact 29. Rebuilding the same one-shot v7 reasoning contract against promoted artifact 36 exposed a stable dense-input failure mode.

### Live rebuild failure 1

The first current-chain v7 rebuild failed after two bounded generations:

- generation 1 omitted most capability-relevant P1.6 requirement links;
- generation 2 repaired much of the requirement ledger but invented responsibility index `9`, even though artifact 36 has responsibility indices `0..7`;
- no Capability artifact persisted.

A narrow inference-time source-link repair was added so mechanically impossible positive indices could be discarded and exact evidence-backed links could be recovered before the existing strict whole-artifact coverage validator ran. Negative/type-invalid indices still failed closed. CI 811 passed.

### Live rebuild failure 2

The rerun still failed after both bounded generations.

Both generations independently collapsed the dense role into one giant capability profile. Even after the retry was told which requirement indices were missing, it did not restructure the answer. After deterministic exact-evidence link recovery, the final validator still reported the same large omitted set:

```text
[2, 3, 4, 5, 6, 9, 10, 12, 13, 15, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30]
```

This is no longer an isolated bookkeeping typo. It is a repeatable architecture mismatch: one small-model answer was being asked to simultaneously invent the whole-job capability decomposition, remember a dense 31-item capability-requirement ledger plus 8 responsibilities, attach exact source indices, add derived reasoning, and satisfy final semantic constraints.

## Decision

Do not increase retries. Do not loosen final coverage validation. Do not keep patching the public v7 one-shot architecture for this dense promoted input.

Capability v7 remains historical accepted evidence. A new v8 candidate changes the inference architecture while preserving the established source-truth and reconciliation boundaries.

## Capability v8 architecture

```text
accepted P1.6 v20/v5 source truth
        ↓
compact semantic capability-group plan
        ↓
bounded source-fact assignment partitions
        ↓
one bounded reasoning call per validated group
        ↓
deterministic source-link injection
        ↓
existing strict v7 whole-artifact reconciliation/source truth
        ↓
persist only after complete coverage validation
```

### Stage 1 — semantic group plan

The model proposes a small coherent group plan only.

It does **not** own requirement/responsibility source indices.

Dense jobs require at least two groups. The planner is told not to turn every technology into a separate group and not to create education/standalone experience-duration groups.

### Stage 2 — bounded source-fact assignment

JobHunter partitions capability-relevant requirements in bounded chunks of at most 8. Responsibilities are distributed across those bounded assignment requests exactly once.

Each assignment response must:

- contain every owned requirement index exactly once;
- contain every owned responsibility index exactly once;
- use only known capability group IDs;
- attach one fact to at most two groups;
- contain no extra or missing owned source fact.

The final dense assignment must use at least two groups.

### Stage 3 — bounded per-group reasoning

For each actually-used group, the model receives only that group's assigned requirements/responsibilities and matching P1.6 evidence references.

The model does **not** emit:

- source requirement indices;
- source responsibility indices;
- source-explicit strength;
- source-explicit depth;
- source-explicit duties.

It may emit only bounded derived reasoning and unknown boundaries.

JobHunter then injects the already-validated source links deterministically.

### Final reconciliation

The assembled v8 draft is passed through the existing strict Capability v7 reconciliation/source-truth machinery.

That still deterministically owns:

- requirement strength from accepted P1.6;
- source-explicit depth from accepted P1.6;
- source-explicit work activities from accepted P1.6 responsibilities;
- complete source-truth projection;
- role-level requirement separation;
- independence suppression;
- cross-capability observation suppression;
- final complete coverage validation.

The persisted shape remains schema `job-capability-intelligence-v4`; the new prompt/runtime identity is `job-capability-intelligence-v8`.

## Additional preserved boundary

P1.6 free-form `rationale` is removed from every model-facing v8 payload. The persisted P1.6 artifact is unchanged. Authoritative concept/type/strength/depth/evidence/confidence remain available, and final deterministic reconciliation still uses the accepted extraction.

## Implementation

```text
src/jobhunter/capability_v8_models.py
src/jobhunter/capability_inference_v8.py
src/jobhunter/capability_service_v8.py
scripts/run_capability_v8_candidate.py
tests/test_capability_v8_models.py
tests/test_capability_v8_service.py
```

Public `jobhunter jobs capability` still routes to v7. V8 is candidate-only until dense and sparse live acceptance passes.

## Deterministic gate

Final corrected v8 code head before this documentation record:

```text
96a4f07605d01f7b6d20ac67af5d35f8c2936022
```

GitHub Actions CI run 821:

```text
Ruff:                  PASS
full pytest:           PASS
warnings-as-errors:    PASS
```

The staged-service tests prove:

- rationale does not reach the model;
- education/standalone role-level constraints remain separate;
- bounded assignments cover all supplied source facts exactly;
- per-profile source links are injected by JobHunter;
- final v7 reconciliation reports no unlinked capability requirement/responsibility in the test chain;
- candidate persistence records the staged v8 architecture.

## Acceptance boundary

V8 is **not accepted or public yet**.

Next live gate:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v8_candidate.py --job-id tG9K
```

If a dense artifact persists, inspect it mechanically and semantically before any promotion. At minimum verify:

- dependency is P1.6 artifact 36;
- contract is v8/v4;
- complete capability-requirement linkage;
- complete responsibility linkage;
- role-level constraints retained separately;
- all explicit source depth represented through deterministic reconciliation;
- at least two coherent capability profiles;
- no contextual/preferred tool promoted to mandatory/mastery;
- no fabricated autonomy/ownership/leadership;
- no unsupported architecture claim;
- no generic curriculum expansion.

Only after dense acceptance should sparse `t4jp` v8 non-regression run. Only after dense + sparse acceptance may public Capability routing/promotion be considered.
