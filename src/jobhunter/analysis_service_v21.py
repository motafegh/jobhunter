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
- Preserve obligation from the parent coverage hint. A preferred parent can supply shared
  optionality wording that is outside a narrower item_excerpt; keep that item preferred.
- item_excerpt is candidate validation evidence. JobHunter removes it before unchanged v5
  persistence; parent evidence and exact depth_signal remain the durable factual representation.
- Keep all inherited v20 coverage, source, subject, strength, ontology, and fail-closed rules.
"""

_ENGLISH_SYSTEM_PROMPT_V21 = _ENGLISH_SYSTEM_PROMPT_V20 + _V21_RULES

__all__ = [
    "ENGLISH_PROMPT_VERSION",
    "_ENGLISH_SYSTEM_PROMPT_V21",
    "_V21_RULES",
]
