"""Bounded browser review surface for the Phase-2 canonical concept registry."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from jobhunter.canonical_registry import (
    AliasProvenanceKind,
    CanonicalRegistryError,
    CanonicalRegistryStore,
    ClaimKind,
    ConceptCategory,
    MappingDisposition,
    build_canonical_registry_service,
    normalize_registry_text,
)
from jobhunter.canonical_registry_review import (
    build_canonical_registry_review_reader,
    list_concept_aliases,
)
from jobhunter.config import Settings
from jobhunter.web.common import TEMPLATES, redirect_with_notice, require_csrf, template_context


def _review_reader(settings: Settings):
    try:
        return build_canonical_registry_review_reader(settings)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


def _filtered_concepts(
    database_path: Path,
    store: CanonicalRegistryStore,
    *,
    category: str,
    status: str,
    query: str,
):
    if category and category not in {item.value for item in ConceptCategory}:
        raise HTTPException(status_code=400, detail="Unsupported registry category")
    if status not in {"active", "deprecated", "all"}:
        raise HTTPException(status_code=400, detail="Unsupported registry status")

    concepts = store.list_concepts(
        category=category or None,
        include_deprecated=status != "active",
        limit=5000,
    )
    if status == "deprecated":
        concepts = tuple(item for item in concepts if item.status == "deprecated")

    normalized_query = normalize_registry_text(query) if query.strip() else ""
    if not normalized_query:
        return concepts

    filtered = []
    for concept in concepts:
        aliases = list_concept_aliases(
            database_path,
            store,
            concept.concept_id,
            include_deprecated=True,
        )
        haystack = " ".join(
            [
                concept.concept_id,
                concept.preferred_label,
                *(alias.alias_text for alias in aliases),
            ]
        )
        if normalized_query in normalize_registry_text(haystack):
            filtered.append(concept)
    return tuple(filtered)


def register_registry_routes(app: FastAPI, settings: Settings) -> None:
    """Attach human-reviewed registry pages and bounded synchronous mutation routes."""

    @app.get("/registry", response_class=HTMLResponse, name="registry_overview")
    def registry_overview(
        request: Request,
        q: str = "",
        category: str = "",
        status: str = "active",
        notice: str = "",
    ):
        store = CanonicalRegistryStore(settings.database_path)
        concepts = _filtered_concepts(
            settings.database_path,
            store,
            category=category,
            status=status,
            query=q,
        )
        claim_counts: Counter[str] = Counter()
        review_error = ""
        try:
            claims = build_canonical_registry_review_reader(settings).list_current_claims(
                mapping_state="all",
                limit=5000,
            )
            claim_counts.update(item.mapping_state for item in claims)
        except ValueError as exc:
            review_error = str(exc)

        return TEMPLATES.TemplateResponse(
            request=request,
            name="registry.html",
            context=template_context(
                request,
                page="registry",
                concepts=concepts,
                categories=tuple(item.value for item in ConceptCategory),
                q=q,
                category=category,
                status=status,
                notice=notice,
                claim_counts=claim_counts,
                review_error=review_error,
            ),
        )

    @app.get(
        "/registry/concepts/{concept_id}",
        response_class=HTMLResponse,
        name="registry_concept_detail",
    )
    def registry_concept_detail(
        request: Request,
        concept_id: str,
        notice: str = "",
    ):
        store = CanonicalRegistryStore(settings.database_path)
        concept = store.get_concept(concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail="Canonical concept not found")
        aliases = list_concept_aliases(
            settings.database_path,
            store,
            concept_id,
            include_deprecated=True,
        )
        review_error = ""
        mappings = ()
        try:
            mappings = build_canonical_registry_review_reader(settings).concept_mappings(
                concept_id,
                limit=500,
            )
        except ValueError as exc:
            review_error = str(exc)
        successors = tuple(
            item
            for item in store.list_concepts(
                category=concept.category,
                include_deprecated=False,
                limit=5000,
            )
            if item.concept_id != concept.concept_id
        )
        return TEMPLATES.TemplateResponse(
            request=request,
            name="registry_concept.html",
            context=template_context(
                request,
                page="registry",
                concept=concept,
                aliases=aliases,
                mappings=mappings,
                successors=successors,
                provenance_kinds=tuple(item.value for item in AliasProvenanceKind),
                notice=notice,
                review_error=review_error,
            ),
        )

    @app.get("/registry/claims", response_class=HTMLResponse, name="registry_claim_queue")
    def registry_claim_queue(
        request: Request,
        job_id: str = "",
        kind: str = "",
        state: str = "pending",
        notice: str = "",
    ):
        if kind and kind not in {item.value for item in ClaimKind}:
            raise HTTPException(status_code=400, detail="Unsupported claim kind")
        allowed_states = {"all", "pending", *(item.value for item in MappingDisposition)}
        if state not in allowed_states:
            raise HTTPException(status_code=400, detail="Unsupported mapping state")

        reader = _review_reader(settings)
        items = reader.list_current_claims(
            source_job_id=job_id or None,
            claim_kind=kind or None,
            mapping_state=state,
            limit=500,
        )
        store = CanonicalRegistryStore(settings.database_path)
        active_concepts = store.list_concepts(limit=5000)
        responsibility_concepts = tuple(
            item for item in active_concepts if item.category == ConceptCategory.RESPONSIBILITY
        )
        return TEMPLATES.TemplateResponse(
            request=request,
            name="registry_claims.html",
            context=template_context(
                request,
                page="registry",
                items=items,
                job_id=job_id,
                kind=kind,
                state=state,
                notice=notice,
                active_concepts=active_concepts,
                responsibility_concepts=responsibility_concepts,
                claim_kinds=tuple(item.value for item in ClaimKind),
                mapping_states=("all", "pending", *(item.value for item in MappingDisposition)),
            ),
        )

    @app.post("/registry/concepts")
    def create_registry_concept(
        request: Request,
        csrf_token: Annotated[str, Form()],
        concept_id: Annotated[str, Form()],
        category: Annotated[str, Form()],
        preferred_label: Annotated[str, Form()],
        reason: Annotated[str, Form()],
        description: Annotated[str, Form()] = "",
    ):
        require_csrf(request, csrf_token)
        try:
            concept = CanonicalRegistryStore(settings.database_path).create_concept(
                concept_id=concept_id,
                category=category,
                preferred_label=preferred_label,
                description=description or None,
                reviewed_at=datetime.now(UTC),
                review_note=reason,
            )
        except (CanonicalRegistryError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return redirect_with_notice(
            f"/registry/concepts/{concept.concept_id}",
            f"Reviewed concept {concept.concept_id}",
        )

    @app.post("/registry/concepts/{concept_id}/aliases")
    def add_registry_alias(
        request: Request,
        concept_id: str,
        csrf_token: Annotated[str, Form()],
        alias_text: Annotated[str, Form()],
        provenance: Annotated[str, Form()],
        reference: Annotated[str, Form()],
        reason: Annotated[str, Form()],
    ):
        require_csrf(request, csrf_token)
        try:
            alias = CanonicalRegistryStore(settings.database_path).add_alias(
                concept_id,
                alias_text=alias_text,
                provenance_kind=provenance,
                provenance_reference=reference,
                reviewed_at=datetime.now(UTC),
                review_note=reason,
            )
        except (CanonicalRegistryError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return redirect_with_notice(
            f"/registry/concepts/{concept_id}",
            f"Reviewed alias {alias.alias_text}",
        )

    @app.post("/registry/concepts/{concept_id}/deprecate")
    def deprecate_registry_concept(
        request: Request,
        concept_id: str,
        csrf_token: Annotated[str, Form()],
        reason: Annotated[str, Form()],
        successor_concept_id: Annotated[str, Form()] = "",
    ):
        require_csrf(request, csrf_token)
        try:
            concept = CanonicalRegistryStore(settings.database_path).deprecate_concept(
                concept_id,
                successor_concept_id=successor_concept_id or None,
                reviewed_at=datetime.now(UTC),
                review_note=reason,
            )
        except (CanonicalRegistryError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return redirect_with_notice(
            f"/registry/concepts/{concept_id}",
            f"Deprecated concept {concept.concept_id}",
        )

    @app.post("/registry/claims/decide")
    def decide_registry_claim(
        request: Request,
        csrf_token: Annotated[str, Form()],
        job_id: Annotated[str, Form()],
        kind: Annotated[str, Form()],
        claim_index: Annotated[int, Form()],
        disposition: Annotated[str, Form()],
        reason: Annotated[str, Form()],
        canonical_concept_id: Annotated[str, Form()] = "",
    ):
        require_csrf(request, csrf_token)
        if claim_index < 0:
            raise HTTPException(status_code=400, detail="claim index must not be negative")
        try:
            disposition_value = MappingDisposition(disposition)
            concept_id = canonical_concept_id.strip() or None
            if disposition_value == MappingDisposition.MAPPED and concept_id is None:
                raise CanonicalRegistryError("mapped disposition requires a canonical concept")
            if disposition_value != MappingDisposition.MAPPED and concept_id is not None:
                raise CanonicalRegistryError(
                    "unmapped/rejected dispositions cannot reference a canonical concept"
                )
            mapping = build_canonical_registry_service(settings).record_current_claim_mapping(
                job_id,
                claim_kind=kind,
                claim_index=claim_index,
                disposition=disposition_value,
                canonical_concept_id=concept_id,
                reviewed_at=datetime.now(UTC),
                review_note=reason,
            )
        except (CanonicalRegistryError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return redirect_with_notice(
            f"/registry/claims?{urlencode({'job_id': job_id, 'state': 'all'})}",
            f"Recorded {mapping.disposition} for {mapping.claim_kind}[{mapping.claim_index}]",
        )
