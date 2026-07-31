# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors working in
this repository.

## 1. Product priority

JobHunter is a real personal utility intended for repeated local use. It is not
primarily a learning exercise.

Prefer a smaller dependable implementation over an impressive but unreliable
one. Speed means completing coherent useful increments, not bypassing evidence,
limits, tests, or explicit state.

## 2. Required reading order

Before material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/SEARCH_CONFIGURATION.md`
5. `docs/ACQUISITION_OPERATIONS.md`
6. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
7. `docs/SOURCE_POLICY.md`
8. `docs/IMPLEMENTATION_PLAN.md`
9. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`

The product specification controls intended behavior. Architecture controls
technical boundaries. The implementation and Phase 1 plans control sequencing
and acceptance.

## 3. Accepted state

Accepted on `main`:

- M0 local foundation;
- P1.1 discovery foundation;
- P1.2 bounded pagination, multiple searches, overlap handling, and repeat-safe
  discovery;
- explicit, missing-only, and refresh-due detail acquisition;
- immutable raw search and detail evidence;
- parser-v2 deterministic Jobinja extraction;
- semantic versions independent from volatile HTML;
- successful and failed fetch observations;
- local job, check-history, and structural audit commands.

Live validation includes:

- 79 unique jobs across two two-page searches;
- one cross-search overlap;
- zero new jobs on the identical rerun;
- fifteen complete varied advertisements;
- fifteen of fifteen latest versions structurally clean;
- unchanged checks producing observations without false versions.

## 4. Current authorized implementation

The active increment is **configurable bilingual acquisition planning and
acquisition-only synchronization**:

```text
built-in profiles and packs
+ custom Persian/English groups
+ optional raw Jobinja URLs
→ normalized term and URL deduplication
→ inspectable search plan
→ search limit, cyclic offset, pages, and global request budget
→ repeat-safe discovery
→ bounded missing and refresh-due details
→ immutable evidence
→ deterministic parsing and semantic versioning
→ fetch observations
→ structural audit
→ acquisition sync summary
```

Active commands:

```text
jobhunter jobinja catalog
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch
jobhunter jobs list
jobhunter jobs show
jobhunter jobs checks
jobhunter jobs audit
```

## 5. Search-registry rules

- Keep built-in profile and pack identifiers stable.
- Add a term to the narrowest relevant pack.
- Include Persian and English forms when both appear in real listings.
- Preserve the original display term.
- Normalize only for identity, deduplication, and exclusions.
- Keep custom groups and exclusions configuration-driven.
- Keep raw URLs for Jobinja-owned filters that keyword generation cannot express.
- Inspect plans before live acquisition.
- Do not equate search vocabulary with accepted career taxonomy or relevance.
- Do not optimize for term count alone; evaluate discovered-job usefulness and
  noise.

One-run CLI selectors must not silently mix configured searches. Search and URL
identity must be deduplicated before acquisition.

## 6. Acquisition bounds

- Search requests are sequential and use the configured delay.
- Discovery enforces a global request budget internally.
- Budget exhaustion must send no additional request.
- Budget exhaustion is `request_budget_reached`, not a failure.
- Detail batches contain at most 50 unique jobs.
- Acquisition sync missing plus refresh limits may not exceed 50.
- Raw evidence is written before parsing.
- One search or job failure must not discard successful work.
- Acquisition remains independent from LM Studio.

## 7. Record boundaries

Never conflate:

```text
JobPosting
  logical source identity

SearchPageSnapshot
  one exact search-page response

JobPostingVersion
  meaningful deterministic content history

JobDetailFetchObservation
  one successful or failed detail-page check

Raw evidence
  exact response bytes and metadata
```

Repeated unchanged checks create observations and raw snapshots, not false
semantic versions.

## 8. Parser and audit boundaries

The parser extracts explicit source fields and complete source text. It must not
infer employer intent.

The deterministic audit may detect shape, contamination, parser-version, and
coverage problems. A clean audit does not prove semantic interpretation.
Missing optional fields alone are not parser failures.

No active acquisition increment may infer:

- role purpose;
- responsibilities;
- required versus preferred qualifications;
- description-derived skills;
- personal relevance;
- capability gaps;
- application readiness;
- career recommendations;
- aggregate market conclusions.

Those belong to P1.6 and later.

## 9. Development rules

- Build complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network and model calls.
- Keep CLI handlers focused on composition and argument validation.
- Keep direct SQL behind focused repository boundaries.
- Treat acquired content as untrusted data.
- Keep LM Studio behind the inference-provider interface.
- Use typed configuration and versioned schemas.
- Prefer explicit failure and review states over fabricated defaults.
- Keep runtime data, local configuration, model artifacts, and personal evidence
  out of Git.
- Add deterministic tests for every new normalization, selection, persistence,
  or orchestration rule.
- Normal tests must not require Jobinja or LM Studio.
- Avoid speculative modules and dependencies.

## 10. Source acquisition discipline

Use public Jobinja pages only. Preserve attribution and canonical URLs. Validate
redirect hosts and paths. Enforce timeouts, delays, limits, response sizes, and
content types.

Do not implement:

- login automation;
- CAPTCHA or access-control bypass;
- proxy rotation or stealth crawling;
- authenticated-platform scraping;
- unrestricted crawling;
- automatic applications.

## 11. LLM extraction discipline

When P1.6 begins:

- require versioned prompts and schemas;
- validate output locally;
- retain request, raw response, model identity, parameters, and timing;
- require source evidence for material claims;
- distinguish explicit content from inference;
- measure quality on a reviewed real-job corpus;
- never grant the model shell, filesystem, browser, or unrestricted network
  tools.

## 12. Change discipline

A material change must state:

- the milestone requirement it implements;
- files changed;
- behavior added or corrected;
- deterministic tests;
- live acceptance required;
- remaining scope exclusions.

Update controlling documents when product or architecture decisions change. Do
not create governance documents for trivial edits.

## 13. Definition of done

An increment is done only when:

- the intended workflow functions locally;
- tests and Ruff pass;
- acceptance criteria are met;
- failures are understandable and inspectable;
- configuration and operation are reproducible;
- documentation matches actual behavior;
- no unrelated future scope is claimed.

Work directly on `main` unless a later change creates a concrete isolation need.
