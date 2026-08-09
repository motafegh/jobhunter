# Capability v7 Source-Truth Boundary Experiment

**Status:** Experimental B3 candidate; implemented on `main`, live semantic acceptance required  
**Date:** 2026-08-09  
**Accepted upstream anchor:** `tG9K` English P1.6 artifact 29  
**Supersedes:** rejected live Capability v6/v3 artifact 8

## Why v7 exists

Capability v6 proved that deterministic reconciliation is useful, but its live `tG9K`
artifact exposed a boundary defect: JobHunter could only preserve source facts that the model chose
to link.

The v6 live result:

- correctly derived `requirement_strength` from linked P1.6 requirements;
- correctly propagated linked `Strong` and `Hands-on` depth;
- linked only 3 of 27 accepted requirements and 2 of 7 responsibilities;
- therefore failed to carry Python `expert`, statistics `Solid`, time-series `Comfort`, and the
  role-level `three to six years` signal into the capability view;
- again inferred unsupported autonomy from partnership language;
- again inferred end-to-end ML lifecycle ownership from pipelines/MLOps/deployment;
- collapsed the dense role into one catch-all capability;
- attached some evidence to semantically unrelated derived claims.

B3 therefore remained open.

## Contract

```text
Capability prompt/runtime: job-capability-intelligence-v7
Capability schema:         job-capability-intelligence-v4
```

v5 remains a historical failed output-budget experiment. v6 remains a historical failed semantic
acceptance experiment. Neither identity is reused.

## Boundary change

v7 moves source truth completely outside model control:

```text
accepted P1.6 artifact 29
        ↓
JobHunter deterministic source partition
        ↓
model produces semantic grouping + derived reasoning draft
        ↓
JobHunter validates complete capability/responsibility coverage
        ↓
JobHunter deterministically reconstructs:
  complete source_truth
  requirement strength
  source-explicit depth
  source-explicit work activities
        ↓
Capability v7 persisted artifact
```

The model may group and interpret accepted facts. It may not decide whether those facts continue to
exist downstream.

## Deterministic source partition

JobHunter classifies accepted P1.6 requirements into:

```text
capability_requirement_indices
role_level_requirement_indices
```

Role-level requirements are deliberately narrow and mechanically identifiable:

- education requirements;
- standalone duration-only professional-experience requirements such as `three to six years`.

All other accepted requirements are capability-relevant and must be linked to at least one
capability profile.

Every accepted P1.6 responsibility must also be linked to at least one capability profile.

This is not a minimum-claim heuristic. It is provenance/coverage accounting over facts already
accepted by P1.6.

## Dense-source grouping guard

For a dense accepted source with at least 5 responsibilities and 12 requirements, one catch-all
capability profile is rejected.

The guard does not dictate a domain taxonomy. It only requires actual decomposition when the
accepted source has materially multi-part work and requirement evidence.

## Persisted `source_truth`

The final v7 artifact contains a JobHunter-owned `source_truth` object containing:

- all accepted role-purpose facts;
- all accepted requirements with index, concept, type, strength, depth, evidence, confidence;
- all accepted responsibilities with index, statement, evidence, confidence;
- capability-vs-role-level requirement partition;
- linked/unlinked requirement coverage;
- linked/unlinked responsibility coverage;
- explicit-depth coverage.

This makes source loss directly auditable in the Capability artifact.

## Deterministic profile fields

For each model-created capability profile JobHunter owns:

### Requirement strength

Derived only from linked accepted P1.6 requirement types:

```text
no linked types       -> unspecified
one unique type       -> that type
multiple types        -> mixed
```

### Source-explicit depth

Copied from every linked accepted P1.6 non-null `depth_signal`.

The model may add only derived depth judgments. Model-generated `source_explicit` depth is discarded.

### Source-explicit work activities

Copied from every linked accepted P1.6 responsibility.

The model does not need to spend output tokens restating responsibilities.

## Reduced model surface

v7 deliberately reduces the semantic surface that repeatedly overreached.

The model focuses on:

- coherent capability labels/summaries;
- source linkage;
- derived sub-capabilities;
- derived underlying knowledge/prerequisites;
- derived operational practices/context;
- useful unknown-scope boundaries;
- role interpretation and uncertainties.

The model is instructed to leave:

```text
requirement_strength = unspecified
source-explicit depth = absent
source-explicit work activities = absent
independence_expectation = null
cross_capability_observations = []
```

JobHunter fills the first three deterministically.

## Ownership/autonomy decision

Positive independence/ownership synthesis is deliberately deferred in v7.

Two reviewed live artifacts converted ordinary `partner`, `build`, `pipeline`, `production`,
`deployment`, and `MLOps` wording into unsupported autonomy/end-to-end ownership despite explicit
prompt restraint.

v7 therefore does not persist positive model-inferred independence. If the model emits one anyway,
JobHunter clears it and records an explicit unknown-scope boundary.

This is intentionally conservative. A future dedicated source-authority contract can reintroduce
positive ownership inference when there is evidence that can be validated generically.

## Cross-capability synthesis decision

v7 clears model-generated `cross_capability_observations`.

The field remains compatible with historical artifacts, but B3 no longer needs a second synthesis
layer inside Capability. Cross-capability professional narrative belongs more naturally in the
downstream Blueprint after Capability itself is accepted.

This also removes the exact location where v6 reintroduced unsupported end-to-end lifecycle
ownership.

## Deterministic gate

Before live inference:

```bash
ruff check .
python -m pytest
python -m pytest -W error
```

The v7 regression suite checks:

- deterministic source partition;
- complete capability-requirement coverage;
- complete responsibility coverage;
- dense-source decomposition;
- deterministic source truth;
- deterministic depth and work activities;
- autonomy deferral;
- cross-capability deferral;
- removal of model-produced `source_explicit` material from derived sections.

## Live `tG9K` procedure

Keep accepted P1.6 artifact 29 fixed.

Run:

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v7_snapshot.py
```

Do not rerun English analysis and do not rebuild Blueprint before B3 passes.

Expected current chain:

```text
English projection 33
→ accepted English P1.6 artifact 29
→ new Capability v7/v4 artifact
→ no current Blueprint
```

## Mechanical acceptance

`scripts/audit_capability_v7_snapshot.py` verifies:

- artifact 29 remains the accepted P1.6 anchor;
- Capability is v7/v4 and current-chain;
- Blueprint remains absent from the current chain;
- `source_truth` exactly preserves accepted P1.6 source facts;
- all capability-relevant requirements are linked;
- all responsibilities are linked;
- dense `tG9K` has at least two profiles;
- requirement strength is deterministic;
- linked source-explicit depth is deterministic;
- linked source-explicit work activities are deterministic;
- positive independence is absent;
- derived sections contain no model-produced `source_explicit` items;
- cross-capability synthesis is empty in v7.

## Semantic acceptance

A mechanical pass is necessary but not sufficient.

B3 still fails if the complete live artifact:

- groups unrelated requirements into incoherent capabilities;
- treats contextual/preferred tools as mandatory/mastery;
- turns cloud/edge listings into a required deployment architecture;
- uses evidence that is exact but semantically irrelevant to the derived claim;
- expands into a generic curriculum;
- produces weak or technically incorrect prerequisites;
- is not materially more useful than accepted P1.6.

If v7 passes mechanically but E2B remains semantically weak, the next controlled experiment is a
model comparison with source/P1.6/prompt/schema/rubric held fixed. Do not add another large prompt
patch collection first.
