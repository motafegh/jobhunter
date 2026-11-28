"""Exercise the frozen fictional E2 contract example with actual A2 reconciliation.

Only authored statements, not a model result or source-first quality assessment.
The earlier example's child references are explicitly mapped to enclosing groups
because this slice exposes group handles, not child-excerpt binding.
"""

from __future__ import annotations

import json
from copy import deepcopy
from html import escape
from pathlib import Path

from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.jobinja_details import _strip_html
from jobhunter.p16_lab import ROOT, canonical, checked_path, digest, load_requirements
from jobhunter.p16_lab_a2_context import packet_for_case
from jobhunter.p16_lab_a2_semantic import candidate_view, reconcile_response, request_scope
from jobhunter.p16_lab_inputs import BoundCase
from jobhunter.translation_store import TranslationSourceVersion

EXAMPLES = "docs/working-memory/2026-11-26_p16_e2/SEMANTIC_CONTRACT_EXAMPLES.json"


def verify(root: Path = ROOT):
    freeze, _ = load_requirements(root)
    path = checked_path(root, EXAMPLES)
    raw_example = path.read_bytes()
    assert digest(raw_example) == freeze["design_inputs_sha256"][EXAMPLES]
    example = json.loads(raw_example)
    fields = deepcopy(example["source"]["fields"])
    lines = fields["description"].splitlines()
    markup = "".join("<p>" + escape(line) + "</p>" for line in lines)
    html = (
        '<script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": markup})
        + "</script>"
    ).encode()
    fields["description"] = _strip_html(markup)
    source = TranslationSourceVersion("authored-e2-a2", 1, _semantic_sha256(fields), "en", fields)
    # L2 does not require a projection; none of this is an actual frozen job.
    b = BoundCase(
        "fictional", "synthetic", "a" * 64, digest(raw_example), source, None, digest(html), html
    )
    p = packet_for_case(b, "L2")
    assert [u["value"] for u in p["units"] if u["kind"] == "description_group"] == lines
    authored = deepcopy(example["illustrative_model_response"])
    children = {"g4a": "g4", "g4b": "g4"}
    for item in authored["statements"]:
        item["evidence"] = list(dict.fromkeys(children.get(h, h) for h in item["evidence"]))
    handles = [u["handle"] for u in p["units"]]
    scope = request_scope(
        p, b, language="L2", run_id="authored-e2-control", request_ordinal=1, handles=handles
    )

    def run(response, execution="completed"):
        raw = canonical(response) if response is not None else None
        r = reconcile_response(p, b, scope, raw, execution=execution)
        v = candidate_view(p, b, scope, raw, r, execution=execution)
        visible = [
            ref
            for c in r["claims"]
            if c["delivery"] == "unreviewed_proposal"
            for ref in c["local_refs"]
        ]
        return r, v, visible

    r, v, visible = run(authored)
    assert len(visible) == 10 and len(r["relations"]) == 2
    assert all(c["semantic_assessment"] == "unreviewed" for c in r["claims"])
    assert not v["whole_candidate_established"] and v["eligibility_summary"] is None
    bad = deepcopy(authored)
    bad["statements"][4]["evidence"] = ["g999"]
    r2, v2, visible2 = run(bad)
    assert "s5" not in visible2 and "s6" not in visible2 and "s9" in visible2
    assert v2["unresolved_relations"] == 1
    empty, source_view, _ = run(None, "budget_stopped")
    assert source_view["delivery"] == "source_only" and source_view["source"]["units"]
    assert empty["execution"] == "budget_stopped" and not empty["absence_established"]
    return {
        "authority": "offline_authored_control_only",
        "fixture_sha256": digest(raw_example),
        "adaptation": "DOM groups; g4a/g4b mapped to parent g4; no exact child claim",
        "statements": len(authored["statements"]),
        "relations": len(authored["relations"]),
        "visible_unreviewed_proposals": len(visible),
        "malformed_group_visible_independent": len(visible2),
        "malformed_group_withheld": ["s5", "s6"],
        "independent_arrangement_retained": "s9" in visible2,
        "source_only_budget_stopped": True,
        "semantic_quality_established": False,
        "real_requests": 0,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
