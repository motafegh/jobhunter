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
bilingual search configuration
→ inspectable search plan
→ repeat-safe Jobinja discovery
→ immutable search-page evidence
→ missing and refresh-due detail selection
→ immutable detail evidence
→ deterministic Jobinja parsing
→ semantic versioning
→ fetch-observation history
→ structural parser audit
```

Acquisition is independent from LM Studio. Successfully acquired postings remain
valid when the local model is unavailable.

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
`ai-security-python` profile with bounded request and detail budgets.

Inspect it before network use:

```bash
jobhunter jobinja catalog
jobhunter jobinja plan
```

Run the normal acquisition-only workflow:

```bash
jobhunter jobinja sync
```

The sync performs discovery, bounded missing and refresh-due detail checks, and
a deterministic parser audit. It does not invoke LM Studio.

## Bilingual search registry

JobHunter supports:

- built-in profiles;
- built-in domain packs;
- custom Persian and English keyword groups;
- one-off command-line terms;
- raw Jobinja result URLs for Jobinja-owned filters;
- normalized exclusions;
- search limits, cyclic offsets, page limits, and a global request budget.

Current broad profile:

```toml
jobinja_search_profiles = ["ai-security-python"]
```

It combines:

```text
ai-ml
llm-applications
python-data
defensive-security
ai-security
network-platform
```

The catalog contains Persian and English terms such as AI, Machine Learning,
LLM, RAG, agents, Python, data engineering, SOC, SIEM, detection engineering,
security automation, AI security, Linux, networking, DevOps, and their Persian
counterparts.

Add personal terminology without changing Python code:

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

See [Search Configuration](docs/SEARCH_CONFIGURATION.md) for the exact
normalization, deduplication, exclusion, and coverage rules.

## Search planning

Plan configured searches without network access:

```bash
jobhunter jobinja plan
```

Plan an explicit profile or pack selection:

```bash
jobhunter jobinja plan --profile ai-security-python
jobhunter jobinja plan --pack ai-security --pack defensive-security
```

Inspect generated URLs:

```bash
jobhunter jobinja plan --show-urls
```

Use stable windows for a large catalog:

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0
```

Later windows can use offsets `40`, `80`, and `120`.

## Discovery

Run configured discovery:

```bash
jobhunter jobinja discover
```

Run an explicit bounded discovery window:

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Discovery is sequential and rate-limited. It reports:

- selected searches;
- requests attempted versus budget;
- pages fetched;
- unique, new, and known jobs;
- cross-search overlap;
- failures;
- one stop reason per search.

Stop reasons:

```text
page_limit_reached
empty_page
repeated_result_set
request_budget_reached
page_failed
invalid_search
```

Repeated pages are identified by stable Jobinja job IDs rather than volatile
HTML.

## Acquisition sync

The normal bounded acquisition command is:

```bash
jobhunter jobinja sync
```

Override its controls when needed:

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

The combined missing and refresh limits may not exceed 50.

## Targeted detail acquisition

Fetch explicit discovered jobs:

```bash
jobhunter jobinja fetch tpLF tmW1 tmkE
```

Fetch jobs with no local detail version:

```bash
jobhunter jobinja fetch --missing --limit 10
```

Refresh jobs whose latest recorded check is old enough:

```bash
jobhunter jobinja fetch \
  --refresh-due \
  --older-than-hours 24 \
  --limit 5
```

Every successful fetch reports its semantic version and fetch-observation ID.
One job failure does not discard successful jobs in the same batch.

## Local inspection

List jobs:

```bash
jobhunter jobs list --limit 100
jobhunter jobs list --details available
jobhunter jobs list --details missing
```

Show one complete local posting without network access:

```bash
jobhunter jobs show tpLF
```

Show successful, unchanged, and failed check history:

```bash
jobhunter jobs checks tpLF
jobhunter jobs checks tpLF --limit 50
```

Audit latest deterministic parsing:

```bash
jobhunter jobs audit
jobhunter jobs audit --only-issues
```

A clean structural audit means no known shape or contamination problem was
detected. It does not replace later semantic interpretation.

## Data integrity model

JobHunter keeps these concepts separate:

```text
JobPosting
  one logical Jobinja job identity

SearchPageSnapshot
  one exact search-page response

JobPostingVersion
  one meaningful deterministic content version

JobDetailFetchObservation
  one successful or failed detail-page check

Raw evidence
  exact HTTP bytes plus metadata sidecar
```

Volatile HTML changes do not create false semantic versions. Repeated unchanged
checks still create inspectable observations and raw snapshots.

## Evidence storage

Runtime data is excluded from Git.

```text
data/evidence/jobinja/search-pages/
data/evidence/jobinja/job-pages/
data/jobhunter.sqlite3
```

Raw HTML is written before parsing. Evidence sidecars retain source identity,
URLs, timestamp, status, selected headers, SHA-256, byte count, and content
path.

## LM Studio foundation

The repository provides an isolated LM Studio provider boundary:

```bash
jobhunter doctor
jobhunter doctor --smoke
```

Current acquisition and parser commands do not invoke it. Evidence-backed job
interpretation remains the next major analysis stage.

## Development checks

```bash
ruff check .
pytest
```

Normal tests do not contact Jobinja or require LM Studio.

## Configuration

Use `jobhunter.toml.example` as the reference. The real `jobhunter.toml`, local
database, evidence, logs, exports, backups, personal data, and model files remain
outside version control.

Environment variables use the `JOBHUNTER_` prefix. JobHunter does not
automatically load `.env`.

## Documentation

- [Product Specification](docs/PRODUCT_SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Search Configuration](docs/SEARCH_CONFIGURATION.md)
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

The current implementation adds configurable bilingual profiles, packs, custom
keyword groups, exclusions, global request budgets, deterministic search
windows, and an acquisition-only `sync` workflow.

Challenge/login/expired-page classification, refined retry policy, complete
lifecycle classification, local LLM interpretation, combined reports, personal
relevance, and career recommendations remain incomplete and must not be claimed
as finished.
