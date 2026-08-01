# Translation and English Corpus

## 1. Purpose

JobHunter preserves employer text in its original language and may also create a
separate English representation for downstream local LLM analysis, SQL/analytics,
and later machine-learning experiments.

Translation is a **derived representation**. It never replaces source evidence and
never creates a new employer-content semantic version by itself.

## 2. Data flow

```text
immutable Jobinja HTML
→ deterministic parser-v2 source fields
→ JobPostingVersion / semantic source version
→ translation decision
   ├─ no Persian text → native-English identity projection
   └─ Persian or mixed text → configured TranslationProvider
→ versioned English translation artifact
→ current English corpus / JSONL export
→ later LLM analysis, embeddings, NLP, or ML
```

The original source version remains authoritative throughout this flow.

## 3. Three distinct records

JobHunter keeps these records separate:

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
- provider model;
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

A provider outage therefore does not alter the source version or destroy a prior
translation artifact.

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

A mixed Persian/English sentence is translated as one semantic unit. Native
technical terms that already contain no Persian characters pass through unchanged.

This allows later experiments to select:

- all English content;
- native-English segments only;
- machine-translated segments only;
- mixed jobs only;
- a particular provider/model/version only.

## 5. Google Cloud Translation provider

The implemented external provider uses the official **Google Cloud Translation
Basic v2 REST API**:

```text
POST https://translation.googleapis.com/language/translate/v2
```

The implementation:

- sends the API key in the `x-goog-api-key` header;
- sends plain text rather than HTML;
- targets English;
- explicitly marks translated source segments as Persian (`fa`);
- batches at most 128 text inputs per API request;
- preserves returned ordering;
- records the configured model with every artifact;
- uses bounded timeout and retry settings;
- never stores the API key in translation artifacts.

The default model is:

```toml
google_translation_model = "nmt"
```

Google Cloud also documents support for the standard Translation LLM through the
Basic API when its full model resource name is provided. Changing this model creates
new translation artifacts rather than overwriting old artifacts because model
identity is part of artifact uniqueness.

## 6. Privacy and external-data boundary

Google translation is disabled by default:

```toml
translation_enabled = false
translation_auto_after_sync = false
```

Enabling it means parsed job-advertisement text is intentionally sent to Google
Cloud. This is an exception to JobHunter's local-first default and must therefore be
explicit.

Recommended credential handling:

```bash
export JOBHUNTER_GOOGLE_TRANSLATION_API_KEY='...'
```

Do not commit the key to `jobhunter.toml`, `.env`, source code, evidence metadata,
or documentation.

Restrict the key in Google Cloud to the Cloud Translation API and apply appropriate
project quota/billing controls.

## 7. Native-English behavior

A source version containing no Persian text does not need an external translation
request.

JobHunter records an identity artifact with:

```text
provider_name = source-identity
provider_model = native-english
translated_segment_count = 0
```

This gives native-English and translated jobs the same downstream corpus shape while
retaining their origin.

## 8. Idempotency and translator upgrades

Artifact identity includes:

```text
source detail version
+ target language
+ provider
+ provider model
+ translation schema version
```

Running the same translation again records `reused` and references the existing
artifact.

A materially changed job creates a new source version and therefore requires a new
English artifact.

Changing the provider model or translation schema also creates a new artifact. This
prevents these different events from being conflated:

```text
employer changed the advertisement
translator/model changed its rendering
projection schema changed
```

## 9. English projection contents

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
- skill tags;
- gender;
- military-service requirement;
- education;
- publication/expiration dates;
- complete job description;
- company description.

Missing values remain missing. Translation must not invent a source field.

## 10. Complete English document

Alongside structured fields, every artifact includes one canonical English document.
It is rendered from the projected fields and is convenient for:

- local LLM prompts;
- embeddings;
- text classification;
- clustering;
- topic modelling;
- information retrieval;
- reproducible NLP/ML experiments.

The structured English fields remain the preferred source for deterministic queries.

## 11. CLI

Inspect current corpus state without network access:

```bash
jobhunter translations status
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

Only artifacts belonging to each job's **latest semantic source version** are
exported. A translation of an older source version is not silently presented as
current data.

## 12. JSONL corpus schema

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

The source database remains the authoritative location for original Persian, English,
or mixed employer text.

## 13. Automatic translation after sync

Enable deliberately:

```toml
translation_enabled = true
translation_auto_after_sync = true
translation_batch_limit = 20
translation_provider = "google-cloud"
google_translation_model = "nmt"
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

Detail jobs checked during that sync are prioritized in the translation queue. The
translation batch remains bounded and failures are reported independently.

## 14. Evidence rule for later LLM analysis

A translated English passage is a convenience representation, not employer evidence.

Later analytical records may reference an English passage for readability, but every
material claim must still retain a path to the original source text or source evidence.

Example:

```text
Original employer text:
آشنایی با Docker

Possible translation:
Familiarity with Docker
```

If a translator accidentally renders that as `Proficiency with Docker`, JobHunter
must not upgrade the employer requirement because of the translation wording.

## 15. Search vocabulary is data, not Python logic

The bilingual search vocabulary is now packaged separately in:

```text
src/jobhunter/data/search_catalog.toml
```

Python code loads and validates the catalog. Terms are no longer embedded as tuples in
`search_registry.py`.

A complete replacement catalog can be configured:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

This makes career vocabulary independently editable, versionable, testable, and
replaceable without source-code changes.

## 16. Current limitations

- Google Cloud is the only remote translation provider currently implemented.
- English is the only derived target language currently supported.
- Translation quality is not yet scored against a manually reviewed Persian→English
  golden corpus.
- Glossary support and terminology locking are not implemented yet.
- The English corpus is not yet consumed by P1.6 LLM analysis because that increment
  has not started.
- Machine learning may use this corpus later, but translated text must remain labelled
  so experiments can control translation-induced bias.

These are deliberate boundaries, not reasons to mix translation into source parsing.
