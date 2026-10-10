# Market RoleFamilyIntelligenceReport R4 final local acceptance

**Date:** 2026-10-10  
**Status:** PASS / ACCEPTED / CLOSED  
**Scope:** Final real-local acceptance of the durable `RoleFamilyIntelligenceReport` persistence program (R1-R4).  
**Controlling plan:** `docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`

## 1. Final disposition

```text
RoleFamilyIntelligenceReport R1 persistence        ACCEPTED / CLOSED
RoleFamilyIntelligenceReport R2 shared service     ACCEPTED / CLOSED
RoleFamilyIntelligenceReport R3 browser/CLI + UX   ACCEPTED / CLOSED
RoleFamilyIntelligenceReport R4 real acceptance    PASS / CLOSED

Persistence program                                ACCEPTED / CLOSED
Candidate generator v6                             ACCEPTED FOR BOUNDED REPORTING
Canonical taxonomy promotion                       NOT AUTHORIZED
```

The durable analytical report is now accepted as a local, immutable, evidence-linked, reviewable Market artifact. A reviewed report remains analytical interpretation rather than employer fact, canonical taxonomy, or broad-market prevalence.

## 2. Real-local baseline

The maintainer machine was synchronized to the accepted R3/R4 code and the existing local SQLite database was backed up before R4 actions:

`data/local-acceptance/role-family-r4/pre-r4.sqlite3`

The working tree already contained three unrelated/pre-existing `corpus/` changes before R4:

```text
 M corpus/jobs/tNpG/source.json
 M corpus/manifest.json
?? corpus/jobs/tNpG/english-projection.json
```

They were not reset or attributed to R4. Their exact pre-R4 SHA-256 hashes were recorded:

```text
5290e82e2e511b056111167fc97e66bbc1d1f9fa01f2f0758e9357b499eac29e  corpus/jobs/tNpG/source.json
7a65485c813a855d144160f1009559decaf0383dba06a089760d2101726fda4a  corpus/manifest.json
ec1e333a3c11bf926abd1751fc0c422329bd8d5e6db89d09c3d9bab3340cb03b  corpus/jobs/tNpG/english-projection.json
```

Initial database checks:

```text
PRAGMA integrity_check       ok
PRAGMA foreign_key_check     []
role-family reports          0
role-family attempts         0
role-family reviews          0
```

Snapshot 15 remained the expected frozen Market input:

```text
snapshot members             10
accepted-semantic members     6
core postings                 6
```

Exact accepted-semantic member analysis identities remained:

```text
tvMm  analysis 50
t7ck  analysis 52
tmvA  analysis 61
tjgi  analysis 60
t7Ay  analysis 62
tNVe  analysis 56
```

## 3. Real local inference environment

Configured maintainer endpoint:

`http://127.0.0.1:18080/v1`

Configured analysis/report model:

`gemma-4-e4b-it-ud`

The model was present in the real LM Studio model inventory.

## 4. First real durable artifact and R4 repair discovery

The first real durable report was persisted as artifact `#1`.

It proved the end-to-end generation/persistence path, but audit evidence exposed an incomplete generation identity:

```text
persisted initial max_tokens       2048
successful persisted LM request   8192
```

The difference came from the accepted inference provider's truncation recovery. The initial request starts at 2048 tokens and may retry at four times the budget. The durable fingerprint had not described that recovery policy.

Artifact `#1` was intentionally preserved immutable and remained `pending` rather than being deleted or accepted.

The repair is recorded in:

`docs/working-memory/2026-10-10_MARKET_R4_RECOVERY_IDENTITY_REPAIR.md`

Repair commits:

```text
5289d4cb  Record role-family recovery policy in generation identity
32f952a3  Cover durable role-family recovery identity
09d1249c  Record R4 generation identity repair
```

CI for the repaired head (`38068073900`) passed:

```text
Ruff                     PASS
pytest                   830 passed
pytest -W error          830 passed
```

## 5. Accepted repaired real artifact

After pulling/restarting on the repaired code, ordinary generate/reuse correctly refused to reuse the old incomplete identity and persisted artifact `#2`.

Accepted artifact identity:

```text
report id                  2
snapshot                   15
model                      gemma-4-e4b-it-ud
candidate contract         market-role-family-candidate-v6
report SHA-256             b6331a227c95de27954ca3e9f3298c69c0dd5372eb1bddffa73e9b0ec51e6d7b
generation fingerprint     963e6d18cfb8d68ec3c735f66c3fb494b0c199efaa894dc6962e55a84b496d1e
```

