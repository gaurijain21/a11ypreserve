from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments/v4"))
from run_frozen_analysis import docx_extract, pdf_extract, compare_feature_v4, final_classification, secondary, FEATURES
BASE = ROOT / "experiments/v4/conversions/libreoffice/repeatability"
def digest(value): return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
def main():
    run_manifest = json.loads((BASE / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
    source_manifest = json.loads((ROOT / "experiments/v4/source_manifest.json").read_text(encoding="utf-8"))
    entries = {x["variant_id"]: x for x in source_manifest["records"]}
    grouped = {}
    for record in run_manifest["records"]:
        fixture = record["fixture_id"]
        source = ROOT / entries[fixture]["fixture"]
        output = ROOT / record["output_path"]
        source_data = docx_extract(source); destination = pdf_extract(output); second = secondary(output)
        feature = FEATURES[entries[fixture]["feature_family"]]
        raw = compare_feature_v4(source_data, destination, feature)
        classification, basis = final_classification(raw, feature, destination, second)
        grouped.setdefault(fixture, []).append({"run": record["run"], "output_path": record["output_path"], "output_sha256": record["output_sha256"], "extraction_sha256": digest(destination), "classification": classification, "raw_fidelity": raw.get("fidelity_classification"), "classification_basis": basis})
    rows=[]
    for fixture, records in sorted(grouped.items()):
        rows.append({"fixture_id": fixture, "runs": records, "byte_identity": len({x["output_sha256"] for x in records}) == 1, "extraction_identity": len({x["extraction_sha256"] for x in records}) == 1, "classification_identity": len({x["classification"] for x in records}) == 1})
    payload = {"protocol": "experiments/v4/REPEATABILITY_MANIFEST.json", "pipeline": "LibreOffice", "records": rows, "fixtures": len(rows), "runs": sum(len(x["runs"]) for x in rows), "byte_identical": sum(x["byte_identity"] for x in rows), "extraction_identical": sum(x["extraction_identity"] for x in rows), "classification_stable": sum(x["classification_identity"] for x in rows), "classification_counts": dict(Counter(x["runs"][0]["classification"] for x in rows)), "conclusion": "All selected LibreOffice repeatability classifications were compared using the frozen extractor/comparator and independent output hashes."}
    (BASE / "REPEATABILITY_RESULTS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("fixtures","runs","byte_identical","extraction_identical","classification_stable","classification_counts")}, indent=2))
if __name__ == "__main__": main()
