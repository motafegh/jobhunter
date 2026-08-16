# Capability v9 Public Promotion

**Date:** 2026-08-15  
**Operational closure verified:** 2026-08-16  
**Branch:** `main`  
**Status:** PUBLIC PROMOTION CLOSED / OPERATIONALLY VERIFIED

## 1. Promotion basis

Capability v9 completed opposite-end bounded acceptance before any public routing change:

```text
dense tG9K
English P1.6 artifact 36
→ Capability v9 artifact 11
→ ACCEPTED

sparse t4jp
English P1.6 artifact 37
→ Capability v9 artifact 12
→ ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

The accepted contract is:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

No new Capability generation was authorized as part of promotion. The accepted artifacts 11 and 12 are the operational reuse anchors.

## 2. Public routing change

The neutral/current Capability facade `src/jobhunter/capability_service.py` now exports and builds Capability v9/v5.

Because current consumers already import the neutral facade, this aligns the normal public path across:

```text
CLI
browser Capability view
Review Snapshot current-chain selection
other current Capability consumers
```

Historical versioned modules remain available for reproducibility:

```text
capability_service_v7.py
capability_service_v8.py
capability_service_v9.py
```

Historical artifacts are not rewritten or deleted.

## 3. Deferred Blueprint isolation

Blueprint v6 remains deferred/non-authoritative and was not promoted with Capability.

To prevent an accidental dependency migration, `role_blueprint_service_v6.py` is explicitly pinned to historical Capability v7 contract constants rather than the neutral/current Capability facade.

The final Blueprint diff against the pre-promotion file is intentionally surgical: one import changes from the neutral facade to `capability_service_v7`. No Blueprint inference, schema, persistence, prompt, or routing logic was changed.

## 4. Promotion compatibility

The neutral Capability facade preserves the established model-inspection surface used by routing/tests:

```text
_analysis_model
_capability_model
_provider
_current_dependencies(...)
```

The current Capability service tests were migrated from the obsolete one-shot v7 fake-provider shape to a deterministic staged v9 provider. The tests still prove the same product invariants:

- exact current accepted English P1.6 dependency selection;
- exact translation dependency even when alternate projections exist;
- deterministic requirement strength and source-explicit depth;
- complete source truth before persistence;
- persistence/reuse under the current v9/v5 contract;
- fail-closed behavior on invalid staged output.

This is a test-fixture migration to the promoted architecture, not a weakening of acceptance rules.

## 5. Deterministic promotion gate

CI run 872 initially exposed four compatibility failures after the facade switch:

- three old public-service tests still injected a one-shot v7 fake provider into the staged v9 service;
- one model-routing test expected the neutral facade to expose its configured model/provider identities directly.

Those were corrected by migrating the obsolete fixture and preserving the neutral facade inspection proxies.

Final promotion gate:

```text
CI run 874
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Promotion tests additionally lock:

- current Capability prompt = `job-capability-intelligence-v9`;
- current Capability schema = `job-capability-intelligence-v5`;
- current service is the v9 service boundary;
- current formatter is the v9 formatter;
- deferred Blueprint v6 remains pinned to v7 rather than following current Capability.

## 6. Operational verification — PASS

Normal public commands were run after pulling current `main`:

```bash
jobhunter jobs capability tG9K
jobhunter jobs capability t4jp

jobhunter jobs snapshot tG9K
jobhunter jobs snapshot t4jp
```

Observed Capability results:

```text
tG9K
Outcome: reused
Contract: job-capability-intelligence-v9 / job-capability-intelligence-v5
English analysis artifact: 36
31/31 capability requirements
8/8 responsibilities
5/5 capability explicit depth
6/6 all explicit depth
role-level indices [31, 32]

 t4jp
Outcome: reused
Contract: job-capability-intelligence-v9 / job-capability-intelligence-v5
English analysis artifact: 37
8/8 capability requirements
0/0 responsibilities
0/0 explicit depth
role-level indices []
```

No fresh Capability generation occurred for either accepted dependency chain.

Review Snapshot files were then inspected directly. Observed current-chain evidence:

```text
tG9K current=True artifact=11 analysis=36
contract=job-capability-intelligence-v9 / job-capability-intelligence-v5
blueprint_current=False

t4jp current=True artifact=12 analysis=37
contract=job-capability-intelligence-v9 / job-capability-intelligence-v5
blueprint_current=False
```

This proves:

- artifact 11 is the current Capability artifact for `tG9K` on P1.6 artifact 36;
- artifact 12 is the current Capability artifact for `t4jp` on P1.6 artifact 37;
- the public contract is v9/v5 through normal routing;
- accepted artifacts are reused instead of regenerated;
- Blueprint remains non-current and was not silently rebased on v9.

## 7. Final promotion disposition

```text
Capability v9 public routing code:    PROMOTED
Deterministic CI:                     PASS
Dense accepted artifact:              11 / CURRENT
Sparse accepted artifact:             12 / CURRENT
Normal CLI routing:                   VERIFIED
Review Snapshot current-chain:        VERIFIED
Fresh generation on accepted chain:   NONE
Historical v7/v8:                     PRESERVED
Blueprint:                            DEFERRED / PINNED TO V7 / NON-CURRENT
Operational promotion:                CLOSED
```

Capability v9 is now the accepted public/current Capability contract for Phase-1 use.

The next semantic gate is heterogeneous live validation on materially different Python/software, network/security, and operations/platform/DevOps jobs. Do not reopen v9 calibration based only on harmless non-authoritative wording variation; reopen only for a repeatable correctness defect, provenance defect, source-strength/depth corruption, fabricated authoritative content, or another contract-level failure.
