# Blueprint v6 / 12B review and Phase-1 defer decision

**Date:** 2026-08-12  
**Job:** `tG9K`  
**Decision:** Blueprint B4 is **not accepted** for Phase-1 use. Further Blueprint prompt/model iteration is deferred from the Phase-1 critical path.

## Fixed evidence chain

The controlled comparison held the upstream chain and Blueprint contract fixed:

```text
English projection artifact 33
→ English P1.6 artifact 29
→ Capability v7/v4 artifact 9
→ Blueprint v6/v5
```

Only the Blueprint model changed from `gemma-4-e4b-it-ud` to `gemma-4-12b-it-qat`.

The selected 12B candidate is Blueprint artifact **7**, published in Review Snapshot commit:

```text
671bd6e3c43555c631958531671a0f1be9726554
```

The v6 mechanical audit passed:

```text
Capability areas:                       2
Deterministic source requirements:     25
Deterministic source responsibilities:  7
Professional considerations:            4
Important unknowns:                     4
Role-level constraints:                 2
Role-purpose items:                     1
```

CI on the committed candidate also passed.

## What improved with 12B

The stronger model was materially better than the E4B v6 attempt:

- it satisfied the v6/v5 structured contract without Instructor repair failure;
- it avoided the rejected v5 free-form `practical_interpretation` surface;
- it did not claim end-to-end infrastructure/lifecycle ownership;
- it did not assemble the full technology list into one runtime architecture;
- it preserved JobHunter-owned source requirements, responsibilities, strengths, depths, evidence, role purpose, and role-level constraints;
- several generated considerations were useful and well grounded.

Examples of useful bounded interpretation included:

- high-dimensional semiconductor metrology + PCA/PLS as a plausible dimensionality-reduction concern;
- the role bridging domain engineering and data science through technical-team problem scoping.

## Why B4 still fails

Mechanical correctness is not semantic acceptance.

The accepted v6 rubric explicitly rejects unknowns or considerations that smuggle in unstated systems, feedback loops, platforms, or implementation obligations.

The 12B candidate still contained examples of this:

1. `Whether any automated feedback loops for APC/SPC are currently operational...`
   - accepted source states APC/SPC/process-control work;
   - it does **not** establish an automated feedback loop;
   - phrasing it as the unknown still narrows the world to an unstated architecture.

2. `Which specific cloud provider (AWS, GCP, Azure) or on-premise infrastructure is currently utilized for model hosting.`
   - cloud names are contextual and edge deployment is preferred;
   - the vacancy does not establish that one of those providers or an on-prem hosting pattern is currently used;
   - the unknown therefore presumes a platform choice that may not exist.

3. `...translating raw sensor physics into actionable process control metrics.`
   - signal processing, sensor/metrology data, industrial statistics, and process control are source supported;
   - `raw sensor physics` is additional domain interpretation not stated by the vacancy.

4. `...strict versioning of both data lineage and model weights to meet quality standards.`
   - traceability, reproducibility, governance, models, and data are source supported;
   - strict versioning of both objects and unspecified quality standards are specific implementation expectations, not accepted source facts.

These are milder than earlier Blueprint failures, but they violate the explicit B4 semantic boundary.

## Experiment history and conclusion

The Blueprint investigation has now covered materially different failure modes and model capacities:

```text
v3/v2 + E2B/E4B
→ provenance namespace confusion + semantic architecture overreach

v4/v3 + E4B
→ deterministic provenance fixed; broad generated prose still overreached

v5/v4 + E4B
→ Capability-derived prose removed; free-form interpretation still inflated role scope

v6/v5 + E4B
→ very narrow contract; failed structured repair and still invented assumptions

v6/v5 + 12B
→ structurally successful and materially better; still violates explicit unknown/inference boundary
```

The observed pattern is now sufficient to stop model shopping and prompt contraction for Phase 1.

Further contraction would leave little or no professional interpretation beyond P1.6 + Capability, while further prompt-specific rules would create the brittle patch collection the project has deliberately avoided.

## Phase-1 disposition

Blueprint is **not deleted** and the v6/v5 code is not declared useless.

Instead:

- v6/v5 + 12B artifact 7 becomes the best bounded experimental Blueprint evidence so far;
- Blueprint remains inspectable as an experimental downstream layer;
- Blueprint is **not** an accepted source for Phase-1 decisions, Market aggregation, personal readiness, or later automatic recommendations;
- no v7 Blueprint contract or additional local-model shopping is authorized during Phase 1;
- Phase-1 semantic acceptance proceeds with the layers that have actually passed bounded acceptance: P1.6 and Capability v7;
- heterogeneous CI-3 review should validate source → English → P1.6 → Capability across materially different roles;
- Blueprint may be observed during that review only as non-gating research evidence.

## Revisit criteria

Reopen Blueprint design only when at least one concrete change materially alters the problem, for example:

- heterogeneous role evidence reveals a precise user-value requirement that P1.6 + Capability cannot satisfy;
- a stronger or materially different inference approach is available and justified;
- deterministic/retrieval-backed professional knowledge can bound inference more reliably;
- a reviewed human-in-the-loop representation can separate source facts, professional examples, and employer-specific claims more safely;
- later Phase-2 domain/canonical structures provide stronger grounding than a single-job prompt can provide.

Do not reopen Blueprint merely to try another prompt version, another small validator patch, or another nearby local model.

## Next gate

Proceed to heterogeneous semantic validation of the accepted stack:

```text
source
→ English projection
→ P1.6 factual extraction
→ Capability v7
```

Use materially different roles, including the sparse `t4jp` anchor and Python/software, network/security, and operations/platform roles where available. Convert repeatable deterministic defects into tests and keep model limitations separate from deterministic failures.
