# P2.2A `t4qV` First Live Generation — Structured Reference Failure and Repair

**Date:** 2026-08-26  
**Phase:** P2.2A Job Work Intelligence v1  
**Status:** STRUCTURAL GENERATION DEFECT REPAIRED / REAL-LOCAL RERUN PENDING  
**Repository branch:** `main`

## 1. Trigger

The first real-local P2.2A semantic/product run was executed against accepted/current `t4qV`:

```text
python -m jobhunter.work_intelligence_cli generate t4qV
```

The run reached the configured local model (`gemma-4-e2b-it`) and Instructor attempted two bounded generations.

Both generations failed Pydantic validation before any successful `JobWorkIntelligenceArtifact` could be persisted.

## 2. Observed failure

All four generated work themes failed the same contract:

```text
A work theme requires at least one responsibility or role-purpose reference;
requirements alone cannot become duties
```

The model's prose/rationales did identify concrete responsibility indices, for example themes corresponding to responsibility groups such as `0,3,8`, `1,2,6`, `5`, and `7,9`.

However, the model omitted the dedicated structured fields:

```text
responsibility_indices
role_purpose_indices
```

Mentioning an index in `rationale` is not provenance. The deterministic validator therefore correctly rejected the candidate.

No successful Work Intelligence artifact was created from this run. Failed-attempt history may remain as bounded operational evidence.

## 3. Root cause

`WorkTheme` originally declared both direct-reference arrays with `default_factory=list`.

That made the fields optional in the JSON Schema supplied to Instructor/LM Studio, while the post-parse Pydantic model validator required at least one direct work reference.

The resulting contract was internally inconsistent:

```text
JSON Schema presented structured reference arrays as optional
→ model omitted them and mentioned indices only in prose
→ Pydantic filled missing arrays with []
→ post-validation correctly rejected every theme
→ Instructor retry repeated the same structurally permitted omission
```

This is a schema/generation-contract defect, not evidence that the direct-work provenance validator is too strict.

## 4. Repair

Implementation commit:

```text
40c3f9a3370308763e75ac911a0b43dbd1c2ec7f
fix: require P2.2A structured work references
```

Changes:

- `WorkTheme.responsibility_indices` is now required in generated JSON;
- `WorkTheme.role_purpose_indices` is now required in generated JSON;
- the same explicit structured-provenance rule is applied to `DeliverableCandidate` reference arrays;
- arrays may still be empty individually, but a `WorkTheme` must retain at least one direct responsibility/role-purpose reference;
- no validator was weakened;
- requirement-only evidence still cannot manufacture a duty.

Regression commit:

```text
d02013efc0d24a3411ef7ef7cb01eb2d4a8612f0
test: lock P2.2A structured provenance schema
```

New regression coverage proves:

1. WorkTheme JSON Schema requires both structured direct-work reference fields;
2. DeliverableCandidate JSON Schema requires both structured direct-work reference fields;
3. prose such as `Covers responsibilities 0, 3, and 8` cannot substitute for structured provenance;
4. deliverable rationale text cannot substitute for structured provenance.

## 5. Repository quality evidence

GitHub Actions run for `d02013efc0d24a3411ef7ef7cb01eb2d4a8612f0` completed successfully.

Observed gates:

```text
Ruff                       PASS
full pytest                PASS
pytest -W error            PASS
```

This proves repository-level mechanical correctness for the repair and regression.

## 6. Separate semantic observation — not yet repaired

The rejected model output twice used wording equivalent to:

```text
end-to-end design, implementation, and management
```

The P2.2A prompt explicitly prohibits inventing `end-to-end` / full-lifecycle scope.

Because both candidates were structurally invalid and no artifact was accepted, do not yet introduce a wording-specific patch solely from this blocked generation.

Next valid `t4qV` generation must be reviewed for this boundary. If lifecycle/ownership inflation persists in a structurally valid candidate, treat it as a separate repeatable semantic defect and add the smallest general evidence-backed guard rather than a vacancy-specific phrase patch.

## 7. Current gate

```text
P2.2A implementation                    COMPLETE
repository deterministic quality gates  PASS
first t4qV live generation               BLOCKED / repaired schema defect
schema/regression repair                 COMPLETE
post-repair real-local t4qV rerun         PENDING
semantic/product usefulness review       PENDING
P2.2A acceptance                         OPEN
P2.2B                                    NOT AUTHORIZED YET
P2.2 public-corpus publication           NOT AUTHORIZED
```

## 8. Exact next action

On the user's real local environment:

```bash
git pull --ff-only origin main
source .venv/bin/activate
python -m jobhunter.work_intelligence_cli generate t4qV
```

Review the resulting valid candidate for:

- structured responsibility/role-purpose reference coverage;
- useful non-collapsed work themes;
- no fabricated duties from requirements;
- no invented lifecycle/ownership/leadership scope;
- deliverable evidence qualification if deliverables are emitted;
- role interpretation calibration;
- whether the output materially reduces manual synthesis effort.

Do not broaden to the other anchors until the first valid `t4qV` candidate is understood.
