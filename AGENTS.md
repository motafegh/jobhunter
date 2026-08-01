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
7. `docs/SEMANTIC_ANALYSIS.md`
8. `docs/ACQUISITION_OPERATIONS.md`
9. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
10. `docs/SOURCE_POLICY.md`
11. `docs/IMPLEMENTATION_PLAN.md`
12. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`

## 3. Accepted foundation and current acceptance target

Live-accepted foundations include:

- M0 local foundation;
- bounded repeat-safe bilingual discovery;
- immutable raw search/detail evidence;
- Jobinja parser v2 and semantic source versions;
- fetch observations and refresh-due selection;
- local browser application, guided sync, Quick Add and backlog acquisition;
- a real browser sync with 40/40 search requests, 273 unique postings, 241 new postings,
  zero search failures, 10/10 selected detail fetches, and 26/26 structurally clean current
  parsed jobs at that point.

Translation v1 proved the derived-corpus architecture but later real data exposed a
field-association defect. V1 artifacts are therefore historical, not the current accepted
analysis input.

The current increment implements, but does not claim live acceptance of:

- `lm-studio-translation-v2` / `english-projection-v2`;
- deterministic translation-integrity rejection;
- user triage and deterministic missing-detail priority;
- classified source errors and cautious lifecycle transitions;
- search-effectiveness/provenance views;
- P1.6 evidence-backed semantic analysis;
- first aggregate Market view.

Follow the acceptance order in `docs/IMPLEMENTATION_PLAN.md` before scaling model work.

## 4. Interaction-surface rules

JobHunter has two interfaces:

```text
local browser UI   normal repeated human use
CLI                automation/debugging/advanced operation
```

Both operate on the same durable SQLite/evidence records and underlying services. Do not
create a second source parser, translation store, lifecycle model, or analytical database
for the browser.

## 5. Record and authority boundaries

Never conflate:

```text
JobPosting                    logical source identity
SearchPageSnapshot            exact search response
JobPostingVersion             meaningful employer-content history
JobDetailFetchObservation     operational source checks
JobLifecycleEvent             classified source-availability evidence
JobTranslationArtifact        derived English view of one source version
JobTranslationAttempt         operational translation history
JobAnalysisArtifact           model-derived interpretation of one source version
JobAnalysisAttempt            operational analysis history
JobUserWorkflow               local human triage state
Browser WebOperation          ephemeral UI runtime state only
Raw evidence                  exact preserved source bytes + metadata
```

Authority hierarchy:

```text
original employer/source text    authoritative
English projection v2            derived convenience
semantic analysis                model-derived interpretation
user triage                       local user workflow preference
market aggregate                  deterministic aggregate of accepted analysis
```

## 6. Web application rules

- Keep the app loopback-first; non-loopback binding requires explicit intent.
- Every mutating HTML form requires CSRF validation.
- Ship CSS/JavaScript/icons locally; no CDN runtime dependency.
- Keep Content Security Policy restrictive.
- Run at most one mutable browser operation at a time unless concurrency is proven safe.
- Browser actions must respect the same source/model bounds as service/CLI paths.
- Explain non-obvious operational limits in user-facing language.
- Keep stable source identifiers available for provenance but visually secondary.
- Discovered-but-unfetched postings are normal actionable states, not UI errors.
- Keep advanced persistent configuration in `jobhunter.toml` until a safe configuration-write
  design is justified.
- Avoid a Node/npm frontend while server-rendered Python remains sufficient.

### Quick Add

Quick Add may accept only:

- one public Jobinja job URL;
- one public Jobinja `/jobs` URL;
- one Persian/English keyword phrase interpreted as a Jobinja search.

It is not a source-policy escape hatch. Non-Jobinja URLs remain rejected until an approved
adapter exists.

## 7. Search and acquisition discipline

- Search vocabulary lives in TOML data, not Python constants.
- Preserve display terms; normalize only for identity/deduplication/exclusion.
- Interleave selected packs for bounded cross-domain coverage.
- Search vocabulary is acquisition recall, not a career taxonomy or relevance proof.
- Jobinja requests remain sequential with configured delay.
- Discovery enforces a global request budget.
- Detail batches contain at most 50 unique jobs.
- Raw evidence is preserved before deterministic parsing of successful source content.
- Source acquisition remains independent from LM Studio availability.

### Classified retries/lifecycle

Source failures must retain classification and retryability.

Bounded automatic retry is allowed only for transient network, rate-limit, or 5xx classes.
Do not blindly retry challenge/CAPTCHA, access denied, missing/gone, auth redirects, or
explicit expiry.

Lifecycle transitions must remain conservative:

- successful normal source check -> active;
- explicit expiry -> expired;
- first 404/410 -> possibly unavailable;
- repeated strong missing/gone evidence may become removed;
- transient/server/access/challenge failures do not prove removal.

## 8. User triage and acquisition priority

User workflow state is not source truth.

Current triage states:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

`not_relevant` may exclude a posting from automatic backlog priority but must not delete its
source evidence/history.

Missing-detail priority may use deterministic discovery evidence such as search/pack matches
and conservative title signals. It must be labelled as acquisition priority, never career
fit, readiness, or recommendation.

## 9. Translation v2 rules

Current trusted contracts:

```text
provider:   lm-studio-translation-v2
projection: english-projection-v2
```

V1 artifacts remain historical and must not be silently relabelled or overwritten.

For Persian/mixed v2 translation:

- translate one semantic source segment per LM Studio request;
- use content-derived response identity;
- require strict structured output;
- validate exact content ID and non-empty translation;
- never shorten employer text;
- recover output truncation only by bounded output-token increases;
- run deterministic source/English integrity checks before persistence;
- reject corrupt output rather than creating a current artifact.

Native-English source strings remain identity projections without model translation.

Current export and P1.6 analysis may consume only the current hardened English schema.
Translation/model/schema changes do not create source semantic versions.

## 10. P1.6 semantic-analysis discipline

P1.6 is a separate derived layer even when it uses the same LM Studio server.

Each artifact must be tied to:

```text
source semantic version
+ supporting current English v2 artifact
+ exact model
+ prompt version
+ analysis schema version
```

The model may extract role purpose, responsibilities and requirements, but:

- original source fields remain authoritative;
- English is a comprehension aid only;
- every material claim requires an original-source evidence excerpt;
- evidence excerpts are validated locally against source fields;
- invalid/hallucinated evidence prevents artifact acceptance;
- required/preferred/contextual/inferred must remain distinct;
- inferred concepts require a rationale and source evidence;
- raw structured request and response must remain auditable;
- reruns of identical current identity reuse artifacts;
- never grant the analysis model shell/filesystem/browser/unrestricted network tools.

Do not scale the model batch until reviewed real-job output passes the live gate.

## 11. Market aggregation rules

Aggregate only accepted current analysis artifacts.

Always expose sample size. Keep required/preferred/contextual/inferred counts separate.
Do not silently turn case-folding into a canonical career taxonomy. Alias consolidation,
role archetypes and reviewed concept taxonomy belong to Phase 2.

Do not claim full-market truth from a small analyzed sample.

## 12. Personal-evidence boundary

Do not implement personal capability gaps, readiness scores, or recommendations until
JobHunter has a reviewed personal-evidence schema with depth, recency, evidence references,
and confidence.

Do not convert conversational assumptions into durable personal capability truth.

## 13. Development rules

- Build complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network/model/provider calls.
- Keep CLI and web handlers focused on composition/validation.
- Keep SQL behind focused repositories/read models.
- Treat acquired content as untrusted data.
- Use typed configuration and versioned schemas/contracts.
- Prefer explicit failure/review states over guesses.
- Keep runtime data, config, secrets, exports, personal evidence, and model files out of Git.
- Normal tests must not contact Jobinja, Google Cloud, or LM Studio.
- Add deterministic tests for important mutation/security/data-integrity boundaries.
- Avoid dependencies/abstractions without a current use.

## 14. Definition of done

An increment is done only when:

- intended workflow functions locally;
- Ruff and tests pass, including warning-as-error where configured for acceptance;
- live acceptance criteria pass when external/runtime/model behavior matters;
- failures are inspectable;
- configuration/operation are reproducible;
- docs match behavior;
- privacy/network boundaries are explicit;
- no unrelated future scope is claimed.

Work directly on `main` unless a concrete isolation need appears.
