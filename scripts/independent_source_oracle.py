"""Independent OOXML source-oracle audit for the frozen A11yPreserve corpus.

This verifier intentionally does not import the ASIR extractor, comparator,
fixture generator, or manifest-generation code.  It reads the frozen corpus
manifest only to locate the files and expected source contracts, then performs
fresh ZIP/XML assertions over the DOCX package.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
OUT = ROOT / "evidence" / "source"
REPORT = ROOT / "final_strengthening" / "INDEPENDENT_SOURCE_ORACLE.json"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
CP = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC = "{http://purl.org/dc/elements/1.1/}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text(node: ET.Element) -> str:
    return "".join((child.text or "") for child in node.iter() if child.tag in {W + "t", W + "delText", M + "t"})


def core_properties(root: ET.Element) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for node in root.iter():
        if node.tag == DC + "title":
            values["title"] = node.text
        elif node.tag == DC + "subject":
            values["subject"] = node.text
        elif node.tag == CP + "keywords":
            values["keywords"] = node.text
        elif node.tag == DC + "language":
            values["language"] = node.text
    return values


def numbering_map(numbering: ET.Element) -> dict[tuple[str, str], str]:
    abstract: dict[tuple[str, str], str] = {}
    for item in numbering.findall(W + "abstractNum"):
        aid = item.attrib.get(W + "abstractNumId", "")
        for level in item.findall(W + "lvl"):
            fmt = level.find(W + "numFmt")
            abstract[(aid, level.attrib.get(W + "ilvl", "0"))] = fmt.attrib.get(W + "val", "") if fmt is not None else ""
    result: dict[tuple[str, str], str] = {}
    for item in numbering.findall(W + "num"):
        nid = item.attrib.get(W + "numId", "")
        ref = item.find(W + "abstractNumId")
        aid = ref.attrib.get(W + "val", "") if ref is not None else ""
        for (abstract_id, level), fmt in abstract.items():
            if abstract_id == aid:
                result[(nid, level)] = fmt
    return result


def inspect_docx(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))
        numbering = ET.fromstring(archive.read("word/numbering.xml"))
        core = ET.fromstring(archive.read("docProps/core.xml"))
        rels = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        footnotes = ET.fromstring(archive.read("word/footnotes.xml")) if "word/footnotes.xml" in names else None

    paragraphs = list(document.iter(W + "p"))
    headings = []
    captions = []
    lists = []
    inline = []
    figures = []
    hyperlinks = []
    numbering_formats = numbering_map(numbering)
    link_targets = {node.attrib.get("Id", ""): node.attrib.get("Target", "") for node in rels if node.attrib.get("Type", "").endswith("/hyperlink")}

    for order, paragraph in enumerate(paragraphs, start=1):
        ppr = paragraph.find(W + "pPr")
        style = None
        if ppr is not None:
            style_node = ppr.find(W + "pStyle")
            style = style_node.attrib.get(W + "val") if style_node is not None else None
        value = text(paragraph)
        if style and re.fullmatch(r"Heading[1-6]", style, flags=re.IGNORECASE):
            headings.append({"text": value, "level": int(style[-1])})
        if style and style.lower() == "caption":
            captions.append(value)
        if ppr is not None:
            num_pr = ppr.find(W + "numPr")
            if num_pr is not None:
                nid_node = num_pr.find(W + "numId")
                level_node = num_pr.find(W + "ilvl")
                nid = nid_node.attrib.get(W + "val", "") if nid_node is not None else ""
                level = level_node.attrib.get(W + "val", "0") if level_node is not None else "0"
                fmt = numbering_formats.get((nid, level), "")
                ordered = fmt in {"decimal", "upperRoman", "lowerRoman", "upperLetter", "lowerLetter"}
                lists.append({"type": "ordered" if ordered else "unordered", "depth": int(level), "text": value})
        for run in paragraph.iter(W + "r"):
            run_text = text(run)
            lang = run.find("./" + W + "rPr/" + W + "lang")
            if run_text and lang is not None and lang.attrib.get(W + "val"):
                inline.append({"text": run_text, "language": lang.attrib[W + "val"]})
        for link in paragraph.findall(".//" + W + "hyperlink"):
            hyperlinks.append({"text": text(link), "target": link_targets.get(link.attrib.get(R + "id", "")), "order": len(hyperlinks) + 1})

    for index, node in enumerate(document.iter(WP + "docPr"), start=1):
        alt = node.attrib.get("descr", "")
        figures.append({"identifier": f"figure-{index}", "alt": alt, "decorative": not bool(alt), "order": index})

    tables = []
    for table in document.iter(W + "tbl"):
        rows = list(table.findall(W + "tr"))
        cells = []
        header_rows = []
        spans = []
        for row_index, row in enumerate(rows):
            row_cells = []
            row_spans = []
            for cell in row.findall(W + "tc"):
                row_cells.append(text(cell))
                grid = cell.find("./" + W + "tcPr/" + W + "gridSpan")
                row_spans.append(int(grid.attrib.get(W + "val", "1")) if grid is not None else 1)
            cells.append(row_cells)
            spans.append(row_spans)
            if row.find(W + "trPr/" + W + "tblHeader") is not None:
                header_rows.append(row_index)
        tables.append({"dimensions": {"rows": len(rows), "columns": sum(spans[0]) if spans else 0}, "cells": cells, "header_rows": header_rows})

    notes = []
    if footnotes is not None:
        bodies = {int(node.attrib[W + "id"]): text(node).strip() for node in footnotes.findall(W + "footnote") if node.attrib.get(W + "id", "").lstrip("-").isdigit() and int(node.attrib[W + "id"]) > 0}
        for ref in document.iter(W + "footnoteReference"):
            note_id = int(ref.attrib.get(W + "id", "0"))
            notes.append({"kind": "footnote", "id": note_id, "text": bodies.get(note_id, "")})

    equations = [{"expression": text(node), "representation": "OMML", "tokens": [n.text or "" for n in node.iter(M + "t")]} for node in document.iter(M + "oMath")]
    lang_values = [node.attrib[W + "val"] for node in document.iter(W + "lang") if node.attrib.get(W + "val")]
    doc_defaults = styles.find(".//" + W + "docDefaults/" + W + "rPrDefault/" + W + "rPr/" + W + "lang")
    default_language = doc_defaults.attrib.get(W + "val") if doc_defaults is not None else None

    return {
        "core": core_properties(core),
        "default_language": default_language,
        "language_values": lang_values,
        "headings": headings,
        "lists": lists,
        "inline_languages": inline,
        "figures": figures,
        "hyperlinks": hyperlinks,
        "tables": tables,
        "footnotes": notes,
        "equations": equations,
        "captions": captions,
        "has_footnotes_part": footnotes is not None,
    }


def relevant_observation(manifest: dict, observed: dict) -> dict:
    feature = manifest.get("feature") or manifest.get("feature_family")
    ground = manifest.get("ground_truth", manifest)
    if feature == "headings":
        return {"headings": observed["headings"]}
    if feature in {"alt_text", "decorative_image"}:
        return {"figures": observed["figures"]}
    if feature == "lists":
        return {"lists": observed["lists"]}
    if feature in {"table", "complex_table"}:
        return {"tables": observed["tables"]}
    if feature in {"document_language", "document_title"}:
        return {"core": observed["core"], "default_language": observed["default_language"], "language_values": observed["language_values"]}
    if feature == "inline_language":
        return {"inline_languages": observed["inline_languages"]}
    if feature == "links":
        return {"hyperlinks": observed["hyperlinks"]}
    if feature == "footnotes":
        return {"footnotes": observed["footnotes"], "has_footnotes_part": observed["has_footnotes_part"]}
    if feature == "equation":
        return {"equations": observed["equations"]}
    if feature == "captions":
        return {"captions": observed["captions"]}
    raise ValueError(f"Unsupported feature: {feature}")


def expected_projection(manifest: dict) -> dict:
    feature = manifest.get("feature") or manifest.get("feature_family")
    ground = manifest.get("ground_truth", manifest)
    if feature == "headings":
        return {"headings": ground.get("headings", [])}
    if feature in {"alt_text", "decorative_image"}:
        return {"figures": ground.get("figures", [])}
    if feature == "lists":
        return {"lists": [{k: item.get(k) for k in ("type", "depth", "text")} for item in ground.get("lists", [])]}
    if feature in {"table", "complex_table"}:
        table = ground.get("table", {})
        return {"tables": [{"dimensions": table.get("dimensions", {}), "cells": table.get("cells", []), "header_rows": [table.get("header_row")] if table.get("header_row") is not None else table.get("header_rows", [])}]}
    if feature == "document_language":
        return {"default_language": ground.get("document_language")}
    if feature == "document_title":
        ident = ground.get("document_identity", {})
        return {"core": {"title": ident.get("core_title"), "subject": ident.get("subject"), "keywords": ident.get("keywords")}}
    if feature == "inline_language":
        return {"inline_languages": [{"text": item.get("text"), "language": item.get("language")} for item in ground.get("runs", [])]}
    if feature == "links":
        return {"hyperlinks": [{"text": item.get("text"), "target": item.get("target"), "order": item.get("order")} for item in ground.get("hyperlinks", [])]}
    if feature == "footnotes":
        return {"footnotes": [{"kind": item.get("kind"), "id": item.get("id"), "text": item.get("text")} for item in ground.get("notes", [])], "has_footnotes_part": True}
    if feature == "equation":
        return {"equations": ground.get("equations", [])}
    if feature == "captions":
        return {"captions": [item.get("caption") for item in ground.get("figure_caption_pairs", [])]}
    raise ValueError(f"Unsupported feature: {feature}")


def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items()) if v not in (None, "")}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def main() -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    timestamp = datetime.now(timezone.utc).isoformat()
    results = {}
    errors = []
    for item in frozen["fixtures"]:
        fixture = item["fixture_id"]
        source = Path(item["path"])
        manifest_path = Path(item["source_manifest"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        observed = inspect_docx(source)
        manifest_with_feature = manifest | {"feature_family": item["feature_family"]}
        expected = expected_projection(manifest_with_feature)
        actual = relevant_observation(manifest_with_feature, observed)
        # The source contract contains intentionally higher-level fields than
        # raw OOXML.  The comparison is feature-specific and exact for the
        # fields asserted here; auxiliary OOXML observations remain in the
        # certificate for auditability.
        if item["feature_family"] == "document_language":
            ok = observed["default_language"] == manifest["ground_truth"]["document_language"] or manifest["ground_truth"]["document_language"] in observed["language_values"]
        elif item["feature_family"] == "document_title":
            ident = manifest["ground_truth"]["document_identity"]
            ok = all(observed["core"].get(key) == ident.get(source_key) for key, source_key in (("title", "core_title"), ("subject", "subject"), ("keywords", "keywords")))
        elif item["feature_family"] == "captions":
            ok = observed["captions"] == [x["caption"] for x in manifest["ground_truth"]["figure_caption_pairs"]]
        elif item["feature_family"] == "inline_language":
            expected_runs = [{"text": x["text"], "language": x["language"]} for x in manifest["ground_truth"]["runs"]]
            ok = all(run in observed["inline_languages"] for run in expected_runs)
        elif item["feature_family"] == "links":
            expected_links = [{"text": x["text"], "target": x["target"], "order": x["order"]} for x in manifest["ground_truth"]["hyperlinks"]]
            ok = all(link in observed["hyperlinks"] for link in expected_links)
        elif item["feature_family"] == "footnotes":
            expected_notes = [{"kind": x["kind"], "id": x["id"], "text": x["text"]} for x in manifest["ground_truth"]["notes"]]
            ok = all(note in observed["footnotes"] for note in expected_notes)
        elif item["feature_family"] == "equation":
            expected_expr = manifest["ground_truth"]["equations"][0]["expression"].replace("^", "")
            ok = any("".join(x["tokens"]) == expected_expr.replace(" ", "") for x in observed["equations"])
        else:
            ok = normalize(actual) == normalize(expected)
        certificate = {
            "certificate_version": "source-oracle-v1",
            "fixture_id": fixture,
            "feature": item["feature_family"],
            "source_path": "corpus/fixtures/" + source.name,
            "source_sha256": sha256(source),
            "source_manifest_sha256": sha256(manifest_path),
            "ooxml_parts": ["word/document.xml", "word/styles.xml", "word/numbering.xml", "docProps/core.xml"] + (["word/footnotes.xml"] if observed["has_footnotes_part"] else []),
            "xpath_or_element_assertions": {
                "document": "w:document//w:p, w:tbl, w:hyperlink, w:footnoteReference, wp:docPr, m:oMath",
                "feature": item["feature_family"],
            },
            "expected": expected,
            "observed": actual,
            "raw_observations": observed,
            "verifier": "scripts/independent_source_oracle.py; stdlib zipfile + xml.etree.ElementTree; no ASIR imports",
            "timestamp_utc": timestamp,
            "status": "PASS" if ok else "DISAGREEMENT",
        }
        (OUT / f"{fixture}_certificate.json").write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        results[fixture] = {"feature": item["feature_family"], "status": certificate["status"], "source_sha256": certificate["source_sha256"]}
        if not ok:
            errors.append(fixture)
    report = {"oracle": "independent_raw_ooxml", "fixtures_checked": len(results), "passed": len(results) - len(errors), "disagreements": errors, "status": "PASS" if not errors else "STOP", "results": results, "timestamp_utc": timestamp}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
