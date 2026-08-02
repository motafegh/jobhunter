# JobHunter Operations, Reliability, Testing, and Observability Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B103-B107, B114-B115, B117-B120, B122

---

## Purpose

This family covers repeated-run reliability as JobHunter grows from individual bounded operations toward full workflows and longitudinal use. The objective is not to build a generic workflow engine or observability platform; it is to make important work resumable, diagnosable, reproducible, and safe under partial failure.

---

## B103 — Durable workflow runs

**Intent:** Preserve what happened during a complete multi-stage workflow beyond the lifetime of an in-memory browser operation.

**Proposal:** Introduce a lightweight durable `WorkflowRun` and optional `WorkflowStageRun` model once full-workflow operation history becomes useful.

**Possible stages:**

```text
discovery
priority/detail acquisition
parser/audit
translation
semantic analysis
aggregation/reporting
```

**Design direction:** Store inputs/bounds, stage status/counts, start/end time, affected record references, failures, and completion summary. Existing domain stores remain the source of actual job/evidence state.

**Guardrails:** Do not duplicate every domain event into a workflow database. Workflow records explain orchestration, not replace evidence/analysis stores.

**Promotion signal:** When users need reliable history across application restarts or need to compare repeated full runs.

---

## B104 — Partial-success semantics

**Intent:** Represent multi-stage workflows accurately when some stages succeed and others fail.

**Proposal:** A workflow should distinguish outcomes such as `completed`, `completed_with_failures`, `blocked`, `cancelled`, or `failed_before_progress`, plus per-stage result states.

**Design direction:** Example: source acquisition can succeed, translation can partially fail, analysis can succeed for eligible jobs, and Market can update from accepted analyses. The operation summary should state each part explicitly.

**Guardrails:** Do not roll back valid immutable acquisition/analysis work merely to make the workflow look atomic.

**Promotion signal:** Near-term for the current end-to-end browser workflow.

---

## B105 — Resume after crash/interruption

**Intent:** Avoid repeating expensive successful work when the application stops mid-batch.

**Proposal:** Make long-running batches naturally resumable from durable artifact state. If 18 of 30 translations/analyses are current, a resumed run should select only the remaining eligible records under the same requested contract.

**Design direction:** Prefer idempotent selectors and current-artifact checks over checkpointing every loop iteration. WorkflowRun may remember original intent/bounds for convenience.

**Guardrails:** Do not resume automatically after configuration/contract changes without re-evaluating eligibility.

**Promotion signal:** When real batch sizes make interruption costly.

---

## B106 — Scheduled operation policies

**Intent:** Support repeated maintenance without manual invocation once all stages are proven idempotent and bounded.

**Proposal:** Future schedules might include light daily discovery, bounded weekly refresh, periodic translation/analysis catch-up, and market snapshot generation.

**Design direction:** Schedules invoke the same application services as browser/CLI operations, with explicit bounds, lock/concurrency rules, and durable run history.

**Guardrails:** No scheduler until manual workflows are accepted. Scheduled jobs must never bypass source rate limits, review gates, cost/privacy policies, or current single-mutator safety.

**Promotion signal:** Phase 5 sustained-operation capability.

---

## B107 — Actionable notifications

**Intent:** Notify only when a future or completed event materially affects user action.

**Proposal:** Notification candidates include an important target job appearing/changing, an interested job becoming unavailable, a scheduled workflow requiring attention, a model/source provider remaining unhealthy, or a review backlog crossing a configured threshold.

**Design direction:** Start with in-app notifications/change summaries; OS/email channels require separate privacy/configuration decisions.

**Guardrails:** Avoid success-noise such as notifying on every routine request. User controls categories/cadence.

**Promotion signal:** After scheduled/repeated workflows exist.

---

## B114 — Reproducible market/data snapshots

**Intent:** Freeze enough analytical context to compare results over time and reproduce reports/decisions.

**Proposal:** Create snapshot manifests referencing the exact eligible job/source versions, analysis contract, taxonomy version, filters/source scope, and creation time.

**Design direction:** Prefer immutable manifests/references rather than copying the entire SQLite database for every analytical snapshot. Raw evidence remains in its existing immutable store.

