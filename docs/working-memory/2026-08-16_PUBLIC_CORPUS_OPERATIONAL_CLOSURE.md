# Public Corpus Operational Closure

**Date:** 2026-08-16  
**Status:** ACCEPTED / OPERATIONALLY CLOSED  
**Contract:** `jobhunter-public-corpus-v1`

## Purpose

Close the repository-safe public-corpus rollout after real local SQLite backfill, deterministic verification, Git publication, remote inspection, and coverage-terminology hardening.

## Accepted architecture

```text
local SQLite
→ runtime/history authority

corpus/
→ complete current repository-safe projection of known public Jobinja state

review-snapshots/
→ small curated semantic-review evidence
```

The corpus does not replace SQLite and is not a runtime import source.

## Real local backfill result

The owner ran the exporter against the real `data/jobhunter.sqlite3` database.

Initial verified projection:

```text
Known/discovered Jobinja jobs: 344
Fetched/parsed job details:     43
English projections:            33
English P1.6:                    2
Original P1.6:                   0
Capability artifacts:           2
Per-job stage files:           381
Corpus size:                  ~3.6 MiB
```

`jobhunter-corpus verify` returned PASS for all 344 known jobs.

Interpretation is deliberately precise:

- `344` is the number of known/discovered Jobinja identities in durable state;
- `43` have a fetched and parsed current detail advertisement;
- discovery-only jobs remain valid corpus entries with `current_detail: null`;
- therefore `344 known jobs` must never be described as `344 fully fetched advertisements`.

## Public-safety audit

A repository scan over `corpus/jobs` and `corpus/manifest.json` found no exported:

- raw model response;
- model request body;
- evidence or metadata local path;
- SQLite path;
- `/home/` path;
- `/mnt/c/` path.

The only earlier `jobhunter.sqlite3` text match was explanatory text in `corpus/README.md`, not job data.

## Accepted dependency anchors

### tG9K

```text
source detail version:          40
source language:                mixed
English projection artifact:    33
English P1.6 artifact:           36
P1.6 contract:                   job-analysis-english-v20 / job-analysis-v5
Capability artifact:             11
Capability P1.6 dependency:      36
Capability translation dep:      33
Capability contract:             job-capability-intelligence-v9 / job-capability-intelligence-v5
```

### t4jp

```text
source detail version:          41
source language:                mixed
English projection artifact:    34
English P1.6 artifact:           37
P1.6 contract:                   job-analysis-english-v20 / job-analysis-v5
Capability artifact:             12
Capability P1.6 dependency:      37
Capability translation dep:      34
Capability contract:             job-capability-intelligence-v9 / job-capability-intelligence-v5
```

## Git publication and remote proof

The full corpus data was published on `main` in:

```text
15dbfa3636bbf7118de79683beec3e7ac4a6359d
data: publish complete public job corpus
```

Remote GitHub inspection confirmed:

- `corpus/manifest.json` exists and reports 344 known jobs;
- current contracts are v20/v5 P1.6 and v9/v5 Capability;
- `corpus/jobs/` contains the published per-job directories;
- `tG9K/capability.json` is artifact 11 depending on analysis 36;
- `t4jp/capability.json` is artifact 12 depending on analysis 37.

Publication CI:

```text
CI 902
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## Coverage terminology hardening

Remote inspection exposed one reporting ambiguity: the old CLI printed `Jobs: 344` and `Sources: 344`, which could be misread as 344 fully fetched detail advertisements.

The CLI was hardened to report separately:

```text
Known/discovered jobs
Fetched/parsed job details
English projections
English P1.6
Original P1.6
Capabilities
```

A dedicated regression test locks this terminology.

Hardening head:

```text
91f1d7edc1cebd2fd8c1fb01b4e2b04163807153
```

Hardening CI:

```text
CI 904
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

No corpus-data regeneration was required because this was reporting-only hardening; the existing per-job corpus schema/content remained valid.

## Final decision

The public corpus feature is **OPERATIONALLY CLOSED**.

Permanent rules:

1. SQLite remains runtime/history authority.
2. `corpus/` remains the complete current repository-safe projection of known public Jobinja state.
3. Discovery-only identities are valid corpus entries and must remain distinguishable from fetched/parsed details.
4. Mutating JobHunter workflows refresh the corpus locally after durable success.
5. Git commit/push remains explicit and never part of runtime correctness.
6. `jobhunter-corpus verify` is the deterministic DB↔corpus integrity gate.
7. Future private/personal evidence must not enter this public corpus.
8. Remote corpus inspection may now be used to choose heterogeneous validation anchors without local SQLite access.

## Next gate

Resume the already-approved heterogeneous semantic review in this order unless corpus evidence supports a better anchor:

```text
1. Python/software
2. network/security
3. operations/platform/DevOps
```

Only jobs with fetched/parsed current details are eligible as semantic-review anchors. Discovery-only entries may be used for acquisition planning, not downstream semantic acceptance.
