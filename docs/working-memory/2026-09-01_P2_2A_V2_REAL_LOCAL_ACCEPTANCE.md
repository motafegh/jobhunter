# P2.2A Work Intelligence v2 Real-Local Acceptance

**Status:** ACCEPTED — P2.2A CLOSED / P2.2B NOT STARTED
**Date:** 2026-09-01
**Scope:** Recorded P2.2A v2 real-local acceptance sequence only
**Controlling amendment:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`

## 1. Environment and checkout

The acceptance run started from clean `main` at:

```text
cebdbb7  docs: reconcile AGENTS with P2.2A Work Intelligence v2
local main == origin/main
```

Real-local prerequisites were available:

```text
SQLite:    data/jobhunter.sqlite3
LM Studio: http://127.0.0.1:12345/v1
model:     gemma-4-e4b-it-ud
```

The configured model was present in the live `/v1/models` response. No v2 Work Intelligence
artifact existed before this sequence. Historical v1 artifacts 1-11 remained unchanged.

The virtual environment did not contain a generated `jobhunter-work` console-script wrapper, so
the equivalent installed module entry point was used:

```bash
.venv/bin/python -m jobhunter.work_intelligence_cli ...
```

The absent wrapper caused no SQLite mutation and is a local editable-install/setup detail, not a
Work Intelligence product failure.

## 2. `t4qV` direct-work generation and review — PASSED

Command:

```bash
.venv/bin/python -m jobhunter.work_intelligence_cli generate t4qV
```

Result:

```text
outcome:             completed
artifact:            12
P1.6 dependency:     44
model:               gemma-4-e4b-it-ud
prompt/runtime:      job-work-intelligence-v2.0
schema:              job-work-intelligence-v2
semantic state:      candidate
evidence status:     sufficient
themes:              3
semantic repair:     none
provider finish:     stop
```

Candidate theme structure:

```text
primary    Security Architecture and Policy Implementation
primary    Perimeter Defense and Connectivity Management
supporting Security Operations, Support, and Documentation
```

Stored-artifact verification against accepted P1.6 artifact 44 proved:

```text
accepted responsibilities:            10
distinct accepted items in themes:    10
kind/index/statement/confidence match: exact
coverage:                              10/10
removed v1 work_summary/summary:       absent
dedicated semantic repair/review pass: absent
```

The three themes materially reduce manual synthesis effort while keeping all accepted work visible
at the evaluation point. Architecture/policy, firewall/VPN operations, and
troubleshooting/documentation remain distinct rather than collapsing into one generic security
theme. Candidate labels/rationales and the candidate role interpretation are visibly labeled as
JobHunter interpretation. Exact accepted P1.6 statements, including the long technical-
documentation responsibility, remain visibly separate and unchanged.

The candidate deliverables remain interpretation even when marked `source_explicit`; their exact
accepted work support is displayed directly below each label. No candidate prose replaced factual
action wording.

Disposition for this bounded gate:

```text
t4qV theme usefulness:                    PASS
t4qV exact accepted-work presentation:    PASS
t4qV fact/interpretation separation:       PASS
```

## 3. `tmBK` deterministic limited-work verification — PASSED

Command:

```bash
.venv/bin/python -m jobhunter.work_intelligence_cli generate tmBK
```

Result and stored payload:

```text
outcome:             completed
artifact:            13
P1.6 dependency:     39
model:               jobhunter-deterministic-limited-work-v2
prompt/runtime:      job-work-intelligence-v2.0
schema:              job-work-intelligence-v2
evidence status:     limited
work themes:         0
deliverables:        0
role interpretation: none
model call:          none
```

The stored request uses `mode=deterministic-limited-work-boundary`; the stored response is
`deterministic=true` with reason `no_direct_work_evidence`.

The only result content is the explicit limitation:

```text
The accepted job analysis contains no direct responsibility or role-purpose evidence,
so JobHunter will not invent duties from qualifications alone.
```

Disposition:

```text
tmBK deterministic limited result: PASS
tmBK zero invented duties:         PASS
```

## 4. Unchanged v2 reuse verification — PASSED

Command:

```bash
.venv/bin/python -m jobhunter.work_intelligence_cli generate t4qV
```

Result:

```text
outcome:                 reused
returned artifact:       12
current v2 artifact rows: 1
completed attempt:       18 → artifact 12
reuse attempt:           20 → artifact 12
new model generation:    none
duplicate artifact:      none
```

The reused CLI rendering retained the same three themes, exact accepted P1.6 work, candidate
deliverables, and candidate role interpretation.

Disposition:

```text
unchanged v2 idempotent reuse: PASS
```

## 5. Browser authority/usability inspection — PASSED

The local app was run with the real settings/database and both artifact pages returned `200` with
the expected restrictive Content Security Policy.

The Windows Computer Use bridge could not initialize directly from the WSL-backed checkout because
its sandbox CWD was not a local Windows file URI. The bundled desktop Playwright runtime and the
preinstalled Microsoft Edge browser were then used without installing or modifying software.
Full-page renders were inspected at a 1440-pixel viewport.

`t4qV` visual result:

- the page leads with the candidate/sufficient state and a one-sentence authority explanation;
- each card labels `JobHunter candidate theme`, then displays `Accepted P1.6 work` prominently at
  the point of evaluation;
- optional `JobHunter interpretation` follows the exact accepted work instead of replacing it;
- all three themes and all 10 accepted responsibilities are readable, including the long technical
  documentation statement;
- candidate deliverables and the candidate role interpretation have distinct candidate badges and
  exact accepted-work support;
- artifact/P1.6/model/prompt/schema identity remains visible;
- the final authority panel explicitly contrasts `Accepted P1.6 facts` with
  `JobHunter interpretation`.

`tmBK` visual result:

- the page shows `candidate · limited` and `limited` status prominently;
- `Unknown / limited` contains the explicit no-invented-duty explanation;
- no theme, deliverable, or role-interpretation card is rendered;
- the same authority panel remains visible.

No generation button was clicked. Browser GET inspection created no artifact or attempt record and
did not change `corpus/`.

Disposition:

```text
browser fact/interpretation distinction: PASS
browser direct-work comprehension:       PASS
browser limited-work behavior:            PASS
browser publication boundary:             PASS
```

## 6. CLI same-semantics inspection — PASSED

Commands:

```bash
.venv/bin/python -m jobhunter.work_intelligence_cli show t4qV
.venv/bin/python -m jobhunter.work_intelligence_cli show tmBK
```

The CLI read artifacts 12/13 without regeneration. For `t4qV` it uses the same hierarchy:

```text
JobHunter candidate theme
→ Accepted P1.6 work
→ optional JobHunter interpretation
```

All candidate theme labels, exact accepted work, rationales, and the candidate role label were
present in both the CLI output and live browser page. `tmBK` showed the same sole limitation and no
fabricated semantic sections.

Disposition:

```text
browser/CLI assembled semantic parity: PASS
```

## 7. Final P2.2A acceptance decision

Acceptance question from the controlling amendment:

> Does the redesigned view materially reduce manual responsibility synthesis while making the
> exact accepted work immediately recoverable and preventing candidate prose from silently
> becoming factual action authority?

Decision:

```text
YES — P2.2A Job Work Intelligence v2 semantic/product acceptance PASSED.
```

Evidence summary:

```text
t4qV real direct-work generation/usefulness: PASS
exact accepted-work assembly/coverage:       PASS (10/10)
tmBK deterministic limited/no fabrication:  PASS
unchanged artifact reuse:                    PASS
browser visual authority/usability:          PASS
CLI same assembled semantics:                PASS
publication boundary:                        PASS
```

P2.2A is closed on:

```text
job-work-intelligence-v2 / job-work-intelligence-v2.0
```

This decision does not promote candidate themes, deliverables, or role labels to canonical
authority. It does not close P2.2 overall.

## 8. Stop point

```text
P2.2A acceptance decision COMPLETE
→ STOP
→ P2.2B remains unstarted and requires a separate decision
```

Do not start P2.2B, Market v2, publication, taxonomy expansion, or another action-authority model
trial from this record.
