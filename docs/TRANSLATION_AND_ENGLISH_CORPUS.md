# Translation and English Corpus

## 1. Purpose

JobHunter preserves employer text in its original language and may also create a
separate English representation for downstream local LLM analysis, SQL/analytics,
and later machine-learning experiments.

Translation is a **derived representation**. It never replaces source evidence and
never creates a new employer-content semantic version by itself.

LM Studio is the default translation provider because it preserves JobHunter's
local-first operating model. Google Cloud Translation remains an optional external
provider.

## 2. Data flow

```text
immutable Jobinja HTML
→ deterministic parser-v2 source fields
→ JobPostingVersion / semantic source version
→ translation decision
   ├─ no Persian text → native-English identity projection
   └─ Persian or mixed text → configured TranslationProvider
        ├─ LM Studio local structured translation (default)
        └─ Google Cloud Translation (optional external provider)
→ versioned English translation artifact
→ current English corpus / JSONL export
→ later LLM analysis, embeddings, NLP, or ML
```

The original source version remains authoritative throughout this flow.

## 3. Three distinct records

JobHunter keeps these records separate.

### Source semantic version

Represents what the employer advertisement says. A source change creates a new
semantic version.

### Translation artifact

Represents one English projection of one exact source semantic version under one
translation provider/model/schema combination.

Important fields:

- source detail-version ID;
- source semantic SHA-256;
- source language;
- target language;
- provider name;
- exact provider model;
- translation schema version;
- translated fields;
- complete English document;
- per-segment provenance;
- translated and native segment counts;
- projection SHA-256;
- creation timestamp.

### Translation attempt

Represents an operational attempt and has one outcome:

```text
completed
failed
reused
```

A provider or model failure therefore does not alter the source version or destroy a
prior translation artifact.

## 4. Segment provenance

Every string placed into the English projection is classified as:

```text
native
translated
```

Examples:

```text
Source: Python
English: Python
Origin: native

Source: مهندس هوش مصنوعی
English: Artificial Intelligence Engineer
Origin: translated

Source: تسلط بر Python و Docker
English: Proficiency in Python and Docker
Origin: translated
```

A mixed Persian/English sentence is translated as one semantic unit. Native technical
terms containing no Persian characters pass through unchanged.

This allows later experiments to select:

- all English content;
- native-English segments only;
- translated segments only;
- mixed jobs only;
- one provider/model/version only.

## 5. LM Studio provider — default

The default provider is:

```toml
translation_provider = "lm-studio"
```

It uses LM Studio's OpenAI-compatible local endpoints:

```text
GET  /v1/models
POST /v1/chat/completions
```

Translation requests use JSON-schema structured output. The model must return one
object containing an ordered set of translation items with integer IDs and translated
text. JobHunter then validates:

- the response is valid JSON;
- the `translations` list exists;
- result count equals input count;
- every input ID appears exactly once;
- no unexpected IDs exist;
- every translation is non-empty;
- final output is restored to exact input order.

Malformed output is rejected and never becomes an English artifact.

### Translation instruction contract

The provider identifier is currently:

```text
lm-studio-translation-v1
```

The version is intentional. The prompt contract requires the local model to:

- translate complete Persian or mixed Persian-English text;
- preserve factual meaning and requirement strength;
- preserve uncertainty, modality, negation, numbers, dates, and names;
- preserve standard technical terms and acronyms when already natural in English;
- avoid summarizing, explaining, classifying, inferring, or adding information;
- return exactly one translation per source segment.

A future material prompt-policy change must receive a new provider-contract version so
old and new translation artifacts are not silently treated as equivalent.

## 6. LM Studio model selection

Model selection is deliberately fail-closed.

