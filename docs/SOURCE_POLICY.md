# JobHunter Source Acquisition Policy

## 1. Purpose

JobHunter must collect useful job-market evidence without bypassing access
controls, violating source restrictions, or becoming an unreliable crawler.

This policy controls which sources may be configured and how acquisition
adapters must behave.

## 2. Default position

A recurring source is disabled until it has an explicit source definition or an
approved source-specific implementation plan.

Every source definition should state:

- what is collected and why;
- whether content is public;
- the acquisition method;
- approved hosts and paths;
- known API, feed, robots, terms, and rate-limit considerations;
- conservative page, request, and batch limits;
- the review date;
- whether the source is enabled.

The system fails closed when source permission or technical behavior is unclear.

## 3. Initially acceptable inputs

### 3.1 User-supplied content

- pasted job-description text;
- locally saved HTML, JSON, text, or PDF files;
- individual public URLs explicitly supplied for analysis.

### 3.2 Public structured sources

- official public job APIs;
- official public job feeds;
- public Applicant Tracking System endpoints intended to publish vacancies;
- embedded structured job data on public pages.

### 3.3 Approved public career pages

A public career page may be configured when:

- authentication is unnecessary;
- acquisition does not bypass restrictions;
- the adapter follows conservative bounds;
- source-specific policy permits the method;
- the application identifies itself appropriately.

## 4. Prohibited acquisition

JobHunter must not:

- automate LinkedIn or another authenticated platform;
- use stored browser sessions, passwords, or private cookies;
- bypass CAPTCHA, anti-bot systems, paywalls, login walls, or access controls;
- rotate proxies or identities to defeat limits;
- ignore explicit denial or repeated blocking;
- scrape private recruiter, applicant, or user data;
- submit applications automatically;
- send messages to employers or recruiters;
- operate an unrestricted internet-wide crawler;
- use a personal browser profile containing unrelated sessions.

A source does not become acceptable merely because extraction is technically
possible.

## 5. Acquisition-method preference

Prefer methods in this order:

1. official public API or feed;
2. embedded structured data;
3. static public HTML;
4. rendered public HTML when explicitly approved and necessary;
5. manual user import.

Rendered-browser acquisition is not the default fallback for a failed request.

## 6. Required request behavior

Every active adapter must implement:

- explicit connection and read timeouts;
- source allowlisting and redirect revalidation;
- sequential operation or an explicit conservative concurrency bound;
- a stable descriptive user agent;
- request delay or equivalent rate control;
- per-search page limits;
- a global run-level request budget;
- maximum response size;
- allowed content types;
- immutable evidence before parsing;
- visible run-level error reporting;
- bounded detail or candidate batches.

A generated bilingual keyword catalog does not authorize broader crawling. Each
generated search remains one bounded request plan against the same approved
Jobinja search endpoint.

## 7. Retry and conditional-request maturity

Retries can amplify blocking or repeatedly request an invalid candidate.
Therefore:

- the currently accepted Jobinja path performs one controlled attempt per
  selected page or detail check;
- expected failures are retained as explicit run errors or fetch observations;
- the user may retry an individual item deliberately;
- automatic retry/backoff must not be enabled until `429`, `403`, login,
  challenge, CAPTCHA, timeout, and transient server responses are classified;
- automatic retries must have a small attempt cap and increasing backoff;
- a blocked or challenge response must never trigger aggressive retry;
- conditional requests using `ETag` or `Last-Modified` should be added when the
  source provides stable validators and tests prove correct behavior.

The absence of automatic retry is safer than an unclassified retry loop.

## 8. Robots and source terms

Robots directives, source terms, API documentation, and technical access
controls answer different questions and must be considered separately.

The absence of a robots prohibition is not a universal grant. JobHunter must not
bypass an explicit technical or contractual restriction.

Source-policy notes are operational records, not legal opinions. Ambiguous or
high-risk sources remain disabled until deliberately reviewed.

## 9. Source allowlist

Recurring acquisition operates only for explicitly configured adapter types,
hosts, and paths.

A future generic single-URL import must still enforce:

- `http` or `https` only;
- hostname and redirect validation;
- private-address and localhost protection;
- response-size and content-type checks;
- no automatic crawling of discovered links.

The current Jobinja adapter accepts only approved Jobinja hosts and `/jobs` or
validated advertisement paths.

## 10. Server-Side Request Forgery protection

Any adapter accepting arbitrary hosts must reject targets resolving to:

- localhost and loopback ranges;
- private IPv4 ranges;
- link-local ranges;
- private or link-local IPv6 ranges;
- cloud metadata addresses;
- unsupported schemes;
- redirects from an approved public host into a blocked range.

The current Jobinja adapter reduces this risk by using a fixed host allowlist and
validating final paths. A future generic URL adapter requires DNS and IP-range
validation before release.

## 11. Content handling

Retrieved pages are untrusted data.

The pipeline must:

- never execute retrieved scripts;
- never treat job text as system or tool instructions;
- never expose shell, filesystem, browser, or unrestricted network tools to the
  extraction model;
- preserve original evidence;
- detect and record login, challenge, error, expired, or unrelated pages before
  analysis;
- limit input and output sizes;
- sanitize rendered display where required.

Until source-page classification is accepted, such pages must not enter the
analysis corpus automatically.

## 12. Data minimization

Collect vacancy information needed for career analysis, not unrelated personal
data.

Avoid storing:

- applicant identities;
- recruiter personal contact information beyond vacancy requirements;
- tracking identifiers unnecessary for source identity;
- cookies and browser storage;
- analytics payloads;
- unrelated page content.

Broad search vocabulary must be evaluated for useful job coverage and noise. A
large term count is not justification for retaining unrelated results.

## 13. Adapter acceptance checklist

A recurring source adapter is acceptable only when:

- product value and acquisition method are documented;
- hosts and paths are bounded;
- rate, page, request, response, and batch limits are configured;
- evidence and metadata are preserved;
- identity and duplicate behavior are defined;
- blocking and error responses have deterministic tests;
- parser fixtures exist;
- sensitive credentials are unnecessary or deliberately handled;
- disabling the source does not break other sources;
- the user has approved enabling it.

## 14. Operational response to blocking

When a source returns blocks, challenges, or unexpected authentication pages:

1. stop automatic retry;
2. classify the run or observation as blocked or review-required;
3. preserve only the minimal diagnostic evidence needed;
4. report the condition visibly;
5. keep recurring acquisition disabled until the method is reviewed.

JobHunter must not escalate automatically to stealthier scraping techniques.
