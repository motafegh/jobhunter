# P1.6 B2 advisory claim grounding — exposed, candidate-only reconciliation

**Date:** 2026-11-16
**Branch / PR:** `feature/p16-b2-source-items-metadata-2026-11-15` / draft #20.
**Parent accepted main:** `5d4a5e0a64e1dc1da64bc9f28848b4357895aa7e`.
**Disposition:** Source-link/location reconciliation **IMPLEMENTED**; B2 semantic gate **OPEN_NO_PROMOTION**. No new model calls, prompt versions, source fetches, production writes, accepted employer facts or downstream authority.

## Why this increment

The native reasoning-off v3 trial was complete JSON but could still invent assigned pentest duties, promote preferred teamwork into required, assign unwarranted preference strength to Kaspersky credentials, and confuse arrangements with applicant alternatives. The earlier seven-array model output gave **no original-item references**. A string match or exact span hash cannot retrospectively establish correct Persian→English semantic entailment.

This increment therefore tests the smallest separable integrity/diagnostic contract: optional explicit model-claim→source-item links, with exact source version/anchor verification and conservative source-candidate disagreement signals. The link has its **own provenance** (`model_suggested` versus `assistant_exposed_diagnostic`). A linked unflagged claim is NOT a semantically verified fact. An unlinked claim is unresolved/unsupported for employer authority, NOT evidence that the employer requires nothing. The source-item heuristics themselves are unreviewed candidate interpretations.

## Delivered

- `src/jobhunter/source_claim_reconciliation_b2.py` — pure candidate-only claim reconciliation; exact job/source-version/field/index/text SHA, verified Stage A original anchors restricted to verified B2 original item candidates; duplicate and stale citation rejection; separate source-location and semantic review states. Disagreement flags are advisory: duties anchored to applicant qualifications, mandatory/preferred strength overstated relative to candidate source classification, eligibility alternatives linked to arrangements, and work-implied capabilities unlinked to duties.
- `scripts/diagnose_b2_claim_grounding.py` — read-only, offline diagnostic over the **unchanged frozen B0 database and immutable saved native-v3 model answers**. Reads a private, explicitly assistant-selected link annotation file. No auto-translation, heuristic cross-language claim matching, new LM Studio call, scrape, schema alteration, accepted analyzer change or source-to-model inference pipeline.
- `tests/test_source_claim_reconciliation_b2.py` and `tests/test_diagnose_b2_claim_grounding.py` — synthetic variants, exact reference and review-provenance boundaries, stale/model-claim fingerprints, misclassification signals, preserved work-capability reasoning, and optional private real-case verification.

The existing `jobhunter-stage-b1-source-evidence-bundle-draft-v1` contract, source identity, accepted English P1.6 v30/original v9, translation v2, downstream Capability/Work/Registry/Market, and publication/currentness paths remain unchanged.

## Exact diagnostic (four already exposed postings; NOT independent evaluation)

Frozen B0 SQLite SHA-256 (unchanged):
`bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`

The saved corrective-v3 output has **85 string claims** across seven fields and four real exposed source postings. The assistant deliberately selected 14 illustrative, exact original-source item links for the known disputes and a few positive/context examples. These annotations are retrospective and prior-outcome-exposed. **71 claims had no source link**, because the existing model output contains none; no fabricated automatic item alignment is supplied.

| Case | Model claims | Explicit assistant links | Candidate disagreements | Unlinked / unresolved |
| --- | ---: | ---: | ---: | ---: |
| `tNhZ` | 20 | 4 | 2 | 16 |
| `tMps` | 25 | 1 | 0 | 24 |
| `tNDx` | 22 | 4 | 3 | 18 |
| `tMjm` | 18 | 5 | 4 | 13 |
| **Total** | **85** | **14** | **9** | **71** |

Of 14 linked claims, **nine candidate disagreements** were raised and **five remained linked but semantically unreviewed**. These numbers are *not* model error rates, detection recall, model-vs-parser superiority, independent Persian-meaning checks, or evidence of improved user accuracy. In particular, the 9 flags are candidate-to-candidate disagreements only:

- `tNDx`: required teamwork linked to original preferred teamwork; two model-preferred credentials/customer-history claims linked to source clauses whose obligation strength is unresolved.
- `tMjm`: four model-assigned duties linked to original applicant-capability clauses; no assertion that the employer assigned those tasks is proven.
- `tNhZ`: two model eligibility alternatives linked to actual part/full-time or remote work arrangements.
- `tMps`: a linked Middle/Senior alternative is not proof of full nested eligibility semantics; its source-owned graph remains candidate-only.
- Positive/context controls preserve a genuine LLM work duty and its optional work-implied capability without inventing prior professional employment.

**No employer facts accepted, zero claims promoted, and no user-facing/current routing changed.**

## Private/public evidence and reproducibility

Only safe metrics are tracked:

- `docs/working-memory/2026-11-16_p16_b2/SAFE_CLAIM_GROUNDING_METRICS.json`
- Safe metrics SHA-256: `27cf4669ced4aff5a603b0c9e773aead777881dbb550370da88a2df7ee237997`.

Ignored private evidence (not for repository publication):

- `data/local-acceptance/p16-stage-b2-2026-11-16/source-claim-grounding-v1/PRIVATE_REVIEW_LINKS.json`; SHA-256 `73b6fbc0bbd2262da45e608e91572349c43eaed4d919a53a6e13e1fab2e32e27`.
- `data/local-acceptance/p16-stage-b2-2026-11-16/source-claim-grounding-v1/PRIVATE_LINKED_RECONCILIATION.json`; SHA-256 `725ed197cc7f1f4aabf5b78031adb6a1061e285d76d66a157ad4c01567741838`.
- Original frozen B0 SQLite and already saved native-v3 raw provider record remain unchanged and ignored.

The diagnostic script requires exact frozen database/trial/claim hashes and explicit reviewer-link provenance, copies the SQLite input before all service reads, checks source data unchanged after completion, writes private claim traces only under ignored `data/local-acceptance`, and writes counts/flags only under the safe B2 evidence directory. It refuses overwritten output and is not in production execution routing.

## What this evidence DOES NOT solve

1. **No scalable automatic source association yet:** the existing native-v3 output never cited original items. Fourteen assistant-added example links do not substitute for a source-citing model interface or verified bilingual item alignment.
2. **No semantic entailment verification:** even a perfect anchor can be attached to the wrong English claim; the source candidate's own categories are heuristic. No automatic accept/reject/semantic-certification follows from absence/presence of a flag.
3. **No independent generalization:** all four ads are exposed, and no B5 untouched cohort has been collected. The 12 earlier assistant checks remain a separate non-independent diagnostic and cannot be combined into an accuracy denominator.
4. **No user-time evidence:** this is a bounded engineering diagnostic, not B4 job-understanding UX or measured applicant decision support.

## Next controlled decision

Keep PR #20 **draft**. The narrow follow-up is to decide whether source-item references can be supplied as part of ONE bounded, versioned advisory-model interface *without increasing model hallucination, suppressing contextual work-capability interpretations or causing material output/token cost*. Measure usable correctly referenced claims and false strength/duty implications against the same exposed cases plus genuinely different negative fixtures. If source-link generation is not useful, retain explicit partial/unlinked status and do **not** enlarge a regex catalog, schema, prompt rulebook or extra LLM call graph. Completion of B2 still requires the focused plan's full gate. B3 translation meaning, B4 usable brief, B5 independent new cohort and B6 promotion remain separately gated.

**No B2 semantic PASS or rollout authorized by this increment.**
