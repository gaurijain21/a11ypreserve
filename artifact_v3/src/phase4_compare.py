from __future__ import annotations

"""Two-axis Phase 4 comparator.

The legacy pilot comparator remains unchanged for historical reports. This
module handles the frozen Phase 4 ASIR shape and returns both preservation
fidelity and destination accessibility.
"""

from typing import Any

FIDELITY = {"EXACT_PRESERVATION", "SEMANTICALLY_EQUIVALENT", "PARTIAL_PRESERVATION", "MUTATED", "REGENERATED", "LOST", "NOT_REPRESENTABLE", "NOT_APPLICABLE", "MEASUREMENT_ERROR", "INVALID_CONVERSION"}
ACCESSIBILITY = {"ACCESSIBLE_EQUIVALENT", "ACCESSIBLE_BUT_ALTERED", "DEGRADED_ACCESSIBILITY", "INACCESSIBLE_FEATURE", "UNKNOWN"}


def result(feature: str, source: Any, destination: Any, fidelity: str, destination_accessibility: str, evidence: list[dict[str, Any]], confidence: str = "high", notes: str = "") -> dict[str, Any]:
    if fidelity not in FIDELITY:
        raise ValueError(fidelity)
    if destination_accessibility not in ACCESSIBILITY:
        raise ValueError(destination_accessibility)
    return {"feature": feature, "source_value": source, "destination_value": destination, "destination_representation": destination, "fidelity_classification": fidelity, "destination_accessibility": destination_accessibility, "evidence": evidence, "confidence": confidence, "notes": notes}


def classify_observation(source: Any, destination: Any, *, exact: bool = False, equivalent: bool = False, partial: bool = False, mutated: bool = False, regenerated: bool = False, representable: bool = True, measured: bool = True, valid_conversion: bool = True, feature: str = "feature", evidence: list[dict[str, Any]] | None = None, notes: str = "") -> dict[str, Any]:
    evidence = evidence or []
    if not valid_conversion:
        fidelity, access = "INVALID_CONVERSION", "UNKNOWN"
    elif not measured:
        fidelity, access = "MEASUREMENT_ERROR", "UNKNOWN"
    elif exact:
        fidelity, access = "EXACT_PRESERVATION", "ACCESSIBLE_EQUIVALENT"
    elif equivalent:
        fidelity, access = "SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT"
    elif partial:
        fidelity, access = "PARTIAL_PRESERVATION", "DEGRADED_ACCESSIBILITY"
    elif mutated:
        fidelity, access = "MUTATED", "ACCESSIBLE_BUT_ALTERED"
    elif regenerated:
        fidelity, access = "REGENERATED", "ACCESSIBLE_BUT_ALTERED"
    elif not representable:
        fidelity, access = "NOT_REPRESENTABLE", "UNKNOWN"
    elif destination is None or destination == [] or destination == {}:
        fidelity, access = "LOST", "INACCESSIBLE_FEATURE"
    else:
        fidelity, access = "MEASUREMENT_ERROR", "UNKNOWN"
    return result(feature, source, destination, fidelity, access, evidence, notes=notes)


def _one(source_items: list[dict[str, Any]], destination_items: list[dict[str, Any]], key: str = "") -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    matched = []
    missing = []
    for item in source_items:
        candidate = next((value for value in destination_items if value.get(key) == item.get(key)) if key else (destination_items[0] if destination_items else None), None)
        if candidate is None:
            missing.append(item)
        else:
            matched.append((item, candidate))
    return matched, missing


