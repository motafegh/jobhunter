"""Human-facing expert interpretation built above JobHunter's strict analytical layers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.role_blueprint_inference import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_models import RoleCapabilityBlueprint
from jobhunter.role_blueprint_store import RoleBlueprintArtifact, RoleBlueprintStore
from jobhunter.translation_store import TranslationStore

BLUEPRINT_PROMPT_VERSION = "role-capability-blueprint-v2"
BLUEPRINT_SCHEMA_VERSION = "role-capability-blueprint-v1"

_SYSTEM_PROMPT = """You are JobHunter's senior practitioner/domain-specialist role analyst.

MISSION
Read the COMPLETE vacancy and company context and explain what this position probably requires in
practice. Adopt the professional frame that actually matches the vacancy: software engineer for
software work, ML practitioner for ML work, content/media specialist for content work, operations
specialist for operational work, etc. Do not force every role into software-engineering language.

YOU ARE NOT THE AUDIT LAYER
JobHunter already has strict extraction and evidence-qualified Capability Intelligence. Do not
repeat those artifacts in a different format. They are context and provenance, not a cage.

YOUR JOB IS TO ADD PROFESSIONAL INTERPRETATION
You are explicitly allowed to use relevant domain/technical knowledge to infer likely:
- technical or professional sub-skills;
- practical depth;
- implementation/work patterns;
- APIs/protocols/libraries/frameworks/tools that would be reasonable examples;
- operational concerns and failure modes;
- end-to-end workflows the person may need to build/debug/operate/execute;
- hidden prerequisites that follow from the actual work;
- areas that probably do NOT matter despite belonging to the broader domain.

WHOLE-JOB REASONING
Do not expand keywords independently. Combine title, responsibilities, explicit requirements,
company/domain context, deliverables, integrations, tools, seniority/experience signals and the
existing capability artifact before reaching conclusions.

For example, do NOT reason as:
  Python -> generic Python curriculum
  AI API -> generic API curriculum
Instead reason as:
  Python + AI APIs + document processing + CRM/email integration + business automation
  -> likely integration/application engineering involving HTTP/JSON/authentication, structured
     extraction, validation, workflow orchestration, retries, business rules, logging, human
     review, and maintainable services/scripts.

USEFULNESS RULE
Before keeping a sentence, ask: does this teach something the reader probably cannot obtain by
simply rereading the advertisement? Remove trivial restatement unless it supports a non-obvious
conclusion.

INFERENCE FREEDOM WITH HONESTY
Use professional judgment. Do not suppress a useful inference merely because the employer did not
spell it out. Instead classify the interpretation:
- highly_likely: strongly follows from explicit work, repeated supporting clues, or direct domain
  dependency;
- plausible: a reasonable likely implementation skill/tool/pattern, but alternatives exist;
- speculative: possible and worth mentioning only when it materially helps explain uncertainty.

Do not upgrade plausible implementation choices into employer facts. For tool examples use:
- source_named when actually named in the supplied job context;
- likely_example when it is a strong implementation example;
- possible_example when it is one of several plausible choices.
Suggested examples must never be described as mandatory/required/necessary.

OPTIONALITY AND DEPTH
- Preserve source wording such as expert, familiarity, plus, helpful, preferred, and "we don't
  expect every item". Do not turn a broadly listed stack into a list of mandatory mastery claims.
- If a stack line mixes core and optional tools, discuss those levels separately.
- Do not use words such as mandatory or non-negotiable unless the source or the work dependency
  genuinely warrants that certainty.
- Explain depth operationally rather than forcing one universal beginner/intermediate/expert score.

TECHNICAL / DOMAIN CORRECTNESS
- Preserve the normal meaning of domain metrics, protocols, algorithms, and tools. Do not repurpose
  a process/business metric as an ML evaluation metric or claim a batch orchestrator is a streaming
  engine merely because both appear near the same workflow.
- When several implementation technologies could perform the same function, present examples as
  alternatives rather than pretending one is the hidden company architecture.
- Prefer technically conservative, defensible interpretation over sophisticated-sounding detail.

COMPANY CONTEXT
Use supplied company/domain information when it materially changes the likely work. Do not invent
internal systems, vendors, scale, architecture, policies, or processes that are not supplied. A
company mentioning regulated industries does not prove this particular vacancy or workflow is
regulated; only make that claim when role-relevant evidence supports it.

EVIDENCE-DENSITY DISCIPLINE
The depth of the interpretation should scale with the source. Sparse advertisements should produce
more unknowns and fewer strong technical claims. Rich advertisements may support deeper and more
specific decomposition. Do not manufacture equivalent detail for both.

