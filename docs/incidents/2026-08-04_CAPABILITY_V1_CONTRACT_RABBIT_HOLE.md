# Capability Intelligence v1 contract rabbit hole

**Date:** 2026-08-04  
**Status:** Corrected by `job-capability-intelligence-v2`

## What kept happening

Live Capability Intelligence runs repeatedly reached the model successfully, produced useful
reasoning, and then failed because the v1 contract mixed semantic reasoning with exact-output
bookkeeping.

Observed failure classes included:

1. the model joined or abbreviated real source passages in `evidence[]`, so exact-quote validation
   failed even though the analytical conclusion was reasonable;
2. Instructor spent a complete second generation repairing quotation formatting;
3. the repair could then introduce a different bookkeeping error, such as placing a derived depth
   conclusion inside `employer_stated_depth`;
4. the whole artifact was rejected even though most of the semantic analysis was usable;
5. long local generations were also initially cut off by generic 30-second, then 120-second read
   deadlines that were not appropriate for multi-thousand-token local reasoning.

The `tajz` live run made the core problem especially clear. Generation 1 failed because the model
abbreviated a company-description quote. Generation 2 corrected that evidence but then produced a
valid derived conclusion inside the employer-only depth bucket. The retry therefore changed the
bookkeeping failure rather than improving the role reasoning.

## Root cause

Capability Intelligence v1 asked the LLM to perform too many mechanically exact jobs at once:

```text
reason about the role
+ classify inference strength
+ choose the exact schema section
+ reproduce exact source quotation text
+ preserve exact punctuation/contiguity
```

The first two are appropriate probabilistic tasks. The last three are largely deterministic
bookkeeping tasks and should not consume a full model retry when JobHunter can own them.

A second contract problem was that `employer_stated_depth` encoded both *where a conclusion lived*
and *whether it was explicit*. That duplicated information already represented by
`evidence_status` and created unnecessary cross-field validation failures.

## v2 correction

`job-capability-intelligence-v2` changes the division of responsibility.

### Evidence references instead of quote copying

JobHunter builds a deterministic evidence catalog from:

- the exact hardened English source fields;
- accepted P1.6 role-purpose evidence;
- accepted P1.6 responsibility evidence;
- accepted P1.6 requirement evidence.

The model receives stable identifiers such as:

```text
p1:requirements:0
p1:responsibilities:2
field:company_description
field:minimum_experience
```

The model puts those identifiers in `evidence[]`. Pydantic/JobHunter resolves the identifiers back
to exact source text before the artifact is persisted. Historical/test callers that provide an
already-exact source excerpt remain supported as a fallback.

This preserves exact traceability while removing quotation transcription from the LLM's job.

### Depth signals instead of employer-only depth bucket

The v1 `employer_stated_depth` field is replaced by `depth_signals`.

A depth signal may be:

- `source_explicit`;
- `strongly_implied_by_work`;
- `model_inferred_prerequisite`.

The status carries the provenance. The section no longer duplicates that provenance rule.

### Mechanically recoverable unknown placement

When the model places an `unknown_or_unsupported` item in another analytical section, JobHunter
moves it to `unknown_scope` without changing the statement, rationale, evidence, or confidence.
Likewise, an item already inside `unknown_scope` is normalized to the section's implied unknown
status. These are section-bookkeeping repairs, not semantic rewrites.

### No long-form read deadline

Capability Intelligence and Role Capability Blueprint now use:

```text
connect timeout: bounded
read timeout: none
transport replay: disabled
```

Once LM Studio is connected and actively generating, JobHunter does not impose an arbitrary
30/120-second deadline. Users can still stop the local operation/process manually. `max_tokens`
and structured response bounds remain the actual generation bounds.

## Permanent lesson

Do not make a probabilistic model repeatedly solve deterministic bookkeeping problems.

For JobHunter semantic layers:

```text
LLM
→ reasoning / interpretation / classification

JobHunter deterministic code
→ source identity
→ evidence resolution
→ provenance linkage
→ exact text recovery
→ stale dependency checks
→ duplicate handling
→ section bookkeeping that is mechanically implied
```

A model retry should be reserved for a genuinely invalid completed semantic/structural response,
not punctuation, quotation transcription, or redundant ontology constraints.
