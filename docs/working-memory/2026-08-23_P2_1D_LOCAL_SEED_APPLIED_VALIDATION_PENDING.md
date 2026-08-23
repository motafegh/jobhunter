# P2.1D local seed application — final validation pending

Date: 2026-08-23
Status: **MACHINE-LOCAL SEED APPLIED / FINAL VALIDATION PENDING**

## 1. Scope

This record follows:

- `docs/working-memory/2026-08-23_P2_1D_SMALL_SEED_REVIEW_CANDIDATE.md`;
- `docs/working-memory/2026-08-23_P2_1D_APPROVAL_REMOTE_VALIDATION_LOCAL_APPLICATION_PENDING.md`.

The repository owner previously approved the exact four-concept / one-alias / six-decision P2.1D seed. This record captures user-provided terminal evidence from the owner's real local JobHunter checkout and distinguishes that evidence from repository/CI execution.

No additional mapping, ontology expansion, Market v2 work, personal intelligence, or registry publication is authorized.

## 2. Local checkout and CLI installation

User-provided terminal output shows the local checkout was on:

```text
27bc5d6dd505b4461e0ed2978562edcbe0465cec
```

The editable package was reinstalled successfully and the newly added CLI resolved to:

```text
/home/motafeq/projects/jobhunter/.venv/bin/jobhunter-registry
```

The earlier `command not found` condition was therefore an environment-installation issue, not a registry/data defect.

## 3. Pre-mutation accepted/current claim check

Before mutation, the real local CLI reported the six approved source claims as current and `pending`:

```text
tG9K artifact=36 requirement[12]
  Source: Linux

tmBK artifact=39 requirement[3]
  Source: Linux operating system

t4jp artifact=37 requirement[4]
  Source: Creativity in creating visual and video content

t4qV artifact=44 requirement[4]
  Source: CCNP Security

t4qV artifact=44 responsibility[1]
  Source: Managing next-generation firewalls

tmyX artifact=46 requirement[11]
  Source: PowerShell
```

This matches the semantically approved P2.1D candidate identities and exact accepted/current P1.6 artifact/claim coordinates.

## 4. Machine-local SQLite mutation evidence

The owner then ran the exact approved application commands against the normal local configuration/database.

User-provided output shows creation/reuse of exactly the approved identities:

```text
Reviewed concept: platform:linux [active]
Reviewed concept: tool:powershell [active]
Reviewed concept: education_credential:ccnp-security [active]
Reviewed concept: responsibility:manage-next-generation-firewalls [active]
Reviewed alias #1: Linux operating system -> platform:linux
Reviewed claim mapping #1: tG9K requirement[12] -> mapped
Reviewed claim mapping #2: tmBK requirement[3] -> mapped
Reviewed claim mapping #3: t4jp requirement[4] -> unmapped
Reviewed claim mapping #4: t4qV requirement[4] -> mapped
Reviewed claim mapping #5: t4qV responsibility[1] -> mapped
Reviewed claim mapping #6: tmyX requirement[11] -> mapped
```

Mapped targets reported by the CLI are exactly:

```text
#1 -> platform:linux
#2 -> platform:linux
#4 -> education_credential:ccnp-security
#5 -> responsibility:manage-next-generation-firewalls
#6 -> tool:powershell
```

This is user-provided execution evidence that the owner's machine-local registry was mutated. It is not a claim that the GitHub connector or remote execution environment directly accessed `data/jobhunter.sqlite3`.

## 5. Idempotency evidence

The owner reran the same eleven mutation commands and captured first/second output to separate files, followed by:

```bash
diff -u /tmp/p21d-first.txt /tmp/p21d-second.txt
```

The second run reported the same concept identities, alias row `#1`, and mapping decision rows `#1` through `#6`. The diff emitted no differences.

Therefore the real local application demonstrates:

- concept reruns reuse the reviewed concept identities;
- alias rerun reuses alias row `#1`;
- claim-decision reruns reuse immutable mapping IDs `#1`–`#6`;
- no duplicate seed identities/decisions were created by rerun.

## 6. Disposable stale-dependency regression

The owner ran:

```text
pytest -q tests/test_canonical_registry_p21d_seed.py
```

Observed result:

```text
2 passed in 2.47s
```

This is local repository execution against disposable temporary SQLite databases. The focused regression proves the approved-seed contract plus stale-dependency behavior without deliberately making a production accepted P1.6 chain stale: historical mapping rows remain preserved while stale mappings cease to count as current.

## 7. Browser startup evidence

The owner ran:

```text
jobhunter-app --no-browser
```

and the application started normally at:

```text
http://127.0.0.1:8765/
```

The provided output proves normal application startup/shutdown only. It does **not yet** provide evidence that the local `/registry`, mapped/unmapped claim views, or Linux concept detail were inspected against the mutated machine-local database.

## 8. Repository quality-gate evidence currently available

The owner ran the final command sequence:

```text
ruff check .
pytest
pytest -W error
```

The provided terminal transcript contains:

```text
All checks passed!
```

which is sufficient evidence for the Ruff command. The supplied transcript ends at that point and does not include the completion/result lines for the subsequent full `pytest` and `pytest -W error` commands.

Accordingly, this record does **not** infer or claim those two gates passed from the command invocation alone.

The GitHub commit-status query for the current repository state also exposed no usable status result, so no CI run/result is substituted for the missing local outputs.

## 9. Remaining acceptance evidence

Before P2.1D / P2.1 can close, capture only the remaining evidence:

1. CLI inspection of the four concepts, Linux alias, five mapped decisions, and one unmapped decision against the real local database;
2. browser inspection (or deterministic local HTTP assertions) proving the same machine-local current mapping state is visible through the browser review surfaces;
3. completed full `pytest` result;
4. completed `pytest -W error` result.

The disposable stale-dependency proof is already complete and should not be repeated by mutating a real accepted production chain.

## 10. Current decision

```text
human semantic approval          PASS
exact local P1.6 preflight       PASS
machine-local seed application   PASS
real-local rerun/idempotency     PASS
disposable stale-dependency      PASS
Ruff                              PASS
CLI post-application inspection  PENDING EVIDENCE
browser current-view inspection  PENDING EVIDENCE
full pytest                       PENDING EVIDENCE
warnings-as-errors pytest         PENDING EVIDENCE
registry publication              NOT AUTHORIZED
P2.1D acceptance                  OPEN
P2.1 closure                      OPEN
```

Do not broaden scope while these final evidence items are being closed.