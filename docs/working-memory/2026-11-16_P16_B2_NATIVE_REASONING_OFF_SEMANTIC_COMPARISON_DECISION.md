# B2 original-context comparison: native reasoning-off repairs runtime, not semantic trust

**Date:** 2026-11-16
**Branch / draft PR:** `feature/p16-b2-source-items-metadata-2026-11-15` / #20
**Parent accepted main:** `5d4a5e0a64e1dc1da64bc9f28848b4357895aa7e`
**Disposition:** Complete bounded local-model diagnostic; **NO semantic promotion**, **B2 full gate remains OPEN**.
**Prior continuation:** `docs/working-memory/2026-11-15_P16_B2_NESTED_ELIGIBILITY_AND_LOCAL_MODEL_PROBE_RESULT.md`.

## 1. Precisely what changed in the runtime experiment

The first original v1 request timed out at 95.02 seconds (one job attempted, three not attempted). A subsequent *unchanged-prompt* warm v1 trial issued four requests through OpenAI-compatible `/v1/chat/completions`. All four returned in ~11 seconds each but returned **no visible answer**, spending about **757 of 760** output tokens on reasoning.

The local LM Studio model listing described `gemma-4-e4b-it-ud` as initially **unloaded**. A separate bounded 8-token readiness request loaded it and returned `OK` in 3.8 seconds. Cold loading contributed to the original uncertainty, but we cannot attribute the entire earlier 95.02-second timeout to loading. After loading, a direct small `/api/v1/chat` request with supported `reasoning: off` succeeded and used zero reasoning tokens.

Two fully versioned, read-only trials followed on the **same exact original frozen B0 database**, with **no cloud fallback**, no new scraped source, no prompt per job, and no persistent product writes:

| Trial | Prompt | Local native inference | Complete seven-array JSON | Total four-case inference time |
| --- | --- | --- | --- | ---: |
| Native v2 | Exact same 7-array prompt as v1 | `/api/v1/chat`; `reasoning: off`, 1400 output tokens | **4/4** | **23.653 s** |
| One corrective v3 | v2 prompt plus short general instruction about duties/qualification, alternatives and unclear strength | Same model, endpoint, token cap and reasoning settings | **4/4** | **24.290 s** |

The runtime problem for these four cases is **solved as response availability**, but semantic correctness is not established by JSON parsing, zero reasoning tokens or faster inference. v2 versus v1 is a transport/reasoning/budget change; v3 versus v2 is one small prompt change. These are not controlled independent model-quality trials.

**Frozen B0 source SHA-256:** `bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe` (unchanged).

## 2. Semantic source checks: exact claim boundaries matter

An assistant with previous case exposure re-examined the outputs against the frozen original Persian descriptions and earlier A1 source interpretation records. These are **12 deliberately selected diagnostic checks** spanning the same four exposed ads, not a blind human audit, not holdout evaluation, not independent model accuracy, and not comprehensive claim coverage.

| Assistant-reviewed diagnostic | v2 | v3 |
| --- | --- | --- |
| Passed | 4 | 6 |
| Partially satisfied | 3 | 2 |
| Failed | 5 | 4 |

The corrective prompt improved two important points: `tMps` explicitly states a Middle **OR** Senior applicant path, and `tNDx` explicitly includes certificate **OR** equivalent knowledge in the alternatives list. It also removed spurious technical implementation-tool choices from `tMps` eligibility alternatives.

**Blocking mistakes remain:**

1. `tNDx` — the original employer says teamwork and accepting a defined management structure **is an advantage**, but both model versions add teamwork to employer **requirements**.
2. `tNDx` — the specialist Kaspersky certifications and experience with government/large-enterprise customers have **unresolved** employer obligation strength on the frozen source; both models upgrade them to **preferred**.
3. `tMjm` — the employer mostly states applicant pentesting abilities. Both versions turn those abilities into **specific assigned tasks** without adequate original duty evidence. v3 introduces an extra derived duty.
4. `tNhZ` — the corrective v3 output adds part-time/full-time and remote work as generic `alternatives` as well as work arrangements, conflating work-mode options with eligibility-alternative structure.
5. `tNhZ` — source duties establish relevant engineering technologies, but work-implied capability arrays are only **partially useful**; rigid review should not erase that relevance or invent paid experience.
6. `tMps` — v3 gives the overall Middle/Senior **OR** path but does not output a complete, independently source-verified machine-readable within-track **AND/OR** eligibility graph. The source-bound deterministic B2 candidate still supplies the only inspectable tentative topology.

We must neither assume that the local LLM's apparent fluency proves employer modality nor assume the deterministic heuristic parser has universally correct semantics. In the exposed samples the two approaches have *different* error risks.

