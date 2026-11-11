# P2.3B — Evidence-backed job capability expectations: first executable experiment

**Date:** 2026-11-11
**Status:** V0 CANDIDATE IMPLEMENTED / MECHANICAL SAFETY PASS / MODEL ADVICE-READINESS FAIL
**Branch:** `experiment/p23b-capability-expectation-2026-11-11`
**Source baseline:** `main` at `2de22a877772cf4a40154d8118a35ad19d1af8b7`
**Controlling proposal:** `2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md`
**Authority:** No P2.3 persistent profile, canonical equivalence, semantic promotion, personal scoring or market aggregate authorization.

## 1. Reuse and gap audit

Existing shared `build_job_comparison` provides current/accepted P1.6 claims, exact immutable claim identity, obligation, explicit depth, direct duties, reviewed Registry mappings, source drill-down and opportunistic current Capability v9 groupings. There is no reason to duplicate these owners.

The *three accepted RAG test postings* currently have **no eligible current Capability v9 overlay or Work Intelligence v2**. Source facts are nevertheless current and recoverable. The separate Python anchor `tG9K` has current Capability v9 artifact 11; that group is interpretive, not a canonical or additive demand partition.

| Public job ID | Phrase | Accepted claims | Matching qualifications | Matching directly stated duties | Explicit depth on matched qualifications | Current Capability v9 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `tvMm` | RAG | 36 | 2 | 1 | 1 | unavailable |
| `tNVe` | RAG | 32 | 3 | 1 | 0 | unavailable |
| `t7Ay` | RAG | 26 | 3 | 0 | 0 | unavailable |
| `tG9K` | Python | 41 | 2 | 0 | 1 | present |

**Important semantic discovery:** `tNVe` contains a disjunctive requirement about alternative project types; marking the *whole claim* required does not mean each mentioned technology is independently mandatory. `t7Ay` has explicit qualifications but zero accepted direct duties, so no RAG job-specific actions or ownership may be asserted as employer facts.

The literal read model is incomplete as semantic interpretation: absence of a matching word cannot establish absence of a capability, and a shared requirement excerpt is not proof of each disjunct's obligation. That is the concrete rationale for P2.3B.

## 2. Executable V0 contract and implementation

The candidate read model in `src/jobhunter/capability_expectations.py` is deliberately separate from source truth:

- Each selected fact retains accepted P1.6 analysis ID, kind, index, exact wording, obligation/depth, and source/claim links.
- Exact matching qualifications and direct work are never silently mixed or restated as newly accepted work.
- A regex-based *possible-alternatives flag* triggers manual review; it is not a general semantic parser or obligation correction.
- Questions to verify technical scope/practice are explicitly candidate guidance, not employer-stated demands.
- `ProposedInterpretation` supports separate `strongly_implied_by_work`, `model_inferred_prerequisite` and `unknown_or_unsupported` statuses, confidence, rationale and exact claim references. This does not supersede the fuller current Capability-v9 internal contract.
- Mechanical validation rejects unselected/stale references, duplicate/oversized support, unsupported statuses, implied-work proposals with **no selected direct responsibility**, and model-prerequisite proposals without a non-alternative required claim.
- These checks are **necessary but not sufficient** for semantic correctness. Even a mechanically valid interpretation may simply echo employer wording, assert unsupported causal implications, or provide no useful career action.

The `inspect_capability_expectation.py` command presents an arbitrary configured job+phrase read-only, with an optional candidate JSON input that passes the same validation. `capture_p23b_capability_expectation_cases.py` deterministically reproduces the four fixed real-case summaries. Both use temporary SQLite online backups and never build new acceptance artifacts, call sources or rewrite local state.

No new browser route, tables, migration, bulk model job, Registry decision or accepted Capability artifact is created.

## 3. Corrected LM Studio endpoint and controlled V0 trial

The correct configured endpoint is **`http://127.0.0.1:18080/v1`**, as already defined by `jobhunter.toml` and `config/local.toml`. This was confirmed by HTTP 200 on `/v1/models`. LM Studio's model-management API confirmed configured `gemma-4-e2b-it` was actually loaded. The earlier check against default port 1234 was a **diagnostic mistake**, not evidence that the local service was down.

