from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from jobhunter.analysis_runtime_v21 import (
    V21CandidateAnalysisProvider,
    _v21_requirement_partitions,
)
from jobhunter.analysis_service_v21 import (
    _ENGLISH_SYSTEM_PROMPT_V21,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
)
from jobhunter.evidence_refs_v21 import (
    build_requirement_coverage_plan_v21,
    build_responsibility_coverage_plan_v21,
)
from jobhunter.inference.instructor_lm_studio_v20 import _validated_partition_plan
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


def test_v21_materializes_one_omitted_depth_within_exact_item_scope() -> None:
    evidence = "practical Python experience, familiarity with Linux and Git"
    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Working with Linux and Git",
            evidence=evidence,
            item_excerpt="familiarity with Linux and Git",
            depth_signal=None,
        ),
        context=_context(evidence),
    )

    assert result.concept == "Working with Linux and Git"
    assert result.depth_signal == "familiarity"


def test_v21_rejects_omitted_depth_from_multi_marker_item_scope() -> None:
    evidence = "familiarity with Linux, familiarity with Git"
    with pytest.raises(ValidationError, match="Explicit item depth must be supplied"):
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept="Linux and Git",
                evidence=evidence,
                item_excerpt=evidence,
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
        requirement_coverage_plan={
            "field:description:segment:0:sentence:0": {
                "text": "Python",
                "source_kind": "requirement_section",
                "obligation_hint": "required",
                "allow_exclusion": True,
            }
        },
        responsibility_coverage_plan={
            "field:description:segment:1:item:0": "Build APIs"
        },
    )

    assert result is expected
    assert captured["response_model"] is JobAnalysisResponseV21
    assert captured["contract_version"] == "v21"
    assert captured["additional_evidence_catalog"] == {
        "field:description:segment:0:sentence:0": "Python",
        "field:description:segment:1:item:0": "Build APIs",
    }


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
            "This is why we need someone who can ship reliable production systems. "
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
        "This is why we need someone who can ship reliable production systems.",
    ]
    assert [item["obligation_hint"] for item in candidate_plan.values()] == [
        "required",
        "preferred",
        "required",
        "required",
    ]
    assert [item["allow_exclusion"] for item in candidate_plan.values()] == [
        True,
        True,
        True,
        False,
    ]

    required_only = build_requirement_coverage_plan_v21(
        {
            "description": (
                "Requirements: Python experience is required. "
                "Interested parties, please send your resume and portfolio if you have "
                "experience building production systems."
            )
        }
    )
    assert [item["text"] for item in required_only.values()] == [
        "Python experience is required."
    ]


def test_v21_explicit_candidate_requirement_cannot_be_excluded() -> None:
    evidence = "This is why we need someone who can ship a reliable production system."
    fields = {"description": "Requirements: " + evidence + " It is a plus to know Docker."}
    plan = build_requirement_coverage_plan_v21(fields)
    reference = next(
        reference
        for reference, candidate in plan.items()
        if candidate["text"] == evidence
    )

    with pytest.raises(ValidationError, match="non_excludable_refs_illegally_excluded"):
        JobAnalysisResponseV21.model_validate(
            {
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [],
                "coverage_exclusions": [
                    {
                        "evidence_reference": reference,
                        "rationale": "Covered by preferred experience elsewhere.",
                    }
                ],
            },
            context={
                "analysis_mode": "english",
                "analysis_fields": fields,
                "evidence_catalog": {},
                "requirement_coverage_plan": plan,
                "responsibility_coverage_plan": {},
            },
        )


@pytest.mark.parametrize(
    "sentence",
    [
        (
            "We are looking for someone who has the ability to research, test, "
            "fine-tune, and deploy speech models."
        ),
        (
            "The company is looking to attract a Python Engineer with experience "
            "developing backend services."
        ),
        (
            "This role is suitable for someone with practical experience in web "
            "application security who can test web services."
        ),
        (
            "If you have built an Agent and have worked with LLMs and orchestration, "
            "you may be the right fit."
        ),
    ],
)
def test_v21_tracks_explicit_headingless_candidate_experience(sentence: str) -> None:
    plan = build_requirement_coverage_plan_v21({"description": sentence})

    assert list(plan.values()) == [
        {
            "text": sentence,
            "source_kind": "candidate_experience",
            "obligation_hint": "required",
            "allow_exclusion": False,
        }
    ]


