# JobHunter independent real-ad product audit — results and product decision

**Date:** 2026-11-12
**Branch:** `evaluation/fresh-job-ads-blind-2026-11-12`
**Base product:** `main` at `2de22a877772cf4a40154d8118a35ad19d1af8b7`
**Status:** Completed bounded native workflow and independent archived-source comparison; fresh live acquisition failed upstream
**Protocol:** `2026-11-12_FRESH_VACANCY_INDEPENDENT_PRODUCT_AUDIT_PROTOCOL.md`

## Executive disposition

**JobHunter is capable of useful grounded technical-job analysis, but the new-ad-to-accepted-intelligence path is not yet robust enough for general promotion.** This small, deliberately selected cohort is an engineering diagnostic, not a statistical estimate of product quality.

Fresh Jobinja acquisition was blocked by HTTP 403 on three modest, approved searches. No current November vacancy was acquired. Rather than bypass the restriction or pretend otherwise, we used **four real, previously archived but never P1.6-analyzed Jobinja postings** from August–September 2026. Their original HTML SHA-256 values were verified against JobHunter's durable acquisition records. We ran all supported stages on an isolated SQLite copy; all unpublished original/derived text remains under ignored local evaluation files.

The important conclusion is **not** to rebuild P2.3B prose immediately: first fix the P1.6 semantic reliability and establish a permitted source-input route for genuinely new ads. A trustworthy downstream Capability layer cannot compensate for missing or incorrectly classified source facts.

## End-to-end results

| Gate (four archived jobs except where specified) | Observed outcome |
| --- | --- |
| Fresh Jobinja searches (3 terms, one page per term) | **0/3 succeeded**, all HTTP 403; adapter stopped without bypass |
| Archived original source bytes / SHA-256 provenance | **4/4 verified** |
| Native English translation | **4/4 available** (2 newly translated, 2 current artifacts reused), 0 failures |
| Current English P1.6 candidate generation | **2/4 generated**, 2/4 validation failures after bounded retries |
| Independent semantic adjudication of generated P1.6 | **1 rejected and archived**, 1 boundedly accepted **only in isolated evaluation database** |
| Work Intelligence v2 on the boundedly accepted job | **1 successful candidate**, 3 source-grounded themes, 5 accepted direct duties |
| Capability Intelligence v9 on the same job | **1 successful candidate**, 5 interpretive groups, source linkage 11/11 capability requirements and 5/5 duties; 4 redundant/misplaced model enrichments filtered |
| Product outputs promoted to main / user-visible accepted claims | **None** |
| Original repository corpus after test cleanup | Restored to base state; generated projections retained under ignored local evaluation folder |

See `2026-11-12_real_ad_independent_product_audit/NATIVE_PRODUCT_EVIDENCE.json` for exact artifact IDs, models, source hashes, review states and diagnostic counts. See `SOURCE_URLS_AND_ORIGINAL_HASHES.json` for every original public ad URL and acquisition date.

## Independence and coverage limitations

The evaluator first examined original source HTML as captured in the existing Jobinja acquisition archive (from each original URL), using a **separate standard-library reader of embedded JobPosting JSON-LD**, not JobHunter's derived English projections or P1.6 models. Four distinct independent domain/requirement/duty checklists were frozen and SHA-256 recorded before the model candidates were inspected.

After unblinding, an additional source-sidebar pass verified structured education/experience categories. This *post-freeze addendum* is explicitly not treated as fully blinded assessment, but prevents incorrect accusations that source-structured fields were fabricated when they were actually present outside the main ad description.

Direct access to individual Jobinja URLs was unavailable through the public browsing route during this audit, and the supported source adapter had already received explicit 403 responses. There was no further access attempt, bypass, account session, or source change. Original HTML captures are not evidence those jobs remain open today.

The selected four were *unprocessed* at baseline but not *newly posted*; source availability, geography, temporal shift and case selection all limit generalization. Model outputs were human-reviewed, not sampled from a protected holdout. A reviewer reading the same original HTML is partially independent, not a separate blind third party.

## Case-by-case independent comparison

### 1. `tNpG` — LLM/RAG healthcare developer

**Independent source assessment:** multiple directly stated technical duties, including clinical-risk grounding, RAG retrieval/reranking/citation quality, test datasets and regression/evaluation, Persian answer-quality benchmarking, token cost/observability and .NET/Angular collaboration. It explicitly distinguishes strong Python from mere applied C#/.NET familiarity. There is also a direct experience minimum in the job description and a coarser experience category in the sidebar.

