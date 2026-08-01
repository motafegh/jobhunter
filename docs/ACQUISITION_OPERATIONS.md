# JobHunter Acquisition and Translation Operations

## 1. Purpose

This runbook defines safe operation for JobHunter source acquisition and the
optional derived English corpus. It covers search planning, discovery, detail
checks, refresh scheduling, parser audit, local translation, export, and expected
failure recovery.

Source acquisition is independent from translation. LM Studio is the normal
local-first translation provider; Google Cloud is an optional external provider.

## 2. Record boundaries

JobHunter separates records by responsibility:

```text
JobPosting
  logical Jobinja identity

SearchPageSnapshot
  exact search-page response

JobPostingVersion
  one semantic source-content version

JobDetailFetchObservation
  one operational detail-page check

JobTranslationArtifact
  one English projection of one exact source semantic version

JobTranslationAttempt
  one completed / failed / reused translation operation
```

Raw Jobinja evidence remains authoritative.

## 3. Preflight

```bash
source .venv/bin/activate
ruff check .
pytest
```

Inspect configuration without invoking Jobinja or translation generation:

```bash
jobhunter jobinja catalog --show-terms
jobhunter jobinja plan
jobhunter translations status
```

When LM Studio translation will be used, also inspect the local server:

```bash
jobhunter translations models
```

## 4. Discovery-only operation

```bash
jobhunter jobinja discover
```

Broad explicit example:

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Controlled stop states:

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
```

Failure stop states:

```text
page_failed
invalid_search
```

## 5. Acquisition sync

```bash
jobhunter jobinja sync
```

Source flow:

```text
configured search plan
→ bounded discovery
→ missing-detail selection
→ refresh-due selection
→ sequential detail checks
→ immutable evidence
→ deterministic parsing
→ semantic versioning
→ fetch observations
→ structural parser audit
```

Defaults:

```toml
jobinja_sync_missing_limit = 10
jobinja_sync_refresh_limit = 5
jobinja_refresh_after_hours = 24.0
```

Combined missing + refresh detail checks may not exceed 50.

## 6. Targeted detail acquisition

```bash
jobhunter jobinja fetch tpLF tmW1 tmkE
jobhunter jobinja fetch --missing --limit 10
jobhunter jobinja fetch --refresh-due --older-than-hours 24 --limit 5
```

Each successful check reports its semantic source version and fetch-observation ID.

## 7. Parser inspection

```bash
jobhunter jobs list --limit 100
jobhunter jobs show tpLF
jobhunter jobs checks tpLF
jobhunter jobs audit
jobhunter jobs audit --only-issues
```

A clean structural audit does not mean semantic interpretation or translation has
been reviewed.

## 8. Local LM Studio translation preflight

Translation is disabled by default so first use is deliberate, but the normal
provider requires no cloud credentials.

Recommended local configuration:

```toml
translation_enabled = true
translation_auto_after_sync = false
translation_provider = "lm-studio"
translation_target_language = "en"
translation_batch_limit = 20
translation_timeout_seconds = 30.0
translation_max_retries = 1
translation_lm_studio_max_tokens = 4096
translation_lm_studio_character_target = 6000
```

Model-selection priority:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic only when exactly one model is visible
```

List exact model IDs:

```bash
jobhunter translations models
```

When multiple models are visible, configure one explicitly:

```toml
translation_lm_studio_model = "exact-model-id"
```

Keep `translation_auto_after_sync = false` during first live quality validation.

## 9. First live LM Studio translation acceptance

Choose one already-parsed Persian/mixed advertisement, such as `tpLF`.

Check status:

```bash
jobhunter translations status
```

Translate one job:

```bash
jobhunter translations run tpLF
```

Inspect the result:

```bash
jobhunter translations show tpLF
```

Manually compare at least:

- title;
- location;
- employment type;
- education/experience wording;
- skill tags;
- complete job description;
- technical names such as Python, RAG, LLM, Docker, MLOps;
- negation and uncertainty;
- strength words such as familiarity, knowledge, proficiency, mastery, required,
  and preferred when present.

Structured-output success alone is not translation-quality acceptance.

## 10. Translation idempotency acceptance

Immediately run the same translation again:

