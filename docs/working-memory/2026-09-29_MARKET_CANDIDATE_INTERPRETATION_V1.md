# Market candidate interpretation v1

**Date:** 2026-09-29  
**Status:** V3 owner usefulness review complete; V3.1 integrity repair implemented as candidate v4/prompt v4 with green regression gates; fresh snapshot-15 real-model/browser rerun pending
**Scope:** One ephemeral candidate work/role-subfamily report over an exact immutable Market snapshot

## Decision and boundaries

The owner authorized the first report-level interpretation increment after bounded I7 closure. V1 is an on-demand analytical candidate. It does not promote responsibility concepts, establish stable archetypes, or make broad-market prevalence claims.

The report reads only core snapshot members whose exact P1.6 artifact is accepted and whose job, source-version, translation, and analysis identities match the frozen snapshot. It provides accepted P1.6 responsibilities and requirements as cited evidence. In current v4, the model proposes group labels plus evidence-bound interpretation points and evidence-bound alternatives; application code resolves citations and owns distinct supporting-posting counts, evidence counts, confidence caps, and support-basis classification.

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

At the first check, tracked `jobhunter.toml` pointed to stale port 12345. The owner clarified that LM Studio listens on custom port `18080`; the tracked maintainer config and current handoff now record `http://127.0.0.1:18080/v1`. The fresh-clone default in `Settings` remains `1234`. `/v1/models` was reachable and returned both model IDs.

The first full claim payload contained 21,595 tokens and failed against the loaded 4K context. V2 compacted model-facing claim rows and uses the existing 16K LM Studio context manager. Structured inference then completed successfully. The first Gemma run took 1:14; after contract/presentation refinements, the final recorded Gemma v2 run took 1:28.98.

The same v2 request with `mimo-v2.6-distill-qwen-9b` completed in 8:45.36. MiMo produced seven work clusters and five role candidates, including a distinct speech/audio engineering posting that Gemma did not surface because that posting had no responsibility claims. MiMo also speculated that a PyTorch qualification might be a copied claim and incorrectly said tools/counts were unavailable. Those defects are visible in the model caveats/limitations and prevent treating its output as accepted. Its response is a promising richer candidate but is about six times slower than Gemma on this call.

Gemma produced five work clusters and four possible subfamilies in v2. Its output was more conservative, but its initial wording said "high demand" for a six-posting sample and it did not propose the speech/audio specialty from requirements. V3 keeps counts scoped to snapshot coverage, lowers confidence for one-posting groups, and resolves model source aliases throughout report prose. The final v3 browser generation completed for snapshot 15; the route returned HTTP 200, rendered exact accepted P1.6 evidence citations, and displayed `t7ck` instead of the model's internal `J2` alias. These outputs are candidate evidence only; neither model is promoted, and no broad-market claim is accepted.

The complete CLI outputs are under `/tmp/jobhunter-market-candidate-gemma-snapshot15-v2.json` and `/tmp/jobhunter-market-candidate-mimo-snapshot15.json`; they are private transient machine files and are not repository artifacts. The v3 browser report is available at `/market/snapshots/15/candidate-report` while the local app process remains running.

The next step is owner review of usefulness and limitations. Keep results separate from P1.6 review, I7 acceptance, promoted taxonomy, and market-scale claims. Change the implementation only for an observed contract, integrity, or usefulness defect.

For a repeat run:

```bash
jobhunter market candidate-report 15
jobhunter market candidate-report 15 --model MiMo-V2.6-Distill-Qwen-9B-Q4_K_L
```

Review the complete outputs under `/tmp/jobhunter-market-candidate-gemma-snapshot15-v2.json` and `/tmp/jobhunter-market-candidate-mimo-snapshot15.json` for useful work clusters, justified role hypotheses, citation support, omission/overreach, generation time, and output length. They are private transient machine files and are not repository artifacts. Restart the browser app to load the pushed route before checking the rendered view. Keep results separate from P1.6 review, I7 acceptance, promoted taxonomy, and market-scale claims. Change the implementation only for an observed contract, integrity, or usefulness defect.


## Regression hardening — 2026-09-29

