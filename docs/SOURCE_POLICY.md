# JobHunter Source Acquisition and External Processing Policy

## 1. Purpose

JobHunter must collect useful job-market evidence without bypassing access controls,
violating source restrictions, or becoming an unreliable crawler.

This policy also defines the boundary between **source acquisition**, local derived
processing such as LM Studio translation, and optional external processing such as
Google Cloud Translation.

## 2. Default position

A recurring source is disabled until it has an explicit source definition or an
approved source-specific implementation plan.

Every source definition should state what is collected, whether it is public, the
acquisition method, approved hosts/paths, known source constraints, conservative
bounds, review date, and enabled state.

The system fails closed when source permission or technical behavior is unclear.

## 3. Acceptable source inputs

- user-supplied job text or local files;
- individual permitted public URLs;
- official public job APIs/feeds;
- public ATS endpoints intended to publish vacancies;
- embedded structured job data;
- approved public career/search pages accessible without authentication.

## 4. Prohibited acquisition

JobHunter must not:

- automate LinkedIn or another authenticated platform;
- use stored personal browser sessions, passwords, or private cookies;
- bypass CAPTCHA, anti-bot systems, paywalls, login walls, or access controls;
- rotate proxies or identities to defeat limits;
- ignore explicit denial or repeated blocking;
- scrape private applicant/recruiter/user data;
- submit applications or recruiter messages automatically;
- operate an unrestricted internet-wide crawler.

Technical possibility is not permission.

## 5. Acquisition-method preference

Prefer:

1. official public API/feed;
2. embedded structured data;
3. static public HTML;
4. rendered public HTML only when explicitly approved and necessary;
5. manual user import.

Rendered-browser acquisition is not an automatic fallback.

## 6. Active Jobinja request behavior

The active Jobinja adapter uses:

- explicit timeouts;
- approved-host/path validation and redirect revalidation;
- sequential requests;
- descriptive user agent;
- configured delay;
- per-search page limits;
- global run-level request budget;
- response-size/content-type limits;
- immutable evidence before parsing;
- bounded detail batches;
- visible run-level and per-job failures.

A large bilingual search catalog does not authorize broader crawling. Each expanded
term remains one bounded request plan against the approved Jobinja search endpoint.

## 7. Retry maturity

The accepted Jobinja path currently performs one controlled attempt per selected search
page or detail check.

Automatic Jobinja retry/backoff must not be enabled until `429`, `403`, login,
challenge, CAPTCHA, timeout, and transient-server responses are classified.

A blocked/challenge response must never trigger aggressive retry.

## 8. Robots, terms, and access controls

Robots directives, source terms, API documentation, and technical controls answer
different questions. Absence of a robots prohibition is not universal permission,
and JobHunter must not bypass explicit technical or contractual restrictions.

## 9. Source allowlist and SSRF

Recurring acquisition uses explicitly configured adapters, hosts, and paths.

Any future generic URL adapter must validate schemes, hosts, redirects, DNS/IP ranges,
response size/type, and must reject localhost, private/link-local ranges, cloud metadata
addresses, and redirects into blocked networks.

The current Jobinja adapter reduces this risk through a fixed host allowlist and path
validation.

## 10. Content handling

Retrieved pages are untrusted data.

The pipeline must:

- never execute retrieved scripts;
- never treat job text as system/tool instructions;
- preserve original evidence;
- detect source error/login/challenge/expired/unrelated pages before analysis;
- limit input/output sizes;
- never grant source text unrestricted shell/filesystem/browser/network tools.

## 11. Data minimization

Collect vacancy information needed for career analysis, not unrelated personal data.
Avoid applicant identities, unnecessary recruiter personal data, cookies, browser
storage, analytics payloads, and unrelated page content.

## 12. Translation is not source acquisition

Translation operates only **after** public source acquisition and deterministic
parsing. It does not discover new URLs, broaden the Jobinja crawl, or change source
semantic identity.

The normal translation provider is local LM Studio:

```toml
translation_provider = "lm-studio"
```

Google Cloud Translation is an optional external provider:

```toml
translation_provider = "google-cloud"
```

## 13. Local LM Studio processing boundary

When LM Studio runs on a loopback URL such as:

```text
http://127.0.0.1:1234/v1
```

translation stays within the local-machine processing boundary.

The local provider must:

- send only parsed job text needed for English projection;
- use bounded model requests and retries;
- use structured output and validate returned items;
- record exact model/provider-contract identity with derived artifacts;
- avoid granting the model tools, shell, filesystem, browser, or unrestricted network
  access;
- fail visibly rather than manufacturing translations from malformed output.

If the user configures LM Studio on another host or non-loopback interface, that
network path becomes a deliberate deployment boundary and must not be described as
strictly on-machine processing.

## 14. Optional Google Cloud external boundary

The Google provider uses Cloud Translation Basic v2. Selecting it intentionally sends
parsed vacancy text containing Persian to Google for English translation.

This must remain explicit in configuration and operation. Google is not required for
normal JobHunter use.

## 15. Translation data minimization

The translation pipeline may process source job fields needed to construct the English
job representation. It must not send or expose through the translation provider:

- personal capability/profile records;
- credentials or local paths;
- raw browser/session data;
- unrelated evidence metadata;
- private user notes;
- P1.6 prompts/responses unrelated to translation.

Native-English strings require no translation-provider call.

## 16. External translation credentials and quotas

When Google Cloud is selected, its API credentials must:

- stay outside Git;
- preferably be provided through `JOBHUNTER_GOOGLE_TRANSLATION_API_KEY`;
- never appear in artifact metadata or exported corpora;
- be restricted to the intended Translation API when possible;
- be protected by appropriate project quota/billing controls.

LM Studio translation requires no Google credential. A local LM Studio API token, when
configured, follows the same secret-handling rule and must stay outside committed
configuration.

## 17. Translation evidence status

Machine translation is **derived data**, not employer evidence.

The system must retain:

- source semantic-version identity;
- original employer fields/text;
- translation provider contract/model/schema;
- native-versus-translated segment provenance;
- translation artifact identity and operational attempt history.

A translation must never silently strengthen, weaken, or replace an original
requirement. Later LLM/ML analysis may consume the English view, but material claims
remain traceable to original source text.

## 18. Provider failure

A local-model failure, Google outage, credential problem, quota error, or malformed
translation response:

- must not modify source evidence;
- must not create a false semantic job version;
- must be recorded as a failed translation attempt when applicable;
- may be retried later explicitly or through a bounded missing-translation queue.

## 19. Source-adapter acceptance checklist

A recurring source adapter is acceptable only when product value/method are documented,
hosts/paths and resource usage are bounded, evidence is preserved, identity/duplicate
behavior is defined, blocking/error conditions are tested, and credentials are
unnecessary or deliberately handled.

## 20. Operational response to source blocking

When a source returns blocking/challenge/authentication responses:

1. stop automatic retry;
2. classify/report the condition;
3. preserve only minimal diagnostic evidence needed;
4. keep recurring acquisition disabled until reviewed;
5. never escalate automatically to stealthier scraping techniques.
