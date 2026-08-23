# P2.1D small reviewed seed and P2.1 final acceptance

Date: 2026-08-23
Status: **P2.1D ACCEPTED / P2.1 CLOSED**

## 1. Decision

P2.1D is accepted and the P2.1 Canonical Concept Registry increment is closed.

This acceptance is limited to the reviewed canonical-registry contract and the deliberately small real-data seed. It does **not** authorize bulk mapping, ontology expansion, Market v2, personal intelligence, or registry publication.

Contract:

```text
jobhunter-canonical-concept-registry-v1
```

## 2. Exact accepted seed

Human/semantic review approved the exact candidate documented at commit:

```text
dd762fe9f8e30e9a19df3c77c5954247bf21febe
```

Accepted canonical concepts:

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

Accepted reviewed alias:

```text
Linux operating system
→ platform:linux
provenance kind: accepted_p16_claim
provenance reference: job=tmBK;analysis_artifact=39;claim=requirement[3]
```

Accepted immutable claim decisions:

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

No additional mappings were accepted.

## 3. Machine-local SQLite evidence

The repository connection did not and could not mutate the repository owner's machine-local database directly. The owner applied the exact approved seed locally through the accepted `jobhunter-registry` CLI against the normal configured database:

```text
data/jobhunter.sqlite3
```

Before mutation, the six exact accepted/current P1.6 claims were inspected and matched the approved artifact IDs, claim kinds, indices, and source wording.

Observed local application created/reused exactly:

```text
concepts:           4
reviewed aliases:   1
claim mappings:     6
  mapped:           5
  unmapped:         1
```

The first application produced alias row `#1` and mapping rows `#1` through `#6`.

The owner reran the same four concept commands, one alias command, and six decision commands. The second run returned the same concept identities, alias row `#1`, and mapping rows `#1` through `#6`; the captured first/second command output had no diff.

Therefore real-local idempotency is accepted: rerun reused identities and immutable decisions without duplication.

## 4. CLI and browser acceptance

Real-local CLI inspection confirmed exactly:

```text
mapped=5
unmapped=1
```

with the approved concepts, source wording, canonical targets, alias provenance, and review notes.

After an earlier transient local runtime/shell episode, the owner restarted the terminal and reactivated the virtual environment. No JobHunter implementation change was made to hide or suppress browser errors.

The normal FastAPI runtime was then exercised in-process against the real configured database. Observed route status:

```text
/                                             200
/registry                                     200
/registry/claims?state=mapped                 200
/registry/claims?state=unmapped               200
/registry/concepts/platform:linux             200
```

Deterministic real-local browser assertions then passed:

```text
PASS: registry overview shows exact four concepts
PASS: browser mapped view shows exact five approved mappings
PASS: browser unmapped view shows approved creativity decision
PASS: Linux detail shows alias provenance and both current source mappings
PASS: real local browser registry acceptance
```

The earlier HTTP 500 is therefore recorded as a non-reproduced transient local runtime/environment condition, not as a demonstrated registry-state defect. It required no product-code workaround and is not used to weaken acceptance.

## 5. Stale-dependency behavior

Focused regression coverage was added in:

```text
tests/test_canonical_registry_p21d_seed.py
```

The owner ran the focused disposable test against temporary SQLite databases:

```text
2 passed in 2.47s
```

The test proves that when an accepted P1.6 dependency becomes stale:

- the historical reviewed mapping row remains preserved;
- the stale mapping no longer counts as current;
- unaffected mappings remain current;
- CLI current-claim views exclude the stale mapping;
- browser concept detail distinguishes historical from current mapping state.

No accepted production P1.6 chain was deliberately made stale for this test.

## 6. Repository quality gates

Observed/confirmed acceptance evidence:

```text
ruff check .          PASS
pytest                PASS — 510 passed in 14.89s
pytest -W error       PASS — explicitly confirmed by repository owner
```

The warnings-as-errors result is accepted from the repository owner's explicit confirmation that the already-run gate passed. No extra rerun is required merely to duplicate that evidence.

Repository-side disposable regression and local machine mutation remain distinct evidence classes:

```text
repository/disposable validation
!=
remote mutation of machine-local SQLite
```

The final decision relies on both: deterministic repository behavior plus the owner's actual local application/inspection evidence.

## 7. P2.1 acceptance criteria

```text
stable IDs/categories/aliases/mappings                 PASS
explicit unmapped state                                PASS
exact P1.6 artifact/claim provenance                   PASS
immutable review history                               PASS
stale dependencies stop counting as current            PASS
no silent model/import acceptance path                 PASS
CLI/browser share canonical-registry contract          PASS
small real-data seed human/semantic reviewed           PASS
real-local application and rerun/idempotency            PASS
real-local CLI/browser exact-state inspection           PASS
Ruff/full pytest/warnings-as-errors                    PASS
docs distinguish correspondence from employer wording  PASS
```

Therefore:

```text
P2.1A deterministic persistence   ACCEPTED
P2.1B manual CLI review           ACCEPTED
P2.1C browser review              ACCEPTED
P2.1D small reviewed seed         ACCEPTED
P2.1 overall                      CLOSED
```

## 8. Publication decision

Registry publication remains **NOT AUTHORIZED**.

Do not add canonical-registry state to `corpus/` or any other repository-safe projection merely because P2.1 is closed. A future publication path requires its own explicit privacy/source review and decision.

## 9. Scope after closure

P2.1 closure does not automatically start Market v2 or any later Phase-2 implementation.

The next action is to inspect the controlling roadmap/implementation-plan sequence and define the next bounded focused Phase-2 increment before implementation. Until that focused plan is selected and authorized:

- do not bulk-map the remaining accepted P1.6 claims;
- do not broaden the canonical ontology;
- do not publish registry state;
- do not start Market v2;
- do not add personal readiness/scoring/recommendations.

Historical P2.1 working-memory records remain preserved as evidence of the approval, local-application boundary, transient browser investigation, and final acceptance path.
