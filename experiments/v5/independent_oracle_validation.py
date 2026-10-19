from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
V5 = ROOT / "experiments" / "v5"


def raw_evidence(pdf: Path) -> dict:
    raw = pdf.read_bytes().decode("latin-1", errors="ignore")
    document = pymupdf.open(pdf)
    text = "\n".join(page.get_text("text") for page in document)
    links = [link.get("uri") for page in document for link in page.get_links() if link.get("uri")]
    markers = {marker: raw.count(marker) for marker in ("/StructTreeRoot", "/H1", "/H2", "/Figure", "/Alt", "/Artifact", "/L", "/LI", "/Table", "/TH", "/Lang", "/Link", "/URI", "/Title", "/Note", "/Formula", "/Caption")}
    return {"sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "markers": markers, "links": links, "text": text, "pages": len(document)}


def independent_conclusion(family: str, evidence: dict) -> str:
    m = evidence["markers"]
    if family == "headings": return "VERIFIED_PRESERVED" if m["/H1"] + m["/H2"] > 0 else "CONFIRMED_LOST"
    if family == "alt_text": return "VERIFIED_PRESERVED" if m["/Figure"] and m["/Alt"] else "CONFIRMED_LOST"
    if family == "lists": return "VERIFIED_PRESERVED" if m["/L"] and m["/LI"] else "CONFIRMED_LOST"
    if family in {"basic_tables", "document_language", "document_metadata", "inline_language", "hyperlinks", "decorative_images"}:
        required = {"basic_tables": m["/Table"] and m["/TH"], "document_language": m["/Lang"], "document_metadata": m["/Title"], "inline_language": m["/Lang"], "hyperlinks": bool(evidence["links"]) or m["/URI"], "decorative_images": m["/Artifact"] or m["/Figure"]}[family]
        return "VERIFIED_PRESERVED" if required else "CONFIRMED_LOST"
    if family == "footnotes": return "UNRESOLVED_EQUIVALENCE" if m["/Note"] else "CONFIRMED_LOST"
    if family == "equations": return "UNRESOLVED_EQUIVALENCE" if m["/Formula"] or re.search(r"E\s*=\s*m\s*c", evidence["text"], re.I) else "CONFIRMED_LOST"
    if family == "captions": return "UNRESOLVED_EQUIVALENCE" if m["/Caption"] or re.search(r"Figure\s+\d+", evidence["text"], re.I) else "CONFIRMED_LOST"
    if family == "complex_tables": return "UNRESOLVED_EQUIVALENCE" if m["/Table"] and m["/TH"] else "CONFIRMED_LOST"
    return "UNRESOLVED_EQUIVALENCE"


def main() -> None:
    paths = [V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json", V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json"]
    rows = []
    for analysis_path in paths:
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        per_family = {}
        for row in analysis["records"]:
            per_family.setdefault(row["feature_family"], row)
        for family, row in sorted(per_family.items()):
            pdf = ROOT / row["output_path"]
            evidence = raw_evidence(pdf)
            independent = independent_conclusion(family, evidence)
            rows.append({"pipeline": analysis["converter"], "fixture_id": row["fixture_id"], "family": family, "original_classification": row["classification"], "independent_conclusion": independent, "agreement": row["classification"] == independent, "evidence": {"pdf_sha256": evidence["sha256"], "markers": evidence["markers"], "links": evidence["links"], "text_preview": evidence["text"][:300]}})
    payload = {"protocol": "V5 independent raw/PyMuPDF validation", "implementation": "independent marker/text/link inspection; no import of destination extractor, comparator, or classification implementation", "status": "COMPLETE", "sample_size": len(rows), "agreement": sum(row["agreement"] for row in rows), "disagreement": sum(not row["agreement"] for row in rows), "rows": rows}
    (V5 / "independent_oracle_validation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("status", "sample_size", "agreement", "disagreement")}, indent=2))


if __name__ == "__main__": main()
