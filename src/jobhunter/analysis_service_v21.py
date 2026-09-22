"""Prompt identity for the isolated P1.6 v21 scoped-evidence candidate."""

from jobhunter.analysis_service_v20 import _ENGLISH_SYSTEM_PROMPT_V20

ENGLISH_PROMPT_VERSION = "job-analysis-english-v21-candidate"

_V21_RULES = """

P1.6 V21 CANDIDATE — EXACT ITEM SCOPE WITH PARENT COVERAGE:
- Every requirement must keep evidence equal to its supplied parent requirement_coverage text.
- Every requirement must also provide item_excerpt as one exact contiguous subspan of that parent
  containing the source wording for this concept. Do not paraphrase, join, or reconstruct it.
- Decide depth_signal only from item_excerpt. Supply the exact applicable marker when the item has
  one. Use null when this exact item has no accepted depth marker, even if neighboring items in the
  parent have markers. Never borrow neighboring depth.
- Keep depth wording out of concept. If the exact item starts with one source marker, JobHunter may
  materialize that one marker into depth_signal even when the generated concept uses wording such
  as "Working with X". If the concept itself starts with the same generated wrapper, JobHunter may
  also remove that wrapper and retain X as the concept.
- When one leading marker scopes a coordinated list (for example "familiarity with RAG, Embedding,
  and Vector Databases"), item_excerpt must retain that exact complete scoped phrase for every
  separately emitted concept. Do not reconstruct "familiarity with Embedding" or cite bare
  "Embedding" while claiming familiarity. The same exact group excerpt may support multiple
  concepts when the employer grammar applies the shared marker to all of them.
- Preserve obligation from the parent coverage hint. A preferred parent can supply shared
  optionality wording that is outside a narrower item_excerpt; keep that item preferred.
- item_excerpt is candidate validation evidence. JobHunter removes it before unchanged v5
  persistence; parent evidence and exact depth_signal remain the durable factual representation.
- Explicit headingless candidate-experience references may be supplied in their own partition so
  dense section decomposition and duty output cannot crowd them out. Every such supplied reference
  is a mandatory candidate qualification and must be represented; it cannot be excluded.
- When candidate_fact_coverage is supplied, represent every listed exact item_excerpt separately.
  Use that exact excerpt rather than the whole parent or a narrower neighboring phrase. Preserve a
  supplied required_concept_type=experience for explicit prior applied exposure.
- Keep requirement evidence equal to candidate_fact_coverage.parent_reference's full supplied
  parent text. If evidence is instead the same exact unique checklist text as item_excerpt,
  JobHunter may restore its one source-proven parent; ambiguous or unknown items remain invalid.
- Keep all inherited v20 coverage, source, subject, strength, ontology, and fail-closed rules.
"""

_ENGLISH_SYSTEM_PROMPT_V21 = _ENGLISH_SYSTEM_PROMPT_V20 + _V21_RULES

__all__ = [
    "ENGLISH_PROMPT_VERSION",
    "_ENGLISH_SYSTEM_PROMPT_V21",
    "_V21_RULES",
]
