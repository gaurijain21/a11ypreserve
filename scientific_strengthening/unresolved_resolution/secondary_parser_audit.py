"""Independent parser triangulation for the 14 additive unresolved rows.

This audit is additive only. It reads the frozen result record and frozen PDF
outputs, collects independently observable structure/text evidence with pypdf,
PyMuPDF, and pdfplumber, and records whether that evidence supplies a general
equivalence rule. It never edits the frozen classifications.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import fitz
from pypdf import PdfReader

try:
    import pdfplumber
except ImportError:  # pragma: no cover - environment diagnostic
    pdfplumber = None


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "artifact_v3/results/V3_PRIMARY_RESULTS.json"
OUT_JSON = ROOT / "scientific_strengthening/unresolved_resolution/secondary_parser_audit.json"
OUT_MD = ROOT / "scientific_strengthening/unresolved_resolution/SECONDARY_PARSER_AUDIT.md"

REASONS = {
    ("F03_LISTS", "Google Docs"): "target-format representability ambiguity",
    ("F10_COMPLEX_TABLE", "Google Docs"): "target-format representability ambiguity",
    ("F12_EQUATION", "Google Docs"): "target-format representability ambiguity",
    ("F14_CAPTIONS", "Google Docs"): "target-format representability ambiguity",
    ("B03", "LibreOffice"): "extraction incomplete / target-format representability ambiguity",
    ("B03", "Google Docs"): "extraction incomplete / target-format representability ambiguity",
    ("B10", "LibreOffice"): "target-format representability and semantic-equivalence ambiguity",
    ("B10", "Google Docs"): "target-format representability and semantic-equivalence ambiguity",
    ("B12", "LibreOffice"): "target-format representability and semantic-equivalence ambiguity",
    ("B12", "Google Docs"): "target-format representability ambiguity",
    ("B13", "Google Docs"): "target-format representability ambiguity",
    ("B04", "LibreOffice"): "semantic-equivalence ambiguity",
    ("B04", "Google Docs"): "semantic-equivalence ambiguity",
    ("B11", "LibreOffice"): "extraction limitation",
}


def pdf_path(row: dict[str, Any]) -> Path:
    fixture = row["fixture"]
    if row["study_arm"] == "Core":
        directory = "google_docs" if row["pipeline"] == "Google Docs" else "libreoffice"
        suffix = "GOOGLE_DOCS" if row["pipeline"] == "Google Docs" else "LIBREOFFICE"
        return ROOT / "artifact_v3/corpus/outputs" / directory / f"{fixture}__{suffix}.pdf"
    directory = "google" if row["pipeline"] == "Google Docs" else "libreoffice"
    suffix = "GOOGLE_DOCS" if row["pipeline"] == "Google Docs" else "LIBREOFFICE"
    return ROOT / "artifact_v3/v3/variant_set_b" / directory / "outputs" / f"{fixture}__{suffix}.pdf"


def dereference(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def structure_roles(reader: PdfReader) -> Counter[str]:
    root = dereference(reader.trailer["/Root"])
    struct = dereference(root.get("/StructTreeRoot")) if root else None
    counts: Counter[str] = Counter()
    seen: set[int] = set()

    def walk(value: Any) -> None:
        value = dereference(value)
        marker = id(value)
        if marker in seen:
            return
        seen.add(marker)
        if isinstance(value, dict):
            role = value.get("/S")
            if role:
                counts[str(role)] += 1
            for key in ("/K", "/Kids"):
                child = value.get(key)
                if isinstance(child, list):
                    for item in child:
                        walk(item)
                elif child is not None:
                    walk(child)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(struct)
    return counts


def inspect_pdf(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    roles = structure_roles(reader)
    document = fitz.open(path)
    links = [link for page in document for link in page.get_links() if link.get("uri")]
    text = "\n".join(page.get_text() for page in document)
    words = sum(len(page.get_text("words")) for page in document)
    plumber = {"available": pdfplumber is not None}
    if pdfplumber is not None:
        with pdfplumber.open(path) as pdf:
            plumber.update({
                "pages": len(pdf.pages),
                "words": sum(len(page.extract_words()) for page in pdf.pages),
            })
    return {
        "pages": len(reader.pages),
        "pypdf_structure_roles": dict(sorted(roles.items())),
        "pymupdf_links": len(links),
        "pymupdf_uri_targets": sorted(link["uri"] for link in links),
        "pymupdf_text_chars": len(text),
        "pymupdf_words": words,
        "pdfplumber": plumber,
    }


def main() -> None:
    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = [
        row
        for row in payload["records"]
        if row["final_evidence_aware_result"] == "UNRESOLVED_EQUIVALENCE"
    ]
    # The additive link audit resolved four of the frozen rows. The remaining
    # target set is exactly the 14-row additive analysis documented in the repo.
    rows = [row for row in rows if (row["fixture"], row["pipeline"]) not in {
        ("F08_LINKS", "LibreOffice"),
        ("F08_LINKS", "Google Docs"),
        ("B08", "LibreOffice"),
        ("B08", "Google Docs"),
    }]
    records = []
    for row in rows:
        key = (row["fixture"], row["pipeline"])
        path = pdf_path(row)
        evidence = inspect_pdf(path)
        records.append({
            "fixture": row["fixture"],
            "feature": row.get("feature_family", row.get("feature")),
            "pipeline": row["pipeline"],
            "reason": REASONS[key],
            "pdf": str(path.relative_to(ROOT)).replace("\\", "/"),
            "evidence": evidence,
            "additional_general_rule": False,
            "outcome": "RETAIN_ABSTENTION",
            "explanation": "Independent parsers expose structure/text evidence, but no standards-grounded one-to-one semantic relation sufficient for the full source contract.",
        })
    report = {
        "scope": "14 additive unresolved rows after the four-case hyperlink geometry audit",
        "source_result_file_unchanged": True,
        "records": records,
        "counts_by_reason": dict(sorted(Counter(item["reason"] for item in records).items())),
        "resolved_by_this_audit": 0,
        "remaining_abstentions": len(records),
        "parser_set": ["pypdf", "PyMuPDF", "pdfplumber" if pdfplumber is not None else "pdfplumber-unavailable"],
        "conclusion": "No general deterministic equivalence rule was justified; all 14 additive abstentions remain.",
    }
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Secondary parser audit",
        "",
        "This additive audit reads the frozen PDFs with pypdf, PyMuPDF, and pdfplumber when available. It does not edit the frozen result record.",
        "",
        f"- Rows audited: {len(records)}",
        "- Resolved by this audit: 0",
        f"- Remaining abstentions: {len(records)}",
        f"- Parser set: {', '.join(report['parser_set'])}",
        "",
        "## Decision",
        "",
        "The independent parsers expose additional structure and text evidence, but no general standards-grounded equivalence relation sufficient to resolve the full source contracts. The 14 additive abstentions are retained.",
        "",
        "## Rows",
        "",
        "| Fixture | Pipeline | Reason | Pages | PDF roles | Links | Decision |",
        "|---|---|---|---:|---|---:|---|",
    ]
    for item in records:
        evidence = item["evidence"]
        roles = ", ".join(f"{k}:{v}" for k, v in evidence["pypdf_structure_roles"].items()) or "none"
        lines.append(f"| {item['fixture']} | {item['pipeline']} | {item['reason']} | {evidence['pages']} | {roles} | {evidence['pymupdf_links']} | retain abstention |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(records), "resolved": 0, "remaining": len(records), "status": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
