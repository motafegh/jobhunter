"""Bounded candidate interpretation contract for target-market membership."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

MARKET_MEMBERSHIP_CONTRACT_VERSION = "market-membership-v1"
MARKET_MEMBERSHIP_PROMPT_VERSION = "market-membership-v1.0"

EvidenceRef = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class MarketMembershipDecision(BaseModel):
    """An interpretation, never employer wording or promoted role taxonomy."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    disposition: Literal["core_match", "adjacent_match", "uncertain", "excluded"]
    reason: str = Field(min_length=1, max_length=1200)
    evidence_refs: list[EvidenceRef] = Field(min_length=1, max_length=12)
    confidence: Literal["high", "medium", "low"]
