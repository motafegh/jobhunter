"""Read-only actual frozen source and packet inventory; emit no private content."""

from __future__ import annotations

import json
from collections import Counter

from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.p16_lab import ROOT, load_requirements
from jobhunter.p16_lab_a2_context import model_context, packet_for_case
from jobhunter.p16_lab_inputs import bind_case, bind_cell


def verify(root=ROOT):
    _, protocol = load_requirements(root)
    rows = []
    for c in protocol["cases"]:
        b = bind_case(c["alias"], root)
        original = packet_for_case(b, "L2")
        groups = [u for u in original["units"] if u["kind"] == "description_group"]
        assert (
            "".join(u["separator_before"] + u["value"] for u in groups)
            + original["original_description_tail"]
            == b.source.fields["description"]
        )
        packets = {}
        # All three forms checked offline, not added to experimental schedule.
        for lang in ("L0", "L2", "L3"):
            p = packet_for_case(b, lang)
            context = model_context(p, b, expected_language=lang)
            assert len(context["units"]) == len(p["units"])
            for rep, expected in (
                ("original", b.source.fields),
                ("english_projection", b.projection.fields),
            ):
                units = [u for u in p["units"] if u["representation"] == rep]
                if not units:
                    assert (rep == "original" and lang == "L0") or (
                        rep == "english_projection" and lang == "L2"
                    )
                    continue
                descr = [u for u in units if u["kind"].startswith("description")]
                tail = p[
                    "original_description_tail" if rep == "original" else "english_description_tail"
                ]
                assert (
                    "".join(u.get("separator_before", "") + u["value"] for u in descr) + tail
                    == expected["description"]
                )
                other = [u for u in units if u["kind"] == "source_field"]
                fields = _analysis_fields_for_english(expected)
                for name, value in fields.items():
                    if name == "description":
                        continue
                    vals = [u["value"] for u in other if u["reference"]["field"] == name]
                    if rep == "original" and isinstance(value, list) and value:
                        assert vals == value
                    else:
                        assert vals == [value]
            packets[lang] = {
                "sha256": p["packet_sha256"],
                "units": len(p["units"]),
                "associations": dict(Counter(u["association"] for u in p["units"])),
            }
        rows.append(
            {
                "alias": b.alias,
                "snapshot_group": b.snapshot_group,
                "source_version": b.source.job_detail_version_id,
                "projection_id": b.projection.id,
                "dom_groups": len(groups),
                "native_description": c["native_description_identity"],
                "packets": packets,
            }
        )
    mapped = []
    for cell in protocol["cells"]:
        spec, b = bind_cell(cell["cell_id"], root)
        assert spec == cell
        mapped.append(
            {
                "cell_id": spec["cell_id"],
                "source_version": b.source.job_detail_version_id,
                "projection_id": b.projection.id,
                "snapshot_group": b.snapshot_group,
            }
        )
    assert len(rows) == 12 and len(mapped) == 47
    return {
        "authority": "offline_input_identity_only",
        "cases": rows,
        "cells": mapped,
        "packet_checks": 36,
        "actual_experiment_cells_executed": 0,
        "real_requests": 0,
        "tokenizer_fit_established": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
