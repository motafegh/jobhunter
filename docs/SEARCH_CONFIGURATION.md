# JobHunter Search Configuration

## 1. Purpose

JobHunter search configuration turns a career direction into an explicit,
inspectable set of Jobinja searches. It supports Persian and English wording,
keeps the vocabulary editable without code changes, and prevents a large search
catalog from creating unbounded requests.

The search registry is an acquisition input. It does not decide that a job is
relevant, suitable, or worth applying to. Those are later evidence-backed
analysis decisions.

## 2. Search-definition layers

JobHunter supports four layers. They can be used separately or combined.

### 2.1 Built-in profiles

A profile combines several built-in packs.

```toml
jobinja_search_profiles = ["ai-security-python"]
```

Current profiles:

| Profile | Packs |
|---|---|
| `ai-security-python` | `ai-ml`, `llm-applications`, `python-data`, `defensive-security`, `ai-security`, `network-platform` |
| `ai-focused` | `ai-ml`, `llm-applications`, `ai-security` |
| `security-focused` | `defensive-security`, `ai-security`, `network-platform` |

Profiles are curated starting points. They are version-controlled and reviewed
like code, but they are not immutable product truth.

### 2.2 Built-in packs

A pack groups related Persian and English search terms.

```toml
jobinja_search_packs = ["ai-security", "defensive-security"]
```

Current packs:

- `ai-ml`: AI, Machine Learning, Deep Learning, NLP, vision, data science, and MLOps;
- `llm-applications`: LLM, RAG, agents, prompt engineering, chatbots, and vector retrieval;
- `python-data`: Python application, API, data engineering, and data-platform terms;
- `defensive-security`: SOC, SIEM, detection, response, AppSec, cloud security, and automation;
- `ai-security`: AI, ML, LLM, model, agent, and prompt-security terms;
- `network-platform`: Linux, networking, DevOps, platform, cloud, and container terms.

Inspect exact pack sizes and descriptions with:

```bash
jobhunter jobinja catalog
```

### 2.3 Custom keyword groups

Custom groups are the preferred extension point for personal terminology,
regional wording, or emerging roles.

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

Each term becomes one Jobinja keyword-filter search. A group may contain up to
200 unique normalized terms.

### 2.4 Raw Jobinja search URLs

Raw result URLs remain supported for Jobinja-owned filters that a keyword alone
cannot represent, such as a location, arrangement, or category filter.

```toml
[[jobhunter.jobinja_searches]]
name = "Tehran remote AI roles"
url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=..."
enabled = true
max_pages = 2
```

Raw URLs and keyword-generated searches are deduplicated by canonical URL before
acquisition.

## 3. Command-line selectors

Command-line selectors create an explicit one-run plan. When any selector is
passed, configured searches are not silently mixed into that run.

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --term "مهندس امنیت هوش مصنوعی" \
  --term "AI Security Automation"
```

Supported selectors:

```text
--url <jobinja-result-url>
--profile <profile-name>
--pack <pack-name>
--term <persian-or-english-term>
```

Each option can be repeated.

## 4. Normalization and deduplication

JobHunter retains the original display term but creates a comparison form for
identity and exclusion checks.

The comparison form:

1. applies Unicode NFKC normalization;
2. maps Arabic `ي` to Persian `ی`;
3. maps Arabic `ك` to Persian `ک`;
4. treats the zero-width non-joiner as a space for term comparison;
5. removes directional marks used only for display;
6. collapses whitespace;
7. applies case-insensitive comparison.

This means variants such as the following become one search identity:

```text
امنیت‌سایبری
امنيت سایبری
```

The original selected spelling is still shown in the plan and persisted search
name.

## 5. Exclusions

Exclusions remove noisy or unwanted terms after normalization and before URL
generation.

```toml
jobinja_excluded_terms = [
  "Data Scientist",
  "دانشمند داده",
]
```

Exclusions apply to built-in profiles, built-in packs, custom groups, and
one-off terms.

## 6. Request and search bounds

A broad profile can expand to many searches. Two independent limits prevent
uncontrolled acquisition.

```toml
jobinja_search_request_budget = 40
jobinja_max_expanded_searches = 100
jobinja_default_keyword_max_pages = 1
```

`jobinja_max_expanded_searches` limits the selected search definitions.
`jobinja_search_request_budget` limits actual search-page requests across the
whole discovery or sync run.

When the budget is reached:

- no additional request is sent;
- already acquired evidence and discoveries remain valid;
- remaining searches receive `request_budget_reached` as their stop reason;
- budget exhaustion is not classified as an acquisition failure.

## 7. Search windows and broad-profile coverage

Use `--search-limit` and `--search-offset` to process a large catalog in
predictable windows.

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0

jobhunter jobinja plan \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 40
```

Offset is cyclic: an offset larger than the plan length wraps around. The plan
is stable for the same configuration and application version, making windows
reproducible.

A practical coverage sequence for the broad profile is:

```text
offset 0
→ offset 40
→ offset 80
→ offset 120
```

Inspect the plan before network acquisition. Do not assume a large vocabulary
should run in full every day.

## 8. Planning commands

List the built-in catalog:

```bash
jobhunter jobinja catalog
```

Inspect configured searches without network access:

```bash
jobhunter jobinja plan
```

Inspect a one-off profile or pack:

```bash
jobhunter jobinja plan --profile ai-focused
jobhunter jobinja plan --pack ai-security --pack defensive-security
```

Include generated URLs:

```bash
jobhunter jobinja plan --show-urls
```

The plan reports:

- selected search count;
- planned page-request count;
- global request budget;
- maximum requests possible in that run;
- ordered search names and page limits;
- canonical URLs when requested.

## 9. Discovery and sync usage

Run discovery only:

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Run the complete acquisition-only workflow:

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

`sync` performs:

```text
search planning
→ repeat-safe discovery
→ missing-detail selection
→ refresh-due selection
→ sequential detail acquisition
→ semantic version decision
→ fetch-observation persistence
→ deterministic parser audit
```

It does not invoke LM Studio.

## 10. Maintenance rules

When updating built-in vocabulary:

- add terms to the narrowest appropriate pack;
- include Persian and English forms when both are used in real listings;
- avoid speculative abbreviations with no demonstrated search value;
- avoid terms so broad that they dominate unrelated jobs;
- preserve pack identifiers once published;
- add normalization and expansion tests;
- inspect the generated plan before live acquisition;
- use exclusions rather than deleting useful built-in terms for one user-specific reason.

Search vocabulary quality should be evaluated by discovered-job usefulness,
cross-search overlap, noise, and missed role families—not by term count alone.
