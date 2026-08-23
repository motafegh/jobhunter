# P2.1D approved seed — remote validation / local application boundary

Date: 2026-08-23
Status: **APPROVED / REPOSITORY REGRESSION ADDED / MACHINE-LOCAL APPLICATION PENDING**

## 1. Human semantic approval

The repository owner explicitly approved the exact six-decision P2.1D seed documented in:

```text
docs/working-memory/2026-08-23_P2_1D_SMALL_SEED_REVIEW_CANDIDATE.md
candidate commit: dd762fe9f8e30e9a19df3c77c5954247bf21febe
```

The approved seed is fixed for this increment:

```text
canonical concepts: 4
reviewed aliases:   1
claim decisions:    6
accepted chains:    5
```

No additional mapping, ontology expansion, Market v2 work, personal intelligence, or registry publication is authorized by this approval.

## 2. Exact approved concepts

```text
platform:linux
  preferred label: Linux

tool:powershell
  preferred label: PowerShell

education_credential:ccnp-security
  preferred label: CCNP Security

responsibility:manage-next-generation-firewalls
  preferred label: Manage next-generation firewalls
```

The exact review notes remain the notes recorded in the review-candidate application commands.

## 3. Exact approved alias

```text
Linux operating system
→ platform:linux

provenance kind: accepted_p16_claim
provenance reference: job=tmBK;analysis_artifact=39;claim=requirement[3]
```

The exact alias review note remains the note recorded in the review-candidate application command.

## 4. Exact approved claim decisions

```text
tG9K artifact 36 requirement[12]
Linux
→ mapped → platform:linux

tmBK artifact 39 requirement[3]
Linux operating system
→ mapped → platform:linux

t4jp artifact 37 requirement[4]
Creativity in creating visual and video content
→ unmapped

t4qV artifact 44 requirement[4]
CCNP Security
→ mapped → education_credential:ccnp-security

t4qV artifact 44 responsibility[1]
Managing next-generation firewalls
→ mapped → responsibility:manage-next-generation-firewalls

tmyX artifact 46 requirement[11]
PowerShell
→ mapped → tool:powershell
```

The exact review notes remain the notes recorded in the review-candidate application commands.

## 5. Repository-side disposable regression

Commit:

```text
14e65fc112cbbd030c56bbc9c24493ed0d28101f
test: verify approved P2.1D seed contract
```

adds:

```text
tests/test_canonical_registry_p21d_seed.py
```

The regression uses a disposable temporary SQLite database and the real registry CLI/service/review/browser paths. It does not read or mutate `data/jobhunter.sqlite3`.

It verifies the approved P2.1D contract shape:

1. exactly four reviewed canonical concepts are created;
2. exactly one reviewed Linux alias is stored with the approved provenance reference;
3. exactly six reviewed decisions are stored with the approved dispositions/targets;
4. rerunning every approved concept/alias/decision command reuses existing concept identities, the same alias row, and the same immutable mapping decision IDs;
5. CLI mapped/unmapped views expose the approved source wording and canonical targets;
6. browser mapped/unmapped views expose the same current reviewed state;
7. the Linux concept browser detail shows the cross-role `tG9K` + `tmBK` correspondence;
8. after a new source/translation dependency makes the disposable `tG9K` accepted P1.6 chain stale, the historical Linux mapping row remains preserved while its derived currentness becomes false;
9. the unaffected `tmBK` Linux mapping remains current;
10. the CLI no longer reports the stale `tG9K` mapping as a current accepted-P1.6 mapping;
11. the browser concept detail distinguishes the stale mapping as historical from the still-current mapping.

The disposable fixture necessarily has its own temporary artifact row IDs. The production provenance reference string for the reviewed alias is nevertheless asserted exactly as approved. Actual machine-local application must bind the six claim decisions to the real accepted artifacts 36, 37, 39, 44, and 46 through the current-claim service boundary.

## 6. Execution-environment limitation

The remote execution container cannot currently resolve `github.com`, so it cannot clone the repository or access the repository owner's machine-local database. The GitHub repository connection can update/read `main`, but it does not provide access to:

```text
data/jobhunter.sqlite3
```

Therefore this record does **not** claim that the owner's local registry has been mutated.

The push-triggered repository CI is configured to run:

```text
ruff check .
pytest
pytest -W error
```

The final P2.1 acceptance record must use observed execution results rather than infer success from the existence of the test commit.

## 7. Machine-local application still required

On the repository owner's machine, after pulling the approved repository state:

1. inspect the exact six current claims before mutation;
2. run the exact four concept commands;
3. run the exact one alias command;
4. run the exact six decision commands;
5. inspect the resulting CLI/browser state;
6. rerun the same eleven mutation commands and confirm reuse/no duplication;
7. run the standard full repository gate;
8. report the exact outputs needed to reconcile final P2.1 acceptance.

Do not deliberately stale one of the real accepted production P1.6 chains just to test currentness. The stale-dependency behavior is exercised in the disposable deterministic regression. Production history should remain untouched unless a real upstream dependency changes naturally.

## 8. Publication decision

For this P2.1D increment:

```text
registry publication: NOT AUTHORIZED
```

Do not add the local canonical-registry state to `corpus/` or any other repository projection during P2.1D.

## 9. Acceptance status

P2.1D and P2.1 remain **open** until both boundaries are reconciled:

```text
repository validation
+ machine-local approved-seed application/inspection
→ final P2.1D acceptance decision
```

A final acceptance record must explicitly distinguish:

- disposable/repository regression evidence;
- CI/local test-gate evidence;
- actual mutation and inspection of the owner's machine-local SQLite registry.
