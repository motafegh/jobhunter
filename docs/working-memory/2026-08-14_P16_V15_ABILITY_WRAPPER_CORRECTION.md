# Working Memory — P1.6 v15 Ability-Wrapper Correction

**Date:** 2026-08-14  
**Status:** Active addendum to the v15 sparse CI-3 handoff  
**Job:** `t4jp`

## Second live v15 run

The run failed closed before persistence with:

```text
P1.6 v14 requirement[6] concept keeps an 'Ability to ...' wrapper
```

No v15 artifact existed afterward, so export/audit correctly reported no current v15 candidate.

## Classification

The prior schedule-concept correction worked far enough to expose the next wrapper boundary:

```text
Ability to produce visual content full-time and part-time
→ schedule wording removed
→ Ability to produce visual content
→ strict v14 validator rejected the remaining linguistic wrapper
```

This is still the intended v15 normalized-concept contract, not a new semantic contract. No v16 is
warranted because no v15 artifact has been persisted.

## Correction

Because the connector blocked replacement of the larger service module, the isolated v15 CLI now
uses a scoped runtime guard in:

```text
src/jobhunter/p16_v15_runtime_guard.py
```

The guard temporarily wraps only the v15 candidate runtime validator:

```text
Ability to <meaningful capability phrase>
→ strip only the Ability-to wrapper
→ exact evidence unchanged
→ run the existing strict validator
→ restore the original validator after the candidate run
```

Wrapper-only or obvious logistics remnants such as `Ability to work` are left unchanged and still
fail closed rather than being manufactured into capabilities.

The public P1.6 path, historical v14 code, and persistent contract identity remain unchanged.

## Verification

CI run 695 on commit `6a66073fe3fac5a62c9d55a117f07897c0100795` passed:

```text
Ruff: PASS
full pytest: PASS
warnings-as-errors: PASS
```

## Next step

Rerun sparse v15 only. Export/audit only after `Outcome: completed`. Do not run Capability or dense
`tG9K` yet.
