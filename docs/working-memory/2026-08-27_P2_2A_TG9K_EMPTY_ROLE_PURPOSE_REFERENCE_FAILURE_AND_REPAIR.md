# P2.2A `tG9K` Empty Role-Purpose Reference Failure and Repair

**Date:** 2026-08-27  
**Phase:** P2.2A Job Work Intelligence v1  
**Status:** INTEGRITY DEFECT REPAIRED / REAL-LOCAL `tG9K` RERUN NEXT  
**Branch:** `main`  
**Current semantic contract:** `job-work-intelligence-v1` / prompt `job-work-intelligence-v1.1`

## 1. Trigger

After `t4qV` and `tmyX` produced useful P2.2A candidate anchors, the user ran the first real `tG9K` generation:

```bash
python -m jobhunter.work_intelligence_cli generate tG9K
```

The run failed before artifact persistence with:

```text
error: Work Intelligence references missing role-purpose indices: [1]
```

## 2. Accepted source boundary

Accepted/current `tG9K` English P1.6 artifact `36` contains:

```text
responsibilities: 8
role_purpose:      0
```

The eight responsibilities cover ML/AI model building and validation, yield/process-control work, high-dimensional industrial data, robust pipelines, problem framing with technical teams, model validation/monitoring, moving models toward production with engineering, and model/data traceability/reproducibility/governance.

The accepted P1.6 `role_purpose` array is explicitly empty.

Therefore any generated `role_purpose_indices` value is structurally impossible. There is no role-purpose item that index `1` could refer to.

## 3. Why the existing validator was still correct

P2.2A already validates every structured source reference after model generation. It correctly rejected the impossible reference and persisted no candidate artifact.

The defect was not that the validator was too strict. The missing behavior was a narrow deterministic normalization for references into a source section that contains zero possible targets.

## 4. Repair decision

The repair deliberately does **not** change prompt identity, schema identity, or semantic interpretation rules.

New rule inside deterministic reference validation:

```text
source section count == 0
AND model emits references into that section
→ remove those impossible references
```

This applies to structurally absent responsibility, role-purpose, and supporting-requirement sections where relevant.

Important safety boundary:

```text
section contains one or more real items
→ never clamp, guess, remap, or silently remove an out-of-range reference
→ ordinary bounds validation still fails
```

After empty-section cleanup, every work theme and deliverable must still retain valid direct work support. If normalization would leave a theme/deliverable with no accepted responsibility or role-purpose reference, generation still fails.

This is deterministic cleanup of an impossible pointer, not semantic repair.

## 5. Implementation and regression

Implementation commit:

```text
b6e3e49daf03657664ac292f3619ee37c150deb0
fix: normalize impossible P2.2A empty-section references
```

Regression/style head:

```text
76ecc689db0b112df8e0d0be8198a5927a09c8f9
style: wrap P2.2A empty-section regression
```

New regression file:

```text
tests/test_work_intelligence_empty_section_reference_normalization.py
```

Coverage proves:

1. a spurious role-purpose reference is removed when the accepted role-purpose section is empty and valid responsibility support remains;
2. cleanup cannot rescue a theme that would otherwise have no valid direct work support;
3. an out-of-range role-purpose reference remains a hard failure when the role-purpose section is non-empty.

## 6. Repository quality evidence

GitHub Actions run `33101421127` on final head `76ecc689db0b112df8e0d0be8198a5927a09c8f9` completed successfully:

```text
Ruff                       PASS
full pytest                PASS
pytest -W error            PASS
overall quality job        PASS
```

No local repository test rerun is required from the user.

## 7. Version/currentness consequence

This repair does not change:

```text
contract:       job-work-intelligence-v1
prompt version: job-work-intelligence-v1.1
schema:         job-work-intelligence-v1
```

Reason: the semantic/generation contract is unchanged. The code now deterministically normalizes an impossible structured pointer that could never denote source evidence.

Existing valid `t4qV` artifact 2 and `tmyX` artifact 3 therefore remain under the same current prompt/schema identity and do not need regeneration solely because of this repair.

## 8. Current P2.2A state

```text
t4qV artifact 2   accepted candidate product anchor
tmyX artifact 3   accepted candidate product anchor with recorded limitation
tG9K              first run failed on impossible empty-section reference
repair             implemented + CI green
tG9K rerun         NEXT
tmBK               pending limited-work boundary
artifact reuse     pending
browser UX         pending
P2.2A overall      OPEN
P2.2B              NOT AUTHORIZED
```

## 9. Exact next action

On the user's real local environment:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Review the resulting candidate for:

- useful grouping of the eight accepted responsibilities;
- no unsupported lifecycle/ownership inflation;
- no fabricated role-purpose claims;
- whether all themes again become `primary` (third cross-domain observation for emphasis usefulness);
- deliverables/role interpretation only when genuinely useful and supported;
- overall reduction in manual reading/synthesis effort.

Do not start `tmBK` or P2.2B until the repaired `tG9K` result is understood.
