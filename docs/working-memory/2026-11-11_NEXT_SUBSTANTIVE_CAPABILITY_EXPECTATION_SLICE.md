# Next substantive JobHunter increment — evidence-backed capability expectations

**Date:** 2026-11-11
**Status:** PROPOSED NEXT FEATURE GATE — NOT YET APPROVAL OF DURABLE P2.3 PROFILES
**Predecessor:** `2026-11-11_P23A_COMPARISON_STAGE_CLOSURE_AND_NEXT_CAPABILITY_GATE.md`
**Product position:** Phase-2 capability-understanding work, before corpus-scale profiles, Market v2, and personal scoring

## Product decision we need to enable

The current /compare view helps read exact qualification and duty claims. It does **not** yet answer the more valuable question:

> “For this vacancy and capability (for example RAG or Python), which technical activities would I actually have to perform, what depth or independence is supported by the employer's evidence, and what would I still need to investigate or practise?”

A useful answer must go beyond echoing keywords, without inventing expertise levels, complete syllabuses, job duties, or market demand. This is the next **semantic reasoning and actionable understanding** capability, not a cosmetic job-card or visual-summary project.

## Stage 0 — Reuse first, narrow candidate contract

Read existing, accepted owners: current P1.6 job facts (requirements, strength, depth, responsibilities), Capability v9 (where current and accepted), Job Work Intelligence v2, and reviewed exact Registry mappings. Inventory *precisely* which decisions can already be recovered and which genuinely require new bounded semantic reasoning. Do not create a duplicate Capability subsystem to reimplement existing group coverage or source lineage.

Create a small **read-only candidate capability-expectation brief** for a selected current job + one explicit capability phrase/reviewed concept, with these typed sections:

1. **Exact employer statements**: selected requirement, obligation, explicit depth, and directly described matching/linked work, with artifact/source version and clickable claim references.
2. **Supported work implications**: traceable inference, separated from an explicit duty and labeled as an interpretation, with evidence/rationale.
3. **Technical sub-capabilities and practical checks**: only where independently supported by the exact source, strong work implication, or transparently bounded model-proposed candidate; never convert a general label into an authoritative checklist.
4. **Unknown or unsupported scope**: independence, production operation, deployment scale, constraints, architecture, performance/reliability, and work-specific depth when not evidenced.
5. **Decision aid**: short, concrete questions for the user to investigate or verify in an interview/project, linked back to why they matter. Candidate advice, not an asserted employer requirement.

No generic skill score or numerical expertise ladder. Preserve "employer says" vs "work implies" vs "model suggests" vs "not established".

## Stage 1 — Three deliberately different real cases

- **`tvMm`, RAG:** accepted P1.6 has explicit related responsibility evidence; can expectation inference stay faithful to this concrete work?
- **`tNVe`, RAG:** compare a second accepted work scope without assuming the two jobs have interchangeable RAG role requirements.
- **`t7Ay`, RAG:** contains qualifications but **zero direct responsibility claims**; the output must not invent job-specific RAG activities or ownership.

Optionally use `tG9K` with Python to test reuse of existing accepted Capability v9 grouping, but do not make it a substitute for examining the six-job current Market sample.

Run against isolated SQLite copies. Start with one curated selected capability/job pair and a human-readable report before building general generation/persistence. Use local LM Studio only if the actual missing inference requires it; record model, prompt, evidence input, output, and validation separately. No cloud or new acquisition required for this experiment.

## Stage 2 — Behavioral acceptance and boundaries

**Hard reject** any candidate that fabricates direct employer duties, misstates required/preferred depth, asserts unsupported sub-capabilities as job facts, uses a wrong/stale source or claim identity, repeats overlapping evidence as independent demand, or presents unknown as absent.

**Soft uncertainty** is allowed: multiple plausible work implications, limited source detail, unknown production scope, and unreviewed prerequisite ideas should be labeled, lower-confidence, or withheld; do not turn the task into a deterministic proof exercise.

Verify:
- end-to-end correct currentness and exact evidence links;
- explicit fact versus reasoning layers in the output;
- requirement-only case stays requirement-only;
- understandable *what to prepare/check next* for the selected job;
- no duplicated inference when reusable accepted/current Capability already covers an area;
- no unsolicited model/source calls on ordinary read pages, no private material exported;
- count/source denominators, source and Market snapshot histories unchanged;
- normal tests, security, real browser reading, reproducible model identity where invoked.

The user-value test is whether the brief answers a **specific technical capability expectation question** that the existing /compare cannot, not whether a panel looks nicer. Report unmeasured user effort honestly. Any candidate artifacts are explicitly non-authoritative until independently accepted.

## Promotion gates and exclusions

**First deliverable:** one bounded capability-expectation prototype + side-by-side evidence review for the three contrasting RAG cases, including an explicit failure/disposition ledger. The next approval chooses whether to (a) improve the candidate reasoning contract, (b) adopt a read-only presentation, or (c) justify versioned persistent P2.3 profiles. No automatic promotion from three examples to corpus-scale authority.

Not authorized by this planning record: new P2.3 profile tables, mass processing, canonical alias bulk generation, P2.2C/P2.2D archetype promotion, Market-v2 demand statistics, personal-fit scoring, auto-applications, blanket regeneration of old accepted P1.6/Capability artifacts, or another cosmetic UI sprint.

**Recommended next starting task:** Reuse/capability semantic gap audit over `tvMm`, `tNVe`, and `t7Ay`; produce a concrete input/output contract and implement only the first bounded testable case once that contract is approved. This is the next feature increment, not an open-ended UX review.
