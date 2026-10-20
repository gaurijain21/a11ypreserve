"""Run a separately implemented, evidence-only oracle audit over archived PDFs.

This is not human adjudication and does not import the frozen extractor,
comparator, or V6 result files.  It uses standard-library DOCX inspection plus
PyMuPDF and pypdf destination inspection to produce bounded observations for
all 130 primary cases and the 65 supplementary Word cases.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

import fitz
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "v7" / "independent_oracle_cases"
REPORT = ROOT / "experiments" / "v7" / "V7_INDEPENDENT_ORACLE.json"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DC = "{http://purl.org/dc/elements/1.1/}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_projection(path: Path, family: str) -> dict:
    """Extract only contract-facing source facts, independently from ASIR."""
    with ZipFile(path) as package:
        document = ET.fromstring(package.read("word/document.xml"))
        core = ET.fromstring(package.read("docProps/core.xml"))
        rels = ET.fromstring(package.read("word/_rels/document.xml.rels"))
        footnotes = ET.fromstring(package.read("word/footnotes.xml")) if "word/footnotes.xml" in package.namelist() else None

    def txt(node: ET.Element) -> str:
        return "".join(x.text or "" for x in node.iter() if x.tag in {W + "t", W + "delText"})

    paragraphs = list(document.iter(W + "p"))
    headings = []
    for paragraph in paragraphs:
        style = paragraph.find(W + "pPr/" + W + "pStyle")
        if style is not None and style.attrib.get(W + "val", "").lower().startswith("heading"):
            value = style.attrib.get(W + "val", "")
            headings.append({"level": int(value[-1]), "text": txt(paragraph)})
    figures = [{"alt": node.attrib.get("descr", ""), "decorative": not bool(node.attrib.get("descr", ""))}
               for node in document.iter("{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr")]
    links = {node.attrib.get("Id"): node.attrib.get("Target") for node in rels if node.attrib.get("Type", "").endswith("/hyperlink")}
    hyperlinks = []
    for order, node in enumerate(document.iter(W + "hyperlink"), start=1):
        hyperlinks.append({"text": txt(node), "target": links.get(node.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")), "order": order})
    notes = []
    if footnotes is not None:
        bodies = {n.attrib.get(W + "id"): txt(n) for n in footnotes.iter(W + "footnote")}
        for ref in document.iter(W + "footnoteReference"):
            notes.append({"id": ref.attrib.get(W + "id"), "text": bodies.get(ref.attrib.get(W + "id"), "")})
    core_values = {node.tag.removeprefix(DC): node.text for node in core.iter() if node.tag.startswith(DC)}
    if family == "headings":
        return {"headings": headings}
    if family in {"alt_text", "decorative_images"}:
        return {"figures": figures}
    if family == "hyperlinks":
        return {"hyperlinks": hyperlinks}
    if family == "footnotes":
        return {"footnotes": notes}
    if family == "document_metadata":
        return {"metadata": {k: core_values.get(k) for k in ("title", "subject", "keywords")}}
    return {"paragraph_count": len(paragraphs), "family": family}


def deref(value):
    try:
        return value.get_object()
    except AttributeError:
        return value


def destination_projection(path: Path) -> dict:
    reader = PdfReader(str(path), strict=False)
    root = deref(reader.trailer.get("/Root"))
    counts: Counter[str] = Counter()
    values: dict[str, list[str]] = {"Alt": [], "Lang": [], "ActualText": []}
    seen: set[int] = set()

    def walk(value):
        value = deref(value)
        if isinstance(value, dict):
            ident = id(value)
            if ident in seen:
                return
            seen.add(ident)
            role = value.get("/S")
            if role:
                counts[str(role)] += 1
            for key in ("/Alt", "/Lang", "/ActualText"):
                if key in value:
                    values[key.removeprefix("/")].append(str(value[key]))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(root.get("/StructTreeRoot") if isinstance(root, dict) else None)
    links = []
    for page in reader.pages:
        for annotation in page.get("/Annots", []) or []:
            item = deref(annotation)
            action = deref(item.get("/A")) if isinstance(item, dict) else None
            if isinstance(action, dict) and action.get("/URI"):
                links.append(str(action.get("/URI")))
    document = fitz.open(path)
    text = "\n".join(page.get_text("text") for page in document)
    projection = {
        "pages": len(document),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "role_counts": dict(sorted(counts.items())),
        "alt_values": values["Alt"],
        "lang_values": values["Lang"],
        "actual_text_values": values["ActualText"],
        "annotation_uri_count": len(links),
        "annotation_uris": links,
        "catalog_lang": str(root.get("/Lang")) if isinstance(root, dict) and root.get("/Lang") else None,
        "metadata_title": str(reader.metadata.title) if reader.metadata and reader.metadata.title else None,
    }
    document.close()
    return projection


def independent_status(family: str, dest: dict) -> str:
    roles = dest["role_counts"]
    if family == "headings":
        return "OBSERVED_STRUCTURE" if sum(roles.get(f"/H{i}", 0) for i in range(1, 7)) else "NO_OBSERVED_STRUCTURE"
    if family == "alt_text":
        return "OBSERVED_FIGURE_ALT" if roles.get("/Figure", 0) and dest["alt_values"] else "NO_OBSERVED_FIGURE_ALT"
    if family == "decorative_images":
        return "OBSERVED_ARTIFACT" if roles.get("/Artifact", 0) else "NO_OBSERVED_ARTIFACT"
    if family == "lists":
        return "OBSERVED_LIST_STRUCTURE" if roles.get("/L", 0) else "NO_OBSERVED_LIST_STRUCTURE"
    if family in {"basic_tables", "complex_tables"}:
        return "OBSERVED_TABLE_STRUCTURE" if roles.get("/Table", 0) else "NO_OBSERVED_TABLE_STRUCTURE"
    if family == "document_language":
        return "OBSERVED_LANGUAGE" if dest["catalog_lang"] or dest["lang_values"] else "NO_OBSERVED_LANGUAGE"
    if family == "inline_language":
        return "OBSERVED_LANGUAGE_EVIDENCE" if dest["lang_values"] else "NO_OBSERVED_LANGUAGE_EVIDENCE"
    if family == "hyperlinks":
        return "OBSERVED_URI_ACTION" if dest["annotation_uri_count"] else "NO_OBSERVED_URI_ACTION"
    if family == "footnotes":
        return "OBSERVED_NOTE_ROLE" if roles.get("/Note", 0) else "NO_OBSERVED_NOTE_ROLE"
    if family == "equations":
        return "OBSERVED_FORMULA_ROLE" if roles.get("/Formula", 0) else "NO_OBSERVED_FORMULA_ROLE"
    if family == "captions":
        return "OBSERVED_CAPTION_ROLE" if roles.get("/Caption", 0) else "NO_OBSERVED_CAPTION_ROLE"
    if family == "document_metadata":
        return "OBSERVED_TITLE_METADATA" if dest["metadata_title"] else "NO_OBSERVED_TITLE_METADATA"
    return "UNSUPPORTED_FAMILY"


def load_records() -> list[dict]:
    paths = [
        ROOT / "experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json",
        ROOT / "experiments/v4/conversions/google/analysis/V4_GOOGLE_ANALYSIS.json",
        ROOT / "experiments/v4/conversions/word/analysis/V4_WORD_ANALYSIS.json",
    ]
    records = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        records.extend(data["records"])
    return records


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []
    errors = []
    for record in load_records():
        source = ROOT / record["source_path"]
        pdf = ROOT / record["output_path"]
        row = {
            "fixture_id": record["fixture_id"],
            "family": record["feature_family"],
            "pipeline": record["converter"],
            "source_sha256": sha256(source),
            "pdf_sha256": sha256(pdf),
            "frozen_classification": record["classification"],
            "source_contract_projection": source_projection(source, record["feature_family"]),
            "destination_projection": None,
            "independent_observation": None,
            "status": "COMPLETE",
            "timestamp_utc": timestamp,
        }
        try:
            row["destination_projection"] = destination_projection(pdf)
            row["independent_observation"] = independent_status(record["feature_family"], row["destination_projection"])
        except Exception as exc:  # preserve a per-case failure instead of hiding it
            row["status"] = "EXTRACTION_ERROR"
            row["error"] = repr(exc)
            errors.append(record["fixture_id"] + ":" + record["converter"])
        OUT.joinpath(f"{record['converter'].replace(' ', '_')}_{record['fixture_id']}.json").write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append(row)
    report = {
        "protocol": "V7 independently implemented raw PDF/OOXML evidence audit",
        "implementation": "stdlib ZIP/XML + pypdf 6.18.1 + PyMuPDF 1.28.2; no frozen destination extractor or comparator imports",
        "cases": len(rows),
        "primary_cases": sum(row["pipeline"] in {"LibreOffice", "Google Docs"} for row in rows),
        "supplementary_word_cases": sum(row["pipeline"] == "Microsoft Word desktop" for row in rows),
        "extraction_errors": len(errors),
        "errors": errors,
        "observation_counts": dict(Counter(row.get("independent_observation") for row in rows)),
        "status": "COMPLETE" if not errors else "INCOMPLETE",
        "not_human_adjudication": True,
        "timestamp_utc": timestamp,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
