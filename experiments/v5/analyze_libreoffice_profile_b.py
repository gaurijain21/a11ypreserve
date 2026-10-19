from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
V5 = ROOT / "experiments" / "v5"
sys.path.insert(0, str(V4)); sys.path.insert(0, str(ROOT / "artifact" / "src"))
from run_frozen_analysis import docx_extract, pdf_extract, secondary, final_classification, FEATURES  # noqa: E402
from v4_comparator import compare_feature_v4  # noqa: E402


def digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def main() -> None:
    source = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    manifest = json.loads((V5 / "conversions" / "libreoffice_profile_b" / "manifest.json").read_text(encoding="utf-8"))
    v4_analysis = json.loads((V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
    old = {row["fixture_id"]: row for row in v4_analysis["records"]}
    new_manifest = {row["fixture_id"]: row for row in manifest["records"]}
    rows = []
    for entry in source["records"]:
        fixture = entry["variant_id"]
        source_data = docx_extract(ROOT / entry["fixture"])
        output = ROOT / new_manifest[fixture]["output_path"]
        destination = pdf_extract(output); second = secondary(output)
        feature = FEATURES[entry["feature_family"]]
        raw = compare_feature_v4(source_data, destination, feature)
        classification, basis = final_classification(raw, feature, destination, second)
        extracted = {"source": source_data, "destination": destination, "secondary": second}
        ext_path = V5 / "extracted" / "libreoffice_profile_b" / f"{fixture}.json"
        ext_path.parent.mkdir(parents=True, exist_ok=True)
        ext_path.write_text(json.dumps(extracted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append({"fixture_id": fixture, "feature_family": entry["feature_family"], "role": entry["role"], "v4_classification": old[fixture]["classification"], "v5_classification": classification, "classification_changed": old[fixture]["classification"] != classification, "v4_output_sha256": old[fixture]["output_sha256"], "v5_output_sha256": new_manifest[fixture]["output"]["sha256"], "v4_pdf_facts": {key: old[fixture].get("evidence", {}).get("secondary", {}).get(key) for key in ()}, "v5_pdf_facts": {key: new_manifest[fixture]["output"].get(key) for key in ("pdf_version", "tagged", "producer", "raw_pdfa_markers")}, "normalized_semantics_sha256": digest(extracted), "classification_basis": basis})
    payload = {
        "analysis_version": "v5-libreoffice-profile-b-1",
        "condition": "V5_PROFILE_B",
        "settings": manifest["settings"],
        "status": "COMPLETE",
        "records": rows,
        "counts": dict(Counter(row["v5_classification"] for row in rows)),
        "classification_changes": [row for row in rows if row["classification_changed"]],
        "profile_summary": {
            "v4_pdfa_setting": "SelectPdfVersion=1 / PDF-A-1b",
            "v5_pdf_setting": "SelectPdfVersion=0 / default PDF 1.7",
            "v5_tagged_count": sum(bool(row["v5_pdf_facts"].get("tagged")) for row in rows),
            "v5_pdfa_marker_totals": {
                marker: sum((row["v5_pdf_facts"].get("raw_pdfa_markers") or {}).get(marker, 0) for row in rows)
                for marker in ("pdfaid:part", "GTS_PDFA1", "PDF/A")
            },
        },
    }
    (V5 / "LIBREOFFICE_PROFILE_B_ANALYSIS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "counts": payload["counts"], "classification_changes": len(payload["classification_changes"]), "profile_summary": payload["profile_summary"]}, indent=2))


if __name__ == "__main__": main()
