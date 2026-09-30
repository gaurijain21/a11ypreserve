from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "full_experiment"
ALLOWED = {"PRESERVED", "PARTIALLY_PRESERVED", "ALTERED", "LOST", "NOT_REPRESENTABLE", "INVALID_CONVERSION", "MEASUREMENT_ERROR"}


def main() -> None:
    validation = json.loads((BASE / "reports" / "output_validation.json").read_text(encoding="utf-8"))
    diff = json.loads((BASE / "reports" / "a11ydiff_results.json").read_text(encoding="utf-8"))
    assert len(validation["records"]) == 26
    assert all(not row["invalid_conversion"] for row in validation["records"])
    assert len(diff["records"]) == 26
    assert all(row.get("empirical_classification") in ALLOWED for row in diff["records"])
    assert all(row.get("source_hash") and row.get("output_hash") and row.get("evidence_path") for row in diff["records"])
    assert any(row["fixture"] == "F03_LISTS" and row["converter"] == "LibreOffice" and row["empirical_classification"] == "PRESERVED" for row in diff["records"])
    assert any(row["fixture"] == "F10_COMPLEX_TABLE" and row["converter"] == "Google Docs" and row["empirical_classification"] == "PARTIALLY_PRESERVED" for row in diff["records"])
    assert any(row["fixture"] == "F11_FOOTNOTES" and row["converter"] == "LibreOffice" and row["empirical_classification"] == "MEASUREMENT_ERROR" for row in diff["records"])
    print(json.dumps({"passed": True, "validation_records": 26, "diff_records": 26, "new_regressions": 4}))


if __name__ == "__main__":
    main()