Priority:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic selection only when exactly one model is visible
```

A dedicated translation model may therefore be configured without changing the model
used later for general JobHunter inference:

```toml
lm_studio_model = "general-analysis-model"
translation_lm_studio_model = "translation-model"
```

If neither is configured:

- exactly one visible LM Studio model → automatically selected;
- zero visible models → translation fails visibly;
- multiple visible models → translation fails and requires an explicit model ID.

This avoids accidentally creating corpus data with an arbitrary local model.

Inspect exact model IDs with:

```bash
jobhunter translations models
```

## 7. LM Studio request bounds

Translation uses bounded local requests:

```toml
translation_batch_limit = 20
translation_timeout_seconds = 30.0
translation_max_retries = 1
translation_lm_studio_max_tokens = 4096
translation_lm_studio_character_target = 6000
```

A job may contain several translatable fields. JobHunter groups unique Persian-bearing
segments into bounded model requests using both:

- a maximum item count per request;
- an approximate input-character target.

A single segment larger than the target is sent intact rather than truncated.
JobHunter never shortens the employer text simply to satisfy a batching heuristic.

Transport retries remain bounded to configured connection/transient-server conditions.
Model-output truncation is handled separately and conservatively when LM Studio returns
`finish_reason = "length"`:

1. a truncated multi-segment request is split recursively into smaller segment groups;
2. if one individual segment still truncates, its output-token budget is doubled;
3. the single-segment budget may increase only up to the hard local cap of 32,768
   output tokens;
4. if the model still truncates at that cap, the translation fails visibly.

The original source segment is never shortened during this recovery. Other malformed
structured output is rejected rather than repaired heuristically or written into the
English corpus.

## 8. Structured-output compatibility

LM Studio supports JSON-schema structured output through its OpenAI-compatible chat
completions endpoint, but structured-output capability is model-dependent.

Operationally:

- use a chat/instruction model with reliable structured-output support;
- run `jobhunter doctor --smoke` for the general configured model when applicable;
- perform a one-job translation acceptance test before translating the corpus;
- inspect semantic fidelity, not only JSON validity.

A model that produces valid JSON but poor Persian→English translation is not accepted
merely because the technical call succeeds.

## 9. Local privacy boundary

With the default provider:

```toml
translation_provider = "lm-studio"
```

parsed job text remains on the machine and is sent only to the configured LM Studio
server URL. In normal local use that URL should be a loopback address such as:

```text
http://127.0.0.1:1234/v1
```

If the user deliberately exposes LM Studio on another host or network interface, that
network boundary becomes part of the user's local deployment configuration.

No Google API key is required for LM Studio translation.

## 10. Optional Google Cloud Translation provider

Google remains available as an explicit alternative:

```toml
translation_provider = "google-cloud"
google_translation_model = "nmt"
```

The Google provider uses the official Cloud Translation Basic v2 REST API and:

- sends the API key in the `x-goog-api-key` header;
- sends plain text rather than HTML;
- targets English;
- batches provider requests;
- preserves returned ordering;
- uses bounded timeout and retry settings;
- never stores the API key in translation artifacts.

Using Google means parsed job text intentionally leaves the machine. Keep credentials
outside the repository:

```bash
export JOBHUNTER_GOOGLE_TRANSLATION_API_KEY='...'
```

Google is optional and is no longer required for the normal JobHunter path.

## 11. Native-English behavior

A source version containing no Persian text does not need an LLM or cloud translation
request.

JobHunter records an identity artifact with:

```text
provider_name = source-identity
provider_model = native-english
translated_segment_count = 0
```

This gives native-English and translated jobs the same downstream corpus shape while
retaining their origin.

## 12. Idempotency and translator upgrades

Artifact identity includes:

```text
source detail version
+ target language
+ provider contract
+ provider model
+ translation schema version
```

Running the same translation again records `reused` and references the existing
artifact.

A materially changed job creates a new source version and therefore requires a new
English artifact.

Changing the LM Studio model, provider contract, Google model, or projection schema
creates a distinct artifact instead of overwriting history.

## 13. Current-version safety

Only the current successfully parsed source semantic version may have a current
English artifact.

If a job receives a newer semantic version:

```text
old English artifact
→ retained historically
→ no longer current
```

If the newest source version is `partial` or `parse_failed`, JobHunter does not fall
back to an older translation and present it as current data.

This prevents stale translated content from silently entering future LLM/ML datasets.

## 14. English projection contents

Parser metadata such as `parser_version` and source `language` are stored as artifact
metadata rather than copied into the projected job fields.

The projected fields include available source fields such as:

- title;
- company;
- job category;
- location;
- employment type;
- minimum experience;
- salary;
- source skill tags;
- gender;
- military-service requirement;
- education;
- publication/expiration dates;
- complete job description;
- company description.

Missing values remain missing. Translation must not invent a source field.

## 15. Complete English document

Alongside structured fields, every artifact includes one canonical English document.
It is rendered from the projected fields and is convenient for:

- local LLM prompts;
- embeddings;
- text classification;
- clustering;
- topic modelling;
- information retrieval;
- reproducible NLP/ML experiments.

Structured English fields remain the preferred source for deterministic queries.

## 16. CLI

Inspect corpus/config state without invoking a translator:

```bash
jobhunter translations status
```

Inspect exact LM Studio model IDs:

```bash
jobhunter translations models
```

Translate a bounded missing queue:

```bash
jobhunter translations run --missing --limit 20
```

Translate explicit jobs:

```bash
jobhunter translations run tpLF tmW1 tmkE
```

Inspect one current English artifact:

```bash
jobhunter translations show tpLF
```

Export the current English corpus:

```bash
jobhunter translations export
```

Default output:

```text
data/exports/job_english_corpus.jsonl
```

Only artifacts belonging to each job's latest successfully parsed source version are
exported.

## 17. JSONL corpus schema

Each line contains:

```text
schema_version
source
source_job_id
source_detail_version_id
source_semantic_sha256
source_language
target_language
english_origin
translation metadata
segment_provenance
english_fields
english_document
```

`english_origin` currently distinguishes:

```text
native
translated_or_mixed
```

The source database remains authoritative for original Persian, English, or mixed
employer text.

## 18. Automatic translation after sync

After one-job quality acceptance, local automatic translation can be enabled:

```toml
translation_enabled = true
translation_auto_after_sync = true
translation_provider = "lm-studio"
translation_batch_limit = 20
```

Then:

```bash
jobhunter jobinja sync
```

runs:

```text
discovery
→ detail acquisition
→ deterministic parser audit
→ bounded missing English-projection queue
```

Jobs checked during that sync are prioritized in the translation queue. Translation
failures are reported independently from successful acquisition.

## 19. Evidence rule for later LLM analysis

A translated English passage is a convenience representation, not employer evidence.

Later analytical records may reference an English passage for readability, but every
material claim must still retain a path to original source text/evidence.

Example:

```text
Original employer text:
آشنایی با Docker

