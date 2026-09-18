# Market I7 — Bounded Real Local Acceptance Protocol

**Date:** 2026-09-18  
**Status:** EXECUTED / RESULT HOLD  
**Branch:** main  
**Repository head at preparation:** a5eff89dfccbad57aad6ff4dc22beeec0d76823b  
**Baseline CI:** run 1214 / 35264034420 — SUCCESS  
**Execution result:** `docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

## Purpose

I7 is the bounded real-machine acceptance of the complete first Market vertical slice.

It is not another architecture or feature phase. The goal is to prove on the owner's actual runtime
and operational SQLite that the accepted I1-I6 path is useful, bounded, currentness-safe,
inspectable, repeatable, and private by default.

Possible outcomes: PASS, BOUNDED REPAIR, or HOLD. Do not force PASS merely because repository CI is green.

## Preconditions

Use the owner's existing local configuration, normally config/local.toml. Do not commit that file,
model identifiers, API keys, operational SQLite, raw evidence, local host paths, or unreviewed screenshots.

Before mutation run:

    git pull --ff-only
    git status --short
    jobhunter --version
    jobhunter-corpus status
    jobhunter --config config/local.toml market target list

Confirm LM Studio/provider readiness using the same local configuration already used by JobHunter.
Do not switch models or prompt contracts merely to obtain a passing result.

Record Git head, config path only, safe effective model names when appropriate, public-corpus counts,
and existing Market target IDs.

## Representative target

Use one intentionally precise Applied AI / ML Engineering target.

Stable target identity if a semantically equivalent one does not already exist:

    slug: applied-ai-ml-engineering
    name: Applied AI / ML Engineering

Membership intent:

    Applied AI / ML engineering where the primary work is developing, evaluating, or improving
    AI/ML models, agents, retrieval, or AI system behavior. Backend/API/database/infrastructure
    roles primarily enabling or integrating AI services are adjacent rather than core. Using AI
    tools for general software or content production does not qualify for this target.

This wording preserves the I3 real-model lesson. Do not patch individual vacancies into the target definition.

### Create only when no equivalent target exists

    jobhunter --config config/local.toml market target create --slug applied-ai-ml-engineering --name "Applied AI / ML Engineering" --description "Bounded I7 acceptance target for direct applied AI/ML engineering work."

Save TARGET_ID.

### Create or reuse one immutable definition

Prefer a small explicit acquisition envelope rather than the broad whole profile for I7:

    jobhunter --config config/local.toml market definition create TARGET_ID --intent "Applied AI / ML engineering where the primary work is developing, evaluating, or improving AI/ML models, agents, retrieval, or AI system behavior. Backend/API/database/infrastructure roles primarily enabling or integrating AI services are adjacent rather than core. Using AI tools for general software or content production does not qualify for this target." --term "AI Engineer" --term "Machine Learning Engineer" --term "RAG" --term "AI Agent" --term "MLOps" --include-hint "direct model, agent, retrieval, evaluation, or AI-system engineering" --exclude-hint "generic software/content work that merely uses AI tools"

Save DEFINITION_ID, definition version, and fingerprint. If an exactly equivalent definition already
exists, intentional reuse is correct.

## Frozen I7 run controls

Use the same controls for the first run and unchanged rerun:

    request_budget       5
    search_limit         5
    default_max_pages    1
    missing_limit        4
    refresh_limit        2
    refresh_after_hours  168
    translation_limit    4
    analysis_limit       2
    membership_limit     8

These are acceptance controls, not new product defaults.

## Read-only preview

Run before acquisition:

    jobhunter --config config/local.toml market preview DEFINITION_ID --request-budget 5 --search-limit 5 --default-max-pages 1 --missing-limit 4 --refresh-limit 2 --refresh-after-hours 168 --translation-limit 4 --analysis-limit 2 --membership-limit 8

Verify exactly the intended five searches are selected, each is one page, the request budget is five,
no unexpected profile/pack expansion appears, and preview itself does not mutate provider/runtime state.

If preview scope is wrong, stop before the run and repair only the owning definition/search boundary.

## First bounded real run

Execute:

    jobhunter --config config/local.toml market run DEFINITION_ID --request-budget 5 --search-limit 5 --default-max-pages 1 --missing-limit 4 --refresh-limit 2 --refresh-after-hours 168 --translation-limit 4 --analysis-limit 2 --membership-limit 8

A non-zero exit because the run completed with bounded stage failures is evidence to inspect, not
automatic proof that the product failed.

Capture run ID, status, snapshot ID, profile ID, candidate count, membership count, and failure summary.

## Inspect durable evidence

For the returned IDs:

    jobhunter --config config/local.toml market run-show RUN_ID
    jobhunter --config config/local.toml market snapshot-show SNAPSHOT_ID
    jobhunter --config config/local.toml market show --definition-id DEFINITION_ID

Verify the run ledger exposes discovery/request bounds and the selected/reused/completed/failed/remaining
states for source, translation, P1.6, and membership where applicable.

Verify semantic/product boundaries:

- candidates outside the target remain possible acquisition noise;
- core_match, adjacent_match, uncertain, and excluded are not collapsed;
- only core enters the primary source denominator;
- accepted-current P1.6 is a separate semantic denominator;
- pending/missing/failed/rejected P1.6 never appears as zero demand;
- source evidence and P1.6 IDs remain traceable;
- aggregate numbers are deterministic and denominators inspectable;
- employer concentration/repost limitations remain visible when applicable.

## Source/lifecycle failure rule

Inspect any refresh/source failures.

Required behavior:

    network / rate-limit / server / challenge / auth failure
    != disappearance
    != successful freshness update

A failed refresh must preserve prior durable evidence and must not silently mark a job removed.

If no natural failure occurs, do not manufacture a destructive source state. Repository tests already
cover the deterministic failure rule; I7 only needs to confirm real-run behavior does not contradict it.

## Browser parity

Start the existing local app:

    jobhunter-app --config config/local.toml --no-browser

Open the loopback browser UI and inspect /market/targets.

Verify the browser shows the same target, definition, run, snapshot/profile identities, denominator
semantics, membership dispositions, and evidence drill-down as the CLI.

Do not commit screenshots until privacy review confirms no local/private material is visible.

## Unchanged rerun

Repeat the identical run command with the same definition and controls, then inspect the new run/snapshot.

The second run must demonstrate meaningful reuse/currentness rather than unnecessary recomputation:

- already-current source details are not blindly refetched outside refresh policy;
- current English artifacts are reused;
- matching current P1.6 is reused;
- matching membership dependencies reuse immutable decisions;
- no unrelated global backlog is consumed because budget remains;
- old run/snapshot/profile history remains immutable.

Record first- versus second-run affected-work counts.

## SQLite integrity

Use Python so no external sqlite3 executable is required:

    python -c "from jobhunter.config import Settings; import sqlite3; p=Settings.load('config/local.toml').database_path; c=sqlite3.connect(p); print('integrity=', c.execute('PRAGMA integrity_check').fetchone()[0]); print('foreign_keys=', c.execute('PRAGMA foreign_key_check').fetchall())"

Acceptance expectation:

    integrity= ok
    foreign_keys= []

## Privacy/publication boundary

After the run inspect repository state:

    git status --short
    git diff -- corpus

Then verify Market-local table names have not appeared in public corpus:

    python -c "from pathlib import Path; names=('market_targets','market_research_runs','market_job_memberships','market_corpus_snapshots','market_aggregate_profiles'); hits=[]; [hits.append(str(p)) for p in Path('corpus').rglob('*') if p.is_file() and any(n in p.read_text(encoding='utf-8', errors='ignore') for n in names)]; print(hits)"

Expected result:

    []

Existing governed public English/P1.6 projection files may legitimately change when the Market run
creates those already-approved upstream artifacts. Review those separately; this does not authorize
publishing Market target/run/membership/snapshot/profile state.

## Acceptance record

After local execution create one sanitized evidence record containing only:

- Git head;
- run controls;
- target and definition IDs/version/fingerprint;
- search/request counts;
- candidate count;
- stage reuse/completion/failure/remaining counts;
- membership disposition counts;
- run status;
- snapshot/profile IDs;
- core source denominator;
- accepted-semantic denominator;
- warnings/limitations;
- representative source/P1.6 evidence references;
- unchanged rerun comparison;
- SQLite integrity result;
- browser/CLI parity result;
- privacy/publication result.

Do not include operational SQLite, API tokens, local host paths, raw LM Studio protocol, raw private
evidence, or unreviewed screenshots.

## Decision rule

PASS only when the complete repeated-use path is correct/useful, immutable/currentness behavior is
preserved, denominators are honest, browser/CLI agree, and no privacy/source-integrity defect appears.

For BOUNDED REPAIR, name the exact owner: I2 affected work, I3 membership, I4 snapshot, I5 aggregate,
or I6 workflow/UI. Repair only that boundary, rerun deterministic CI, then repeat the affected I7 checks.

Use HOLD when provider/source/local conditions prevent a defensible conclusion. Preserve the evidence
and keep the first Market slice open.

## Stop lines

During I7 do not add semantic role-subfamily synthesis, trends/emerging/forecasting, Market-to-You
scoring, P1.6 auto-acceptance, Capability/Work mandatory gating, speculative repost dedup, Market
publication, another workflow/currentness/persistence stack, or test weakening around live-provider behavior.

I7 exists to validate I1-I6, not to broaden the product.
