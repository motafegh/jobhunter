# P1.6 Stage B5 — fourth prospective failure, B2v5 exposed-only repair, and utility-first next gate

**Decision date:** 2026-11-22
**Execution:** `main`, local-only original-source evidence; no provider or network calls during replay
**Disposition:** **FOURTH B5 PROSPECTIVE SOURCE GATE FAILED**. B2v5 passes a bounded **exposed-regression engineering** check, **not** independent semantic acceptance. **B6 remains CLOSED.**

## 1. What was frozen and actually tested

At the pre-source `f2e396a` commit, B2v4 was selected and its exact source SHA frozen **before** original descriptions were acquired for the fourth cohort. The separate metadata selection excluded the previously consumed B0 index, public corpus, earlier three B5 primary and reserve sources, and company/repost overlap. Eight original Jobinja descriptions were fetched through the existing approved adapter, verified against raw-HTML and parsed-source SHA receipts, and stored in an isolated eight-job SQLite snapshot.

An assistant source-only assessment sealed 76 selected original-source assertions before seeing candidate output; a second source-only explicit-alternatives supplement sealed four assertions **before** the first candidate comparison. This gives 80 original-first assertions (73 role-comparable). This is **not** a complete inventory, independence from all prior assistant knowledge, or certified blind human assessment. The selected employer evidence, reviews and model-free comparison remain private and Git-ignored.

The unchanged B2v4 candidate failed on its **first prospective** comparison:

| Selected source-first measure | Frozen fourth B2v4 |
| --- | ---: |
| Original assertions | 80 |
| Role-comparable assertions | 73 |
| Correctly matched role assertions | 56 |
| Wrong-role assertions | 13 |
| Missed explicit duties | 1 |
| False optional/negative-to-required assertions | 0 |
| Jobs with missing explicit alternatives | 1 |
| Jobs with structural/category gaps | 4 of 8 |

Role matches/mismatches do not necessarily sum to the comparable denominator because some spans are not contained in a comparable candidate. **Do not convert the table to full-ad semantic accuracy percentages.** The same-source parser and source identity are mechanical prerequisites, not proof of semantic meaning. One missed duty and one missing alternative are sufficient for an upstream stop.

No B3 translation, B4 candidate output, unchanged English v30, or original-language v9 paired interpretation was requested for this cohort. No new accepted employer facts, production routing, downstream reuse, application SQLite mutation or public corpus update occurred. **These eight jobs are now EXPOSED and cannot be presented again as independent B5 evidence.**

The new read-only `scripts/verify_p16_b5_fourth_source_gate.py` replays the immutable metadata/source-review/candidate sequence and checks the frozen B2v4 SHA, raw and parsed source identities, production/public-corpus hashes, exact previously failed result and explicit non-promotion. Its successful status means **failure evidence faithfully replayed**, not B5 passed.

## 2. Separate B2v5 repair, after exposure — candidate-only

After the fourth failed result was sealed, a new `src/jobhunter/source_item_candidate_b2_v5_dom.py` was built on top of B2v4; it does **not** modify B2v4, the original description parser, v30/v9, B3/B4 contracts, or accepted history. It uses source-DOM block/heading evidence and exact original anchors to recover some unrecognized qualification, behavioral, and working-condition scopes. It refuses mismatched raw source HTML and leaves unproved alternatives as **unresolved** rather than manufacturing an eligibility DAG. Existing exact source IDs and preserved v4 duties remain authoritative for this diagnostic layer only.

A narrow explicit modality safeguard prevents an inferred minimum-years qualification from overriding source wording that marks the statement **preferred**, **optional**, or **not required**; no generic assertion of employer-required prior professional experience is created from a work assignment. Synthetic counterexamples cover source SHA mismatch, role/qualification separation, preferred wording, technical examples, case variation, and B1 candidate validation.

B2v5 was compared **only against the four already exposed source-first reviews**. No new pages were acquired, no local LLM called and no post-hoc change made to any frozen source-review assertions.

| Already-exposed cohort | Role-comparable anchors | B2v4 matched | B2v5 matched | B2v5 role mismatches | B2v5 missed duties | B2v5 missing alternative jobs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| First | 86 | 80 | 83 | 1 | 0 | 0 |
| Second | 85 | 83 | 84 | 0 | 0 | 0 |
| Third | 78 | 77 | 78 | 0 | 0 | 0 |
| Fourth | 73 | 56 | 71 | 1 | **1** | **1** |

Zero false-required assertions were observed on these *selected* checks. **All 32 B1 candidate bundles validated**. The retrospective improvements are real for the selected frozen anchor comparison, but are **not** evidence of unseen generalization, exhaustive employer-claim recall or measured user usefulness. In particular, B2v5 remains incomplete on the fourth cohort. Do not erase, patch or rename the originally failed B2v4 result.

## 3. Engineering and evidence boundaries

