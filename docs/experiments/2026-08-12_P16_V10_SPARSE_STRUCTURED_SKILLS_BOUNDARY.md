# P1.6 v10 Sparse / Structured-Skills Boundary

**Date:** 2026-08-12  
**Status:** Concluded — artifact `31` mechanically passed but semantically failed; superseded by isolated v11 candidate  
**Trigger job:** `t4jp`  
**Rejected v9 artifact:** English P1.6 artifact `30` (`job-analysis-english-v9` / `job-analysis-v4`)  
**Rejected v10 artifact:** English P1.6 artifact `31` (`job-analysis-english-v10` / `job-analysis-v4`)

## 1. Why this experiment existed

CI-3 deliberately moved from the dense `tG9K` baseline to the sparse/ambiguous `t4jp` posting. The goal was to verify that accepted P1.6 behaves conservatively when the employer supplies little detail.

The evidence-first workflow was:

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

It was grounded and superficially conservative, but semantic review exposed two repeatable contract defects. Therefore artifact `30` was not accepted and Capability was not generated above it.

## 2. Source evidence that exposed the v9 defects

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

However `build_requirement_coverage_plan()` only forced accounting for meaningful structured education/experience plus description spans under recognized requirement/qualification/skills/technical-stack headings. It did not include the top-level structured `skills[]` field.

Consequently artifact `30` could validate while omitting the explicit `social networks` skill and without mechanically accounting for the exact structured skill items.

This was a deterministic P1.6 recall-boundary defect, not merely a model-quality issue.

## 4. Defect B — qualification wording leaked into responsibilities

Artifact `30` persisted:

```text
Produce visual content full-time and part-time
```

as a responsibility, while its evidence was the broad qualification-heavy description containing:

```text
ability to produce visual content ...
```

The v9 semantic rules already say ability/mastery/familiarity/knowledge/skill wording belongs under requirements unless explicitly framed as employee work. Sparse text with no responsibility checklist nevertheless allowed the model to paraphrase this qualification into a duty.

This was a qualification-vs-work classification boundary defect.

## 5. What v10 changed

v10 kept the persisted schema at `job-analysis-v4` but changed artifact identity because the semantic/validation contract changed:

```text
job-analysis-english-v10
job-analysis-v4
```

### Structured-skill invariant

Every non-empty top-level `skills[]` item had to:

1. appear as a requirement;
2. cite that exact structured skill as evidence;
3. preserve `required` obligation strength for this Jobinja required-skills surface;
4. receive deterministic persisted coverage accounting.

### Qualification-vs-responsibility invariant

v10 rejected responsibilities when they reused qualification evidence, paraphrased `ability to ...` into employee work, or were plainly qualification-framed.

### Bounded correction

The isolated v10 runtime permitted one bounded correction after the normal Instructor/Pydantic analysis validation, then failed closed.

## 6. Live v10 result — artifact 31

The user ran the isolated v10 candidate on `t4jp` and produced:

```text
artifact:          31
model:             gemma-4-e4b-it-ud
prompt/schema:     job-analysis-english-v10 / job-analysis-v4
responsibilities:  0
requirements:      7
structured skills: 3/3 covered
mechanical audit:  PASS
snapshot commit:   23348b2
```

v10 successfully fixed both targeted v9 defects:

- all three structured required skills survived with exact evidence;
- the unsupported qualification-derived responsibility disappeared.

## 7. Why v10 still failed semantic acceptance

Complete semantic review of artifact `31` found a remaining recall/provenance defect.

The source explicitly states distinct qualification facts:

```text
Skills in content creation with AI
creativity in creating visual and video content
website design
ability to produce visual content full-time and part-time
```

Artifact `31` did not preserve the first two as their own requirements. A broad structured tag `Artificial Intelligence` is not semantically equivalent to the narrower qualification `content creation with AI`.

The reason was deterministic coverage granularity: the description-side requirement planner still treated the whole qualification-heavy sentence/paragraph as one broad evidence unit. One requirement citing that broad span could therefore satisfy coverage while neighboring explicit qualification facts disappeared.

This means v10 was **mechanically correct for the boundaries it introduced, but still semantically incomplete** for sparse comma-separated qualification lists.

## 8. Disposition

Artifact `31` is rejected as sparse CI-3 P1.6 evidence despite its mechanical PASS.

Do not:

- run Capability above artifact `31`;
- run the dense `tG9K` regression under v10;
- promote v10 to the public analysis path;
- mutate v10 semantics while reusing the same artifact identity.

The public/accepted P1.6 baseline remains v9 while the isolated candidate advances to v11.

## 9. Successor

The successor experiment is documented in:

```text
docs/experiments/2026-08-12_P16_V10_SEMANTIC_FAILURE_AND_V11_QUALIFICATION_GRANULARITY.md
```

v11 retains the useful v10 boundaries and adds generic item-level coverage for clearly introduced comma-separated qualification lists, including truthful `decomposed_requirement` provenance when granular requirements supersede a coarse legacy coverage span.
