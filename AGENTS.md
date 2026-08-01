# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product priority

JobHunter is a real repeated-use local utility. Prefer dependable, inspectable behavior
over impressive complexity. Speed means coherent useful increments, not bypassing evidence,
bounds, tests, provenance, or state.

## 2. Required reading order

Before material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/LOCAL_WEB_APP.md`
5. `docs/SEARCH_CONFIGURATION.md`
6. `docs/TRANSLATION_AND_ENGLISH_CORPUS.md`
7. `docs/ACQUISITION_OPERATIONS.md`
8. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
9. `docs/SOURCE_POLICY.md`
10. `docs/IMPLEMENTATION_PLAN.md`
11. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`

## 3. Accepted foundation

Live-accepted before the browser increment:

- M0 local foundation;
- P1.1/P1.2 bounded repeat-safe discovery;
- explicit/missing/refresh-due detail acquisition;
- immutable raw search/detail evidence;
- Jobinja parser v2;
- semantic source versions independent from volatile HTML;
- successful/failed fetch observations;
- parser audit;
- data-driven bilingual search catalog;
- local LM Studio structured translation;
- 15/15 current English artifacts;
- current English JSONL export;
- bounded recovery from real LM Studio output truncation.

Live evidence includes 79 unique discovered jobs in the initial accepted discovery corpus,
zero new logical jobs on identical rerun, fifteen structurally clean current source jobs,
and fifteen current English artifacts.

The local web interface is implemented but remains pending deterministic/live acceptance.

## 4. Interaction-surface rules

JobHunter has two interfaces:

```text
local browser UI   normal repeated human use
CLI                automation/debugging/advanced operation
```

Both must call the same application services and use the same SQLite/evidence records.
Do not duplicate parser, source, versioning, translation, or lifecycle logic in the UI.

The browser may have focused read models for presentation but must not become a second
durable data store.

## 5. Web application rules

- Keep the app loopback-first.
- Non-loopback binding requires explicit operator intent.
- Every mutating HTML form requires CSRF validation.
- Do not expose source/model mutation through unauthenticated cross-origin endpoints.
- Ship CSS/JavaScript/icons locally; do not introduce CDN runtime dependencies.
- Keep Content Security Policy restrictive.
- Do not expose Swagger/OpenAPI UI unless a concrete debugging need is approved.
- Run at most one mutable browser operation at a time unless later concurrency is proven safe.
- Long browser operations may use ephemeral runtime state, but durable outcomes belong in
  existing acquisition/observation/translation records.
- Browser buttons must respect the same page/request/detail/translation bounds as CLI paths.
- Keep advanced persistent configuration explicit in `jobhunter.toml` until a proper
  configuration-write design is justified.
- Avoid adding a Node/npm frontend toolchain while server-rendered Python remains sufficient.

## 6. Search-catalog rules

- Career search words live in TOML data, not Python tuples/constants.
- Pack/profile identifiers should remain stable once published.
- A complete catalog may be replaced through `jobinja_search_catalog_path`.
- Use small custom groups for personal additions.
- Preserve display terms; normalize only for identity/deduplication/exclusion.
- Keep Persian and English forms when real listings use both.
- Interleave selected packs for bounded cross-domain coverage.
- Raw URLs remain the escape hatch for Jobinja-owned filters.
- Search vocabulary is not a career taxonomy and does not prove relevance.

## 7. Acquisition bounds

- Jobinja requests remain sequential with configured delay.
- Discovery enforces a global request budget internally.
- Budget exhaustion sends no extra request and is not a failure.
- Detail batches contain at most 50 unique jobs.
- Sync missing + refresh limits may not exceed 50.
- Raw evidence is written before parsing.
- One search/job failure must not discard successful work.
- Source acquisition remains independent from LM Studio/translation availability.

## 8. Record boundaries

Never conflate:

```text
JobPosting                    logical source identity
SearchPageSnapshot            exact search response
JobPostingVersion             meaningful employer-content history
JobDetailFetchObservation     operational source checks
JobTranslationArtifact        derived English view of one source version
JobTranslationAttempt         operational translation history
Raw evidence                  exact source bytes + metadata
Browser WebOperation          ephemeral UI runtime state only
```

Translator/model/schema/prompt-contract changes do not create source semantic versions.
Browser operation cards do not replace durable run/attempt records.

## 9. Translation rules

- `lm-studio` is the normal local-first translation provider.
- `google-cloud` remains optional external processing.
- Native-English strings pass through without translation calls.
- Persian-containing strings use the configured provider; do not hard-code a translation
  dictionary.
- Mixed Persian/English strings translate as semantic units.
- Preserve per-string `native` versus `translated` provenance.
- Artifact identity includes source version, target language, provider contract, exact model,
  and translation schema.
- Repeated identical work must reuse artifacts.
- Older source-version translations are historical, not current.
- A newer incomplete parse blocks an older translation from current use/export.
- Translation failure never alters source evidence/versions.
- Translation quality review remains separate from parser structural audit.

## 10. LM Studio translation discipline

The local translator must:

- use configured LM Studio URL/token;
- select model by dedicated translation model, general model, then exactly-one-visible model;
- fail closed on ambiguous model selection;
- use structured JSON output;
- validate exact translation count and IDs;
- reject empty/malformed/missing/extra output;
- keep bounded request and output limits;
- never shorten employer source text to satisfy batching;
- recover explicit output truncation only through bounded splitting/token-budget increases;
- preserve versioned provider/prompt contract identity.

A material translation-policy change increments the provider contract.

## 11. Evidence hierarchy

```text
original employer text       authoritative
translated English text      derived convenience
future LLM interpretation    model-derived
```

P1.6 may consume English text for convenience, but material claims must remain traceable to
original source evidence.

## 12. Parser/audit boundaries

The parser extracts source-explicit fields and complete source text. It does not infer
employer intent.

A clean structural audit does not prove translation quality or semantic interpretation.

## 13. Development rules

- Build complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network/model/provider calls.
- Keep CLI and web handlers focused on composition/validation.
- Keep SQL behind focused repositories/read models.
- Treat acquired content as untrusted data.
- Keep P1.6 analysis and translation as separate interfaces even when both use LM Studio.
- Use typed configuration and versioned schemas/contracts.
- Prefer explicit failure/review states over guesses.
- Keep runtime data, config, secrets, exports, personal evidence, and model files out of Git.
- Normal tests must not contact Jobinja, Google Cloud, or LM Studio.
- Add deterministic tests for every important browser mutation/security boundary.
- Avoid dependencies/abstractions without a current use.

## 14. Source acquisition discipline

Use approved public Jobinja pages only. Preserve canonical URLs/attribution. Validate
redirects. Enforce timeouts, delays, request/page/response/batch bounds.

Do not implement login automation, CAPTCHA/access-control bypass, proxy rotation,
authenticated scraping, unrestricted crawling, or automatic applications.

## 15. P1.6 discipline

When semantic analysis begins:

- require versioned prompts/schemas;
- validate structured output locally;
- retain request/raw response/model/parameters/timing;
- require original-source evidence for material claims;
- distinguish source-explicit, translation-derived, and inferred content;
- measure quality on reviewed real-job corpora;
- never grant the analysis model shell/filesystem/browser/unrestricted network tools.

## 16. Definition of done

An increment is done only when:

- intended workflow functions locally;
- Ruff and tests pass;
- live acceptance criteria are met when external/runtime behavior matters;
- failures are inspectable;
- configuration/operation are reproducible;
- docs match behavior;
- privacy/network boundaries are explicit;
- no unrelated future scope is claimed.

Work directly on `main` unless a concrete isolation need appears.
