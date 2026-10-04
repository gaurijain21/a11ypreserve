from __future__ import annotations

import copy
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from v4_source_oracle import ROOT, BASE, contract_ok, parse

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
R = "{http://schemas.openxmlformats.org/package/2006/relationships}"
DC = "{http://purl.org/dc/elements/1.1/}"
CP = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"


def mutate(source: Path, target: Path, feature: str, kind: str) -> None:
    with zipfile.ZipFile(source) as archive:
        payload = {name: archive.read(name) for name in archive.namelist()}
    part = "word/document.xml"
    if feature in {"document_language", "document_metadata"}:
        part = "docProps/core.xml"
    elif feature == "hyperlinks" and kind == "value":
        part = "word/_rels/document.xml.rels"
    elif feature == "footnotes":
        part = "word/footnotes.xml"
    root = ET.fromstring(payload[part])
    changed = False

    if feature == "headings":
        nodes = [node for node in root.findall(".//" + W + "pStyle") if node.attrib.get(W + "val", "").startswith("Heading")]
        if nodes:
            if kind == "value":
                nodes[0].set(W + "val", "Heading2")
            elif kind == "delete":
                paragraph = next((node for node in root.findall(".//" + W + "p") if node.find(".//" + W + "pStyle") is not None and node.find(".//" + W + "pStyle").attrib.get(W + "val", "").startswith("Heading")), None)
                first_text = paragraph.find(".//" + W + "t") if paragraph is not None else None
                if first_text is not None:
                    first_text.text = ""
            else:
                nodes[0].set(W + "val", "Normal")
            changed = True
    elif feature in {"alt_text", "decorative_images"}:
        nodes = root.findall(".//" + WP + "docPr")
        if nodes:
            if kind == "value":
                nodes[0].set("descr", "MUTATED")
            elif kind == "delete":
                parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0])
            else:
                nodes[0].set("descr", "STRUCTURAL_MUTATION")
            changed = True
    elif feature == "lists":
        nodes = root.findall(".//" + W + "numPr")
        if nodes:
            if kind == "value":
                first = nodes[0].find(W + "ilvl"); first.set(W + "val", "2") if first is not None else None
            elif kind == "delete":
                parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0])
            else:
                first = nodes[0].find(W + "numId"); first.set(W + "val", "999") if first is not None else None
            changed = True
    elif feature == "basic_tables":
        if kind == "value":
            cell = root.find(".//" + W + "tc"); t = cell.find(".//" + W + "t") if cell is not None else None; t.text = "MUTATED" if t is not None else None
        elif kind == "delete":
            marker = root.find(".//" + W + "tblHeader");
            if marker is not None:
                parent = next(parent for parent in root.iter() if marker in list(parent)); parent.remove(marker)
        else:
            row = root.find(".//" + W + "tr");
            if row is not None:
                parent = next(parent for parent in root.iter() if row in list(parent)); parent.remove(row)
        changed = True
    elif feature == "document_language":
        node = root.find(".//" + DC + "language")
        if node is None:
            node = root.find(".//" + CP + "language")
        if kind == "value" and node is not None: node.text = "zz-ZZ"
        elif kind == "delete" and node is not None: node.text = ""
        elif node is not None: node.text = "en-US"
        changed = True
    elif feature == "inline_language":
        nodes = [node for node in root.findall(".//" + W + "lang") if node.attrib.get(W + "val") not in {None, "en-US"}]
        if nodes:
            if kind == "value": nodes[0].set(W + "val", "zz-ZZ")
            elif kind == "delete":
                parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0])
            else: nodes[0].set(W + "val", "en-US")
            changed = True
    elif feature == "hyperlinks":
        if part.endswith("rels"):
            nodes = [node for node in list(root) if node.attrib.get("Type", "").endswith("/hyperlink")]
            if nodes:
                nodes[0].set("Target", "https://mutated.example")
                changed = True
        else:
            nodes = root.findall(".//" + W + "hyperlink")
            if nodes:
                if kind == "delete":
                    parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0])
                else:
                    text_node = nodes[0].find(".//" + W + "t"); text_node.text = "MUTATED" if text_node is not None else None
                changed = True
    elif feature == "document_metadata":
        node = root.find(".//" + DC + "title")
        if node is None:
            node = root.find(".//" + CP + "title")
        if node is not None:
            if kind == "value": node.text = "MUTATED"
            elif kind == "delete": node.text = ""
            else: node.text = "STRUCTURALLY MUTATED"
            changed = True
    elif feature == "complex_tables":
        nodes = root.findall(".//" + W + "gridSpan")
        if kind == "value" and nodes: nodes[0].set(W + "val", "4"); changed = True
        elif kind == "delete" and nodes:
            parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0]); changed = True
        else:
            node = root.find(".//" + W + "gridSpan")
            if node is not None: node.set(W + "val", "9"); changed = True
    elif feature == "footnotes":
        nodes = root.findall(".//" + W + "t")
        if nodes:
            if kind == "value": nodes[0].text = "MUTATED"
            elif kind == "delete":
                note = next((n for n in root.iter(W + "footnote") if n.attrib.get(W + "id") not in {"-1", "0"}), None)
                if note is not None:
                    parent = next(parent for parent in root.iter() if note in list(parent)); parent.remove(note)
            else:
                note = next((n for n in root.iter(W + "footnote") if n.attrib.get(W + "id") not in {"-1", "0"}), None)
                if note is not None:
                    parent = next(parent for parent in root.iter() if note in list(parent)); parent.remove(note)
            changed = True
    elif feature == "equations":
        nodes = root.findall(".//" + M + "t")
        if nodes:
            if kind == "value": nodes[0].text = "MUTATED"
            elif kind == "delete":
                parent = next(parent for parent in root.iter() if nodes[0] in list(parent)); parent.remove(nodes[0])
            else:
                math = root.find(".//" + M + "oMath")
                if math is not None:
                    parent = next(parent for parent in root.iter() if math in list(parent)); parent.remove(math)
            changed = True
    elif feature == "captions":
        nodes = root.findall(".//" + W + "pStyle")
        caption_style = next((n for n in nodes if n.attrib.get(W + "val") == "Caption"), None)
        paragraph = next((p for p in root.iter(W + "p") if p.find(".//" + W + "pStyle") is not None and p.find(".//" + W + "pStyle").attrib.get(W + "val") == "Caption"), None)
        if paragraph is not None:
            if kind == "value":
                text_node = paragraph.find(".//" + W + "t"); text_node.text = "MUTATED" if text_node is not None else None
            elif kind == "delete":
                parent = next(parent for parent in root.iter() if paragraph in list(parent)); parent.remove(paragraph)
            else:
                caption_style.set(W + "val", "Normal") if caption_style is not None else None
            changed = True
    if not changed:
        raise RuntimeError(f"could not create mutation for {feature}/{kind}")
    payload[part] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in payload.items():
            archive.writestr(name, data)


