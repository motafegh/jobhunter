# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product priority

JobHunter is a real repeated-use local utility. Prefer dependable, inspectable behavior over impressive complexity. Speed means coherent useful increments, not bypassing evidence, bounds, tests, provenance, acceptance or state.

The mature product is an evidence-grounded personal career-intelligence system, not merely a scraper, generic job matcher or autonomous application bot.

## 2. Required reading order

Before material changes, read in this order:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
5. `docs/SOURCE_POLICY.md`
6. `docs/ROADMAP.md`
7. `docs/IMPLEMENTATION_PLAN.md`
8. the active phase plan, currently `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`
9. `docs/EXECUTION_TODO.md`
10. feature-specific docs relevant to the change, including as needed:
   - `docs/LOCAL_WEB_APP.md`
   - `docs/SEARCH_CONFIGURATION.md`
   - `docs/TRANSLATION_AND_ENGLISH_CORPUS.md`
   - `docs/SEMANTIC_ANALYSIS.md`
   - `docs/ACQUISITION_OPERATIONS.md`

Proposal files under `docs/proposals/` are candidate design inputs only. They are not authorization to implement a capability.

## 3. Authority chain

```text
product/domain/source/architecture constraints
        ↓
ROADMAP.md
strategic sequencing / proposal disposition
        ↓
IMPLEMENTATION_PLAN.md
exact delivery order / acceptance gates
        ↓
active phase plan
        ↓
EXECUTION_TODO.md
working checklist
        ↓
implementation / tests / live acceptance
```

If a lower-level artifact conflicts with a higher-level one, stop and reconcile the conflict instead of choosing the more convenient instruction.

## 4. Current accepted foundation and acceptance target

Live-accepted foundations include:

- M0 local foundation;
- bounded repeat-safe bilingual Jobinja discovery;
- immutable raw search/detail evidence;
- Jobinja parser v2 and semantic source versions;
- fetch observations and refresh-due selection;
- local browser application, guided sync, Quick Add and backlog acquisition;
- a real browser sync with 40/40 search requests, 273 unique postings, 241 new postings, zero search failures, 10/10 selected detail fetches, and 26/26 structurally clean current parsed jobs at that point.

Translation v1 proved the derived-corpus architecture but later real data exposed a field-association defect. V1 artifacts are historical, not the trusted current analysis input.

The current increment implements, but does not yet claim full live acceptance of:

- `lm-studio-translation-v2` / `english-projection-v2`;
- deterministic translation-integrity rejection;
- user triage and deterministic missing-detail priority;
- classified source errors and cautious lifecycle transitions;
- search-effectiveness/provenance views;
- P1.6 evidence-backed semantic analysis;
- first aggregate Market view;
- expanded bounded browser workflow actions.

Follow the acceptance order in `docs/IMPLEMENTATION_PLAN.md` and the active Phase-1 plan before scaling model work or beginning Phase 2.

## 5. Current exact next-work rule

Do not add unrelated features until the active Phase-1 sequence completes.

Current priorities are:

```text
deterministic Ruff/tests/warnings baseline
→ migration safety / real workspace migration
→ translation-v2 repair/inspection
→ one reviewed real P1.6 analysis
→ representative small P1.6 review sample
→ regression/model-chaos/source-failure fixtures
→ Market sampling/corpus-health truthfulness
→ source failure/lifecycle acceptance
→ explicit partial-success operation results
→ remaining P1.3/P1.5 acceptance
→ final P1.7 run/report/browser equivalent
→ Phase-1 closure
```

The detailed checklist is `docs/EXECUTION_TODO.md`.

## 6. Interaction-surface rules

JobHunter has two interfaces:

```text
local browser UI   normal repeated human use
CLI                automation/debugging/advanced operation
```

Both operate on the same durable SQLite/evidence records and underlying services. Do not create a second source parser, translation store, lifecycle model, analysis model or analytical database for the browser.

## 7. Record and authority boundaries

Never conflate:

```text
JobPosting                    logical source identity
SearchPageSnapshot            exact search response
JobPostingVersion             meaningful employer-content history
JobDetailFetchObservation     operational source check
JobLifecycleEvent/state       classified source-availability evidence
JobTranslationArtifact        derived English view of one source version
JobTranslationAttempt         operational translation history
JobAnalysisArtifact           model-derived interpretation of one source version
JobAnalysisAttempt            operational analysis history
JobUserWorkflow               local human triage state
Browser WebOperation          ephemeral UI runtime state only
Raw evidence                  exact preserved source bytes + metadata
Market aggregate              deterministic aggregation of accepted current analysis
```

