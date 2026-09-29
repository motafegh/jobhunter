# Market candidate interpretation v1

**Date:** 2026-09-29  
**Status:** Implementation complete; real-model and usefulness review pending  
**Scope:** One ephemeral candidate work/role-subfamily report over an exact immutable Market snapshot

## Decision and boundaries

The owner authorized the first report-level interpretation increment after bounded I7 closure. V1 is an on-demand analytical candidate. It does not promote responsibility concepts, establish stable archetypes, or make broad-market prevalence claims.

The report reads only core snapshot members whose exact P1.6 artifact is accepted and whose job, source-version, translation, and analysis identities match the frozen snapshot. It provides accepted P1.6 responsibilities and requirements as cited evidence. The model proposes group labels, summaries, and alternatives; application code resolves every citation and computes distinct supporting posting counts.

Browser and CLI use the same generator. The browser executes through the existing one-at-a-time `WebOperationManager`. Browser output is held only in the current process, and CLI output is printed as JSON. No report table, candidate report file, raw prompt/response, or Market state is written to the public corpus. Browser output is cleared on process restart.

Model output remains interpretive. It must cite supplied evidence. Unknown references fail structured validation. Empty groupings are allowed. A cited group may overlap another group or leave postings unclassified. The report displays exact claim text, job links, P1.6 artifact IDs, qualitative confidence, alternatives, sample limits, and the model identity. No numeric value comes from the model.

## Current snapshot input

Snapshot 15 contains ten qualified members, six core postings, and six accepted-semantic core postings. The frozen accepted P1.6 inputs are:

| Job | P1.6 artifact | Prompt identity | Duties | Requirements |
|---|---:|---|---:|---:|
| `tvMm` | 50 | `job-analysis-english-v23` | 11 | 25 |
| `t7ck` | 52 | `job-analysis-english-v23` | 0 | 18 |
| `tmvA` | 61 | `job-analysis-english-v28` | 7 | 22 |
| `tjgi` | 60 | `job-analysis-english-v23` | 9 | 25 |
| `t7Ay` | 62 | `job-analysis-english-v30` | 0 | 26 |
| `tNVe` | 56 | `job-analysis-english-v23` | 8 | 24 |

This is 35 responsibility claims and 140 requirement claims. Exact historical prompt identities remain attached. Requirements provide context; they are not relabeled as performed work. Two core postings have no extracted responsibilities, which the report must preserve as a coverage limitation.

## Implementation

- `src/jobhunter/market_candidate_report.py` builds the exact source catalog, calls local structured inference, validates citations, and derives counts.
- `src/jobhunter/market_cli.py` adds `jobhunter market candidate-report SNAPSHOT_ID [--model MODEL]`.
- `src/jobhunter/web/market_workspace.py` and `src/jobhunter/web/templates/market_snapshot.html` add on-demand generation and a report view.
- `src/jobhunter/web/templates/market_candidate_report.html` renders evidence, counts, model identity, uncertainty, and source links.

The optional CLI `--model` supports a same-snapshot model comparison, including the owner's downloaded MiMo model, without changing global configuration.

## Verification and remaining acceptance

Ruff passed for the changed Python modules. Tests were not run in this increment.

The configured model is `gemma-4-e4b-it-ud`, and the configured URL is `http://127.0.0.1:12345/v1`. On this date `/v1/models` returned connection refused at port 12345; port 1234 did not return within the short probe. No LM Studio or llama server process was visible in the Linux process table. Therefore no real report was generated, and schema compatibility, output quality, citation fidelity, rendered report, and model speed remain unverified.

Next run, once the local model server is reachable:

```bash
jobhunter market candidate-report 15
jobhunter market candidate-report 15 --model MiMo-V2.6-Distill-Qwen-9B-Q4_K_L
```

Review the two complete outputs side by side for useful work clusters, justified role hypotheses, citation support, omission/overreach, generation time, and output length. Keep results separate from P1.6 review, I7 acceptance, promoted taxonomy, and market-scale claims. Change the implementation only for an observed contract, integrity, or usefulness defect.
