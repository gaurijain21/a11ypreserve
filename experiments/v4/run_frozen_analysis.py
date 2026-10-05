from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import fitz

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "experiments" / "v4"))
from extract_semantics import docx_extract, pdf_extract  # noqa: E402
from v4_comparator import compare_feature_v4  # noqa: E402

V4 = ROOT / "experiments" / "v4"
OUT = V4 / "conversions" / "libreoffice"
EXTRACTED = OUT / "extracted"
ANALYSIS = OUT / "analysis"
FEATURES = {
    "headings": "headings", "alt_text": "image_alt_text", "lists": "lists", "basic_tables": "table",
    "alternative_text": "image_alt_text", "document_title": "document_title",
    "document_language": "document_language", "inline_language": "inline_language", "decorative_images": "decorative_image",
    "hyperlinks": "hyperlinks", "document_metadata": "document_title", "complex_tables": "complex_table",
    "footnotes": "footnotes", "equations": "equation", "captions": "captions",
}
RAW_TO_FROZEN = {
    "EXACT_PRESERVATION": "VERIFIED_PRESERVED", "SEMANTICALLY_EQUIVALENT": "VERIFIED_PRESERVED",
    "PARTIAL_PRESERVATION": "OBSERVED_PARTIAL", "MUTATED": "ALTERED", "REGENERATED": "ALTERED",
    "MEASUREMENT_ERROR": "MEASUREMENT_ERROR", "INVALID_CONVERSION": "MEASUREMENT_ERROR",
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def secondary(path: Path) -> dict[str, Any]:
    doc = fitz.open(path)
    raw = path.read_bytes().decode("latin-1", errors="ignore")
    markers = ["/StructTreeRoot", "/ParentTree", "/RoleMap", "/Lang", "/Alt", "/Title", "/Artifact", "/Formula", "/Note", "/Caption", "/Table", "/TH", "/TD", "/L", "/LI", "/Figure", "/H1", "/H2", "/H3", "/H4", "/H5", "/H6"]
    text = "\n".join(page.get_text("text") for page in doc)
    links = [link.get("uri") for page in doc for link in page.get_links() if link.get("uri")]
    return {
        "library": "PyMuPDF " + fitz.VersionBind, "pages": len(doc), "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "text_preview": text[:2000], "links": links, "page_image_counts": [len(page.get_images(full=True)) for page in doc],
        "serialized_marker_counts": {marker: raw.count(marker) for marker in markers}, "pdf_sha256": sha256(path),
    }

def corroborated_absence(feature: str, destination: dict[str, Any], second: dict[str, Any]) -> bool:
    markers = second["serialized_marker_counts"]
    if feature == "headings": return not destination.get("headings") and not any(markers.get("/H" + str(i), 0) for i in range(1, 7))
    if feature == "image_alt_text" or feature == "decorative_image": return not destination.get("figures") and not markers.get("/Figure") and not any(second["page_image_counts"])
    if feature == "lists": return not destination.get("lists") and not markers.get("/L") and not markers.get("/LI")
    if feature == "table" or feature == "complex_table": return not destination.get("tables") and not markers.get("/Table") and not markers.get("/TH") and not markers.get("/TD")
    if feature == "hyperlinks": return not destination.get("hyperlinks") and not second.get("links")
    if feature == "document_title": return destination.get("title") is None and not markers.get("/Title")
    if feature == "footnotes": return not destination.get("footnotes") and not markers.get("/Note") and "footnote" not in second["text_preview"].lower()
    if feature == "equation": return not destination.get("equations") and not markers.get("/Formula") and not re.search(r"E\s*=\s*m\s*c", second["text_preview"], re.I)
    if feature == "captions": return not destination.get("captions") and not markers.get("/Caption") and not re.search(r"Figure\s+\d+", second["text_preview"], re.I)
    if feature == "document_language": return destination.get("language") is None and not markers.get("/Lang")
    if feature == "inline_language": return not destination.get("inline_languages") and not any(markers.get(token, 0) for token in ("fr-FR", "es-ES", "de-DE", "it-IT", "ja-JP"))
    return False

def final_classification(raw: dict[str, Any], feature: str, destination: dict[str, Any], second: dict[str, Any]) -> tuple[str, str]:
    fidelity = raw.get("fidelity_classification")
    if fidelity in RAW_TO_FROZEN: return RAW_TO_FROZEN[fidelity], "frozen raw-fidelity mapping"
    if fidelity == "LOST":
        if corroborated_absence(feature, destination, second): return "CONFIRMED_LOST", "raw loss corroborated by independent PyMuPDF/object-marker absence"
        return "UNRESOLVED_EQUIVALENCE", "raw loss not independently corroborated; conservative abstention"
    if fidelity in {"NOT_REPRESENTABLE", "NOT_APPLICABLE"}: return "UNRESOLVED_EQUIVALENCE", "frozen non-representability/abstention mapping"
    return "MEASUREMENT_ERROR", "unmapped comparator outcome treated as measurement error"

def feature_row(source_path: Path, output_path: Path, fixture_id: str, family: str, role: str, corpus: str, expected_source_hash: str | None = None) -> dict[str, Any]:
    source = docx_extract(source_path)
    destination = pdf_extract(output_path)
    second = secondary(output_path)
    feature = FEATURES[family]
    raw = compare_feature_v4(source, destination, feature)
    classification, classification_basis = final_classification(raw, feature, destination, second)
    out_path = EXTRACTED / corpus
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / f"{fixture_id}.json").write_text(json.dumps({"source": source, "destination": destination, "secondary": second}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "corpus": corpus, "fixture_id": fixture_id, "feature_family": family, "comparator_feature": feature, "role": role,
        "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha256(source_path), "expected_source_sha256": expected_source_hash,
        "output_path": str(output_path.relative_to(ROOT)).replace("\\", "/"), "output_sha256": sha256(output_path),
        "converter": "LibreOffice", "raw_fidelity": raw.get("fidelity_classification"), "destination_accessibility": raw.get("destination_accessibility"),
        "classification": classification, "classification_basis": classification_basis, "notes": raw.get("notes", ""),
        "evidence": {"primary": raw.get("evidence", []), "secondary": second},
    }

def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {"total": len(rows), "counts": dict(Counter(row["classification"] for row in rows)), "by_feature": {feature: dict(Counter(row["classification"] for row in rows if row["feature_family"] == feature)) for feature in FEATURES}}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(OUT / "manifest.json"))
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    atomic_manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for entry in atomic_manifest["records"]:
        fixture = entry["variant_id"]
        family = entry["feature_family"]
        record = next(row for row in manifest["records"] if row["fixture_id"] == fixture and row["corpus"] == "atomic")
        rows.append(feature_row(ROOT / entry["fixture"], ROOT / record["output_path"], fixture, family, entry["role"], "atomic", entry["source_sha256"]))
    realistic_rows: list[dict[str, Any]] = []
    realistic = json.loads((V4 / "realistic" / "REALISTIC_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
    for entry in realistic["records"]:
        doc_id = entry["document_id"]
        record = next(row for row in manifest["records"] if row["fixture_id"] == doc_id and row["corpus"] == "realistic")
        source_path, output_path = ROOT / entry["path"], ROOT / record["output_path"]
        source = docx_extract(source_path)
        destination = pdf_extract(output_path)
        second = secondary(output_path)
        for contract_index, contract in enumerate(entry["contracts"], start=1):
            family = contract["property"]
            if family not in FEATURES: continue
            raw = compare_feature_v4(source, destination, FEATURES[family])
            classification, basis = final_classification(raw, FEATURES[family], destination, second)
            realistic_rows.append({"corpus": "realistic", "document_id": doc_id, "contract_index": contract_index, "feature_family": family, "contract": contract, "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha256(source_path), "output_path": str(output_path.relative_to(ROOT)).replace("\\", "/"), "output_sha256": sha256(output_path), "raw_fidelity": raw.get("fidelity_classification"), "classification": classification, "classification_basis": basis, "notes": raw.get("notes", ""), "evidence": {"primary": raw.get("evidence", []), "secondary": second}})
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    payload = {"analysis_version": "v4-frozen-analysis-runner-1", "protocol": "experiments/v4/V4_PROTOCOL.md", "converter": "LibreOffice", "manifest": str(Path(args.manifest).relative_to(ROOT)).replace("\\", "/"), "method": "frozen source extractor + frozen V4 comparator boundary + independent PyMuPDF secondary evidence", "records": rows, "summary": summarize(rows), "holdout": summarize([row for row in rows if row["role"] == "holdout"]), "development": summarize([row for row in rows if row["role"] != "holdout"]), "realistic": {"records": realistic_rows, "summary": summarize(realistic_rows)}}
    (ANALYSIS / "V4_LIBREOFFICE_ANALYSIS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"atomic": payload["summary"], "development": payload["development"], "holdout": payload["holdout"], "realistic": payload["realistic"]["summary"]}, indent=2, ensure_ascii=False))

if __name__ == "__main__": main()