Dedicated coverage now exists in `tests/test_market_candidate_report.py`.

The regression harness uses real temporary SQLite source/translation/P1.6/Market state and stubs only the local model response. It verifies:

- exact accepted snapshot/P1.6 evidence is used;
- model-facing citation enums are bounded to the supplied compact evidence catalog;
- source aliases are resolved before user presentation;
- supporting-posting counts are application-derived;
- one-posting groups are downgraded to low confidence;
- high confidence over fewer than four supporting postings is capped at moderate;
- postings without extracted responsibilities remain visible as a coverage limitation;
- report generation does not persist a report or mutate snapshot/P1.6 counts;
- a snapshot/P1.6 source-identity mismatch is rejected;
- CLI `--model` override reaches the shared generator;
- browser generation uses the operation queue and renders the stored ephemeral report;
- missing in-process browser reports return 404 rather than implying durable persistence.

CI run `36597463699` on commit `3d557130` passed Ruff, **812 tests**, and **812 warnings-as-errors tests**.

Engineering hardening is therefore complete for the current bounded v3 increment. The remaining gate is owner usefulness review and the explicit decision to keep the report ephemeral or authorize a separately versioned persisted report contract. This does not promote any role family or taxonomy.

## Owner usefulness review and V3.1 integrity repair — 2026-09-29

The owner reviewed the exact rendered v3 snapshot-15 artifact preserved in commit `c0c8998`. The product conclusion was **useful synthesis, not persistence-ready**. The work-cluster layer reduced manual reading and surfaced a meaningful Speech AI specialty from requirement evidence, but the review exposed concrete defects:

- the top support display repeated the same posting once per cited claim instead of showing distinct supporting postings;
- `175` available P1.6 claims were labeled as though all 175 were cited by the report;
- model-facing compact `C*` IDs leaked into user-facing prose;
- the overall reading could mention a source such as `t7Ay` or `t7ck` without evidence from that same source being attached to the statement;
- group prose could import a concrete detail from an uncited claim, and free-text alternatives could introduce uncited jobs;
- one-posting candidates such as Speech AI and Full-Stack AI were presented too much like reusable role subfamilies;
- the role-subfamily section often repeated work clusters rather than clearly adding a distinct multi-posting role-shape interpretation.

Decision: keep the report **ephemeral**, repair the observed integrity/usability defects once, rerun the same frozen snapshot, and only then decide whether a separately persisted report contract is warranted.

Because the response/evidence semantics changed materially, V3.1 uses new contract identities rather than silently reusing v3:

```text
report: market-role-family-candidate-v4
prompt: market-role-family-candidate-prompt-v4
```

V4 changes:

- replaces one broad overall paragraph with evidence-bound overall observations;
- replaces free summary/rationale prose with evidence-bound interpretation points;
- makes every alternative an evidence-bound object;
- fails closed if an internal compact `C*` ID leaks into user-facing prose;
- fails closed when an interpretation mentions a source alias without citing evidence from that source;
- withholds employer names and job titles from the model-facing input so source-specific interpretation must come from accepted claims;
- computes distinct overall support, available-vs-cited evidence counts, and responsibility/requirement support basis in application code;
- marks requirement-only groups explicitly as specialty/qualification signals rather than inferred duties;
- keeps one-posting work patterns low-confidence and routes one-posting role candidates to a specialty/outlier section instead of the multi-posting role-subfamily section;
- instructs role-subfamily generation to require at least two postings and add a role-shape distinction rather than merely rename a work cluster.

Regression coverage now also proves compact-ID rejection, same-source evidence binding for source mentions, evidence-bound alternatives, available-vs-cited counts, responsibility-vs-requirement support basis, and singleton specialty routing. Final CI run `36611296932` passed Ruff, **814 tests**, and **814 warnings-as-errors tests** on commit `76e8e320`.

The remaining acceptance action is intentionally local and bounded: pull/restart the maintainer app, regenerate snapshot 15 once with the default Gemma analysis model, capture the rendered v4 artifact, and compare it directly against the defects above. No report persistence, role-family promotion, or broader taxonomy work is authorized before that review.
