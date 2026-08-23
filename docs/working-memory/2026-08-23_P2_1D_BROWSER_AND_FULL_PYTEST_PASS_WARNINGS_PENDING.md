# P2.1D browser-content and full-pytest acceptance — warnings gate pending

Date: 2026-08-23
Status: **P2.1D FINAL GATE PENDING: WARNINGS-AS-ERRORS ONLY**

## 1. Context

This record follows the approved P2.1D seed application and the temporary populated-registry browser blocker records.

No additional mappings, ontology expansion, Market v2 work, personal intelligence, or registry publication are authorized.

## 2. Browser blocker reconciliation

After restarting the local terminal and reactivating the project virtual environment, the repository owner reran the registry browser routes in-process through the normal FastAPI runtime against the real configured database:

```text
data/jobhunter.sqlite3
```

Observed status:

```text
/                                             200
/registry                                     200
/registry/claims?state=mapped                 200
/registry/claims?state=unmapped               200
/registry/concepts/platform:linux             200
```

The previously observed HTTP 500 could not be reproduced after the terminal/runtime restart. No implementation change was made to suppress or weaken browser errors. Current evidence therefore treats the earlier 500 as a transient local runtime/environment condition rather than a demonstrated registry-state defect.

## 3. Exact real-local browser content acceptance

The owner then executed deterministic TestClient assertions against the same real local configuration/database.

Observed output:

```text
PASS: registry overview shows exact four concepts
PASS: browser mapped view shows exact five approved mappings
PASS: browser unmapped view shows approved creativity decision
PASS: Linux detail shows alias provenance and both current source mappings
PASS: real local browser registry acceptance
```

This proves the real local browser surfaces expose the approved P2.1D state:

```text
concepts: 4
reviewed alias: 1
mapped decisions: 5
unmapped decisions: 1
```

including the Linux alias provenance and both current Linux source mappings.

## 4. Full pytest acceptance

The owner ran the normal full repository test suite.

Observed result:

```text
collected 510 items
510 passed in 14.89s
```

Therefore the normal full-pytest gate is PASS for this repository state.

## 5. Remaining gate

The supplied output does not include the separate result of:

```text
pytest -W error
```

Do not infer that warnings-as-errors passed from the normal pytest result.

Current acceptance matrix:

```text
human semantic approval          PASS
exact real-P1.6 preflight        PASS
machine-local seed application   PASS
real-local rerun/idempotency     PASS
CLI exact post-application state PASS
disposable stale dependency      PASS
Ruff                              PASS
real-local browser route health  PASS
real-local browser exact content PASS
full pytest                       PASS: 510/510
warnings-as-errors pytest         PENDING EVIDENCE
registry publication              NOT AUTHORIZED
P2.1D acceptance                  OPEN
P2.1 closure                      OPEN
```

## 6. Exact next step

Run only:

```bash
pytest -W error
```

If that gate passes, reconcile final P2.1D/P2.1 acceptance documentation. Do not broaden scope before closure.
