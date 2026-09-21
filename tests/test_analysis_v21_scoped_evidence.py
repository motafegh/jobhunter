from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from jobhunter.analysis_runtime_v21 import V21CandidateAnalysisProvider
from jobhunter.analysis_service_v21 import (
    _ENGLISH_SYSTEM_PROMPT_V21,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs import (
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
)
from jobhunter.evidence_refs_v21 import (
    build_requirement_coverage_plan_v21,
    build_responsibility_coverage_plan_v21,
)
from jobhunter.inference.instructor_lm_studio_v21 import (
    AnalysisRequirementV21,
    JobAnalysisResponseV21,
    complete_analysis_partition_with_instructor_v21,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_ACCEPTED_ANCHORS = ("tG9K", "t4jp", "tmBK", "t4qV", "tmyX")
_TMBK_ITEM_EXCERPTS = {
    "Python/Django": "Mastery of Python/Django",
    "DRF, FastAPI": "Mastery of DRF, FastAPI",
    "Git": "Familiarity with Git",
    "Linux operating system": "Familiarity with Linux operating system",
    "SQL and NoSQL databases": "Familiarity with SQL and NoSQL databases",
    "Object-Oriented concepts, modular design": (
        "Sufficient knowledge of Object-Oriented concepts, modular design"
    ),
    "Database Locking, Concurrency, and Transaction Management": (
        "Familiarity with Database Locking, Concurrency, and Transaction Management"
    ),
}


def _context(evidence: str, *, obligation: str = "required") -> dict[str, object]:
    return {
        "analysis_mode": "english",
        "analysis_fields": {"description": evidence},
        "evidence_catalog": {},
        "requirement_coverage_plan": {
            "field:description:segment:0": {
                "text": evidence,
                "source_kind": "requirement_section",
                "obligation_hint": obligation,
                "allow_exclusion": True,
            }
        },
    }


def _requirement(
    *,
    concept: str,
    evidence: str,
    item_excerpt: str,
    depth_signal: str | None,
    requirement_type: str = "required",
    concept_type: str = "skill",
) -> dict[str, object]:
    return {
        "concept": concept,
        "depth_signal": depth_signal,
        "requirement_type": requirement_type,
        "concept_type": concept_type,
        "evidence": evidence,
        "item_excerpt": item_excerpt,
        "confidence": "high",
        "rationale": "Direct employer qualification.",
    }


def test_v21_distinguishes_null_experience_depth_from_neighbor_familiarity() -> None:
    evidence = (
        "practical experience with LLMs and language model APIs in Python and/or TypeScript, "
        "familiarity with Tool Calling / Function Calling, familiarity with RAG, Embedding, "
        "and Vector Databases"
    )
    context = _context(evidence)
    response = JobAnalysisResponseV21.model_validate(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                _requirement(
                    concept="LLM and language model API experience",
                    evidence=evidence,
                    item_excerpt=(
                        "practical experience with LLMs and language model APIs in Python "
                        "and/or TypeScript"
                    ),
                    depth_signal=None,
                    concept_type="experience",
                ),
                _requirement(
                    concept="Tool Calling / Function Calling",
                    evidence=evidence,
                    item_excerpt="familiarity with Tool Calling / Function Calling",
                    depth_signal="familiarity with Tool Calling / Function Calling",
                ),
            ],
            "coverage_exclusions": [],
        },
        context=context,
    )

    assert response.requirements[0].depth_signal is None
    assert response.requirements[1].depth_signal == "familiarity"
    assert {item.evidence for item in response.requirements} == {evidence}


def test_v21_rejects_omitted_depth_within_exact_item_scope() -> None:
    evidence = "practical Python experience, familiarity with Linux and Git"
    with pytest.raises(ValidationError, match="Explicit item depth must be supplied"):
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept="Linux and Git",
                evidence=evidence,
                item_excerpt="familiarity with Linux and Git",
                depth_signal=None,
            ),
            context=_context(evidence),
        )


