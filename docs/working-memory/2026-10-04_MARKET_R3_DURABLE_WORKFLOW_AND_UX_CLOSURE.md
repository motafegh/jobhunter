# Market RoleFamilyIntelligenceReport R3 durable workflow and UX closure

**Date:** 2026-10-04  
**Status:** ACCEPTED / CLOSED  
**Scope:** Durable browser + CLI workflow over the accepted R2 service, including bounded Market usability redesign.  
**Controlling plan:** `docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`

## 1. Why R3 included UX work

Owner feedback during R3 was explicit: the existing browser UI required trial-and-error to find the desired workflow and the presentation of Market intelligence was not good enough.

That is a product defect, not cosmetic polish. R3 therefore had two coupled goals:

1. expose durable role-family report state consistently through browser and CLI;
2. make the normal Market journey obvious without removing advanced controls or evidence depth.

The server-rendered FastAPI/Jinja architecture remains unchanged. No SPA/front-end framework was introduced.

## 2. Durable browser workflow

The old in-process candidate-report cache is removed.

Browser authority now comes from `MarketRoleFamilyReportService` and local SQLite:

```text
snapshot
→ durable report history
→ ordinary generate/reuse OR explicit regenerate
→ report detail by durable artifact ID
→ append-only owner review
```

Routes:

```text
GET  /market/snapshots/{snapshot_id}
GET  /market/reports/{report_id}
GET  /market/snapshots/{snapshot_id}/candidate-report   compatibility redirect
POST /market/actions/snapshots/{snapshot_id}/candidate-report
POST /market/actions/reports/{report_id}/review
```

The snapshot page shows report history and effective accepted report state. Report detail survives app restart because it is read from persisted state rather than process memory.

## 3. Durable CLI workflow

The historical `candidate-report` command now generates/reuses a durable report instead of producing browser/CLI-only ephemeral state. `--regenerate` explicitly bypasses reuse.

A primary durable command family is also available:

```text
jobhunter market role-report list <snapshot_id>
jobhunter market role-report generate <snapshot_id> [--model ...] [--regenerate]
jobhunter market role-report show <report_id>
jobhunter market role-report review <report_id> --disposition accepted_for_bounded_use|rejected [--note ...]
```

Normal CLI output exposes durable metadata, normalized report payload, and effective review state. Private request/raw-model-response audit payloads are not included.

## 4. Market usability redesign

### Market workspace

The page now presents a four-step journey:

```text
1 Choose target
2 Define scope
3 Refresh evidence
4 Read intelligence
```

The current/next action is visually primary. Advanced target-definition fields, run budgets, history, memberships, and acquisition details remain available through progressive disclosure rather than competing with the normal workflow.

Creating a new definition version is pre-filled from the selected definition so collapsing complexity does not silently change definition semantics.

### Snapshot

Snapshot is now the intelligence decision hub:

- accepted-semantic/core denominators remain prominent;
- durable role-family report status/action is primary;
- exact reuse and explicit fresh regeneration are visibly distinct;
- durable report history is directly accessible;
- requirements and responsibilities are presented as readable intelligence sections;
- raw/frozen authority details remain inspectable one level deeper.

### Role-family report

The report now leads with:

- effective review state;
- generated time/model/snapshot;
- evidence-use metrics;
- executive observations;
- work clusters;
- possible multi-posting role subfamilies;
- singleton specialty/outlier signals;
- limitations/integrity status.

Exact cited P1.6 evidence remains available under each interpretation. Review actions are explicit and append-only. Provenance/fingerprints are retained in a dedicated section. Private request/raw response remain hidden from ordinary UI.

## 5. Compatibility and integrity

The existing direct V6 generator contract remains unchanged.

The historical snapshot candidate-report URL redirects to the newest durable artifact when one exists.

Stable frozen evidence wording used by existing acceptance tests was preserved in the redesigned snapshot view.

No R3 code:

- promotes role taxonomy;
- changes P1.6 authority;
- publishes Market reports to the public corpus;
- adds live-model CI requirements;
- exposes private raw inference payloads.

## 6. Acceptance evidence

Main R3 implementation:

`107b0eedf88860b13f29cb06bd3cf14e508392ad`

Follow-up compatibility/test repairs:

```text
8930032d  preserve frozen evidence wording
d7f517c0  correct durable browser fixture scope
f3e5b8f1  update Market web tests for guided R3 workflow
```

Final CI:

`37223301900`

```text
Ruff                     PASS
pytest                   830 passed
pytest -W error          830 passed
```

Deterministic acceptance proves:

- browser-generated report persists in SQLite;
- ordinary second generation reuses the exact artifact and does not call generation again;
- browser and CLI see the same durable report ID;
- CLI show excludes private request/raw response;
- CLI review changes the same append-only effective review state rendered by browser;
- a fresh app instance reads the same report after restart;
- new durable report/review routes are registered;
- existing frozen snapshot evidence remains visible;
- guided Market workspace renders from persisted target/definition state.

## 7. R3 disposition

```text
R3 durable browser/CLI workflow     ACCEPTED / CLOSED
Market guided UX redesign           ACCEPTED for current Market scope
R4 bounded real-local acceptance    NEXT / AUTHORIZED
taxonomy promotion                  NOT AUTHORIZED
```

The UX is not declared globally finished. The accepted R3 change establishes the product direction: default screens optimize for user journey and decision relevance; advanced mechanics and provenance remain available through progressive disclosure.

R4 must now validate the durable workflow with the real snapshot-15/local-LM setup, including persistence across app restart, browser/CLI agreement, owner review, SQLite integrity, and unchanged public-corpus state.