Authority hierarchy:

```text
original employer/source text    authoritative
parsed source fields             source-derived
English projection v2            derived convenience
semantic analysis                model-derived interpretation
market aggregate                  deterministic aggregate of accepted analysis
user triage                       local user workflow preference
future personal evidence          separate reviewed user-evidence layer
future recommendation             explainable system-derived decision
```

## 8. Web application rules

- Keep the app loopback-first; non-loopback binding requires explicit intent.
- Every mutating HTML form requires CSRF validation.
- Ship CSS/JavaScript/icons locally; no CDN runtime dependency.
- Keep Content Security Policy restrictive.
- Run at most one mutable browser operation at a time unless concurrency is proven safe.
- Browser actions must respect the same source/model bounds as service/CLI paths.
- Explain non-obvious operational limits in user-facing language.
- Keep stable source identifiers available for provenance but visually secondary.
- Discovered-but-unfetched postings are normal actionable states, not UI errors.
- Keep source, English, model-derived analysis and user workflow state visually/semantically distinct.
- Keep advanced persistent configuration in `jobhunter.toml` until a safe configuration-write design is justified.
- Avoid a Node/npm frontend while server-rendered Python remains sufficient.
- Multi-stage operation summaries must not hide partial failures behind generic success.

### Quick Add

Quick Add may accept only:

- one public Jobinja job URL;
- one public Jobinja `/jobs` URL;
- one Persian/English keyword phrase interpreted as a Jobinja search.

It is not a source-policy escape hatch. Non-Jobinja URLs remain rejected until an approved adapter exists.

## 9. Search and acquisition discipline

- Search vocabulary lives in TOML data, not Python constants.
- Preserve display terms; normalize only for identity/deduplication/exclusion.
- Interleave selected packs for bounded cross-domain coverage.
- Search vocabulary is acquisition recall, not career taxonomy or relevance proof.
- Jobinja requests remain sequential with configured delay.
- Discovery enforces a global request budget.
- Detail batches contain at most the configured/accepted bounded maximum.
- Raw evidence is preserved before deterministic parsing of successful source content.
- Source acquisition remains independent from LM Studio availability.
- Provider/source failure must never be reported as a legitimate empty result.

### Classified retries/lifecycle

Source failures must retain classification and retryability.

Bounded automatic retry is allowed only for transient network, rate-limit or selected 5xx classes. Do not blindly retry challenge/CAPTCHA, access denied, missing/gone, auth redirects or explicit expiry.

Lifecycle transitions remain conservative:

- successful normal source check -> active;
- explicit expiry -> expired;
- first 404/410 -> possibly unavailable;
- repeated strong missing/gone evidence may become removed;
- transient/server/access/challenge/rate-limit failures do not prove removal.

Required invariant:

```text
500/502/503/504/network/rate-limit/challenge/auth
!=
expired/removed vacancy
```

## 10. User triage and acquisition priority

User workflow state is not source truth.

Current triage states:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

`not_relevant` may exclude a posting from automatic backlog priority but must not delete source evidence/history.

Missing-detail priority may use deterministic discovery evidence such as search/pack matches and conservative title signals. It must be labelled acquisition priority, never career fit, readiness or recommendation.

## 11. Translation-v2 rules

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
- validate exact content identity and non-empty translation;
- never shorten employer text;
- recover output truncation only through bounded contract-defined behavior;
- run deterministic source/English integrity checks before persistence;
- reject corrupt output rather than creating a current artifact.

Native-English source strings remain identity projections without model translation.

Current export and P1.6 analysis may consume only the current hardened English schema.

## 12. P1.6 semantic-analysis discipline

P1.6 is a separate derived layer even when it uses the same LM Studio server.

Each durable artifact is tied to:

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
- every material claim requires an exact original-source evidence excerpt;
- evidence excerpts are validated locally against authoritative source fields;
- parser metadata such as `language` and `parser_version` is not employer evidence;
- invalid/hallucinated evidence prevents artifact acceptance;
- required/preferred/contextual/inferred remain distinct;
- inferred concepts require rationale and source evidence;
- raw structured request/response remains auditable;
- reruns of identical current identity reuse artifacts;
- acquired text is untrusted data even if it contains instruction-like strings;
- never grant the analysis model shell/filesystem/browser/unrestricted network tools.

