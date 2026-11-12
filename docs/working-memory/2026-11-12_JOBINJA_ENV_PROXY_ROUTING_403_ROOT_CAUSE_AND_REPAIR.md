# Jobinja HTTP 403 — Network routing root cause, repair and acceptance

**Date:** 2026-11-12
**Branch:** `fix/jobinja-env-proxy-routing-2026-11-12`
**Source:** Authorized Jobinja static/public search and job-detail pages
**Status:** Source routing repair implemented, isolated real acquisition verified. No claims about permanent availability or corpus-wide success.

## 1. Reproduced fault

The first November 12 diagnostic run sent three modest Jobinja searches (Persian AI, RAG, Python) from WSL and received HTTP 403 on all three. The product stopped correctly. The initial conclusion that Jobinja broadly blocked JobHunter was **too broad** because it did not distinguish the egress routes.

Investigation found:

- WSL exports both `HTTPS_PROXY` and `HTTP_PROXY` to `http://127.0.0.1:8080`; Jobinja was not bypassed by `NO_PROXY`.
- The Windows listener at that port belongs to **VeePNService**. There was no Linux-owned socket, but WSL can connect to that Windows-side local port.
- The Jobinja source client constructed `httpx.Client` without an explicit `trust_env` argument. HTTPX defaults to trusting proxy environment variables, so acquisition silently followed the VeePN proxy route.
- A controlled GET to the **same** `https://jobinja.ir/robots.txt` returned HTTP **403**, HTML and `server: ArvanCloud` when proxy-routed, versus HTTP **200**, normal text/plain and `server: ArvanCloud` when direct. The direct robots file did not disallow the public `/jobs` path.
- A controlled *direct* Python search with **the same declared JobHunter User-Agent and headers** returned **HTTP 200**, passed the existing HTML validation, classified as active, and yielded **20 parsed job links**.

The evidence establishes an **unintended proxy-routing problem**. It does **not** establish the specific ArvanCloud or VeePN rule responsible for denying the proxy egress address. The correct fix is to stop inheriting an unrelated system proxy by accident, not to spoof a browser or bypass a source access control.

## 2. Narrow source-client repair

- `JobinjaClient` now passes an explicit HTTPX environment-trust flag. **Default: direct HTTPS** (`use_env_proxy=False`).
- `Settings.jobinja_use_env_proxy` defaults to `false`; the same option is present in the shipped TOML. `JOBHUNTER_JOBINJA_USE_ENV_PROXY=true` opt-in is available for environments in which the proxy is both approved and necessary.
- The existing URL/redirect whitelist, honest descriptive User-Agent, delay/budget limits, HTML/challenge checks, HTTP 403 fail-closed behavior, and source evidence retention are unchanged.
- No Windows or WSL global proxy, VeePN configuration, account credentials, cookies, browser fingerprint or cloud provider was modified. The setting applies only to Jobinja acquisition; local LM Studio uses its existing independent HTTP path.
- Existing installations without the new TOML property automatically use the safe direct default. To intentionally use the environment proxy for this source, set `jobinja_use_env_proxy = true` in the chosen TOML or the corresponding environment override.

This repair is source-specific and optional. If Jobinja later denies **direct** source acquisition, stop and respect that denial; do not cycle proxies or user identities.

## 3. Real native CLI acceptance

The supported JobHunter CLI was run from an **ignored isolated working directory** with an isolated database, evidence directory and public corpus projection root, to prevent prior evaluation's `corpus/` side effect.

| Check | Outcome |
| --- | --- |
| Post-fix direct Python discovery | **1 page fetched / HTTP 200** |
| Unique and new job links stored | **20 / 20** |
| Failed search requests | **0** |
| New public job-detail probes (`tMqd`, `tu3p`) | **2 / 2 succeeded with HTTP 200** |
| Detail parse state | **parsed / parsed** |
| Search and both detail HTML content SHA-256 | **All three match immutable stored evidence** |
| Isolated SQLite integrity / foreign keys | **ok / 0 violations** |
| Root repository tracked corpus | **unchanged** |
| Main local runtime DB and accepted P1.6/Capability artifacts | **not mutated by this experiment** |

The search was a new acquisition on November 12, but an observed search result does **not** prove a vacancy was newly posted or is still open at a later time. No model analysis or semantic review of the new ads was performed as part of this connectivity repair.

The reviewable machine-readable result is `docs/working-memory/2026-11-12_jobinja_proxy_routing_repair/ACQUISITION_ROUTING_ACCEPTANCE.json`. Raw HTML, full discovery logs, isolated SQLite, generated corpus and source-specific data remain ignored under `data/local-acceptance/jobinja-proxy-fix-2026-11-12/`.

## 4. Automated regression evidence

- New settings/TOML and environment-override tests verify default off, explicit on, and correct precedence.
- Client-construction tests verify `httpx.Client(trust_env=...)` is explicit, both on and off.
- A deterministic local-loopback origin and denying-proxy test verifies the routing outcome: **default direct -> HTTP 200; explicitly enabled proxy -> classified HTTP 403 access_denied**. No external network calls occur in this regression.
- Configuration is wired through the actual Jobinja CLI factory. Both discovery and detail acquisition share the same client.

The complete local warnings-as-errors suite passed **884 tests in 47.95 seconds**, repository Ruff passed, Python dependency check reported no broken requirements, and `git diff --check` passed.

## 5. Final interpretation and next work

The prior proxy-routed **0/3** acquisition result remains a valid historical observation, but cannot be used to claim that Jobinja now denies *direct* JobHunter access. The controlled direct native run proves **20 discovered jobs and two detailed parsed jobs** using the existing supported adapter, without changing system proxy settings.

**Next substantive evaluation:** Continue the separate fresh real-job audit using the isolated 20-result cohort. Select approximately 3–5 job ads, lock the source captures, run translation/P1.6/Work/Capability under normal review gates, and independently compare source wording to extracted claims. Prior P1.6 depth/category failures from older archived cases remain separate unresolved semantic work. No promotion of candidate analyses is implied by successful acquisition.

**Source rules and user setup:** `docs/SOURCE_POLICY.md` and `docs/DEVELOPMENT_AND_LOCAL_SETUP.md` document the direct-default/explicit-proxy option and the requirement to respect actual source-side denials.
