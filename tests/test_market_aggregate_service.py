from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.canonical_registry import CanonicalRegistryStore
from jobhunter.market_aggregate_service import MarketAggregateService
from jobhunter.market_membership_models import MARKET_MEMBERSHIP_CONTRACT_VERSION
from jobhunter.market_models import MarketDefinitionSpec, MarketSnapshotMemberInput
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 17, 12, tzinfo=UTC)
_MODEL = "analysis-model"


class Harness:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.now = _NOW
        self.source = JobHunterStore(database_path)
        self.source.initialize()
        self.market = MarketStore(database_path)
        self.translations = TranslationStore(database_path)
        self.analyses = AnalysisStore(database_path)
        self.translation_service = TranslationService(
            store=self.translations,
            provider=None,
            clock=lambda: self.now,
        )
        self.registry = CanonicalRegistryStore(database_path)
        target = self.market.create_target(
            slug="applied-ai",
            name="Applied AI",
            description=None,
            created_at=self.now,
        )
        self.definition = self.market.create_definition_version(
            target.id,
            spec=MarketDefinitionSpec(
                membership_intent="Applied AI engineering; enabling backend is adjacent.",
                search_catalog_version="fixture-v1",
            ),
            created_at=self.now,
        )

    def seed_source(
        self,
        job_id: str,
        *,
        company: str | None,
        version: int = 1,
        location: str = "Tehran",
    ) -> tuple[int, int]:
        posting = self.source.upsert_job(
            job=DiscoveredJobLink(
                source_job_id=job_id,
                company_slug=f"slug-{job_id}",
                canonical_url=f"https://jobinja.ir/companies/fixture/jobs/{job_id}/role",
                observed_text="Applied AI Engineer",
            ),
            observed_at=self.now,
        )
        fields = {
            "title": "Applied AI Engineer",
            "description": "Build production AI systems.",
            "language": "en",
            "location": location,
            "employment_type": "Full time",
            "minimum_experience": "3 years",
            "education": "Bachelor",
            "job_category": "Engineering",
        }
        if company is not None:
            fields["company"] = company
        detail = self.source.record_job_detail(
            job_posting_id=posting.job_posting_id,
            fetched_at=self.now,
            requested_url=f"https://jobinja.ir/jobs/{job_id}",
            final_url=f"https://jobinja.ir/jobs/{job_id}",
            status_code=200,
            content_sha256=f"raw-{job_id}-{version}",
            semantic_sha256=f"semantic-{job_id}-{version}",
            evidence_path=Path(f"{job_id}-{version}.html"),
            metadata_path=Path(f"{job_id}-{version}.json"),
            parser_version="jobinja-detail-v2",
            parse_status="parsed",
            fields=fields,
        )
        translation = self.translation_service.translate_job(job_id)
        return detail.version_id, translation.artifact_id

    def analysis(
        self,
        detail_id: int,
        translation_id: int,
        *,
        requirements: list[dict],
        responsibilities: list[dict],
        status: str = "accepted",
    ) -> int:
        return self.analyses.record_artifact(
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            model=_MODEL,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            analysis={
                "role_purpose": [],
                "requirements": requirements,
                "responsibilities": responsibilities,
            },
            request_body={},
            raw_response={},
            created_at=self.now,
            semantic_review_status=status,
        )

    def membership(
        self,
        detail_id: int,
        *,
        disposition: str,
        translation_id: int | None,
        analysis_id: int | None,
        identity: str,
    ):
        return self.market.record_membership(
            target_definition_version_id=self.definition.id,
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            analysis_artifact_id=analysis_id,
            classifier_contract_version=MARKET_MEMBERSHIP_CONTRACT_VERSION,
            classifier_method="model",
            classifier_identity={"provider": "fixture", "model": identity},
            disposition=disposition,
            reason="Fixture membership decision.",
            evidence_refs=("source:description",),
            confidence="high",
            created_at=self.now,
        )

    def snapshot(self, members: tuple[MarketSnapshotMemberInput, ...]):
        run = self.market.start_run(
            self.definition.id,
            controls={"fixture": True},
            started_at=self.now,
        )
        run = self.market.finish_run(
            run.id,
            status="completed",
            ledger={"fixture": "complete"},
            completed_at=self.now,
        )
        return self.market.record_snapshot(
            target_definition_version_id=self.definition.id,
            run_id=run.id,
            freshness_rule=self.definition.spec.freshness_rule,
            source_scope={"source": "jobinja", "fixture": True},
            metadata={"fixture": True},
            members=members,
            created_at=self.now,
        )

    def aggregate(self) -> MarketAggregateService:
        return MarketAggregateService(
            database_path=self.database_path,
            market_store=self.market,
            analysis_store=self.analyses,
            clock=lambda: self.now,
        )


