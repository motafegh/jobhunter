# P1.6 — live real-ad end-to-end source-first audit (23 November 2026)

**Disposition: BLOCKED for real product semantic usefulness; source/translation mechanics largely worked; no B5 or B6 acceptance.** This is a diagnostic trial, not a new prospective blinded B5 gate or a production rollout. Keep the original findings before applying fixes.

## What was actually exercised

- From a frozen metadata selection, ran three approved, bounded Jobinja one-page search requests across backend, AI/LLM and security categories, discovering 59 unique job IDs. The current CLI auto-regenerated the root public-corpus export from an otherwise isolated trial configuration. This was promptly restored to its original Git state and verified by SHA-256. **This side effect is an operational isolation defect** needing a dedicated fix before repeating isolated CLI searches.
- Retrieved **six** original job detail pages successfully with the approved product source service (three initial, two preselected reserves and one separately frozen extra security replacement). Matched original-description hashes against 37 archived description versions from seven prior evaluation databases. **Three fetched descriptions were already archived duplicates**, including one case under a different Jobinja ID. Those were excluded from the new-source evaluation. **Three source-distinct cases** remained for the manual diagnostic: Python/backend, AI backend/LLM/speech and security operational reporting. They are not a random sample of the market.
- Captured original HTML, exact source fingerprints, parsed source versions and B2v6/B1 candidates into a **private, ignored, isolated SQLite and evidence directory**. The selected three source candidates passed deterministic B1 validation. Translated the selected three with the current LM Studio E2B translation service; all completed. The initial duplicated cases were also translated before the archival source duplicate discovery. Translation completion is not semantic accuracy.
- Ran the **current production-contract English P1.6 v30 service** with the locally configured Gemma E4B model against all three source-distinct cases: three generated failures and **zero valid current English P1.6 artifacts**.
- Ran a separately bounded **original-language P1.6 v9** attempt on the Persian source: mechanically completed and persisted an automatic status of **accepted** in the **isolated trial** database. Subsequent human-style assistant source review found an unsupported mandatory experience claim and one omitted qualification. **Automatic acceptance was not independent semantic certification**.
- Invoked the product Capability command on the Persian job: correctly refused because **current, semantically accepted English P1.6 analysis was absent**, despite the original-language v9 artifact. This is a correct prerequisite guard and an end-to-end usefulness block.

## Source-first manual comparison — material observations

### Backend / software case
- Two distinct work-duty headings contain seven + eight action passages, with some semantic overlap. The experimental B2v6 candidate preserves the first seven as original text but calls them **context** instead of **work duties**, making the work overview incomplete.
- Its postqualification section includes company growth, mentoring and culture **benefits** that B2v6 partly mislabeled qualifications or behavioral expectations due to heading-state inheritance.
- Original wording offers a **Python OR Go** capability route, not necessarily both. Work arrangement says **hybrid prioritized with full remote flexibility available**. The source also has **contradictory structured versus narrative professional-experience ranges**. None should be flattened into a single unqualified mandatory claim.
- English v30 failed on model-produced requirement concepts that contained explicit technical-depth adjectives, violating depth/concept separation (111.1s runtime; two structured attempts; one persisted SafeFailure, no accepted artifact).

### Applied AI / LLM and speech case
- Six explicitly assigned duties. Under a heading meaning **Must Have**, there are **five** substantive qualifications; under **Nice to Have** there are three advantages. B2v6 treats the **heading itself** as a required item while treating **all five actual must-haves as unresolved**. The three optional ones were correctly marked preferred.
- The source text permits an academic eligibility alternative; do not flatten it into all degrees required. The board metadata names one employer while its own vacancy description names another. The source conflict must remain unresolved.
- Translation retains the English job description but one transliterated board employer name is misspelled, despite an official Latin name also present in source metadata.
- English v30 failed on inappropriate **strong** depth wording in a requirement concept (76.0s; two structured attempts; no artifact).

