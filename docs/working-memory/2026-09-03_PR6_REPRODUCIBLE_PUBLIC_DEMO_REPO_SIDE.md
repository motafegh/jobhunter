# PR6 — Reproducible Public Demo / Repository-Side Closure

**Status:** REPOSITORY-SIDE COMPLETE / REAL BROWSER SCREENSHOTS DEFERRED  
**Date:** 2026-09-03  
**Track:** Portfolio readiness / public presentation  
**Product-development authority:** unchanged; P2.2B-B1 remains locally blocked on `ta9l` P1.6 acceptance.

## 1. Scope completed

PR6 established a truthful fresh-clone demonstration path that does not require the maintainer's private/runtime SQLite database, LM Studio, or live Jobinja acquisition.

Implemented repository-side outputs:

- `docs/demo/README.md` — guided public-corpus walkthrough;
- root `README.md` link to the guided demo;
- `docs/README.md` reviewer/navigation route updated to include the demo;
- no fake demo application;
- no fabricated data;
- no automatic import of committed corpus data into runtime SQLite;
- no publication of private/local-only state.

The demo uses the existing committed `corpus/` projection and Python standard-library inspection rather than adding maintenance-only runtime code.

## 2. Selected real examples

### `t4qV` — rich responsibility evidence

Senior Network Security Engineer.

Current accepted chain:

```text
source detail version 30
→ English projection artifact 20
→ accepted English P1.6 artifact 44
→ Capability artifact 14
```

The P1.6 artifact contains 10 accepted responsibilities, including network-security architecture, NGFW management, VPN design, troubleshooting, Zero Trust/network segmentation, and technical documentation. Capability Intelligence preserves exact P1.6 dependency/source indices while organizing supported capability areas.

### `tmBK` — sparse responsibility evidence

Python Developer.

Current accepted chain:

```text
source detail version 44
→ English projection artifact 38
→ accepted English P1.6 artifact 39
→ Capability artifact 13
```

The vacancy contains substantial employer requirements but no explicit duties. Accepted P1.6 therefore retains:

```text
responsibilities: []
role_purpose: []
```

Capability may organize supported requirements, while source-responsibility references and work activities remain empty. This demonstrates the product rule that requirements do not automatically establish duties.

## 3. Demo integrity / authority boundaries

The walkthrough explicitly distinguishes:

```text
committed public corpus
≠ local SQLite runtime authority
```

It also states that:

- only current accepted English P1.6 is published into the corpus;
- Capability is published only when its exact dependencies are current;
- Job Work Intelligence v2 is not currently a public-corpus stage;
- Canonical Registry runtime state is not currently projected into the public corpus;
- personal/profile/application state is neither part of this public demo nor current public product state;
- two curated examples are engineering evidence, not market-wide model-quality proof.

## 4. Fresh-clone reviewer route

The documented path is:

```text
GitHub-only inspection
or
clone
→ Python 3.12+
→ python -m pip install -e ".[dev]"
→ jobhunter-corpus status
→ inspect t4qV and tmBK JSON chains
→ run read-only lineage assertions
```

The walkthrough provides exact expected corpus counts and artifact lineage for the current committed baseline.

## 5. Screenshot substep

Real browser screenshots remain intentionally deferred because the normal browser application operates on local SQLite state and machine-local runtime access is currently unavailable.

Do not fabricate screenshots from templates, mock state, or hand-built visualizations and present them as JobHunter runtime output.

When local runtime access returns, capture approximately 2–4 real screenshots after checking that no private/local-only information is visible. Good candidates are:

1. dashboard/overview;
2. a representative accepted job detail such as `t4qV`;
3. the corresponding Capability Intelligence page;
4. optionally a safe current Registry or Work Intelligence view if it improves the public story.

Only after that substep should PR6 be described as visually complete.

## 6. CI dependency drift discovered during PR6

The documentation commit exposed a fresh-environment dependency drift in CI rather than a JobHunter logic regression.

Run 1075:

```text
ruff check .        PASS
pytest              PASS — 540 tests
pytest -W error     FAIL during collection
```

Cause:

- the fresh resolver selected AnyIO 4.15;
- Starlette TestClient still referenced the deprecated `anyio.abc.BlockingPortal` alias;
- the repository's deliberate warnings-as-errors gate correctly surfaced the third-party compatibility issue.

Response:

- warnings-as-errors was NOT weakened;
- no broad warning ignore was added;
- `pyproject.toml` received a dev-only `anyio>=4,<4.15` compatibility cap until the Starlette/TestClient boundary is compatible;
- runtime semantic contracts and application behavior were unchanged.

Commit:

`4d230f8331d2cbc5fd999ed6136016271658f6ba — build: stabilize strict web test dependency`

CI run 1076 then passed all gates:

```text
ruff check .        PASS
pytest              PASS
pytest -W error     PASS
```

The cap should be revisited in normal dependency-hygiene work (PR8 or later) after upstream compatibility changes; it is not intended as a permanent arbitrary pin.

## 7. PR6 disposition

```text
ADD       reproducible evidence-first demo walkthrough
POLISH    README/docs discoverability
KEEP      public-corpus/runtime authority separation
KEEP      strict warnings-as-errors quality gate
DEFER     real browser screenshots until local runtime is available
SKIP      demo-specific runtime/helper code because existing corpus/CLI is sufficient
```

PR6 repository-side acceptance is complete. The visual screenshot substep remains a recorded local-runtime follow-up and must not block PR7 repository-side onboarding work.

## 8. Next portfolio phase

Proceed to PR7 — installation/developer onboarding.

PR7 should verify and document the fresh-clone developer path, configuration boundaries, browser/CLI entrypoints, optional LM Studio/live acquisition requirements, quality commands, and expected local-only files without adding unnecessary task runners or ceremonial contribution files.