def test_v21_isolates_headingless_candidate_experience_from_dense_sections() -> None:
    plan = {
        "section:0": {
            "text": "Experience with Python, APIs, databases, and distributed systems.",
            "source_kind": "requirement_section",
            "obligation_hint": "required",
            "allow_exclusion": True,
        },
        "candidate:0": {
            "text": "We are looking for someone with experience building reliable services.",
            "source_kind": "candidate_experience",
            "obligation_hint": "required",
            "allow_exclusion": False,
        },
        "candidate:1": {
            "text": "If you have built an agent and worked with LLMs, you may be a fit.",
            "source_kind": "candidate_experience",
            "obligation_hint": "required",
            "allow_exclusion": False,
        },
    }

    partitions = _v21_requirement_partitions(plan)

    assert [list(partition) for partition in partitions] == [
        ["section:0"],
        ["candidate:0", "candidate:1"],
    ]
    assert all(
        {candidate["source_kind"] for candidate in partition.values()}
        in ({"requirement_section"}, {"candidate_experience"})
        for partition in partitions
    )


@pytest.mark.parametrize(
    "sentence",
    [
        "We are looking forward to expanding our product next year.",
        "This role is suitable for remote work.",
        "If you enjoy building software, meet our team.",
    ],
)
def test_v21_does_not_turn_generic_recruiting_prose_into_coverage(sentence: str) -> None:
    assert build_requirement_coverage_plan_v21({"description": sentence}) == {}


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


def test_v21_keeps_including_modifier_and_splits_final_independent_duty() -> None:
    fields = {
        "description": (
            "Responsibilities include designing APIs, developing backend services, including "
            "LLM integrations, implementing access controls, and preparing technical "
            "documentation. Requirements: Python."
        )
    }

    plan = build_responsibility_coverage_plan_v21(fields)

    assert list(plan.values()) == [
        "include designing APIs",
        "developing backend services, including LLM integrations",
        "implementing access controls",
        "preparing technical documentation.",
    ]


def test_v21_tracks_job_description_and_tasks_sections_as_duties() -> None:
    fields = {
        "description": (
            "Job Description: Building assistants, connecting tools to APIs, designing "
            "reliable workflows. Qualifications: Python. Tasks: Maintain services. "
            "Document APIs. Benefits: Bonus."
        )
    }

    plan = build_responsibility_coverage_plan_v21(fields)

    assert list(plan.values()) == [
        "Building assistants",
        "connecting tools to APIs",
        "designing reliable workflows.",
        "Maintain services.",
        "Document APIs.",
    ]


def test_v21_preserves_nominal_prefix_before_gerund_duty_list() -> None:
    fields = {
        "description": (
            "Job Description: Design of automation services, building assistants, connecting "
            "tools to APIs, testing workflows. Qualifications: Python."
        )
    }

    assert list(build_responsibility_coverage_plan_v21(fields).values()) == [
        "Design of automation services",
        "building assistants",
        "connecting tools to APIs",
        "testing workflows.",
    ]


def test_v21_splits_repeated_base_verb_duty_list() -> None:
    fields = {
        "description": (
            "Responsibilities: Design and implement automation, build assistants, connect "
            "tools to APIs, analyze results, and train users. Requirements: Python."
        )
    }

    assert list(build_responsibility_coverage_plan_v21(fields).values()) == [
        "Design and implement automation",
        "build assistants",
        "connect tools to APIs",
        "analyze results",
        "train users.",
    ]


def test_v21_drops_partial_heading_fragments_from_duty_coverage() -> None:
    fields = {
        "description": (
            "Responsibilities: Build services. Skills and Minimum Requirements: Python."
        )
    }

    assert list(build_responsibility_coverage_plan_v21(fields).values()) == [
        "Build services."
    ]


def test_v21_requirement_planner_preserves_unaffected_accepted_anchor_ledgers() -> None:
    for source_job_id in set(_ACCEPTED_ANCHORS) - {"t4jp"}:
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


def test_v21_all_public_projection_ledgers_are_exact_and_transport_valid() -> None:
    projection_paths = sorted(
        (_REPOSITORY_ROOT / "corpus" / "jobs").glob("*/english-projection.json")
    )
    assert len(projection_paths) == 27

    for projection_path in projection_paths:
        fields = json.loads(projection_path.read_text(encoding="utf-8"))["fields"]
        requirement_plan = build_requirement_coverage_plan_v21(fields)
        responsibility_plan = build_responsibility_coverage_plan_v21(fields)
        requirement_partitions = _v21_requirement_partitions(requirement_plan)
        catalog = build_field_evidence_catalog(fields)
        candidate_catalog = {
            reference: str(candidate["text"])
            for reference, candidate in requirement_plan.items()
        }
        candidate_catalog.update(responsibility_plan)

        assert len(set(candidate_catalog.values())) == len(candidate_catalog)
        assert all(
            reference not in catalog or catalog[reference] == text
            for reference, text in candidate_catalog.items()
        )
        assert all(
            reference in catalog or any(text in parent for parent in catalog.values())
            for reference, text in candidate_catalog.items()
        )
        assert all(text.count("(") == text.count(")") for text in responsibility_plan.values())
        partitioned_references = [
            reference
            for partition in requirement_partitions
            for reference in partition
        ]
        assert set(partitioned_references) == set(requirement_plan)
        assert len(partitioned_references) == len(set(partitioned_references))
        assert all(
            not (
                "candidate_experience"
                in {candidate.get("source_kind") for candidate in partition.values()}
                and len(
                    {candidate.get("source_kind") for candidate in partition.values()}
                )
                > 1
            )
            for partition in requirement_partitions
        )

        merged_catalog = {**catalog, **candidate_catalog}
        _validated_partition_plan(
            requirement_plan,
            merged_catalog,
            label="requirement",
        )
        _validated_partition_plan(
            {
                reference: {"text": text}
                for reference, text in responsibility_plan.items()
            },
            merged_catalog,
            label="responsibility",
        )


