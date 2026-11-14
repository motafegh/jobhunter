# P1.6 Stage B0 — frozen baseline, reference rubric and unseen-cohort protocol

**Date:** 2026-11-14
**Status:** B0 baseline captured and verified; **B0 PASS for baseline/protocol only**. B1 contract design is next.
**Control:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md` §B0
**Baseline repository commit:** `c3a4d1bf060dd3c8a1ba44a75a9c93940d3a1f68`
**Execution branch:** `work/p16-stage-b0-baseline-evaluation-2026-11-14`
**Safe machine record:** `docs/working-memory/2026-11-14_p16_b0/SAFE_BASELINE_METRICS.json`
**Selection/scoring contract:** `docs/working-memory/2026-11-14_p16_b0/EVALUATION_PROTOCOL.json`
**Private original evidence:** ignored `data/local-acceptance/p16-stage-b0-2026-11-14/`; this location MUST NOT be committed or exported to public corpus.

## 1. The B0 decision

B0 is complete **as a read-only source/evaluation baseline**, not as a generated bilingual interpretation, independent accuracy evaluation, or new semantic promotion. The baseline was frozen from the configured application database and the separately retained exposed A1/v31 research databases. **No** job acquisition, provider inference, prompt, schema, migration, public analyzer, or accepted P1.6/Capability/Work/Registry/Market state changed. The local configured database file SHA-256 remained byte-identical during the operation, and exact source hashes were checked.

B0 closes the specific moving-baseline risk. It does **not** assert that a 6–8 job unseen cohort already exists; that is still a **B5 evaluation prerequisite**. B0 freezes selection rules, evaluation measures and the previous-exposure exclusion index before B1–B4 implementation can bias selection.

## 2. Exact accepted/current repository state frozen

| Component or evidence | Verified B0 baseline |
| --- | --- |
| Git main baseline | `c3a4d1bf060dd3c8a1ba44a75a9c93940d3a1f68` |
| Source parser | `jobinja-detail-v2` |
| Translation schema | `english-projection-v2`; translations have field association, **not** per-item original alignment |
| English P1.6 public generation | `job-analysis-english-v30 / job-analysis-v5` |
| Original-language P1.6 public generation | `job-analysis-original-v9 / job-analysis-v4` |
| Passive source anchor | `jobhunter-source-span-identity-v1`, original description only |
| Accepted historical English P1.6 anchors | `tG9K=36`, `t4jp=37`, `tmBK=39`, `t4qV=44`, `tmyX=46` |
| Corresponding accepted Capability v9 artifacts | `11, 12, 13, 14, 15` respectively |
| Current snapshot and report | Market snapshot `15`; report `2` latest review `accepted_for_bounded_use` |
| Source corpus in configured local DB | 420 logical posting IDs; 57 *source detail versions* (not 57 distinct current vacancies); 49 translation artifacts |
| Historical analysis artifact table | 47 artifacts total; 46 stored `accepted` across **historical** prompt versions; do **not** confuse with 11 public-corpus accepted/current English artifacts |
| Other historical persisted table rows | 15 Capability; 13 Work; 10 canonical concepts; 18 claim mappings; 15 snapshots; 2 role-family reports |
| Source/raw integrity | All **9 of 9** selected exposed/anchor original HTML files SHA-256 verified against stored raw evidence identities |
| Database integrity | Production and both exposed SQLite snapshots: `integrity_check=ok`; `foreign_key_check=[]` |

Artifact identities, source semantic SHAs, translation hashes, model/prompt/schema identities, JSON hashes, and the reviewed-state boundary are frozen in safe machine-readable metadata. The original old accepted `v20/v5` English anchor artifacts are deliberately compatibility-current; the fact that **new** analysis uses v30 is not permission to regenerate them.

### Private backup/provenance boundary

Three **online SQLite** backups passed integrity/FK checks and are stored only in the ignored B0 workspace:

- Configured local DB snapshot SHA-256: `693c054338cdd2a4e6652f3d78129d24b4ae6c29ac7c`.
- Exposed original A1 DB snapshot SHA-256: `bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`.
- Exposed v31 trial DB snapshot SHA-256: `e66c0e67c40cad5695ff3d5a7aa1cf912ea4f7859809904c18d5edffe6bec790`.

The configured DB file before/after SHA-256 is `d9068fcb503860638cb2187b537e57151bea0192ff69ab7dbe381c84fb2353d8`.

Separately, B0 copied **9 source HTML files, 9 fetch metadata files, and 5 private review/seal files** with independent content hashes to the ignored workspace. The additional private retention manifest SHA-256 is `64bf63a14f8be2a091637505ade15de46db676689c9ff71b0eb24f957840304f`. All full source text and owner review payloads remain **private**; Git records only hashes, counts, reviewed-state labels and accepted artifact IDs.

*Reproducibility limit:* runtime paths, source pages and local LM Studio history are private, potentially ephemeral, and not guaranteed to exist on a clean clone. A clean clone can inspect the public safe evidence and assertions but cannot reconstruct private employer text from hashes alone. Preserve the B0 ignored directory with any future backup/recovery operation.

## 3. Frozen exposed diagnostic reference rubric (no independent holdout claim)

**Source of truth:** retained original employer description, not translation, not a model candidate and not Jobinja skill-tag assumptions. The assistant source-only A1 interpretations (59 anchored statements) are labeled **assistant-reviewed, prior-context-exposed**, never independently blind/human-accepted.

| Case | Concrete expected fact boundaries for B2–B4 regression | Unknown or withheld |
| --- | --- | --- |
| `tNhZ` (Python/AI trading product) | Six explicit work duties; good Python/backend qualification; prior LLM/financial-market/backtesting familiarity explicitly optional; part-time OR full-time by agreement, remote and negotiable salary; GitHub sample optional application material; board-required-like `LLM` tag must not override employer source | Exact prior-experience years and technology stack |
| `tMps` (enterprise applied AI) | Explicit duties and required vector-search/reranking/context-management awareness; Middle **OR** Senior eligibility, AND within each path, **one of** listed Middle domains; full-time/hybrid arrangements; tools under advantages remain preferred | Whether any named preferred tool is universally indispensable |
| `tNDx` (EDR support) | Five direct duties including implementation/configuration/support; 3 years continuous experience; Network+/Security+ **certificate OR equivalent knowledge**; teamwork explicitly preferred (historic false reading corrected); entrance exam for hiring; board versus prose salary conflict distinct | Kaspersky specialist certificate strength, large-government-client experience strength, employee work-from-home status |
| `tMjm` (penetration testing) | Skills and abilities explicitly described; do **not** invent a day-to-day duty list from applicant abilities; remote option is employment arrangement, not required skill; conscientiousness not “identification of duties”; 30–50m toman range | Targets, specific mandatory tools, precise remote-work conditions |

For each, B0 retains original source SHA, HTML evidence SHA, source-version identity and full review source-anchor IDs privately. Existing `ASSISTANT_PASS_A_SOURCE_REVIEW.json` is the frozen source-first assistant reference, and `ASSISTANT_PASS_B_SOURCE_MODEL_RECONCILIATION.json` the separately frozen prior-model comparison. They are **not** authoritative corrected employer artifacts; discrepancies must be adjudicated against the original text, not overfitted to assistant annotations. All four cases are **exposed**; no accuracy/generalization score is derived from them.

### Regression protection: five accepted historical anchors

`tG9K` / `t4jp` / `tmBK` / `t4qV` / `tmyX` have accepted English P1.6 artifact IDs `36/37/39/44/46`, exactly paired with Capability IDs `11/12/13/14/15`, source semantic SHAs, translation artifacts and original HTML content hashes. All five were verified against the current configured database and are frozen in machine-readable metadata.

**Regression checks:** source versions remain current; no accepted ID/model/prompt/schema/dependency changes; no automatic recomputation; no new pending or rejected candidate silently becomes accepted; Work/Capability/Registry/Market unaffected; legacy English v2 item alignment still unknown. These are backward-compatibility anchors, **not** a B5 unseen test set.

## 4. Predeclared unseen-cohort selection protocol (capture NOT performed)

**Target:** 6–8 genuinely new, distinct publicly available employer postings, selected **only after B0**, using approved Jobinja source acquisition and normal access rules; no site bypass, browser challenge evasion or implicit second source adapter. Prioritize direct source capture and source metadata rather than purported posting freshness.

**Exclusion set:** B0 scanned **45 local SQLite datasets** with `job_postings`, collecting **485 unique known job IDs**. The newline-delimited sorted exclusion index is retained privately, SHA-256 `71c957c30f1d1229aa80bcee9dfac124e9c81f890d492893a1ed9c85a6201e08`. **This index is not exhaustive**: before selection, also exclude source jobs referenced by repository public corpus, experiment/research branches, previous manual evaluations, duplicate URLs/employer-repost identities and any case already viewed by the evaluating assistant. Neither a different posting ID nor a changed scrape timestamp makes a known ad unseen.

**Selection procedure:**

1. Record source-access status, acquisition terms, limits, 200/challenge/rate-limit response classes, date/time and URLs without inventing posting dates. If access is restricted, stop normally.
2. Fix quotas **before viewing candidate analysis**: at least two software/Python/backend cases, two applied-AI/LLM/RAG cases, and two cyber/network/security cases when available. Aim for one sparse/low-structure example and one native-English example *if the supported source supplies them*. These can overlap the three base strata; do not add artificial sources to hit a quota.
3. Classify/select initially by title, board category and visible source metadata. Preserve complete candidate-pool order/eligibility/exclusion reasons (so a favorable result cannot be cherry-picked). Use unique employer/source identity and avoid duplicates/identical reposts.
4. Fetch the chosen original detail pages through the approved adapter, record exact time and response/provenance. Verify raw HTML and parsed source field hashes. Freeze the complete list of selected IDs, original-source snapshots and selection decisions **before any candidate analysis/model output is seen**.
5. Perform a source-only original-language reading, record evidence references, uncertainty and reviewer exposure, and freeze that judgment separately before comparing model results. The assistant may carry general research context; label it `source_first_assistant_assessment`, **not** blind independent human verification. Use separately isolated reviewer evidence if a later promotion decision needs stronger independence.
6. Run the unchanged v30 baseline and the single selected Stage B candidate against the same frozen source/projection dependencies in isolated copies. For a case lacking a valid English projection, label that limitation rather than fabricating equivalence.
7. Reveal/summarize only after original-source review freeze, score once, and mark the tested cohort **exposed thereafter**. If any critical defect requires repair, use other **newly acquired** sources for a subsequent fresh evaluation, not the failed group again.

A source captured on November 14 is *newly captured*, not automatically *newly posted*. If 6–8 eligible new postings cannot be obtained, B5 is **NOT ESTABLISHED** and B6 production promotion remains blocked; maintain a useful isolated candidate without falsifying the validation sample.

## 5. Predeclared scorecard and evaluation logic

Unit of truth: **job × source statement × claimed category/strength**, with alternative-group relations and model-availability states evaluated separately. The private source-only rubric defines the denominator after evidence capture, never from the model's predictions.

Per job record at minimum: source/parsing validity; original source statement count and evidence identity; explicit duties (identified/correctly recovered/omitted/fabricated); explicit qualifications and strength (supported/wrong/unknown); alternative AND/OR logic; work arrangements misclassified as skills; board metadata conflicts; translation negative/optional/years/heading fidelity; full/partial/no candidate outcome; schema/transport/timeout failures; exact source/translation/analysis identity; provider model, retry count, elapsed time and token use when available.

**Critical promotion blockers:** source identity mismatch or invented evidence; unsupported mandatory qualification; required/preferred reversal; incorrect OR/AND collapsing into mandatory eligibility; missing/changed original text during translation used as fact; fabricated explicit work; privacy leakage; unsafe old-artifact currentness; altered Market denominators. The absence of a model-generated candidate is a coverage/availability failure, **not** evidence that the employer said nothing. Source ambiguity, optional inference depth and noncritical missing details may remain explicit `unresolved` in an honestly labeled candidate view.

**Reporting:** publish per-case denominators and event types, not a fictitious cross-market success percentage. A failure in one critical dimension blocks promotion even if most other items score well. Compare candidate usefulness to unchanged v30 on specific same-source questions, not solely schema-validity or model fluency. No owner-time savings claim without observed measurement.

## 6. Predeclared model/resource ceiling

B0 itself used **0 local model calls and 0 new external source requests**.

All later experiments must use configured local provider scope (`127.0.0.1:18080/v1`, configured analysis model `gemma-4-e4b-it-ud`, translation `gemma-4-e2b-it`) unless a separately recorded model choice is justified. Current settings at B0: inference transport timeout `30` seconds, `1` retry, analysis max `8192` output tokens, translation max `4096` output tokens, translation character target `6000`. Do **not** reinterpret a transport timeout as a guarantee of total model runtime or enforce an arbitrarily short reasoning cutoff.

**Initial ceilings to avoid endless prompt/version churn:** B1 design and B2 deterministic candidate tests use zero model calls by default. B3 may issue up to 64 source-bound item-generation requests for the **exposed development cohort**, B4 up to 40 candidate/baseline analysis requests, and B5 up to 80 candidate/baseline requests across 6–8 new frozen cases. Each slice starts with **one** primary candidate design and permits at most **one** evidence-justified corrective candidate before root-cause/stop review; do not automatically exhaust call ceilings. Reserve a measured operational per-request wall ceiling of 15 minutes for **evaluation orchestration only**, with explicit failure capture and checkpointing; keep model/provider transport and legitimate post-connect generation semantics distinct. Cap active model experiment wall time per B3/B4 slice to 3 hours and B5 to 6 hours before a documented stop/rebudget decision. These are **engineering budgets, not predictions**.

No cross-source calls, cloud inference, historical mass regeneration or new expensive model comparison is authorized by B0. Log request count, failures, retries, model identity, source SHA, output schema, elapsed time and observed tokens; do not infer absent token counts.

## 7. B0 gate verdict, known limitations and B1 handoff

**B0: PASS (baseline and evaluation protocol).** Criteria met: healthy, source-exact configured database and frozen private backups; four exposed source cases with 59 verified anchored review statements; five accepted artifact/capability pairs with source/translation/content identities; nine raw original HTML files hash-verified and privately retained; 485 known IDs recorded for holdout exclusion; explicit fresh-source selection/independent-review/scoring protocol; bounded model-call budget and owner-review policy; **no** new job/model calls and **no** accepted-state mutation.

**Not yet proven:** source/metadata authority semantics, per-item bilingual fidelity, useful new candidate behavior, 6–8 actually unseen cases, generalized accuracy, independent human source certification, production route/migration/rollback. These are B1–B6 gates.

**Next: B1 contract/ADR** on a separate branch from the current main. Resolve the source item and structured-field anchor identity, exact clause splits, one-to-many translation links, alternative eligibility representation, review state transitions, source/board authority ledger and candidate-vs-durable read rules. Demonstrate contract examples against the frozen A1 cases; do not run a new model, activate experimental research code, or change public P1.6 in B1 without its own decision.
