# P1.7 and Phase-1 Closure

**Date:** 2026-08-23
**Disposition:** ACCEPTED / PHASE 1 CLOSED
**Branch:** `main`

## Accepted implementation

P1.7 now has one neutral `Phase1Report` read model used by:

```text
jobhunter report
/report
```

It reports exact current configured dependencies, separate translation/analysis/review/
Capability queues, and immutable detail → English → P1.6 → Capability artifact IDs. Pending
P1.6 remains review work rather than analysis-ready work. `not_relevant` jobs remain excluded from
the analysis-ready queue.

Browser operation results now carry validated local links. CLI and browser complete workflows use
the same `Phase1RunService` and formatter, including requested, attempted, completed, reused,
failed, intentionally skipped, and remaining-eligible accounting.

## Dependency correctness repair

The P1.6 persistence identity previously omitted the exact English projection artifact. An
unchanged source version with a newly configured projection could therefore reuse analysis from
the older projection. The schema now preserves separately versioned English dependencies with
partial unique indexes, while original-language identity remains one artifact per source/model/
prompt/schema contract.

Exact configured translation dependency now controls P1.6 reuse/review, Capability eligibility,
Market aggregation, report counts, job detail presentation, and public-corpus downstream export.
The legacy database migration completed with an empty `PRAGMA foreign_key_check` result.

## Public-corpus reconciliation

Remote projection inspection found 13 historical `english-projection-v1` files counted as current.
Those files were removed from `corpus/`; their SQLite artifacts remain preserved as history. The
exporter now excludes historical translation contracts and all downstream artifacts that do not
match the selected current projection.

Accepted post-run corpus state:

```text
known/discovered Jobinja identities: 353
current parsed detail jobs:           43
current English projection v2:        20
accepted/current English P1.6:         5
accepted/current Capability v9:        5
```

`jobhunter-corpus verify` passes for all 353 known jobs.

## Deterministic acceptance

```text
ruff check .                 PASS
pytest -q -W error           492 passed
git diff --check             PASS
```

Two consecutive `jobhunter report` runs produced the same SHA-256:

```text
5c31765c2ab459514663e4c62a4789add50b5a3afd6106482b2b432805fc2625
```

The exact accepted chains remain:

```text
tG9K: detail 40 → English 33 → P1.6 36 → Capability 11
tmBK: detail 44 → English 38 → P1.6 39 → Capability 13
t4qV: detail 30 → English 20 → P1.6 44 → Capability 14
tmyX: detail 35 → English 24 → P1.6 46 → Capability 15
t4jp: detail 41 → English 34 → P1.6 37 → Capability 12
```

## Bounded live acceptance

Command:

```bash
jobhunter run \
  --search-limit 1 \
  --request-budget 1 \
  --missing-limit 0 \
  --refresh-limit 0 \
  --translation-limit 1 \
  --analysis-limit 1
```

Observed result: `completed_with_failures` with exit code 1.

```text
discovery:   1 requested / 1 attempted / 0 failed
             20 observed / 9 newly discovered
detail:      intentionally zero
translation: 23 eligible / 1 attempted / 0 completed / 1 failed / 23 remaining
analysis:    15 eligible / 1 attempted / 0 completed / 1 failed / 15 remaining
```

Translation job `tmNr` timed out against configured LM Studio. Analysis job `tpLF` exhausted its
one bounded validation retry because three model-produced depth signals failed the established
validator. Neither failure persisted a derived artifact. The successful discovery state remained
durable and the public corpus synchronized to 353 jobs. This is the intended accepted
partial-success behavior; it does not promote `tpLF` or reopen accepted semantic anchors.

## Phase-1 closure decision

Phase 1 is closed. Frozen Phase-2 input contracts are:

```text
parser:            jobinja-detail-v2
translation:       lm-studio-translation-v2 / english-projection-v2
English P1.6:      job-analysis-english-v20 / job-analysis-v5
Capability:        job-capability-intelligence-v9 / job-capability-intelligence-v5
Review Snapshot:   job-review-snapshot-v1
Public Corpus:     jobhunter-public-corpus-v1
```

Blueprint remains experimental, deferred, non-current, and non-authoritative. The 23 translation
repairs and 15 analysis-ready jobs are operational backlog, not Phase-1 acceptance prerequisites.
Phase 2 may now begin with a focused canonical concept registry plan; corpus-wide model generation,
personal readiness, and Blueprint promotion remain out of scope.
