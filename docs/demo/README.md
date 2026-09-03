# JobHunter Reproducible Public Demo

This walkthrough lets an external reviewer inspect meaningful JobHunter output from a fresh clone **without** the maintainer's SQLite database, LM Studio, or live Jobinja access.

It uses only committed repository-safe evidence from [`../../corpus/`](../../corpus/README.md). Nothing in this demo is fabricated or generated specifically for presentation.

## What this demo proves

The committed public corpus demonstrates that JobHunter can preserve and connect a real public job through these current accepted stages:

```text
public source state
→ provenance-preserving English projection
→ reviewed P1.6 factual extraction
→ Capability Intelligence
```

It also demonstrates an important negative capability: when a vacancy supplies qualifications but no explicit duties, JobHunter keeps the responsibility set empty instead of inventing work from role stereotypes or tool requirements.

This demo does **not** prove production-scale labor-market coverage, personal fit scoring, autonomous applications, or the correctness of every discovered vacancy. The repository currently contains 353 discovered job identities, 43 fetched/parsed details, 20 current English projections, 5 accepted English P1.6 artifacts, and 5 accepted Capability artifacts.

## 1. Fastest path: GitHub only

No installation is required. Open these two accepted chains directly in the repository.

### Rich responsibility example — `t4qV`

Senior Network Security Engineer:

- [`source.json`](../../corpus/jobs/t4qV/source.json)
- [`english-projection.json`](../../corpus/jobs/t4qV/english-projection.json)
- [`p16-english.json`](../../corpus/jobs/t4qV/p16-english.json)
- [`capability.json`](../../corpus/jobs/t4qV/capability.json)

This example contains explicit employer duties such as network-security architecture, next-generation firewall management, VPN design, troubleshooting, Zero Trust/network segmentation, and technical documentation. The accepted P1.6 artifact preserves those as factual responsibilities with exact evidence, and Capability Intelligence groups them without replacing the accepted statements.

### Sparse responsibility example — `tmBK`

Python Developer:

- [`source.json`](../../corpus/jobs/tmBK/source.json)
- [`english-projection.json`](../../corpus/jobs/tmBK/english-projection.json)
- [`p16-english.json`](../../corpus/jobs/tmBK/p16-english.json)
- [`capability.json`](../../corpus/jobs/tmBK/capability.json)

This vacancy contains substantial requirements—Python/Django, DRF/FastAPI, Git, Linux, databases, concurrency/transactions, problem solving, AI-assisted development, and ownership expectations—but does not state concrete job duties. The accepted P1.6 artifact therefore contains:

```text
responsibilities: []
role_purpose: []
```

Capability Intelligence may still organize employer-stated capability requirements, but its `source_responsibility_indices` and `work_activities` remain empty. This is intentional evidence discipline, not missing output.

## 2. Fresh-clone CLI path

Requirements:

- Git
- Python 3.12+

Clone and install:

```bash
git clone https://github.com/motafegh/jobhunter.git
cd jobhunter
python -m pip install -e ".[dev]"
```

Read the committed manifest without opening SQLite:

```bash
jobhunter-corpus status
```

For the current committed baseline, the meaningful counts are:

```text
Known/discovered jobs: 353
Fetched/parsed job details: 43
English projections: 20
English P1.6: 5
Original P1.6: 0
Capabilities: 5
```

`353` means discovered job identities, not 353 fully processed advertisements.

## 3. Inspect the complete accepted chains

The Python standard library is enough; no `jq`, database, or model server is required.

```bash
python -m json.tool corpus/jobs/t4qV/source.json
python -m json.tool corpus/jobs/t4qV/english-projection.json
python -m json.tool corpus/jobs/t4qV/p16-english.json
python -m json.tool corpus/jobs/t4qV/capability.json
```

Then compare the sparse case:

```bash
python -m json.tool corpus/jobs/tmBK/source.json
python -m json.tool corpus/jobs/tmBK/english-projection.json
python -m json.tool corpus/jobs/tmBK/p16-english.json
python -m json.tool corpus/jobs/tmBK/capability.json
```

## 4. Verify lineage, not just prose

JobHunter's derived artifacts carry exact dependency identities. The following read-only script checks the two demo chains and prints the evidence shape that matters to a reviewer:

```bash
python - <<'PY'
import json
from pathlib import Path


def load(job_id: str, name: str):
    return json.loads((Path("corpus/jobs") / job_id / name).read_text(encoding="utf-8"))


for job_id in ("t4qV", "tmBK"):
    projection = load(job_id, "english-projection.json")
    p16 = load(job_id, "p16-english.json")
    capability = load(job_id, "capability.json")

    assert projection["artifact_id"] == p16["translation_artifact_id"]
    assert p16["artifact_id"] == capability["analysis_artifact_id"]
    assert projection["artifact_id"] == capability["translation_artifact_id"]
    assert p16["semantic_review_status"] == "accepted"

    responsibilities = p16["analysis"]["responsibilities"]
    capabilities = capability["intelligence"]["capabilities"]
    work_activities = sum(len(item["work_activities"]) for item in capabilities)

    print(
        f"{job_id}: translation={projection['artifact_id']} "
        f"-> p16={p16['artifact_id']} -> capability={capability['artifact_id']}"
    )
    print(
        f"  accepted responsibilities={len(responsibilities)}, "
        f"capability groups={len(capabilities)}, work activities={work_activities}"
    )
PY
```