Model calls were made only from the local WSL environment, using the configured endpoint/model, accepted P1.6 facts, a bounded prompt, zero temperature and bounded token caps. Trial raw source/model text remains ignored under `data/local-acceptance/p23b-capability-expectations/`; only public job IDs, model name, counts, failure class and authority flags are published.

| Trial | Case | Model/condition | Outcome |
| --- | --- | --- | --- |
| 1 | `tNVe` RAG | Gemma E2B, initial prompt; 1400 tokens | JSON wrapped in Markdown fence; initial strict parser rejected. After safe whole-fence parsing, one proposed item merely re-echoed explicit work; another illicitly inferred work from a qualification. **Not advice-ready.** |
| 2 | `tNVe` RAG | Gemma E2B, tightened prompt; 1700 tokens | Three candidate items; one direct-work paraphrase without useful new insight; two attempted to promote qualification-only evidence into work implications. Mechanical proposal gate rejects the batch. **Not advice-ready.** |
| 3 | `t7Ay` RAG | Gemma E2B, tightened prompt; 1500 tokens | Three items: two tried to infer duties from requirements, one converted a preferred qualification into a prerequisite. All three independently fail mechanical grounding. **Not advice-ready.** |

No trial is treated as a pass merely because the endpoint responded, JSON was well-formed, or an isolated proposal referenced a real claim. Empty/non-improving candidates are legitimate outcomes. Model evidence must not be silently elevated to source facts.

Public-safe reproducible summaries:
- `2026-11-11_p23b_capability_expectation/REAL_CASE_MECHANICAL_AUDIT.json`
- `2026-11-11_p23b_capability_expectation/LOCAL_MODEL_EVALUATION_FIRST_TRIAL.json`
- `2026-11-11_p23b_capability_expectation/LOCAL_MODEL_EVALUATION_tNVe_rag.json`
- `2026-11-11_p23b_capability_expectation/LOCAL_MODEL_EVALUATION_t7Ay_rag.json`

## 4. Independent quality and stop decision

Engineering acceptance checks include synthetic alternatives versus required-claim semantics, requirement-only/no-duty cases, preferred-only source limitations, stale/unknown claim-reference rejection, preserved original wording and claim URLs, explicit current P1.6 fallback, JSON fence handling, read-only GET/composition and no unnecessary model calls. **The full strict-warning test suite passed 887/887 tests in 54.40 seconds; repository Ruff and dependency consistency checks passed.** The original main baseline had 879 tests; the eight additional regressions belong only to this isolated experiment.

**Disposition:** V0 is a reproducible non-authoritative candidate **instrument**, not an accepted job-side technical expectation intelligence feature. The model-produced content has **failed** the initial advice-readiness cases; do not ship these generated interpretations to the normal browser, mark them accepted, or create persistent P2.3 profiles.

## 5. Recommended next substantive iteration

1. **Contract V1:** Require candidate ideas to contribute a distinct *technical activity, work-implied depth observation or explicitly bounded unknown*, not simply echo exact source statements. Every proposed activity needs a direct-duty source identity; a generic requirement cannot create a duty. Alternative-choice logic and preferred-strength guard remain independent.
2. **Quality experiment:** Fix the evidence set and contract, then compare a stronger *locally available* model against the configured Gemma E2B in a bounded paired experiment, keeping full raw outputs local. Grade specificity, source-grounding, added explanatory value, harmful overstatement and helpful next checks rather than only JSON validity.
3. **Promotion gate:** Only after at least the three contrasting RAG cases show useful, independently reviewed outputs without fabrication should a read-only user-facing trial be considered. Persistent corpus-wide profiles, taxonomy and personal recommendations remain separately gated.

This increment advances the *capability understanding engine and its error-detection substrate*, not the UI appearance. The next step is model/contract semantic quality, not another cosmetic comparison sprint.