**JobHunter result:** translation available, but English P1.6 **failed closed** after two model attempts. The reported structured failure concerned a combined Python/C# requirement with incompatible explicit-depth markers. No semantically accepted job analysis or downstream Capability/Work was fabricated.

**Verdict:** high-impact **coverage/throughput failure** on a meaningful real posting, paired with a **correct safety rejection**. Repair source-aware decomposition of mixed-strength requirements rather than relaxing the depth validator.

### 2. `t4Ay` — senior AI/LLM/agent developer

**Independent source assessment:** real direct work spans LLM agents, RAG, NLP operations, text/image generation, recommendations, data/MLOps, backend APIs, inference optimization and conditional fine-tuning/evaluation. Explicit qualifications include AI/LLM/agent experience, architectural design capability and production-model deployment. Backend .NET Core / SQL Server integration is required as an interface constraint; it does not independently prove C# proficiency. The original sidebar separately includes a bachelor's degree.

**JobHunter result:** generated 13 purported direct responsibilities, 4 requirements and one role-purpose item. Many real duties were correctly extracted, including alternative image-model tools. However:
- one *required-experience and production-capability* paragraph was classified as a **direct responsibility**;
- the substantive narrative qualifications were correspondingly **missing from the requirement list**, which instead contained structured education/skill tags;
- the standalone role-purpose statement was an **incomplete fragment** rather than an intelligible supported statement;
- a list of possible project outputs was grouped as one high-confidence duty, which warrants a clearer deliverable-versus-action distinction.

**Verdict:** **reject** P1.6 due source-category leakage and corrupted role-purpose extraction, despite substantial correct work capture. JobHunter archived the rejected artifact with its original content hash preserved. This was verified in the isolated rejection archive.

### 3. `ta9l` — senior applied AI, financial intelligence

**Independent source assessment:** five explicit duties: financial semantic representation, agents/RAG, scalable embedding/retrieval pipelines, evaluation/observability, and entity resolution/text-to-SQL. Core requirements include production LLM/RAG/vector-db work, deep retrieval understanding, alternatives among agent frameworks, strong SQL and Python. The original *sidebar* additionally states bachelor's degree and a three-to-six-year experience category.

**JobHunter P1.6:** five of five direct duties correctly preserved; 13 requirement records include original narrative qualifications, structured education/experience and overlapping skill tags. A vector database *such as Qdrant* is source-example language, **not a mandatory Qdrant-only requirement**. Framework alternatives remain explicit. Multiple overlapping source/skill-tag records must not be interpreted as independent market frequency.

**Diagnostic review:** allowed to feed downstream **only within the isolated evaluation SQLite**. No acceptance was performed on the user's live database.

**Work v2:** three work themes cover all five source-explicit responsibilities, with no speculative deliverables. The role label is interpretive, not employer-stated; a possible “solutions architect” reading must not become an asserted job title or ownership scope.

**Capability v9:** five job-local capability groups preserve 5/5 work linkage, 11/11 owned capability requirements and source-explicit depth; four model-generated redundant/misplaced expectations were removed. The label “MLOps & System Reliability” is **interpretive grouping** over explicit evaluation/observability work and a reliability qualification; the job did not explicitly require an MLOps job title or generic platform ownership. Its group-level required strength should not be misread as a source-mandated independent MLOps specialty.

**Verdict:** a **promising supported end-to-end example**, with specifically bounded example/alternative/overlap interpretation risks. It demonstrates downstream value *conditional on accepted-quality P1.6*, not a general reliability claim.

### 4. `t4wP` — senior offensive/application security engineer

**Independent source assessment:** concrete offensive security work (penetration testing, complex access-control and API issues, remediation verification, DevSecOps scan findings, exposed-asset/CVE hunting, reporting and automation). The description requires at least five years in offensive/application security, while the original site's coarse sidebar experience category is three to six years. These statements overlap but are **not equivalent** and must not be silently merged. Offensive/security certifications are expressly preferred, not mandatory. The position interacts with SOC teams but is not primarily a SOC detection role.

**JobHunter result:** translation available, but English P1.6 **failed closed** after two attempts because the years/depth text was left inside a requirement concept rather than separately represented by the depth field.

**Verdict:** second substantive **requirement-depth throughput failure**, with an appropriately strict validator; no downstream artifact was invented.

## Root-cause priorities

