# Market I7 — persisted v21 runtime failure

**Date:** 2026-09-22  
**Status:** EXECUTED / HOLD  
**Current English contract:** `job-analysis-english-v21 / job-analysis-v5`  
**Selected core case:** `tvMm`

## Purpose

Record the first normal persisted current-contract execution after v21 promotion. This is operational acceptance evidence, not a new prompt/model experiment.

## Preconditions and safety

The owner fast-forwarded local `main` to the promoted v21 head and used the tracked `jobhunter.toml` configuration. The initially documented `config/local.toml` path did not exist, so that failed invocation stopped before any database/model mutation. The corrected run first created a local SQLite backup at `data/local-acceptance/i7/pre-v21-persist.sqlite3`.

Pre-run checks:

```text
integrity= ok
foreign_keys= []
```

The backup and operational database are local/private evidence and must not be published.

## Execution

The owner ran:

```bash
jobhunter --config jobhunter.toml jobs analyze tvMm
jobhunter --config jobhunter.toml jobs review-analysis tvMm status
```

The analysis path used the current v21 contract and the configured analysis model. The provider exhausted the one bounded validation retry, producing two generations total.

### Generation 1

Three validation failures were reported:

1. `practical experience` was incorrectly placed in `depth_signal` for the LLM/API experience item;
2. `experience` was incorrectly placed in `depth_signal` for the Agent/Agentic Workflow item;
3. `turn an Agent into a reliable system in a real product` was labeled `concept_type=experience` even though the exact item states a required capability and contains no prior applied-exposure evidence.

### Generation 2 / correction

The correction generation fixed both depth-signal errors by setting those fields to null. It repeated the third semantic error unchanged: the required reliable-product capability was again typed as `experience`.

The v21 prior-exposure validator rejected the candidate with:

```text
concept_type=experience requires prior applied exposure in the exact item
```

This is the intended fail-closed authority boundary. A statement that a candidate must be able to turn an Agent into a reliable production system does not, by itself, state that the candidate has previously done so.

## Result

- no valid v21 candidate was persisted;
- no semantic review acceptance/rejection decision was possible;
- `jobs review-analysis tvMm status` reported no current English P1.6 artifact matching the configured review contract;
- public corpus synchronization remained at 394 jobs, 27 English projections, 5 accepted English P1.6 artifacts, and 5 Capability artifacts;
- no Market snapshot/profile closure occurred;
- I7 remains **HOLD**.

## Diagnosis

The evidence does **not** show a validator defect. The validator preserved the semantic distinction introduced by the prior-exposure guard. It also does not show that the Instructor correction path is wholly broken: the second generation corrected the two depth errors. The remaining failure is model adherence to the concept-type boundary during correction.

This run therefore narrows the unresolved question to model/contract correction adequacy on a live persisted path. It is not justification to weaken validation, auto-correct an unsupported historical-experience claim, retry until stochastic PASS, or select a different vacancy merely to close I7.

## Versioning boundary

Current architecture requires prompt/runtime changes to create distinct current/historical identities. Therefore do **not** patch additional semantic correction wording into `job-analysis-english-v21` in place merely to make this case pass.

A future repair that changes prompt/runtime semantics must be evaluated as a new versioned candidate contract. A deterministic normalization is acceptable only if semantic equivalence/type can be proved from source grammar generally; absence of experience evidence alone is not enough to infer whether the correct ontology is skill, practice, knowledge, domain, or another type.

## Next bounded decision

Before another live generation:

1. preserve this run as independent real persistent-runtime evidence;
2. determine whether fail-closed rejection is acceptable operational behavior for v21 or whether repeated model non-adherence materially harms the product workflow;
3. if a contract change is justified, design it under a new prompt/runtime identity and prove it across representative positive/negative cases plus the 27-projection regression before any live retry;
4. do not change source, evidence boundary, prompt contract, model, and vacancy simultaneously;
5. keep I7 HOLD until a genuinely valid accepted-current core artifact reaches snapshot/profile and browser/CLI semantic drill-down.
