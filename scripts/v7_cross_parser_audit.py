"""Compare independent pypdf role observations with archived PyMuPDF markers."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "experiments" / "v7" / "V7_CROSS_PARSER.json"


def main() -> None:
    case_dir = ROOT / "experiments/v7/independent_oracle_cases"
    analyses = [
        ROOT / "experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json",
        ROOT / "experiments/v4/conversions/google/analysis/V4_GOOGLE_ANALYSIS.json",
        ROOT / "experiments/v4/conversions/word/analysis/V4_WORD_ANALYSIS.json",
    ]
    rows = []
    for analysis_path in analyses:
        data = json.loads(analysis_path.read_text(encoding="utf-8"))
        for record in data["records"]:
            key = (record["converter"], record["fixture_id"])
            case_path = case_dir / f"{record['converter'].replace(' ', '_')}_{record['fixture_id']}.json"
            other = json.loads(case_path.read_text(encoding="utf-8"))
            archived = record.get("evidence", {}).get("secondary", {}).get("serialized_marker_counts", {})
            roles = other.get("destination_projection", {}).get("role_counts", {})
            comparisons = {}
            for role in ("H1", "Figure", "Artifact", "L", "LI", "Table", "TH", "TD", "Note", "Formula", "Caption"):
                comparisons[role] = {"pypdf": roles.get("/" + role, 0), "pymupdf": archived.get("/" + role, 0), "equal": roles.get("/" + role, 0) == archived.get("/" + role, 0)}
            rows.append({"pipeline": record["converter"], "fixture_id": record["fixture_id"], "comparisons": comparisons})
    disagreements = [row for row in rows if any(not value["equal"] for value in row["comparisons"].values())]
    report = {
        "protocol": "V7 pypdf-versus-archived-PyMuPDF marker comparison",
        "cases": len(rows),
        "cases_with_any_marker_count_difference": len(disagreements),
        "comparison_units": len(rows) * 11,
        "disagreement_units": sum(1 for row in rows for value in row["comparisons"].values() if not value["equal"]),
        "interpretation": "Parser disagreement is an extraction diagnostic, not ground truth. Archived PyMuPDF markers and fresh pypdf structure-role counts use different traversal boundaries and are not expected to be byte-identical.",
        "rows": rows,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("cases", "cases_with_any_marker_count_difference", "comparison_units", "disagreement_units")}, indent=2))


if __name__ == "__main__":
    main()
