# JobHunter

JobHunter is a local-first personal career-intelligence application.

It collects postings from user-approved public sources, preserves original
evidence, distinguishes logical jobs from raw HTTP snapshots and semantic
versions, and prepares trustworthy local data for later evidence-backed career
analysis.

JobHunter is a **utility-first personal application**. Reliability,
inspectability, idempotency, configurability, and daily usefulness control its
engineering decisions.

## Current workflow

```text
data-driven bilingual search catalog
→ inspectable search plan
→ repeat-safe Jobinja discovery
→ immutable search-page evidence
→ missing and refresh-due detail selection
→ immutable detail evidence
→ deterministic Jobinja parsing
→ semantic versioning
→ fetch-observation history
→ structural parser audit
→ optional versioned English projection
→ current English corpus export
```

Acquisition remains independent from translation and later P1.6 analysis. The
normal translation path is local LM Studio; Google Cloud remains an optional
external provider.

## Quick start

Requires Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
jobhunter init
```

The generated configuration enables the broad bilingual
`ai-security-python` search profile with bounded request and detail budgets.
Translation remains disabled until explicitly enabled.

Inspect the system before network use:

```bash
jobhunter jobinja catalog --show-terms
jobhunter jobinja plan
jobhunter translations status
```

Run the normal acquisition workflow:

```bash
jobhunter jobinja sync
```

## Data-driven bilingual search registry

Search vocabulary is data, not Python logic.

The packaged catalog lives at:

```text
src/jobhunter/data/search_catalog.toml
```

It defines profiles, packs, descriptions, Persian terms, English terms, and a
catalog version. Python code loads and validates the file.

The default profile:

```toml
jobinja_search_profiles = ["ai-security-python"]
```

combines:

```text
ai-ml
llm-applications
python-data
defensive-security
ai-security
network-platform
```

The catalog includes AI, Machine Learning, LLM, RAG, agents, Python, data
engineering, SOC, SIEM, detection engineering, security automation, AI
security, Linux, networking, DevOps, and Persian counterparts.

Exact terms are inspectable with:

```bash
jobhunter jobinja catalog --show-terms
```

### Replace the whole search catalog without editing Python

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

The replacement uses the same TOML schema as the packaged catalog.

### Add small user-specific groups

```toml
[[jobhunter.jobinja_keyword_groups]]
name = "My highest-priority hybrid roles"
terms = [
  "مهندس امنیت هوش مصنوعی",
  "AI Security Engineer",
  "Python Security Automation",
  "مهندس تشخیص",
  "Detection Engineer",
]
enabled = true
max_pages = 1
```

See [Search Configuration](docs/SEARCH_CONFIGURATION.md).

## Search planning

Plan configured searches without network access:

```bash
jobhunter jobinja plan
```

Plan an explicit profile:

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Generated pack terms are interleaved round-robin so a bounded window represents
AI/ML, LLM applications, Python/data, defensive security, AI security, and
network/platform searches instead of exhausting one category first.

## Discovery

Run configured discovery:

```bash
jobhunter jobinja discover
```

Discovery is sequential and rate-limited. It reports request-budget usage,
pages, unique/new/known jobs, cross-search overlap, failures, and one stop reason
per search.

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
page_failed
invalid_search
```

Repeated result pages are identified using stable Jobinja job IDs rather than
volatile HTML.

## Acquisition sync

The normal bounded acquisition command is:

```bash
jobhunter jobinja sync
```

Override controls when needed:

```bash
jobhunter jobinja sync \
  --profile ai-security-python \
  --search-limit 40 \
  --request-budget 40 \
  --missing-limit 10 \
  --refresh-limit 5 \
  --refresh-after-hours 24
```

The sync performs discovery, missing/refresh-due detail acquisition, semantic
version decisions, fetch-observation persistence, and structural parser audit.

When translation is enabled with `translation_auto_after_sync = true`, it then
processes a bounded missing-English queue using the configured translation
provider.

## Targeted detail acquisition

```bash
jobhunter jobinja fetch tpLF tmW1 tmkE
jobhunter jobinja fetch --missing --limit 10
jobhunter jobinja fetch --refresh-due --older-than-hours 24 --limit 5
```

Every successful fetch reports its semantic version and fetch-observation ID.
One job failure does not discard successful jobs in the same batch.

## Original source versus English corpus

JobHunter keeps these layers separate:

```text
original employer text
  Persian / English / mixed

semantic source version
  meaningful deterministic advertisement content

English translation artifact
  derived convenience representation
```

Translation never overwrites the original Persian or mixed-language fields.
Changing a translator does not create a new employer-content semantic version.

### Native English

If a source field contains no Persian text, it passes into the English projection
unchanged and is labelled `native`.

### Persian or mixed text

Persian-containing strings are translated and labelled `translated`. Technical
English already embedded in a mixed sentence is handled as part of that semantic
unit rather than through a hard-coded terminology dictionary.

Per-segment provenance is retained so later ML work can distinguish native
English from translated English.

## Local LM Studio translation

LM Studio is the default translation provider:

```toml
translation_enabled = true
translation_auto_after_sync = false
translation_provider = "lm-studio"
translation_target_language = "en"
translation_batch_limit = 20
translation_lm_studio_max_tokens = 4096
translation_lm_studio_character_target = 6000
```