Faithful translation:
Familiarity with Docker
```

If any translator renders that as `Proficiency with Docker`, JobHunter must not upgrade
the employer requirement because of the derived wording.

## 20. Search vocabulary is data, not Python logic

The bilingual search vocabulary is packaged separately in:

```text
src/jobhunter/data/search_catalog.toml
```

Python loads and validates the catalog. Terms are not embedded as career-vocabulary
tuples in `search_registry.py`.

A complete replacement catalog can be configured:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

This makes acquisition vocabulary independently editable, versionable, testable, and
replaceable without source-code changes.

## 21. Translation-quality acceptance

Technical success is not enough. Before enabling bulk/automatic translation, review a
representative Persian/mixed corpus for:

- requirement-strength preservation;
- negation and uncertainty;
- technical terminology;
- job-title rendering;
- employment/experience/education wording;
- long-description completeness;
- company/proper-name handling;
- mixed Persian-English fluency;
- omissions or hallucinated additions.

A later translation golden corpus should store approved source/English pairs and allow
provider/model comparisons before a translation model change becomes the default.

## 22. Current limitations

- English is the only derived target language currently supported.
- Translation quality is not yet scored against a manually reviewed Persian→English
  golden corpus.
- Glossary/terminology locking is not implemented yet.
- Structured output depends on the selected LM Studio model's capabilities.
- The English corpus is not yet consumed by P1.6 analysis because that increment has
  not started.
- Machine learning may consume this corpus later, but translated text must stay
  labelled so experiments can control translation-induced bias.

These boundaries keep translation useful without mixing it into authoritative source
parsing.
