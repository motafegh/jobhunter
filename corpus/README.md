# JobHunter Public Corpus

`corpus/` is the complete repository-safe projection of JobHunter's current public job corpus.

It exists so public Jobinja vacancies and their successfully completed processing stages are available both:

```text
locally  → data/jobhunter.sqlite3
remotely → corpus/
```

The local SQLite database remains the runtime authority. `corpus/` is a deterministic, Git-versioned projection for review, research, AI-assisted development, reproducibility, heterogeneous semantic testing, Market work, and later Phase-2 analysis.

## Authority and purpose

```text
public Jobinja acquisition
        ↓
local SQLite durable state              ← runtime authority
        ↓ deterministic projection
corpus/                                  ← versioned public dataset
```

The corpus is not imported automatically into SQLite and is not a replacement for the operational database.

## Layout

```text
corpus/
├── README.md
├── manifest.json
└── jobs/
    └── <source-job-id>/
        ├── source.json
        ├── english-projection.json     # when current projection exists
        ├── p16-english.json            # when current accepted English contract exists
        ├── p16-original.json           # when current original-language contract exists
        └── capability.json             # when current public Capability contract exists
```

Every discovered Jobinja job is represented in `manifest.json` and receives `source.json`. A discovery-only job may have `current_detail: null` until its detail page is acquired.

## `source.json`

`source.json` contains repository-safe current public source state:

- stable Jobinja job ID;
- canonical public URL and company slug;
- first/last seen and lifecycle state;
- current detail-version ID when available;
- fetch/status/hash/parser metadata;
- complete deterministic `jobinja-detail-v2` parsed vacancy fields;
- original Persian/English vacancy content preserved as UTF-8.

The parser's public vacancy fields include title, company, category, location, employment type, minimum experience, salary, description, skills, gender, military-service requirement, education, company description, source dates, language, and parser version where Jobinja supplies them.

## Derived stage files

Derived files contain only durable public-domain results and dependency identities.

`english-projection.json` includes the current English projection, provider/model/schema identity, source hash, translated fields/document, segment provenance, and translation artifact ID.

`p16-english.json` and `p16-original.json` include the current public P1.6 artifact ID, dependency IDs, model/prompt/schema identity, and analysis payload.

`capability.json` includes the current public Capability artifact ID, exact translation/P1.6 dependencies, model/prompt/schema identity, and capability intelligence.

When the source changes, old downstream files are removed from the current corpus until those stages are successfully rebuilt for the new current source version. Previous committed states remain available through Git history.

## Deliberately excluded

The public corpus does **not** contain:

- SQLite/WAL/SHM implementation files;
- machine-local evidence paths;
- raw HTML evidence files;
- LM Studio request bodies or raw protocol responses;
- system prompts;
- API tokens or secrets;
- logs/debug histories;
- local configuration;
- future private/personal evidence, applications, notes, or profile data.

Those exclusions keep the repository dataset focused on reusable public job-domain facts and accepted processing outputs.

## Commands

Backfill or refresh the complete corpus from the local database:

```bash
jobhunter-corpus export
```

Verify that every corpus file exactly matches current durable SQLite public state:

```bash
jobhunter-corpus verify
```

Inspect repository coverage without opening SQLite:

```bash
jobhunter-corpus status
```

The default output directory is `./corpus`.

## Automatic local synchronization

The installed `jobhunter` CLI refreshes `corpus/` after durable mutating workflows including:

```text
jobhunter run
jobhunter jobinja discover
jobhunter jobinja fetch
jobhunter jobinja sync
jobhunter translations run
jobhunter jobs analyze
jobhunter jobs capability
```

SQLite persistence happens first. Corpus synchronization happens afterward. A projection failure never rolls back durable SQLite state, but it is surfaced as a non-zero command outcome when the underlying operation otherwise succeeded so repository divergence cannot be silent.

Read-only commands do not rewrite the corpus.

## Git publishing

JobHunter deliberately does not auto-commit or auto-push data. Runtime correctness must not depend on Git credentials, internet availability, or repository state.

After local work:

```bash
jobhunter-corpus verify
git status --short
git diff -- corpus/
git add corpus/
git commit -m "data: update JobHunter public corpus"
git push origin main
```

Once pushed, the complete current public corpus is directly inspectable from GitHub by humans and AI assistants without access to the local SQLite database.

## Difference from `review-snapshots/`

These directories serve different purposes:

```text
corpus/
→ complete current public dataset
→ every known job
→ current successful processing stages
→ routine version-controlled projection

review-snapshots/
→ deliberately selected acceptance/review evidence
→ small curated examples
→ semantic decision records and regression anchors
```

Do not replace either with the other.
