# JobHunter Role Capability Blueprint Plan

**Status:** Active implementation plan  
**Date:** 2026-08-04

## Purpose

JobHunter already has strict English extraction and evidence-qualified Capability Intelligence. Keep both unchanged. Add a separate human-facing layer that answers: what does this vacancy probably require in practice when read by a senior engineer/domain specialist?

## Layering

```text
English job context
-> strict English extraction
-> Capability Intelligence
-> Role Capability Blueprint
```

The blueprint is independently versioned and persisted.

## Freedom contract

This layer intentionally has more reasoning freedom than Capability Intelligence.

It may:
- synthesize conclusions not literally stated in the posting;
- use professional software/domain knowledge;
- infer likely sub-skills, technical scope, operational concerns and expected depth;
- suggest plausible libraries/frameworks/APIs/protocols as examples;
- connect company domain, responsibilities, requirements and technologies into end-to-end interpretations;
- identify likely non-requirements so broad technologies do not become generic curricula.

It must not:
- present inferred tools/libraries as explicit employer requirements;
- invent factual company systems, vendors, scale or architecture;
- dump a generic curriculum for every technology;
- waste output repeating facts that are obvious from rereading the advertisement;
- present weak speculation with the same certainty as a strong inference.

Guiding rule: **be professionally useful; label uncertainty instead of suppressing reasonable expert inference.**

## Interpretation strength

Use:

```text
highly_likely
plausible
speculative
```

These describe expert interpretation, not employer truth.

## Whole-job reasoning

Reason from combinations, not isolated keywords.

Example:

```text
Python + AI APIs + shipping documents + CRM/email integration + agents + logistics company
-> likely applied-AI automation/integration work involving document ingestion, structured extraction,
validation, workflow orchestration, API integration, business rules, human review and operational reliability.
```

Responsibilities/deliverables and company domain carry more weight than isolated skill tags.

## User-value test

Before keeping a sentence, ask: **does this teach something that is not obvious from simply rereading the vacancy?**

Avoid statements such as "the job is titled AI Specialist" unless needed for a non-obvious conclusion.

## Artifact contract

`RoleCapabilityBlueprint`:

```text
role_read
likely_role_shape
capability_areas[]
hidden_requirements[]
likely_end_to_end_scenarios[]
what_probably_does_not_matter[]
important_unknowns[]
bottom_line
```

Each capability area:

```text
name
interpretation_strength
likely_depth
why_this_matters
likely_subskills[]
likely_tools_or_examples[]
likely_work_products[]
likely_failure_modes_or_operational_concerns[]
probably_not_required[]
```

Each scenario:

```text
name
why_likely
flow_steps[]
engineering_concerns[]
interpretation_strength
```

No exact-quote requirement exists in this artifact.

## Inputs

The model receives together:

```text
analysis_fields
accepted_extraction
capability_intelligence
```

`analysis_fields` provides the complete hardened English vacancy/company context. `accepted_extraction` prevents missing explicit duties. `capability_intelligence` is supporting analytical substrate, not a cage; the blueprint may reorganize or improve its interpretation.

## Inference/validation philosophy

Use Instructor/Pydantic only as a light structural envelope: required sections, object/list types, the interpretation-strength enum, and broad list-count bounds. Do not impose exact evidence matching, rigid depth enums, source-status labels on every statement, or large provider-facing prose-length constraints.

The layer should fail for malformed/unusable structure, not because a useful professional inference lacks an exact quotation.

## Persistence identity

```text
job detail version
+ English projection artifact
+ English analysis artifact
+ Capability Intelligence artifact
+ model
+ blueprint prompt version
+ blueprint schema version
```

## Product surfaces

Browser: `Capability Intelligence -> Role Capability Blueprint`

CLI: `jobhunter jobs blueprint <job-id>`

The browser page should prioritize readable expert explanation rather than evidence cards.

## Operational bounds

- one model call plus at most one structural validation retry;
- bounded output tokens;
- bounded number of major areas/scenarios/list items;
- no automatic corpus-wide blueprint generation yet.

These bounds control cost/runtime, not reasoning freedom.

## Acceptance

The slice is acceptable when:
1. strict extraction and Capability Intelligence remain unchanged;
2. blueprint artifacts persist independently and reuse unchanged dependencies;
3. vague terms such as Python/AI APIs/automation can be expanded into likely practical scope and depth;
4. tool/library suggestions are clearly examples when not explicit requirements;
5. whole-job/company context materially informs interpretation;
6. output avoids trivial restatement and generic curriculum dumping;
7. uncertainty is expressed as highly likely/plausible/speculative;
8. local Ruff, pytest and warnings-as-errors gates pass;
9. live output is reviewed before bulk generation is enabled.

## Lessons carried forward

- Do not make human explanation inherit audit/evidence constraints.
- Do not make analytical prose exact-copy evidence.
- Do not put large prose-length rules into LM Studio sampling grammar.
- Use deterministic software for bookkeeping; use the model for interpretation.
- Model success is not semantic-quality acceptance.

```text
strict extraction -> truth
Capability Intelligence -> auditable machine reasoning
Role Capability Blueprint -> useful expert explanation
```
