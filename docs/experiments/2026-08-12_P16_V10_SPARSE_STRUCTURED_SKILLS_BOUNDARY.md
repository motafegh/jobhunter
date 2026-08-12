# P1.6 v10 Sparse / Structured-Skills Boundary

**Date:** 2026-08-12  
**Status:** Active acceptance experiment; v10 is **not** promoted to the production P1.6 contract  
**Trigger job:** `t4jp`  
**Rejected baseline artifact:** English P1.6 artifact `30` (`job-analysis-english-v9` / `job-analysis-v4`)  
**Candidate contract:** `job-analysis-english-v10` / `job-analysis-v4`

## 1. Why this experiment exists

CI-3 deliberately moved from the dense `tG9K` baseline to the sparse/ambiguous `t4jp` posting. The goal was to verify that accepted P1.6 behaves conservatively when the employer supplies little detail.

The first evidence-first workflow was:

```text
snapshot t4jp
→ mechanical CI-3 audit
→ discover missing English P1.6
→ generate only English P1.6
→ snapshot again
→ review P1.6 before Capability
```

Artifact `30` was generated with the accepted v9 contract and contained:

```text
role purpose:      0
responsibilities:  1
requirements:      4
```

The artifact was grounded and superficially conservative, but semantic review exposed two repeatable contract defects. Therefore artifact `30` is **not accepted** as the sparse CI-3 P1.6 result and Capability must not be generated above it.

## 2. Source evidence that exposed the defects

The current Jobinja source and hardened English projection contain a structured `skills` array:

```text
Artificial Intelligence
Video content production
social networks
```

The Jobinja parser obtains this field from the source label `مهارت‌های مورد نیاز` / `مهارت های مورد نیاز`, i.e. required skills.

The English description is sparse and qualification-heavy:

```text
Skills in content creation with AI, creativity in creating visual and video content,
website design, ability to produce visual content full-time and part-time, the work is
teachable. Ethics and your work commitment are important to us. ...
```

No explicit responsibility section exists.

## 3. Defect A — structured required skills were outside deterministic coverage

The v9 evidence catalog already exposed structured skill references such as:

```text
field:skills:0
field:skills:1
field:skills:2
```

However `build_requirement_coverage_plan()` only forced accounting for:

- meaningful `minimum_experience`;
- meaningful `education`;
- description spans under recognized requirements/qualifications/skills/technical-stack headings.

It did **not** include the top-level structured `skills[]` field.

Consequently artifact `30` could validate while omitting the explicit `social networks` skill and without mechanically accounting for the exact structured skill items.

This is a deterministic P1.6 recall-boundary defect, not merely a model-quality issue.

## 4. Defect B — qualification wording leaked into responsibilities

Artifact `30` persisted:

```text
Produce visual content full-time and part-time
```

as a responsibility, while its evidence was the same broad qualification-heavy description containing:

```text
ability to produce visual content ...
```

The existing v9 semantic rules already say that ability/mastery/familiarity/knowledge/skill wording belongs under requirements unless the source explicitly frames it as employee work. Sparse text with no responsibility checklist nevertheless allowed the model to paraphrase this qualification into a duty.

This is a qualification-vs-work classification boundary defect.

## 5. What v10 changes

v10 intentionally keeps the persisted schema at `job-analysis-v4`. The artifact identity changes because the semantic/validation contract changes.

Candidate identity:

```text
job-analysis-english-v10
job-analysis-v4
```

### Structured-skill invariant

Every non-empty top-level `skills[]` item must:

1. appear as a requirement;
2. cite that exact structured skill as evidence;
3. preserve `required` obligation strength for this Jobinja required-skills surface;
4. receive deterministic persisted coverage accounting.

The candidate fails closed if any structured skill disappears.

### Qualification-vs-responsibility invariant

v10 rejects responsibilities when:

- they reuse the exact evidence already serving as qualification evidence;
- they paraphrase an `ability to ...` qualification into an employee action;
- their evidence is plainly qualification-framed (`ability to`, `skill(s) in`, `knowledge of`, `experience with`, `familiarity with`).

The model must either cite narrower explicit duty evidence or omit the responsibility.

### Bounded correction

The isolated v10 runtime runs the existing Instructor/Pydantic analysis validation first, then the additional v10 semantic checks.

If only the v10 boundary fails, JobHunter permits one bounded correction request. The corrected output is revalidated; a second failure fails closed.

This is not open-ended retry or prompt patching.

## 6. Why v10 is isolated instead of immediately replacing v9

`tG9K` artifact `29` is an accepted dense baseline under v9. Silently modifying v9 while retaining the same prompt identity would make artifact reuse semantically dishonest. Immediately changing the public P1.6 contract would also invalidate the accepted dense chain before proving the new rules do not regress it.

Therefore:

```text
production/accepted baseline remains v9
+
isolated v10 candidate path
→ sparse t4jp review
→ dense tG9K regression review
→ only then decide promotion
```

The production `jobhunter jobs analyze` command remains v9 during this experiment.

## 7. Candidate tooling

Run one candidate:

```bash
python scripts/run_p16_v10_candidate.py --job-id <job-id>
```

Export a review snapshot selecting that candidate:

```bash
python scripts/export_p16_v10_candidate_snapshot.py --job-id <job-id>
```

Run candidate-specific mechanical checks:

```bash
python scripts/audit_p16_v10_candidate_snapshot.py --job-id <job-id>
```

Candidate implementation:

```text
src/jobhunter/analysis_service_v10.py
src/jobhunter/analysis_runtime_v10.py
scripts/run_p16_v10_candidate.py
scripts/export_p16_v10_candidate_snapshot.py
scripts/audit_p16_v10_candidate_snapshot.py
tests/test_analysis_v10_candidate.py
```

## 8. Acceptance sequence

### Gate A — sparse `t4jp`

Require:

- all structured required skills survive exactly;
- no unsupported responsibilities are invented from qualifications;
- no false role purpose;
- requirement strength is not inflated or weakened;
- sparse evidence remains sparse rather than becoming a generic AI/content curriculum;
- evidence remains exact and relevant;
- candidate mechanical audit passes.

### Gate B — dense `tG9K` regression

Only after `t4jp` passes, generate v10 for `tG9K` and compare against accepted artifact `29`.

Require no material regression in:

- 27 requirements;
- 7 responsibilities;
- optionality/contextual strength;
- Python-only `expert` depth;
- preferred MATLAB/C++;
- all explicit depth facts;
- education and 3–6 years experience;
- dense requirement/responsibility coverage.

### Promotion decision

Only if both sparse and dense gates pass should v10 replace v9 as the public English P1.6 contract. Promotion must update the normal analysis service, Review Snapshot routing, CI-3 audit identity, docs, and downstream current-chain semantics together.

Capability v7 must then be rebuilt/reviewed from the promoted P1.6 identity rather than reused from an older analysis artifact.

## 9. Stop rules

Do not:

- run Capability above rejected artifact `30`;
- call v10 accepted merely because its mechanical audit passes;
- weaken candidate validators to make `t4jp` pass;
- add `t4jp`-specific skill names or phrases to the prompt;
- promote v10 before dense regression;
- silently relabel existing v9 artifacts as v10.

If v10 cannot pass sparse and dense evidence without brittle vacancy-specific rules, keep v9 as the accepted baseline and redesign the general P1.6 boundary based on the observed failure class.
