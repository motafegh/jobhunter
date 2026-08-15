# Capability v9 Public Promotion

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** promotion implementation complete; deterministic CI PASS; local operational verification pending

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

## 6. Current status

```text
Capability v9 public routing code:    IMPLEMENTED
Deterministic CI:                     PASS
Dense accepted artifact:              11
Sparse accepted artifact:             12
Historical v7/v8:                     PRESERVED
Blueprint:                            DEFERRED / PINNED TO V7
Local operational verification:       PENDING
```

Do not call the promotion operationally closed until normal local commands prove that the promoted public path reuses artifacts 11 and 12 and Review Snapshot reports v9/v5 as current.

## 7. Required local operational verification

Run from the project repository after pulling `main`:

```bash
jobhunter jobs capability tG9K
jobhunter jobs capability t4jp

jobhunter jobs snapshot tG9K
jobhunter jobs snapshot t4jp
```

Expected Capability behavior:

```text
tG9K → reuse Capability artifact 11 → v9/v5 → P1.6 artifact 36
t4jp → reuse Capability artifact 12 → v9/v5 → P1.6 artifact 37
```

No new model generation should be necessary for those accepted current dependencies.

Expected Review Snapshot behavior:

- Capability contract is `job-capability-intelligence-v9 / job-capability-intelligence-v5`;
- Capability is current for the current source/P1.6 dependency chain;
- dense and sparse snapshots select artifacts 11 and 12 respectively;
- historical v7/v8 artifacts remain historical/non-current;
- Blueprint remains deferred and is not silently rebuilt/rebased on v9.

Only after this local proof should the public Capability v9 promotion be marked operationally complete.
