# P2.1B manual CLI implementation — pending validation

Date: 2026-08-23
Status: **IMPLEMENTED / NOT YET ACCEPTED**

## 1. Handoff baseline

P2.1A remains accepted. The governing next step is `docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md` section 7 and `docs/EXECUTION_TODO.md` D2: implement only the bounded human-operated CLI review surface over the accepted canonical-registry store/service.

The implementation parent was:

```text
ce49cded447295ce11ab229b3fecdd0e930173d4
feat: close phase 1 and establish P2.1 registry
```

## 2. P2.1B implementation landed

Commit:

```text
c9f6a237073f816cbc7c2e6673831d9771d1e6de
feat: add P2.1B manual registry review CLI
```

Files added/changed:

- `src/jobhunter/canonical_registry_cli.py`
- `tests/test_canonical_registry_cli.py`
- `pyproject.toml`

The new auxiliary entrypoint is:

```text
jobhunter-registry
```

Using an auxiliary CLI is deliberate. JobHunter already has bounded auxiliary CLIs such as `jobhunter-corpus`; P2.1B therefore does not need to modify the large accepted Phase-1 dispatcher merely to expose registry review operations.

## 3. Implemented manual review surface

Concept review:

```text
jobhunter-registry concepts list
jobhunter-registry concepts show <concept-id>
jobhunter-registry concepts add <concept-id> --category <category> --label <label> --reason <note>
jobhunter-registry concepts deprecate <concept-id> [--successor <concept-id>] --reason <note>
```

Reviewed aliases:

```text
jobhunter-registry aliases add <concept-id> <alias> \
  --provenance <manual|accepted_p16_claim|external_standard> \
  --reference <provenance-reference> \
  --reason <note>
```

Accepted-current P1.6 review queue:

```text
jobhunter-registry claims list
jobhunter-registry claims list --job-id <job-id>
jobhunter-registry claims list --kind <requirement|responsibility>
jobhunter-registry claims list --state <all|pending|mapped|unmapped|rejected>
```

Immutable decisions:

```text
jobhunter-registry claims decide <job-id> <requirement|responsibility> <index> mapped \
  --concept <concept-id> --reason <note>

jobhunter-registry claims decide <job-id> <requirement|responsibility> <index> unmapped \
  --reason <note>

jobhunter-registry claims decide <job-id> <requirement|responsibility> <index> rejected \
  --reason <note>
```

## 4. Boundary behavior

The implementation intentionally does **not**:

- seed any canonical concept or alias;
- call an LLM/model to create or accept taxonomy state;
- expose browser mutation;
- change the accepted P2.1A SQLite schema;
- change P1.6 or Capability contracts;
- project canonical-registry state into `corpus/`;
- trigger public-corpus synchronization;
- implement Market v2, personal evidence/gap state, scoring, ranking, or applications.

Claim listing is fail-closed to the frozen current English P1.6 contract:

- configured analysis model;
- `job-analysis-english-v20` prompt contract;
- `job-analysis-v5` schema contract;
- semantic-review status `accepted`;
- current source-detail dependency;
- exact current English translation-artifact dependency.

Mapping writes continue through `CanonicalRegistryService.record_current_claim_mapping(...)`; therefore stale/pending P1.6 artifacts cannot receive a current mapping, meaningful review notes remain mandatory, mapped responsibility claims retain the responsibility-category constraint, repeated identical decisions remain idempotent, and attempts to rewrite an existing decision remain rejected.

## 5. Tests added

`tests/test_canonical_registry_cli.py` covers:

1. accepted/current claim enumeration and pending state;
2. transition to a reviewed mapped state;
3. concept creation, alias provenance, show, and deprecation workflow;
4. CLI claim queue inspection;
5. mapped decision recording;
6. immutable-decision rewrite rejection;
7. mapped decisions requiring a canonical concept.

The new Python source and test file were syntax-compiled successfully before repository publication.

## 6. Validation status

Repository CI is configured on every push to `main` to run:

```text
ruff check .
pytest
pytest -W error
```

At this checkpoint the connected GitHub interface does not expose the push-triggered Actions run/check result for the new commit. Therefore **P2.1B is not accepted yet**, and the D2 checkboxes in `docs/EXECUTION_TODO.md` intentionally remain unchecked.

Do not claim the deterministic/warning gate passed until the actual repository CI result or an equivalent complete local validation is observed.

## 7. Exact next step

1. Observe the CI result for the current `main` head (or run the repository-equivalent Ruff + full pytest + warning-as-error suite locally).
2. If any failure exists, fix it without broadening scope.
3. If all gates pass, mark D2 accepted and reconcile the controlling/current-memory documents.
4. Only after that decide the next bounded P2.1 increment; do not seed concepts or open browser mutation merely because the CLI exists.
