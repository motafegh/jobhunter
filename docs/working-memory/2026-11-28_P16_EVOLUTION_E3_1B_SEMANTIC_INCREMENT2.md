# E3.1b — independent R2/R3/R4 repair seams (2026-11-28)

**Status:** second verified offline semantic implementation increment. E3.1 remains open. Base `20d6de04ee606aa6560d7de1348f763377923371`; [previous CI 46052599131](https://github.com/motafegh/jobhunter/actions/runs/46052599131) passed. Continues [increment 1](2026-11-27_P16_EVOLUTION_E3_1B_SEMANTIC_INCREMENT1.md). No production module changes, actual inference, source acquisition, fresh translation or accepted authority change.

## Implementation and evidence

| Seam | Owner and mechanism | Verified result and boundary |
| --- | --- | --- |
| R2 | `p16_lab_a1_r23.AnalysisRequirementR2` and `_validate_motivation`: narrow exact unmixed motivational item, preserve whole meaning and source strength, reject invented technical depth/typing; otherwise incumbent validators | Both retained motivation items recover, neither full response passes because independent requirement coverage remains incomplete. Genuine depth and preference controls preserved. Not a general motivation classifier. |
| R3 | `p16_lab_a1_r23.corrected_duty_plan`: derive incumbent plan; remove only a supplemental duty whose exact Skills heading and qualification text match the independent explicit qualification plan, unique source heading boundary and bounded clause | One false duty removed, 7 genuine duties retained; one retained partition passes unchanged raw output, deleting a genuine duty still rejects. First retained security response still fails unrelated item checks. No general classification by heading alone. |
| R4 | `p16_lab_a1_r4.BoardSkillObservation`, `board_skill_observations`, `separate_board_skills`, `verify_board_observations`: original source-version identity, exact array selector and value, field/value hashes, separate board authority with employer obligation not established | 52 tags across all 12 frozen source versions verified with immutable read-only snapshots; no asserted obligation by observation. Original tag values and duplicates retained, no inferred per-tag translation equivalence; projection association must be established by caller. Existing V5 deterministic skill requirement path is not yet replaced in combined adapter. |

The R1+R2 response class is available as an experimental schema composition, not a fully integrated A1 provider. R3 must be applied consistently at generation and persistence ledgers. R4 must be separated at the actual inherited provider and persistence boundaries, not merely relabeled after generation. Legacy V5 expects skill tags in the requirement array, and strips item_excerpt: candidate-only envelope and explicit boundary handling are needed before declaring combined A1 complete. Avoid introducing board observations into the accepted V5 namespace or weakening actual employer prose coverage. No per-ad rules or silently changed incumbent behavior.

## Verification

- 27 new automated controls (all pass), 154 total lab/qualification/semantic repair tests, 235 focused regression tests with warnings as errors. Repository-wide Ruff and diff checks passed.
- `scripts/verify_p16_a1_r234_replay.py`: hash-pinned E1 reconstructed partition contexts, all six retained completions evaluated independently for R2, actual V21 duty plan compared with captured partition before R3, same original response revalidated after correction. R2 2 item recoveries; 0/6 full response passes. R3 1 full partition recovery, 7/8 planned work references preserved, exact missing genuine duty negative rejected. This is not a complete service-level or live end-to-end result.
- R4 actual original source checks on all 12 selected versions: verify frozen snapshot and selection hashes, source version/semantic/original description hashes, closed read-only immutable SQLite; 52 tags independently bound and reverified. No employer qualification inference from board metadata. No original source content included in the public receipt.
- R1 original replay remains passing its bounded assertions (4/4 recovered items; 0/6 full response passes). Protected-state reconciliation, freeze and governing inputs verified unchanged.
- Remaining original 15 E1 counterfactuals need combined adapter verification; individual synthetic controls and retained replay are not equivalent to a combined result.

[Safe verification](2026-11-28_p16_e3_1b/SAFE_E3_1B_INCREMENT2_VERIFICATION.json).

## Next

Complete explicit combined A1 provider/service and candidate envelope (raw vs normalized scope, R3 persistence, R4 board observations separate), actual offline guarded partition path and all applicable retained controls. General A0 schedule binding beyond fixed D1, then A2 contextual contract/reconciliation. E3.1 is not closed; real runtime/rights/tokenizer/context/resource/idle/ownership and executable preflight gates unchanged. No model requests or authority promotion. Master checklist remains 26/45.