| Priority | Observed defect | Recommendation |
| --- | --- | --- |
| **P1** | Fresh approved Jobinja discovery now returns 403 | Support policy-compliant manual pasted-text/URL import with a distinct source identity, and/or add one approved public ATS/feed source. Do **not** bypass Jobinja controls |
| **P1** | 2/4 P1.6 generations fail on explicit/mixed depth | Use source-section-aware requirement decomposition and targeted bounded repair; preserve original mixed depth/experience evidence, avoid invented uniform level |
| **P1** | Qualification wrongly promoted to a duty; truncated role purpose; important required narrative missed | Add explicit responsibility-versus-qualification boundary checks, coverage invariants and concrete hard-case tests using the archived sources |
| **P2** | Qdrant/example wording and overlapping structured skill tags can look independently required | Preserve alternatives, examples, source-level claim provenance and nonindependent denominators through P1.6 and Capability |
| **P2** | Native operations wrote tracked `corpus/` despite isolated database and evidence directory | Make corpus projection destination explicitly configurable for evaluations or provide a dry-run/read-only capture mode. This run backed up and restored every generated corpus file |
| **P2** | Some Capability group names/scope may read like direct employer demands | Retain the clear distinction between interpretive grouping and source-explicit obligation; test the exact user-facing display before authority promotion |

## Next milestone recommendation

**First: P1.6 correctness and fresh-source availability, before more P2.3B model tuning.**

1. Promote these four public-source *case identities and test questions* to a regression **diagnostic cohort**, keeping private/raw source captures in approved local evidence storage, and not manufacturing accepted P1.6 labels.
2. Resolve at least the two explicit depth failures and the qualification→responsibility misclassification with bounded source-aware repairs. Retain fail-closed validation, attribution and negative evidence.
3. Create a first-class permitted input path for **3–5 genuinely new** public/owner-supplied vacancies that does not impersonate Jobinja. Preserve immutable original text/URL, fetch-access state, timestamp and content hashes.
4. Re-run fresh acquisition/ingestion → translation → P1.6 review → Work/Capability (only on accepted facts), and conduct another independent source comparison with actual current ad URLs.
5. Only then resume P2.3B semantic interpretation and decide whether one of its proposed model-backed explanations is accurate and useful enough to expose.

**Stop line:** No broad product-quality percentage, no autoacceptance from this cohort, no automatic model-powered source remediation outside policy, no promotion of optional P2.3B profiles, and no cosmetic UI work as a substitute for data correctness.

## Records and reproducibility

- `docs/working-memory/2026-11-12_FRESH_VACANCY_INDEPENDENT_PRODUCT_AUDIT_PROTOCOL.md` — predeclared evaluation method and limits
- `docs/working-memory/2026-11-12_real_ad_independent_product_audit/SOURCE_URLS_AND_ORIGINAL_HASHES.json` — public URLs / original capture identity
- `docs/working-memory/2026-11-12_real_ad_independent_product_audit/NATIVE_PRODUCT_EVIDENCE.json` — machine-checkable stage and artifact outcomes
- Original source snapshots, translations, failed model diagnostics, raw product outputs, adjudication checklists and independent-note hashes: saved under ignored `data/local-acceptance/fresh-job-ads-blind-2026-11-12/` on the authorized local machine.
- The experimental evaluation branch contains **no raw ads**, no applicant data, no credentials and no SQLite files. Main branch and the original corpus are unchanged by the published review. **Final baseline engineering gates: 879 tests passed with warnings as errors in 48.01 seconds; Ruff and Python dependency consistency passed.** This confirms the existing code remains green; it does not cure the real-ad semantic errors found above.


## November 12 network-diagnostic correction (after original audit)

The original **three HTTP 403** responses were real and the diagnostic cohort results remain valid **for that proxy-routed execution**. A separate follow-up identified the operative failure mode:

- The WSL environment sets HTTP_PROXY / HTTPS_PROXY to the authorized Windows-side local listener at 127.0.0.1:8080; the listener is served by VeePNService.
- The existing Jobinja source client instantiates httpx.Client without an explicit proxy trust setting, so its default behavior uses that proxy.
- Jobinja robots.txt returned **403 ArvanCloud HTML protection** via the proxy versus **200 text/plain** on the direct route with the same declared JobHunter user agent.
- A single direct request to the **same Jobinja Python search endpoint** returned **200 HTML**, passed the project's HTML/body validation and produced **20 valid public job links**.

Therefore, the broad interpretation “Jobinja blocks our acquisition” was incomplete. The measurable immediate blocker is **implicit environment proxy routing**. The original three-search 0/3 metric should not be read as direct-access or all-source unavailability. A narrowly scoped client routing fix and fresh isolated end-to-end retest are being tracked separately; their outcomes must be recorded distinctly, not retroactively substituted for the original test.
