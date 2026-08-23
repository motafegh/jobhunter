# P2.1D small canonical-registry seed — review candidate

Date: 2026-08-23
Status: **SEMANTIC REVIEW CANDIDATE / NOT YET APPLIED**

## 1. Purpose

P2.1A, P2.1B, and P2.1C are accepted. P2.1D must now prove the canonical registry on a deliberately small real-data seed without turning the accepted P1.6 corpus into an automatic taxonomy-generation exercise.

This record proposes the smallest useful seed found after inspecting the exact accepted/current P1.6 artifacts for all five accepted chains:

```text
tG9K → artifact 36
t4jp → artifact 37
tmBK → artifact 39
t4qV → artifact 44
tmyX → artifact 46
```

No registry mutation is authorized by this file. The decisions below require explicit human/semantic review before application because claim mappings are immutable once recorded.

## 2. Candidate canonical concepts

### 2.1 `platform:linux`

Preferred label: `Linux`

Reason:

- `tG9K` artifact 36 requirement `[12]` is the exact structured requirement `Linux`;
- `tmBK` artifact 39 requirement `[3]` is `Linux operating system` with source depth `Familiarity`;
- the shared identity is the Linux operating-system platform;
- source-specific depth remains attached to the source claim and must not become part of the canonical concept.

### 2.2 `tool:powershell`

Preferred label: `PowerShell`

Reason:

- `tmyX` artifact 46 requirement `[11]` is the exact structured requirement `PowerShell`;
- this is a clean tool identity with no need to import the broader source-specific mastery/use context into the canonical concept.

### 2.3 `education_credential:ccnp-security`

Preferred label: `CCNP Security`

Reason:

- `t4qV` artifact 44 requirement `[4]` is `CCNP Security`;
- accepted P1.6 explicitly classifies the claim as education/certification;
- its `preferred` requirement strength remains source truth and is not encoded in the canonical credential identity.

### 2.4 `responsibility:manage-next-generation-firewalls`

Preferred label: `Manage next-generation firewalls`

Reason:

- `t4qV` artifact 44 responsibility `[1]` is `Managing next-generation firewalls`;
- the canonical label performs only grammatical normalization and adds no lifecycle, ownership, architecture, or autonomy claim;
- the mapping remains tied to the exact source-backed responsibility.

## 3. Candidate reviewed alias

Alias:

```text
Linux operating system
→ platform:linux
```

Provenance:

```text
kind:      accepted_p16_claim
reference: job=tmBK;analysis_artifact=39;claim=requirement[3]
```

Reason:

`Linux operating system` is the exact accepted P1.6 concept wording in `tmBK`. It is a direct wording variant of the reviewed `Linux` platform identity. The source `Familiarity` depth is not part of the alias.

## 4. Candidate claim decisions

| Job | Artifact | Claim | Exact accepted P1.6 text | Candidate decision |
| --- | ---: | --- | --- | --- |
| `tG9K` | 36 | requirement `[12]` | `Linux` | mapped → `platform:linux` |
| `tmBK` | 39 | requirement `[3]` | `Linux operating system` | mapped → `platform:linux` |
| `t4jp` | 37 | requirement `[4]` | `Creativity in creating visual and video content` | **unmapped** |
| `t4qV` | 44 | requirement `[4]` | `CCNP Security` | mapped → `education_credential:ccnp-security` |
| `t4qV` | 44 | responsibility `[1]` | `Managing next-generation firewalls` | mapped → `responsibility:manage-next-generation-firewalls` |
| `tmyX` | 46 | requirement `[11]` | `PowerShell` | mapped → `tool:powershell` |

This uses every accepted chain while keeping the seed to six claim decisions.

## 5. Why `t4jp` requirement `[4]` should remain unmapped

Accepted claim:

```text
Creativity in creating visual and video content
concept_type: other
```

The current canonical-registry categories have no explicit trait/personality category. Mapping this to `skill` merely to avoid an unmapped result would change the ontology rather than record correspondence.

Candidate decision:

```text
unmapped
```

Review rationale:

```text
Trait-like creativity requirement has no appropriate current canonical category. Preserve the
accepted source claim explicitly unmapped rather than forcing it into skill/knowledge taxonomy.
Revisit only if a later evidence-backed taxonomy change introduces a suitable category.
```

