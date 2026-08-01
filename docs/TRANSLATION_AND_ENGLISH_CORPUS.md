# Translation and English Corpus

## 1. Purpose

JobHunter preserves employer text in its original language and may create a separate
English representation for downstream local semantic analysis, SQL/analytics, and later
machine-learning experiments.

Translation is **derived data**. It never replaces source evidence and never creates a new
employer-content semantic version by itself.

LM Studio is the normal local-first translation provider. Google Cloud Translation remains
an optional external provider.

## 2. Evidence hierarchy

```text
original employer/source text     authoritative
English projection                derived convenience
semantic analysis                 model-derived interpretation
```

A downstream claim may use English to help a model understand Persian, but material claims
must remain traceable to original employer/source text.

## 3. Current data flow

```text
immutable Jobinja HTML
→ deterministic parser-v2 source fields
→ current semantic source version
→ translation decision
   ├─ native English → identity projection, no model call
   └─ Persian/mixed → configured translation provider
                      ↓
                 translation v2
                      ↓
        deterministic integrity validation
                      ↓
          current English v2 artifact
                      ↓
      export / P1.6 semantic analysis
```

A translation/model failure never modifies source evidence or source semantic history.

## 4. Why translation v2 exists

Translation v1 proved the architecture and worked on the initial live corpus, but later
real postings exposed a serious association defect: plausible English strings could be
returned under the wrong source fields. Examples included company-description text appearing
as the company name and short categorical values shifting across location, salary, gender,
and military-service fields.

The original source remained correct because translation was already isolated as derived
data. JobHunter therefore treats v1 as historical evidence rather than rewriting it.

Current contracts are:

```text
provider contract:   lm-studio-translation-v2
projection schema:   english-projection-v2
export schema:       jobhunter-english-corpus-v2
```

V1 artifacts remain in SQLite. They are not considered current v2 data, are not exported by
the v2 exporter, and are not accepted as the English input to P1.6 analysis.

## 5. Translation v2 association guarantee

Each Persian/mixed semantic string receives a content-derived identifier based on its source
text. The LM Studio structured response must return that exact identifier.

More importantly, v2 sends **one semantic source segment per LM request**.

```text
source segment A → one structured request → translation A
source segment B → one structured request → translation B
source segment C → one structured request → translation C
```

This deliberately trades model-call throughput for field-association safety. A model cannot
swap salary/location/company/category translations between simultaneous items because those
independent items are never present in the same translation request.

The response still must satisfy strict JSON-schema validation, exact content-derived ID
matching, non-empty translation, and normal provider error handling.

## 6. Deterministic translation-integrity gate

Before a v2 projection is persisted, JobHunter checks source and English structures.
Current checks include:

- identical projected root fields;
- dictionary/list shape preservation;
- list-length preservation;
- stable fields such as dates remain unchanged;
- non-empty translations for non-empty source text;
- suspicious scalar-field paragraph expansion;
- suspicious long-form omission or extreme expansion;
- translated scalar fields do not remain Persian/Arabic-script text;
- translated segment provenance remains explicit.

These checks detect corruption classes. They do **not** claim to judge whether an English
sentence is elegant or whether every nuanced translation is linguistically optimal.

If integrity fails:

```text
model response
→ rejected
→ failed translation attempt retained
→ no current English artifact
→ no export
→ no P1.6 analysis
```

## 7. Three translation record types

### Source semantic version

Represents meaningful employer advertisement content. Translation never changes it.

### Translation artifact

Represents one English projection of one exact source semantic version under one
provider/model/schema contract.

Important fields include:

- source detail-version ID;
- source semantic SHA-256;
- source language;
- target language;
- provider name;
- exact provider model;
- translation schema version;
- structured English fields;
- complete English document;
- per-segment provenance;
- translated/native segment counts;
- projection SHA-256;
- creation time.

### Translation attempt

Records operational outcomes:

```text
completed
failed
reused
```

Provider/model errors and integrity rejection therefore remain inspectable.

## 8. Segment provenance

Each projected source string is classified as:

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

Mixed Persian/English strings are translated as one semantic unit. Native technical tokens
without Persian text pass through unchanged.

## 9. LM Studio model selection

