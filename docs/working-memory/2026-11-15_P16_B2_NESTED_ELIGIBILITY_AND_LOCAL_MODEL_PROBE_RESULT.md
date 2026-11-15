# P1.6 B2 continuation — exact-source nested eligibility candidate and bounded local-model trial

**Date:** 2026-11-15
**Branch:** `feature/p16-b2-source-items-metadata-2026-11-15`, extending draft PR #20.
**Parent accepted main:** `5d4a5e0a64e1dc1da64bc9f28848b4357895aa7e`.
**Disposition:** Nested eligibility **mechanically verified on the two exposed formats**; **semantic model comparison NOT ESTABLISHED**. The full B2 acceptance gate stays **OPEN**.
**Previous slice:** `docs/working-memory/2026-11-15_P16_B2_SOURCE_ITEM_DIAGNOSTIC_FIRST_SLICE_AND_OPEN_GATE.md`.
**Constraint:** Original employer evidence authoritative; no inferred source skills or scope becomes automatically accepted or eligible-for-job policy; no public or downstream writes.

## A. Nested eligibility — what improved

The prior draft B2 sidecar preserved source-anchored alternative clauses, but projected only the seniority-track **OR** without within-track conditions. The new isolated `src/jobhunter/source_eligibility_candidate_b2.py` admits exactly two recognizable patterns:

1. **`tMps` Middle/Senior:** a candidate `any_of` root with **Middle = all_of(years, any_of(domain choices), executed project)** versus **Senior = all_of(years, design/production-deployment experience)**. A dedicated exact Stage A anchor is created for each source clause/option; the source-owned domain scope is preserved as graph basis. The B1 draft graph has **13 nodes, 9 leaves**, with scope-marked conditional requirements.
2. **`tNDx` certification equivalence:** a candidate `any_of(certificate, equivalent knowledge)`, **3 nodes, 2 leaves**, anchored to the exact original alternative within the broader source-required Network+/Security+ knowledge item. The distinct bare Kaspersky certificates and government-client experience statements remain unresolved, not mandatory.

All graphs remain `candidate` with `candidate_unreviewed_not_eligibility_authority` semantics; they're usable to inspect logical topology, **not** to qualify/disqualify applicants or construct accepted employer requirements.

The extractor deliberately **does not** build a complete graph for unsupported or ambiguous syntax. For example, mixed comma/OR technical domains such as a list ending in "RAG or NLP" are withheld rather than treated as an atomic required domain. An explicit **AND** between certificate and knowledge is not wrongly converted into **OR**. No new B1 schema or production analyzer change is required.

The projection in `scripts/diagnose_stage_b2_candidate.py` now includes source-owned component items and qualified graph nodes. Every source anchor, board reference and conditional graph passes the B1 draft structural/source verifier in the private frozen diagnostic. This verifies reference integrity and Boolean structure only, not semantic interpretation. The old 78 original item candidates, 53 separate board references and 10 optional duty-capability hints remain; the 11 conditional graph leaves are **subspan components**, not 11 newly discovered independently validated employer facts.

**Truth-table defense:** Middle years plus project without a domain does **not** satisfy Middle; Senior years plus deployment does; mixing Middle years with Senior deployment does **not** make an invented path. Certificate **or** knowledge satisfies the alternative, neither fails. Tests also cover altered source hashes, malformed source boundaries and unsupported syntax, plus a synthetic different-years/different-domains positive case (to reduce case-specific memorization).

**Second read-only diagnostic output (private):**
`data/local-acceptance/p16-stage-b2-2026-11-15/nested-eligibility-v2/`

**Public source-safe metrics:**
`docs/working-memory/2026-11-15_p16_b2/SAFE_NESTED_ELIGIBILITY_METRICS.json`

SHA-256 of safe metrics:
`601d54055053c1791e98f8d688d843f184ce4e5a502f26c28a9f126720a1af17`.

SHA-256 of full ignored diagnostic:
`95645cb00989855b5383aa83e2202b726085a64f98c843147369df3d361d7b11`.

Frozen B0 SQLite remained exactly:
`bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`.

## B. One bounded local original-language semantic model probe

