# P1.6 Stage B — calibrated source gate and candidate-only B2v6 remediation

**Date:** 2026-11-22
**Branch:** `main`
**Disposition:** **PASS versioned offline evaluation-method repair and exposed-regression engineering only. NOT B5 accepted, NOT B6 promotion.**
**Authority:** Historical prospective fourth-cohort failure remains as published at `f2e396a` / `2c85bea`; the original evaluator, source-first reviews, raw source files and frozen output were not edited.

## 1. Why a new evaluation contract was necessary

The original B5 evaluator required each selected exact-source assertion to fit **inside one source item** and counted every reviewer-labeled alternative as missing unless the entire advertisement had at least one alternative group.

Two source-first assertions in the fourth cohort exposed weaknesses in those rules:

1. A selected duty assertion crossed two *adjacent* separate original HTML bullets. Both were retained as `work_duty`, one source item each, but no single item contained the combined review span. This caused a **false missed-duty result**. The new method requires exact nonwhitespace source coverage by contiguous source items of the correct duty category; gaps, skipped content and wrong-category pieces still fail. This does not retroactively change the original source review span.
2. A source statement naming Agile methods as examples (`Scrum, Kanban`) was labeled `alternative` by the assistant. No explicit employer one-of eligibility rule was present. Requiring a formal OR graph was **an invalid gate criterion** for that source meaning. The new scorer distinguishes example/illustrative option lists, explicitly reviewed eligibility disjunctions, and genuinely unresolved alternatives. Formal eligibility scope must attach to the **same exact source item**, not an unrelated OR elsewhere in the advertisement.

These are **post-exposure corrections to the evaluation method**; they do not convert the original prospective failure into a pass. The original script `scripts/evaluate_p16_b5_source_gate.py`, fourth source receipt `B5_FOURTH_FROZEN_PROSPECTIVE_SOURCE_GATE_RESULT.json`, B2v4 and B2v5 code/scorecard are all preserved byte-for-byte.

## 2. What remains a real semantic defect

The frozen B2v4 still loses heading context and contaminates later items with an earlier section's category. Real source statements on qualifications, behavior and scheduling were originally called `context`, `work_duty` or `candidate_qualification` incorrectly. The corrected evaluator retains **12 material category mismatches** on B2v4's selected fourth-cohort assertions even after removing the two spurious hard-stop findings.

Categories are **not** independent hard obligations. A behavioral trait can also be a broad applicant qualification; when it is visible and not strengthened to `required`, the calibrated score labels that a **compatible broad qualification**, not a source-truth failure. This does not mean genuine applicant requirements may disappear into generic context, nor that working hours become hard technical skills. Explicit duties, invented requiredness, original source identity and proven OR requirements remain strict.

The parser's real remaining false-heading issue was separately addressed in a new, opt-in `B2v6` candidate:

- Retains all existing B2v5 source SHA, offset, item and authority boundaries.
- Corrects an already-exposed, explicitly phrased teamwork/responsibility trait from an inherited technical-qualification category to `behavioral_expectation` **without requiring paid prior experience**.
- Recovers previously skipped source-DOM list bullets only as **`unresolved` exact-source candidates**. They are never silently promoted as required qualifications, eligibility ORs, accepted benefits or facts.
- Does not add new per-vacancy regex patches, replace v30/v9, claim independent semantic understanding, or write production data.

## 3. Exact fourth-cohort post-exposure comparison

The versioned recalibrator checks the same eight original descriptions, 80 original-source assistant-selected assertions and 73 type-comparable assertions under the **same corrected method**:

| Selected original-source check | Frozen B2v4 rescored | B2v5 exposed | B2v6 exposed |
| --- | ---: | ---: | ---: |
| Strict category role matches | 57/73 | 72/73 | 73/73 |
| Broad compatible qualifications, scored separately | 1 | 1 | 0 |
| Material wrong categories | 12 | 0 | 0 |
| Genuinely missed explicit-duty assertions | 0 | 0 | 0 |
| Explicit employer eligibility OR scopes missing | 0 | 0 | 0 |
| Illustrative options (never formal eligibility authority) | 4 | 4 | 4 |
| Not fully source-covered selected assertions | 4 | 1 | 0 |
| Optional/negative wording upgraded to required | 0 | 0 | 0 |

