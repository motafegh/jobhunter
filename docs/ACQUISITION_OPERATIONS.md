# JobHunter Acquisition and Translation Operations

## 1. Purpose

This runbook defines safe operation for JobHunter source acquisition and the
optional derived English corpus. It covers search planning, discovery, detail
checks, refresh scheduling, parser audit, translation, export, and expected
failure recovery.

Source acquisition is independent from LM Studio and from Google translation.
External translation is opt-in.

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

Inspect configuration without external network calls:

```bash
jobhunter jobinja catalog --show-terms
jobhunter jobinja plan
jobhunter translations status
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

Each successful check reports its semantic source version and fetch-observation
ID.

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

## 8. Translation privacy preflight

Translation is disabled by default because Google Cloud is external.

Before enabling it:

1. enable the Cloud Translation API in the intended Google Cloud project;
2. create/restrict an API key for that API;
3. configure billing/quota deliberately;
4. keep the key outside Git;
5. understand that parsed job-advertisement text will be sent to Google.

Recommended environment setup:

```bash
export JOBHUNTER_GOOGLE_TRANSLATION_API_KEY='...'
```

Local configuration:

```toml
translation_enabled = true
translation_auto_after_sync = false
translation_provider = "google-cloud"
translation_target_language = "en"
translation_batch_limit = 20
translation_timeout_seconds = 30.0
translation_max_retries = 1
google_translation_model = "nmt"
```

Keep `translation_auto_after_sync = false` during first live validation.

## 9. First live translation acceptance

Choose one already-parsed Persian/mixed advertisement, for example a known clean
fixture such as `tpLF`.

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
- job description;
- technical names such as Python, RAG, LLM, Docker, MLOps;
- strength words such as familiarity, knowledge, proficiency, mastery, required,
  and preferred when present.

Transport success alone is not translation-quality acceptance.

## 10. Translation idempotency acceptance

Immediately run the same translation again:

```bash
jobhunter translations run tpLF
```

Expected outcome:

```text
reused
```

The same source version/provider/model/schema must reference the same artifact
rather than calling Google again.

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

No Google translation request is required.

## 12. Bounded missing translation queue

After individual validation:

```bash
jobhunter translations run --missing --limit 5
```

One job's translation failure does not discard successful artifacts from the
same batch.

## 13. English corpus export

```bash
jobhunter translations export
```

Default:

```text
data/exports/job_english_corpus.jsonl
```

Inspect a few JSONL records before using them in ML/LLM experiments.

Only artifacts tied to each job's latest semantic source version are exported.
An older translated artifact is preserved historically but not exposed as current
corpus data after the employer posting changes.

## 14. Automatic translation after sync

Enable only after manual live acceptance:

```toml
translation_enabled = true
translation_auto_after_sync = true
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

Source acquisition runs first. The translation queue then prioritizes source jobs
checked during that sync and fills remaining capacity from current parsed versions
missing an English artifact.

Translation failure may make the command return attention-required status but does
not roll back successful acquisition, evidence, parsing, or semantic versions.

## 15. Failure handling

### Search/detail failure

Inspect source summaries and `jobs checks`. Retry explicitly only after the
underlying condition is understood.

### Parser finding

```bash
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

Preserve a regression fixture/test before generalizing a parser fix.

### Google translation failure

Source data remains valid. Fix credentials/quota/network/provider configuration,
then rerun:

```bash
jobhunter translations run <job-id>
```

A failed translation attempt is retained; a later success creates an artifact.

### Translation quality concern

Do not edit original Jobinja fields to compensate for a translation problem.
Record the example for a future reviewed translation corpus and compare provider/
model/schema alternatives.

## 16. Daily/weekly patterns

### Source-only daily sync

Keep translation disabled or `translation_auto_after_sync = false`, then run:

```bash
jobhunter jobinja sync
```

### Source + translation daily sync

After acceptance, enable automatic translation and keep both acquisition and
translation batch limits conservative.

### Weekly quality check

```bash
ruff check .
pytest
jobhunter jobs audit
jobhunter translations status
```

Periodically inspect both original and English representations rather than only
aggregate counts.

## 17. Safety rules

- Use public Jobinja pages only.
- Keep source acquisition bounded/rate-limited.
- Do not bypass access controls or CAPTCHA.
- Treat acquired text as untrusted data.
- Keep runtime data and secrets outside Git.
- Do not send personal capability/profile data to Google through the translation
  pipeline; the current translation scope is parsed job-advertisement content.
- Treat English translations as derived data, never stronger evidence than the
  original employer text.

## 18. Current stop line

The system may discover, preserve, parse, version, refresh, audit, translate, and
export current English derived documents.

It must not yet claim responsibility classification, required/preferred semantic
interpretation, personal relevance, readiness, skill gaps, recommendations, or
combined market conclusions. Those require P1.6/P1.7 evidence-backed analysis.
