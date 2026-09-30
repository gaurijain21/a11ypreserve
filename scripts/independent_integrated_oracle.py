from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "integrated_study"
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text(node: ET.Element) -> str:
    return "".join(node.itertext())


def load_docx(path: Path) -> dict[str, ET.Element | dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        def xml(name: str):
            return ET.fromstring(archive.read(name))
        return {
            "document": xml("word/document.xml"),
            "styles": xml("word/styles.xml"),
            "core": xml("docProps/core.xml"),
            "rels": xml("word/_rels/document.xml.rels"),
            "footnotes": xml("word/footnotes.xml") if "word/footnotes.xml" in archive.namelist() else None,
            "path": path,
        }


def paragraphs(doc: dict) -> list[ET.Element]:
    return doc["document"].findall(".//w:body/w:p", NS)


def check_contract(doc: dict, contract: dict) -> tuple[bool, str]:
    feature = contract["feature"]
    expected = contract["expected"]
    ps = paragraphs(doc)
    if feature == "headings":
        levels = []
        for p in ps:
            style = p.find("./w:pPr/w:pStyle", NS)
            if style is not None:
                value = style.get(f"{{{NS['w']}}}val", "")
                if value.lower().startswith("heading"):
                    levels.append(int(value[-1]))
        return levels == expected["levels"], f"heading levels={levels}"
    if feature == "document_language":
        node = doc["styles"].find(".//w:docDefaults/w:rPrDefault/w:rPr/w:lang", NS)
        value = None if node is None else node.get(f"{{{NS['w']}}}val")
        return value == expected["language"], f"default language={value}"
    if feature == "document_title":
        node = doc["core"].find("dc:title", NS)
        value = None if node is None else text(node)
        return value == expected["title"], f"core title={value!r}"
    if feature == "inline_language":
        found = []
        for run in doc["document"].findall(".//w:r", NS):
            lang = run.find("./w:rPr/w:lang", NS)
            if lang is not None:
                found.append((text(run), lang.get(f"{{{NS['w']}}}val")))
        target = (expected["text"], expected["language"])
        return target in found, f"language runs include target={target in found}"
    if feature == "image_alt_text":
        values = [n.get("descr", "") for n in doc["document"].findall(".//wp:docPr", NS)]
        return expected["alt"] in values, f"image descriptions={values}"
    if feature == "decorative_image":
        values = [n.get("descr", "") for n in doc["document"].findall(".//wp:docPr", NS)]
        return expected["decorative"] is True and "" in values, f"image descriptions={values}"
    if feature == "lists":
        depths = []
        for p in ps:
            node = p.find("./w:pPr/w:numPr/w:ilvl", NS)
            if node is not None:
                depths.append(int(node.get(f"{{{NS['w']}}}val", "-1")))
        return depths == expected["depths"], f"list depths={depths}"
    if feature == "table":
        tables = doc["document"].findall(".//w:tbl", NS)
        if not tables:
            return False, "no table"
        table = tables[0]
        rows = table.findall("./w:tr", NS)
        headers = [text(cell) for cell in rows[0].findall("./w:tc", NS)] if rows else []
        ok = len(rows) == expected["rows"] and headers == expected["headers"] and rows[0].find("./w:trPr/w:tblHeader", NS) is not None
        return ok, f"rows={len(rows)} headers={headers} header_marked={bool(rows and rows[0].find('./w:trPr/w:tblHeader', NS) is not None)}"
    if feature == "hyperlinks":
        targets = [node.get("Target") for node in doc["rels"].findall("./pr:Relationship", NS) if node.get("Type", "").endswith("/hyperlink")]
        return expected["target"] in targets, f"hyperlink targets={targets}"
    if feature == "equation":
        count = len(doc["document"].findall(".//m:oMath", NS))
        return expected["omml"] is True and count > 0, f"OMML equations={count}"
    if feature == "footnotes":
        if doc["footnotes"] is None:
            return False, "footnotes.xml missing"
        value = text(doc["footnotes"])
        return expected["text"] in value, f"footnote body present={expected['text'] in value}"
    if feature == "captions":
        values = []
        for p in ps:
            style = p.find("./w:pPr/w:pStyle", NS)
            if style is not None and style.get(f"{{{NS['w']}}}val") == "Caption":
                values.append(text(p))
        return expected["text"] in values, f"captions={values}"
    return False, f"unsupported feature={feature}"


def main() -> None:
    manifest = json.loads((OUT / "INTEGRATED_CONTRACTS.json").read_text(encoding="utf-8"))
    records = []
    for document in manifest["documents"]:
        path = ROOT / document["source_docx"]
        doc = load_docx(path)
        source_hash = sha256(path)
        for contract in document["contracts"]:
            passed, observation = check_contract(doc, contract)
            records.append({
                "document_id": document["document_id"],
                "instance": contract["instance"],
                "feature": contract["feature"],
                "source_sha256": source_hash,
                "expected": contract["expected"],
                "passed": passed,
                "observation": observation,
            })
    result = {"oracle": "independent_integrated_raw_ooxml_oracle", "contract_count": len(records), "passed": sum(r["passed"] for r in records), "failed": sum(not r["passed"] for r in records), "records": records}
    (OUT / "INTEGRATED_SOURCE_ORACLE.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Integrated source-oracle audit", "", f"The separate ZIP/XML verifier checked {result['passed']}/{result['contract_count']} integrated source contracts. It does not import the integrated-document generator, ASIR, or the frozen comparator.", "", "| Document | Instance | Feature | Status | Observation |", "|---|---|---|---|---|"]
    for row in records:
        lines.append(f"| {row['document_id']} | {row['instance']} | {row['feature']} | {'PASS' if row['passed'] else 'FAIL'} | {row['observation']} |")
    (OUT / "INTEGRATED_SOURCE_ORACLE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"contracts": len(records), "passed": result["passed"], "failed": result["failed"]}, indent=2))


if __name__ == "__main__":
    main()
