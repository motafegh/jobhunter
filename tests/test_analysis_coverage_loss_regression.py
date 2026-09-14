"""Source coverage must survive flattened headings and partial list decomposition."""

from jobhunter.analysis_service_v11 import qualification_list_spans
from jobhunter.analysis_service_v14 import residual_requirement_spans
from jobhunter.evidence_refs import build_responsibility_coverage_plan


def test_flattened_capitalized_responsibility_heading_preserves_duties():
    duties = "Build semantic layers. Create evaluation and observability frameworks."
    fields = {
        "description": (
            "We build a financial intelligence platform. Responsibilities "
            + duties
            + " Required Qualifications Strong Python skills."
        )
    }
    assert duties in build_responsibility_coverage_plan(fields).values()


def test_ordinary_responsibility_word_does_not_create_duties():
    fields = {
        "description": "Experience discussing responsibilities with product teams is required."
    }
    assert build_responsibility_coverage_plan(fields) == {}


def test_partial_decomposition_preserves_prefix_middle_and_tail_requirements():
    fields = {
        "description": (
            "Required Qualifications Production experience with storage engines. "
            "Experience with indexing, query planning. Deep understanding of transactions. "
            "Experience with monitoring, alerting. Strong troubleshooting skills."
        )
    }
    residuals = residual_requirement_spans(fields)
    for text in [
        "Production experience with storage engines.",
        "Deep understanding of transactions.",
        "Strong troubleshooting skills.",
    ]:
        assert text in residuals


def test_alternative_frameworks_remain_one_qualification():
    fields = {"description": "Experience with LangGraph, PydanticAI, or similar agent frameworks."}
    assert qualification_list_spans(fields) == [fields["description"].rstrip(".")]
