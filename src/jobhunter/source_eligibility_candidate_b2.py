"""Bounded, source-exact B2 conditional eligibility graph candidates.

Only two explicit, recognizable source forms are handled:
* Middle/Senior eligibility tracks with within-track conditions and one-of domains;
* certificate OR equivalent knowledge within a required qualification.

Other forms remain unresolved rather than being flattened to global requirements.
All graph semantics are unreviewed and unsuitable for applicant eligibility
or downstream accepted facts. Does not invoke an LLM or modify persistence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from jobhunter.source_item_candidate_b2 import (
    B2SourceCandidate,
    SourceItemCandidate,
    verify_b2_candidate,
)
from jobhunter.source_span_identity import OriginalSourceAnchor, bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

LogicScope = Literal["alternative_path", "chosen_option"]
_TRACK_LABEL = re.compile(r"سطح\s+(Middle|Senior|میانی|ارشد)\s*[:：]", re.I)
_YEARS = re.compile(r"^(?:دارا\s+بودن|داشتن)\s+.+?\s+سال\s+تجربه\s+کاری\s+مرتبط", re.I)
_ONE_OF = re.compile(r"یکی\s+از\s+حوزه[‌\s]*های\s+", re.I)
_EQUIVALENT = re.compile(r"(گواهینامه)\s+یا\s+(دانش\s+معادل)", re.I)
_TOKEN = re.compile(r"[^\W_][\w+ .\-/]{0,65}\Z", re.UNICODE)


@dataclass(frozen=True, slots=True)
class EligibilityLeaf:
    anchor: OriginalSourceAnchor
    scope: LogicScope
    label: str


@dataclass(frozen=True, slots=True)
class EligibilityGraphCandidate:
    graph_id: str
    basis_anchor_ids: tuple[str, ...]
    root_id: str
    nodes: tuple[dict, ...]
    leaves: tuple[EligibilityLeaf, ...]
    interpretation_state: str = "candidate_unreviewed_not_eligibility_authority"


@dataclass(frozen=True, slots=True)
class EligibilityLogicResult:
    graphs: tuple[EligibilityGraphCandidate, ...]
    unresolved_group_kinds: tuple[str, ...]


class _NotEstablished(ValueError):
    """Structural cue not sufficient to infer the full nested graph."""


def _anchor(
    source: TranslationSourceVersion, unit: SourceItemCandidate, fragment: str
) -> OriginalSourceAnchor:
    original = unit.anchor.exact_text
    fragment = fragment.strip()
    at = original.find(fragment)
    if not fragment or at < 0 or original.find(fragment, at + 1) >= 0:
        raise _NotEstablished("Expected unique exact text fragment")
    start = unit.anchor.char_start + at
    return bind_original_source_span(source, char_start=start, char_end=start + len(fragment))


def _leaf(
    source: TranslationSourceVersion,
    unit: SourceItemCandidate,
    text: str,
    scope: LogicScope,
    label: str,
) -> EligibilityLeaf:
    return EligibilityLeaf(anchor=_anchor(source, unit, text), scope=scope, label=label)


def _track_parts(
    source: TranslationSourceVersion, unit: SourceItemCandidate, level: str
) -> tuple[list[EligibilityLeaf], dict[str, list[str]]]:
    """Return original-exact necessary conditions; abort on unsupported syntax."""
    text = unit.anchor.exact_text
    years = _YEARS.match(text)
    if years is None or not unit.employer_strength == "required":
        raise _NotEstablished("No supported explicit relevant-years clause")
    years_frag = years.group()
    leaves = [_leaf(source, unit, years_frag, "alternative_path", level + "_years")]
    conditions: dict[str, list[str]] = {"parts": [level + "_years"]}
    remainder = text[years.end() :].strip()
    if level == "middle":
        if not remainder.startswith("، به همراه "):
            raise _NotEstablished("Missing within-track conjunction")
        rem = remainder[len("، به همراه ") :]
        divider = re.search(r"\s+و\s+(?=حداقل\s+\S+\s+پروژه)", rem)
        if divider is None:
            raise _NotEstablished("Missing required project conjunction")
        domain_clause = rem[: divider.start()].strip()
        project = rem[divider.end() :].strip()
        one_of = _ONE_OF.search(domain_clause)
        if one_of is None or not domain_clause.startswith("تجربه عملی "):
            raise _NotEstablished("Missing explicit one-of-domain scope")
        domains = domain_clause[one_of.end() :]
        values = [x.strip() for x in domains.split("،")]
        if not (2 <= len(values) <= 8) or not all(
            value
            and _TOKEN.fullmatch(value)
            and not re.search(r"(?<!\w)(?:یا|or)(?!\w)", value, re.I)
            for value in values
        ):
            raise _NotEstablished("Domain options cannot be uniquely parsed")
        if not project.startswith("حداقل") or "پروژه" not in project:
            raise _NotEstablished("Project condition not explicit")
        leaves.append(_leaf(source, unit, domain_clause, "alternative_path", "middle_domain_scope"))
        for i, value in enumerate(values):
            leaves.append(_leaf(source, unit, value, "chosen_option", f"domain_{i}"))
        leaves.append(_leaf(source, unit, project, "alternative_path", "middle_project"))
        conditions["parts"] = ["middle_years", "middle_domain_choice", "middle_project"]
        conditions["domain_labels"] = [f"domain_{i}" for i in range(len(values))]
    else:
        if not remainder.startswith("، تجربه طراحی "):
            raise _NotEstablished("Missing senior design/deployment conjunction")
        deployment = remainder[len("، ") :].strip()
        if "Production Deployment" not in deployment or "حداقل یک سیستم" not in deployment:
            raise _NotEstablished("Incomplete senior production condition")
        leaves.append(_leaf(source, unit, deployment, "alternative_path", "senior_deployment"))
        conditions["parts"].append("senior_deployment")
    return leaves, conditions


def _seniority_graph(
    source: TranslationSourceVersion,
    candidate: B2SourceCandidate,
    group: tuple[str, ...],
) -> EligibilityGraphCandidate:
    items = [item for item in candidate.items if item.anchor.anchor_id in group]
    if len(items) != 2:
        raise _NotEstablished("Exactly two source-owned tracks required")
    tracks: dict[str, SourceItemCandidate] = {}
    for item in items:
        m = _TRACK_LABEL.search(item.heading or "")
        if m is None:
            raise _NotEstablished("No explicitly delimited seniority heading")
        level = "middle" if m.group(1).casefold() in ("middle", "میانی") else "senior"
        if level in tracks:
            raise _NotEstablished("Duplicate seniority track")
        tracks[level] = item
    if set(tracks) != {"middle", "senior"}:
        raise _NotEstablished("Missing middle or senior alternative")
    middle, mparts = _track_parts(source, tracks["middle"], "middle")
    senior, sparts = _track_parts(source, tracks["senior"], "senior")
    all_leaves = tuple(middle + senior)
    if len({x.anchor.anchor_id for x in all_leaves}) != len(all_leaves):
        raise _NotEstablished("Duplicated conditional leaf")

    nodes: list[dict] = [
        {"id": "tracks", "operator": "any_of", "children": ["middle", "senior"]},
        {"id": "middle", "operator": "all_of", "children": mparts["parts"]},
        {"id": "senior", "operator": "all_of", "children": sparts["parts"]},
        {
            "id": "middle_domain_choice",
            "operator": "any_of",
            "children": mparts["domain_labels"],
        },
    ]
    # The domain scope itself is evidence supporting the choice, not
    # a separately satisfied eligibility condition.
    nodes.extend(
        {"id": leaf.label, "operator": "item", "anchor_id": leaf.anchor.anchor_id}
        for leaf in all_leaves
        if leaf.label != "middle_domain_scope"
    )
    return EligibilityGraphCandidate(
        graph_id="candidate_middle_or_senior",
        basis_anchor_ids=(
            tracks["middle"].anchor.anchor_id,
            tracks["senior"].anchor.anchor_id,
            next(leaf.anchor.anchor_id for leaf in middle if leaf.label == "middle_domain_scope"),
        ),
        root_id="tracks",
        nodes=tuple(nodes),
        leaves=all_leaves,
    )


def _equivalent_graph(
    source: TranslationSourceVersion, candidate: B2SourceCandidate, group: tuple[str, ...]
) -> EligibilityGraphCandidate:
    items = [x for x in candidate.items if x.anchor.anchor_id in group]
    if len(items) != 1 or items[0].employer_strength != "required":
        raise _NotEstablished("Equivalent credentials not in explicit qualification")
    m = _EQUIVALENT.search(items[0].anchor.exact_text)
    if m is None:
        raise _NotEstablished("No exact certificate/equivalent option")
    cert = _leaf(source, items[0], m.group(1), "chosen_option", "certificate")
    knowledge = _leaf(source, items[0], m.group(2), "chosen_option", "knowledge")
    return EligibilityGraphCandidate(
        graph_id="candidate_certificate_or_knowledge",
        basis_anchor_ids=(items[0].anchor.anchor_id,),
        root_id="credential_choice",
        nodes=(
            {"id": "credential_choice", "operator": "any_of", "children": ["cert", "knowledge"]},
            {"id": "cert", "operator": "item", "anchor_id": cert.anchor.anchor_id},
            {"id": "knowledge", "operator": "item", "anchor_id": knowledge.anchor.anchor_id},
        ),
        leaves=(cert, knowledge),
    )


def build_candidate_eligibility_logic(
    source: TranslationSourceVersion, candidate: B2SourceCandidate
) -> EligibilityLogicResult:
    """Fail open to uncertainty, never to globally required conditions.

    No graph is created when partial syntax cannot prove *all* its leaves.
    All returned graphs are still semantic candidates, not accepted policy.
    """
    verify_b2_candidate(candidate, source)
    completed: list[EligibilityGraphCandidate] = []
    unknown: list[str] = []
    for group in candidate.alternatives:
        try:
            if group.kind == "seniority_tracks":
                graph = _seniority_graph(source, candidate, group.source_anchor_ids)
            elif group.kind == "certificate_or_equivalent_knowledge":
                graph = _equivalent_graph(source, candidate, group.source_anchor_ids)
            else:
                # An explicit one-of clause inside a track is represented by
                # the full seniority graph, not a second independent demand.
                continue
        except _NotEstablished:
            unknown.append(group.kind)
            continue
        completed.append(graph)
    if any(
        group.kind == "one_of_technical_domains" for group in candidate.alternatives
    ) and not any(graph.graph_id == "candidate_middle_or_senior" for graph in completed):
        unknown.append("one_of_technical_domains")
    return EligibilityLogicResult(
        graphs=tuple(completed),
        unresolved_group_kinds=tuple(dict.fromkeys(unknown)),
    )


__all__ = [
    "EligibilityLeaf",
    "EligibilityGraphCandidate",
    "EligibilityLogicResult",
    "build_candidate_eligibility_logic",
]
