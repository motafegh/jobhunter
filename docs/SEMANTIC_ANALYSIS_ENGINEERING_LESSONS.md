# Semantic Analysis Engineering Lessons

**Status:** Living engineering memory  
**Date started:** 2026-08-04  
**Purpose:** Preserve real JobHunter semantic-analysis failures, fixes, rejected approaches, and design lessons so later work does not repeat the same rabbit holes.

This file is not a source of product authority. Controlling behavior remains in the product/domain/architecture/planning documents and tested implementation. This file records **why** some approaches were rejected or constrained.

---

## 1. General rule

When semantic/model behavior fails, classify the problem before changing code:

```text
transport / connectivity
context-window / truncation
structured-output shape
exact evidence grounding
semantic classification
model capability
product-contract mismatch
```

Do not solve one class by weakening another.

Example:

- context truncation is not fixed by changing semantic prompts;
- semantic hallucination is not fixed by increasing `max_tokens`;
- exact-evidence failure is not evidence that source validation should be removed;
- weak product analysis is not necessarily a model failure if the prompt contract explicitly asks for conservative extraction.

---

## 2. LM Studio localhost proxy failure

### Symptom

LM Studio requests returned a Privoxy-related HTTP 500 even though direct `curl --noproxy` calls to the local server succeeded.

### Root cause

HTTPX inherited host proxy environment variables for localhost requests.

### Fix

Local LM Studio HTTPX clients use:

```python
trust_env=False
```

### Do not repeat

Do not treat a localhost provider error as model/server failure until proxy inheritance is ruled out.

---

## 3. Requested `max_tokens` is not loaded context

### Symptom

Analysis still truncated after JobHunter increased `max_tokens` from 8192 to 32768.

### Evidence

LM Studio logs showed:

```text
n_ctx_slot = 4096
prompt + completion reached 4096
finish_reason = length
```

LM Studio model metadata showed:

```text
max_context_length = 131072
loaded_context_length = 4096
```

### Root cause

`max_tokens` is an output request ceiling. It cannot exceed the model instance's loaded total context window.

### Fix

Load the model with a larger context window. A 16K working context was sufficient for the observed JobHunter analysis/repair payloads.

### Do not repeat

Do not keep increasing JobHunter `max_tokens` when LM Studio's loaded context is the actual bottleneck.

---

## 4. Bilingual evidence mixing was structurally wrong

### Early design

One analysis request received:

- original Persian source;
- English translation as comprehension aid;
- requirement to return exact original-source evidence.

### Failure

The small model often reasoned over English and then copied English translation text into the `evidence` field even though original Persian was the authoritative evidence surface.

### Attempted repair

A bounded repair pass removed the English aid and asked the model to re-ground against original Persian only.

### Result

This reduced cross-language contamination but still relied on the model to reproduce exact original-language strings perfectly.

### Final architectural decision

Separate products:

```text
Analyze English
→ English projection only
→ English evidence only

Analyze Original
→ original source only
→ original-language evidence only
```

The two artifacts have different prompt identities and cannot satisfy/reuse each other.

### Do not repeat

Do not ask one structured artifact to reason from one language while citing another language unless a deterministic bilingual span-alignment mechanism exists.

---

## 5. Exact evidence copying is bookkeeping, not intelligence

### Failure pattern

The model understood the role but sometimes:

- synthesized a plausible evidence sentence;
- copied translation instead of source;
- prepended field names such as `education:`;
- changed harmless Unicode/spacing details.

### Lesson

LLMs are useful for semantic interpretation but unreliable as exact Unicode/string-copy machines.

### Current handling

JobHunter preserves fail-closed grounding and uses deterministic normalization/canonicalization only where mechanically provable, including:

- safe `field_name: exact value` removal;
- exact duplicate collapse;
- source-span recovery for harmless whitespace/ZWNJ differences.

Anything not mechanically provable remains invalid.

### Do not repeat

Do not weaken evidence validation merely because the model almost copied the right text.

---

## 6. Manual repair-loop growth became infrastructure debt

### Early implementation

JobHunter manually implemented:

```text
model request
→ JSON Schema validation
→ domain/evidence validation
→ record failed attempt
→ construct repair prompt
→ second model request
→ validate again
```

### Problem

Each new model failure encouraged another repair-specific prompt or heuristic. This was gradually recreating generic structured-LLM infrastructure inside JobHunter.

### Replacement

Instructor + Pydantic now handles:

- typed structured response models;
- JSON-schema response mode;
- runtime validation context;
- validation-feedback retries;
- bounded re-asks.

JobHunter retains domain-specific deterministic rules and final guards.

### Do not repeat

Do not build custom generic LLM repair orchestration when a mature structured-output library already provides it, unless a JobHunter-specific requirement cannot be expressed cleanly.

---

## 7. Duplicate model claims should not spend model calls

### Real failure

The model emitted the same PowerShell requirement twice. The old validator rejected the whole artifact and spent another LLM repair request.