def compare_feature(source: dict[str, Any], destination: dict[str, Any], feature: str) -> dict[str, Any]:
    sdoc, ddoc = source.get("document", {}), destination.get("document", {})
    evidence = [{"source": source.get("extraction", {}), "destination": destination.get("extraction", {})}]
    if destination.get("invalid_conversion"):
        return classify_observation(sdoc, destination, feature=feature, valid_conversion=False, evidence=evidence, notes="destination validation marked the output invalid")
    if feature == "headings":
        src, dst = source.get("headings", []), destination.get("headings", [])
        src_levels = [item.get("level") for item in src]
        dst_levels = [item.get("level") for item in dst]
        evidence.append({"source_heading_levels": src_levels, "destination_heading_levels": dst_levels, "destination_heading_roles": [item.get("evidence", {}).get("pdf_role") for item in dst]})
        if src and not dst:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="no PDF heading structure was extracted")
        if src_levels == dst_levels and all(item.get("evidence", {}).get("pdf_role") for item in dst):
            return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence, notes="heading level/order preserved; PDF marked-content text was not available for every heading node")
        return classify_observation(src, dst, partial=bool(dst), feature=feature, evidence=evidence, notes="PDF contains heading structure but the level/order sequence differs from source")
    if feature == "image_alt_text":
        src, dst = source.get("figures", source.get("images", [])), destination.get("figures", destination.get("images", []))
        if not dst:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="no PDF figures were extracted")
        if len(src) == len(dst) and all(a.get("alt") == b.get("alt") and a.get("decorative") == b.get("decorative") for a, b in zip(src, dst)):
            return classify_observation(src, dst, exact=True, feature=feature, evidence=evidence)
        if len(src) == len(dst) and all(bool(a.get("alt")) == bool(b.get("alt")) for a, b in zip(src, dst)) and all(bool(b.get("alt")) for b in dst if not b.get("decorative")):
            return classify_observation(src, dst, mutated=True, feature=feature, evidence=evidence, notes="destination retains non-decorative figures with different alternative text")
        return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="figure count or decorative/alternative-text state differs")
    if feature == "lists":
        src = source.get("lists", [])
        dst = destination.get("lists", [])
        src_items = [item for item in src if item.get("type") in {"ordered", "unordered"}]
        dst_items = [item for item in dst if item.get("type") == "LI"]
        src_blocks = sum(1 for index, item in enumerate(src_items) if index == 0 or item.get("type") != src_items[index - 1].get("type"))
        dst_blocks = sum(1 for item in dst if item.get("type") == "L" and item.get("depth") == 0)
        src_nested = sum(1 for item in src_items if item.get("depth", 0) > 0)
        dst_nested_blocks = sum(1 for item in dst if item.get("type") == "L" and item.get("depth", 0) > 0)
        summary = {"source_items": len(src_items), "destination_items": len(dst_items), "source_blocks": src_blocks, "destination_blocks": dst_blocks, "source_nested_items": src_nested, "destination_nested_blocks": dst_nested_blocks}
        evidence.append(summary)
        if not dst_items:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="no PDF list-item structure was extracted")
        src_block_types = []
        for item in src_items:
            if not src_block_types or item.get("type") != src_block_types[-1]:
                src_block_types.append(item.get("type"))
        dst_block_types = [item.get("list_type") for item in dst if item.get("type") == "L" and item.get("depth") == 0]
        source_texts = [str(item.get("text", "")).strip() for item in src_items]
        destination_texts = [str(item.get("text", "")).strip() for item in dst_items]
        if all(source_texts) and all(destination_texts) and source_texts != destination_texts:
            evidence.append({"source_item_texts": source_texts, "destination_item_texts": destination_texts})
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="list item text order or identity differs")
        if len(src_items) == len(dst_items) and src_blocks == dst_blocks and bool(src_nested) == bool(dst_nested_blocks) and dst_block_types == src_block_types:
            return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence, notes="PDF /L, /LI, nesting, and /ListNumbering match the source contract")
        if len(src_items) == len(dst_items) and src_blocks == dst_blocks and bool(src_nested) == bool(dst_nested_blocks):
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="list items and nesting survive, but PDF extraction found no explicit ordered/unordered type representation")
        return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="some list structure survives but item count or nesting differs")
    if feature == "table":
        src = source.get("tables", [])
        dst = destination.get("tables", [])
        src_table = src[0] if src else {}
        dst_tables = [item for item in dst if item.get("identifier", "").startswith("table-")]
        dst_cells = [item for item in dst if item.get("role") in {"TH", "TD"}]
        src_cell_count = sum(len(row) for row in src_table.get("cells", []))
        dst_header_count = sum(item.get("role") == "TH" for item in dst_cells)
        evidence.append({"source_dimensions": src_table.get("dimensions"), "destination_table_count": len(dst_tables), "source_cell_count": src_cell_count, "destination_cell_count": len(dst_cells), "destination_header_count": dst_header_count, "destination_table_headers": destination.get("table_headers")})
        if not dst_tables:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="no PDF Table structure was extracted")
        if dst_header_count == len(src_table.get("headers", [])) and len(dst_cells) == src_cell_count and destination.get("table_headers"):
            return classify_observation(src_table, dst, equivalent=True, feature=feature, evidence=evidence, notes="PDF Table/TR/TH/TD structure and header-cell count match the source table contract")
        return classify_observation(src_table, dst, partial=True, feature=feature, evidence=evidence, notes="PDF table exists but cell/header correspondence is incomplete")
    if feature == "document_language":
        sv, dv = sdoc.get("language", source.get("language")), ddoc.get("language", destination.get("language"))
        if sv == dv and sv is not None:
            return classify_observation(sv, dv, exact=True, feature=feature, evidence=evidence)
        if dv is None:
            return classify_observation(sv, dv, feature=feature, evidence=evidence, notes="destination supports document language but no value was extracted")
        return classify_observation(sv, dv, mutated=True, feature=feature, evidence=evidence)
    if feature == "inline_language":
        src = [item for item in source.get("inline_languages", []) if item.get("language") != sdoc.get("language")]
        dst = [item for item in destination.get("inline_languages", []) if item.get("language") != ddoc.get("language")]
        if src and len(src) == len(dst) and all(a.get("language") == b.get("language") and (a.get("text") == b.get("text") or (not b.get("text") and a.get("text") in destination.get("pdf_text", ""))) for a, b in zip(src, dst)):
            return classify_observation(src, dst, exact=True, feature=feature, evidence=evidence)
        if src and not dst:
            return classify_observation(src, dst, partial=bool(ddoc.get("language") == sdoc.get("language")), feature=feature, evidence=evidence, notes="document language may survive while inline override is absent")
        return classify_observation(src, dst, mutated=bool(dst), feature=feature, evidence=evidence)
    if feature in {"decorative_image", "image_alt_text"}:
        src, dst = source.get("figures", source.get("images", [])), destination.get("figures", destination.get("images", []))
        if feature == "decorative_image" and any(a.get("decorative") for a in src):
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="destination uses Figure elements with empty alternative text; no explicit PDF Artifact/decorative representation was established")
        if len(src) == len(dst) and all(a.get("alt") == b.get("alt") and a.get("decorative") == b.get("decorative") for a, b in zip(src, dst)):
            return classify_observation(src, dst, exact=True, feature=feature, evidence=evidence)
        if not dst:
            return classify_observation(src, dst, feature=feature, evidence=evidence)
        if len(src) == len(dst) and all(a.get("decorative") == b.get("decorative") and bool(b.get("alt")) for a, b in zip(src, dst)):
            return classify_observation(src, dst, mutated=True, feature=feature, evidence=evidence, notes="destination retains meaningful alternative text with changed wording")
        return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence)
    if feature == "hyperlinks":
        src, dst = source.get("hyperlinks", []), destination.get("hyperlinks", [])
        if not dst:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="no PDF link annotation/structure was extracted")
        if src and len(src) == len(dst) and all(a.get("target") == b.get("target") for a, b in zip(src, dst)):
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure")
        return classify_observation(src, dst, mutated=True, feature=feature, evidence=evidence, notes="destination link target or count differs from source")
    if feature == "document_title":
        sv = sdoc.get("metadata", {}).get("title", source.get("title"))
        dv = ddoc.get("metadata", {}).get("Title", ddoc.get("metadata", {}).get("title", destination.get("title")))
        if sv == dv and sv is not None:
            return classify_observation(sv, dv, exact=True, feature=feature, evidence=evidence)
        return classify_observation(sv, dv, mutated=bool(dv), feature=feature, evidence=evidence)
    if feature == "complex_table":
        src = source.get("tables", [])
        dst = destination.get("tables", [])
        if not src:
            return classify_observation(src, dst, feature=feature, evidence=evidence, notes="source feature is not present")
        if not dst:
            return classify_observation(src, dst, feature=feature, evidence=evidence)
        a = src[0]
        dst_cells = [item for item in dst if item.get("role") in {"TH", "TD"}]
        header_count = sum(item.get("role") == "TH" for item in dst_cells)
        scope_count = sum(bool(item.get("scope")) for item in dst_cells)
        colspan_count = sum(bool(item.get("col_span")) for item in dst_cells)
        evidence.append({"source_header_rows": a.get("header_rows"), "source_grid_spans": a.get("grid_spans"), "destination_header_count": header_count, "destination_scope_count": scope_count, "destination_colspan_count": colspan_count})
        if header_count == sum(len(row) for row in a.get("cells", [])[:2]) and scope_count >= header_count and colspan_count >= 1:
            return classify_observation(a, dst, equivalent=True, feature=feature, evidence=evidence, notes="PDF TH cells, scope attributes, and span evidence establish the multi-level header structure")
        return classify_observation(a, dst, partial=True, feature=feature, evidence=evidence, notes="PDF table and header roles survive, but complete multi-level header associations are not established")
    if feature == "footnotes":
        src, dst = source.get("footnotes", []), destination.get("footnotes", [])
        if dst and any(item.get("evidence", {}).get("pdf_role") == "Note" for item in dst) and not any(item.get("text") for item in dst):
            return classify_observation(src, dst, measured=False, feature=feature, evidence=evidence, notes="PDF /Note structure exists, but marked-content extraction did not recover note-body text for association verification")
        if src and len(src) == len(dst) and all(a.get("id") == b.get("id") and a.get("text") == b.get("text") for a, b in zip(src, dst)):
            return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence)
        return classify_observation(src, dst, partial=bool(dst), feature=feature, evidence=evidence)
    if feature == "equation":
        src, dst = source.get("equations", []), destination.get("equations", [])
        if src and dst and any(item.get("representation") == "PDF /Formula" for item in dst):
            return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence, notes="PDF /Formula structure is present and the visible expression is retained; token-level math extraction remains limited")
        if src and dst and any(item.get("representation") == "PDF visible text fallback" for item in dst):
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="equation survives as visible text but no machine-readable PDF math structure was extracted")
        if src and not dst and destination.get("format") == "pdf" and destination.get("tagged"):
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="equation rendering is present in page text/content, but no machine-readable PDF math structure was extracted")
        if src and len(src) == len(dst) and all(a.get("tokens") == b.get("tokens") for a, b in zip(src, dst)):
            return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence)
        return classify_observation(src, dst, partial=bool(dst), feature=feature, evidence=evidence)
    if feature == "captions":
        src, dst = source.get("captions", []), destination.get("captions", [])
        if src and len(src) == len(dst) and all(a.get("text") == b.get("text") for a, b in zip(src, dst)):
            if all("PDF /Caption structure" in str(item.get("association")) for item in dst):
                return classify_observation(src, dst, equivalent=True, feature=feature, evidence=evidence, notes="caption text and PDF /Caption structure are present")
            return classify_observation(src, dst, partial=True, feature=feature, evidence=evidence, notes="caption text survives but destination association is established only by ordered page-text adjacency")
        return classify_observation(src, dst, partial=bool(dst), feature=feature, evidence=evidence)
    raise ValueError(f"unsupported Phase 4 feature: {feature}")


def compare_all(source: dict[str, Any], destination: dict[str, Any], feature: str | None = None) -> list[dict[str, Any]]:
    if feature:
        return [compare_feature(source, destination, feature)]
    features = []
    if source.get("headings"):
        features.append("headings")
    if source.get("lists"):
        features.append("lists")
    if source.get("tables") and not source.get("footnotes"):
        features.append("table")
    if source.get("figures") and not source.get("inline_languages"):
        features.append("image_alt_text")
    if source.get("document", {}).get("language") or source.get("language"):
        features.append("document_language")
    if source.get("inline_languages"):
        features.append("inline_language")
    if source.get("figures") or source.get("images"):
        features.append("decorative_image")
    if source.get("hyperlinks"):
        features.append("hyperlinks")
    if source.get("document", {}).get("metadata", {}).get("title") or source.get("title"):
        features.append("document_title")
    if source.get("tables"):
        features.append("complex_table")
    if source.get("footnotes"):
        features.append("footnotes")
    if source.get("equations"):
        features.append("equation")
    if source.get("captions"):
        features.append("captions")
    return [compare_feature(source, destination, item) for item in features]
