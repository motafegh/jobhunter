# JobHunter Privacy, Security, Backup, Portability, and Local-App Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B108-B113, B174-B176, B178-B183

---

## Purpose

This family preserves JobHunter's local-first trust boundary as the product gains more source adapters, model providers, personal evidence, exports, and richer UI. The guiding principle is that convenience must not make data flow opaque. Public employer data, private personal evidence, credentials, and generated artifacts have different handling requirements.

---

## B108 — Privacy dashboard

**Intent:** Make it obvious what data stays local and what configured features can send data outside the machine.

**Proposal:** Add a System/Privacy surface showing active providers, local versus external processing, enabled external capabilities, data classes each provider may receive, and recent external-processing status.

**Design direction:** Display policy and configuration rather than every low-level network packet. Link to the egress ledger for actual recorded calls.

**Guardrails:** Do not claim “nothing leaves the device” when external translation/model/source requests are enabled. Be explicit about public job text versus personal data.

**Promotion signal:** Before multiple remote inference providers or personal evidence processing are enabled.

---

## B109 — External egress ledger

**Intent:** Record when JobHunter intentionally sends content to external processors/APIs.

**Proposal:** Maintain a privacy-oriented ledger with fields such as timestamp, provider, purpose/task, data classification, record/reference, and outcome. Example: `Google translation — public employer field — no personal profile data`.

**Design direction:** Avoid storing secrets or full sensitive payloads in the ledger. Reference durable records and policy categories instead.

**Guardrails:** Normal source acquisition requests are operational network activity and may be summarized separately; the ledger should focus on privacy-relevant data egress rather than becoming a full packet log.

**Promotion signal:** Before external AI providers process more than public job data.

---

## B110 — Explicit market-data / personal-data boundary

**Intent:** Prevent future personal evidence from accidentally entering pipelines designed for public job data.

**Proposal:** Introduce data-sensitivity classes and enforce them at service/provider boundaries. Public source text, derived public analysis, personal evidence, and secrets should have distinct policies.

**Design direction:** Provider routing and export code declare accepted data classes. Personal records live in dedicated domain tables/stores and are not added to translation/RAG indexes by default.

**Guardrails:** Do not rely on prompt instructions alone to protect personal data. The application layer enforces routing.

**Promotion signal:** Mandatory before Phase-3 personal evidence is sent to any model/retrieval system.

---

## B111 — Sensitive evidence controls

**Intent:** Give the user control over personal evidence that should not be included in model processing, exports, or application preparation.

**Proposal:** Allow evidence records or categories to be marked with processing/export policies such as `local_only`, `exclude_from_ai`, `exclude_from_export`, or `private_note`.

**Design direction:** Policy is enforced by data-access/query services, not merely hidden in the UI.

**Guardrails:** Avoid overly complicated ACL systems for a single-user app. A few understandable privacy flags are preferable.

**Promotion signal:** Alongside personal evidence storage.

---

## B112 — Tested backup and restore

**Intent:** Protect years of local evidence, corrections, and career history from machine/database loss.

**Proposal:** Provide a supported backup format covering SQLite, immutable evidence files, configuration required for interpretation, reviewed taxonomy/corrections, and personal evidence where enabled.

**Design direction:**

- create backups while writes are safely quiesced or through SQLite-safe mechanisms;
- include manifest/schema/application version;
- validate restore into a temporary/test destination;
- allow encrypted backup as a later option when personal data exists.

**Guardrails:** Model binaries and reproducible external dependencies need not be duplicated unless required. Secrets should not be exported in plaintext.

**Promotion signal:** High priority before the application holds irreplaceable personal evidence.

---

## B113 — Structured data export

**Intent:** Keep JobHunter data portable and inspectable outside the application.

**Proposal:** Offer versioned exports for selected domains such as raw/source corpus manifests, English corpus, semantic analysis corpus, canonical market matrices, personal evidence, gaps, and reports.

**Design direction:** Exports have schemas, provenance references, creation time, filter scope, and contract versions. Separate public-market exports from personal/private exports.

**Guardrails:** Do not export credentials, transient operation internals, or private notes unless explicitly selected.

**Promotion signal:** Add exports as real downstream use cases appear rather than building every format immediately.

---

## B174 — Local desktop packaging

**Intent:** Make JobHunter feel like an installable local application while preserving the Python/server-rendered architecture.

**Proposal:** Investigate packaging that provides an application launcher, predictable local data directory, startup/shutdown management, upgrade guidance, and eventually installer bundles where maintainable.

**Design direction:** The packaged app can still run the local FastAPI server on loopback and open the user's browser or embedded safe shell only if justified.

**Guardrails:** Do not rewrite into Electron/native mobile solely for packaging. Packaging must not hide logs/data paths needed for recovery.

**Promotion signal:** After core workflows stabilize enough that installation friction becomes a major usability issue.

---

## B175 — Offline analytical mode

**Intent:** Ensure stored career intelligence remains usable without internet access.

