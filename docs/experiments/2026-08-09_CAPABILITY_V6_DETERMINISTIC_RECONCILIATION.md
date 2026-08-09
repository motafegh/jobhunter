# Capability v6 Deterministic Reconciliation Experiment

**Status:** Experimental B3 candidate; implemented on `main`, not semantically accepted
**Date:** 2026-08-09
**Accepted upstream anchor:** `tG9K` English P1.6 artifact 29

## 1. Purpose

Capability v4 is structurally valid but failed B3 semantic review on the accepted `tG9K` P1.6 substrate. The main observed failures were:

- accepted explicit P1.6 depth signals were omitted from Capability `depth_signals`;
- contextual/optional stack items were strengthened into required capability claims;
- cloud/deployment wording was overstated;
- pipeline/MLOps evidence was converted into unsupported end-to-end ownership;
- unrelated evidence could leak across capability areas.

A historical prompt-heavy Capability v5 experiment passed focused deterministic tests but exhausted `max_tokens` during the live bounded retry and was reverted. **v5 remains historical and must not be reused.**

The current B3 candidate reserves:

```text
Capability prompt/runtime: job-capability-intelligence-v6
Capability schema:         job-capability-intelligence-v3
```

## 2. Design decision

The model should reason. JobHunter should perform mechanically provable bookkeeping.

The v6 candidate changes the boundary to:

```text
accepted P1.6 artifact
        ↓
model chooses coherent capability areas
and links accepted P1.6 facts by index
        ↓
JobHunter validates those links
        ↓
JobHunter deterministically derives requirement strength
and source-explicit depth from the linked P1.6 facts
        ↓
revalidated Capability v6 artifact
```

Each capability profile now carries:

```text
source_requirement_indices
source_responsibility_indices
```

Every profile must link at least one accepted P1.6 requirement or responsibility. Out-of-range indices fail validation.

## 3. Deterministic reconciliation

### Requirement strength

The model emits `requirement_strength = unspecified` during generation.

After generation JobHunter derives the persisted value from linked accepted P1.6 requirement types:

```text
no linked requirement types       -> unspecified
one unique linked type            -> that exact type
multiple linked types             -> mixed
```

This prevents Capability from silently upgrading contextual/preferred P1.6 facts into required claims through bookkeeping drift.

### Source-explicit depth

The model is instructed not to reproduce source-explicit depth. After generation JobHunter copies accepted non-null P1.6 `depth_signal` values from linked requirements into Capability `depth_signals` with:

```text
evidence_status = source_explicit
exact accepted P1.6 evidence
explicit deterministic rationale
```

Model-generated `source_explicit` depth entries are discarded during reconciliation. The model may still add genuinely `strongly_implied_by_work` or `model_inferred_prerequisite` depth judgments when useful.

## 4. Prompt changes

The v6 prompt adds generic rules rather than domain-specific patches:

- explicit accepted-P1.6 source linkage per capability;
- fewer coherent capability profiles instead of catch-all tool-list profiles;
- requirement-strength bookkeeping delegated to JobHunter;
- source-explicit depth delegated to JobHunter;
- ownership/autonomy restraint unless authority evidence exists;
- direct evidence relevance per analytical statement;
- contextual/preferred tools must not be described as mandatory without independent support;
- unknown scope remains explicit.

No semiconductor-specific validator or word list is added.

## 5. What this candidate intentionally does not solve deterministically

The following remain semantic-review questions rather than brittle code heuristics:

- whether one capability grouping is professionally coherent;
- whether a derived prerequisite is technically justified;
- whether a scenario is realistic;
- whether prose overstates a contextual tool even when the stored strength is correct;
- whether evidence is semantically relevant beyond exact-source grounding;
- whether independence/ownership interpretation is professionally calibrated.

These are evaluated on the complete live artifact. They should become deterministic validators only when a relationship is mechanically provable and general.

## 6. Deterministic acceptance gate

Before any live model run:

```bash
python -m pip install -e ".[dev]"
ruff check .
python -m pytest
python -m pytest -W error
```

`main` CI must remain green. A deterministic failure blocks B3 acceptance.

## 7. Live `tG9K` acceptance procedure

Keep the accepted upstream chain fixed. Do **not** rerun P1.6 merely to test Capability v6.

Confirm LM Studio has the configured Capability model available, then run:

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v6_snapshot.py
```

The audit script performs the mechanical checks that previously required a large pasted terminal script. It exits non-zero on a deterministic failure and prints any accepted explicit-depth P1.6 requirements that the model failed to link to a capability.

Review the repository-safe live result with:

```bash
git diff -- review-snapshots/jobs/tG9K.json
```

The snapshot should select:

```text
accepted English P1.6 artifact 29
new dependency-current Capability v6/v3 artifact
no Blueprint from an older Capability chain
```

Do not rebuild Blueprint until B3 passes.

## 8. Mechanical live checks

`scripts/audit_capability_v6_snapshot.py` checks that:

- the snapshot remains anchored to accepted English P1.6 artifact 29;
- the selected Capability uses v6/v3 and belongs to the current dependency chain;
- every profile has at least one valid P1.6 requirement/responsibility link;
- persisted `requirement_strength` agrees with linked P1.6 requirement types;
- source-explicit depth entries exactly match deterministic propagation from linked P1.6 depth signals;
- no extra model-produced `source_explicit` depth survives reconciliation;
- no stale Blueprint is selected as the current chain.

The script also reports explicit-depth P1.6 requirements that are not linked to any capability. That condition remains a semantic-quality warning rather than mechanically forcing unrelated capability grouping.

## 9. Semantic live review

B3 still fails if the complete artifact materially repeats the v4 failure classes, including:

- contextual framework lists described as mastery/mandatory;
- optional cloud/edge wording described as necessary deployment scope;
- unsupported end-to-end lifecycle ownership;
- unrelated evidence attached to the wrong capability area;
- broad generic curriculum expansion;
- weak or incoherent capability grouping;
- useful accepted evidence disappearing because the model did not link it to any relevant capability.

The last point matters: deterministic reconciliation can only propagate a P1.6 fact into profiles the model actually links. Missing important links remain a semantic-quality failure.

## 10. Acceptance decision

Do not mark B3 accepted merely because deterministic tests pass or because a v6 artifact persists.

B3 passes only when the complete `tG9K` Capability v6 artifact is materially more useful than P1.6 while remaining correctly calibrated. Only then should the representative CI-3 sequence and Blueprint calibration continue.

If the v6 live generation again fails by output length, inspect the raw attempt finish reason/token usage before changing token limits. The next design option would be output reduction or bounded partitioning, not blindly increasing `max_tokens` or adding another prompt patch collection.
