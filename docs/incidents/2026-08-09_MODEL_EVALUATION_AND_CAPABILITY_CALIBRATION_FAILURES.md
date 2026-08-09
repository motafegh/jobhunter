# Model Evaluation and Capability Calibration Failure Record

**Status:** Closed as a negative evaluation; later remediation required
**Date:** 2026-08-09
**Acceptance job:** Jobinja `tG9K`
**Accepted upstream artifact:** English P1.6 artifact 29
**Current production decision:** local `gemma-4-e4b-it-ud` remains the P1.6 analysis model; Capability remains `job-capability-intelligence-v4` / schema v2

## 1. Why this record exists

This record preserves the local and hosted model experiments performed while closing P1.6 SQ-1 and beginning Capability SQ-2. It distinguishes:

- transport and provider failures;
- completion/reasoning budget failures;
- strict JSON/schema success;
- JobHunter semantic-validation failure;
- reviewed semantic overreach;
- accepted production decisions.

No candidate is accepted merely because it is fast, returns JSON, or sounds technically sophisticated.

## 2. Fixed P1.6 comparison contract

The meaningful hosted comparisons kept these inputs fixed:

```text
source job:                tG9K
source detail version:     40
English projection:        artifact 33 / english-projection-v2
P1.6 prompt/runtime:       job-analysis-english-v9
P1.6 schema:               job-analysis-v4
evidence catalog:          identical leaf references
requirement coverage:      identical 28-item plan
responsibility coverage:   identical 8-item plan
semantic validator:        JobAnalysisResponse with production context
```

Results were evaluation-only unless explicitly identified as a persisted local artifact.

## 3. Accepted local P1.6 baseline

### Gemma 4 E4B

```text
model:                     gemma-4-e4b-it-ud
LM Studio load context:    20,480
artifact:                  29
elapsed:                   76 seconds
finish_reason:             stop
prompt tokens:             4,243
completion tokens:         3,709
reasoning tokens:          697
total tokens:              7,952
role purpose:              1
responsibilities:          7
requirements:              27
requirement coverage:      28/28
responsibility coverage:   8/8
semantic validation:       passed
```

This is the only tested model/configuration that completed and passed the full P1.6 contract.

## 4. Local operational rejections

### Larger Qwen reasoning candidate

- Loaded as a larger local reasoning candidate.
- One run remained too slow after approximately ten minutes and was cancelled.
- No semantic result was accepted.

### Gemma 4 12B QAT

Tested load configurations included:

| Context | KV placement | Approximate GPU allocation | Result |
|---|---|---:|---|
| 32K | GPU/default | 7.62 GB / 8 GB | Too slow |
| 16K | CPU KV | 7.08 GB | Slower |
| 12K | GPU KV | about 7.3 GB | GPU utilization remained about 41%; too slow |

The model was operationally rejected on this 8 GB GPU. Reducing context did not produce a useful full-GPU speedup, and no semantic candidate was accepted.

## 5. OpenCode free-endpoint results

### `nemotron-3-ultra-free`

```text
elapsed:               about 195 seconds
finish_reason:         stop
JSON:                  complete
semantic validation:  failed
```

Observed failures:

- invented unsupported depth signals such as `Discipline around` and `some`;
- retained `Hands-on` inside a supposedly depth-neutral concept;
- placed a context-only modifier into `coverage_exclusions`;
- slower than accepted local E4B.

### `deepseek-v4-flash-free`

Anonymous/free behavior:

- an 8,192-token full request was rejected with `FreeUsageLimitError`;
- two 4,096-token attempts each completed in about 20 seconds but ended with `finish_reason=length` before valid JSON;
- the low-reasoning follow-up was rate-limited before inference.

Authenticated behavior:

- the supplied OpenCode key authenticated, but the full request was still rejected by the same free-model usage limit;
- authentication did not increase the free model's usable quota.

Decision: fast token generation did not produce one complete, valid artifact. No OpenCode provider was added to JobHunter.

## 6. NVIDIA Build results

### Network/proxy finding

- direct `httpx` requests with environment proxies disabled returned HTML `403` responses;
- requests through the configured environment proxy succeeded for short NVIDIA calls;
- long non-streaming calls could be closed by the proxy before a response;
- SSE streaming kept active responses alive once NVIDIA began emitting chunks;
- streaming could not fix provider queue/prefill delays before the first response byte.

This is a transport finding, not evidence that a model passed semantic validation.

### `thinkingmachines/inkling`

Non-think:

- strict probe passed in 0.7 seconds;
- full first attempt completed in about 41 seconds with valid JSON shape;
- three invented/invalid depth signals failed semantic validation;
- the correction attempt repeated the same three errors; total time was about 77 seconds.

Low reasoning:

- one run completed in 32.5 seconds with 1,425 reasoning characters and failed three depth checks;
- the production-style bounded protocol completed its first attempt in 39.8 seconds;
- correction reduced three depth errors to two but still failed;
- total bounded latency was 72 seconds.

Decision: promising throughput, but no valid P1.6 artifact after the allowed correction.

### `google/gemma-4-31b-it`

- strict probes disconnected through the proxy twice before inference;
- observed waits were approximately 58 and 65 seconds;
- no model output or semantic result was obtained.

Decision: operationally unreliable in the tested NVIDIA route.

### `nvidia/nemotron-3-super-120b-a12b`

- strict reasoning-off probe passed in 2.2 seconds;
- the full request exceeded two minutes without a result and was stopped;
- no semantic candidate was accepted.

### `deepseek-ai/deepseek-v4-flash-0731`

Think High:

- strict reasoning probe passed in 7.8 seconds;
- a non-streaming full request ended in a proxy disconnect after about 288 seconds;
- a streaming full request did not produce a useful response within the bounded operational window and was stopped.

