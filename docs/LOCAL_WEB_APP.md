# JobHunter Local Web Application

## Purpose

The web application is the normal human-facing interface for repeated local use.
The command-line interface remains available for automation, debugging, tests, and
advanced workflows, but daily operation should not require memorizing CLI commands.

The browser interface is a **second interface over the same application services and
SQLite database**. It does not maintain a separate job store, parser, translation
pipeline, or hidden workflow state.

## Launch

Install/update the editable package first:

```bash
python3 -m pip install -e ".[dev]"
```

Start the local application:

```bash
jobhunter-app
```

Default address:

```text
http://127.0.0.1:8765/
```

The launcher opens the default browser automatically. Starting `jobhunter-app` again while
the same loopback instance is already running reopens that instance instead of attempting
to bind a second server to the same port.

### Linux application-menu launcher

Install once from the project/config directory:

```bash
jobhunter-app --install-desktop
```

This creates a local application entry under `~/.local/share/applications` and installs
the packaged JobHunter icon. The desktop entry stores the **exact resolved
`jobhunter.toml` path and working directory used during installation**, so application-menu
launches do not depend on the desktop environment's current directory.

Normal use can then start JobHunter from the application menu without opening a terminal.
Repeated clicks reuse/open an already-running local instance.

## Network boundary

The launcher binds to loopback by default. It refuses a non-loopback host unless the
operator explicitly supplies `--allow-network`.

This is intentional. The UI can trigger source acquisition and local-model work, so it
must not silently become a LAN service.

## Main screens

### Overview

The dashboard shows:

- unique discovered jobs;
- jobs with complete local details;
- current English-corpus coverage;
- missing details/translations;
- number of detail-fetch observations;
- recent acquisition runs;
- recent browser operations.

It also provides the primary bounded sync form and one-click parser audit, translation,
and English-corpus export actions.

#### Understanding the sync controls

The browser labels are intentionally phrased in operational language rather than internal
configuration names.

- **Search terms to try** — how many configured searches from the effective bilingual
  plan participate in this run. `12` is a quick cross-domain sample; `40` is the normal
  working default. Raising this increases coverage, not quality by itself.
- **Search-page request limit** — the hard ceiling on actual Jobinja search-page HTTP
  requests. With one page per term, it is normally equal to the search count. If lower,
  JobHunter stops safely when the budget is exhausted.
- **New jobs to fully fetch** — how many discovered jobs that do not yet have local detail
  evidence may be fetched. `5–10` is a normal bounded batch; `0` performs discovery only.
- **Old jobs to recheck** — how many previously acquired jobs may be revisited when old
  enough. `5` is conservative; `0` disables refresh work for that run.
- **Recheck after** — the minimum age of the last detail check before a job becomes
  refresh-eligible. `24` hours gives daily freshness; `72–168` reduces network work.

Missing-detail plus refresh checks may never exceed 50 in one sync.

The UI also provides three deterministic presets:

- **Light scan:** 12 searches / 12 search requests / 3 missing details / 2 refreshes;
- **Normal:** 40 / 40 / 10 / 5;
- **Thorough:** 80 / 80 / 20 / 10 with a 72-hour refresh threshold.

Presets only fill the form. The values remain visible and editable before submission.

### Jobs

The jobs table supports local filtering by:

- free-text title/company/location/Jobinja-reference search;
- detail availability;
- English projection availability;
- lifecycle state.

No network request is made when browsing/filtering the local catalog.

Opaque source job codes such as `tmW5` remain in persistence because they are the stable
Jobinja identity, but the UI labels them explicitly as **Jobinja reference** and keeps
them visually secondary to role/company information.

#### Quick Add

The Jobs screen provides a bounded **Quick Add** input for one focused intake task.
It accepts:

1. **a public Jobinja job URL** — save/update that logical posting and immediately fetch
   its complete detail page;
2. **a public Jobinja `/jobs` search URL** — preserve its Jobinja-owned filters, discover
   matching postings, and optionally fetch a bounded detail sample;
3. **a Persian or English keyword/role phrase** — build a normal Jobinja keyword search,
   discover matches, and optionally fetch a bounded detail sample.

Quick Add exposes separate bounds for search pages (`1–3`) and full detail fetches
(`0–20`). `0` detail pages means discovery-only. When translation is enabled, a checkbox
can translate only the successfully fetched jobs after acquisition.

Quick Add does not expand the source policy. Arbitrary external job websites are rejected
until a dedicated approved adapter exists for those sources.

### Job detail

One job view combines:

- original authoritative Jobinja fields;
- current English derived fields;
- source skill tags;
- complete source and English descriptions;
- parser/audit status;
- semantic/raw evidence hashes;
- source URL and evidence path;
- fetch-observation history;
- per-job source refresh and translation actions.

A posting that has only been discovered is shown as a normal **details not acquired yet**
state with a Fetch details button; it is not presented as an application error.

The source and translated columns are deliberately visually separated because the
English projection is derived data, not employer evidence.

### Search plan

The search screen displays:

- catalog version;
- configured profiles;
- the effective bounded search sequence;
- request budget;
- every search pack, description, and Persian/English term.

This keeps acquisition coverage inspectable without requiring terminal commands.

### Operations

Mutable browser operations run through one local single-worker queue. Long-running
sync/translation work therefore does not block the initial HTTP response, and accidental
double-clicks cannot start overlapping mutable acquisition runs.

Operation pages poll local status and display the same concise service summaries used by
the CLI.

The queue is intentionally in-memory. Durable acquisition history, fetch observations,
translation attempts, and artifacts continue to live in SQLite; browser operation cards
are only UI runtime state.

### System

The system page exposes the important current runtime boundary:

- SQLite/evidence/export paths;
- configured LM Studio URL and model identities;
- translation provider and automatic-translation state;
- acquisition/search/detail limits;
- current parsed/translated coverage.

Advanced persistent configuration remains in `jobhunter.toml`. Daily per-run limits are
available directly on the dashboard.

## Browser security

The local app includes several safeguards even though it defaults to loopback:

- a process-local CSRF token is required for every mutating HTML form;
- `X-Frame-Options: DENY`;
- restrictive Content Security Policy;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- no CDN JavaScript, fonts, images, or CSS;
- no exposed OpenAPI/Swagger endpoints in the browser app.

The web application must not weaken JobHunter's source-access policy. Browser buttons
still call the same bounded/rate-limited source services.

## Dependency strategy

The UI intentionally avoids a Node/npm toolchain.

Current web dependencies are:

- FastAPI;
- Uvicorn;
- Jinja2;
- python-multipart;
- packaged CSS and small vanilla JavaScript.

This keeps the product a local Python modular monolith and avoids maintaining a second
frontend build ecosystem before the product requires one.

## Failure model

A browser operation can finish as:

```text
completed
failed
```

A failed UI operation does not roll back previously preserved source evidence, semantic
versions, fetch observations, successful translations, or exports.

The operation page surfaces the exception type/message or service summary for inspection.

## Testing

Normal deterministic tests use FastAPI's local test client and do not contact Jobinja or
LM Studio.

Coverage includes:

- rendering all primary pages against an empty local database;
- packaged static assets;
- browser security headers;
- CSRF rejection;
- asynchronous local operation execution/polling;
- safe empty-catalog filtering;
- discovered-but-unfetched job rendering;
- Quick Add input classification and external-source rejection;
- sync guidance/preset presence;
- loopback-only launcher behavior;
- desktop launcher binding to the exact configuration path.

Live acceptance should additionally confirm Quick Add against a real Jobinja keyword or
job URL and verify that the resulting posting/detail state appears immediately in the same
local catalog.