def requirement(
    concept: str,
    *,
    concept_type: str = "skill",
    strength: str = "required",
    depth: str | None = None,
    evidence: str | None = None,
) -> dict:
    return {
        "concept": concept,
        "concept_type": concept_type,
        "requirement_type": strength,
        "depth_signal": depth,
        "evidence": evidence or concept,
        "confidence": "high",
        "rationale": "fixture",
    }


def responsibility(statement: str) -> dict:
    return {
        "statement": statement,
        "evidence": statement,
        "confidence": "high",
        "rationale": "fixture",
    }


@pytest.fixture
def h(tmp_path: Path) -> Harness:
    return Harness(tmp_path / "jobhunter.sqlite3")


def test_profile_uses_explicit_source_and_semantic_denominators(h: Harness) -> None:
    a_detail, a_translation = h.seed_source("a", company="Alpha")
    a_analysis = h.analysis(
        a_detail,
        a_translation,
        requirements=[
            requirement("Python", strength="required", depth="Expert"),
            requirement("Python", strength="preferred"),
            requirement("SQL", concept_type="tool"),
        ],
        responsibilities=[
            responsibility("Build ML models."),
            responsibility("Build ML models."),
        ],
    )
    a = h.membership(
        a_detail,
        disposition="core_match",
        translation_id=a_translation,
        analysis_id=a_analysis,
        identity="a",
    )

    b_detail, b_translation = h.seed_source("b", company="Alpha")
    b_analysis = h.analysis(
        b_detail,
        b_translation,
        requirements=[requirement("Python", strength="required")],
        responsibilities=[responsibility("Validate ML models.")],
    )
    b = h.membership(
        b_detail,
        disposition="core_match",
        translation_id=b_translation,
        analysis_id=b_analysis,
        identity="b",
    )

    c_detail, c_translation = h.seed_source("c", company="Beta")
    c = h.membership(
        c_detail,
        disposition="core_match",
        translation_id=c_translation,
        analysis_id=None,
        identity="c",
    )

    d_detail, d_translation = h.seed_source("d", company="Gamma")
    d_analysis = h.analysis(
        d_detail,
        d_translation,
        requirements=[requirement("Python")],
        responsibilities=[responsibility("Build ML models.")],
    )
    d = h.membership(
        d_detail,
        disposition="adjacent_match",
        translation_id=d_translation,
        analysis_id=d_analysis,
        identity="d",
    )

    snapshot = h.snapshot(
        (
            MarketSnapshotMemberInput(
                a.id, "accepted", a_translation, a_analysis, {"lifecycle_state": "active"}
            ),
            MarketSnapshotMemberInput(
                b.id, "accepted", b_translation, b_analysis, {"lifecycle_state": "active"}
            ),
            MarketSnapshotMemberInput(
                c.id, "missing", c_translation, None, {"lifecycle_state": "active"}
            ),
            MarketSnapshotMemberInput(
                d.id, "accepted", d_translation, d_analysis, {"lifecycle_state": "active"}
            ),
        )
    )

    result = h.aggregate().build_profile(snapshot.id)
    corpus = result.profile["corpus"]
    assert corpus["raw_snapshot_members"] == 4
    assert corpus["primary_core_postings"] == 3
    assert corpus["accepted_semantic_core_postings"] == 2
    assert corpus["accepted_semantic_coverage"] == {
        "numerator": 2,
        "denominator": 3,
        "share": 0.666667,
    }
    assert corpus["dispositions"] == {
        "core_match": 3,
        "adjacent_match": 1,
        "uncertain": 0,
        "excluded": 0,
    }
    assert corpus["semantic_coverage_core"] == {
        "accepted": 2,
        "pending": 0,
        "missing": 1,
        "failed": 0,
        "rejected": 0,
    }

    employers = result.profile["employers"]
    assert employers["distinct_known_employers"] == 2
    assert employers["largest_employer_postings"] == 2
    assert employers["largest_employer_share_of_core"] == 0.666667

    python = next(row for row in result.profile["requirements"] if row["label"] == "Python")
    assert python["postings"] == 2
    assert python["share_of_accepted_semantic_core"] == 1.0
    assert python["distinct_known_employers"] == 1
    assert python["strength_postings"] == {
        "required": 2,
        "preferred": 1,
        "contextual": 0,
        "inferred": 0,
    }
    assert python["depth_signal_postings"] == [{"depth_signal": "Expert", "postings": 1}]
    assert len(python["evidence"]) == 2

    build_models = next(
        row
        for row in result.profile["responsibilities"]
        if row["label"] == "Build ML models."
    )
    assert build_models["postings"] == 1
    assert len(build_models["evidence"][0]["claim_indexes"]) == 2
    assert not any(item["source_job_id"] == "d" for item in python["evidence"])

    warning_codes = {item["code"] for item in result.profile["warnings"]}
    assert {
        "repost_adjustment_missing",
        "small_core_sample",
        "small_semantic_sample",
        "incomplete_semantic_coverage",
    } <= warning_codes