```bash
jobhunter translations run tpLF
```

Expected outcome:

```text
reused
```

The same source version/provider-contract/model/schema must reference the same artifact
rather than invoking the model again.

## 11. Native-English acceptance

For a parsed advertisement containing no Persian text:

```bash
jobhunter translations run <english-job-id>
jobhunter translations show <english-job-id>
```

Expected provider identity:

```text
source-identity / native-english
```

No LM Studio or cloud translation request is required.

## 12. Bounded missing translation queue

After individual validation:

```bash
jobhunter translations run --missing --limit 5
```

One job's translation failure does not discard successful artifacts from the same
batch.

## 13. English corpus export

```bash
jobhunter translations export
```

Default:

```text
data/exports/job_english_corpus.jsonl
```

Inspect several JSONL records before using them in ML/LLM experiments.

Only artifacts tied to each job's latest successfully parsed semantic source version
are exported. Historical translations are retained but not exposed as current data.

## 14. Automatic translation after sync

Enable only after manual quality acceptance:

```toml
translation_enabled = true
translation_auto_after_sync = true
translation_provider = "lm-studio"
translation_batch_limit = 20
```

Then:

```bash
jobhunter jobinja sync \
  --profile ai-security-python \
  --search-limit 12 \
  --request-budget 12 \
  --missing-limit 4 \
  --refresh-limit 2
```

Source acquisition runs first. The translation queue then prioritizes jobs checked
during that sync and fills remaining capacity from current parsed versions missing an
English artifact.

Translation failure may make the command return attention-required status but does not
roll back successful acquisition, evidence, parsing, or semantic versions.

## 15. Optional Google Cloud provider

Google Cloud Translation remains available when deliberately desired:

```toml
translation_provider = "google-cloud"
google_translation_model = "nmt"
```

Provide its credential outside Git:

```bash
export JOBHUNTER_GOOGLE_TRANSLATION_API_KEY='...'
```

This path intentionally sends parsed job text to Google. It is not required for normal
JobHunter operation.

## 16. Failure handling

### Search/detail failure

Inspect source summaries and `jobs checks`. Retry explicitly only after the underlying
condition is understood.

### Parser finding

```bash
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

Preserve a regression fixture/test before generalizing a parser fix.

### LM Studio translation failure

Source data remains valid. Check:

```bash
jobhunter translations models
jobhunter translations status
```

Then verify the configured model is loaded and supports the required structured output.
A failed translation attempt remains inspectable; rerunning later can create a valid
artifact without changing source history.

### Google translation failure

When the optional Google provider is selected, fix credentials/quota/network/provider
configuration and rerun the affected job. Source data remains valid.

### Translation quality concern

Do not edit original Jobinja fields to compensate for a translation problem. Preserve
the example for the reviewed translation corpus and compare model/provider versions.

## 17. Daily/weekly patterns

### Source-only daily sync

Keep translation disabled or `translation_auto_after_sync = false`, then run:

```bash
jobhunter jobinja sync
```

### Source + local translation daily sync

After acceptance, enable automatic LM Studio translation and keep both acquisition and
translation/model request bounds conservative.

### Weekly quality check

```bash
ruff check .
pytest
jobhunter jobs audit
jobhunter translations status
```

Periodically inspect both original and English representations rather than only
aggregate counts.

## 18. Safety and privacy rules

- Use public Jobinja pages only.
- Keep source acquisition bounded/rate-limited.
- Do not bypass access controls or CAPTCHA.
- Treat acquired text as untrusted data.
- Keep runtime data and secrets outside Git.
- Prefer LM Studio on loopback for local translation.
- Treat a non-loopback LM Studio deployment as an explicit network boundary.
- When Google is selected, do not send personal capability/profile data through the
  translation pipeline; current translation scope is parsed job-advertisement content.
- Treat English translations as derived data, never stronger evidence than original
  employer text.

## 19. Current stop line

The system may discover, preserve, parse, version, refresh, audit, translate locally,
and export current English derived documents.

It must not yet claim responsibility classification, required/preferred semantic
interpretation, personal relevance, readiness, skill gaps, recommendations, or
combined market conclusions. Those require P1.6/P1.7 evidence-backed analysis.
