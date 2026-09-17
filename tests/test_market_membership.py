"""I3 contract tests. Scripted semantic outcomes are fixtures, not model-quality proof."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.market_affected_work import MarketAffectedWorkPlanner
from jobhunter.market_membership_models import MarketMembershipDecision
from jobhunter.market_membership_service import (
    MarketMembershipError,
    MarketMembershipService,
    MarketMembershipUnavailableError,
)
from jobhunter.market_models import MarketDefinitionSpec
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 17, 12, tzinfo=UTC)


def _decision(disposition="core_match", refs=("source:description",)):
    return MarketMembershipDecision(
        disposition=disposition,
        reason="Fixture role/work judgment.",
        confidence="medium",
        evidence_refs=list(refs),
    )


class FakeProvider:
    def __init__(self, decision=None, callback=None, model="fixture-model"):
        self.decision = decision or _decision()
        self.callback = callback
        self.calls = []
        self.identity = {"model": model, "provider": "fixture"}

    def classify(self, payload):
        self.calls.append(payload)
        if self.callback:
            self.callback()
        return self.decision


class Harness:
    def __init__(self, path):
        self.path = path
        self.now = _NOW
        self.source = JobHunterStore(path)
        self.source.initialize()
        self.market = MarketStore(path)
        self.translations = TranslationStore(path)
        self.analyses = AnalysisStore(path)
        target = self.market.create_target(
            slug="applied-ai", name="Applied AI", description=None, created_at=_NOW
        )
        self.spec = MarketDefinitionSpec(
            membership_intent="Applied AI / ML engineering work",
            search_catalog_version="fixture-v1",
        )
        self.definition = self.market.create_definition_version(
            target.id, spec=self.spec, created_at=_NOW
        )
        self.translation_service = TranslationService(store=self.translations, provider=None)

    def seed(self, job_id="job", fields=None, version=1, age_hours=1, parse_status="parsed"):
        fields = (
            fields
            if fields is not None
            else {
                "title": "AI engineer",
                "description": "Build and evaluate AI models.",
                "language": "en",
            }
        )
        posting = self.source.upsert_job(
            job=DiscoveredJobLink(
                source_job_id=job_id,
                company_slug="fixture",
                canonical_url=f"https://jobinja.ir/companies/fixture/jobs/{job_id}/role",
                observed_text="Discovery title must not override parsed detail",
            ),
            observed_at=_NOW,
        )
        return self.source.record_job_detail(
            job_posting_id=posting.job_posting_id,
            fetched_at=_NOW - timedelta(hours=age_hours),
            requested_url=f"https://jobinja.ir/jobs/{job_id}",
            final_url=f"https://jobinja.ir/jobs/{job_id}",
            status_code=200,
            content_sha256=f"raw-{job_id}-{version}",
            semantic_sha256=f"semantic-{job_id}-{version}",
            evidence_path=Path("fixture.html"),
            metadata_path=Path("fixture.json"),
            parser_version="jobinja-detail-v2",
            parse_status=parse_status,
            fields=fields,
        ).version_id

    def analysis(self, detail, translation, status="accepted", **kwargs):
        return self.analyses.record_artifact(
            job_detail_version_id=detail,
            translation_artifact_id=translation,
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            analysis=kwargs.get(
                "analysis",
                {
                    "responsibilities": [
                        {"statement": "Build AI models.", "evidence": "Build AI models."}
                    ],
                    "requirements": [],
                    "role_purpose": [],
                },
            ),
            request_body={},
            raw_response={},
            created_at=_NOW,
            semantic_review_status=status,
        )

    def service(self, provider):
        planner = MarketAffectedWorkPlanner(
            market_store=self.market,
            source_store=self.source,
            observations=JobDetailObservationStore(self.path),
            translation_store=self.translations,
            translation_service=self.translation_service,
            analysis_store=self.analyses,
            analysis_model="analysis-model",
            clock=lambda: self.now,
        )
        return MarketMembershipService(
            planner=planner,
            market_store=self.market,
            translation_store=self.translations,
            analysis_store=self.analyses,
            provider=provider,
            clock=lambda: self.now,
        )

    def qualify(self, service, job_id="job", definition_id=None):
        return service.qualify(
            target_definition_version_id=definition_id or self.definition.id, source_job_id=job_id
        )


@pytest.fixture
def h(tmp_path):
    return Harness(tmp_path / "jobs.sqlite3")


@pytest.mark.parametrize(
    ("job_id", "description", "disposition"),
    [
        (
            "ta9l",
            "Develop AI agents and RAG systems using vector search and retrieval optimization.",
            "core_match",
        ),
        (
            "tG9K",
            "Build and validate ML/AI models on semiconductor process and manufacturing data.",
            "core_match",
        ),
        ("tGM0", "Develop backend services and APIs in the AI platform team.", "adjacent_match"),
        ("t4jp", "Create images and videos with AI for content production.", "excluded"),
        (
            "tmBK",
            "Python/Django development; ability to use AI to improve development speed.",
            "excluded",
        ),
        ("t4qV", "Design network security and manage next-generation firewalls.", "excluded"),
        ("tmyX", "Assess Microsoft server and infrastructure security.", "excluded"),
        ("sparse", "Join our technical team. Work scope to be discussed.", "uncertain"),
    ],
)
def test_representative_scripted_interpretations_persist_without_p16(
    h, job_id, description, disposition
):
    # Bounded paraphrase fixtures from the foundation decision, not source quotations or an eval.
    h.seed(job_id, {"title": "AI specialist", "description": description, "language": "en"})
    provider = FakeProvider(_decision(disposition))
    service = h.service(provider)
    first = h.qualify(service, job_id)
    second = h.qualify(service, job_id)
    assert first.membership.disposition == disposition
    assert first.membership.analysis_artifact_id is None
    assert second.membership.id == first.membership.id
    assert second.outcome == "reused"
    assert len(provider.calls) == 1
    assert provider.calls[0]["evidence"]["source:description"] == description
    assert "search_catalog_version" not in provider.calls[0]["target"]


def test_exact_accepted_p16_and_translation_are_consumed(h):
    detail = h.seed()
    translation = h.translation_service.translate_job("job").artifact_id
    analysis = h.analysis(detail, translation)
    provider = FakeProvider(_decision(refs=("p16:responsibilities:0",)))
    result = h.qualify(h.service(provider))
    assert result.membership.translation_artifact_id == translation
    assert result.membership.analysis_artifact_id == analysis
    assert (
        provider.calls[0]["evidence"]["p16:responsibilities:0"]["statement"] == "Build AI models."
    )


def test_pending_p16_is_not_consumed_or_a_gate(h):
    detail = h.seed()
    translation = h.translation_service.translate_job("job").artifact_id
    pending = h.analysis(detail, translation, "pending")
    provider = FakeProvider()
    result = h.qualify(h.service(provider))
    assert result.membership.analysis_artifact_id is None
    assert h.analyses.artifact_by_id(pending).semantic_review_status == "pending"
    assert not any(k.startswith("p16:") for k in provider.calls[0]["evidence"])


@pytest.mark.parametrize(
    "fields",
    [
        {"title": "AI engineer", "language": "en"},
        {"title": "AI engineer", "skills": ["AI", "Python"], "language": "en"},
    ],
)
def test_title_or_skills_alone_cannot_establish_core(h, fields):
    h.seed(fields=fields)
    provider = FakeProvider(_decision(refs=("source:title",)))
    with pytest.raises(MarketMembershipError, match="substantive evidence"):
        h.qualify(h.service(provider))
    provider.decision = _decision("uncertain", refs=("source:title",))
    result = h.qualify(h.service(provider))
    assert result.membership.disposition == "uncertain"


def test_bad_refs_fail_without_persistence_or_retry(h):
    h.seed()
    provider = FakeProvider(_decision(refs=("p16:responsibilities:98",)))
    with pytest.raises(MarketMembershipError, match="Unknown membership evidence"):
        h.qualify(h.service(provider))
    assert len(provider.calls) == 1
    provider.decision = _decision()
    assert h.qualify(h.service(provider)).membership.id == 1


def test_deterministic_employment_conflict_precedes_model_and_derived_dependencies(h):
    h.seed(
        fields={
            "title": "AI engineer",
            "employment_type": "تمام وقت",
            "description": "Build models.",
            "language": "mixed",
        }
    )
    definition = h.market.create_definition_version(
        h.definition.target_market_id,
        spec=replace(h.spec, employment_type_scope="part-time"),
        created_at=_NOW,
    )
    # No translation provider or membership model: explicit source constraint is sufficient.
    result = h.qualify(h.service(None), definition_id=definition.id)
    assert result.membership.disposition == "excluded"
    assert result.membership.classifier_method == "deterministic"
    assert result.membership.translation_artifact_id is None


@pytest.mark.parametrize(
    "employment,description",
    [
        ("Full time or part time", "Build models."),
        ("Full time", "Part-time arrangements are also available."),
        (None, "Build models."),
    ],
)
def test_ambiguous_constraints_reach_reasoner(h, employment, description):
    h.seed(
        fields={
            "title": "AI engineer",
            "employment_type": employment,
            "description": description,
            "language": "en",
        }
    )
    definition = h.market.create_definition_version(
        h.definition.target_market_id,
        spec=replace(h.spec, employment_type_scope="part-time", geography_scope="Tehran or remote"),
        created_at=_NOW,
    )
    provider = FakeProvider(_decision("uncertain"))
    result = h.qualify(h.service(provider), definition_id=definition.id)
    assert result.membership.classifier_method == "model"
    assert provider.calls[0]["target"]["geography_scope"] == "Tehran or remote"


@pytest.mark.parametrize("condition", ["missing", "stale", "invalid", "removed", "expired"])
def test_ineligible_sources_never_reach_model(h, condition):
    h.seed(
        age_hours=48 if condition == "stale" else 1,
        parse_status="failed" if condition == "invalid" else "parsed",
    )
    if condition in ("removed", "expired"):
        # Lifecycle store API is deliberately bypassed only to arrange this state fixture.
        with h.source._connect() as connection:
            connection.execute("UPDATE job_postings SET lifecycle_state = ?", (condition,))
    if condition == "missing":
        with h.source._connect() as connection:
            connection.execute("DELETE FROM job_detail_versions")
    provider = FakeProvider()
    with pytest.raises(MarketMembershipError, match="I2 source-eligible"):
        h.qualify(h.service(provider))
    assert not provider.calls


def test_source_change_during_inference_cannot_persist_stale_decision(h):
    h.seed()
    provider = FakeProvider(callback=lambda: h.seed(version=2))
    with pytest.raises(MarketMembershipError, match="changed during qualification"):
        h.qualify(h.service(provider))
    provider.callback = None
    assert h.qualify(h.service(provider)).membership.id == 1


def test_freshness_expiry_during_inference_is_not_persisted(h):
    h.seed()
    provider = FakeProvider(callback=lambda: setattr(h, "now", _NOW + timedelta(days=2)))
    with pytest.raises(MarketMembershipError, match="I2 source-eligible"):
        h.qualify(h.service(provider))


def test_source_target_and_model_changes_do_not_reuse(h):
    h.seed()
    provider = FakeProvider()
    service = h.service(provider)
    first = h.qualify(service).membership
    h.seed(version=2)
    second = h.qualify(service).membership
    definition = h.market.create_definition_version(
        h.definition.target_market_id,
        spec=replace(h.spec, membership_intent="ML research work"),
        created_at=_NOW,
    )
    third = h.qualify(service, definition_id=definition.id).membership
    fourth = h.qualify(
        h.service(FakeProvider(model="other-model")), definition_id=definition.id
    ).membership
    assert len({first.id, second.id, third.id, fourth.id}) == 4
    assert h.market.get_membership(first.id) == first


def test_new_translation_and_accepted_analysis_change_exact_consumed_identity(h):
    detail = h.seed()
    provider = FakeProvider()
    service = h.service(provider)
    first = h.qualify(service).membership
    translation = h.translation_service.translate_job("job").artifact_id
    second = h.qualify(service).membership
    analysis = h.analysis(detail, translation)
    third = h.qualify(service).membership
    assert len({first.id, second.id, third.id}) == 3
    assert first.translation_artifact_id is None
    assert second.translation_artifact_id == translation
    assert second.analysis_artifact_id is None
    assert third.analysis_artifact_id == analysis


def test_correction_supersedes_and_exact_rerun_reuses_correction(h):
    h.seed()
    provider = FakeProvider()
    service = h.service(provider)
    original = h.qualify(service).membership
    corrected = service.correct(
        original.id,
        decision=_decision("adjacent_match"),
        review_note="Reviewed enabling-work scope.",
    ).membership
    assert corrected.supersedes_membership_id == original.id
    assert h.qualify(service).membership.id == corrected.id
    assert h.market.get_membership(original.id) == original
    assert len(provider.calls) == 1
    with pytest.raises(MarketMembershipError, match="latest membership"):
        service.correct(original.id, decision=_decision(), review_note="Old decision")


def test_missing_provider_is_failure_not_persisted_uncertainty(h):
    h.seed()
    with pytest.raises(MarketMembershipUnavailableError):
        h.qualify(h.service(None))
    assert h.qualify(h.service(FakeProvider())).membership.id == 1


def test_provider_failure_remains_failure(h):
    h.seed()

    def fail():
        raise RuntimeError("provider offline")

    provider = FakeProvider(callback=fail)
    with pytest.raises(RuntimeError, match="provider offline"):
        h.qualify(h.service(provider))
    provider.callback = None
    assert h.qualify(h.service(provider)).membership.id == 1


@pytest.mark.parametrize(
    "update",
    [
        {"disposition": "promoted"},
        {"confidence": 0.95},
        {"reason": " "},
        {"evidence_refs": []},
        {"taxonomy": "ai-engineer"},
    ],
)
def test_output_contract_is_bounded(update):
    with pytest.raises(ValidationError):
        MarketMembershipDecision.model_validate({**_decision().model_dump(), **update})


def test_review_cannot_cite_fabricated_evidence(h):
    h.seed()
    service = h.service(FakeProvider())
    original = h.qualify(service).membership
    with pytest.raises(MarketMembershipError, match="Unknown membership evidence"):
        service.correct(
            original.id,
            decision=_decision(refs=("source:invented",)),
            review_note="Review still needs evidence",
        )
    assert h.qualify(service).membership.id == original.id


def test_consumed_analysis_change_during_generation_rejects_persistence(h):
    detail = h.seed()
    translation = h.translation_service.translate_job("job").artifact_id
    provider = FakeProvider(callback=lambda: h.analysis(detail, translation))
    with pytest.raises(MarketMembershipError, match="changed during qualification"):
        h.qualify(h.service(provider))
    assert h.market.get_membership(1) is None


def test_original_language_can_be_interpreted_without_translation_gate(h):
    h.seed(
        fields={
            "title": "مهندس هوش مصنوعی",
            "description": "توسعه مدل‌های یادگیری ماشین",
            "language": "fa",
        }
    )
    provider = FakeProvider()
    result = h.qualify(h.service(provider))
    assert result.membership.translation_artifact_id is None
    assert provider.calls[0]["evidence"]["source:description"] == "توسعه مدل‌های یادگیری ماشین"


def test_input_bound_fails_before_call_without_silent_truncation(h):
    h.seed(fields={"title": "AI engineer", "description": "a" * 33000, "language": "en"})
    provider = FakeProvider()
    with pytest.raises(MarketMembershipError, match="not truncated"):
        h.qualify(h.service(provider))
    assert not provider.calls