Persisted generation policy:

```text
initial max_tokens                  2048
truncation recovery multiplier         4
maximum recovery tokens            32768
successful request max_tokens       8192
```

The actual successful 8192-token request is therefore explicitly covered by the persisted generation policy rather than being an unexplained identity mismatch.

Application-authored durable authority wording is:

> Bounded analytical candidate based on accepted P1.6 in this frozen snapshot. Not employer wording, a promoted taxonomy, or broad-market prevalence.

## 6. Accepted report result

Artifact `#2` contained:

```text
accepted-semantic source postings     6
available P1.6 claims                175
unique cited claims                   27
work clusters                          4
possible multi-posting subfamilies     1
single-posting specialties/outliers    2
integrity rejections                    0
```

The difference from the earlier V6 review run's exact model-authored grouping/counts is acceptable for a reviewed interpretive artifact and is precisely why this layer is not canonical taxonomy authority.

## 7. Durability and cross-surface proof

The JobHunter app was stopped and restarted after artifact `#2` was persisted. The same durable report remained available from the new process.

Browser and CLI resolved the same persisted artifact and effective review state. Private request/raw-response audit payloads remained outside ordinary browser/CLI presentation.

## 8. Exact reuse proof

After the repair and restart, the ordinary generate/reuse path was invoked again.

Final durable attempt history:

```text
(1, completed, artifact 1)
(2, completed, artifact 2)
(3, reused,    artifact 2)
```

Final report count remained:

```text
reports = 2
```

No artifact `#3` was created. This proves the repaired generation fingerprint now drives exact reuse and avoids unnecessary inference.

## 9. Owner review proof

The owner accepted artifact `#2` for bounded analytical use.

Final effective review state:

```text
artifact #2   accepted_for_bounded_use
artifact #1   pending
```

Persisted append-only review history:

```text
(1, artifact 2, accepted_for_bounded_use)
```

The accepted review does not promote any generated work-cluster, specialty, or subfamily label into canonical taxonomy.

## 10. Final integrity / non-mutation proof

Post-R4 database checks:

```text
PRAGMA integrity_check       ok
PRAGMA foreign_key_check     []
reports                      2
```

Snapshot authority remained:

```text
snapshot id                  15
snapshot members             10
accepted-semantic members     6
```

The three pre-existing local corpus files were re-hashed after R4 and remained byte-identical to the pre-R4 baseline:

```text
5290e82e2e511b056111167fc97e66bbc1d1f9fa01f2f0758e9357b499eac29e  corpus/jobs/tNpG/source.json
7a65485c813a855d144160f1009559decaf0383dba06a089760d2101726fda4a  corpus/manifest.json
ec1e333a3c11bf926abd1751fc0c422329bd8d5e6db89d09c3d9bab3340cb03b  corpus/jobs/tNpG/english-projection.json
```

Therefore R4 did not mutate the repository-safe public-corpus state or the pre-existing local corpus modifications.

## 11. Closure decision

R4 passes all required acceptance dimensions:

- real local V6 inference;
- immutable durable report persistence;
- complete/auditable generation identity including recovery policy;
- restart durability;
- browser/CLI agreement;
- exact reuse without another report artifact;
- append-only owner review;
- SQLite integrity/foreign-key integrity;
- frozen snapshot/P1.6 authority preserved;
- public-corpus/pre-existing corpus state unchanged.

The `RoleFamilyIntelligenceReport` persistence program is therefore **ACCEPTED / CLOSED**.

## 12. Routing after closure

Do not open R5 or another report-infrastructure increment merely because more presentation/prompt variation is possible.

The next project action is **Phase-2 semantic direction reconciliation**, using the now-accepted factual Market substrate plus reviewed bounded report evidence to decide the next focused semantic increment.

Candidate strategic directions already present in the controlling implementation plan are:

```text
P2.2  responsibilities / deliverables / role-family semantics
P2.3  corpus-scale capability requirement profiles
P2.4  Market v2 over reviewed/current canonical mappings/profiles
```

No P2.2C responsibility-family promotion, P2.2D stable archetype promotion, or P2.3 implementation is automatically authorized by this closure. The next step is to reconcile the accepted evidence, current plans, and promotion prerequisites, then explicitly choose/plan the next bounded increment.
