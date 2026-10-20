"""Post-hoc diagnostic for coarse complex-table classifications.

This does not rewrite V4/V6 labels. It tests whether a role-count delta can
surface a complex-table fault that remains inside OBSERVED_PARTIAL.
"""
from __future__ import annotations

import json
from pathlib import Path

from v7_independent_oracle_audit import destination_projection

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
REPORT = ROOT / "experiments" / "v7" / "V7_COMPLEX_TABLE_DIAGNOSTIC.json"


def main() -> None:
    mutation = json.loads((V6 / "V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    rows = []
    for item in mutation["rows"]:
        if item["feature_family"] != "complex_tables" or not (item.get("mutation_applied") and item.get("valid_pdf")):
            continue
        before = destination_projection(ROOT / item["baseline_pdf_path"])
        after = destination_projection(ROOT / item["mutated_pdf_path"])
        before_th = before["role_counts"].get("/TH", 0)
        after_th = after["role_counts"].get("/TH", 0)
        rows.append({
            "fixture_id": item["fixture_id"],
            "baseline_classification": item["baseline_classification"],
            "mutated_classification": item["mutated_classification"],
            "baseline_th_count": before_th,
            "mutated_th_count": after_th,
            "role_delta_alert": before_th != after_th,
        })
    report = {
        "protocol": "V7 complex-table role-delta diagnostic",
        "cases": len(rows),
        "role_delta_alerts": sum(row["role_delta_alert"] for row in rows),
        "interpretation": "This additive diagnostic exposes a role-count change without retroactively changing the frozen six-way classification. It is evidence of a coarse-category blind spot, not a repaired V4 result.",
        "rows": rows,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": report["cases"], "role_delta_alerts": report["role_delta_alerts"]}, indent=2))


if __name__ == "__main__":
    main()