The one previously mis-scored duty is shown separately as a cross-item source span, not omitted. Four illustrative alternatives have no mandatory DAG status. All values are **selected diagnostic assertions**, not whole-ad accuracy or proof of market-scale generalization.

The original B2v4 prospective record still reports one missed duty and one missing alternative **under the old evaluator**. That report and its original integrity-replay script must continue to reproduce exactly; do not rewrite its historical verdict.

## 4. Broader non-regression across all four EXPOSED cohorts

| Exposed cohort | B2v6 strict role matches | Material category errors | Unreviewed alternative meaning | Missing explicit duties |
| --- | ---: | ---: | ---: | ---: |
| First | 83/86 | 1 | 3 | 0 |
| Second | 84/85 | 0 | 4 | 0 |
| Third | 78/78 | 0 | 4 | 0 |
| Fourth | 73/73 | 0 | 0 | 0 |

All **32 B1 original-source design/validation bundles** passed. However, the first cohort still contains a material category error and source items absent from some selected review spans; the second has missing/uncertain noncritical source coverage, and earlier cohorts have alternatives whose specific formal eligibility semantics were never established. Unknowns are explicitly **incomplete review**, not artificially promoted as verified OR graphs.

This result is bounded **regression engineering**. Four previously exposed samples do not support independent prospective B5 acceptance. The review labels were written by an assistant, not an independent blinded human assessor; the selected assertions are nonexhaustive. The new candidate was created after observing these examples.

## 5. Implementation and reproducible checks

- Original fourth frozen evidence: `scripts/verify_p16_b5_fourth_source_gate.py` — original expected FAILED result intact.
- New pure calibrated scorer: `src/jobhunter/source_gate_evaluation_v2.py` — byte-identical source assertions, multi-item duty coverage, locally anchored choices, source-role compatible/critical distinctions and mandatory-strength safeguards.
- New opt-in candidate: `src/jobhunter/source_item_candidate_b2_v6_dom.py` — preserves B2v5 and accepted runtime.
- New read-only fourth source replay: `scripts/verify_p16_b5_fourth_calibrated_gate.py`. This first runs the old immutable verification, checks old code hashes, compares B2v4/v5/v6 under one new method, and validates the eight B1 bundles. `--write-once` sealed the ignored private task diagnostics and tracked source-safe scorecard; subsequent invocations only verify identity.
- Source-safe aggregate/checksum scorecard: `docs/working-memory/2026-11-22_p16_b5_calibrated/SAFE_EXPOSED_SOURCE_GATE_CALIBRATION.json`.
- Synthetic adversarial and optional private multi-cohort regression tests: `tests/test_source_gate_evaluation_v2.py` (including nonwhitespace-gap rejection, exact source quote hash mismatch, illustrative examples, unrelated OR graphs, optionality and source-DOM unclassified evidence).

No local LLM requests, additional advertisements, new translation, accepted employer facts, schema migration or production route were involved. Private original employer text, local raw HTML and full review diagnostics remain ignored.

## 6. What is and is not finished

**Finished:** Engineering correction of the known misleading evaluation criteria; a separate read-only, inspectable fourth-cohort re-score; a source-exact B2v6 exploratory candidate with regression evidence and explicit uncertainty; immutable original failure preserved.

**Not finished:** Full source-semantic generalization; exhaustive employer-fact recall; independent review of ambiguous OR semantics in earlier cohorts; validating a compact user-facing B4v6 against real decisions, reading effort and a genuinely comparable accepted baseline; B5 acceptance; B6 rollback-controlled production routing.

**Next responsible steps:** Freeze the revised evaluation methodology **before** collecting another unseen sample; require granular duty annotations, distinguish illustrative examples from explicit eligibility disjunctions, validate source-scope locality, and separate soft taxonomy disagreements from harmful mandatory/eligibility errors. Pair this with the planned **B4v6 decision-question-first usability experiment** on exposed ads. Do not consume another purported blind cohort merely to chase a perfect source-role percentage. A subsequent B5 attempt must use genuinely untouched sources, independent or appropriately isolated review, bounded translation/analysis costs and a qualified same-source baseline where available. B6 requires its own explicit promotion and rollback gate.
