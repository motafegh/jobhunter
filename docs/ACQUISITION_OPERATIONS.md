# JobHunter Acquisition Operations

## 1. Purpose

This runbook defines the safe operating workflow for JobHunter acquisition.
It covers search planning, repeat-safe discovery, detail acquisition, refresh
checks, fetch history, structural parser auditing, and recovery from expected
failures.

This workflow is independent from LM Studio. Model availability must never
block preservation of source evidence.

## 2. Record boundaries

JobHunter deliberately separates four records that answer different questions.

### 2.1 JobPosting

Represents one logical Jobinja advertisement identity.

Identity is based primarily on Jobinja's stable source job code. Cross-search
appearances do not create duplicate postings.

### 2.2 SearchPageSnapshot

Represents one exact search-page HTTP response and metadata sidecar.

It proves what JobHunter received while discovering candidates.

### 2.3 JobPostingVersion

Represents one semantic version of a job advertisement.

A new version is created only when deterministic extracted source fields change.
Volatile HTML differences do not create false versions.

### 2.4 JobDetailFetchObservation

Represents one attempt to check a job-detail page.

Possible outcomes:

```text
new_version
unchanged
failed
```

A repeated unchanged check creates a new observation and raw snapshot but keeps
the same semantic version. A failed observation preserves the error without
deleting earlier successful data.

## 3. Preflight

Activate the environment and validate the repository:

```bash
source .venv/bin/activate
ruff check .
pytest
```

Inspect the local configuration:

```bash
jobhunter jobinja catalog
jobhunter jobinja plan
```

The plan command performs no network requests.

## 4. Discovery-only operation

Use discovery when validating search coverage or when detail acquisition should
remain separate.

```bash
jobhunter jobinja discover
```

A broad explicit run:

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Discovery output reports:

- searches attempted;
- page requests attempted versus budget;
- pages fetched;
- combined unique jobs;
- new and known jobs;
- cross-search overlaps;
- failures;
- per-search page count, unique jobs, overlap, and stop reason.

Valid stop reasons:

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
page_failed
invalid_search
```

`request_budget_reached`, `empty_page`, and `repeated_result_set` are controlled
termination states, not acquisition failures.

## 5. Acquisition sync

The normal acquisition-only command is:

```bash
jobhunter jobinja sync
```

It composes accepted components in this order:

```text
configured search plan
→ bounded discovery
→ missing-detail selection
→ refresh-due selection
→ bounded sequential detail checks
→ immutable raw evidence
→ deterministic parsing
→ semantic versioning
→ fetch observations
→ structural parser audit
```

Configuration defaults:

```toml
jobinja_sync_missing_limit = 10
jobinja_sync_refresh_limit = 5
jobinja_refresh_after_hours = 24.0
```

The combined missing and refresh limits may not exceed 50 in one sync.

A controlled broad-profile run:

```bash
jobhunter jobinja sync \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40 \
  --missing-limit 10 \
  --refresh-limit 5 \
  --refresh-after-hours 24
```

The command returns a non-zero status when discovery or detail failures occur,
or when the parser audit reports structural findings. Successful earlier stages
remain committed and inspectable.

## 6. Targeted detail acquisition

Fetch explicit jobs:

```bash
jobhunter jobinja fetch tpLF tmW1 tmkE
```

Fetch jobs with no local detail version:

```bash
jobhunter jobinja fetch --missing --limit 10
```

Refresh acquired jobs whose latest check is old enough:

```bash
jobhunter jobinja fetch \
  --refresh-due \
  --older-than-hours 24 \
  --limit 5
```

Selection modes are mutually exclusive.

Each batch:

- removes duplicate IDs while preserving order;
- performs requests sequentially;
- applies the configured delay between requests;
- limits the batch to 50 unique jobs;
- isolates expected failures per job;
- prints new-version, unchanged, and failure counts;
- prints the semantic version and fetch-observation ID for each success.

## 7. Inspection commands

List discovered jobs:

```bash
jobhunter jobs list --limit 100
```

List jobs with or without local details:

```bash
jobhunter jobs list --details available
jobhunter jobs list --details missing
```

Show one complete local job without network access:

```bash
jobhunter jobs show tpLF
```

Show operational fetch history:

```bash
jobhunter jobs checks tpLF
jobhunter jobs checks tpLF --limit 50
```

Audit latest parsed details:

```bash
jobhunter jobs audit
jobhunter jobs audit --only-issues
```

## 8. Parser-audit interpretation

The deterministic audit checks structural invariants, including:

- title and description presence;
- current parser version;
- parse status;
- description length;
- scalar-field shape;
- source skill-tag shape;
- obvious navigation or interface contamination;
- Python mapping representations accidentally stored as text;
- implausibly long scalar fields.

Missing optional fields are coverage gaps, not automatic parser failures.

A clean audit means no known structural anomaly was detected. It does not prove
that every employer statement has been semantically interpreted correctly. That
belongs to the later evidence-backed LLM analysis stage.

## 9. Failure handling

### 9.1 Search-page failure

One search failure does not discard successful searches. Inspect the per-search
summary and evidence from completed pages.

### 9.2 Detail-page failure

Expected acquisition and evidence-write failures produce a failed fetch
observation when the job identity is known. Earlier versions and observations
remain valid.

Retry by explicit ID after resolving the underlying issue:

```bash
jobhunter jobinja fetch <job-id>
```

### 9.3 Parser finding

Use:

```bash
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

Then inspect the version-defining raw HTML path. Do not patch the parser from a
single unexplained output without preserving a regression fixture or test.

### 9.4 LM Studio unavailable

Acquisition commands do not invoke LM Studio. No acquisition recovery is needed.
The job remains available for later analysis.

## 10. Daily and weekly operating patterns

### Daily focused sync

```bash
jobhunter jobinja sync \
  --pack ai-ml \
  --pack ai-security \
  --pack defensive-security \
  --request-budget 30 \
  --missing-limit 10 \
  --refresh-limit 5
```

### Broad catalog rotation

```text
Day or run 1: --search-offset 0
Day or run 2: --search-offset 40
Day or run 3: --search-offset 80
Day or run 4: --search-offset 120
```

Always inspect the plan when changing offsets, limits, packs, or profiles.

### Weekly quality check

```bash
ruff check .
pytest
jobhunter jobs audit
jobhunter jobs list --details missing --limit 100
```

## 11. Safety and source discipline

- Use public Jobinja pages only.
- Keep requests sequential and rate-limited.
- Preserve a descriptive user agent.
- Keep global search and detail limits bounded.
- Do not automate login or applications.
- Do not bypass CAPTCHA, blocking, authentication, or access controls.
- Do not use proxy rotation or stealth crawling.
- Treat acquired text as untrusted data.
- Keep runtime evidence and the local database outside Git.

## 12. Current stop line

The acquisition system may discover, preserve, parse, version, refresh, audit,
and report operational failures.

It must not yet claim:

- responsibility classification;
- required-versus-preferred qualification interpretation;
- personal relevance;
- skill gaps;
- readiness;
- career recommendations;
- combined market conclusions.

Those require versioned, evidence-backed local analysis and review states.
