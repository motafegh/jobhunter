from types import SimpleNamespace

from jobhunter.phase1_report import Phase1ReportService, format_phase1_report


def _source(job_id: str, detail_id: int):
    return SimpleNamespace(
        source_job_id=job_id,
        job_detail_version_id=detail_id,
        source_language="en",
        fields={"title": f"Role {job_id}"},
    )


class _SourceStore:
    def latest_source_versions(self, *, limit: int):
        assert limit == 5000
        return tuple(_source(job_id, index) for index, job_id in enumerate("abcdefg", 1))


class _Translations:
    def __init__(self):
        self._ids = {job_id: index * 10 for index, job_id in enumerate("bcdefg", 2)}

    def current_artifact(self, job_id: str):
        artifact_id = self._ids.get(job_id)
        if artifact_id is None:
            return None
        return SimpleNamespace(
            id=artifact_id,
            provider_name="source-identity",
            provider_model="native-english",
            translation_schema_version="english-projection-v2",
        )


class _Analyses:
    def find_artifact(self, **kwargs):
        assert kwargs["require_translation_dependency"] is True
        artifacts = {
            (3, 30): SimpleNamespace(
                id=303,
                semantic_review_status="pending",
            ),
            (4, 40): SimpleNamespace(
                id=404,
                semantic_review_status="accepted",
            ),
            (5, 50): SimpleNamespace(
                id=505,
                semantic_review_status="accepted",
            ),
        }
        return artifacts.get(
            (kwargs["job_detail_version_id"], kwargs["translation_artifact_id"])
        )


class _Capabilities:
    def find_artifact(self, **kwargs):
        if kwargs["analysis_artifact_id"] == 505:
            return SimpleNamespace(id=9005)
        return None


class _Workflow:
    def get_state(self, job_id: str):
        return SimpleNamespace(
            triage_state="not_relevant" if job_id == "f" else "unreviewed"
        )


def _market():
    return SimpleNamespace(
        discovered_jobs=12,
        analyzed_jobs=2,
        source_scope="Public Jobinja postings",
        filter_scope="Accepted current English P1.6 only",
        duplicate_adjustment="No repost adjustment",
        sample_warning="Small sample",
        concentration_warning=None,
    )


def test_report_uses_exact_dependencies_and_separates_action_queues() -> None:
    service = Phase1ReportService(
        source_store=_SourceStore(),
        translation_service=_Translations(),
        analysis_store=_Analyses(),
        capability_store=_Capabilities(),
        workflow_store=_Workflow(),
        market_insights=SimpleNamespace(market_summary=_market),
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    report = service.build()

    assert report.discovered_jobs == 12
    assert report.current_parsed_jobs == 7
    assert report.current_english_projections == 6
    assert report.pending_english_analyses == 1
    assert report.accepted_english_analyses == 2
    assert report.current_capabilities == 1
    assert report.translation_missing == ("a",)
    assert report.analysis_ready == ("b", "g")
    assert report.analysis_pending_review == ("c",)
    assert report.capability_ready == ("d",)
    assert report.current_chains == ("e",)
    assert next(row for row in report.rows if row.source_job_id == "f").chain_status == (
        "analysis_not_selected"
    )


def test_report_formatter_is_deterministic_and_includes_exact_lineage() -> None:
    service = Phase1ReportService(
        source_store=_SourceStore(),
        translation_service=_Translations(),
        analysis_store=_Analyses(),
        capability_store=_Capabilities(),
        workflow_store=_Workflow(),
        market_insights=SimpleNamespace(market_summary=_market),
        analysis_model="analysis-model",
        capability_model="capability-model",
    )
    report = service.build()

    first = format_phase1_report(report)
    second = format_phase1_report(report)

    assert first == second
    assert "Translation missing (1): a" in first
    assert "Analysis ready (2): b, g" in first
    assert "Source scope: Public Jobinja postings" in first
    assert "Sampling warning: Small sample" in first
    assert "e: detail=5, translation=50, p16=505, capability=9005" in first
