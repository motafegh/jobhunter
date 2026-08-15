# Capability v9 Strictness Audit and Contract Simplification

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** implementation complete; deterministic CI PASS; dense live acceptance pending

## Why this audit happened

Two dense `tG9K` Capability v9 live runs failed before persistence even though accepted English
P1.6 artifact 36 remained correct/current.

The failures showed that JobHunter had mixed two very different kinds of strictness:

1. **truth-protection strictness** — rules that protect source coverage, provenance, evidence,
   requirement strength, explicit depth, and fail-closed persistence;
2. **forced-enrichment strictness** — rules that require the model to invent additional analytical
   content even when accepted source facts are already sufficient.

The second category created direct contradictions with v9's goal of avoiding unsupported semantic
inflation. This audit removes or narrows that category while preserving the first.

## Decision principle

A validation rule remains hard only when violating it could corrupt or lose authoritative source
truth, provenance, or the meaning of the accepted job evidence.

A model-owned analytical enrichment is optional. If it is unsupported or unsafe, JobHunter may
filter it. The system must not require another inference merely so the artifact looks more
"intelligent."

## Rules retained as hard boundaries

| Rule | Disposition | Reason |
|---|---|---|
| Every capability-relevant P1.6 fact must be assigned/linked | KEEP HARD | Prevents source loss |
| Every P1.6 responsibility must be linked | KEEP HARD | Prevents duty loss |
| Assignment indices must exist and belong to owned partitions | KEEP HARD | Provenance integrity |
| Evidence must resolve to known source evidence | KEEP HARD | Prevents invented evidence |
| Dense jobs cannot collapse all source facts into one group | KEEP HARD | v7 live failures proved this architecture is unreliable |
| Education / duration-only experience remain role-level constraints | KEEP HARD | Prevents role-entry constraints becoming technical capability groups |
| Requirement strength is JobHunter-owned/deterministic | KEEP HARD | Prevents preferred/contextual → required inflation |
| Source-explicit depth is JobHunter-owned/deterministic | KEEP HARD | Prevents model depth inflation |
| Preferred/contextual-only facts cannot independently justify an inferred prerequisite | KEEP HARD | Preserves source optionality |
| Unsupported ownership/lifecycle/autonomy/architecture claims are rejected/filtered | KEEP HARD | Prevents authority/scope inflation |
| Incomplete final source truth cannot persist | KEEP HARD | Artifact integrity |

## Rules removed or relaxed

### 1. Mandatory derived reasoning per profile — REMOVED FOR V9

Historical v8 required every profile to contain at least one derived analytical statement or an
explicit `unknown_scope` item.

That contradicted v9's truth policy. A model that responsibly returned no extra inference was
rejected merely because it did not invent something.

V9 now allows:

```text
neutral capability grouping
+ exact source links
+ deterministic requirement strength
+ deterministic source-explicit depth
+ deterministic source work activities
+ zero optional model-derived enrichment
```

Historical v8 keeps its old behavior; the change is v9-specific.

### 2. Forced unknown-scope filler — REMOVED

Absence of a safe derived claim does not itself prove an unknown boundary. V9 no longer requires the
model to manufacture `unknown_scope` simply to satisfy schema shape.

### 3. Duplicate hard-coded v8 revalidation after typed provider validation — REMOVED

The Instructor provider already validates and normalizes the model result against the requested
response model. The staged engine previously discarded that type information and revalidated the
serialized dictionary using hard-coded v8 classes.

This accidentally reintroduced obsolete v8 semantics after a v9 stage had already passed v9
validation.

The inference result now carries its validated Pydantic model. The staged engine uses that typed
result when available and only falls back to historical revalidation for legacy/fake providers.
V8 defaults remain unchanged.

### 4. Whole-profile failure for one unsafe optional inference — REPLACED WITH ITEM FILTERING

Optional model-derived expectations are evaluated independently. One unsafe item is discarded and
recorded in uncertainties instead of causing regeneration of the whole profile.

This does not affect deterministic source facts.

### 5. Inflated per-profile summary causing another model retry — REPLACED WITH SAFE FALLBACK

The semantic group planner has already produced and validated a neutral group summary. If the later
profile model expands that summary with unsupported depth/ownership/obligation, v9 falls back to the
validated group summary and records the replacement.

The group-planning semantic boundary itself remains hard because there is no earlier safe semantic
grouping to fall back to.

### 6. Blanket ban on `necessary` / `prerequisite` — NARROWED

V9 exposes an explicit `model_inferred_prerequisite` evidence status. Rejecting the words
`necessary` or `prerequisite` even inside that semantic type was contradictory.

New rule:

- an explicit `model_inferred_prerequisite` may use necessity/prerequisite language;
- its **statement** still may not present the inference as employer-stated `required`, `must`, or
  `mandatory`;
- its rationale may accurately refer to a required source fact;
- preferred/contextual-only facts still cannot independently support that inference.

### 7. Derived depth as a mandatory source of value — REMOVED

`depth_signals` remain available as optional work-implied analytical enrichment, but source-explicit
depth is already deterministic. A profile is not considered incomplete merely because the model
adds no extra depth inference.

## Compatibility approach

Historical v7/v8 models remain intact.

V9 introduces its own final profile/draft contract that allows zero enrichment while retaining exact
source linkage. The trusted historical deterministic v7 reconciliation logic is reused through an
internal compatibility bridge for zero-enrichment profiles; that temporary bridge is removed before
v9 validation/persistence and never becomes user-visible semantic content.

The v8 staged engine is now version-neutral at two extension points:

- version-specific reasoning-draft model;
- version-specific reconciler.

Its default values remain the historical v8 classes/functions, so existing v8 behavior is preserved.

## Regression proofs

The v9 tests now prove:

- zero-derived/no-unknown per-group reasoning is valid in v9;
- the same zero-derived response still fails under historical v8;
- a final v9 profile with zero model-derived enrichment survives deterministic reconciliation;
- deterministic source strength/depth are still injected;
- complete source truth remains required;
- unsafe optional items are filtered individually;
- summary inflation falls back to the validated group summary;
- required-grounded inferred prerequisites may use prerequisite language;
- preferred-only inferred prerequisites are still filtered;
- typed v9 stage output is not accidentally revalidated as v8.

## Deterministic gate

```text
CI run 849
Ruff:               PASS
full pytest:        PASS (434 tests)
warnings-as-errors: PASS
```

## Resulting v9 semantic contract

```text
STRICT / AUTHORITATIVE
accepted P1.6 source truth
+ complete coverage
+ provenance/evidence
+ source requirement strength
+ source-explicit depth
+ source work activities
+ role-level constraints

OPTIONAL / MODEL-OWNED
neutral semantic grouping
+ strongly implied decomposition when defensible
+ inferred prerequisites when defensible
+ operational context/practices when defensible
+ work-implied extra depth when defensible
+ explicit unknown scope when genuinely useful

If optional enrichment is absent:
  VALID

If optional enrichment overreaches:
  FILTER/FALL BACK

If authoritative source truth is incomplete or invalid:
  FAIL CLOSED
```

## Current state and next gate

No Capability v9 artifact existed before this simplification, so no persisted v9 artifact needs to
be deleted or migrated. The candidate identity remains:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Public Capability remains v7/v4.

The next gate is one dense `tG9K` v9 candidate run against accepted P1.6 artifact 36, followed by
mechanical and semantic review. Do not promote v9 from deterministic tests alone. Sparse `t4jp`
non-regression remains after dense acceptance.