### Security reporting / operations case (Persian original)
- B2v6 kept all **six** explicit work duties and **six** technical skill items under broadly correct sections; this is the strongest source-candidate result of the three.
- English translation merged the last two separate duty passages into an ambiguous sentence, blurring who performs the trend analysis; it also fragmented one performance-related bonus into two loosely expressed benefits.
- English v30 failed **dense responsibility coverage**: one required source-duty reference was not accounted for in the candidate analysis (71.5s; two structured attempts; no accepted artifact).
- Original-language v9 generated work duties broadly faithful to the source, but also an automatically **accepted, unsupported mandatory experience requirement**: it took an employer **benefit about professional working environment** as an applicant experience concept, improperly sourcing that concept to a structured **less-than-three-years** field. It also missed the explicit source skill on measuring performance indicators, and some depth remained embedded in concepts instead of depth_signal. Manual assessment: **semantic rejection** even though automated artifact status is **accepted**. Preserving this discrepancy in evidence is essential; do not auto-promote this research artifact or claim a human approval.

## Reproducible aggregate result

| Stage | Selected three source-distinct cases |
| --- | ---: |
| Live original-source acquisition | 3 / 3 parsed, source fingerprints retained |
| B2v6 + B1 original-source contract | 3 / 3 mechanically valid; two material category defects |
| Current English translation v2 | 3 / 3 mechanically completed; noted meaningful-language defects |
| Current English P1.6 v30 | **0 / 3 completed valid analysis artifacts** |
| Separate original-language v9 | **1 / 1 mechanically accepted; 0 / 1 independently semantically approved** |
| Capability v9 above current English P1.6 | **0 / 3: correct upstream block** |

No false statistical accuracy percentage or performance estimate is inferred from three deliberate diagnostic cases. Fail-closed v30 validation is a genuine safety positive; 0/3 delivery is a genuine product failure. Automatically accepted v9 with a source-inconsistent claim is a separate, potentially higher-risk reliability issue.

**Source-safe aggregate receipt:** `docs/working-memory/2026-11-23_p16_real_e2e/SAFE_REAL_AD_E2E_MANUAL_AUDIT.json`. Full original employer text, identifiers, raw HTML, translations, generated model content, exact case audit and SHA-verified replay live only in ignored local evidence at `data/local-acceptance/2026-11-23-fresh-e2e-manual-audit/`. The latest original-source manual review was prepared **before opening** generated model analysis. It is same-assistant inspection, not a blinded human or independent reviewer study.

## Practical product implications (recommendations, NOT automatically approved implementation)

1. **First:** Protect source-first coverage and obligation meaning for heading hierarchies and heading/list-item structure (including work sections, Must Have and Nice to Have). Keep relational work/implied capability reasoning flexible; do not proliferate per-job hardcoded regex exceptions merely to force success percentages. Reject invented professional experience and pseudo-eligibility.
2. **Second:** Resolve v30 repeated concept/depth validation failures with bounded model trials, inspectable targeted repair and source-local checklists; preserve strict no-fabrication and declared alternatives. Offer existing B4v6 source-first candidate fallback on model failure only behind a separate explicit product/authority gate, instead of a blank semantic screen.
3. **Third:** Tighten v9 acceptance/reuse: exact cited source-concept correspondence, employer benefit-vs-requirement boundary, mandatory/optional modality, whole-description overbroad references and source-item recall must survive semantic review. An automatically accepted original-language artifact is not an excuse to skip reviewer truth checks.
4. **Fourth:** For translation, preserve explicit HTML bullets/roles and technical depth; guard named brands by source bilingual identity and prioritize recognized Latin forms. Preserve company and board/prose contradictions as inspectable conflicts.
5. **Fifth:** Add source-text content-hash deduplication across job IDs and all previous prospective/exposed cohort receipts **before** asserting new-source independence. Isolate public corpus export targets for research CLI discovery; the public repository must not be temporarily overwritten by an isolated test database.

**Do not claim B5 acceptance, B6 promotion, or product perfection.** Next appropriate step is to review these actual failures together and select a tightly scoped implementation/validation milestone; any next prospective gate must use genuinely untouched sources under a pre-frozen method. This run made no production code, accepted fact, production database or public corpus change.