def test_v21_canonicalizes_one_source_proven_leading_depth_wrapper() -> None:
    evidence = "familiarity with Tool Calling / Function Calling"
    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Familiarity with Tool Calling / Function Calling",
            evidence=evidence,
            item_excerpt=evidence,
            depth_signal=None,
        ),
        context=_context(evidence),
    )

    assert result.concept == "Tool Calling / Function Calling"
    assert result.depth_signal == "familiarity"


def test_v21_requires_shared_marker_scope_for_coordinated_list_item() -> None:
    evidence = "familiarity with RAG, Embedding, and Vector Databases"
    with pytest.raises(ValidationError, match="concept contains familiarity"):
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept="Familiarity with Embedding",
                evidence=evidence,
                item_excerpt="Embedding",
                depth_signal=None,
            ),
            context=_context(evidence),
        )

    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Embedding",
            evidence=evidence,
            item_excerpt=evidence,
            depth_signal="familiarity",
        ),
        context=_context(evidence),
    )
    assert result.depth_signal == "familiarity"


def test_v21_preserves_shared_preferred_parent_context() -> None:
    evidence = (
        "It is an advantage if you have experience building Production-grade Agents, "
        "familiarity with LLM system Observability and Evaluation"
    )
    context = _context(evidence, obligation="preferred")
    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Production-grade Agent experience",
            evidence=evidence,
            item_excerpt="experience building Production-grade Agents",
            depth_signal=None,
            requirement_type="preferred",
            concept_type="experience",
        ),
        context=context,
    )

    assert result.requirement_type == "preferred"
    assert result.item_excerpt == "experience building Production-grade Agents"
    assert result.evidence == evidence


def test_v21_rejects_item_excerpt_outside_parent_or_wrong_parent_strength() -> None:
    evidence = "It is an advantage if you have familiarity with Docker and Cloud services"
    payload = _requirement(
        concept="Docker and Cloud services",
        evidence=evidence,
        item_excerpt="familiarity with Kubernetes",
        depth_signal="familiarity",
        requirement_type="preferred",
    )
    with pytest.raises(ValidationError, match="exact contiguous source subspan"):
        AnalysisRequirementV21.model_validate(
            payload,
            context=_context(evidence, obligation="preferred"),
        )

    payload["item_excerpt"] = "familiarity with Docker and Cloud services"
    payload["requirement_type"] = "required"
    with pytest.raises(ValidationError, match="Preferred parent coverage"):
        AnalysisRequirementV21.model_validate(
            payload,
            context=_context(evidence, obligation="preferred"),
        )


def test_v21_handles_accepted_anchor_style_multi_depth_list() -> None:
    evidence = (
        "Mastery of Python/Django - Mastery of DRF, FastAPI - Familiarity with Git - "
        "Familiarity with Linux operating system - Sufficient knowledge of Object-Oriented "
        "concepts, modular design"
    )
    context = _context(evidence)
    requirements = [
        ("Python/Django", "Mastery of Python/Django", "Mastery", "tool"),
        ("DRF, FastAPI", "Mastery of DRF, FastAPI", "Mastery", "tool"),
        ("Git", "Familiarity with Git", "Familiarity", "tool"),
        (
            "Linux operating system",
            "Familiarity with Linux operating system",
            "Familiarity",
            "tool",
        ),
        (
            "Object-Oriented concepts, modular design",
            "Sufficient knowledge of Object-Oriented concepts, modular design",
            "Sufficient knowledge",
            "knowledge",
        ),
    ]

    results = [
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept=concept,
                evidence=evidence,
                item_excerpt=item_excerpt,
                depth_signal=depth,
                concept_type=concept_type,
            ),
            context=context,
        )
        for concept, item_excerpt, depth, concept_type in requirements
    ]

    assert [item.depth_signal for item in results] == [
        "Mastery",
        "Mastery",
        "Familiarity",
        "Familiarity",
        "Sufficient knowledge",
    ]


