# Stage B planning reconciliation — decisions, legacy owners and execution handoff

**Date:** 2026-11-13
**Scope:** Documentation/authority reconciliation only; **no code, model or database work in Stage B**.
**Focused execution authority:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`
**Base accepted main when drafted:** `8eded9e15949fc34a041984a90e40d930f91f6fd`
**Planning decision:** B0 is next; B1–B6 remain conditional on their gates. P2.3 capability-expectation idea moves after Stage B source-fidelity qualification.

**November 14 execution supersession:** B0 is now PASS for frozen baseline/selection protocol and B1 contract/ADR is next. The historical B0-next steps below describe the prior planning decision, not current status. See `docs/working-memory/2026-11-14_P16_B0_FROZEN_BASELINE_AND_EVALUATION_PROTOCOL.md`. No Stage B runtime behavior has changed.

## 1. Evidence used, with authority and exposure distinguished

| Evidence/owner | What was actually established | Planning consequence |
| --- | --- | --- |
| `AGENTS.md`, product/domain/source/architecture/reasoning policies | Source facts, projection, semantic reasoning and accepted authority are separate; hard integrity failure vs soft interpretive uncertainty | No hidden bilingual upgrade into v30; sidecar candidate and separately reviewed durable promotion |
| `source_span_identity.py` on accepted main | Versioned exact original-description anchors, field-only legacy translation alignment; no categories or parsing authority | Reuse the accepted 64-character anchor; do **not** use research 32-character IDs |
| `evaluation/current-real-ads-2026-11-12` | New actual source capture/translation cases exposed quality failures, including an EDR adjudication subsequently corrected | Treat original Persian text as authority; preserve dated source correction, not the old mandatory-teamwork interpretation |
| `experiment/p16-source-fidelity-2026-11-12` | V31 helped some duty coverage but most cases failed/timed out; post-trial ledger safety changes were not live model re-tested | Borrow generalized tests/provenance ideas, **not** model-ready acceptance or prompt-only iteration |
| `research/p16-original-source-evidence-spine-2026-11-13` | 53 original exact spans across five jobs, two local source-bound translation trials; field-v2 item alignment still missing | Prototype per-item association but separately verify meaning and avoid unreviewed semantic heading heuristics |
| Stage A `3b13e7f` and A1 `8eded9e` on main | Passive source identity accepted; 59 assistant source-anchored A1 claims, 18 flags and 11 translation observations; user's two original drafts preserved | Implementation from known material problems, not arbitrarily broader taxonomy/UX expansion |
| `docs/working-memory/2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md` | Previous next-feature candidate investigated work/capability expectations; **not a deployed P2.3 profile** | Retain as future feature; do source-quality prerequisite Stage B first |
| B2, Market R4 and P2.3A comparison closures | Existing accepted Registry/Market/Work/Capability/compare conclusions and currentness | Do not regenerate old accepted anchors or reopen closed normalization just to satisfy Stage B |

All November 12–13 case findings are **exposed diagnostic evidence**. Assistant interpretations were not truly blinded from prior chat context. No claim that these are statistically representative, or that all 18 flags are distinct proven production defects, is justified.

## 2. Explicit decisions taken for the new plan

| Decision | Status / reason |
| --- | --- |
| Stage B takes next execution slot ahead of P2.3 capability-expectation feature | **SELECTED**, material original source-quality and obligation errors affect the latter's evidence |
| Source-exact original anchors are versioned and separate from classification | **SELECTED**, use accepted `jobhunter-source-span-identity-v1` |
| Metadata tag treated unconditionally as required | **REJECTED**, source may explicitly say the same prior familiarity is optional |
| Auto-promote item/classification because a model is schema-valid | **REJECTED**, EDR v9 acceptance without independent source fidelity proved the distinction |
| Auto-correct legacy translated English v2 by inserting original Persian evidence into v30 | **REJECTED**, violates mode-specific source/evidence boundary |
| Bulk merge heuristic research parser or v31 to main | **REJECTED**, unverified meaning and mixed heading/strength defects |
| New bilingual candidate sidecar before durable migration | **SELECTED DEFAULT**, minimizes currentness blast radius and enables utility tests |
| New v3 English projection or new persistent table immediately | **DEFERRED**, B1/B3 must establish necessity, owner and migration first |
| Independent unseen cohort and predeclared rubric | **REQUIRED B0/B5**, else generalization/promotion NOT ESTABLISHED |
| Human owner manually review all sources | **NOT REQUIRED**, owner delegated routine assessment; assistant states own review provenance |
| Unknown Kaspersky certificate requirement, remote-work policy, salary contradictions | **UNRESOLVED**, source insufficient; do not ask owner to guess employer intent |
| Candidate job brief may be useful before durable P1.6 | **ALLOWED CONDITIONALLY**, correct source labels, traceability, partial/failure status and no downstream reuse |
| New public P1.6 routing | **NOT AUTHORIZED**, B6 requires separate promotion decision after evaluation |
| Multiple prompt-only candidates until pass | **REJECTED**, predeclared budget, general defects and bounded corrective cycle |

## 3. What each controlling document now owns

- `AGENTS.md`: mandatory Stage B read path and no-promotion caveat.
- `docs/ROADMAP.md`: strategic *priority* of original-source fidelity prerequisite over the old next P2.3 candidate.
- `docs/IMPLEMENTATION_PLAN.md`: explicit stage B B0–B6 delivery and acceptance order, distinct from historical closed P2.2B.
- `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`: status-only overlay, superseding older present-tense “P2.3 is next” wording without erasing accepted history.
- `docs/EXECUTION_TODO.md`: B0 operator tasks and gates, old P2.3 task clearly deferred.
- `docs/WORKING_MEMORY.md`: concise current handoff, state, stop conditions and next operator work.
- `docs/working-memory/2026-11-13_JOBHUNTER_RESEARCH_PROMOTION_AND_MANUAL_REVIEW_INDEX.md`: reconciled historical branch references, user review delegation and new controlling plan.
- This decision record: exact historical inputs, selected/rejected/deferred interpretations and open questions.
- The focused plan: detailed architecture, acceptance semantics, B0–B6 implementation and evaluation tasks.

No older independent audit notes, model output or frozen JSON are rewritten by planning. Existing corpus/SQLite files must remain untouched on the planning branch.

## 4. Immediate B0 operator handoff

1. Start from the new accepted `main` commit; verify governance/read order and clean tree; create a **new implementation branch**, not a feature from previous unmerged experiments.
2. Produce a state/status-only baseline record: accepted source/translation/P1.6/Work/Capability/Market identity and current SQLite integrity/FKs. Use **SQLite online backup** for all experiments.
3. Freeze four A1 exposed test cases, historical accepted five anchors and source-exact expected outcomes without falsely converting the assistant's earlier classifications to independent human truth.
4. Predeclare **6–8 suitable new, not-yet-inspected vacancies** if ethically and technically obtainable through permitted source acquisition. Preserve timestamps, URLs and original hashes; no proxy bypass, invented freshness or post-hoc reuse.
5. Specify model budget, timeout semantics, fallback output acceptance, source review exposure labels, metrics/denominators and B1 contract questions. Finalize an inspectable B0 gate report. **Do not begin B2 coding merely because the plan has been committed.**

**Completion criteria for this planning increment:** all cross-owner links resolve, there is one active next stage, no code/currentness changes, accepted closed work remains closed, and the user can start B0 without reconstructing the November 12–13 conversations.