### Lesson

Exact duplicates are deterministic data-cleaning problems.

### Current behavior

Identical normalized claim/type/evidence duplicates are collapsed deterministically before persistence.

### Do not repeat

Do not ask an LLM to repair a defect that deterministic software can prove and fix without changing semantic meaning.

---

## 8. `familiarity` is depth, not optionality

### Real failure

Small Gemma repeatedly mapped phrases such as:

```text
Familiarity with ...
```

to:

```text
preferred
```

### Why this is wrong

`familiarity` describes **technical depth**. `preferred` describes **employer obligation/optionality**.

A posting can require familiarity.

### Contract rule

Keep these axes separate:

```text
requirement strength/optionality
required | preferred | contextual | inferred

technical depth wording
familiarity | proficiency | mastery | expertise | years | ...
```

### Do not repeat

Do not infer `preferred` from low-depth wording alone.

---

## 9. P1.6 became a good extractor because we told it to

### Observed product-quality issue

After evidence grounding and Instructor validation became reliable, accepted English analyses were often close restatements of job-ad sentences.

Example behavior:

```text
Employer:
Mastery of network infrastructure and VPN

P1.6:
Mastery of network infrastructure and VPN required
```

### This was not primarily a bug

The P1.6 contract explicitly emphasized:

- exact evidence;
- omission over uncertain inference;
- no unsupported concepts;
- conservative semantic normalization.

That naturally produces an extraction layer.

### Product correction

Do **not** loosen P1.6 until it starts hallucinating.

Instead separate:

```text
P1.6 factual extraction
        ↓
Capability Intelligence reasoning
```

The second layer is allowed to synthesize, connect facts, decompose capabilities, and infer reasonable prerequisites as long as inference status/evidence/rationale remain explicit.

### Do not repeat

Do not try to force one artifact to be simultaneously:

- exact employer-fact extraction;
- broad technical reasoning;
- career recommendation.

Those have different uncertainty and validation contracts.

---

## 10. Reasoning must be allowed, but labeled

The capability-intelligence layer must not inherit the same anti-inference restrictions as P1.6.

Allowed reasoning statuses:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

Example:

```text
Source:
- VPN/network infrastructure mastery
- troubleshoot connectivity/security incidents

Potential reasoning:
- VPN operations: source_explicit
- VPN troubleshooting: strongly_implied_by_work
- TCP/IP/routing fundamentals: model_inferred_prerequisite
- exact VPN vendor/HA architecture: unknown_or_unsupported
```

This is inference with provenance, not hallucination.

---

## 11. Responsibilities outweigh isolated keyword mentions for practical scope

A tool/technology mention alone usually supports only broad demand.

Example:

```text
Docker required
```

supports little technical decomposition.

But:

```text
Docker required
+ containerize services
+ maintain CI/CD pipelines
+ troubleshoot production deployments
```

can support narrower work expectations such as image/Dockerfile work, runtime configuration, deployment integration, and troubleshooting.

### Do not repeat

Do not generate a technology curriculum from a keyword. Let responsibilities/deliverables determine how far decomposition can defensibly go.

---

## 12. Company context is evidence, not stereotype

Company/product/team descriptions may help interpret actual work context.

They may **not** justify generic stereotypes such as:

```text
startup → broad ownership
enterprise → narrow specialization
security company → every security technique is required
```

Use company context only when combined with explicit role evidence.

---

## 13. Stronger model is an experiment, not an assumption

The configured local analysis model has been a small Gemma model. Some observed semantic mistakes may be model-capability limitations.

If quality remains poor after the capability-intelligence contract is correct, compare stronger models on the **same reviewed jobs** using:

- useful synthesis;
- evidence-status correctness;
- responsibility/requirement interpretation;
- sub-capability precision;
- unsupported inference rate;
- omission rate;
- latency/memory.

Do not assume a larger model is automatically better without side-by-side evidence.

---

## 14. Real failures become regression assets

Every repeatable production/live failure should become one of:

- deterministic unit test;
- integration fixture;
- reviewed acceptance case;
- explicit documented model limitation.

Important existing examples include:

- localhost proxy inheritance;
- LM context-window truncation;
- English evidence in original artifact;
- synthesized evidence;
- duplicate requirements;
- `field_name: value` evidence;
- familiarity/preferred confusion;
- prompt-injection-like source strings;
- extractor-vs-intelligence product mismatch.

---

## 15. Change-control checklist before the next semantic patch

Before changing prompts/models/validators, answer:

1. Is the failure mechanical or semantic?
2. Is it deterministic enough for software to fix safely?
3. Is it caused by the current product contract doing exactly what it says?
4. Would changing P1.6 weaken source truth?
5. Does the failure belong in capability intelligence instead?
6. Is this a model-capability limitation that should be measured rather than patched?
7. Can the failure become a regression test?
8. Does the change require a new prompt/schema/artifact identity?

If those questions are not answered, do not add another prompt rule reflexively.