This is the required deliberate ambiguous/unmapped seed case.

## 6. Required-case coverage

The candidate seed satisfies the P2.1D shape without bulk mapping:

```text
all five accepted chains        yes
reviewed alias                  Linux operating system → platform:linux
ambiguous/unmapped case         t4jp requirement[4]
responsibility mapping          t4qV responsibility[1]
education/credential signal     t4qV requirement[4] → CCNP Security
cross-role canonical identity   Linux across tG9K + tmBK
additional clean tool identity  PowerShell from tmyX
```

## 7. Exact application commands after human review

Do **not** run these until the candidate decisions above are explicitly accepted for P2.1D.

Create concepts:

```bash
jobhunter-registry concepts add platform:linux \
  --category platform \
  --label "Linux" \
  --reason "Reviewed from accepted P1.6 artifact 36 requirement[12] and artifact 39 requirement[3]; shared Linux platform identity without source-specific depth."

jobhunter-registry concepts add tool:powershell \
  --category tool \
  --label "PowerShell" \
  --reason "Reviewed from accepted P1.6 artifact 46 requirement[11] as the canonical PowerShell tool identity."

jobhunter-registry concepts add education_credential:ccnp-security \
  --category education_credential \
  --label "CCNP Security" \
  --reason "Reviewed from accepted P1.6 artifact 44 requirement[4], explicitly classified as a preferred certification/education claim."

jobhunter-registry concepts add responsibility:manage-next-generation-firewalls \
  --category responsibility \
  --label "Manage next-generation firewalls" \
  --reason "Reviewed from accepted P1.6 artifact 44 responsibility[1]; grammatical normalization only, with exact source wording retained by the mapping."
```

Add alias:

```bash
jobhunter-registry aliases add platform:linux "Linux operating system" \
  --provenance accepted_p16_claim \
  --reference "job=tmBK;analysis_artifact=39;claim=requirement[3]" \
  --reason "Exact accepted tmBK P1.6 concept wording reviewed as an alias of Linux; Familiarity remains source depth rather than canonical identity."
```

Record claim decisions:

```bash
jobhunter-registry claims decide tG9K requirement 12 mapped \
  --concept platform:linux \
  --reason "Exact accepted P1.6 Linux requirement corresponds to the reviewed Linux platform concept."

jobhunter-registry claims decide tmBK requirement 3 mapped \
  --concept platform:linux \
  --reason "Exact accepted P1.6 Linux operating system requirement corresponds to Linux; Familiarity remains source depth."

jobhunter-registry claims decide t4jp requirement 4 unmapped \
  --reason "Trait-like creativity requirement has no appropriate current canonical category; preserve it unmapped rather than forcing a skill/knowledge classification."

jobhunter-registry claims decide t4qV requirement 4 mapped \
  --concept education_credential:ccnp-security \
  --reason "Exact accepted P1.6 CCNP Security certification corresponds to the reviewed credential; preferred strength remains source metadata."

jobhunter-registry claims decide t4qV responsibility 1 mapped \
  --concept responsibility:manage-next-generation-firewalls \
  --reason "Exact accepted responsibility Managing next-generation firewalls corresponds to the reviewed responsibility concept without added scope."

jobhunter-registry claims decide tmyX requirement 11 mapped \
  --concept tool:powershell \
  --reason "Exact accepted P1.6 PowerShell structured requirement corresponds to the reviewed PowerShell tool concept."
```

## 8. Acceptance sequence after application

1. Inspect `jobhunter-registry concepts list` and each seeded concept detail.
2. Inspect `jobhunter-registry claims list --state mapped` and `--state unmapped` for the exact six decisions.
3. Re-run the exact concept/alias/mapping commands and verify existing identities/decision IDs are reused rather than duplicated.
4. Verify the current review reader reports these mappings as current.
5. Exercise the stale-dependency boundary in deterministic tests without mutating the accepted production chain.
6. Run:

```text
ruff check .
pytest
pytest -W error
```

7. Only then decide whether P2.1 closes.
8. Registry publication remains a separate privacy/source decision; no `corpus/` registry projection is implied by this seed.
