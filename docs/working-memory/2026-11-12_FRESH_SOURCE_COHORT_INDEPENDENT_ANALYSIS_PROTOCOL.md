# JobHunter Fresh-Source Cohort — Independent P1.6/Work/Capability Audit

**Date:** 2026-11-12
**Branch:** `evaluation/current-real-ads-2026-11-12`
**Base code:** `main` at `74ffec25533c5cd4b1afa90b0c3bc76ee023e7aa`
**Status:** Evaluation only; no automatic P1.6/Capability authority

## Purpose and exposure controls

Test JobHunter's *current accepted product code* against real public vacancies newly acquired in this run, then independently assess actual original advertisements and compare with the preserved model outputs. This is a **diagnostic exposed cohort**, not a protected holdout or an estimate of general model reliability.

The repaired Jobinja source client uses direct HTTPS with a declared `JobHunter/0.1` user agent, sequential requests, conservative delays and bounded budgets. No cookies, CAPTCHA circumvention, proxy rotation, login or hidden API have been used.

All evaluation inputs and derived material are local-only under the ignored `data/local-acceptance/current-real-ads-2026-11-12/` directory. The evaluation uses isolated SQLite, evidence and corpus roots; neither main nor production data is intentionally touched.

## Preselected acquisition/execution scope

Four source searches, each limited to one page: Persian AI, RAG, Persian cybersecurity, Python. **Four pages, 71 unique job URLs, 0 discovery failures.** The cohort was selected before reading full advertisements or model outcomes:

| Job ID | Discovered title category | Reason |
| --- | --- | --- |
| `tNhZ` | AI/LLM engineer | Explicit LLM expectations, may contain alternative work |
| `tMps` | Applied AI engineer | Compare interpretive depth of general applied AI |
| `tMqd` | AI/Python backend developer | Distinguish job role from adjacent backend requirements |
| `tNDx` | EDR technical security | Distinguish security tooling/operations/technical support |
| `tMjm` | Pentesting/security | Offensive work and tools/credentials distinction |

All five individual source URLs yielded HTTP 200, passed the existing Jobinja parser, and were saved with immutable HTML SHA-256. No prior P1.6 analysis artifacts existed for these exact acquired source versions.

**Caveat:** First encountered by this isolated run on November 12 does *not* prove the ads were first posted on November 12 or will remain available.

## Product-first methodology

1. Freeze the five original `canonical_url`, detail version, timestamp and content-hash identities without evaluating semantic text.
2. Run the configured native translation, then bounded P1.6 analysis for all five under ordinary acceptance rules. Never switch model or change prompt silently. Record per-job subprocess exit, model, duration, prompt/schema, artifact ID, candidate integrity hash and any fail-closed diagnostic.
3. Freeze each JobHunter case's terminal candidate/outcome, log SHA-256 and artifact hash **before opening that case's original ad** for independent review. Cases may be reviewed one by one while other product runs continue, but an evaluator must never open a case's generated semantic output before sealing that case and writing its independent source checklist. Generated analyses are **not autoaccepted**.
4. Independently open the original public URLs using standard direct HTTP, examine the original HTML/JSON-LD, and construct source-only checklists covering directly described work, required/preferred qualifications, alternative sets, tools/examples, experience and explicit/unknown technical scope. Include source HTML hash and whether live URL's source changed.
5. Freeze independent checklists with SHA-256 before viewing the model-generated P1.6 analyses. Compare the frozen original facts to JobHunter claims, translation fidelity, source classification, eligibility and omissions. Classify each discrepancy with source references.
6. Only candidates passing source-grounded P1.6 review in the isolated evaluation DB may be fed to Work Intelligence and Capability v9. Record any withholding or failed downstream run.
7. Publish only public job IDs/URLs, source hashes, stage statuses and aggregate classifications. Raw ads, local files, model completions and full review checklists stay ignored in local data.

## Evaluation questions and stop lines

- Does acquisition/deduplication work across four areas, including original URL/provenance?
- Can local translation and P1.6 handle new live source versions without silently losing duties, obligation, alternatives and requirement/depth?
- Do Work/Capability outputs preserve explicit-versus-inferred authority, avoid hallucinated job duties, and remain useful for explaining actual expectations?
- Are errors caused by translation, source parser, model schema, prompt/retry, interpretation, or UI/provenance?
- Can a maintainer reproduce case-specific failures without repeating whole acquisition?

**Stop lines:** No third-party challenge bypass, no raw ad/source text published, no implicit main database changes, no acceptance without review, no market-wide reliability percentages from five cases, no inference that a listing is still open beyond the capture check, and no polishing of comparison UI as a substitute for correcting factual defects.

**Success criterion:** concrete actionable source-backed mismatches or trustworthy bounded positive cases that select the next substantive engineering repair.