def test_v21_candidate_scope_is_explicit_and_does_not_change_v5_shape() -> None:
    schema = JobAnalysisResponseV21.model_json_schema()
    requirement_ref = schema["properties"]["requirements"]["items"]["$ref"]
    requirement_name = requirement_ref.rsplit("/", 1)[1]
    assert "item_excerpt" in schema["$defs"][requirement_name]["required"]

    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                "concept": "Git",
                "depth_signal": "Familiarity",
                "requirement_type": "required",
                "concept_type": "tool",
                "evidence": "Familiarity with Git and Linux",
                "item_excerpt": "Familiarity with Git",
                "confidence": "high",
                "rationale": "Direct employer qualification.",
            }
        ],
        "coverage_exclusions": [],
    }
    persisted = persisted_v20_shape(structured)

    assert "item_excerpt" not in persisted["requirements"][0]
    assert "item_excerpt" in structured["requirements"][0]


def test_v21_provider_boundary_uses_scoped_contract_and_returns_v5_shape(
    monkeypatch,
) -> None:
    evidence = (
        "practical experience with LLM APIs, familiarity with Tool Calling / Function Calling"
    )
    fields = {"description": "Requirements: " + evidence}
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v20.ensure_lm_studio_model_context",
        lambda **kwargs: SimpleNamespace(
            context_length=32768,
            action="reused",
            instance_id="offline-v21",
        ),
    )

    def complete_partition(**kwargs):
        calls.append(kwargs)
        parent = next(iter(kwargs["requirement_coverage_plan"].values()))["text"]
        return StructuredInferenceResult(
            model="offline-v21",
            structured={
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [
                    _requirement(
                        concept="LLM API experience",
                        evidence=parent,
                        item_excerpt="practical experience with LLM APIs",
                        depth_signal=None,
                        concept_type="experience",
                    ),
                    _requirement(
                        concept="Tool Calling / Function Calling",
                        evidence=parent,
                        item_excerpt="familiarity with Tool Calling / Function Calling",
                        depth_signal="familiarity",
                    ),
                ],
                "coverage_exclusions": [],
            },
            request_body={
                "runtime": {"p16_v21_item_scoped_evidence": True},
                "instructor": {"response_model": "JobAnalysisResponseV21"},
            },
            raw_response={"offline": True},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v21.complete_analysis_partition_with_instructor_v21",
        complete_partition,
    )
    provider = V21CandidateAnalysisProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="offline-v21",
        api_token=None,
        timeout_seconds=10,
        max_retries=0,
    )
    result = provider._run_once(
        kwargs={"user_payload": {"analysis_fields": fields}},
        system_prompt=_ENGLISH_SYSTEM_PROMPT_V21,
        original_fields=fields,
        effective_fields=fields,
        qualification_refs=[],
        residual_refs=[],
        additional_plan={},
        decomposed_refs=[],
    )

    assert calls
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v21-candidate"
    assert "EXACT ITEM SCOPE WITH PARENT COVERAGE" in _ENGLISH_SYSTEM_PROMPT_V21
    assert all("item_excerpt" not in item for item in result.structured["requirements"])
    partition_request = result.request_body["partition_requests"][0]
    assert partition_request["runtime"]["p16_v21_item_scoped_evidence"] is True
    assert partition_request["instructor"]["response_model"] == "JobAnalysisResponseV21"


def test_v21_transport_wrapper_selects_v21_response_model(monkeypatch) -> None:
    captured = {}
    expected = StructuredInferenceResult(
        model="offline-v21",
        structured={},
        request_body={},
        raw_response={},
        finish_reason="stop",
    )

    def shared_transport(**kwargs):
        captured.update(kwargs)
        return expected

    monkeypatch.setattr(
        "jobhunter.inference.instructor_lm_studio_v20."
        "_complete_analysis_partition_with_instructor",
        shared_transport,
    )
    result = complete_analysis_partition_with_instructor_v21(
        base_url="http://127.0.0.1:1234/v1/",
        api_token=None,
        timeout_seconds=10,
        network_retries=0,
        selected_model="offline-v21",
        system_prompt=_ENGLISH_SYSTEM_PROMPT_V21,
        user_payload={"analysis_fields": {"description": "Requirements: Python"}},
        max_tokens=1024,
        seed=0,
        requirement_coverage_plan={},
        responsibility_coverage_plan={},
    )

    assert result is expected
    assert captured["response_model"] is JobAnalysisResponseV21
    assert captured["contract_version"] == "v21"


