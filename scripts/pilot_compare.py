from __future__ import annotations

from copy import deepcopy
from typing import Any


VALID = {"PRESERVED", "DEGRADED", "LOST", "MIS_MAPPED", "NOT_REPRESENTABLE", "AMBIGUOUS"}


def _result(feature: str, source: Any, destination: Any, classification: str, method: str, evidence: dict[str, Any]) -> dict[str, Any]:
    if classification not in VALID:
        raise ValueError(classification)
    return {"feature": feature, "source": source, "destination": destination, "classification": classification, "classification_method": method, "evidence": evidence}


def compare(source: dict[str, Any], destination: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    sdoc, ddoc = source.get("document", {}), destination.get("document", {})
    for feature, key in (("document_title", "title"), ("document_language", "language")):
        sv, dv = sdoc.get(key), ddoc.get(key)
        if sv is None:
            continue
        if dv == sv:
            cls, reason = "PRESERVED", "exact metadata value"
        elif dv is None:
            cls, reason = "LOST", "destination metadata field is absent"
        else:
            cls, reason = "DEGRADED", "destination metadata value differs"
        results.append(_result(feature, sv, dv, cls, "deterministic exact comparison", {"reason": reason}))

    shead = source.get("headings", [])
    dhead = destination.get("headings", [])
    destination_text = destination.get("pdf_text", "")
    for i, item in enumerate(shead):
        dest = dhead[i] if i < len(dhead) else None
        text_verified = bool(item.get("text")) and item.get("text") in destination_text
        if dest is None:
            cls, reason = "LOST", "no destination heading at the source order position"
        elif dest.get("level") == item.get("level") and text_verified:
            cls, reason = "PRESERVED", "heading role/level is present and visible text is independently verified in page text"
        elif dest.get("text") == item.get("text") and dest.get("level") == item.get("level"):
            cls, reason = "PRESERVED", "heading text and level match at the same order position"
        elif text_verified:
            cls, reason = "DEGRADED", "heading text survives in page text but the destination heading level differs"
        elif dest.get("text") == item.get("text"):
            cls, reason = "DEGRADED", "heading text survives but level differs"
        elif any(x.get("text") == item.get("text") for x in dhead):
            cls, reason = "MIS_MAPPED", "heading text survives but is associated with a different order position"
        else:
            cls, reason = "LOST", "source heading text is absent"
        results.append(_result(f"heading[{i}]", item, dest, cls, "deterministic order/text/level comparison", {"reason": reason}))

    sfig = source.get("figures", [])
    dfig = destination.get("figures", [])
    for i, item in enumerate(sfig):
        dest = dfig[i] if i < len(dfig) else None
        if dest is None:
            cls, reason = "LOST", "no destination figure at the source order position"
        elif dest.get("alt") == item.get("alt") and dest.get("decorative") == item.get("decorative"):
            cls, reason = "PRESERVED", "alternative text and non-decorative state match"
        elif dest.get("alt") and dest.get("alt") != item.get("alt"):
            cls, reason = "DEGRADED", "destination figure has alternative text but not the source text"
        elif dest.get("decorative") and not item.get("decorative"):
            cls, reason = "LOST", "meaningful source figure is marked decorative or has no usable alternative text"
        else:
            cls, reason = "AMBIGUOUS", "figure exists but evidence does not establish its semantic association"
        results.append(_result(f"figure_alt[{i}]", item, dest, cls, "deterministic figure-order and alt comparison", {"reason": reason}))

    slist = source.get("lists", [])
    raw_dlist = destination.get("lists", [])
    if destination.get("format") != "pdf":
        dlist = raw_dlist
    else:
        dlist = []
        current_list_type = "unordered"
        for row in raw_dlist:
            if row.get("type") == "list":
                numbering = str(row.get("evidence", {}).get("object", ""))
                current_list_type = "ordered" if "ListNumbering': '/Decimal" in numbering else "unordered"
            elif row.get("type") == "LI":
                item = dict(row)
                item["type"] = current_list_type
                # The extractor's walk depth counts both the L and LI nodes;
                # ASIR list depth counts only nested list containers.
                item["depth"] = max(int(row.get("depth", 0)) - 2, 0)
                dlist.append(item)
    for i, item in enumerate(slist):
        dest = dlist[i] if i < len(dlist) else None
        text_verified = bool(item.get("text")) and item.get("text") in destination_text
        if dest is None:
            cls, reason = "LOST", "no destination list item at the source order position"
        elif all(dest.get(k) == item.get(k) for k in ("type", "depth", "text", "parent")):
            cls, reason = "PRESERVED", "list type, nesting depth, text, and parent match"
        elif text_verified and dest.get("type") == item.get("type") and dest.get("depth") == item.get("depth"):
            cls, reason = "PRESERVED", "list role/type/depth/order are present and each source item is independently verified in page text"
        elif text_verified and dest.get("type") == item.get("type"):
            cls, reason = "DEGRADED", "list item text and type survive but nesting depth differs"
        elif dest.get("text") == item.get("text") and dest.get("type") == item.get("type") and dest.get("parent") == item.get("parent"):
            cls, reason = "DEGRADED", "list item survives but nesting depth differs"
        elif text_verified:
            cls, reason = "MIS_MAPPED", "list item text survives but type or parent relationship differs"
        elif dest.get("text") == item.get("text"):
            cls, reason = "MIS_MAPPED", "list item survives but type or parent relationship differs"
        else:
            cls, reason = "LOST", "source list item text is absent"
        results.append(_result(f"list_item[{i}]", item, dest, cls, "deterministic list sequence/type/depth/parent comparison", {"reason": reason}))

    stables = source.get("tables", [])
    dtables = destination.get("tables", [])
    for i, item in enumerate(stables):
        dest = next((row for row in dtables if row.get("evidence", {}).get("pdf_role") == "Table"), None)
        cells = [row for row in dtables if row.get("role") in {"TH", "TD"}]
        header_cells = [row for row in cells if row.get("role") == "TH"]
        expected_cell_count = int(item.get("dimensions", {}).get("rows", 0)) * int(item.get("dimensions", {}).get("columns", 0))
        source_cells_verified = all(str(value) in destination_text for row in item.get("cells", []) for value in row)
        table_structure_verified = dest is not None and len(cells) == expected_cell_count and len(header_cells) == len(item.get("headers", []))
        if dest is None:
            cls, reason = "LOST", "no destination table at the source order position"
        elif table_structure_verified and source_cells_verified:
            cls, reason = "PRESERVED", "Table/TH/TD structure and header count are present; source cell text is independently verified in page text"
        elif all(dest.get(k) == item.get(k) for k in ("dimensions", "cells", "headers", "header_row")):
            cls, reason = "PRESERVED", "table dimensions, cell order, header row, and header cells match"
        elif dest.get("cells") == item.get("cells") and not dest.get("headers"):
            cls, reason = "DEGRADED", "table cells survive but header semantics are absent"
        elif dest.get("dimensions") == item.get("dimensions") and dest.get("headers") != item.get("headers"):
            cls, reason = "MIS_MAPPED", "table shape survives but header/data relationship differs"
        elif dest.get("cells"):
            cls, reason = "DEGRADED", "some table structure survives but content or relationships differ"
        else:
            cls, reason = "LOST", "no equivalent table structure remains"
        results.append(_result(f"table[{i}]", item, dest, cls, "deterministic table shape/cell/header comparison", {"reason": reason}))
    return results


def synthetic_cases() -> dict[str, bool]:
    base = {
        "document": {"title": "T", "language": "en-US"},
        "headings": [{"text": "A", "level": 1}],
        "figures": [{"identifier": "figure-1", "alt": "A meaningful figure", "decorative": False}],
        "lists": [{"type": "unordered", "depth": 0, "text": "A", "parent": None}],
        "tables": [{"dimensions": {"rows": 2, "columns": 2}, "cells": [["H", "V"], ["a", "b"]], "headers": ["H", "V"], "header_row": 0}],
    }
    cases = {
        "PRESERVED": deepcopy(base),
        "DEGRADED": deepcopy(base),
        "LOST": deepcopy(base),
        "MIS_MAPPED": deepcopy(base),
    }
    cases["DEGRADED"]["headings"][0]["level"] = 2
    cases["LOST"]["figures"] = []
    cases["MIS_MAPPED"]["lists"][0]["parent"] = "wrong"
    observed: dict[str, bool] = {}
    for expected, dest in cases.items():
        rows = compare(base, dest)
        observed[expected] = any(row["classification"] == expected for row in rows)
    return observed
