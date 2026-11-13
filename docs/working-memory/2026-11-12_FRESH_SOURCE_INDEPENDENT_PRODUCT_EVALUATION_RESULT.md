# Fresh Jobinja Cohort — Independent JobHunter Product Evaluation

**Date:** 2026-11-12
**Status:** COMPLETED DIAGNOSTIC / NOT A PRODUCT-QUALITY PASS / MAIN UNCHANGED
**Branch:** `evaluation/current-real-ads-2026-11-12`
**Product baseline:** `main` at `74ffec25533c5cd4b1afa90b0c3bc76ee023e7aa`
**Method:** `2026-11-12_FRESH_SOURCE_COHORT_INDEPENDENT_ANALYSIS_PROTOCOL.md`

**Source-interpretation correction (2026-11-13):** The original Persian tNDx statement says teamwork and accepting a defined management structure are an ADVANTAGE (`مزیت محسوب می‌شود`), not mandatory. The earlier Section 3 assertions that teamwork was required and the original-language model wrongly marked it preferred are superseded. See `2026-11-13_EDR_TEAMWORK_SOURCE_INTERPRETATION_ERRATUM.md`. Frozen original review notes and JSON remain unchanged as historical evidence. No P1.6 candidate or downstream result is newly approved.


## 1. Decision summary

JobHunter can now acquire live Jobinja search and individual vacancy pages, preserve immutable original source evidence and complete local English translation. **The acquisition issue has been resolved.** The next material reliability bottleneck is **P1.6 semantic extraction**, not adding another market source or polishing the comparison UI.

On five deliberately varied, newly acquired real public vacancy snapshots, standard English P1.6 produced one structurally valid candidate and four validation failures. Independent review rejected the one generated candidate for a real source-category error. Consequently **zero of five were approved for Work/Capability Intelligence**; none was promoted to production or used as reliable market demand.

The cohort is exposed development evidence, not a protected holdout, unbiased sampling, or an estimate of how often JobHunter fails in the market. This is nevertheless sufficient to **change our immediate engineering priorities**.

## 2. Product-first test and controls

Four bounded, declared source searches were used: Persian AI, RAG, Persian cybersecurity, Python. All four search pages returned HTTP 200, delivering **71 distinct public job IDs** in a clean isolated database with no source failure. Five preselected postings each returned HTTP 200 and `parsed`; original HTML SHA-256 was checked against persisted evidence.

The identical configured JobHunter translation pipeline (`gemma-4-e2b-it` via `http://127.0.0.1:18080/v1`) completed all five. The normal English P1.6 pipeline (`gemma-4-e4b-it-ud`, `job-analysis-english-v30` / `job-analysis-v5`) was then invoked once per case, with its built-in retries, source/response evidence, and runtime result preserved. No model was changed, no manual corrective prompt was substituted, and no invalid result was autoaccepted.

For **each job**, the native P1.6 terminal outcome and artifact/log hash were sealed before independently opening the original public URL. Each direct URL independently returned HTTP 200. Full HTML bytes varied between accesses (dynamic site HTML), but the original JSON-LD **title, description, datePosted, and employmentType matched** the preserved acquisition snapshot for all five. Source-only checklists were written and SHA-256 locked before unblinding the generated claim contents or validation details.

The independent assessor was this assistant reading the original source directly, not a second human evaluator or a protected blind reviewer. All original/translation/model text and full source notes remain private to the ignored local evaluation directory. Repository-visible material is restricted to original public URLs/hashes, diagnostics, case classifications and source-review hashes.

### Results

| Native gate | Outcome |
| --- | ---: |
| New-to-this-run unique job links | 71 |
| Search HTTP 200 | 4 / 4 |
| Five selected source pages HTTP 200 / parsed / SHA verified | 5 / 5 |
| Native English translation completed | 5 / 5 |
| Standard English P1.6 invoked | 5 / 5 |
| Standard English P1.6 fail-closed validation | 4 / 5 |
| Structurally valid English P1.6 candidate | 1 / 5 |
| English candidate rejected in independent source review | 1 / 1 |
| English P1.6 cases approved for downstream Work/Capability | **0 / 5** |
| P1.6 semantic artifacts accepted into live database | 0 |
| Actual Work v2 / Capability v9 run for this new cohort | 0 (correctly gated) |

**Publication-date and prior-seen corrections:** These source versions were *acquired into a new isolated database* on November 12. Their original structured `datePosted` values are September 30, October 1, October 18, October 24 and October 25, 2026. Four of the five selected public IDs were absent from the historical live JobHunter database. The fifth, `tNhZ`, had already been seen there in September 2026, but this run acquired a newly inspected source version with no prior P1.6 analysis for that version. A site's `datePosted` is not proof of true first publication; these pages were merely demonstrably live/readable at evaluation time.

