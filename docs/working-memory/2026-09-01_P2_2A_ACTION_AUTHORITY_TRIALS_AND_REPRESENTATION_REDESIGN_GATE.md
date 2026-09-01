# P2.2A Action-Authority Trials and Representation Redesign Gate

**Date:** 2026-09-01
**Scope:** P2.2A real-local semantic/product acceptance
**Status:** Existing v1.3 implementation restored; acceptance remains open; representation redesign decision required before more live-anchor generation

## 1. Starting authority boundary

The accepted P1.6 dependencies did not change:

```text
tG9K → accepted English P1.6 artifact 36
tmyX → accepted English P1.6 artifact 46
```

The two repeated action-authority cases were:

```text
tG9K responsibility 6
→ Partner with the semiconductor technical lead and engineering to move models toward production.

tmyX role purpose 0
→ Assess security posture of servers and Microsoft services and to develop and provide
  security requirements, Best Practices, and hardening solutions.
```

The acceptance question was whether candidate synthesis could remain useful without turning these
relationships into direct deployment, production completion, implementation, or hardening
execution.

## 2. Controlled trials

All trials retained the accepted P1.6 evidence and candidate schema
`job-work-intelligence-v1`. Historical artifacts and failed attempts remain immutable in local
SQLite.

```text
attempt 10  tG9K  v1.3 / 4B
→ full-document authority reviewer omitted all work themes twice
→ failed safely; no artifact

artifact 7  tG9K  v1.4 / 4B
→ compact document-level verdict persisted structurally
→ reviewer accepted direct `deploying` wording

artifact 8  tG9K  v1.5 / 4B
→ field-complete review removed direct ownership language
→ still changed `toward production` to `partnering in deployment`

attempt 13  tG9K  v1.5 / 12B
→ semantic reasoning preserved collaborative production readiness
→ full generation omitted work themes twice; no artifact

attempt 14  tG9K  v1.6 / split 4B generation + 12B field review
→ reviewer exhausted the 4,096-token cap; no artifact

artifact 9  tG9K  v1.6 / split 4B generation + 12B field review
→ completed only after an 8,192-token reviewer allowance and roughly half-hour latency
→ removed direct deployment ownership but changed `toward production` to `into production`
→ operationally unsuitable for repeated-use UX

artifact 10  tG9K  v1.7 / 4B
→ useful three-theme grouping
→ top summary and role interpretation no longer assigned direct deployment ownership
→ one collaborative theme still used `moving models into production environments`
→ useful candidate evidence, not sufficient proof that free-form action review is reliable

artifact 11  tmyX  v1.7 / 4B
→ useful three-theme grouping
→ theme/role prose preserved `developing hardening solutions`
→ top summary strengthened the role purpose into directly `hardening the security posture`
→ cross-job material action-authority defect remains
```

## 3. Finding

The trials separate three facts:

1. Model grouping and job-level role/work synthesis remain useful and materially reduce manual
   reading.
2. Stronger/larger models and field-complete semantic review improve some wording but do not
   reliably preserve action relationship and lifecycle endpoint across heterogeneous jobs.
3. Requiring a model to rewrite or approve every action-bearing summary is both semantically
   unreliable and, for the 12B split route, operationally too slow.

This is not evidence for a deterministic action-verb equivalence table. It is evidence that the
representation asks free-form candidate prose to carry more factual action authority than it can
reliably preserve.

## 4. Source-code disposition

The v1.4-v1.7 protocol/model-role experiments were not retained in repository source. The worktree
was restored to committed v1.3 behavior and focused Ruff/tests passed. No unaccepted 12B model role,
configuration surface, schema migration, or prompt identity remains in source.

Local SQLite deliberately preserves artifacts 4-11 and all attempt records. All five accepted
English P1.6 v20/v5 chains remain present and unchanged.

## 5. Next plan decision

Do not run more prompt-only or model-only action-authority trials. Before generating `t4qV`, amend
the focused P2.2A representation plan around this bounded architecture direction:

```text
accepted/current P1.6 direct-work statements
→ model candidate grouping and relative emphasis
→ deterministic injection of exact accepted work statements inside each theme
→ optional clearly labeled candidate interpretation kept separate from factual action wording
→ deterministic reference/coverage/currentness validation
→ persisted candidate artifact and browser presentation
```

The amendment must decide which free-form fields remain useful, which action-bearing fields become
source-injected, and how the browser visually separates exact employer/P1.6 work from JobHunter
interpretation. It must preserve useful grouping and avoid turning P2.2A into exhaustive
canonicalization.

## 6. Boundaries

- P2.2A remains open.
- Do not start P2.2B.
- Do not publish Work Intelligence.
- Do not add deterministic verb-equivalence machinery.
- Do not rerun closed Phase-1/P2.1 gates.
- Do not delete or rewrite artifacts 4-11 or their attempt history.