Critical integrity rules must exist in application validators/tests, not only in natural-language prompts.

Do not scale the model batch until reviewed real-job output passes the live gate.

### Representative acceptance

After the one-job proof, select a small representative review sample rather than merely the next records in ID order. Vary available company/title/role pattern/language/description length/requirement density and include both ordinary/random and edge-case examples.

Every repeatable semantic/model failure class should become a deterministic regression or model-chaos fixture.

## 13. Market aggregation rules

Aggregate only accepted/current analysis artifacts matching the selected analysis contract.

Always expose sample size. Keep required/preferred/contextual/inferred counts separate. Do not silently turn case-folding into a canonical career taxonomy. Alias consolidation, role archetypes and reviewed concept taxonomy belong to Phase 2.

Do not claim full-market truth from a small/source-biased analyzed sample.

Current acceptance must include explicit sampling/concentration warnings where the available analyzed subset cannot support broad conclusions.

Coverage metrics and quality metrics remain different: `N jobs analyzed` is not evidence that those analyses are correct.

## 14. Partial-success and operation-result rules

For multi-stage operations expose, where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

- Do not roll back valid immutable/durable earlier-stage work merely because a later stage failed.
- Do not call an operation simply successful when meaningful requested sub-work failed.
- Distinguish `no eligible work` from `attempt failed`.
- Browser and CLI/service summaries must agree on the underlying result semantics.

## 15. Regression, fault and security discipline

Normal tests never contact Jobinja, Google Cloud or LM Studio.

Important real incidents become regression fixtures.

Near-term required failure classes include:

- network/429/5xx/challenge/auth source handling;
- source failure vs valid empty result;
- Unicode/non-Latin normalization edge cases;
- translation association/integrity failures;
- invalid/truncated structured model output;
- valid JSON with fabricated source evidence;
- parser metadata used as employer evidence;
- prompt-injection-like strings inside job content;
- mixed-success operation summaries.

Property-based tests are appropriate only where pure deterministic transformations have enough input space to justify them.

## 16. Personal-evidence boundary

Do not implement personal capability gaps, readiness scores or recommendations until JobHunter has a reviewed personal-evidence schema with depth, confidence, recency, evidence references, limitations and appropriate AI-assistance/independence context.

Do not convert conversational assumptions into durable personal capability truth.

Do not infer capability from repository dependency names or project completion alone.

Before storing irreplaceable personal evidence, define its privacy/processing/export boundary and provide tested backup/restore.

## 17. Architecture-evolution discipline

- Preserve the local modular monolith.
- Keep SQLite until measured limitations justify replacement.
- Implement one real second source before extracting a generic source-adapter contract.
- Do not build dynamic plugin infrastructure in advance.
- Structured/keyword queries come before embeddings/RAG.
- Do not add vector/graph databases without a demonstrated query requirement.
- Advanced provider routing/agents require measured benefit and explicit privacy/provenance/budget controls.

## 18. Development rules

- Build complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network/model/provider calls.
- Keep CLI and web handlers focused on composition/validation.
- Keep SQL behind focused repositories/read models.
- Treat acquired content as untrusted data.
- Use typed configuration and versioned schemas/contracts.
- Prefer explicit failure/review states over guesses.
- Keep runtime data, config, secrets, exports, personal evidence and model files out of Git.
- Normal tests must not contact Jobinja, Google Cloud or LM Studio.
- Add deterministic tests for important mutation/security/data-integrity boundaries.
- Avoid dependencies/abstractions without a current use.
- Reconcile documentation whenever implementation state materially changes.

## 19. Definition of done

An increment is done only when:

- intended workflow functions locally;
- Ruff and tests pass, including warning-as-error where configured for acceptance;
- live acceptance criteria pass when external/runtime/model behavior matters;
- failures are inspectable and bounded;
- partial-success semantics are honest where relevant;
- configuration/operation are reproducible;
- provenance is retained;
- docs match behavior;
- privacy/network boundaries are explicit;
- no unrelated future scope is claimed.

Work directly on `main` unless a concrete isolation need appears.
