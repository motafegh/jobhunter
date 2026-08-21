# Translation and English Corpus

**Status:** Current translation/English-projection architecture guide  
**Date:** 2026-08-21

## 1. Purpose

JobHunter preserves employer text in its original language and may create a separate English representation for downstream local semantic analysis, analytics, review, and later market intelligence.

Translation is **derived data**. It never replaces source evidence and never creates a new employer-content semantic version by itself.

LM Studio is the normal local-first translation provider. Google Cloud Translation remains an optional external provider.

## 2. Authority hierarchy

```text
original employer/source text     ultimate authoritative source
parsed source fields              deterministic source-derived structure
English projection                derived comprehension representation
English P1.6                      strict factual interpretation of English projection
Original P1.6                     strict factual interpretation of original source
Capability Intelligence v9        bounded reasoning above accepted English P1.6
```

The original employer source remains ultimate product authority. English analysis does **not** receive hidden original-language evidence as a repair channel; source-vs-translation review occurs outside the English P1.6 model call.

## 3. Current data flow

```text
immutable Jobinja evidence
→ deterministic jobinja-detail-v2 source fields
→ current semantic source version
→ translation decision
   ├─ native English → identity projection, no translation-model call
   └─ Persian/mixed → configured translation provider
                      ↓
           lm-studio-translation-v2
                      ↓
        deterministic integrity validation
                      ↓
             english-projection-v2
                      ↓
              English P1.6 v20/v5
```

A translation/model failure never modifies source evidence or source semantic history.

A materially incorrect translation found during manual review blocks that English downstream chain; P1.6 is not allowed to compensate by silently mixing original-language evidence into the English artifact.

## 4. Why translation v2 exists

Translation v1 proved the architecture but later real postings exposed a field-association defect: plausible English strings could be returned under the wrong source fields.

The source remained correct because translation was already isolated as derived data. V1 therefore remains historical rather than being rewritten.

Current contracts:

```text
provider contract:   lm-studio-translation-v2
projection schema:   english-projection-v2
export schema:       jobhunter-english-corpus-v2
```

V1 artifacts remain preserved in SQLite but are not current v2 input to public English P1.6.

## 5. Translation v2 association guarantee

Each Persian/mixed semantic string receives a content-derived identifier based on its source text, and the structured response must return that exact identifier.

V2 sends **one semantic source segment per LM request**:

```text
source segment A → one structured request → translation A
source segment B → one structured request → translation B
source segment C → one structured request → translation C
```

This trades throughput for association safety: independent source fields are never simultaneously available for the model to swap.

The response must also satisfy JSON-schema validation, exact content-derived ID matching, non-empty translation and provider error handling.

## 6. Deterministic integrity gate

Before a v2 projection persists, JobHunter checks source/English structure and corruption classes including:

- identical projected root fields;
- dictionary/list shape preservation;
- list-length preservation;
- stable fields such as dates unchanged;
- non-empty translations for non-empty source text;
- suspicious scalar-field paragraph expansion;
- suspicious long-form omission/extreme expansion;
- translated scalar fields not left as Persian/Arabic-script text;
- explicit translated/native segment provenance.

These checks detect deterministic corruption classes. They do **not** certify full linguistic or semantic perfection.

If integrity fails:

```text
model response
→ rejected
→ failed translation attempt retained
→ no current English artifact
→ no export/current English P1.6
```

## 7. Translation records

### Source semantic version

Represents meaningful employer advertisement content. Translation never changes it.

### Translation artifact

Represents one English projection of one exact source semantic version under one provider/model/schema contract.

Important fields include:

- source detail-version ID;
- source semantic SHA-256;
- source language;
- target language;
- provider/model/schema identity;
- structured English fields and complete English document;
- per-segment provenance;
- translated/native counts;
- projection SHA-256;
- creation time.

### Translation attempt

Operational outcomes remain inspectable:

```text
completed
failed
reused
```

## 8. Segment provenance

Each projected source string is classified as:

```text
native
translated
```

Mixed Persian/English strings are translated as one semantic unit. Native technical tokens without Persian text pass through unchanged.

## 9. LM Studio model selection