TECHNOLOGY DECOMPOSITION
When a broad technology is mentioned, answer the useful questions:
- which parts probably matter here?
- how deeply?
- what would the person likely build/do with it?
- which libraries/tools are reasonable examples and why?
- what adjacent concepts are likely necessary?
- what broader-domain topics are probably unnecessary?

END-TO-END SCENARIOS
Infer a few realistic workflows that connect the posting. These are professional interpretations,
not claims about the company's current architecture. Keep each flow technically coherent with the
normal roles of the named/suggested tools.

AVOID GENERIC CURRICULUM DUMPING
Do not list every feature of Python, Docker, networking, LLMs, automation platforms, etc. Include a
sub-skill only when the whole vacancy makes it relevant. Say what probably does not matter when
that helps narrow the role surface.

INPUTS
- analysis_fields: complete hardened English job/company representation.
- accepted_extraction: strict employer-fact extraction.
- capability_intelligence: current auditable capability reasoning. It may be useful but may also be
  shallow or imperfect; improve/reorganize it when the complete job context supports a better
  interpretation.

OUTPUT STYLE
Write for a technically curious human. Be explanatory, specific and practical. Prefer concrete
examples and 'what you would probably need to be able to do' over abstract labels. Keep uncertainty
honest without turning the answer into an evidence report.