def test_v21_validates_all_current_accepted_anchor_requirements_read_only() -> None:
    validated = 0
    for source_job_id in _ACCEPTED_ANCHORS:
        job_dir = _REPOSITORY_ROOT / "corpus" / "jobs" / source_job_id
        fields = json.loads(
            (job_dir / "english-projection.json").read_text(encoding="utf-8")
        )["fields"]
        analysis = json.loads(
            (job_dir / "p16-english.json").read_text(encoding="utf-8")
        )["analysis"]
        context = {
            "analysis_mode": "english",
            "analysis_fields": fields,
            "evidence_catalog": {},
            "requirement_coverage_plan": {},
        }
        for persisted in analysis["requirements"]:
            item_excerpt = persisted["evidence"]
            if source_job_id == "tmBK":
                candidate_excerpt = _TMBK_ITEM_EXCERPTS.get(persisted["concept"])
                if candidate_excerpt and candidate_excerpt in persisted["evidence"]:
                    item_excerpt = candidate_excerpt
            AnalysisRequirementV21.model_validate(
                {**persisted, "item_excerpt": item_excerpt},
                context=context,
            )
            validated += 1

    assert validated == 85


def test_v21_splits_mixed_obligation_sentences_and_stops_at_application() -> None:
    fields = {
        "description": (
            "Requirements: Architecture experience is required. "
            "It is an advantage if you have production Agent experience. "
            "Our company builds accounting software. "
            "To apply for collaboration, please send your resume. "
            "A short portfolio is welcome."
        )
    }

    accepted_plan = build_requirement_coverage_plan(fields)
    candidate_plan = build_requirement_coverage_plan_v21(fields)

    assert len(accepted_plan) == 1
    assert [item["text"] for item in candidate_plan.values()] == [
        "Architecture experience is required.",
        "It is an advantage if you have production Agent experience.",
        "Our company builds accounting software.",
    ]
    assert [item["obligation_hint"] for item in candidate_plan.values()] == [
        "required",
        "preferred",
        "required",
    ]
    assert all(item["allow_exclusion"] is True for item in candidate_plan.values())

    required_only = build_requirement_coverage_plan_v21(
        {
            "description": (
                "Requirements: Python experience is required. "
                "Interested parties, please send your resume and portfolio."
            )
        }
    )
    assert [item["text"] for item in required_only.values()] == [
        "Python experience is required."
    ]


def test_v21_decomposes_repeated_gerund_duties_without_splitting_coordination() -> None:
    fields = {
        "description": (
            "Responsibilities include designing production Agents, connecting Agents to APIs, "
            "evaluating, debugging, and improving Agent performance, paying attention to cost "
            "and reliability. Close collaboration with Product teams to ship AI features is "
            "important. Practical experience matters more than degrees. "
            "Requirements: Python."
        )
    }

    accepted_plan = build_responsibility_coverage_plan(fields)
    candidate_plan = build_responsibility_coverage_plan_v21(fields)

    assert len(accepted_plan) == 1
    assert list(candidate_plan.values()) == [
        "include designing production Agents",
        "connecting Agents to APIs",
        "evaluating, debugging, and improving Agent performance",
        "paying attention to cost and reliability.",
        "Close collaboration with Product teams to ship AI features is important.",
    ]
    assert all("Practical experience" not in text for text in candidate_plan.values())


def test_v21_requirement_planner_leaves_accepted_anchor_ledgers_unchanged() -> None:
    for source_job_id in _ACCEPTED_ANCHORS:
        fields = json.loads(
            (
                _REPOSITORY_ROOT
                / "corpus"
                / "jobs"
                / source_job_id
                / "english-projection.json"
            ).read_text(encoding="utf-8")
        )["fields"]

        assert build_requirement_coverage_plan_v21(fields) == (
            build_requirement_coverage_plan(fields)
        )
