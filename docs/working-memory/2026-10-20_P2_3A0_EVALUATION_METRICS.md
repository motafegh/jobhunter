# P2.3A-0 Evaluation Measurement Layer — 2026-10-20

**Status:** EXPERIMENTAL MEASUREMENT SUPPORT / NON-AUTHORITATIVE  
**Current product gate:** P2.2B-B2 remains open pending maintainer-local R3-R6 Registry application and verification.  
**P2.3 authority:** NOT AUTHORIZED.

## Purpose

The merged P2.3A-0 experiment can construct:

- Strategy A — deterministic accepted/current P1.6 + reviewed Registry composition;
- Strategy B — Strategy A plus an explicit accepted/current public Capability-v9 job-local organization where available.

The experiment previously emitted raw composition structure and basic counts. This increment adds deterministic measurements needed to inspect the A/B evidence without turning the measurement code into an architecture selector.

The evaluator does not decide that Strategy A or Strategy B is sufficient. Human/semantic usefulness review remains necessary for questions such as whether the output is understandable, appropriately scoped, or materially reduces user effort.

## Strategy-A measurements

For each job the evaluator records:

```text
exact claim count
requirement claim count
responsibility claim count
mapped claim count
mapped requirement count
mapped responsibility count
bucket count
canonical bucket count
source-local bucket count
deterministic grouping savings
overall canonical mapping coverage
requirement mapping coverage
responsibility mapping coverage
bucket-per-claim ratio
exact-claim recoverability
```

Requirement and responsibility mapping coverage are intentionally separate. B2 currently reviews responsibility correspondence; sparse requirement canonicalization must not be hidden by a single aggregate ratio.

## Strategy-B measurements

Where an accepted/current public Capability-v9 artifact is available, the evaluator records:

```text
base claim / requirement / responsibility counts
grouped distinct claim / requirement / responsibility counts
ungrouped claim count
group count
reviewed canonical concept count
overall grouped-claim coverage
grouped requirement coverage
grouped responsibility coverage
group-per-grouped-claim ratio
semantic grouping savings
requirement-only group count
responsibility-backed group count
exposed work-activity count
suppressed work-activity count
duplicate cross-group membership count
exact partition integrity
work-activity boundary integrity
```

`exact_partition_ok` is false if a claim appears in more than one Strategy-B group, if grouped and ungrouped sets overlap, or if their union does not exactly recover the Strategy-A claim set.

`work_activity_boundary_ok` verifies that requirement-only groups expose no work activities. This complements the 2026-10-20 requirement-only work-activity guard.

## Unknown / unevaluated semantics

Aggregate boolean checks use `null` when the relevant evidence set does not exist.

For example, when none of the selected jobs has an eligible Strategy-B artifact:

```text
all_exact_partitions_ok = null
all_work_activity_boundaries_ok = null
```

They must not become `true` through empty-set/vacuous truth. Missing evidence is not a passing result.

Ratios with a zero denominator similarly remain `null` rather than being coerced to zero or one.

## Authority boundary

The exported summary states:

```text
decision_authority = none_mechanical_measurements_only
```

This increment does not:

- choose Strategy A, B, or C;
- establish semantic usefulness;
- mutate the Canonical Registry;
- add a model call;
- persist a P2.3 profile;
- canonicalize requirements in bulk;
- authorize or close P2.3;
- substitute for the maintainer-local B2 proof;
- close P2.2B-B2.

## Next evidence use

After B2 is actually proven and formally closed, these measurements can be run on the heterogeneous P2.3A-0 evidence set and combined with direct output review to decide whether:

1. Strategy A is already sufficiently useful;
2. optional Strategy B materially improves usability while preserving authority boundaries; or
3. the conditional Strategy-C grouping experiment is justified.

No one numeric threshold is defined here because the architecture decision includes semantic usefulness, precision, unknown preservation, and user effort rather than a single optimization score.
