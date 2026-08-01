# JobHunter Search Configuration

## 1. Purpose

JobHunter turns a career direction into an explicit, inspectable set of Jobinja
searches. It supports Persian and English wording, keeps vocabulary editable as
data rather than Python code, and prevents a large catalog from creating
unbounded requests.

Search vocabulary is an acquisition input. It does not decide that a discovered
job is relevant, suitable, or worth applying to.

## 2. Catalog architecture

The packaged default catalog is:

```text
src/jobhunter/data/search_catalog.toml
```

It contains:

```toml
catalog_version = "..."

[profiles]
...

[packs.some-pack]
description = "..."
terms = ["English term", "واژه فارسی"]
```

`search_registry.py` contains loading, validation, normalization, expansion, and
URL-generation logic. It does **not** contain the career word lists.

Inspect the effective catalog:

```bash
jobhunter jobinja catalog
jobhunter jobinja catalog --show-terms
```

## 3. Complete catalog replacement

A user may replace the packaged vocabulary without editing Python:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
```

The replacement is complete rather than implicitly merged. This makes the exact
active vocabulary obvious and reproducible.

Example:

```toml
catalog_version = "personal-v1"

[profiles]
personal = ["hybrid"]

[packs.hybrid]
description = "My target hybrid roles"
terms = [
  "AI Security Engineer",
  "مهندس امنیت هوش مصنوعی",
  "Python Security Automation",
]
```

Then configure:

```toml
jobinja_search_catalog_path = "my-search-catalog.toml"
jobinja_search_profiles = ["personal"]
```

Catalog loading fails before network acquisition if a profile references an
unknown pack or the TOML structure is invalid.

## 4. Search-definition layers

The effective plan may combine:

1. catalog profiles;
2. catalog packs;
3. custom keyword groups in `jobhunter.toml`;
4. raw Jobinja result URLs;
5. one-run CLI selectors.

### 4.1 Profiles

Default broad profile:

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

### 4.2 Packs

```toml
jobinja_search_packs = ["ai-security", "defensive-security"]
```

### 4.3 Small custom groups

Custom groups are useful when only a few personal/regional terms need to be added
without maintaining a full replacement catalog:

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

### 4.4 Raw Jobinja URLs

Raw result URLs remain supported for Jobinja-owned filters that a keyword alone
cannot represent, such as location or arrangement filters.

## 5. Command-line selectors

Any selector makes that run explicit rather than silently mixing configured
searches:

```text
--url <jobinja-result-url>
--profile <profile-name>
--pack <pack-name>
--term <persian-or-english-term>
```

Example:

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --term "مهندس امنیت هوش مصنوعی" \
  --term "AI Security Automation"
```

## 6. Normalization and deduplication

The displayed term is preserved, while comparison identity:

1. applies Unicode NFKC;
2. maps Arabic `ي` to Persian `ی`;
3. maps Arabic `ك` to Persian `ک`;
4. treats zero-width non-joiner as a comparison space;
5. removes display-only directional marks;
6. collapses whitespace;
7. compares case-insensitively.

Thus these may deduplicate for search identity:

```text
امنیت‌سایبری
امنيت سایبری
```

This is not translation and not career-taxonomy canonicalization.

## 7. Exclusions

```toml
jobinja_excluded_terms = [
  "Data Scientist",
  "دانشمند داده",
]
```

Exclusions apply after normalized comparison and before Jobinja URL generation.

## 8. Search ordering and bounded coverage

Selected catalog packs are interleaved round-robin. For the broad profile the
first cycle is:

```text
ai-ml
→ llm-applications
→ python-data
→ defensive-security
→ ai-security
→ network-platform
```

This prevents the first bounded search window from being dominated by one pack.

Default operational bounds in the generated/example configuration:

```toml
jobinja_search_request_budget = 40
jobinja_max_expanded_searches = 40
jobinja_default_keyword_max_pages = 1
```

The request budget is enforced inside discovery, not only in CLI planning.

## 9. Windows

```bash
jobhunter jobinja plan \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0
```

Later windows can rotate with offsets such as `40`, `80`, and `120`. Offset is
cyclic.

The exact number of useful windows depends on the current catalog version; use
`catalog --show-terms` and `plan` rather than assuming a permanent term count.

## 10. Planning output

```bash
jobhunter jobinja plan
jobhunter jobinja plan --show-urls
```

The plan reports selected search count, planned page requests, global request
budget, maximum requests for the run, ordered search names, page limits, and
optionally generated URLs.

No Jobinja request is sent by `plan`.

## 11. Discovery and sync

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --request-budget 40
```

```bash
jobhunter jobinja sync \
  --profile ai-security-python \
  --search-limit 40 \
  --request-budget 40 \
  --missing-limit 10 \
  --refresh-limit 5 \
  --refresh-after-hours 24
```

`sync` performs source acquisition and parser audit. It invokes translation only
when both:

```toml
translation_enabled = true
translation_auto_after_sync = true
```

are deliberately configured.

## 12. Search vocabulary versus English translation

These are separate systems:

```text
search catalog
  controls which Jobinja keyword queries are made

translation provider
  creates a derived English view of already-acquired job content
```

Google translation does not dynamically invent search terms and JobHunter does
not translate every possible English word into Persian at runtime to build search
queries. Search terms remain an explicit, reviewable acquisition configuration.

This separation keeps acquisition reproducible and prevents translator output
from silently changing the scope of crawling.

## 13. Maintenance rules

When editing the packaged or replacement catalog:

- edit TOML data, not Python word tuples;
- increment `catalog_version` when vocabulary changes materially;
- put terms in the narrowest useful pack;
- include Persian/English forms when real postings use both;
- avoid speculative abbreviations and overly broad terms;
- preserve published pack identifiers where practical;
- run catalog/normalization tests;
- inspect early bounded windows after changes;
- evaluate usefulness, overlap, noise, and missed role families rather than term
  count alone.