def test_profile_uses_exact_historical_source_detail_not_later_version(h: Harness) -> None:
    detail, translation = h.seed_source("historical", company="Original Employer")
    analysis = h.analysis(
        detail,
        translation,
        requirements=[requirement("Python")],
        responsibilities=[],
    )
    membership = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
        analysis_id=analysis,
        identity="historical",
    )
    snapshot = h.snapshot(
        (
            MarketSnapshotMemberInput(
                membership.id,
                "accepted",
                translation,
                analysis,
                {"lifecycle_state": "active"},
            ),
        )
    )

    h.now += timedelta(days=1)
    h.seed_source("historical", company="Later Employer Name", version=2)
    profile = h.aggregate().build_profile(snapshot.id).profile
    assert profile["employers"]["postings_by_employer"] == [
        {"employer": "Original Employer", "postings": 1}
    ]


def test_registry_mapping_is_applied_only_as_of_snapshot_time(h: Harness) -> None:
    first_detail, first_translation = h.seed_source("first", company="Alpha")
    first_analysis = h.analysis(
        first_detail,
        first_translation,
        requirements=[requirement("Python programming")],
        responsibilities=[],
    )
    first = h.membership(
        first_detail,
        disposition="core_match",
        translation_id=first_translation,
        analysis_id=first_analysis,
        identity="first",
    )

    second_detail, second_translation = h.seed_source("second", company="Beta")
    second_analysis = h.analysis(
        second_detail,
        second_translation,
        requirements=[requirement("Python")],
        responsibilities=[],
    )
    second = h.membership(
        second_detail,
        disposition="core_match",
        translation_id=second_translation,
        analysis_id=second_analysis,
        identity="second",
    )

    third_detail, third_translation = h.seed_source("third", company="Gamma")
    third_analysis = h.analysis(
        third_detail,
        third_translation,
        requirements=[requirement("Python language")],
        responsibilities=[],
    )
    third = h.membership(
        third_detail,
        disposition="core_match",
        translation_id=third_translation,
        analysis_id=third_analysis,
        identity="third",
    )

    h.registry.create_concept(
        concept_id="skill:python",
        category="skill",
        preferred_label="Python",
        description="Python programming language skill.",
        reviewed_at=h.now - timedelta(minutes=2),
        review_note="Reviewed canonical Python concept.",
    )
    for artifact_id in (first_analysis, second_analysis):
        h.registry.record_claim_mapping(
            analysis_artifact_id=artifact_id,
            claim_kind="requirement",
            claim_index=0,
            disposition="mapped",
            canonical_concept_id="skill:python",
            reviewed_at=h.now - timedelta(minutes=1),
            review_note="Reviewed equivalent Python requirement.",
        )

    snapshot = h.snapshot(
        tuple(
            MarketSnapshotMemberInput(membership_id, "accepted", translation_id, analysis_id, {})
            for membership_id, translation_id, analysis_id in (
                (first.id, first_translation, first_analysis),
                (second.id, second_translation, second_analysis),
                (third.id, third_translation, third_analysis),
            )
        )
    )

    h.registry.record_claim_mapping(
        analysis_artifact_id=third_analysis,
        claim_kind="requirement",
        claim_index=0,
        disposition="mapped",
        canonical_concept_id="skill:python",
        reviewed_at=h.now + timedelta(minutes=1),
        review_note="Reviewed only after the historical snapshot.",
    )

    service = h.aggregate()
    first_build = service.build_profile(snapshot.id)
    second_build = service.build_profile(snapshot.id)
    assert second_build.artifact.id == first_build.artifact.id
    assert second_build.artifact.profile_sha256 == first_build.artifact.profile_sha256

    canonical = next(
        row
        for row in first_build.profile["requirements"]
        if row["canonical_concept_id"] == "skill:python"
    )
    raw_late = next(
        row
        for row in first_build.profile["requirements"]
        if row["label"] == "Python language"
    )
    assert canonical["postings"] == 2
    assert canonical["mapping_ids"]
    assert raw_late["postings"] == 1
    assert raw_late["canonical_concept_id"] is None
    assert raw_late["normalization_states"] == ["raw_unreviewed"]


