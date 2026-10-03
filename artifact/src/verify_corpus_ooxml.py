from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import docx_extract, xml_text  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

FIXTURE_IDS = ["F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE", "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE", "F11_FOOTNOTES", "F12_EQUATION", "F14_CAPTIONS"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def verify_one(fixture_id: str) -> dict:
    path = ROOT / "corpus" / "fixtures" / f"{fixture_id}.docx"
    manifest_path = ROOT / "corpus" / "manifests" / f"{fixture_id}.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        core = ET.fromstring(archive.read("docProps/core.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))
        rels = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        footnotes = ET.fromstring(archive.read("word/footnotes.xml")) if "word/footnotes.xml" in archive.namelist() else None

    source = docx_extract(path)
    ground = manifest["ground_truth"]
    raw_lang = styles.find(".//" + W + "docDefaults/" + W + "rPrDefault/" + W + "rPr/" + W + "lang")
    raw_default_lang = raw_lang.attrib.get(W + "val") if raw_lang is not None else None

    if fixture_id in {"F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE", "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE", "F11_FOOTNOTES", "F12_EQUATION", "F14_CAPTIONS"}:
        expected = manifest["document"]["language"]
        if raw_default_lang != expected:
            fail(errors, f"raw document default language {raw_default_lang!r} != {expected!r}")
        if source["document"]["language"] != expected:
            fail(errors, f"source extractor language {source['document']['language']!r} != {expected!r}")

    if fixture_id == "F05_DOCUMENT_LANGUAGE":
        if ground["document_language"] != raw_default_lang:
            fail(errors, "manifest/raw language mismatch")
    elif fixture_id == "F06_INLINE_LANGUAGE":
        target = ground["runs"][0]
        if not any(item["text"] == target["text"] and item["language"] == target["language"] for item in source["inline_languages"]):
            fail(errors, "inline language override missing from source extractor")
        runs = [run for run in document.iter(W + "r") if xml_text(run) == target["text"]]
        if not runs or runs[0].find("./" + W + "rPr/" + W + "lang").attrib.get(W + "val") != target["language"]:
            fail(errors, "raw OOXML inline language override mismatch")
    elif fixture_id == "F07_DECORATIVE_IMAGE":
        raw_figures = [{"alt": node.attrib.get("descr", ""), "title": node.attrib.get("title", "")} for node in document.iter(WP + "docPr")]
        expected = ground["figures"]
        if [item["alt"] for item in raw_figures] != [item["alt"] for item in expected]:
            fail(errors, "raw figure descriptions mismatch")
        if [item["decorative"] for item in source["figures"]] != [item["decorative"] for item in expected]:
            fail(errors, "source extractor decorative states mismatch")
    elif fixture_id == "F08_LINKS":
        expected = ground["hyperlinks"]
        if [{key: item[key] for key in ("text", "target")} for item in source["hyperlinks"]] != [{key: item[key] for key in ("text", "target")} for item in expected]:
            fail(errors, "hyperlink manifest/source mismatch")
        relationship_targets = {rel.attrib.get("Id"): rel.attrib.get("Target") for rel in rels if rel.attrib.get("Type", "").endswith("/hyperlink")}
        if not relationship_targets or expected[0]["target"] not in relationship_targets.values():
            fail(errors, "raw hyperlink relationship target missing")
    elif fixture_id == "F09_DOCUMENT_TITLE":
        raw = {node.tag.rsplit("}", 1)[-1]: node.text for node in core.iter() if node.tag.rsplit("}", 1)[-1] in {"title", "subject", "keywords"}}
        expected = ground["document_identity"]
        for key in ("core_title", "subject", "keywords"):
            raw_key = "title" if key == "core_title" else key
            if raw.get(raw_key) != expected[key]:
                fail(errors, f"core property {key} mismatch")
            if source["document"]["metadata"].get(raw_key) != expected[key]:
                fail(errors, f"source metadata {key} mismatch")
    elif fixture_id == "F10_COMPLEX_TABLE":
        table = source["tables"][0]
        expected = ground["table"]
        for key in ("dimensions", "cells", "header_rows"):
            if table[key] != expected[key]:
                fail(errors, f"complex table {key} mismatch: {table[key]!r} != {expected[key]!r}")
        if table["grid_spans"][0] != [2, 1]:
            fail(errors, f"raw grid span mismatch: {table['grid_spans'][0]!r}")
        if len(list(document.iter(W + "tblHeader"))) != 2:
            fail(errors, "raw table header row count is not two")
    elif fixture_id == "F11_FOOTNOTES":
        expected = ground["notes"][0]
        if footnotes is None:
            fail(errors, "word/footnotes.xml is missing")
        else:
            raw_note = next((node for node in footnotes.findall(W + "footnote") if node.attrib.get(W + "id") == str(expected["id"])), None)
            if raw_note is None or xml_text(raw_note).strip() != expected["text"]:
                fail(errors, "raw footnote text mismatch")
        if not any(item["id"] == expected["id"] and item["text"] == expected["text"] for item in source["footnotes"]):
            fail(errors, "source footnote extraction mismatch")
        reference_paragraphs = [xml_text(p) for p in document.iter(W + "p") if p.find(".//" + W + "footnoteReference") is not None]
        if not reference_paragraphs or expected["reference_text"] not in reference_paragraphs[0]:
            fail(errors, "raw footnote reference association mismatch")
    elif fixture_id == "F12_EQUATION":
        expected = ground["equations"][0]
        if not list(document.iter(M + "oMath")):
            fail(errors, "raw OMML equation missing")
        actual = source["equations"][0] if source["equations"] else None
        if not actual or actual["tokens"] != expected["tokens"] or actual["representation"] != expected["representation"]:
            fail(errors, "source OMML equation extraction mismatch")
    elif fixture_id == "F14_CAPTIONS":
        expected = ground["figure_caption_pairs"][0]
        if len(list(document.iter(WP + "docPr"))) != 1:
            fail(errors, "raw figure count mismatch")
        if not any(item["text"] == expected["caption"] and item["style"].lower() == "caption" and item["figure"] == expected["figure"] for item in source["captions"]):
            fail(errors, "source figure/caption association mismatch")

    return {"fixture": fixture_id, "path": str(path), "sha256": sha256(path), "manifest": str(manifest_path), "manifest_sha256": sha256(manifest_path), "manifest_matches_ooxml": not errors, "source_extractor_matches": not errors, "errors": errors}


def main() -> None:
    rows = [verify_one(fixture_id) for fixture_id in FIXTURE_IDS]
    report = {"verified_at": __import__("datetime").datetime.now().astimezone().isoformat(), "fixtures": rows, "passed": all(row["manifest_matches_ooxml"] and row["source_extractor_matches"] for row in rows)}
    output = ROOT / "corpus" / "reports"
    output.mkdir(parents=True, exist_ok=True)
    (output / "source_verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
