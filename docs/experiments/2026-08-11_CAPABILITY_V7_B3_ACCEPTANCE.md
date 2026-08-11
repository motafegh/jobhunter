# Capability v7 B3 Acceptance Decision

**Status:** B3 accepted for the bounded `tG9K` semantic gate; v7/v4 frozen pending heterogeneous review  
**Date:** 2026-08-11  
**Accepted upstream anchor:** English P1.6 artifact 29  
**Accepted Capability artifact:** 9  
**Runtime/schema:** `job-capability-intelligence-v7` / `job-capability-intelligence-v4`

## Decision

Capability v7 passes B3 on the rich `tG9K` acceptance case. This acceptance is sufficient to proceed to B4 Role Capability Blueprint calibration. It is not a claim that Capability is already validated across every role family; that broader claim remains gated by CI-3/B5 heterogeneous live review.

## Why v6 failed

The v6 model/system boundary still allowed the model to decide which accepted P1.6 facts survived into Capability. The live v6 artifact linked only 3/27 requirements and 2/7 responsibilities, omitted four explicit depth facts, repeated unsupported autonomy/end-to-end ownership, strengthened contextual tools, leaked evidence across areas, and collapsed the role into one broad profile.

## Why v7 passes

v7 moved mechanically provable source truth out of model discretion. The live artifact and repository audit establish:

```text
English P1.6 artifact:             29
Capability artifact:                9
Capability requirements linked: 25/25
Responsibilities linked:           7/7
Capability profiles:                 2
Explicit P1.6 depth facts:           6
Role-level requirements:       [25, 26]
```

The two capability profiles are coherently separated into industrial ML/statistical modeling and ML engineering/MLOps work. Positive autonomy inference is absent, cross-capability synthesis is empty, and all source responsibilities are deterministically represented.

## Explicit-depth clarification

The CLI reports five of six explicit depth facts represented inside capability profiles. This is correct, not an omission.

Capability-level explicit depths are:

```text
0   Statistics/signal processing       Solid
2   Python                              expert
22  industrial/manufacturing AI/ML     Strong
23  process-control/manufacturing work Hands-on
24  high-dimensional sensor data       Comfort
```

The sixth depth-bearing requirement is deliberately role-level:

```text
26  Professional experience            three to six years
```

Requirement 26 therefore belongs in `source_truth.role_level_requirement_indices`, not in a capability profile. All six accepted depth facts survive in v7 source truth.

## Known bounded observations

The model can still produce debatable derived wording, for example describing source-named industrial systems as implied knowledge or using broad labels such as “Full-Stack ML Engineering & MLOps.” These are not source-truth losses and did not justify another Capability contract revision. Downstream Blueprint must not amplify such prose into employer facts, ownership claims, mandatory architecture, or stronger tool depth.

## Freeze rule

Do not revise Capability v7 merely to polish prose. Reopen the contract only if B4 or heterogeneous CI-3 evidence demonstrates a repeatable correctness problem that cannot be handled at the appropriate downstream layer.

## Next gate

Proceed to B4 Role Capability Blueprint calibration while holding fixed:

```text
source job/version
English projection artifact 33
accepted P1.6 artifact 29
accepted Capability artifact 9
analysis model:   gemma-4-e4b-it-ud
Capability model: gemma-4-e2b-it
Blueprint model:  gemma-4-e2b-it
```

B4 must preserve upstream optionality/depth and distinguish source-stated work from practitioner-created examples. A technology list remains evidence of technologies, not an employer architecture specification.
