from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_compare import compare, synthetic_cases  # noqa: E402
from pilot_semantics import extract_docx, extract_pdf  # noqa: E402


def main() -> None:
    pilot2 = ROOT / "pilot2"
    frozen = json.loads((pilot2 / "FROZEN_INPUT_VERIFICATION.json").read_text(encoding="utf-8"))
    validation = json.loads((pilot2 / "reports" / "output_validation.json").read_text(encoding="utf-8"))
    diffs = json.loads((pilot2 / "reports" / "semantic_diff_results.json").read_text(encoding="utf-8"))
    semantic_pairs = {(row.get("fixture"), row.get("converter")) for row in diffs["results"]}
    result = {
        "frozen_input_hashes": frozen["all_match"],
        "source_extraction": {},
        "comparator_synthetic": synthetic_cases(),
        "output_validation_records": len(validation["outputs"]),
        "semantic_diff_records": len(diffs["results"]),
        "semantic_diff_pairs": len(semantic_pairs),
        "pdf_extractor_smoke": None,
        "real_pdf_semantic_regression": {},
    }
    for fixture_id in ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE"):
        path = ROOT / "pilot" / "fixtures" / f"{fixture_id}.docx"
        asir = extract_docx(path)
        result["source_extraction"][fixture_id] = {
            "headings": len(asir["headings"]),
            "figures": len(asir["figures"]),
            "lists": len(asir["lists"]),
            "tables": len(asir["tables"]),
        }
    prior_pdf = ROOT / "outputs" / "G01_chrome.pdf"
    if prior_pdf.exists():
        parsed = extract_pdf(prior_pdf)
        result["pdf_extractor_smoke"] = {"tagged": parsed.get("pdf", {}).get("tagged"), "headings": len(parsed.get("headings", [])), "figures": len(parsed.get("figures", []))}
    for fixture_id in ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE"):
        source = extract_docx(ROOT / "pilot" / "fixtures" / f"{fixture_id}.docx")
        destination = extract_pdf(ROOT / "pilot2" / "outputs" / "libreoffice_pdf" / f"{fixture_id}__LIBREOFFICE.pdf")
        rows = compare(source, destination)
        feature_prefix = {
            "F01_HEADINGS": "heading[",
            "F02_ALT_TEXT": "figure_alt[",
            "F03_LISTS": "list_item[",
            "F04_TABLE": "table[",
        }[fixture_id]
        result["real_pdf_semantic_regression"][fixture_id] = sorted({row["classification"] for row in rows if row["feature"].startswith(feature_prefix)})
    expected = {
        "F01_HEADINGS": {"PRESERVED"},
        "F02_ALT_TEXT": {"DEGRADED"},
        "F03_LISTS": {"PRESERVED"},
        "F04_TABLE": {"PRESERVED"},
    }
    result["real_pdf_semantic_regression_passed"] = all(set(value) == expected[key] for key, value in result["real_pdf_semantic_regression"].items())
    result["all_passed"] = bool(result["frozen_input_hashes"] and all(result["comparator_synthetic"].values()) and result["output_validation_records"] == 8 and result["semantic_diff_pairs"] == 8 and result["semantic_diff_records"] >= result["semantic_diff_pairs"] and result["real_pdf_semantic_regression_passed"])
    result["failures"] = [] if result["all_passed"] else ["one or more pilot2 checks failed"]
    (pilot2 / "reports" / "test_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
