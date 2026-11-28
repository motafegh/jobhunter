"""Compact A2 proposals and deterministic offline reconciliation.

This module checks associations and structure, not entailment. It cannot
dispatch, review, promote or write accepted artifacts.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from jobhunter.p16_lab import canonical, digest
from jobhunter.p16_lab_a2_context import packet_for_case, verify_packet
from jobhunter.p16_lab_inputs import BoundCase

CONTRACT = "p16-e3-a2-semantic-v1"
ENVELOPE = "p16-e3-candidate-envelope-v1"


class Proposal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    ref: str
    meaning: str
    evidence: list[str] = Field(min_length=1)
    basis: Literal["explicit", "inferred", "unresolved"]
    roles: list[str] | None = None
    strength: str | None = None
    depth: str | None = None
    experience: str | None = None
    open_questions: list[str] | None = None

    @model_validator(mode="after")
    def nonempty(self):
        if not self.ref.strip() or not self.meaning.strip():
            raise ValueError("empty statement")
        if any(not v.strip() for v in self.evidence):
            raise ValueError("empty handle")
        return self


class Relation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    type: str
    evidence: list[str] = Field(min_length=1)
    ref: str | None = None
    members: list[str] | None = None
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    scope: str | None = None

    @model_validator(mode="after")
    def shape(self):
        if not self.type.strip() or (self.ref is not None and not self.ref.strip()):
            raise ValueError("empty relation")
        if self.members is not None:
            if self.from_ is not None or self.to is not None or len(self.members) < 2:
                raise ValueError("invalid group")
            if len(set(self.members)) != len(self.members) or not all(
                m.strip() for m in self.members
            ):
                raise ValueError("duplicate or empty members")
        elif not self.from_ or not self.to or self.from_ == self.to:
            raise ValueError("invalid directed relation")
        return self


class SemanticResponse(BaseModel):
    """Model-facing schema; reconciliation validates each entry independently."""

    model_config = ConfigDict(extra="forbid", strict=True)
    statements: list[Proposal]
    relations: list[Relation] | None = None
    open_questions: list[str] | None = None


def request_scope(
    packet: dict,
    bound: BoundCase,
    *,
    language: str,
    run_id: str,
    request_ordinal: int,
    handles: list[str],
) -> dict:
    """Bind a planned logical scope; not a physical dispatch or fit receipt."""
    verify_packet(packet, bound, expected_language=language)
    known = [u["handle"] for u in packet["units"]]
    if (
        not isinstance(run_id, str)
        or not run_id.strip()
        or type(request_ordinal) is not int
        or request_ordinal < 1
        or not isinstance(handles, list)
        or not handles
        or not all(isinstance(h, str) for h in handles)
        or len(set(handles)) != len(handles)
        or handles != [h for h in known if h in handles]
    ):
        raise ValueError("invalid request scope")
    scope = {
        "contract": CONTRACT,
        "run_id": run_id,
        "request_ordinal": request_ordinal,
        "packet_sha256": packet["packet_sha256"],
        "language": language,
        "handles": handles.copy(),
    }
    return {**scope, "scope_sha256": digest(canonical(scope))}


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def _invalid_constant(_):
    raise ValueError("nonfinite JSON constant")


def _parse(raw):
    try:
        obj = json.loads(raw, object_pairs_hook=_unique_pairs, parse_constant=_invalid_constant)
        # Reject lone surrogate strings and non-canonicalizable values.
        json.dumps(obj, ensure_ascii=False, allow_nan=False).encode()
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return None
    if (
        not isinstance(obj, dict)
        or set(obj) - {"statements", "relations", "open_questions"}
        or not isinstance(obj.get("statements"), list)
        or (obj.get("relations") is not None and not isinstance(obj["relations"], list))
        or (
            obj.get("open_questions") is not None
            and (
                not isinstance(obj["open_questions"], list)
                or not all(isinstance(v, str) for v in obj["open_questions"])
            )
        )
    ):
        return None
    return obj


def _ref(raw):
    ref = raw.get("ref") if isinstance(raw, dict) else None
    return ref if isinstance(ref, str) and ref.strip() else None


def _dependencies(raw):
    if not isinstance(raw, dict):
        return []
    members = raw.get("members")
    values = (members if isinstance(members, list) else []) + [raw.get("from"), raw.get("to")]
    return [v for v in values if isinstance(v, str) and v.strip()]


def _held_dependencies(raw):
    # A broken group holds its leaves; a broken directed edge holds its target,
    # not independently stated source work. No inference about unstated edges.
    if not isinstance(raw, dict):
        return []
    members = raw.get("members")
    values = (members if isinstance(members, list) else []) + [raw.get("to")]
    return [v for v in values if isinstance(v, str) and v.strip()]


def reconcile_response(
    packet: dict, bound: BoundCase, scope: dict, raw: bytes | None, *, execution: str
) -> dict:
    """Reconcile one trusted offline logical attempt, retaining independent fragments.

    Caller-owned scope/execution are not model fields. Physical dispatch binding,
    cross-request reconciliation and review are separate integration gates.
    """
    rebuilt = request_scope(
        packet,
        bound,
        language=scope["language"],
        run_id=scope["run_id"],
        request_ordinal=scope["request_ordinal"],
        handles=scope["handles"],
    )
    if scope != rebuilt:
        raise ValueError("request scope identity mismatch")
    if execution not in {"completed", "failed", "budget_stopped", "timeout", "not_attempted"}:
        raise ValueError("unknown execution status")
    if execution == "not_attempted" and raw is not None or execution == "completed" and raw is None:
        raise ValueError("response/execution mismatch")
    if raw is not None and type(raw) is not bytes:
        raise ValueError("exact raw bytes required")
    obj = _parse(raw) if raw is not None else None
    raw_sha = digest(raw) if raw is not None else None
    units = {u["handle"]: u for u in packet["units"]}
    allowed = set(scope["handles"])
    claims = []
    relations = []
    quarantine = []
    held = set()
    claim_by_ref = {}
    relation_by_ref = {}
    if obj is not None:
        raw_claims = obj["statements"]
        raw_relations = obj.get("relations") or []
        counts = Counter(r for v in raw_claims + raw_relations if (r := _ref(v)) is not None)
        for i, item in enumerate(raw_claims):
            ref = _ref(item)
            try:
                proposal = Proposal.model_validate(item)
                if counts[proposal.ref] != 1:
                    raise ValueError("ambiguous_ref")
                if not set(proposal.evidence) <= allowed:
                    raise ValueError("unknown_or_out_of_scope_evidence")
            except ValidationError:
                quarantine.append(
                    {
                        "kind": "statement",
                        "index": i,
                        "ref": ref,
                        "reason": "invalid_statement_shape",
                    }
                )
                continue
            except ValueError as exc:
                quarantine.append({"kind": "statement", "index": i, "ref": ref, "reason": str(exc)})
                continue
            content = proposal.model_dump(exclude_none=True, exclude={"ref"})
            evidence = list(dict.fromkeys(content["evidence"]))
            content["evidence"] = evidence
            content_sha = digest(canonical(content))
            # Exact normalized equivalence only, within this response, not text-only.
            existing = next((c for c in claims if c["content_sha256"] == content_sha), None)
            if existing is None:
                identity = digest(canonical([scope["scope_sha256"], raw_sha, content_sha]))
                existing = {
                    "claim_id": identity,
                    "content_sha256": content_sha,
                    "content": content,
                    "raw_indices": [],
                    "local_refs": [],
                    "normalization": [],
                    "association": [units[h]["association"] for h in evidence],
                    "evidence_surfaces": [
                        "description"
                        if units[h]["kind"].startswith("description")
                        else "structured_skill_tags"
                        if units[h]["reference"].get("field") == "skills"
                        else "source_metadata_or_context"
                        for h in evidence
                    ],
                    "semantic_assessment": "unreviewed",
                    "authority": "candidate_only",
                }
                claims.append(existing)
            if evidence != proposal.evidence:
                existing["normalization"].append(
                    {
                        "raw_index": i,
                        "operation": "deduplicate_identical_evidence_handles",
                    }
                )
            existing["raw_indices"].append(i)
            existing["local_refs"].append(proposal.ref)
            claim_by_ref[proposal.ref] = existing
            if proposal.basis == "unresolved" or set(existing["evidence_surfaces"]) == {
                "structured_skill_tags"
            }:
                # Keep board-only model proposals for review, not as interpreted
                # employer obligations. The exact board observation is in the
                # original source view. Do not rewrite the proposal.
                held.add(proposal.ref)
        valid_rel = {}
        for i, item in enumerate(raw_relations):
            ref = _ref(item)
            try:
                rel = Relation.model_validate(item)
                if ref is not None and counts[ref] != 1:
                    raise ValueError("ambiguous_ref")
                if not set(rel.evidence) <= allowed:
                    raise ValueError("unknown_or_out_of_scope_evidence")
                # Keep unknown types as meaning proposals; structure alone is checked.
                valid_rel[i] = rel
                if ref is not None:
                    relation_by_ref[ref] = i
            except ValidationError:
                quarantine.append(
                    {"kind": "relation", "index": i, "ref": ref, "reason": "invalid_relation_shape"}
                )
                held.update(_held_dependencies(item))
            except ValueError as exc:
                quarantine.append({"kind": "relation", "index": i, "ref": ref, "reason": str(exc)})
                held.update(_held_dependencies(item))

        resolved_groups = {}

        def resolve(ref, trail):
            if ref in claim_by_ref:
                return [claim_by_ref[ref]["claim_id"]]
            index = relation_by_ref.get(ref)
            if index is None or index in trail or index not in valid_rel:
                raise ValueError("missing_or_cyclic_dependency")
            # Nested groups only; a directed semantic link is not an eligibility leaf.
            relation = valid_rel[index]
            if relation.members is None:
                raise ValueError("non_group_dependency")
            if index in resolved_groups:
                return resolved_groups[index]
            # Bound recursive work by the finite number of claims, not by a
            # semantic limit on how many paths the employer may express.
            leaves = []
            seen = set()
            for member in relation.members:
                for leaf in resolve(member, trail | {index}):
                    if leaf in seen:
                        raise ValueError("duplicate_relation_leaf")
                    seen.add(leaf)
                    leaves.append(leaf)
            resolved_groups[index] = leaves
            return leaves

        broken = {}
        for i, rel in valid_rel.items():
            try:
                deps = _dependencies(raw_relations[i])
                leaves = [leaf for ref in deps for leaf in resolve(ref, {i})]
                if len(leaves) != len(set(leaves)):
                    raise ValueError("duplicate_relation_leaf")
                # Every cited relation and leaf remains within this request scope.
                relations.append(
                    {
                        "raw_index": i,
                        "local_ref": rel.ref,
                        "content": rel.model_dump(exclude_none=True, by_alias=True),
                        "claim_ids": leaves,
                        "consistency": "resolved_candidate",
                        "semantic_assessment": "unreviewed",
                    }
                )
            except (ValueError, RecursionError) as exc:
                broken[i] = (
                    "relation_nesting_unresolved" if isinstance(exc, RecursionError) else str(exc)
                )
                held.update(_held_dependencies(raw_relations[i]))
        # Reject cyclic directed dependency chains and group endpoints in
        # directed links (the first slice supports statement-to-statement links).
        graph = {}
        edges = {}
        for i, rel in valid_rel.items():
            if i in broken or rel.members is not None:
                continue
            if rel.from_ not in claim_by_ref or rel.to not in claim_by_ref:
                broken[i] = "directed_group_endpoint_unresolved"
                held.update(_held_dependencies(raw_relations[i]))
                continue
            a, b = (claim_by_ref[r]["claim_id"] for r in (rel.from_, rel.to))
            graph.setdefault(a, set()).add(b)
            edges[i] = (a, b)
        for i, (a, b) in edges.items():
            pending = [b]
            visited = set()
            while pending:
                node = pending.pop()
                if node == a:
                    broken[i] = "cyclic_directed_dependency"
                    held.update(_held_dependencies(raw_relations[i]))
                    break
                if node not in visited:
                    visited.add(node)
                    pending.extend(graph.get(node, ()))
        relations = [r for r in relations if r["raw_index"] not in broken]
        # Propagate unresolved group dependencies to all group leaves, including
        # nested groups and duplicate aliases. A bad directed edge holds its target.
        changed = True
        while changed:
            before = set(held)
            for ref in list(held):
                if ref in claim_by_ref:
                    held.update(claim_by_ref[ref]["local_refs"])
                if ref in relation_by_ref:
                    held.update(_held_dependencies(raw_relations[relation_by_ref[ref]]))
            for i, item in enumerate(raw_relations):
                if i in broken or any(ref in held for ref in _dependencies(item)):
                    held.update(_held_dependencies(item))
                    if _ref(item):
                        held.add(_ref(item))
            changed = before != held
        for i, reason in broken.items():
            quarantine.append(
                {"kind": "relation", "index": i, "ref": _ref(raw_relations[i]), "reason": reason}
            )
        for relation in relations:
            if any(ref in held for ref in _dependencies(raw_relations[relation["raw_index"]])):
                relation["consistency"] = "unresolved"
            relation["relation_sha256"] = digest(canonical(relation))
    for claim in claims:
        if set(claim["evidence_surfaces"]) == {"structured_skill_tags"}:
            claim["delivery"] = "withheld_board_only"
        else:
            claim["delivery"] = (
                "withheld_dependency" if set(claim["local_refs"]) & held else "unreviewed_proposal"
            )
    linked = {
        h
        for c in claims
        if c["delivery"] == "unreviewed_proposal"
        for h in c["content"]["evidence"]
    }
    coverage = [
        {
            "handle": u["handle"],
            "execution": execution if u["handle"] in allowed else "not_attempted",
            "association": u["association"],
            "coverage": "linked_candidate" if u["handle"] in linked else "unresolved",
            "material_meaning_coverage": "unreviewed",
        }
        for u in packet["units"]
    ]
    visible = [c["claim_id"] for c in claims if c["delivery"] == "unreviewed_proposal"]
    # Deliberately conservative: no whole-candidate claim until planned work and
    # material dependencies are integrated across requests. Empty is not absence.
    record = {
        "contract": ENVELOPE,
        "semantic_contract": CONTRACT,
        "authority": "candidate_only",
        "scope": scope,
        "raw_sha256": raw_sha,
        "execution": execution,
        "response_state": "parsed"
        if obj is not None
        else ("invalid_envelope" if raw is not None else "no_response"),
        "claims": claims,
        "relations": relations,
        "quarantine": quarantine,
        "open_questions": obj.get("open_questions") or [] if obj is not None else [],
        "coverage": coverage,
        "delivery": "qualified_partial" if visible else "source_only",
        "visible_proposal_ids": visible,
        "semantic_assessment": "unreviewed",
        "whole_candidate_established": False,
        "absence_established": False,
        "eligibility_summary": None,
        "actual_experiment_cell": False,
    }
    return {**record, "revision_sha256": digest(canonical(record))}


def candidate_view(
    packet: dict, bound: BoundCase, scope: dict, raw: bytes | None, record: dict, *, execution: str
) -> dict:
    """Read-only verified proposal/source view, never a supported-facts view.

    Rebuild against the exact supplied current binding. An independently valid
    original remains available even when the scoped response is empty or fails.
    """
    if reconcile_response(packet, bound, scope, raw, execution=execution) != record:
        raise ValueError("candidate revision mismatch")
    original = packet_for_case(bound, "L2")
    known = {u["handle"]: u for u in packet["units"]}
    proposals = []
    for c in record["claims"]:
        if c["delivery"] != "unreviewed_proposal":
            continue
        proposals.append(
            {
                "claim_id": c["claim_id"],
                "proposal": c["content"],
                "label": "unreviewed_model_proposal_not_established_fact",
                "evidence": [known[h] for h in c["content"]["evidence"]],
                "employer_obligation_established": False,
            }
        )
    return {
        "authority": "candidate_only",
        "execution": execution,
        "delivery": record["delivery"],
        "source": original,
        "proposals": proposals,
        "unresolved_relations": sum(r["consistency"] == "unresolved" for r in record["relations"])
        + sum(q["kind"] == "relation" for q in record["quarantine"]),
        "coverage": record["coverage"],
        "eligibility_summary": None,
        "absence_established": False,
        "semantic_assessment": "unreviewed",
        "whole_candidate_established": False,
        "revision_sha256": record["revision_sha256"],
    }