Non-think streaming:

- first full attempt completed in 81.7 seconds with `finish_reason=stop`;
- two invented depth signals failed semantic validation;
- the bounded correction completed at 133.8 seconds total and increased the failure to four invalid depth signals.

Decision: the NVIDIA route removed OpenCode's quota/truncation problem, but was slower than local E4B and still failed semantic validation.

## 7. Security and secret handling

- No API key was written to repository files, source, configuration, snapshots, prompts, or reports.
- OpenCode and NVIDIA credentials were supplied through mode-600 temporary files under `/run/user/1000`.
- Each temporary credential file was securely removed after its evaluation.
- Raw hosted responses were not persisted in the repository or production database.
- Keys pasted into chat should be rotated because chat disclosure is outside JobHunter's intended secret boundary.

## 8. Capability v4 evidence on accepted P1.6

Capability artifact 7 was generated from accepted P1.6 artifact 29:

```text
model:                gemma-4-e2b-it
prompt/runtime:       job-capability-intelligence-v4
schema:               job-capability-intelligence-v2
elapsed:              about 103 seconds
outcome:              completed
```

The new P1.6 substrate improved factual availability, but Capability still overreached:

- all six accepted explicit P1.6 depth signals were omitted from `depth_signals`;
- a contextual framework/library list became `Mastery of core ML/DL frameworks`;
- contextual cloud wording became necessary/explicit deployment knowledge;
- `build robust pipelines` plus MLOps names became end-to-end lifecycle ownership;
- cloud evidence was attached to a data-persistence statement;
- tool proficiency was placed under `work_activities`;
- optional MATLAB/C/C++ wording was converted into an unsupported claim that Python/ML is the primary gatekeeper.

Artifact 7 is structurally valid and dependency-current, but it is not semantically accepted for B3.

## 9. Experimental Capability v5 attempt

An unaccepted local experiment added:

- stronger generic prompt rules for list-vs-depth, obligation, independence, section placement, and evidence relevance;
- deterministic validation requiring every accepted non-null P1.6 `depth_signal` to appear in a source-explicit Capability `depth_signals` item;
- two focused regression tests for explicit-depth coverage.

Focused code evidence before the live run:

```text
Ruff:                  passed
focused tests:         21 passed
```

Live result:

```text
analysis dependency:   artifact 29
model:                 gemma-4-e2b-it
candidate runtime:     job-capability-intelligence-v5
schema:                job-capability-intelligence-v2
outcome:               failed
persisted artifact:    none
failure:               output incomplete due to max_tokens length limit
bounded retries:       one validation retry attempted
```

The experiment was reverted from source/tests after the negative result. Current source remains Capability v4, matching repository authority. The failed v5 attempt remains in the local SQLite attempt ledger as historical operational evidence.

## 10. Current decision

```text
P1.6 analysis model:       gemma-4-e4b-it-ud
P1.6 acceptance:           artifact 29 accepted
Capability current code:   v4 / schema v2
Capability B3 acceptance:  not passed
hosted provider support:   not implemented
Blueprint rebuild:         not authorized by this negative result
```

No tested hosted model displaced local E4B for P1.6. Capability artifact 7 does not justify moving to B4.

## 11. Later remediation route

When B3 resumes:

1. Keep source version, English projection, P1.6 artifact 29, and the review rubric fixed.
2. Treat explicit P1.6 depth propagation as deterministic bookkeeping where possible instead of asking the model to reproduce a large ledger inside already long output.
3. Reduce or partition Capability output before increasing `max_tokens`; inspect `finish_reason` and token usage first.
4. Add generic validators only for mechanically provable relationships. Do not add semiconductor-specific word patches.
5. Separate required work scope from contextual tool availability in both prompt and review rubric.
6. Require independence/ownership claims to cite actual autonomy or authority evidence.
7. Require direct evidence relevance per analytical statement; do not permit cross-area evidence leakage.
8. If hosted comparison resumes, implement an explicit evaluation harness with streaming, response/token diagnostics, provider identity, and no database persistence before considering production provider support.
9. Re-run `tG9K`, review the complete Capability artifact, and accept B3 only before rebuilding Blueprint.

## 12. Non-conclusions

This evaluation does not prove that the rejected model families are universally poor. It proves that the tested provider/model/runtime combinations did not beat the accepted local baseline or pass the current JobHunter contracts under the observed environment.

## 13. Closeout verification

After reverting the unaccepted v5 source/test experiment and regenerating the selected snapshot:

```text
Ruff:                         passed
pytest:                       278 passed
pytest with warnings errors:  278 passed
git diff --check:             passed
repository diff secret scan:  clean
selected snapshot analysis:   artifact 29
selected snapshot capability: artifact 7 (present for negative review)
selected snapshot Blueprint:  absent from the current chain
```

No commit or push was performed as part of this evaluation/closeout.

## 14. Provider references

- OpenCode Zen model/endpoints documentation: <https://opencode.ai/docs/zen>
- NVIDIA NIM OpenAI-compatible API reference: <https://docs.nvidia.com/nim/large-language-models/latest/reference/api-reference.html>
- NVIDIA structured-generation guidance: <https://docs.nvidia.com/nim/large-language-models/1.15.0/structured-generation.html>
- NVIDIA Inkling endpoint/model page: <https://build.nvidia.com/thinkingmachines/inkling?section=deploy>
- NVIDIA DeepSeek V4 Flash endpoint page: <https://build.nvidia.com/deepseek-ai/deepseek-v4-flash/deploy>
- NVIDIA DeepSeek V4 Flash model card: <https://build.nvidia.com/deepseek-ai/deepseek-v4-flash/modelcard>
- NVIDIA Nemotron Super reasoning controls/model card: <https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b/modelcard>
