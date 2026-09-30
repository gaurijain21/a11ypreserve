from __future__ import annotations

import json
from pathlib import Path

import fitz
from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "integrated_study"


def deref(value):
    return value.get_object() if hasattr(value, "get_object") else value


def walk(node, roles: list[str], langs: list[str]) -> None:
    node = deref(node)
    if not isinstance(node, DictionaryObject):
        return
    role = node.get("/S")
    if role:
        roles.append(str(role))
    lang = node.get("/Lang")
    if lang:
        langs.append(str(lang))
    kids = deref(node.get("/K"))
    if isinstance(kids, ArrayObject):
        for child in kids:
            walk(child, roles, langs)
    elif kids is not None:
        walk(kids, roles, langs)


def inspect(path: Path, expected_text: str) -> dict:
    raw = path.read_bytes()
    reader = PdfReader(str(path))
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    roles: list[str] = []
    langs: list[str] = []
    if isinstance(struct, DictionaryObject):
        walk(struct.get("/K"), roles, langs)
    pdf = fitz.open(str(path))
    page_text = "\n".join(page.get_text() for page in pdf)
    links = [link for page in pdf for link in page.get_links()]
    marker_absent = not any(marker in raw.decode("latin-1", errors="ignore") for marker in ("/Note", "/Footnote", "/Lang es-MX", "es-MX"))
    return {
        "path": str(path.relative_to(ROOT)),
        "pypdf_roles": sorted(set(roles)),
        "pypdf_languages": sorted(set(langs)),
        "pypdf_absence": {"note_or_footnote": not any(role in {"/Note", "/Footnote"} for role in roles), "es-MX": "es-MX" not in langs},
        "raw_marker_scan_absence": marker_absent,
        "pymupdf_text_contains_expected": expected_text in page_text,
        "pymupdf_link_count": len(links),
        "pymupdf_text_preview": page_text[:500],
    }


def main() -> None:
    cases = [
        ("I02_EDUCATIONAL_HANDOUT", "inline_language", "Buenos días"),
        ("I02_EDUCATIONAL_HANDOUT", "footnotes", "This note identifies the source used for the classroom example."),
        ("I03_POLICY_NOTE", "inline_language", "información pública"),
    ]
    records = []
    for document, feature, expected_text in cases:
        path = OUT / "outputs" / "google_docs" / f"{document}__GOOGLE_DOCS.pdf"
        result = inspect(path, expected_text)
        result.update({"document": document, "feature": feature, "expected_text": expected_text})
        if feature == "inline_language":
            result["status"] = "INDEPENDENTLY_CONFIRMED_ABSENCE" if result["pypdf_absence"]["es-MX"] and result["raw_marker_scan_absence"] and result["pymupdf_text_contains_expected"] else "UNRESOLVED_EQUIVALENCE"
        else:
            result["status"] = "INDEPENDENTLY_CONFIRMED_ABSENCE" if result["pypdf_absence"]["note_or_footnote"] and result["raw_marker_scan_absence"] and result["pymupdf_text_contains_expected"] else "UNRESOLVED_EQUIVALENCE"
        records.append(result)
    output = {"tool_paths": ["pypdf structure traversal", "PyMuPDF page/text/link extraction", "raw serialized-PDF marker scan"], "records": records}
    (OUT / "PARSER_TRIANGULATION.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Integrated parser triangulation", "", "The three Google Docs rows that the primary comparator marked LOST were checked using pypdf structure traversal, PyMuPDF page/text/link extraction, and a raw serialized-PDF marker scan. This is secondary evidence for the integrated sanity check; it does not alter the primary 26-case freeze.", "", "| Document | Feature | Status | Pypdf absence | Raw marker scan | PyMuPDF visible text |", "|---|---|---|---|---|---|"]
    for row in records:
        absence = row["pypdf_absence"]["es-MX"] if row["feature"] == "inline_language" else row["pypdf_absence"]["note_or_footnote"]
        lines.append(f"| {row['document']} | {row['feature']} | {row['status']} | {absence} | {row['raw_marker_scan_absence']} | {row['pymupdf_text_contains_expected']} |")
    (OUT / "PARSER_TRIANGULATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "statuses": [row["status"] for row in records]}, indent=2))


if __name__ == "__main__":
    main()