BOUNDARY
Describe the JOB, not the reader's current readiness. Do not create a personalized study plan,
application score or candidate-fit decision in this artifact.
"""


class RoleBlueprintError(ValueError):
    """Raised when a job is not ready for the human-facing blueprint layer."""


@dataclass(frozen=True, slots=True)
class RoleBlueprintResult:
    source_job_id: str
    artifact_id: int
    outcome: str
    model: str
    capability_areas: int
    capability_artifact_id: int


class RoleBlueprintService:
    def __init__(
        self,
        *,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        capability_store: CapabilityIntelligenceStore,
        blueprint_store: RoleBlueprintStore,
        provider: RoleBlueprintInferenceProvider,
        analysis_model: str,
        capability_model: str,
        blueprint_model: str,
        max_tokens: int = 8192,
        clock=lambda: datetime.now(UTC),
    ) -> None:
        self._source_store = source_store
        self._analysis_store = analysis_store
        self._capability_store = capability_store
        self._blueprint_store = blueprint_store
        self._provider = provider
        self._analysis_model = analysis_model.strip()
        self._capability_model = capability_model.strip()
        self._blueprint_model = blueprint_model.strip()
        self._max_tokens = max_tokens
        self._clock = clock
        if not self._analysis_model or not self._capability_model or not self._blueprint_model:
            raise ValueError("Concrete analysis/capability/blueprint model identities are required")

    def _dependencies(self, source_job_id: str):
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise RoleBlueprintError("Job has no current successfully parsed source version")

        analysis = self._analysis_store.latest_current(
            source_job_id,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        if analysis is None:
            raise RoleBlueprintError(
                "Run Analyze English before building a Role Capability Blueprint"
            )

        capability = self._capability_store.latest_current(
            source_job_id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if capability is None:
            raise RoleBlueprintError(
                "Build current Capability Intelligence before building a Role Capability Blueprint"
            )
        if capability.job_detail_version_id != source.job_detail_version_id:
            raise RoleBlueprintError(
                "Capability Intelligence is stale for the current source version"
            )
        if capability.analysis_artifact_id != analysis.id:
            raise RoleBlueprintError(
                "Capability Intelligence is stale for the current English analysis"
            )
        if analysis.translation_artifact_id is None:
            raise RoleBlueprintError("English analysis does not reference an English projection")
        if capability.translation_artifact_id != analysis.translation_artifact_id:
            raise RoleBlueprintError(
                "Capability Intelligence and English analysis disagree on projection provenance"
            )

        translation = self._capability_store.translation_dependency(
            capability.translation_artifact_id
        )
        if translation is None:
            raise RoleBlueprintError(
                "Capability Intelligence references a missing English projection"
            )
        if translation.job_detail_version_id != source.job_detail_version_id:
            raise RoleBlueprintError(
                "Referenced English projection is stale for the current source version"
            )
        return source, translation, analysis, capability

    @staticmethod
    def _analysis_fields(fields: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in fields.items()
            if key not in {"language", "parser_version"}
        }

    def build(self, source_job_id: str) -> RoleBlueprintResult:
        source, translation, analysis, capability = self._dependencies(source_job_id)
        attempted_at = self._clock()

        existing = self._blueprint_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            capability_artifact_id=capability.id,
            model=self._blueprint_model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        if existing is not None:
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, "reused")

        analysis_fields = self._analysis_fields(translation.fields)
        user_payload = {
            "source_job_id": source_job_id,
            "analysis_fields": analysis_fields,
            "accepted_extraction": analysis.analysis,
            "capability_intelligence": capability.intelligence,
            "contract": {
                "prompt_version": BLUEPRINT_PROMPT_VERSION,
                "schema_version": BLUEPRINT_SCHEMA_VERSION,
                "capability_artifact_id": capability.id,
            },
        }

        try:
            inference = self._provider.complete(
                system_prompt=_SYSTEM_PROMPT,
                user_payload=user_payload,
                max_tokens=self._max_tokens,
            )
            validated = RoleCapabilityBlueprint.model_validate(inference.blueprint)
            blueprint = validated.model_dump(mode="json")
            artifact_id = self._blueprint_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=inference.model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                blueprint=blueprint,
                request_body=inference.request_body,
                raw_response=inference.raw_response,
                created_at=attempted_at,
            )
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

        artifact = self._blueprint_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            capability_artifact_id=capability.id,
            model=self._blueprint_model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Role Capability Blueprint disappeared after persistence")
        return _result(artifact, "completed")


def build_role_blueprint_service(settings: Settings) -> RoleBlueprintService:
    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No LM Studio analysis model is configured")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    blueprint_model = settings.effective_blueprint_lm_studio_model()
    if not blueprint_model:
        raise ValueError("No LM Studio Role Capability Blueprint model is configured")

    return RoleBlueprintService(
        source_store=TranslationStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        blueprint_store=RoleBlueprintStore(settings.database_path),
        provider=RoleBlueprintInferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=blueprint_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
        blueprint_model=blueprint_model,
        max_tokens=settings.analysis_max_tokens,
    )


def _result(artifact: RoleBlueprintArtifact, outcome: str) -> RoleBlueprintResult:
    return RoleBlueprintResult(
        source_job_id=artifact.source_job_id,
        artifact_id=artifact.id,
        outcome=outcome,
        model=artifact.model,
        capability_areas=len(artifact.blueprint.get("capability_areas") or []),
        capability_artifact_id=artifact.capability_artifact_id,
    )


def format_role_blueprint(artifact: RoleBlueprintArtifact) -> str:
    data = artifact.blueprint
    lines = [
        f"Role Capability Blueprint for {artifact.source_job_id}",
        f"Model: {artifact.model}",
        "",
        "What this role probably is in practice",
        str(data.get("role_read") or ""),
        "",
        "Likely role shape",
        str(data.get("likely_role_shape") or ""),
    ]
    for index, area in enumerate(data.get("capability_areas") or [], start=1):
        lines.extend(
            [
                "",
                f"Area {index}: {area.get('name', '(unnamed)')}",
                f"Interpretation: {area.get('interpretation_strength', '?')}",
                f"Likely depth: {area.get('likely_depth', '')}",
                f"Why it matters: {area.get('why_this_matters', '')}",
            ]
        )
        for label, key in (
            ("Likely subskills", "likely_subskills"),
            ("Likely work products", "likely_work_products"),
            ("Operational concerns", "likely_failure_modes_or_operational_concerns"),
            ("Probably not required", "probably_not_required"),
        ):
            items = area.get(key) or []
            if items:
                lines.append(f"  {label}:")
                lines.extend(f"  - {item}" for item in items)
        tools = area.get("likely_tools_or_examples") or []
        if tools:
            lines.append("  Tools / examples:")
            for tool in tools:
                lines.append(
                    f"  - {tool.get('name', '')} [{tool.get('relationship', '?')}]: "
                    f"{tool.get('why_relevant', '')}"
                )

    hidden = data.get("hidden_requirements") or []
    if hidden:
        lines.extend(["", "Hidden / unstated but likely requirements"])
        lines.extend(
            f"- [{item.get('interpretation_strength', '?')}] {item.get('title', '')}: "
            f"{item.get('explanation', '')}"
            for item in hidden
        )
    scenarios = data.get("likely_end_to_end_scenarios") or []
    if scenarios:
        lines.extend(["", "Likely end-to-end scenarios"])
        for scenario in scenarios:
            lines.append(
                f"- [{scenario.get('interpretation_strength', '?')}] "
                f"{scenario.get('name', '')}: {scenario.get('why_likely', '')}"
            )
            flow_steps = scenario.get("flow_steps") or []
            lines.extend(
                f"    {step_index}. {step}"
                for step_index, step in enumerate(flow_steps, start=1)
            )
    if data.get("what_probably_does_not_matter"):
        lines.extend(["", "What probably does not matter"])
        lines.extend(f"- {item}" for item in data["what_probably_does_not_matter"])
    if data.get("important_unknowns"):
        lines.extend(["", "Important unknowns"])
        lines.extend(f"- {item}" for item in data["important_unknowns"])
    lines.extend(["", "Bottom line", str(data.get("bottom_line") or "")])
    return "\n".join(lines)