def test_v21_removes_application_and_benefits_from_t4jp_candidate_ledger() -> None:
    fields = json.loads(
        (
            _REPOSITORY_ROOT
            / "corpus"
            / "jobs"
            / "t4jp"
            / "english-projection.json"
        ).read_text(encoding="utf-8")
    )["fields"]

    plan = build_requirement_coverage_plan_v21(fields)
    texts = [item["text"] for item in plan.values()]

    assert texts == [
        (
            "in content creation with AI, creativity in creating visual and video content, "
            "website design, ability to produce visual content full-time and part-time, "
            "the work is teachable."
        ),
        "Ethics and your work commitment are important to us.",
    ]
    assert all("resume" not in text.casefold() for text in texts)
    assert all("benefits" not in text.casefold() for text in texts)


def test_v21_stops_non_requirement_sections_and_preserves_list_optionality() -> None:
    fields = {
        "description": (
            "Required skills: * Proficiency in Python * Familiarity with Linux is an advantage: "
            "* Experience with Docker * Familiarity with Git "
            "Performance Indicators (KPIs): * Tickets closed * Response time "
            "Please send your resume and portfolio."
        )
    }

    plan = build_requirement_coverage_plan_v21(fields)

    assert [(item["text"], item["obligation_hint"]) for item in plan.values()] == [
        ("Proficiency in Python", "required"),
        ("Familiarity with Linux is an advantage:", "preferred"),
        ("Experience with Docker", "preferred"),
        ("Familiarity with Git", "preferred"),
    ]


def test_v21_propagates_explicit_preferred_group_heading_across_clauses() -> None:
    fields = {
        "description": (
            "Qualifications: Core Python. Points Considered: Experience with Docker; "
            "Familiarity with Linux; Experience with Git. Benefits of Collaboration: Bonus."
        )
    }

    plan = build_requirement_coverage_plan_v21(fields)
    grouped = [
        item
        for item in plan.values()
        if "Docker" in item["text"] or "Linux" in item["text"] or "Git" in item["text"]
    ]

    assert len(grouped) == 3
    assert {item["obligation_hint"] for item in grouped} == {"preferred"}
    assert all("Benefits" not in item["text"] for item in plan.values())


def test_v21_treats_portfolio_review_impact_as_preferred() -> None:
    evidence = (
        "Submitting samples of work has a significant impact on the resume review."
    )
    fields = {
        "description": (
            "Expected skills: Python. " + evidence
        )
    }

    plan = build_requirement_coverage_plan_v21(fields)
    candidate = next(item for item in plan.values() if item["text"] == evidence)
    assert candidate["obligation_hint"] == "preferred"

    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Work samples",
            evidence=evidence,
            item_excerpt=evidence,
            depth_signal=None,
            requirement_type="preferred",
            concept_type="experience",
        ),
        context={
            "analysis_mode": "english",
            "analysis_fields": fields,
            "evidence_catalog": {},
            "requirement_coverage_plan": {"candidate": candidate},
        },
    )
    assert result.requirement_type == "preferred"


def test_v21_filters_explicit_company_and_product_subjects_only() -> None:
    fields = {
        "description": (
            "Requirements: Python experience is required. "
            "It is an advantage to know Docker. "
            "Our company is a cloud platform for small businesses. "
            "Our goal is to automate routine accounting tasks. "
            "We want AI to examine records and choose tools. "
            "Our company requires candidates to explain system tradeoffs."
        )
    }

    texts = [
        item["text"] for item in build_requirement_coverage_plan_v21(fields).values()
    ]

    assert texts == [
        "Python experience is required.",
        "It is an advantage to know Docker.",
        "Our company requires candidates to explain system tradeoffs.",
    ]