Expected evidence shape for the committed examples:

```text
t4qV: translation=20 -> p16=44 -> capability=14
  accepted responsibilities=10, capability groups=4, work activities>0

tmBK: translation=38 -> p16=39 -> capability=13
  accepted responsibilities=0, capability groups=5, work activities=0
```

The exact purpose is more important than the numbers: every accepted downstream layer can be traced to the exact upstream artifact it used.

## 5. What to look for in `t4qV`

### Source

[`source.json`](../../corpus/jobs/t4qV/source.json) preserves:

- stable source job ID and canonical Jobinja URL;
- source/lifecycle timestamps;
- HTTP/fetch and parser metadata;
- `jobinja-detail-v2` parsed fields;
- the original mixed-language vacancy content;
- the semantic source hash used by downstream currentness checks.

### English projection

[`english-projection.json`](../../corpus/jobs/t4qV/english-projection.json) records translation artifact `20` and distinguishes native from translated segments through `segment_provenance`. The original source remains authoritative; the projection is a derived representation.

### Accepted P1.6 factual extraction

[`p16-english.json`](../../corpus/jobs/t4qV/p16-english.json) is accepted artifact `44` under `job-analysis-english-v20 / job-analysis-v5`.

It separates:

- employer requirements;
- required vs preferred strength;
- explicit depth such as `more than six years`;
- factual responsibilities;
- exact supporting evidence;
- coverage bookkeeping;
- semantic-review status.

The artifact is explicitly `accepted`; pending candidates do not enter the committed public corpus.

### Capability Intelligence

[`capability.json`](../../corpus/jobs/t4qV/capability.json) is artifact `14` under `job-capability-intelligence-v9 / job-capability-intelligence-v5` and depends on P1.6 artifact `44` plus translation artifact `20`.

The key engineering distinction is visible inside each capability: `source_requirement_indices`, `source_responsibility_indices`, deterministic `work_activities`, depth evidence, uncertainty, and the exact accepted source truth remain inspectable alongside higher-level grouping labels.

## 6. What to look for in `tmBK`

The sparse case is deliberately valuable because a generic role-based LLM could easily hallucinate backend duties from the title and technology stack.

[`p16-english.json`](../../corpus/jobs/tmBK/p16-english.json) accepts the explicit requirements while leaving `responsibilities` empty. [`capability.json`](../../corpus/jobs/tmBK/capability.json) can group the supported requirements—such as backend frameworks, persistence, engineering fundamentals, and development environment—but does not populate work activities from qualifications alone.

This is one concrete example of JobHunter's authority rule:

> requirements may describe what the employer expects a candidate to know; they do not automatically prove what the employee will do.

## 7. Public corpus vs runtime-only state

The committed demo is intentionally narrower than the full local application.

| Layer | Inspectable from committed corpus? | Why |
| --- | --- | --- |
| Source state | Yes | public, deterministic projection |
| English projection | Yes when current | repository-safe derived public representation |
| Accepted English P1.6 | Yes | only explicitly accepted factual artifacts are published |
| Capability Intelligence | Yes when dependency-current | accepted public downstream artifact |
| Job Work Intelligence v2 | Not currently in `corpus/` | publication of this analytical layer has not been authorized |
| Canonical Registry runtime state | Not currently projected into `corpus/` | reviewed SQLite state remains a separate current subsystem |
| Personal profile/gaps/applications | No | not implemented as current public product state and would be private by design |

Do not infer absence of a corpus file to mean the subsystem does not exist. See [`../ARCHITECTURE.md`](../ARCHITECTURE.md) for the current runtime architecture and [`../../review-snapshots/README.md`](../../review-snapshots/README.md) for selected acceptance evidence.

## 8. Browser demo boundary

The normal application can be launched with:

```bash
jobhunter-app
```

but a fresh clone has no maintainer SQLite database, and JobHunter intentionally does not import the committed public corpus into runtime SQLite behind the user's back. The corpus walkthrough is therefore the reproducible zero-private-state demo.

Real browser screenshots are intentionally **not fabricated from templates or mock state**. Portfolio screenshots should be captured from the real local application once the maintainer has machine-local runtime access again, then added only after confirming they contain no private/local-only information.

## 9. Deeper review evidence

For reviewers who want to inspect selected historical semantic acceptance chains beyond the current public projection:

- [`../../review-snapshots/README.md`](../../review-snapshots/README.md)
- [`../../review-snapshots/jobs/t4qV.json`](../../review-snapshots/jobs/t4qV.json)
- [`../../review-snapshots/jobs/tmBK.json`](../../review-snapshots/jobs/tmBK.json)

Review snapshots are curated acceptance evidence; `corpus/` remains the complete current repository-safe projection.

## Demo integrity rules

Keep this walkthrough truthful as the project evolves:

1. use real committed artifacts only;
2. never paste private SQLite/local state into the demo;
3. keep current vs experimental/runtime-only layers explicit;
4. update counts and artifact IDs when the committed current corpus changes;
5. do not claim that two examples establish market-wide model quality;
6. do not replace evidence inspection with screenshots alone;
7. add screenshots only from the real application, never from mockups presented as runtime output.
