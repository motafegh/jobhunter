# P2.1D populated registry browser 500 blocker

Date: 2026-08-23
Status: **ACTIVE P2.1D BLOCKER / ROOT CAUSE NOT YET ESTABLISHED**

## 1. Context

This record follows:

- `docs/working-memory/2026-08-23_P2_1D_SMALL_SEED_REVIEW_CANDIDATE.md`;
- `docs/working-memory/2026-08-23_P2_1D_APPROVAL_REMOTE_VALIDATION_LOCAL_APPLICATION_PENDING.md`;
- `docs/working-memory/2026-08-23_P2_1D_LOCAL_SEED_APPLIED_VALIDATION_PENDING.md`.

The exact approved P2.1D seed has now been applied to the repository owner's real machine-local registry. No additional mapping, ontology expansion, Market v2 work, personal intelligence, or registry publication is authorized.

## 2. Real local registry state confirmed

User-provided CLI evidence after application confirms exactly:

```text
concepts: 4
reviewed aliases: 1
mapped claim decisions: 5
unmapped claim decisions: 1
```

The four concepts and Linux alias show the approved review notes and exact alias provenance:

```text
platform:linux
  Linux operating system
  accepted_p16_claim: job=tmBK;analysis_artifact=39;claim=requirement[3]

tool:powershell
education_credential:ccnp-security
responsibility:manage-next-generation-firewalls
```

The current mapped CLI view reports exactly:

```text
tG9K artifact 36 requirement[12] -> platform:linux
tmBK artifact 39 requirement[3] -> platform:linux
t4qV artifact 44 requirement[4] -> education_credential:ccnp-security
t4qV artifact 44 responsibility[1] -> responsibility:manage-next-generation-firewalls
tmyX artifact 46 requirement[11] -> tool:powershell
```

The current unmapped CLI view reports exactly:

```text
t4jp artifact 37 requirement[4]
Creativity in creating visual and video content
```

Observed CLI counts:

```text
mapped=5
unmapped=1
```

Therefore the machine-local seed application itself is not the blocker.

## 3. Browser failure discovered during acceptance

The local deterministic browser-check command started `jobhunter-app --no-browser` in the background and used `/registry` as its readiness probe.

Observed result:

```text
curl: (22) The requested URL returned error: 500
```

This repeated for the readiness attempts until the owner interrupted the command.

At this point the evidence proves only that the populated local `/registry` overview returns HTTP 500. It does **not** yet establish whether `/registry/claims?state=mapped`, `/registry/claims?state=unmapped`, or `/registry/concepts/platform:linux` fail independently, because execution never advanced past the readiness loop.

## 4. Test-gap observation

The focused disposable P2.1D regression currently verifies populated browser visibility through:

```text
/registry/claims?state=mapped
/registry/claims?state=unmapped
/registry/concepts/platform:linux
```

but does not request the populated `/registry` overview after applying the seed.

Earlier P2.1C coverage verifies the `/registry` overview in its empty state. The newly observed production-data failure therefore exposes a real acceptance/test coverage gap: populated-overview behavior is not presently proved by the focused disposable seed test.

This observation does not yet identify the implementation root cause.

## 5. Required next evidence

Before changing implementation, capture the application traceback from the failed background run:

```text
/tmp/p21d-app.log
```

The traceback must be used to distinguish among:

- populated overview template/rendering failure;
- registry-store/listing failure;
- current-claim count/read failure specific to the real accepted corpus;
- configuration/runtime integration failure;
- another concrete exception.

Do not weaken browser acceptance or suppress the exception merely to make the probe green.

## 6. Acceptance impact

Current status:

```text
human semantic approval          PASS
machine-local seed application   PASS
real-local rerun/idempotency     PASS
disposable stale-dependency      PASS
CLI post-application inspection  PASS
browser populated overview       BLOCKED: HTTP 500
browser exact mapping views      NOT YET EXECUTED IN THIS ATTEMPT
full pytest                       still pending from prior evidence boundary
warnings-as-errors pytest         still pending from prior evidence boundary
registry publication              NOT AUTHORIZED
P2.1D acceptance                  OPEN
P2.1 closure                      OPEN
```

P2.1D must remain open until the browser defect is explained/fixed with regression coverage and the remaining validation gates pass.