## 3. Independent source-by-source verdicts

### `tNhZ` — LLM headline versus Python-fintech backend body

- **Source meaning:** The page headline emphasizes an AI/LLM engineer, but the actual job description primarily seeks a Python backend developer implementing trading/backtest services, APIs, data processing, and participating in selected AI/LLM development. Familiarity with financial markets, backtesting and LLMs is explicitly beneficial, **not mandatory**. A conditional invitation to include GitHub/portfolio examples does not make a portfolio a technical qualification.
- **JobHunter:** Native English P1.6 terminated after two attempts. Its last validation failure was a *preferred item lacking exact source preference* triggered by the conditional GitHub/portfolio wording.
- **Verdict:** Correct fail-closed validation, but severe downstream coverage loss. Required/preferred qualifiers and non-qualification application instructions need source-specific handling. A title alone cannot define job capability authority.

### `tMps` — Applied AI with distinct Middle and Senior eligibility

- **Source meaning:** Direct enterprise LLM/RAG/agent work and deployment are clear. Middle eligibility permits **2–4 relevant years, at least one of several AI domains, and one practical project**. Senior eligibility describes **4–7 years** and successful production system design/deployment. Familiarity with a long tool/security/observability catalog is expressly advantageous; not all named products are mandatory.
- **JobHunter:** English P1.6 exhausted native validation on multiple qualifications incorrectly given a preferred classification while encoding the tiered experience/project statements.
- **Verdict:** Safe rejection, but failure to represent genuine alternative eligibility tracks. A single `required/preferred` label for a compound statement is not sufficient for this source.

### `tMqd` — AI/Python backend with optional LLM experience

- **Source meaning:** Direct work includes Python backend and API engineering, AI/ML integration, data/model inference, performance/architecture and maintainable tested code. Strong Python and practical backend experience are required. Specific backend frameworks are examples; LLM frameworks, vector DBs, AI agents, async and high-traffic experience are **bonus** qualifications.
- **JobHunter:** Native P1.6 failed exact-source coverage because a source span describing independent communication and code quality was improperly associated with the adjacent advantageous LLM/agent experience.
- **Verdict:** Fail-closed rather than persisting a mixed claim; source-section/provenance segmentation and translation-to-claim linkage need attention.

### `tNDx` — EDR support role, English versus original P1.6 diagnostic

- **Source meaning:** Five direct duties concern Kaspersky/other vendor EDR deployment, setup/support, enterprise troubleshooting, technical customer interaction and documentation/reporting. Requirements include 3+ years in IT/network security, Network+/Security+ certificate **or equivalent knowledge**, Windows Server/VMware familiarity, independent judgment and teamwork. Specialized Kaspersky certificates and government/large-client experience are merely preferred.
- **Standard English P1.6:** Returned an empty claim structure for an information-rich source. The validator rejected it after the native retry limit. The stored English translation **does contain** the five duties and qualification text, though some source headings/sections are flattened or concatenated.
- **Controlled original-language diagnostic:** Running the independently supported `--mode original` against the same source with the same model—but **different language, prompt and schema** (`job-analysis-original-v9` / `job-analysis-v4`) completed in 42 seconds, yielding four `responsibilities`, eight `requirements`, one `role_purpose`; it stored `semantic_review_status=accepted`.
- **Independent review of that original result:** The most important EDR deployment/configuration/support duty was misplaced under `role_purpose`, an actually required teamwork item was misclassified as preferred due to an adjacent heading, and preferred specialized Kaspersky certifications were omitted. Structured and narrative experience ranges were duplicated without a nonindependence warning.
- **Verdict:** A successful model response and stored accepted state **do not establish correct semantic review**. Original-mode output is **not** a safe alternative for the failed current English P1.6 contract. The contrast justifies testing the English source representation, model prompt and schema **separately**; it does not prove translation alone caused the failure.

### `tMjm` — Penetration-testing qualifications versus direct work

- **Source meaning:** The advertisement lists web/network penetration-test competencies, OWASP-related familiarity, vulnerability identification/reporting, remediation advice, technical documentation and teamwork chiefly under **technical conditions/abilities**. It does not clearly separate concrete assigned-duty bullets. Source-side minimum professional years are not specified; remote work is a **possibility**, not an applicant requirement.
- **JobHunter:** Standard English P1.6 passed structural validation with **20 requirements, zero responsibilities and zero explicit role-purpose items**. Preserving zero direct responsibilities is a legitimate conservative choice. However, it incorrectly promoted *remote work possibility* into a **required candidate qualification**, allowed a long general-conditions span mixing employment terms and salary into qualification evidence, and duplicated several narrative concepts through structured skill tags.
- **Verdict:** Independently **rejected** in the isolated SQLite review workflow. Its rejected-artifact archive retains the exact frozen candidate SHA-256; no accepted English P1.6 projection remains for that posting. This is a **semantic false positive inside a structurally valid artifact**, not merely an unavailable source.

