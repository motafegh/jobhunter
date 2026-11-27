"""R4 evidence ownership seam, not a V5 requirement or production route."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from jobhunter.p16_lab import canonical, digest
from jobhunter.translation_store import TranslationSourceVersion


@dataclass(frozen=True, slots=True)
class BoardSkillObservation:
    source_job_id: str
    job_detail_version_id: int
    source_semantic_sha256: str
    selector: str
    value: str
    field_json_sha256: str
    selected_value_json_sha256: str
    authority: str = "structured_job_board_metadata_not_employer_prose"
    employer_obligation: str = "not_established"
    depth_signal: None = None


def board_skill_observations(source: TranslationSourceVersion) -> tuple[BoardSkillObservation, ...]:
    """Bind original structured tags, retaining duplicates and exact value/index.

    This records metadata, not a technical prerequisite or proficiency degree.
    It does not translate tags or compare their semantics to employer prose.
    """
    if (
        not source.source_job_id
        or type(source.job_detail_version_id) is not int
        or source.job_detail_version_id <= 0
        or not re.fullmatch(r"[0-9a-f]{64}", source.semantic_sha256)
    ):
        raise ValueError("invalid source identity")
    skills = source.fields.get("skills")
    if skills is None:
        return ()
    if not isinstance(skills, list) or any(not isinstance(v, str) or not v.strip() for v in skills):
        raise ValueError("malformed original board skills")
    field_hash = digest(canonical(skills))
    return tuple(
        BoardSkillObservation(
            source.source_job_id,
            source.job_detail_version_id,
            source.semantic_sha256,
            f"/skills/{index}",
            value,
            field_hash,
            digest(canonical(value)),
        )
        for index, value in enumerate(skills)
    )


def separate_board_skills(
    source: TranslationSourceVersion, analysis_fields: dict[str, Any]
) -> tuple[dict[str, Any], tuple[BoardSkillObservation, ...]]:
    """Separate board evidence without touching prose or inferring translation links.

    The caller must establish the L0 projection association separately. The
    projection tag list can differ in language; no index-level translation
    equivalence is claimed here. A1 integration must retain the original
    observations in the candidate envelope, not the accepted V5 schema.
    """
    observations = board_skill_observations(source)
    model_fields = dict(analysis_fields)
    model_fields.pop("skills", None)
    return model_fields, observations


def verify_board_observations(source: TranslationSourceVersion, records: list[dict]) -> None:
    if records != [asdict(o) for o in board_skill_observations(source)]:
        raise ValueError("stale, missing or altered board observations")
