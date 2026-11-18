# P1.6 B3 — source-bound bilingual translation milestone

**Date:** 2026-11-18
**Disposition:** PASS_BOUNDED_EXPOSED_COHORT
**Branch:** feature/p16-b3-source-bound-item-translation-2026-11-18
**Base:** feature/p16-b2-source-items-metadata-2026-11-15 at 97d5fda
**Scope:** Candidate-only source-bound translation on four previously exposed B0 development ads. This is not unseen generalization, independent human certification, accepted employer-fact promotion, or a production route change.

## Decision

B3 passes its bounded exposed-cohort gate. Every Persian translation request was tied to exactly one frozen source item and original source span. The model received the exact item text, not its heading context or neighboring clauses. The native-English item remained an identity case. All four B1-compatible bundles validate, and all selected translations have an explicit source-bound candidate or identity record.

The initial primary run produced one material personal-trait mistranslation. The original result was retained, one evidence-justified corrective request consumed the final request-budget slot, and the corrective candidate was selected with a documented terminology normalization. No other material meaning-changing translation issue remained in the assistant's review of the four exposed ads.

## Frozen selection and execution

| Measure | Result |
| --- | ---: |
| Original B2 source items | 78 |
| Eligible top-level items | 64 |
| Persian primary translations | 63 |
| Native-English identity items | 1 |
| Justified corrective generation requests | 1 |
| Total model generation requests | 64 / 64 |
| Context-only items excluded | 12 |
| Generic application instructions excluded | 2 |
| Nested eligibility leaves retained as source subspans | 12 |
| B1-compatible bundles validated | 4 |

The 12 nested eligibility leaves (10 in tMps, 2 in tNDx) are contained within selected parent qualification items. They were not translated again as duplicate requests. Their source identities remain preserved, while separate child target offsets remain not established.

The local gemma-4-e2b-it translation-v2 provider completed 63 primary requests and one corrective request. The 63 primary requests each contained one exact source item only. The corrective request contained that same exact source item plus a narrowly scoped correction note. Heading context was not sent to the model.

- Model completion attempts: 64
- Transport retries: 0
- Truncation recoveries: 0
- Prompt tokens: 18,462
- Completion tokens: 24,496
- Per-item request/response hashes verified: 64
- Native identity model requests: 0

## Semantic review and correction

The assistant reviewed all 63 Persian translation candidates against their exact original spans across the four exposed ads. This was an exposed-cohort review with prior project context, not a blind or independent human review.

One primary translation rendered Persian وظیفه‌شناس as “duty identifier” and مسئولیت‌پذیر as “responsibility acceptance.” This was a material trait mistranslation. The primary output and raw response remain preserved. One corrective request produced “Organized, duty-conscious, responsible, and committed.” The selected target uses the standard idiomatic equivalent “conscientious”:

**Selected candidate:** “Organized, conscientious, responsible, and committed.”

The normalization from “duty-conscious” to “conscientious” is explicitly recorded as a reviewer terminology edit; it is not represented as raw model output. The corrected candidate is used by the B1-compatible alignment. No further correction was needed.

The first run-time lexical warning set was overinclusive: substring matching for Persian يا, generic تست, and positive “mandatory” in “not mandatory” created false positives. The post-run diagnostic reassessment added word boundaries, distinguished generic testing from entrance exams, and corrected the negation logic. It did not alter the other 62 translation texts. The selected corrected target has no remaining B3 diagnostic flags.

### Critical source-meaning checks

- tNhZ: LLM familiarity remains preferred, explicitly not mandatory; work arrangements and remote context remain separate from applicant eligibility.
- tMps: Middle/Senior alternatives and one-of-domain structure remain in the source-owned candidate graph; translation does not absorb heading context.
- tNDx: teamwork remains preferred; Kaspersky credentials and government/large-customer experience do not gain unsupported strength; certificate or equivalent knowledge is preserved; the technical entrance-exam/final-acceptance condition is translated.
- tMjm: the conscientiousness trait is corrected; the requirements-only pentesting ad still has zero fabricated work duties.
- Exact source anchors and field hashes remain unchanged; no legacy whole-description translation is retroactively assigned item-level alignment.

Some literal or compressed source list wording remains less than publication-polished in English. These are recorded as minor fluency observations, not material changes to obligation, alternative, number, role scope, or work arrangement.

## Verification and reproducibility

The private run and audit artifacts are under ignored data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1/. The tracked scorecard contains counts, hashes, authority boundaries, and no raw source/translation text.

- B3_FINAL_AUDIT.json: PASS
- 63 primary source-only requests and one corrective request: raw request/response hashes verified
- Four B1-compatible bundles: PASS
- Authorization headers persisted: false
- Production database written: false
- Accepted employer facts promoted: 0
- Public route changed: false
- Downstream authority: none

Local engineering verification after the B3 implementation and review:
- Full suite: 1,063 passed with warnings treated as errors.
- ruff check .: passed.
- pip check: passed.
- compileall: passed.
- All six changed Python files pass targeted ruff format --check.
- A full-repository ruff format --check . still reports 227 pre-existing formatting deviations outside this change; no repository-wide reformat was applied.

The B3 run manifest retains the exact runner/support-module fingerprints used at inference time. A separate post-run flag reassessment records the corrected diagnostic module fingerprint; the original inference provenance is not rewritten.

## Limits and next gate

B3 PASS is bounded to these four exposed development ads. It does not establish accuracy on unseen postings or independent human certification. B2 full semantic generalization and B5 unseen-cohort generalization remain NOT ESTABLISHED. Candidate categories and employer-strength judgments remain candidate-only; no accepted P1.6 facts or downstream records changed.

Next: B4 — useful non-authoritative job understanding. Build a source-qualified candidate brief with explicit unknowns and partial/fail-soft states; compare it against unchanged v30/v9 on the same frozen sources. Measure useful information and reviewability without asserting owner-time savings or promoting the candidate into production. B5 fresh unseen verification and B6 explicit promotion/rollback remain separate gates.
