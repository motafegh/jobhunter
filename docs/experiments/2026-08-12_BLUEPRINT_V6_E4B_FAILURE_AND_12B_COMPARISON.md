# Blueprint v6 E4B failure and controlled 12B comparison

**Date:** 2026-08-12  
**Gate:** B4 / SQ-3  
**Status:** E4B run rejected; controlled stronger-model comparison active

## Fixed upstream chain

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7/v4 artifact 9
Blueprint contract role-capability-blueprint-v6 / role-capability-blueprint-v5
```

## E4B result

Blueprint model:

```text
gemma-4-e4b-it-ud
```

The v6 request failed after one bounded Instructor repair. The validator correctly rejected the second professional consideration in Capability area 1 because the generated statement used obligation language (`must`).

The retry did not repair the semantic boundary. It changed the wording but retained the same prescriptive structure.

The rejected generations also exposed a deeper semantic concern in model-created unknowns. Examples included questions that introduced unstated implementation details such as a feature store and an entire raw-sensor ingestion pipeline. Those are not established by accepted P1.6 and therefore cannot be accepted merely because they are phrased as questions.

Decision:

- do not weaken the v6 validator;
- do not add a semiconductor-specific phrase blacklist;
- keep v6/v5 unchanged for the next comparison;
- compare a stronger local Blueprint model before another contract redesign.

## Controlled stronger-model comparison

Change only the Blueprint model:

```text
analysis:   gemma-4-e4b-it-ud          (frozen)
capability: gemma-4-e2b-it             (frozen)
blueprint:  gemma-4-12b-it-qat         (comparison variable)
```

The tracked `jobhunter.toml` now selects `gemma-4-12b-it-qat` for Blueprint only.

The Blueprint runtime context was right-sized from 16,384 to 8,192 tokens. The failed v6 E4B request had a roughly 2.2k-token initial prompt and bounded 4,096-token Blueprint output budget, so the previous 16k allocation was unnecessary for this contract.

Blueprint runtime now requests exclusive LLM residency before generation: other loaded LLM instances are unloaded while embedding models remain loaded. This is runtime/resource management only; it does not change source evidence, P1.6, Capability, Blueprint prompt/schema, or the B4 semantic rubric.

## Acceptance rule

A structurally valid 12B result still does not pass B4 automatically.

Review must reject:

- source-unsupported employer obligations;
- end-to-end/full-scope ownership;
- technology-list-to-architecture synthesis;
- invented feature stores, pipelines, interfaces, deployment topology, or operating modes;
- real-time/low-latency/feedback-loop assumptions;
- unknowns that smuggle unstated system facts into the question itself;
- optionality/depth promotion.

If the 12B model still fails the same bounded v6 contract, treat that as evidence against further model shopping and reassess whether the remaining generative Blueprint surface is worth retaining at this Phase-1 gate.
