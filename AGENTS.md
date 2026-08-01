# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors working in
this repository.

## 1. Product priority

JobHunter is a real personal utility for repeated local use. Prefer dependable,
inspectable behavior over impressive complexity. Speed means coherent useful
increments, not bypassing evidence, bounds, tests, or state.

## 2. Required reading order

Before material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/SEARCH_CONFIGURATION.md`
5. `docs/TRANSLATION_AND_ENGLISH_CORPUS.md`
6. `docs/ACQUISITION_OPERATIONS.md`
7. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
8. `docs/SOURCE_POLICY.md`
9. `docs/IMPLEMENTATION_PLAN.md`
10. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`

## 3. Accepted source state

Accepted on `main` before the current translation acceptance:

- M0 local foundation;
- P1.1 discovery;
- P1.2 bounded repeat-safe multi-search discovery;
- explicit/missing/refresh-due detail acquisition;
- immutable raw search/detail evidence;
- parser-v2 deterministic Jobinja extraction;
- semantic source versions independent from volatile HTML;
- successful/failed fetch observations;
- local job/check-history/parser-audit commands.

Live source validation includes 79 unique discovered jobs, one overlap, zero new
jobs on identical rerun, fifteen varied complete advertisements, fifteen of
fifteen structurally clean parser versions, and unchanged refresh checks without
false semantic versions.

## 4. Current authorized increment

Current acceptance target combines:

```text
data-driven bilingual search catalog
→ bounded search planning/acquisition
→ deterministic source semantic versions
→ optional derived English projection
→ current English corpus export
```

Active commands:

```text
jobhunter jobinja catalog [--show-terms]
jobhunter jobinja plan
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch
jobhunter jobs list
jobhunter jobs show
jobhunter jobs checks
jobhunter jobs audit
jobhunter translations status
jobhunter translations run
jobhunter translations show
jobhunter translations export
```

## 5. Search-catalog rules

- Search words live in TOML data, not Python tuples/constants.
- Pack/profile identifiers should remain stable once published.
- A complete catalog may be replaced through `jobinja_search_catalog_path`.
- Use small custom groups for personal additions that do not justify a full
  replacement catalog.
- Preserve original display terms.
- Normalize only for search identity/deduplication/exclusion.
- Keep Persian and English forms when real listings use both.
- Interleave selected packs round-robin for bounded cross-domain coverage.
- Raw URLs remain the escape hatch for Jobinja-owned filters.
- Search vocabulary is not a career taxonomy and does not prove relevance.

## 6. Acquisition bounds

- Jobinja requests remain sequential with configured delay.
- Discovery enforces a global request budget internally.
- Budget exhaustion sends no extra request and is not a failure.
- Detail batches contain at most 50 unique jobs.
- Sync missing + refresh limits may not exceed 50.
- Raw evidence is written before parsing.
- One search/job failure must not discard successful work.
- Source acquisition remains independent from LM Studio and translation.

## 7. Source and derived record boundaries

Never conflate:

```text
JobPosting
  logical source identity

SearchPageSnapshot
  one exact search response

JobPostingVersion
  meaningful employer-content history

JobDetailFetchObservation
  operational source checks

JobTranslationArtifact
  derived English view of one exact source version

JobTranslationAttempt
  operational translation history

Raw evidence
  exact source bytes and metadata
```

A translator/model/schema change does not create a new source semantic version.

## 8. Translation rules

- Translation is optional and disabled by default.
- Google Cloud translation is an explicit external-data boundary.
- Never put Google API keys in source code, committed config, artifacts, exports,
  or logs.
- Native-English source strings pass through without provider calls.
- Persian-containing strings are translated through the provider; do not maintain
  an ad hoc hard-coded translation dictionary.
- Mixed Persian/English strings are translated as semantic units.
- Preserve per-string-path `native` versus `translated` provenance.
- Artifact identity includes source version, target language, provider, model,
  and translation schema version.
- Repeated identical work must reuse the existing artifact.
- A translation of an older source semantic version is historical, not current.
- Translation failure must not alter source evidence/versions.
- English corpus export contains only artifacts for current source versions.
- Translation quality review is separate from parser structural audit.

## 9. Evidence hierarchy

For employer meaning:

```text
original source text       authoritative
translated English text    derived convenience
LLM interpretation         model-derived
```

P1.6 may consume translated English text, but every material claim must retain a
path to original employer text. Never strengthen/weaken employer intent merely
because a translation does so.

## 10. Parser and audit boundaries

The parser extracts source-explicit fields and complete source text. It does not
infer employer intent.

A clean structural audit does not prove translation quality or semantic
interpretation. Missing optional source fields alone are not parser failures.

## 11. Development rules

- Build complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network/model/provider calls.
- Keep CLI focused on composition/validation.
- Keep SQL behind focused repository boundaries.
- Treat acquired content as untrusted data.
- Keep LM Studio behind inference interfaces and translation behind translation
  interfaces.
- Use typed configuration and versioned schemas.
- Prefer explicit failure/review states over guesses.
- Keep runtime data, config, secrets, exports, personal evidence, and model files
  out of Git.
- Add deterministic tests for normalization, selection, persistence, translation,
  export, and orchestration.
- Normal tests must not contact Jobinja, Google Cloud, or LM Studio.
- Avoid dependencies/abstractions without a current use.

## 12. Source acquisition discipline

Use public Jobinja pages only. Preserve attribution/canonical URLs. Validate
redirects. Enforce timeouts, delays, page/request/response/batch bounds.

Do not implement login automation, CAPTCHA/access-control bypass, proxy rotation,
authenticated scraping, unrestricted crawling, or automatic applications.

## 13. External translation discipline

When Google translation is enabled:

- send only parsed job-advertisement text required for English projection;
- do not send personal capability/profile data through this pipeline;
- use bounded provider retries/batches;
- retain provider/model/schema metadata;
- retain failed attempts without corrupting source data;
- recommend API-key restriction/quota controls;
- do not silently enable translation for existing installations.

## 14. LLM extraction discipline

When P1.6 begins:

- require versioned prompts/schemas;
- validate structured output locally;
- retain request/raw response/model/parameters/timing;
- require original-source evidence for material claims;
- distinguish source-explicit, translation-derived, and model-inferred content;
- measure quality on a reviewed real-job corpus;
- never grant the model shell/filesystem/browser/unrestricted network tools.

## 15. Change discipline

A material change states milestone requirement, changed files, behavior,
deterministic tests, live acceptance required, and remaining exclusions.

Update existing controlling docs for material product/architecture changes instead
of creating unnecessary governance files.

## 16. Definition of done

An increment is done only when:

- intended workflow functions locally;
- Ruff and tests pass;
- acceptance criteria are met;
- failures are inspectable;
- configuration/operation are reproducible;
- docs match behavior;
- privacy/external-data boundaries are explicit;
- no unrelated future scope is claimed.

Work directly on `main` unless a concrete isolation need appears.
