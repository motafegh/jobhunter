# Blueprint v3 Grounded Interpretation Experiment

**Status:** Active B4 candidate; implemented on `main`, not semantically accepted  
**Date:** 2026-08-11  
**Accepted upstream chain:** English P1.6 artifact 29 → Capability artifact 9  
**Candidate runtime/schema:** `role-capability-blueprint-v3` / `role-capability-blueprint-v2`

## Purpose

The earlier Blueprint v2 structure was useful but could turn a technology list into an overly specific architecture, label plausible workflows `highly_likely`, strengthen optional cloud/edge wording, or assign source-named tools runtime roles the vacancy did not establish.

B4 keeps Blueprint as the human-facing professional interpretation layer while making the strongest conclusions auditable against accepted upstream truth.

## Boundary

```text
accepted P1.6 artifact 29
        ↓
accepted Capability v7 artifact 9
        ↓
model produces practitioner interpretation
with explicit upstream links / scenario basis
        ↓
JobHunter deterministic reconciliation
        ↓
Blueprint v3/v2 artifact
```

The model remains free to add useful professional interpretation. It does not become the source-of-truth layer.

## Deterministic protections

### Capability-area grounding

Every Blueprint capability area carries `source_capability_indices`. The union of those links must cover every accepted Capability profile. A generic ungrounded curriculum area cannot satisfy the contract.

### Source-named tools

A `source_named` tool must link accepted P1.6 requirement/responsibility indices. JobHunter deterministically derives:

```text
source_requirement_strength
source_depth_signals
```

from accepted P1.6 rather than trusting model-generated bookkeeping.

This prevents examples such as contextual PyTorch/TensorFlow from inheriting `Python (expert)` and prevents preferred/contextual tools from silently becoming required.

`likely_example` and `possible_example` tools carry no P1.6 source links, source strength, or source depth.

### Role-level constraints

Degree/experience constraints are injected deterministically from Capability v7 `source_truth.role_level_requirement_indices`. For `tG9K` the expected indices are:

```text
25  Master's degree
26  Professional experience — three to six years
```

### Hidden requirements

A `highly_likely` hidden requirement must link accepted Capability work and/or responsibilities. Plausible professional judgment may remain less strongly grounded, but it must not be presented as employer fact.

### Scenario basis

Every end-to-end scenario declares one of:

```text
source_stated_workflow
professional_example
```

A practitioner-created `professional_example` cannot be `highly_likely`. If it depends on unstated topology, latency, vendor, batch/streaming mode, cloud/edge placement, scale, or ownership, those assumptions remain explicit.

A `source_stated_workflow` must link accepted responsibilities. A `highly_likely` scenario cannot carry unresolved assumptions.

## What remains semantic review

The deterministic contract does not pretend to prove whether:

- an inferred subskill is professionally useful;
- a work product is a good interpretation;
- a failure mode is relevant enough to include;
- an example workflow is technically coherent;
- the prose is more useful than rereading the vacancy;
- the model over-focuses one area despite mechanically complete coverage.

These remain B4 live-review questions.

## Deterministic gate

Before a live Blueprint run:

```bash
python -m pip install -e ".[dev]"
ruff check .
python -m pytest
python -m pytest -W error
```

Confirm the active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v3
role-capability-blueprint-v2
```

## Live `tG9K` B4 procedure

Keep the accepted upstream chain fixed. Do not rerun P1.6 or Capability merely to test Blueprint.

```bash
jobhunter jobs blueprint tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v3_snapshot.py
```

Then inspect:

```bash
git diff --check
git diff -- review-snapshots/jobs/tG9K.json
git status --short
```

If the mechanical audit passes and the snapshot contains only the intended current Blueprint change, commit the review artifact:

```bash
git add review-snapshots/jobs/tG9K.json
git commit -m "review: evaluate tG9K blueprint v3"
git push origin main
```

If generation fails, preserve the failure in the local attempt ledger and diagnose the exact validation/length/model behavior. Do not fabricate or commit an empty Blueprint.

## Semantic acceptance criteria

B4 passes only if complete live review confirms, at minimum:

- Blueprint covers both accepted Capability profiles without generic curriculum expansion;
- Master's degree and 3–6 years are preserved exactly as role-level constraints;
- source-named tools retain accepted P1.6 strength/depth;
- only Python carries explicit `expert` depth unless another tool has independent source depth;
- contextual/preferred cloud, edge, frameworks, MATLAB, and C/C++ are not promoted;
- technology lists are not assembled into a claimed hidden architecture;
- practitioner-created workflows are clearly examples rather than employer topology;
- source-stated/high-confidence workflows do not contradict unresolved unknowns;
- hidden requirements are professionally defensible and correctly calibrated;
- tool/protocol/platform semantics remain technically correct;
- `important_unknowns` preserve materially unresolved architecture/operational questions;
- the Blueprint adds useful professional interpretation beyond P1.6/Capability without manufacturing certainty.

Passing deterministic checks alone does not accept B4.