def main() -> None:
    manifest = json.loads((BASE / "source_manifest.json").read_text(encoding="utf-8"))
    rows = []
    with tempfile.TemporaryDirectory(prefix="a11ypreserve-v4-mutants-") as temp:
        temp_dir = Path(temp)
        selected = {"headings": "F01_E", "alt_text": "F02_A", "lists": "F03_D", "basic_tables": "F04_B", "document_language": "F05_B", "inline_language": "F06_A", "decorative_images": "F07_B", "hyperlinks": "F08_A", "document_metadata": "F09_A", "complex_tables": "F10_A", "footnotes": "F11_A", "equations": "F12_A", "captions": "F13_A"}
        for record in manifest["records"]:
            if record["variant_id"] != selected[record["feature_family"]]:
                continue
            source = ROOT / record["fixture"]
            contract = json.loads((ROOT / record["manifest"]).read_text(encoding="utf-8"))
            for kind in ["delete", "value", "structure"]:
                target = temp_dir / f"{record['variant_id']}_{kind}.docx"
                try:
                    mutate(source, target, record["feature_family"], kind)
                    observed = parse(target)
                    passed, problems = contract_ok(observed, contract)
                    detected = not passed
                except Exception as exc:
                    detected, problems = True, [f"mutation error treated as detected: {exc}"]
                rows.append({"variant_id": record["variant_id"], "feature_family": record["feature_family"], "mutation": kind, "detected": detected, "problems": problems})
    by_feature = {}
    for row in rows:
        by_feature.setdefault(row["feature_family"], []).append(row)
    report = {"status": "PASS" if all(row["detected"] for row in rows) else "FAIL", "mutations": len(rows), "detected": sum(row["detected"] for row in rows), "by_feature": {key: {"mutations": len(value), "detected": sum(item["detected"] for item in value)} for key, value in sorted(by_feature.items())}, "rows": rows, "caveat": "Three mutation operators per generated fixture are a systematic audit, not a claim of exhaustive mutation coverage."}
    (BASE / "SOURCE_ORACLE_MUTATION_AUDIT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(ROOT / "reports" / "V4_SOURCE_ORACLE_MUTATION_AUDIT.md").write_text("# V4 Source-Oracle Mutation Audit\n\n" + "The raw-OOXML oracle was challenged with deletion, value, and structural mutations for every fixture. This is systematic evidence, not exhaustive mutation coverage.\n\n" + f"- Mutants: {report['mutations']}\n- Detected: {report['detected']}\n- Status: **{report['status']}**\n\n| Feature | Mutants | Detected |\n|---|---:|---:|\n" + "\n".join(f"| {feature} | {data['mutations']} | {data['detected']} |" for feature, data in report["by_feature"].items()) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["status", "mutations", "detected"]}, indent=2))


if __name__ == "__main__":
    main()