Selection remains fail-closed:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic selection only when exactly one LM Studio model is visible
```

This permits a dedicated translation model without forcing later semantic analysis to use
the same model.

Inspect visible model IDs with:

```bash
jobhunter translations models
```

## 10. LM Studio request and recovery bounds

Typical configuration:

```toml
translation_batch_limit = 20
translation_timeout_seconds = 30.0
translation_max_retries = 1
translation_lm_studio_max_tokens = 4096
```

`translation_batch_limit` limits how many jobs one operation selects. V2 may issue several
local model requests per job because every semantic segment is isolated.

The original source segment is never shortened.

If LM Studio reports `finish_reason = "length"` for one segment, JobHunter doubles the
output-token budget boundedly:

```text
4096 → 8192 → 16384 → 32768
```

If the single segment still truncates at the hard cap, translation fails visibly.

Transport retries remain bounded separately.

## 11. Local privacy boundary

With:

```toml
translation_provider = "lm-studio"
```

parsed job text is sent only to the configured LM Studio URL. Normal use should keep that
URL on loopback, for example:

```text
http://127.0.0.1:1234/v1
```

No Google API key or cloud billing is required for the normal path.

## 12. Optional Google provider

Google Cloud Translation remains an explicit alternative:

```toml
translation_provider = "google-cloud"
google_translation_model = "nmt"
```

Google is external processing. Credentials stay outside the repository. The same projection
schema and deterministic integrity gate apply after provider output.

## 13. Native-English behavior

A current source version containing no Persian text creates an identity artifact without a
translation-model call:

```text
provider_name = source-identity
provider_model = native-english
translated_segment_count = 0
```

Native English jobs still receive the current `english-projection-v2` schema so downstream
records have one uniform structure.

## 14. Idempotency and upgrades

Artifact identity includes:

```text
source detail version
+ target language
+ provider contract
+ provider model
+ projection schema version
```

Repeating identical current work records `reused` instead of multiplying artifacts.

A new source semantic version requires a new English artifact. Changing provider/model,
provider contract, or projection schema also creates a distinct artifact rather than
rewriting history.

## 15. V1 -> V2 migration behavior

After upgrading an existing database:

```text
historical v1 artifact
→ remains stored
→ UI labels current English as repair needed
→ current missing queue selects the job for v2 work
→ successful v2 translation creates a new artifact
→ v1 remains historical
```

This is expected. It may temporarily reduce the dashboard's current-English count until the
parsed corpus is repaired in bounded batches.

Do not delete v1 rows to make the metric look complete.

## 16. Current-version safety

Only the current successfully parsed source semantic version can be current English data.
If a newer source version exists, older translations remain historical.

If the newest source version is `partial` or `parse_failed`, JobHunter does not silently
fall back to an older translation for current export/analysis.

## 17. English projection contents

Available source fields are carried structurally, including:

- title;
- company;
- job category;
- location;
- employment type;
- minimum experience;
- salary;
- required skill tags;
- gender;
- military-service field;
- education;
- date posted / valid through;
- full job description;
- full company description.

Parser metadata such as `parser_version` and source `language` stay artifact metadata rather
than pretending to be employer job fields.

## 18. Export

The current exporter writes JSON Lines to the configured data directory and includes only
current `english-projection-v2` artifacts.

A record carries source/version identity, translation provider/model/schema/projection hash,
segment provenance, structured English fields, and the complete English document.

Original source fields are not duplicated as authority into this derived export; source IDs
and hashes link back to the authoritative local database/evidence.

## 19. P1.6 boundary

P1.6 refuses to analyze a current source version unless JobHunter can resolve its current
hardened English artifact.

The model receives both:

- original authoritative source fields;
- English v2 comprehension aid.

Every accepted semantic claim must still cite an evidence excerpt present in original source
fields. This prevents a translation error from becoming the sole evidence for a material
career claim.

## 20. Quality work that remains

Translation v2 removes the known field-association corruption class and adds deterministic
integrity checks. It does not establish a perfect linguistic benchmark.

A later reviewed Persian→English golden corpus should compare candidate local models on:

- semantic fidelity;
- requirement-strength preservation;
- negation/modality;
- technical terminology;
- names/transliteration;
- long-description completeness.

Until that benchmark exists, v2 should be described as hardened and structurally guarded,
not as human-certified translation quality.