## 3. Evidence and reproducibility

**Private, ignored raw provider records** (never committed):

- Warm v1: `data/local-acceptance/p16-stage-b2-2026-11-16/local-semantic-probe-v1-warm/PRIVATE_MODEL_TRIAL.json`.
- Native v2: `data/local-acceptance/p16-stage-b2-2026-11-16/native-reasoning-off-v2/PRIVATE_NATIVE_TRIAL.json`.
- Corrective v3: `data/local-acceptance/p16-stage-b2-2026-11-16/native-corrective-v3/PRIVATE_NATIVE_TRIAL.json`.

Private v2 record SHA-256: `991f91c1f436603d48dbcc2b33e473d0c9846d91cd235e71615fe727e841d7bb`.
Private v3 record SHA-256: `3912139e3b9b5efdb95c8e610495998ca223e1dc170e667714036cb5d87e885a`.

**Public/source-safe manifests, without original ad or model answer text:**

- `docs/working-memory/2026-11-16_p16_b2/SAFE_NATIVE_MODEL_COMPARISON_METRICS.json`: source hashes, prompt hashes, case-level counts/timing and raw-record SHA.
- `docs/working-memory/2026-11-16_p16_b2/SAFE_ASSISTANT_SOURCE_SEMANTIC_CHECKS.json`: 12 assistant-diagnostic pass/partial/fail rationales with source identities and explicit non-independent authority.
- `docs/working-memory/2026-11-16_p16_b2/SAFE_RECONCILED_B2_GATE.json`: **`OPEN_NO_PROMOTION`**, generated offline from the exact raw model records plus the prior checks. It validates source snapshot equality, model/prompt identity, nonreasoning JSON outputs, review provenance and presence of material failure; it does **not** claim to algorithmically adjudicate employer meaning.

**Quality verification:** local full suite **1,013 passed** with warnings-as-errors; focused native/reconciliation controls **20 passed**; repository Ruff, pip dependency checks, and Git whitespace checks passed. GitHub branch CI remains separately required before any acceptance claim.

**Code and tests:** `scripts/probe_b2_native_reasoning_off.py`, `scripts/probe_b2_native_corrective_v3.py`, `scripts/reconcile_b2_native_trials.py`, `tests/test_b2_native_reasoning_control.py`, `tests/test_reconcile_b2_native_trials.py`.

No B1 schema, Stage A anchor identity, accepted English v30/original v9 analyzer, translation projection, database migration, Career/Capability/Work/Registry/Market authority, or production route was changed.

## 4. Product/architecture decision

**Stop prompt-only iterations for this slice** (v2 baseline + one bounded v3 correction). The additional wording helped some alternates but did not remove known false employer requirements and false duties, and even caused new arrangement-vs-eligibility confusion. No automatic correctness improvement is claimed.

If we build a combined source + model diagnostic, use this **minimal non-promoting design**:

- Original source and Stage A exact anchors remain the evidence owner. The B2 deterministic source parser and source-owned AND/OR candidates remain *candidate only*, with known unsupported grammar unresolved.
- A local LLM response is **advisory interpretation**, not an employer statement or approved B1 item. Keep work-implied ability useful without turning it into previous professional employment requirements.
- Inferred employer requirements/duties with no admitted original **item-level** source association must remain `unresolved` or unsupported, not automatically promoted. Existing whole-field translation provenance and valid JSON cannot substitute for item-level semantic review. A potential source cue can **flag** discrepancy; a regex match must not claim independent semantic proof.
- When the deterministic and LLM views disagree, preserve both source-referenced candidates and an explicit conflict rather than auto-picking one. In `tNDx`, `tMjm` and `tNhZ`, that is safer than either relying exclusively on the model or expanding a fragile parser.
- Do not add a new global skill ontology, extensive per-case prompt rules, nested validation retries, or extra LLM calls unless measured improvement on fresh work justifies them.

**B2 semantic acceptance: NOT PASSED.** The deterministic subspan logic is mechanically verified on two exposed formats; the model now responds but still fails material semantic checks. Do **not** merge the experimental source interpretation into accepted main as if employer facts are validated, and do **not** advance these model claims into B3 translation or downstream job/career recommendations.

**Next controlled milestone:** a **minimal candidate reconciliation/grounding contract** that can admit exact original spans and flag unsupported model-generated role assertions, while preserving uncertainties and useful duty-capability relationships. Validate it against the four exposed cases and genuinely different synthetic phrasing; only then decide whether more model inference or new corpus cases are needed to close B2. B3–B6 remain separately gated.