Selection remains fail-closed:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic selection only when exactly one LM Studio model is visible
```

Inspect visible model IDs with:

```bash
jobhunter translations models
```

Translation, analysis and Capability models may be configured independently.

## 10. LM Studio bounds and recovery

Typical configuration includes bounded job selection, transport retry and output-token budgets.

V2 may issue several local model requests per job because every semantic segment is isolated.

The original source segment is never shortened.

If one segment ends with `finish_reason = "length"`, JobHunter may increase the output-token budget boundedly up to the configured hard cap. If the isolated segment still truncates, translation fails visibly.

## 11. Local privacy boundary

With:

```toml
translation_provider = "lm-studio"
```

parsed job text is sent only to the configured LM Studio URL. Normal use should keep it on loopback, for example:

```text
http://127.0.0.1:1234/v1
```

No cloud translation credential is required for the normal path.

## 12. Optional Google provider

Google Cloud Translation remains an explicit alternative under source/privacy policy. Credentials stay outside the repository. The same projection schema and deterministic post-provider integrity boundary apply.

## 13. Native-English behavior

A current source version containing no Persian text creates an identity artifact without a translation-model call:

```text
provider_name = source-identity
provider_model = native-english
translated_segment_count = 0
```

Native English jobs still use `english-projection-v2` so downstream records share one structure.

## 14. Idempotency and upgrades

Artifact identity includes the exact source version plus target language/provider/model/projection contract.

Repeating unchanged current work records `reused` instead of multiplying artifacts.

A new source semantic version or changed translation contract/model requires a distinct artifact rather than history rewrite.

## 15. V1 → V2 migration behavior

Historical v1 artifacts remain stored. Current-state selection requires v2, so an older database may temporarily show repair-needed English coverage until eligible jobs are rebuilt in bounded batches.

Do not delete historical rows to make current metrics look complete.

## 16. Current-version safety

Only the current successfully parsed source semantic version can support current English data.

If a newer source version exists, older translations remain historical. If the newest source is partial/parse-failed, JobHunter does not silently fall back to an older translation for current analysis/export.

## 17. English projection contents

Available source fields are carried structurally, including title, company, category, location, employment type, minimum experience, salary, skill tags, gender, military-service field, education, source dates, job description and company description.

Parser metadata such as `parser_version` and source `language` remain metadata rather than employer facts.

## 18. Export and repository projection

The dedicated English exporter writes only current English-projection-v2 artifacts for its export contract.

The repository-safe public corpus separately projects current public stage state into:

```text
corpus/jobs/<job-id>/english-projection.json
```

The public corpus deliberately excludes raw model protocol, local evidence paths, secrets and future personal/private state. SQLite remains runtime/history authority.

## 19. P1.6 boundary — English and Original stay separate

Current English P1.6:

```text
current source version
→ current English projection v2
→ English analysis fields/evidence only
→ job-analysis-english-v20 / job-analysis-v5
```

Current Original P1.6:

```text
current source version
→ original employer/source fields only
→ job-analysis-original-v9 / job-analysis-v4
```

The two modes do not provide hidden cross-language evidence to each other and do not satisfy/reuse each other's artifacts.

This architecture is intentional. Earlier bilingual mixed-evidence designs caused models to reason in one language while citing another. Until deterministic bilingual span alignment exists, cross-language repair inside one structured artifact is prohibited.

The source remains ultimate authority through human/review comparison. If an English projection materially changes source meaning, the English downstream chain is blocked/rejected rather than silently repaired inside P1.6.

A current heterogeneous example is `tI1n`, whose English projection materially mistranslated a portfolio/work-sample application condition. It was correctly withheld from P1.6 and remains translation-quality evidence.

## 20. Quality work that remains

Translation v2 removes the known field-association corruption class and adds deterministic structural/integrity checks. It does not establish perfect linguistic quality.

A later reviewed Persian→English golden corpus should compare candidate local models on:

- semantic fidelity;
- negation/modality;
- requirement-strength preservation;
- technical terminology;
- names/transliteration;
- long-description completeness.

Until such a benchmark exists, v2 should be described as **hardened and structurally guarded**, not human-certified translation quality.
