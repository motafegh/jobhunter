# tmyX Operations/Platform P1.6 and Capability Acceptance

Date: 2026-08-21
Status: CLOSED / P1.6 46 ACCEPTED / CAPABILITY 15 ACCEPTED

## Selection

The first nominal DevOps candidate, `t49N` (Cloud Security Engineer), was blocked before P1.6 because English projection artifact 17 has a material field-association failure: education, employment type, gender, location, military service, experience, salary, and skills are shifted across fields. Downstream analysis must not hide that translation defect.

`tmyX` was selected as the valid operations/platform anchor:

```text
job:                 Infrastructure and Microsoft Services Security Specialist
source detail:       35
English projection:  24
category:             IT / DevOps / Server
P1.6 contract:       job-analysis-english-v20 / job-analysis-v5
```

Its source exercises Windows infrastructure, Active Directory and related services, hardening standards, PowerShell audit automation, tickets, SIEM/EDR, documentation, explicit Mastery/Familiarity wording, and structured experience/education.

## Deterministic incidents

The first run failed safely because the generic heading matcher split `communicate security requirements to technical teams` at the ordinary word `requirements`, creating a stranded `to technical teams.` coverage item. Generic headings now require heading-like punctuation/context, while composite required/preferred headings remain recognized. Regression coverage preserves the complete qualification span.

P1.6 artifact 45 then covered 13 requirements and five listed duties but omitted the explicit opening role clause: assess server/Microsoft-service security posture and develop security requirements, best practices, and hardening solutions. Artifact 45 was rejected and archived. A general pre-heading `we are looking/seeking ... to ...` duty rule now makes such explicit role actions non-optional coverage.

The next run failed without persistence because the model repeatedly used ordinary `Ability to ...` and `Skill in ...` wording as technical depth. V20 now clears those exact application/capability phrases only when the cited evidence contains no genuine depth marker; mixed real depth still fails closed. Regression coverage includes both patterns.

## Accepted chain

P1.6 artifact 46 passed complete source review:

```text
role purpose:            1
requirements:           13
responsibilities:        5
structured skills:       3/3
explicit depth facts:    6
```

Mastery applies only to Windows Server hardening/services, Active Directory security concepts, and PowerShell use. Familiarity applies only to hardening standards and SIEM/EDR evidence analysis. The three-to-six-years extent is role-level experience. Ordinary ability/skill wording has no fabricated depth.

Capability v9 artifact 15 then passed review on exact dependencies P1.6 46 / translation 24:

```text
capability requirements:       11/11
responsibilities:               5/5
capability explicit depth:      5/5
all explicit depth:             6/6
role-level requirements:        experience + Bachelor's degree
```

The four groups are coherent, source links are complete, overlaps remain bounded, and unsupported optional enrichment was discarded fail-closed. The operations/platform heterogeneous anchor is accepted and closed.

## Resulting gate

Python/software, network/security, and operations/platform heterogeneous semantic validation are all closed. The next controlling Phase-1 gate is Market truthfulness and sampling, followed by source/lifecycle acceptance, partial-success semantics, and P1.7 report/run/browser acceptance.