## 4. Root-cause boundaries

This cohort shows at least three separate quality risks; solving only one will not restore useful coverage:

1. **Source representation and section lineage.** Jobinja structured fields, narratives and skill tags can repeat or concatenate content. English translation preserves key text but sometimes flattens headings and parent/child preference boundaries. Requirement-vs-duty classification must derive from exact source-section identity, not inferred from adjacent prose or job title alone.
2. **P1.6 candidate modeling and validation interaction.** Source-conditional evidence (`if you have a portfolio`), alternate seniority tracks, preference sections and example tools are currently difficult for the model to encode without false-strength tags or coverage collisions. Keep fail-closed validation; fix candidate decomposition and targeted evidence-bound repair, rather than relaxing rules to increase throughput.
3. **Authority and review-state semantics.** English P1.6 correctly rejects unsafe generations, but the older independent original-language v9/v4 route persists an `accepted` state despite the observed semantic mistakes. Do not interpret storage status as independent factual truth. Audit whether any product reader or downstream task could unintentionally rely on this unreviewed original-language artifact.

No systematic performance or general market reliability percentage is claimed: these are five exposed, chosen cases and the evaluator knew each case's native success/failure state before source reading, although the substantive model output was withheld until source notes were locked.

## 5. Recommendation: next engineering milestone

**Prioritize one targeted P1.6 source-faithfulness and analysis-recovery increment before new P2.3B model reasoning.**

The first increment should:

1. Build an exact, typed source-section spine: narrative qualification, explicit duty, preference, application instruction, employment arrangement, structured sidebar metadata, alternative-tier eligibility and example tools—with immutable original source identities and section offsets where supported.
2. Add candidate classification gates that prevent arrangements and conditional portfolio text from becoming qualifications and avoid promotion of required capabilities into duties. Preserve **Middle vs Senior**, **required vs preferred**, example-vendor and certificate-or-equivalent disjunctions.
3. Investigate why a complete English EDR document yields zero claims while the separate original-language contract extracts them; use comparable frozen source spans in a narrow diagnostic before changing models.
4. Resolve original-language artifact `accepted` authority semantics: do not let mechanically valid unreviewed source interpretations bypass the same epistemic safeguards expected for English P1.6.
5. Re-run these five **exposed regression cases** with full immutable evidence, and only then challenge the fix on **new, separately selected cases** to avoid overfitting this cohort.
6. Permit Work/Capability and ultimately a useful technical-expectation brief **only after the upstream evidence survives independent review**.

**Not next:** More comparison UI refinement, mass Registry mappings, persistent P2.3 capability profiles, speculative employer-skill generation, or new recruitment-source expansion just to compensate for unreliable interpretation.

## 6. Reproducibility and exact artifacts

Public, source-backed and machine-checkable files:

- `docs/working-memory/2026-11-12_FRESH_SOURCE_COHORT_INDEPENDENT_ANALYSIS_PROTOCOL.md`
- `docs/working-memory/2026-11-12_fresh_source_cohort/SOURCE_ACQUISITION_EVIDENCE.json` — public original URLs, acquisition/parse state and source SHA-256
- `docs/working-memory/2026-11-12_fresh_source_cohort/NATIVE_PRODUCT_OUTPUT_FREEZE.json` — frozen pipeline model/attempt/status and artifact hash identities **before** source reading
- `docs/working-memory/2026-11-12_fresh_source_cohort/INDEPENDENT_LIVE_SOURCE_CHECK.json` — independently revisited public URLs and stable JSON-LD title/description/date
- `docs/working-memory/2026-11-12_fresh_source_cohort/INDEPENDENT_ADJUDICATION.json` — case-level reviewer verdicts, factual-source checklist hashes and original-mode diagnostic

Local-only under ignored `data/local-acceptance/current-real-ads-2026-11-12/`: five original HTML pages, repeated independent direct-source fetches, unredacted candidate SQL, all translation/model logs, source-only checklists, separate per-case SHA seals, exact diagnostics, and the source-reader/runner scripts. None of these raw materials is committed.

The normal live SQLite database and the tracked repository `corpus/` are untouched by this evaluation. A source-state cross-check also confirmed that one selected ID (`tNhZ`) already existed in the live database from September 2026, while the other four selected IDs did not; its old record was not altered by the new isolated capture. All validation/integrity checks passed, including the independent-note and model-output SHA-256 seals. The unchanged application code passed **884 warnings-as-errors tests**, repository Ruff and dependency checks during this evaluation. The work is kept on its own branch and should be reviewed independently before any planning modifications to `main`.
