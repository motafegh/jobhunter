# P2.3A-0 Requirement-Only Work-Activity Guard — 2026-10-20

**Status:** REPOSITORY REPAIR / P2.3A-0 REMAINS EXPERIMENTAL / B2 REMAINS OPEN  
**Scope:** Strategy-B composition only.  
**Authority change:** None.

## Finding

The merged P2.3A-0 Strategy-B overlay correctly required exact accepted/current P1.6 claim links before reusing an accepted public Capability-v9 group, but it copied the group's `work_activities` verbatim even when the group linked only requirement claims.

That was too permissive for the recorded P2.3A-0 acceptance boundary. The technical feasibility audit requires requirement-only cases to preserve qualification/depth evidence without fabricating work activity when P1.6 contains no responsibility evidence.

Capability-v9 work activities are optional derived interpretation. They therefore cannot become work evidence in this experiment merely because the accepted Capability artifact contains them.

## Repair

Strategy B now exposes Capability-v9 `work_activities` only when the same group links at least one exact accepted/current P1.6 responsibility.

For a requirement-only group:

```text
accepted Capability-v9 grouping and qualification/depth context  retained
exact P1.6 requirement links                                     retained
reviewed Registry identity from exact mapped claims              retained
Capability-v9 work_activities                                    suppressed
suppressed count                                                  exported
```

For a group with an exact linked P1.6 responsibility, accepted Capability-v9 work activities remain available as job-local interpretation.

The repair deliberately does **not**:

- create a responsibility from a requirement;
- treat Capability-v9 labels as canonical identity;
- mutate Registry state;
- add a model call;
- persist a P2.3 profile;
- authorize P2.3;
- close P2.2B-B2.

## Implementation

Changed:

- `src/jobhunter/p2_3a0_profile_experiment.py`
  - records `suppressed_work_activity_count` per Strategy-B group and composition;
  - suppresses work activities when the group has no exact P1.6 responsibility link.
- `scripts/experiment_p2_3a0_strategy_a.py`
  - exports the suppression count at composition and group level.
- `tests/test_p2_3a0_requirement_only_boundary.py`
  - proves requirement-only groups suppress derived work activity;
  - proves groups with an exact responsibility preserve it.

## Current gate

This is a repository-side correctness repair to the already-merged non-authoritative experiment. It does not substitute for the current B2 maintainer-SQLite gate.

Current authority remains:

```text
P2.2B-B2 R3-R6 local Registry application + verification   PENDING
P2.3A-0 composition experiment                             NON-AUTHORITATIVE
P2.3 production authority                                  NOT AUTHORIZED
```

After repository verification, continue to preserve this distinction until the machine-local B2 proof exists and B2 is formally closed.
