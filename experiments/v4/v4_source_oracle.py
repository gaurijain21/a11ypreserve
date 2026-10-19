"""Raw OOXML source oracle for V4.

This module intentionally does not import the V4 generator, primary extractor,
or PDF comparator. It reads only a DOCX ZIP/XML package and the frozen
machine-readable contract. Its output is an evidence certificate, not a PDF
preservation decision.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "v4"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
DC = "{http://purl.org/dc/elements/1.1/}"
CP = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text(node: ET.Element) -> str:
    return "".join(item.text or "" for item in node.iter() if item.tag in {W + "t", W + "delText", M + "t"})


def parse(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))
        core = ET.fromstring(archive.read("docProps/core.xml"))
        numbering = ET.fromstring(archive.read("word/numbering.xml"))
        rels = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        footnotes = ET.fromstring(archive.read("word/footnotes.xml")) if "word/footnotes.xml" in names else None

    core_values = {element.tag.rsplit("}", 1)[-1]: element.text for element in core.iter() if element.text is not None}
    default_language = None
    default_node = styles.find(".//" + W + "docDefaults/" + W + "rPrDefault/" + W + "rPr/" + W + "lang")
    if default_node is not None:
        default_language = default_node.attrib.get(W + "val")
    language = core_values.get("language") or default_language or "en-US"

    headings = []
    lists = []
    inline_languages = []
    captions = []
    hyperlinks = []
    for paragraph in document.iter(W + "p"):
        props = paragraph.find(W + "pPr")
        style = props.find(W + "pStyle") if props is not None else None
        if style is not None and style.attrib.get(W + "val", "").startswith("Heading"):
            value = style.attrib.get(W + "val", "")
            match = re.search(r"(\d+)$", value)
            headings.append({"text": text(paragraph), "level": int(match.group(1)) if match else 0})
        if style is not None and style.attrib.get(W + "val") == "Caption":
            captions.append({"text": text(paragraph)})
        num_pr = props.find(W + "numPr") if props is not None else None
        if num_pr is not None:
            ilvl = num_pr.find(W + "ilvl")
            num_id = num_pr.find(W + "numId")
            lists.append({"depth": int(ilvl.attrib.get(W + "val", "0")) if ilvl is not None else 0, "num_id": num_id.attrib.get(W + "val") if num_id is not None else None, "text": text(paragraph)})
        for run in paragraph.iter(W + "r"):
            rpr = run.find(W + "rPr")
            lang_node = rpr.find(W + "lang") if rpr is not None else None
            if lang_node is not None and lang_node.attrib.get(W + "val"):
                inline_languages.append({"text": text(run), "language": lang_node.attrib[W + "val"]})
        for hyperlink in paragraph.findall(".//" + W + "hyperlink"):
            hyperlinks.append({"text": text(hyperlink), "rid": hyperlink.attrib.get(R + "id")})

    relation_targets = {node.attrib.get("Id"): node.attrib.get("Target") for node in rels if node.attrib.get("Type", "").endswith("/hyperlink")}
    for index, link in enumerate(hyperlinks, 1):
        link["target"] = relation_targets.get(link.pop("rid"), "")
        link["order"] = index

    figures = []
    for drawing in document.iter(W + "drawing"):
        for docpr in drawing.iter(WP + "docPr"):
            figures.append({"alt": docpr.attrib.get("descr", ""), "decorative": not bool(docpr.attrib.get("descr", "")), "title": docpr.attrib.get("title", "")})

    tables = []
    for table in document.iter(W + "tbl"):
        rows = list(table.iter(W + "tr"))
        cells = list(table.iter(W + "tc"))
        headers = []
        for row_index, row in enumerate(rows):
            trpr = row.find(W + "trPr")
            if trpr is not None and trpr.find(W + "tblHeader") is not None:
                headers.append(row_index)
        spans = []
        for cell in cells:
            props = cell.find(W + "tcPr")
            grid = props.find(W + "gridSpan") if props is not None else None
            vmerge = props.find(W + "vMerge") if props is not None else None
            if grid is not None or vmerge is not None:
                spans.append({"gridSpan": grid.attrib.get(W + "val") if grid is not None else None, "vMerge": vmerge.attrib.get(W + "val", "continue") if vmerge is not None else None})
        table_values = [[text(cell) for cell in row.iter(W + "tc")] for row in rows]
        tables.append({"rows": len(rows), "cells": len(cells), "header_rows": headers, "spans": spans, "values": table_values})

    numbering_formats = {}
    for abstract in numbering.findall(W + "abstractNum"):
        abstract_id = abstract.attrib.get(W + "abstractNumId")
        numbering_formats[abstract_id] = {level.attrib.get(W + "ilvl"): (level.find(W + "numFmt").attrib.get(W + "val") if level.find(W + "numFmt") is not None else None) for level in abstract.findall(W + "lvl")}
    number_map = {}
    for number in numbering.findall(W + "num"):
        abstract = number.find(W + "abstractNumId")
        number_map[number.attrib.get(W + "numId")] = numbering_formats.get(abstract.attrib.get(W + "val") if abstract is not None else "", {})
    for item in lists:
        raw_type = number_map.get(item.get("num_id"), {}).get(str(item.get("depth")))
        item["type"] = "ordered" if raw_type in {"decimal", "upperRoman", "lowerRoman", "upperLetter", "lowerLetter"} else "unordered" if raw_type == "bullet" else raw_type

    footnote_values = []
    if footnotes is not None:
        for note in footnotes.findall(W + "footnote"):
            note_id = note.attrib.get(W + "id")
            if note_id not in {"-1", "0"}:
                footnote_values.append({"id": int(note_id), "text": text(note)})
    equations = [{"tokens": [node.text or "" for node in math.iter(M + "t")], "expression": text(math)} for math in document.iter(M + "oMath")]

    return {
        "source_sha256": sha256(path),
        "headings": headings,
        "figures": figures,
        "lists": lists,
        "tables": tables,
        "document_language": language,
        "inline_languages": inline_languages,
        "hyperlinks": hyperlinks,
        "metadata": {key: core_values.get(key) for key in ["title", "subject", "keywords", "language"]},
        "footnotes": footnote_values,
        "equations": equations,
        "captions": captions,
        "ooxml_parts": sorted(names),
    }


def contract_ok(observed: dict, manifest: dict) -> tuple[bool, list[str]]:
    feature = manifest["feature_family"]
    truth = manifest["ground_truth"]
    problems: list[str] = []
    if feature == "headings" and observed["headings"] != truth["headings"]:
        problems.append("heading sequence differs")
    elif feature == "alt_text" and [{"alt": item["alt"], "order": i} for i, item in enumerate(observed["figures"], 1)] != truth["figures"]:
        problems.append("alternative-text values differ")
    elif feature == "lists":
        actual = [{key: item.get(key) for key in ["type", "depth", "text"]} for item in observed["lists"]]
        if actual != truth["lists"]:
            problems.append("list structure differs")
    elif feature == "basic_tables":
        item = observed["tables"][0] if observed["tables"] else {}
        if {"rows": item.get("rows"), "columns": item.get("cells", 0) // max(item.get("rows", 1), 1)} != truth["dimensions"] or item.get("header_rows") != truth["header_rows"] or item.get("values") != truth["cells"]:
            problems.append("basic table dimensions/header differ")
    elif feature == "document_language" and observed["document_language"] != truth["document_language"]:
        problems.append("document language differs")
    elif feature == "inline_language":
        expected = truth["spans"]
        actual = [{"text": item["text"].strip(), "language": item["language"]} for item in observed["inline_languages"] if item["language"] != "en-US"]
        if actual != expected:
            problems.append("inline language spans differ")
    elif feature == "decorative_images" and [{"alt": x["alt"], "decorative": x["decorative"], "order": i} for i, x in enumerate(observed["figures"], 1)] != truth["figures"]:
        problems.append("decorative/image state differs")
    elif feature == "hyperlinks" and observed["hyperlinks"] != [{"text": x["text"], "target": x["target"], "order": x["order"]} for x in truth["hyperlinks"]]:
        problems.append("hyperlink values differ")
    elif feature == "document_metadata":
        if observed["metadata"].get("title") != truth["core_title"] or observed["metadata"].get("subject") != truth["subject"]:
            problems.append("metadata differs")
    elif feature == "complex_tables":
        item = observed["tables"][0] if observed["tables"] else {}
        signature = truth.get("span_signature", {})
        spans_ok = any(signature.get("gridSpan") is not None and span.get("gridSpan") == signature["gridSpan"] for span in item.get("spans", [])) or any(signature.get("vMerge") is not None and span.get("vMerge") == signature["vMerge"] for span in item.get("spans", []))
        if item.get("rows") != truth["rows"] or item.get("header_rows") != truth["header_rows"] or not item.get("spans") or not spans_ok:
            problems.append("complex-table structure differs")
    elif feature == "footnotes":
        actual = [{"id": item["id"], "text": item["text"].strip()} for item in observed["footnotes"]]
        expected = [{"id": item["id"], "text": item["text"]} for item in truth["notes"]]
        if actual != expected:
            problems.append("footnotes differ")
    elif feature == "equations":
        actual = [{"tokens": item["tokens"]} for item in observed["equations"]]
        expected = [{"tokens": item["tokens"]} for item in truth["equations"]]
        if actual != expected:
            problems.append("equations differ")
    elif feature == "captions" and observed["captions"] != [{"text": x["caption"]} for x in truth["pairs"]]:
        problems.append("caption text differs")
    return not problems, problems


def validate() -> dict:
    manifest = json.loads((BASE / "source_manifest.json").read_text(encoding="utf-8"))
    certificates = BASE / "source_oracle_certificates"
    certificates.mkdir(parents=True, exist_ok=True)
    rows = []
    for record in manifest["records"]:
        fixture = ROOT / record["fixture"]
        metadata = json.loads((ROOT / record["manifest"]).read_text(encoding="utf-8"))
        observed = parse(fixture)
        ok, problems = contract_ok(observed, metadata)
        certificate = {"variant_id": record["variant_id"], "feature_family": record["feature_family"], "source_sha256": observed["source_sha256"], "contract_sha256": sha256(ROOT / record["manifest"]), "status": "PASS" if ok and observed["source_sha256"] == metadata["source_sha256"] else "FAIL", "raw_ooxml": observed, "problems": problems}
        path = certificates / f"{record['variant_id']}.json"
        path.write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append({"variant_id": record["variant_id"], "status": certificate["status"], "problems": problems})
    report = {"oracle": "v4_raw_ooxml_contract_oracle", "fixture_count": len(rows), "passed": sum(row["status"] == "PASS" for row in rows), "failed": sum(row["status"] == "FAIL" for row in rows), "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL", "results": rows}
    (BASE / "SOURCE_ORACLE_CERTIFICATE.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
