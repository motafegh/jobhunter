# P2.3A /compare — Compact overview refinement and comparative browser result

**Date:** 2026-11-11
**Status:** Experimental candidate, engineering verified in scope; owner repeated-use acceptance still pending
**Branch:** `experiment/p23a-compare-at-glance-2026-11-11`
**Predecessors:** `2026-11-11_P23A_COMPARISON_FIRST_VIEW_PREDECISION.md`, `2026-11-11_P23A_AT_A_GLANCE_EXPERIMENT_RESULT.md`

## Why refine the initial experiment?

The first read-only overview made exact requirement-vs-duty facts visible earlier, but moved the existing job selectors and evidence far down the page. On 390px mobile, the three-job RAG case moved first detail claim from 1,411px in the accepted baseline to 2,233px in the first prototype. This is an observed interaction cost independent of whether the summary is useful.

## Bounded modification

- Keep the factual at-a-glance overview in place, with all original per-job evidence available and linked.
- Wrap the job/wording selection form in a native accessible `details` element. The form is **open by default when no jobs are selected**, and **collapsed when a comparison is already selected**.
- Clearly label the disclosure "Change selected jobs or wording" on comparison pages and "Choose jobs and wording" before selection. The selected literal filter is displayed in the disclosure label.
- Tighten only mobile overview spacing. Do not remove explicit counts, unknown-state text, source links, or original wording.
- No added model inference, Registry mapping, SQLite schema, persistence, source acquisition, or third-party browser dependency in product code.

The editing tradeoff is explicit: changing a pre-existing comparison now requires **one disclosure click**. A first-time visitor sees all controls immediately, without that extra click.

## Comparative geometry — same machine, same RAG three-job scenario

Chromium/Playwright rendered the original and both experimental revisions using isolated SQLite backups, loopback-only server ports, a 1440×900 desktop viewport, and a 390×844 mobile viewport. Values are approximate document-Y geometry (pixels), not time/user-experience measurements.

| Measurement | Accepted baseline | First experimental overview | Refined overview |
| --- | ---: | ---: | ---: |
| Desktop first claim Y | 822 | 1,166 | **913** |
| Desktop document height | 1,851 | 2,195 | **1,942** |
| Mobile first claim Y | 1,411 | 2,233 | **1,554** |
| Mobile document height | 4,740 | 5,562 | **4,883** |
| Mobile overview first job Y | N/A | 557 | **551** |
| Mobile editing controls default | Always visible | Always visible below overview | Collapsed after comparison; open before selection |

Refinement recovers **679px** of the original prototype's mobile first-claim displacement and **253px** on desktop. Compared with accepted baseline it still displaces first claims by **143px** mobile and **91px** desktop, while providing earlier summary of requirements/duties.

This is a structural tradeoff, not proof of a net speed or comprehension gain.

## Technical and security checks

Four scenarios (RAG, Python with optional existing job-local Capability groups, requirement-only, and literal no-match) were exercised at both viewport sizes. All rendered HTTP 200 with unchanged exact matching-claim and direct-duty counts. Source evidence expansion and drill-down worked; browser Back returned to the selected wording. Summary anchor links scrolled to the correct source job card. The selection editor could be opened on both widths, and retained the selected filter. No horizontal overflow, JavaScript errors, or off-origin requests were observed in these checks.

A supplementary mobile Chromium interaction changed the filter from RAG to Python via the reopened editor; the page retained all three selected public job IDs, recomputed the overview, and collapsed the editor again after submission. The no-selected-jobs page was checked separately: its editor is open on initial load. Additional regression assertions verify this default, collapsed selected-state, query HTML escaping, distinct counts, direct-duty boundary, and that repeated GETs do not mutate persistent domain data.

**Final local engineering gates:** 879 tests passed with strict warnings-as-errors in 47.94 seconds; repository Ruff check passed; dependency consistency check reported no broken requirements; `git diff --check` passed. All checks were executed on the refined experimental branch.

## Disposition and next decision

**Keep this refined version as a candidate on the experimental branch.** It resolves most of the previously measured layout regression without changing accepted factual semantics, but makes repeated editing a click more expensive. Neither original nor experimental UX is yet validated through an owner's genuine comparison task, and no durable product acceptance is claimed.

The next owner trial should compare original and refined interfaces for the same RAG/Python questions, checking whether the new summary shortens evidence-oriented decisions despite the editor being one click away. Do not merge to `main`, approve P2.3 persistent profiles, or assert time savings from viewport geometry alone.

Ignored `data/local-acceptance/` contains temporary visual scripts/screenshots for maintainer inspection. It is deliberately not published; no local/private SQLite, source text, or secrets were committed.