The translator uses LM Studio's local OpenAI-compatible `/v1/models` and
`/v1/chat/completions` endpoints with JSON-schema structured output.

Model selection is fail-closed:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic only when exactly one model is visible
```

Inspect exact model identifiers with:

```bash
jobhunter translations models
```

The prompt contract is versioned as `lm-studio-translation-v1`. It requires the
model to preserve requirement strength, modality, negation, numbers, names, and
technical terminology; it forbids summarization, inference, or additions.
Malformed or incomplete structured responses are rejected rather than stored.

LM Studio translation keeps job text on the configured local LM Studio server
boundary. No Google API key is required.

## Optional Google Cloud Translation

Google Cloud remains supported when an external translation provider is
deliberately desired:

```toml
translation_provider = "google-cloud"
google_translation_model = "nmt"
```

Keep the API key outside the repository:

```bash
export JOBHUNTER_GOOGLE_TRANSLATION_API_KEY='your-restricted-key'
```

Using this provider intentionally sends parsed job text to Google. It is not
required for normal JobHunter operation.

See [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md).

## Translation commands

Inspect configuration and corpus coverage without invoking a translator:

```bash
jobhunter translations status
```

Inspect exact LM Studio model IDs:

```bash
jobhunter translations models
```

Create missing English projections:

```bash
jobhunter translations run --missing --limit 20
```

Translate explicit latest job versions:

```bash
jobhunter translations run tpLF tmW1 tmkE
```

Inspect one current projection:

```bash
jobhunter translations show tpLF
```

Export a separate current English corpus:

```bash
jobhunter translations export
```

Default output:

```text
data/exports/job_english_corpus.jsonl
```

Only artifacts for each job's latest successfully parsed semantic version are
exported.

## English corpus for later LLM/ML work

Each JSONL record includes:

- source job ID;
- source semantic version ID and SHA-256;
- source language;
- translation provider/model/schema metadata;
- `native` versus `translated` segment provenance;
- structured English fields;
- one complete canonical English document.

This can later support local LLM prompts, embeddings, clustering, text
classification, information retrieval, and reproducible ML experiments.

The English translation is not the final evidence authority. A future analytical
claim must remain traceable to original employer text so translation errors
cannot silently strengthen or weaken a requirement.

## Local inspection

```bash
jobhunter jobs list --limit 100
jobhunter jobs show tpLF
jobhunter jobs checks tpLF
jobhunter jobs audit
jobhunter jobs audit --only-issues
```

A clean structural audit means no known parser shape/contamination problem was
detected. It does not prove semantic interpretation.

## Data integrity model

```text
JobPosting
  logical Jobinja identity

SearchPageSnapshot
  exact search-page response

JobPostingVersion
  meaningful deterministic source-content version

JobDetailFetchObservation
  one successful or failed detail-page check

JobTranslationArtifact
  one English projection of one exact source version under one provider/model/schema

JobTranslationAttempt
  completed / failed / reused translation operation

Raw evidence
  exact HTTP bytes plus metadata sidecar
```

Volatile HTML changes do not create false semantic versions. Translator/model
changes do not overwrite source versions or old translation artifacts.

## Evidence storage

Runtime data remains outside Git:

```text
data/evidence/jobinja/search-pages/
data/evidence/jobinja/job-pages/
data/jobhunter.sqlite3
data/exports/
```

Raw HTML is written before parsing. Translation artifacts are derived database
records, not replacements for evidence.

## LM Studio foundation

```bash
jobhunter doctor
jobhunter doctor --smoke
jobhunter translations models
```

Acquisition does not require LM Studio. Translation may use LM Studio when
enabled. P1.6 responsibility/requirement interpretation remains a separate
future analysis boundary even when it later reuses the same local server.

## Development checks

```bash
ruff check .
pytest
```

Normal tests do not contact Jobinja, Google Cloud, or LM Studio. Provider calls
are represented with deterministic mock transports.

## Documentation

- [Product Specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Search Configuration](docs/SEARCH_CONFIGURATION.md)
- [Translation and English Corpus](docs/TRANSLATION_AND_ENGLISH_CORPUS.md)
- [Acquisition Operations](docs/ACQUISITION_OPERATIONS.md)
- [Domain and Analysis Model](docs/DOMAIN_AND_ANALYSIS_MODEL.md)
- [Source Acquisition Policy](docs/SOURCE_POLICY.md)
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Phase 1 Jobinja Automation Plan](docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md)
- [Repository Instructions](AGENTS.md)

## Current status

M0, P1.1, and P1.2 are accepted. Repeat-safe discovery was validated live across
two two-page searches with 79 unique jobs, one cross-search overlap, and zero new
jobs on the identical rerun.

Fifteen structurally varied Jobinja advertisements have complete parser-v2
details and all fifteen pass the deterministic structural audit. Operational
fetch observations and bounded refresh scheduling are live-validated.

The implementation now also includes a data-driven bilingual search catalog,
custom replacement catalogs, local LM Studio and optional Google translation
providers, versioned English artifacts and attempts, native-versus-translated
segment provenance, bounded automatic translation after sync, and current
English-corpus JSONL export.

Translation quality still requires live acceptance against real Persian/mixed
jobs and later a manually reviewed golden corpus. Challenge/login/expired-page
classification, complete lifecycle classification, P1.6 semantic LLM analysis,
combined reports, personal relevance, and career recommendations remain
incomplete.
