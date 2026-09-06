# P2.2B-B1 `ta9l` Local-Runtime Preflight

**Date:** 2026-09-06  
**Status:** REPOSITORY PREFLIGHT COMPLETE / LOCAL RUNTIME REQUIRED NEXT  
**Branch:** `main`  
**Controlling plan:** `docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`

## 1. Purpose

Prepare the exact next B1 operation before touching local runtime, confirm there is no repository-side ambiguity, and preserve the semantic stop conditions so the local run cannot accidentally turn into automatic promotion.

## 2. Current committed `ta9l` source state

Committed public source projection confirms:

```text
source job id:          ta9l
role:                   Senior Applied AI Engineer
company:                Mofid Securities
current detail version: 25
parser:                 jobinja-detail-v2
parse status:           parsed
lifecycle:              active
semantic sha256:        cd9dbf6be622113836b951e9042c87798954fc01dea520ba08b090eae2b54fc6
```

The relevant employer duty remains exactly:

```text
Create evaluation, testing, and observability frameworks for LLM and agent performance.
```

Other nearby responsibilities include semantic/knowledge layers, AI agents/RAG, retrieval pipelines, and entity-resolution/text-to-SQL work. The selected evaluation/testing/observability duty is therefore a distinct direct responsibility in the source rather than a qualification or title-only inference.

## 3. Current missing dependency

The committed public corpus contains `corpus/jobs/ta9l/source.json` but no current `english-projection.json` for `ta9l`.

Therefore B1 cannot yet establish an accepted/current English P1.6 responsibility claim for the candidate duty.

This is the genuine next dependency, not documentation drift.

## 4. Current CLI contract verified

Repository CLI/runtime inspection confirms the intended explicit-job path:

```text
jobhunter translations run <job-id>
jobhunter translations show <job-id>
jobhunter jobs analyze <job-id> --mode english
jobhunter jobs review-analysis <job-id> status
jobhunter jobs review-analysis <job-id> accept|reject --reason "..."
```

`jobs analyze` is explicitly designed to build/reuse one P1.6 artifact without discovery, refresh, translation, or batch orchestration. `review-analysis` resolves the current English projection and only reviews the P1.6 artifact matching the configured current English contract/dependency.

Current English P1.6 authority remains:

```text
job-analysis-english-v20 / job-analysis-v5
```

## 5. Exact local execution packet

Use the actual local configuration path. If the normal default `jobhunter.toml` is already the intended runtime configuration, `--config` may be omitted. Otherwise substitute the real local path for `<config>`.

### Step A — local/provider preflight

```bash
jobhunter --config <config> doctor
jobhunter --config <config> translations status
jobhunter --config <config> translations models
```

Purpose:

- confirm SQLite/local paths resolve to the real owner runtime;
- confirm the intended local LM Studio provider/model identity;
- do not proceed against a fresh/empty database by mistake.

### Step B — build/reuse only the `ta9l` English projection

```bash
jobhunter --config <config> translations run ta9l
jobhunter --config <config> translations show ta9l
```

Verify that the resulting current projection depends on current source detail/version 25 / semantic identity above and preserves the selected responsibility meaning without semantic strengthening or weakening.

### Step C — build/reuse only the `ta9l` English P1.6 candidate

```bash
jobhunter --config <config> jobs analyze ta9l --mode english
jobhunter --config <config> jobs review-analysis ta9l status
```

`review-analysis status` must be used to inspect the complete current artifact before any accept/reject mutation.

## 6. Semantic review questions

Review the entire P1.6 artifact, not only the desired candidate responsibility.

For the selected B1 question specifically, determine:

1. Does P1.6 preserve a direct responsibility corresponding to:

```text
Create evaluation, testing, and observability frameworks for LLM and agent performance.
```

2. What is the exact persisted responsibility index and statement?
3. What exact source evidence is attached?
4. Did the extractor split the source duty into multiple responsibilities?
5. Did it weaken `create ... frameworks` into generic familiarity/support?
6. Did it strengthen it into unsupported ownership, deployment, lifecycle, production operation, or broader AI reliability authority?
7. Did it merge this duty with unrelated RAG/retrieval/entity-resolution work?
8. Does the full artifact satisfy ordinary P1.6 factual/coverage/depth/optionality rules sufficiently for acceptance?

Do not accept an otherwise materially defective P1.6 artifact merely because this one responsibility looks useful for B1.

## 7. Accept/reject boundary

Only after complete semantic review:

```bash
jobhunter --config <config> jobs review-analysis ta9l accept --reason "<specific semantic review note>"
```

or:

```bash
jobhunter --config <config> jobs review-analysis ta9l reject --reason "<specific defect>"
```

Acceptance is not predetermined by this preflight.

A rejection is a valid B1 outcome and must stop the proposed canonical mutation until the focused plan authorizes another evidence decision.

## 8. Final correspondence gate after acceptance

Only if `ta9l` P1.6 is accepted/current, compare its exact accepted responsibility against:

```text
tG9K P1.6 artifact 36 responsibility[5]
Design rigorous validation and monitoring for models running in an industrial setting.
```

Tentative canonical identity remains unpromoted:

```text
responsibility:design-ai-evaluation-monitoring
Design AI evaluation and monitoring
```

The pair is eligible only if both exact accepted claims preserve the same reusable semantic core without losing a material extra action/object/ownership/lifecycle endpoint or compound duty.

Source-specific detail must remain recoverable:

```text
tG9K → industrial-setting models; rigorous validation + monitoring
ta9l → LLM/agent performance; evaluation + testing + observability frameworks
```

If correspondence is not non-lossy, record B1 NO-PROMOTION / DEFER. Do not broaden the concept to force a success.

## 9. Promotion remains a separate step

Even after P1.6 acceptance, do **not** automatically mutate the Canonical Registry.

Required order remains:

```text
accepted ta9l P1.6
→ report exact artifact/responsibility/evidence
→ final two-claim semantic correspondence review
→ only then possible one-concept/two-mapping mutation
→ idempotency/currentness/CLI/browser verification
→ B1 closure decision
```

## 10. Market/role-family track interaction

The owner has now explicitly activated the future Market/role-family responsibility, but that activation is queued behind B1.

```text
Market/role-family activation → GIVEN
Market foundation audit       → QUEUED
current executable frontier   → ta9l B1 local-runtime gate
```

After B1 closes, the planned Market/role-family foundation investigation may begin directly without a second activation ceremony unless the owner changes direction.

## 11. Exact handoff

Repository-side preparation is complete.

Next executable action requires the owner's real local JobHunter SQLite state and local inference/translation provider:

```text
doctor/status/models
→ translations run ta9l
→ translations show ta9l
→ jobs analyze ta9l --mode english
→ review-analysis ta9l status
→ complete semantic review
→ accept or reject with explicit reason
```

No Market-v2 implementation, P2.2C family work, or Canonical Registry mutation is authorized before this gate resolves.