- Public-safe aggregate counts and source/code/DB hashes: `docs/working-memory/2026-11-22_p16_b5_fourth/SAFE_FOURTH_B5_FAILURE_AND_B2V5_EXPOSED.json`.
- Private original documents and immutable reviewer verdicts: ignored `data/local-acceptance/p16-stage-b5-2026-11-22/fourth-source-cohort-v1/`.
- Executable fourth-cohort source gate replay: `scripts/verify_p16_b5_fourth_source_gate.py`.
- Versioned non-production candidate and synthetic/private regression tests: `src/jobhunter/source_item_candidate_b2_v5_dom.py` and `tests/test_source_item_candidate_b2_v5_dom.py`.
- All four previously exposed original-source cohorts retain historical v2/v3/v4 findings; `f2e396a` remains the prior prospective B2v4 freeze.
- The tracked document and scorecard intentionally contain no exact employer prose, listing IDs, source URLs, local absolute paths or model payloads.

## 4. Architecture decision: stop the endless heading-patch loop

Four separate fresh original-source experiments have now stopped at the source gate. B2v2, B2v3, B2v4 and B2v5 gains measured **after** viewing previous cohorts are useful regression engineering, but source-role micro-rules alone have not demonstrated dependable generalization. The original Jobinja HTML/DOM is clearly valuable *evidence*; it is not always a sufficient semantic interpreter.

**Decision:** Keep DOM/source offsets, SHA, provenance, version checks, alternative-source spans and bookkeeping deterministic. Treat ambiguous duties, qualifications and alternative meanings as semantics: preserve exact original scope, a conservative non-authoritative category or explicit unresolved state, and optionally test bounded local-model assistance in a separately versioned research candidate. Never replace uncertainty with mandatory requirements, never let a model's valid citation certify its claim, and do not make per-posting keyword fixes. The prior three-case exposed model-item relabeling pilot performed worse than deterministic B2v3 on selected checks; that rejects automatic wholesale model relabeling, **not** all targeted model reasoning.

**No fifth blind cohort is authorized by this record.** Running another before choosing and freezing a materially different, assessed design would only continue the same sample-consumption cycle. Conversely, previous failures do not imply that source-labeled, partially uncertain job briefs are useless: they may already help a person decide whether to read/apply without qualifying as accepted market facts.

## 5. Next actual product gate — bounded usefulness, not automatic promotion

Use only **already exposed jobs** for a separately preregistered, read-only product comparison. Do not rename it B5 unseen acceptance. Freeze a small heterogeneous sample and the current `B4v5` source-qualified brief, compare with unchanged v30/v9 *where runnable* using identical frozen sources. Explicitly include v30 unavailable/failed/abstained outcomes as observed states rather than assuming missing facts. This is a **development usefulness trial**, not a request to regenerate accepted v30 or to promote B2v5.

Evaluate per source-anchored decision instead of measuring mere JSON compliance:

1. **Source truth:** unsupported mandatory claims, missed explicit actions, alternatives, optionality, negative constraints, wrongly sourced arrangements, omissions or translation drift.
2. **Useful interpretation:** can a user understand the role purpose, actual work, qualifications, required-versus-advantage distinctions and key uncertainty; is the result more useful than reading the source?
3. **Cost/coverage:** original items visible, source links intact, partial/fail-soft handling, local requests, observed time/tokens where actually measured, abstentions/unknowns and human inspection effort. Neither counted model output nor deterministic coverage alone equals usefulness.
4. **Blast radius:** any candidate-only source-qualified first view must stay out of accepted P1.6, Capability, Work, Registry and Market; keep real model hallucination and unverified semantic links plainly labeled.

A short independent or appropriately isolated reviewer study can strengthen usefulness evidence; if only the same assistant reviews it, record non-independence. A later **new** B5 promotion attempt requires a chosen frozen design, genuine untouched cohort, original-first assessment, independent translation and paired-analysis budgets, and the predeclared critical stop rules. B6 remains a separate rollback-reviewed decision.

## 6. Verification and closure standard

**Local result (2026-11-22):** 1,219 warnings-as-errors tests passed; 31 focused B2v4/B2v5 tests passed; original fourth source-gate failure replay passed; Ruff lint/format, pip consistency, JSON validity and whitespace checks passed. The production DB and public corpus SHA-256 values match the frozen pre-fourth manifest. GitHub CI on the published commit must be checked independently.

Before publishing this milestone on `main`: run the original fourth evidence replay, B2v5 and B2v4 synthetic/private regression suite, warnings-as-errors full suite, Ruff, dependency consistency, diff checks, local database/public corpus SHA comparison, then check GitHub Actions on the exact pushed commit. **Tests passing means engineering safety on the evaluated scope; B5 remains NOT ESTABLISHED.**

**Outcome:** Fourth genuine B5 source-semantic FAIL honestly preserved; B2v5 exposed-only engineering improvements measured; production remains on English v30/v5 and original v9/v4; future work is utility-first and bounded rather than another automatic acquisition cycle.