The WSL environment had `HTTP_PROXY` settings that intercepted ordinary localhost requests. A direct no-proxy connection to `http://127.0.0.1:18080/v1/models` succeeded and exposed Gemma 4 E4B, permitting a fixed local-only trial setup with **no cloud fallback**.

The new `scripts/probe_b2_local_semantics.py` uses:

- **Model:** `gemma-4-e4b-it-ud` via the fixed loopback LM Studio endpoint.
- **Input:** complete preserved parsed *original* job description from the same four exposed B0 versions.
- **Prompt:** one compact English-output source-understanding prompt with seven arrays: duties, requirements, preferences, alternatives, arrangements, uncertainties and work-implied capabilities. It explicitly distinguishes employer statements from work-implied ability; it is not tuned per advertisement and does not impose a long category micro-rulebook.
- **Budget:** temperature 0; max 760 output tokens; one attempt per case; 95-second per-request timeout; stop on the first failed/slow request; no retry or prompt repair.
- **Privacy:** output under ignored local data only; raw prompt, metadata and source hashes retained; no network service other than the authorized fixed loopback endpoint.

**Observed run:** the first original job `tNhZ` returned **no response** before the 95.02-second timeout. The remaining **three were deliberately not attempted**. The private interrupted run was retained as evidence. Therefore **0 completed model answers / 1 attempted / 4 planned**; no source-semantic comparison, useful-answer completeness score, or claim that the deterministic baseline is semantically superior is authorized. This is a **runtime/availability failure of the selected local configuration**, not evidence that LLMs cannot improve B2.

Private first-attempt record:
`data/local-acceptance/p16-stage-b2-2026-11-15/local-semantic-probe-v1/PRIVATE_MODEL_TRIAL.json`

Its SHA-256:
`74392e80d803deb9c1e41d165a575799a30a2b645e9c3f8b348bd6f97c8e200a`

Frozen prompt SHA-256:
`7ac4dc5ac048ed18db2c301a67859afd9bdcd04ffc642dd3561bc1d1f3d77a07`

Public safe outcome:
`docs/working-memory/2026-11-15_p16_b2/SAFE_LOCAL_SEMANTIC_PROBE_OUTCOME.json`

**Decision:** Do not compensate for this failure with more job-specific regexes or a longer prompt, and do not run additional 95-second calls blindly. Diagnose LM Studio model loading/throughput in a separate, bounded hardware check before reattempting a fixed semantic comparison. Keep the original baseline and failed attempt retained; any new model/configuration or prompt is a *new* experiment, not a retrospective repair of this fixed run.

## C. Engineering acceptance, full B2 gate

The current continuation adds `tests/test_source_eligibility_candidate_b2.py` and `tests/test_b2_local_semantic_probe.py`, together with a correction to prior diagnostic-test expectations. Focused tests verify source identity, exact component provenance, Boolean truth tables, fail-open unsupported syntax, no cross-track mixing, no claims of independent review, no cloud/fallback and no semantic acceptance.

**Local verification:** 993 full repository pytest tests passed with warnings as errors; Ruff, pip dependency consistency and Git diff checks passed. There are 24 new nested eligibility-focused and 3 new no-network model-probe tests (47 focused B2/probe tests combined). **GitHub PR CI remains a separate requirement; do not claim CI acceptance before GitHub reports it.**

The B2 engineering **nested-topology candidate** is stronger than PR #20's first slice, but the full B2 gate is **OPEN** because:
- Both admitted patterns are *exposed* examples; unknown document layouts and other eligibility grammar remain unresolved.
- Graphs have not received independent source-semantic adjudication and are not applicant-eligibility decisions.
- Minimal local-model comparison has **no usable response**; comparative model relevance, omissions, overclaiming, prompt complexity, latency and downstream usefulness are **not established**.
- No B3 translation, B4 user brief, B5 untouched holdout evidence, or B6 controlled product integration.

**Next:** investigate the local inference throughput/model-load boundary, make a new (clearly versioned) bounded trial if the runtime is responsive, compare responses to the *same* exact sources on factual misclassification, alternative path fidelity and false-suppressed work capabilities. Avoid over-expanding deterministic grammar; preserve unresolved cases honestly. Continue only on the draft research branch until semantic usefulness and generalization gates justify any merge.