**Guardrails:** Snapshot retention should be bounded/configurable. A snapshot does not imply source data itself was complete.

**Promotion signal:** Before trend analysis and durable reports depend on historical comparability.

---

## B115 — Migration Inspector

**Intent:** Make schema/data migrations visible and recoverable as the SQLite model grows.

**Proposal:** A System surface/CLI command could show current schema version, required version, applied migrations, pending migrations, backup/recovery guidance, and last migration outcome.

**Design direction:** Migrations remain deterministic code with tests. A pre-migration backup/snapshot can be offered for high-risk changes.

**Guardrails:** Do not expose arbitrary schema-edit controls in the browser.

**Promotion signal:** When migration count/complexity makes troubleshooting opaque.

---

## B117 — Artifact-staleness explanation

**Intent:** Explain why a translation, analysis, aggregate, report, or recommendation is no longer current.

**Proposal:** Build dependency-aware staleness reasons such as:

```text
source semantic version changed
translation contract changed
analysis contract changed
taxonomy version changed
personal evidence changed
market snapshot superseded
```

**Design direction:** Current-artifact resolution already encodes parts of this concept. Expose those reasons through stores/UI rather than relying on hidden equality checks.

**Guardrails:** Stale is not failed. Historical artifacts remain valid records of past inputs.

**Promotion signal:** As multiple versioned layers begin to depend on one another.

---

## B118 — Regression corpus

**Intent:** Preserve real source/model failure cases as durable tests.

**Proposal:** Maintain curated fixtures for unusual HTML, Persian/English mixtures, ambiguous requirement language, long descriptions, translation association failures, lifecycle edge cases, duplicate/repost scenarios, and other real incidents.

**Design direction:** Each regression fixture records why it exists and what invariant it protects. Keep normal tests offline/deterministic.

**Guardrails:** Sanitize/handle source content appropriately and avoid huge fixture growth when a minimal reproducer is sufficient.

**Promotion signal:** Permanent engineering practice; add cases whenever real failures reveal a new class.

---

## B119 — Property-based tests for deterministic invariants

**Intent:** Exercise large input spaces for pure logic where example tests are insufficient.

**Proposal:** Candidate targets include URL canonicalization, Unicode/search normalization, semantic hashing, stable identity, schema round-trips, deduplication, and bounded selection logic.

**Design direction:** Add property-based tooling only where it finds edge cases more efficiently than hand-written examples.

**Guardrails:** Do not use generated tests for network/model behavior where deterministic fakes and explicit cases are clearer.

**Promotion signal:** When repeated edge cases appear in pure transformation logic.

---

## B120 — Fault-simulation suite

**Intent:** Validate end-to-end failure handling without live outages.

**Proposal:** Deterministically simulate conditions such as HTTP 429/5xx, timeout, redirect, challenge content, corrupt HTML, database locking where practical, LM Studio timeout, truncated output, invalid JSON, and provider unavailability.

**Design direction:** Verify classification, retry bounds, evidence preservation, partial-success behavior, and user-visible diagnostics.

**Guardrails:** Fault tests must remain isolated and should not require real Jobinja/provider calls.

**Promotion signal:** Expand with each operational boundary.

---

## B122 — Performance and capacity observability

**Intent:** Measure real bottlenecks before introducing architectural complexity.

**Proposal:** Track bounded operational metrics such as DB query latency, source acquisition latency, translation/analysis latency, jobs/minute, token counts, queue/run duration, database size, evidence-store size, and selected slow operations.

**Design direction:** Start with structured logs/timing summaries and System diagnostics. Add persistent metrics only when trend history matters.

**Guardrails:** Do not build Prometheus/Grafana/distributed tracing for a local personal app without a demonstrated need. Never log sensitive payloads/secrets merely for observability.

**Promotion signal:** When performance begins to affect repeated use or architectural decisions.

---

## Category-level recommendation

The immediate reliability priorities are partial-success semantics, clear operation results, idempotent resumability, warning-free deterministic tests, and explicit staleness. Durable orchestration/scheduling should be earned by stable workflows rather than introduced ahead of them.