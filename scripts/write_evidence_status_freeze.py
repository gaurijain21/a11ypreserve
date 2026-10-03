"""Write an evidence-status overlay without modifying the primary freeze."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/full_experiment/PRIMARY_RESULTS_FREEZE.json"
OUT = ROOT / "results/full_experiment/EVIDENCE_STATUS_FREEZE_V2.json"

PARTIAL = {
    ("F01_HEADINGS", "Google Docs"): "OBSERVED_PARTIAL",
    ("F03_LISTS", "Google Docs"): "UNRESOLVED_EQUIVALENCE",
    ("F07_DECORATIVE_IMAGE", "LibreOffice"): "OBSERVED_PARTIAL",
    ("F07_DECORATIVE_IMAGE", "Google Docs"): "OBSERVED_PARTIAL",
    ("F08_LINKS", "LibreOffice"): "UNRESOLVED_EQUIVALENCE",
    ("F08_LINKS", "Google Docs"): "UNRESOLVED_EQUIVALENCE",
    ("F10_COMPLEX_TABLE", "Google Docs"): "UNRESOLVED_EQUIVALENCE",
    ("F12_EQUATION", "Google Docs"): "UNRESOLVED_EQUIVALENCE",
    ("F14_CAPTIONS", "Google Docs"): "UNRESOLVED_EQUIVALENCE",
}

def main() -> None:
    raw = SOURCE.read_bytes()
    freeze = json.loads(raw)
    records = []
    for item in freeze["records"]:
        key = (item["fixture"], item["converter"])
        if key in PARTIAL:
            status = PARTIAL[key]
        elif item["classification"] == "PRESERVED":
            status = "VERIFIED_EQUIVALENCE"
        elif item["classification"] == "ALTERED":
            status = "OBSERVED_DIFFERENCE"
        elif item["classification"] == "LOST" and key in {("F06_INLINE_LANGUAGE", "Google Docs"), ("F11_FOOTNOTES", "Google Docs")}:
            status = "INDEPENDENTLY_CONFIRMED_ABSENCE"
        elif item["classification"] == "MEASUREMENT_ERROR":
            status = "MEASUREMENT_FAILURE"
        else:
            status = "INSUFFICIENT_EVIDENCE"
        records.append({"fixture": item["fixture"], "feature": item["feature"], "converter": item["converter"], "outcome": item["classification"], "evidence_status": status, "source_sha256": item["source_sha256"], "destination_sha256": item["destination_sha256"], "evidence_path": {"source_extraction": f"results/full_experiment/extracted/source/{item['fixture']}.json", "destination_extraction": f"results/full_experiment/extracted/{'libreoffice' if item['converter'] == 'LibreOffice' else 'google_docs'}/{item['fixture']}.json"}})
    result = {"freeze_type": "EVIDENCE_STATUS_FREEZE_V2", "primary_results_freeze_sha256": hashlib.sha256(raw).hexdigest(), "primary_outcomes_unchanged": True, "allowed_evidence_statuses": ["VERIFIED_EQUIVALENCE", "OBSERVED_DIFFERENCE", "OBSERVED_PARTIAL", "INDEPENDENTLY_CONFIRMED_ABSENCE", "UNRESOLVED_EQUIVALENCE", "INSUFFICIENT_EVIDENCE", "MEASUREMENT_FAILURE"], "records": records}
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "outcomes_unchanged": True, "status_counts": {status: sum(r["evidence_status"] == status for r in records) for status in result["allowed_evidence_statuses"]}}, indent=2))

if __name__ == "__main__":
    main()