**Proposal:** Browsing existing jobs, market analytics, personal evidence, reviews, reports, and local-model analysis should work offline where dependencies are local. Acquisition/source refresh and configured remote providers fail clearly as unavailable.

**Design direction:** Separate network-required capabilities from local read/compute paths. System status shows offline/degraded mode rather than failing the entire application.

**Guardrails:** Do not claim full offline operation if a selected model/provider is remote.

**Promotion signal:** Natural local-first quality target as provider abstractions grow.

---

## B176 — Workspace import/export portability

**Intent:** Move a JobHunter installation between computers without reconstructing state manually.

**Proposal:** Build a workspace bundle/restore workflow using the supported backup/export schema. The bundle includes database/evidence/configuration manifests and validates versions on import.

**Design direction:** Migration can support copy-to-new-machine and disaster recovery. Personal/secrets handling is explicit.

**Guardrails:** Avoid platform-specific absolute paths inside durable records where possible. Never silently overwrite an existing workspace.

**Promotion signal:** After backup/restore is accepted.

---

## B178 — Red-team untrusted acquired content

**Intent:** Treat job descriptions and imported content as adversarial data that may contain instructions designed to manipulate models or UI.

**Proposal:** Add security tests and model-boundary prompts/structures ensuring source text is always data, even if it contains strings such as `SYSTEM:` or `ignore previous instructions`.

**Design direction:** Use structured request envelopes, strict schemas, deterministic evidence validation, and no model tools that could execute source instructions.

**Guardrails:** Prompt wording alone is insufficient; tool and application permissions must enforce the boundary.

**Promotion signal:** Permanent requirement for every model workflow consuming acquired text.

---

## B179 — Evidence-poisoning tests

**Intent:** Verify that malicious source content cannot cause false personal/readiness conclusions or escape its evidence role.

**Proposal:** Regression fixtures should include postings that explicitly try to instruct the model to mark the candidate qualified, change system behavior, disclose secrets, or fabricate facts.

**Design direction:** The accepted result should either extract employer-language facts with valid evidence or reject invalid model output. No source instruction gets execution authority.

**Guardrails:** Keep test payloads inert and local.

**Promotion signal:** Extend current semantic-analysis security tests as agent/RAG capability grows.

---

## B180 — HTML sanitization and safe rendering

**Intent:** Ensure preserved/source HTML cannot execute scripts or load unsafe external resources when viewed in JobHunter.

**Proposal:** Render parsed/plain fields by default. If raw HTML inspection is provided, sanitize/escape it and prevent scripts, event handlers, unsafe URLs, frames, and remote-resource loading.

**Design direction:** Keep the existing restrictive CSP and server-rendered escaping. Raw evidence download/view can use a safe text representation.

**Guardrails:** Never render arbitrary source HTML as trusted page content.

**Promotion signal:** Permanent web-security invariant; add explicit raw-evidence UI tests if such a surface is built.

---

## B181 — Network-exposure hardening if loopback is intentionally expanded

**Intent:** Define the security work required before JobHunter is used across a LAN or remotely.

**Proposal:** Non-loopback use should trigger a separate threat model covering authentication, TLS/secure transport, origin/host validation, sessions, CSRF, rate limits, access logging, and exposure of personal evidence.

**Design direction:** Keep loopback the default. `--allow-network` remains explicit and should carry clear warnings until full remote-use controls exist.

**Guardrails:** Do not treat a LAN as inherently trusted. Do not add cloud/multi-user architecture unless explicitly approved.

**Promotion signal:** Only if real remote/LAN use becomes a product requirement.

---

## B182 — Secret management improvement

**Intent:** Store provider/API credentials more safely and conveniently than source files or plaintext application records.

**Proposal:** Continue environment-variable references initially; later evaluate OS keyring/secret-store integration if multiple remote providers make credential management painful.

**Design direction:** Configuration stores credential references, never secret values. Logs, artifacts, exports, and exception messages are scrubbed.

**Guardrails:** Do not introduce a custom cryptographic secret vault without a strong reason.

**Promotion signal:** When external-provider usage becomes normal rather than experimental.

---

## B183 — Strict local/privacy mode

**Intent:** Let the user guarantee that no external AI/translation provider receives content during a session/configuration mode.

**Proposal:** Add a policy mode that disables all non-source external processing and rejects attempts to route translation/analysis/personal data to remote providers. Source acquisition can remain separately configurable because it necessarily contacts job sources.

**Design direction:** System/Privacy visibly shows when strict-local mode is active and which functions are unavailable.

**Guardrails:** The mode must be enforced in provider composition, not merely a UI label.

**Promotion signal:** When multiple local/remote inference routes exist.

---

## Category-level recommendation

Backup/restore, explicit data classes, and untrusted-content boundaries are architectural fundamentals. Desktop packaging, portability, remote exposure, and richer privacy controls should be driven by actual repeated-use needs, but future personal evidence should never be added before its storage, processing, export, and backup boundaries are explicit.