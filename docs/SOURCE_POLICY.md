# JobHunter Source Acquisition Policy

## 1. Purpose

JobHunter must collect useful job-market evidence without bypassing access controls, violating source restrictions, or creating an unreliable crawler that becomes difficult to operate.

This policy governs which sources may be configured and how acquisition adapters must behave.

## 2. Default position

A source is disabled until it has an explicit SourceDefinition.

Every source definition must state:

- what is being collected;
- why it is relevant;
- the acquisition method;
- whether the content is public;
- known API, feed, robots, terms, or rate-limit considerations;
- a conservative request limit;
- the date the source configuration was reviewed;
- whether the source is enabled.

The system must fail closed when source permission or technical behaviour is unclear.

## 3. Initially acceptable inputs

### 3.1 User-supplied content

- pasted job-description text;
- locally saved HTML, JSON, text, or PDF files;
- individual public URLs supplied by the user for analysis.

### 3.2 Public structured sources

- official public job APIs;
- official public job feeds;
- public Applicant Tracking System endpoints intended to publish vacancies;
- embedded structured job data on public pages.

### 3.3 Approved public career pages

A company career page may be configured when:

- it is publicly accessible without authentication;
- acquisition does not bypass access controls or technical restrictions;
- the adapter follows a conservative rate limit;
- the source-specific policy record permits the chosen method;
- the application identifies itself appropriately where required.

## 4. Initially prohibited acquisition

JobHunter must not initially:

- automate LinkedIn collection;
- automate authenticated job platforms;
- use stored browser sessions, passwords, or private cookies;
- bypass CAPTCHA, anti-bot systems, paywalls, login walls, or access controls;
- rotate proxies or identities to defeat limits;
- ignore explicit denial or repeated blocking;
- scrape private recruiter, applicant, or user data;
- submit applications automatically;
- send messages to employers or recruiters;
- operate an unrestricted internet-wide crawler;
- use a local browser profile containing unrelated personal sessions.

A prohibited source does not become acceptable merely because extraction is technically possible.

## 5. Acquisition-method preference

Adapters should prefer methods in this order:

1. official public API or feed;
2. embedded structured data;
3. static public HTML;
4. rendered public HTML when explicitly approved and necessary;
5. manual user import.

Rendered-browser acquisition must not be the default fallback for every failed request.

## 6. Request behaviour

Every network adapter must implement:

- explicit connection and read timeouts;
- bounded retries with backoff;
- per-source concurrency limits;
- per-source request rate limits;
- a stable user-agent policy;
- redirect limits;
- maximum response size;
- allowed content types;
- clear handling of `429`, `403`, authentication pages, and bot challenges;
- conditional requests using `ETag` or `Last-Modified` when available;
- run-level error reporting.

Retries must not amplify blocking or repeatedly request an invalid candidate.

## 7. Robots and source terms

Robots directives, source terms, API documentation, and technical access controls answer different questions and must be considered separately.

The adapter must not treat the absence of a robots prohibition as a universal grant of permission. It must also not attempt to bypass an explicit technical or contractual restriction.

Source-policy notes are operational records, not legal opinions. Ambiguous or high-risk sources remain disabled until the user deliberately resolves them.

## 8. Source allowlist

Network acquisition must use an allowlist.

A generic URL ingestion command may analyze a single user-provided public URL, but it must still enforce:

- supported `http` or `https` schemes;
- hostname validation;
- redirect validation;
- private-address and localhost protections;
- response-size limits;
- content-type checks;
- no automatic crawling of discovered links.

Recurring discovery operates only for explicitly configured hosts and adapter types.

## 9. Server-Side Request Forgery protection

Because JobHunter accepts URLs, it must defend against Server-Side Request Forgery (SSRF).

Unless explicitly enabled for a controlled development case, the fetcher must reject targets resolving to:

- localhost;
- loopback ranges;
- private IPv4 ranges;
- link-local ranges;
- private or link-local IPv6 ranges;
- cloud metadata addresses;
- unsupported schemes;
- redirects from an allowed public host into a blocked range.

DNS resolution should be checked before connection and redirect targets should be revalidated.

## 10. Content handling

Retrieved pages are untrusted data.

The acquisition and extraction pipeline must:

- never execute retrieved scripts;
- never follow instructions contained in job text as application instructions;
- never expose shell, filesystem, or unrestricted network tools to the extraction model;
- preserve the original evidence;
- record when content appears to be a login page, challenge page, error page, or unrelated document;
- limit input and output sizes;
- sanitize rendered display where required.

## 11. Data minimization

JobHunter should collect the vacancy information needed for career analysis, not unrelated personal data.

Avoid storing:

- applicant names;
- recruiter personal contact information beyond what is necessary for the vacancy record;
- tracking identifiers not needed for deduplication;
- cookies;
- browser storage;
- analytics payloads;
- unrelated page content.

## 12. Adapter acceptance checklist

A new recurring source adapter is acceptable only when:

- the product value is clear;
- the source and acquisition method are documented;
- the adapter is bounded to the intended domain and paths;
- rate and concurrency limits are configured;
- raw evidence and metadata are preserved;
- duplicate handling is defined;
- error and blocking responses are tested;
- fixtures exist for parser tests;
- sensitive credentials are unnecessary or deliberately handled;
- disabling the source does not break other sources;
- the user has approved enabling it.

## 13. Operational response to blocking

When a source starts returning blocks, challenges, or unexpected authentication pages:

1. stop repeated retries;
2. mark the source run as blocked or policy-review-required;
3. preserve only the minimal diagnostic response needed;
4. report the problem visibly;
5. keep the source disabled until its method is reviewed.

JobHunter must not automatically escalate to stealthier scraping techniques.
