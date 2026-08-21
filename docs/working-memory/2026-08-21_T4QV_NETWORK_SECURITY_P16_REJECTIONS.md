# t4qV Network/Security P1.6 Heterogeneous Review

Date: 2026-08-21
Status: CLOSED / P1.6 44 ACCEPTED / CAPABILITY 14 ACCEPTED

## Selected chain

```text
job:                 t4qV — Senior Network Security Engineer
source detail:       30
English projection:  20
P1.6 contract:       job-analysis-english-v20 / job-analysis-v5
analysis model:      gemma-4-e4b-it-ud
```

Source-vs-English review found no blocking translation defect for factual extraction. The role stresses enterprise network-security architecture, NGFW/VPN/HA/Zero Trust duties, dense vendor/protocol/tool context, more-than-six-years experience, degree constraints, and explicitly preferred technologies/certifications.

## Rejected candidates

### Artifact 40 — preferred block inflated to required

The section parser matched the inner word `qualifications` inside `Preferred qualifications`, stranded `Preferred` on the preceding responsibility span, and supplied evidence beginning with `include ...`. All preferred technologies/certifications were therefore persisted as required.

Disposition: rejected and archived; no Capability.

General fix: recognize composite optional headings, retain their optionality in the exact evidence span, and carry `preferred` as the coverage obligation.

### Artifact 41 — opening responsibility sentence omitted

Preferred strength and the explicit `more than six years` extent were corrected. Complete review then found that `This position will be responsible for ... implementing security policies` sat outside the recognized responsibility ledger, so security-policy implementation disappeared.

Disposition: rejected and archived; no Capability.

General fixes: preserve lower-bound experience modifiers and recognize explicit position/role responsibility clauses.

### Artifact 42 — domain-specific experience omitted

Both responsibility spans and preferred strength were correct. The opening sentence explicitly required experience designing, implementing, and managing enterprise-scale network-security infrastructure, but the pre-heading sentence was not in the requirement ledger. The generic duration constraint did not preserve that domain-specific experience.

Disposition: rejected and archived; no Capability.

General fix: non-excludable requirement coverage for explicit pre-heading `we are looking/seeking ... with experience in ...` candidate clauses.

### Artifact 43 — certification ontology crossed the role-level boundary

Artifact 43 achieved complete source coverage:

- required enterprise network-security experience;
- exact `more than six years` bound;
- required degree and structured skills;
- ten source-grounded responsibilities across both exact spans;
- eight explicitly preferred technologies/certifications.

However, CCNP Security, CCIE Security, PCNSE, Fortinet FCP/FCSS, and JNCIS/JNCIP were persisted as `concept_type=skill` rather than credential/education facts. Capability would therefore group preferred certifications as capability skills instead of preserving them as role-level constraints.

Disposition: rejected and archived; no Capability.

## Boundary decision and accepted result

No vacancy-specific or vendor-acronym prompt/validator patch was added. The general ontology rule was clarified instead:

- formal certifications, licenses, and named certification awards are credential facts;
- they use `concept_type=education`, even when abbreviated or mixed with technologies;
- an unfamiliar name is not guessed to be a credential without semantic or source evidence.

Rebuilt P1.6 artifact 44 then passed complete review with 15 requirements, 10 responsibilities, correct preferred strength, exact more-than-six-years experience, three preferred tools, five preferred credentials, the degree and four structured skills. Artifact 44 was explicitly accepted.

Capability v9 artifact 14 then passed review on exact dependencies P1.6 44 / translation 20:

```text
capability requirements:  9/9
responsibilities:         10/10
explicit depth:            1/1
role-level requirements:  five certifications + Bachelor's degree
```

The network/security heterogeneous anchor is accepted and closed.