def test_nonaccepted_semantic_members_never_contribute_claim_counts(h: Harness) -> None:
    detail, translation = h.seed_source("pending", company="Alpha")
    analysis = h.analysis(
        detail,
        translation,
        requirements=[requirement("Should not count")],
        responsibilities=[responsibility("Should not count")],
        status="pending",
    )
    membership = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
        analysis_id=None,
        identity="pending",
    )
    snapshot = h.snapshot(
        (
            MarketSnapshotMemberInput(
                membership.id,
                "pending",
                translation,
                analysis,
                {},
            ),
        )
    )
    profile = h.aggregate().build_profile(snapshot.id).profile
    assert profile["corpus"]["primary_core_postings"] == 1
    assert profile["corpus"]["accepted_semantic_core_postings"] == 0
    assert profile["requirements"] == []
    assert profile["responsibilities"] == []


def test_unknown_employer_is_explicit_not_fabricated(h: Harness) -> None:
    detail, translation = h.seed_source("unknown-company", company=None)
    analysis = h.analysis(
        detail,
        translation,
        requirements=[],
        responsibilities=[],
    )
    membership = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
        analysis_id=analysis,
        identity="unknown-company",
    )
    snapshot = h.snapshot(
        (
            MarketSnapshotMemberInput(
                membership.id,
                "accepted",
                translation,
                analysis,
                {},
            ),
        )
    )
    profile = h.aggregate().build_profile(snapshot.id).profile
    assert profile["employers"]["distinct_known_employers"] == 0
    assert profile["employers"]["unknown_employer_postings"] == 1
    assert profile["employers"]["postings_by_employer"] == []
    assert "unknown_employer_evidence" in {
        item["code"] for item in profile["warnings"]
    }
