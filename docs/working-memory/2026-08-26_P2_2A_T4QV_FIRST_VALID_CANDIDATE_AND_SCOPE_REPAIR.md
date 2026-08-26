# P2.2A `t4qV` First Valid Candidate and Semantic Scope Repair

**Date:** 2026-08-26  
**Status:** P2.2A live semantic/product acceptance in progress  
**Scope:** first structurally valid real `t4qV` Job Work Intelligence candidate, semantic review, and bounded v1.1 repair  
**Authority:** subordinate to `AGENTS.md`, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, and `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

## 1. Context

The first real `t4qV` generation attempt previously failed because the model placed accepted responsibility indices only inside prose rationales while omitting the dedicated structured provenance arrays. That schema contradiction was repaired by making the reference arrays required in the generation schema without weakening the invariant that every work theme must own direct accepted work evidence.

After pulling that repair, the user reran:

```bash
python -m jobhunter.work_intelligence_cli generate t4qV
```

The run succeeded and persisted the first real candidate:

```text
source job:        t4qV
artifact:          1
semantic state:    candidate
work evidence:     sufficient
model:             gemma-4-e2b-it
P1.6 dependency:   artifact 44
work themes:       4
```

This proves the structured-reference repair worked in the actual LM Studio path.

## 2. First valid candidate output

The candidate summarized the role as centered on design, implementation, management, and operational support of large-scale network-security infrastructure and grouped work into:

1. `Security Architecture and Design` — primary/high;
2. `Firewall and VPN Management` — primary/high;
3. `Policy Implementation and Operations` — primary/high;
4. `Technical Documentation` — supporting/high.

This is materially more useful than a flat ten-responsibility list and confirms the basic P2.2A product direction is viable.

## 3. Accepted `t4qV` factual substrate checked during review

The public accepted P1.6 artifact 44 contains:

- required experience designing, implementing, and managing network-security infrastructures at Enterprise scale;
- ten accepted responsibilities including security-solution design/execution, NGFW management, security-policy implementation, network-security architecture, VPNs, High Availability, troubleshooting, Zero Trust/segmentation, and technical documentation;
- preferred/required supporting technologies and credentials including Cisco-family items, PCNSE, Fortinet FCP/FCSS, and other security credentials;
- a broad responsibility evidence sentence whose equipment examples appear grammatically after the technical-documentation clause and include Cisco, Palo Alto, Fortinet, Juniper, and other security technologies.

Important semantic consequence:

```text
vendor/equipment name appears somewhere in accepted shared evidence
!=
that vendor/equipment is automatically in scope for every responsibility sharing that evidence
```

The accepted responsibility statement remains the primary bounded work claim.

## 4. Semantic findings

### 4.1 Useful grouping — positive

The four-theme structure is coherent and substantially reduces manual synthesis effort. Architecture/design, firewall/VPN work, policy/operations, and documentation are all supported work areas.

The candidate therefore should not be discarded merely because some interpretive wording needs refinement.

### 4.2 Repeatable unsupported lifecycle inflation — material defect

The valid candidate stated:

```text
end-to-end design, implementation, management, and operational support
```

and later:

```text
across the entire security stack
```

`end-to-end` had also appeared in both structurally rejected generations before this candidate. It is therefore repeatable model behavior, not a one-off wording variation.

The accepted P1.6 direct-work statements do not say `end-to-end`, `full lifecycle`, `entire lifecycle`, or `entire security stack`.

This matters because P2.2A explicitly permits semantic synthesis but does not permit invented lifecycle/ownership scope. The problem is not that the model paraphrased; the problem is that the paraphrase strengthened scope beyond the direct work claim.

### 4.3 Shared-evidence scope transfer — real risk

The `Firewall and VPN Management` theme said the job includes managing specific Cisco, Palo Alto, and Fortinet platforms.

Those vendor names are not hallucinated: they exist in accepted/source evidence. However, the long accepted evidence sentence lists equipment after the documentation clause, while the direct accepted management responsibility is simply `Managing NGFW equipment`.

Therefore P2.2A must not automatically transfer every example/entity present in a shared evidence sentence into every responsibility that cites the same evidence.

This is a general semantic-boundary issue, not a `t4qV`-specific prompt patch.

## 5. Repair decision

The smallest general repair is implemented without weakening semantic reasoning.

### 5.1 Prompt identity

```text
contract:       job-work-intelligence-v1
schema:         job-work-intelligence-v1
prompt version: job-work-intelligence-v1.1
```

Only the prompt identity changes. The typed schema contract remains v1.

The identity bump is required so artifact 1 remains immutable historical evidence and is not silently reused after the semantic contract changes.

### 5.2 Statement-versus-shared-evidence boundary

The v1.1 prompt now tells the model:

- responsibility/role-purpose `statement` defines the accepted work claim;
- `evidence` may contain neighboring clauses/examples because multiple accepted claims can share a source sentence;
- details from one neighboring clause must not silently broaden a different responsibility;
- supporting requirements remain context only and cannot independently manufacture duties.

This is deliberately general and not vacancy-specific.

### 5.3 Unsupported scope-intensifier guard

A small deterministic post-validation guard now rejects unsupported lifecycle/scope intensifiers such as:

```text
end-to-end
full lifecycle
whole/entire/complete lifecycle
entire/whole security stack
```

The guard is conditional:

```text
intensifier appears in generated interpretive summary
AND
intensifier is absent from accepted direct responsibility/role-purpose statements
→ reject candidate before persistence
```

If the employer's accepted direct work statement explicitly contains the scope wording, the wording remains allowed.

This preserves the revised governance principle:

```text
determinism protects authority boundaries
!=
determinism chooses semantic wording
```

The validator does not require exact theme labels or phrasing and does not canonicalize interpretation.

## 6. Regression evidence

Added regression coverage proves:

1. unsupported `end-to-end` in candidate interpretation is rejected when direct work does not state it;
2. source-explicit `end-to-end` remains allowed;
3. Work Intelligence prompt identity is now `job-work-intelligence-v1.1`.

The implementation commit itself passed the full repository quality gates. The final regression/style commit also passed:

```text
Ruff                 PASS
full pytest           PASS
pytest -W error       PASS
```

No local rerun of repository quality gates is required from the user for this repair.

## 7. Artifact/currentness consequence

Local artifact 1 remains preserved under the historical prompt identity:

```text
job-work-intelligence-v1
```

The current service now looks for:

```text
job-work-intelligence-v1.1
```

Therefore artifact 1 will not be silently reused as the current candidate after the user pulls the repair.

This is expected historical/currentness behavior, not deletion or mutation.

## 8. Exact next action

Pull current `main` and rerun only the real `t4qV` generation:

```bash
git pull --ff-only origin main
source .venv/bin/activate
python -m jobhunter.work_intelligence_cli generate t4qV
```

Then inspect the new candidate for:

- removal of unsupported lifecycle/scope inflation;
- work-theme usefulness;
- whether shared evidence still broadens responsibility scope;
- deliverables when genuinely supported;
- candidate role interpretation when useful;
- confidence/emphasis quality;
- overall reduction in manual reading/synthesis effort.

Do not demand exact wording equality with earlier candidates.

## 9. Stop lines preserved

This repair does not authorize:

- P2.2A acceptance yet;
- P2.2B responsibility promotion;
- global responsibility families/archetypes;
- Market v2;
- personal scoring/recommendations;
- P2.2 public-corpus publication;
- reopening accepted P1.6 artifact 44 merely because P2.2A interpretation needed refinement.
