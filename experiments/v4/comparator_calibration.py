from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "v4"
sys.path.insert(0, str(ROOT / "artifact" / "src"))
from v4_comparator import compare_feature_v4  # type: ignore  # noqa: E402

FEATURES = [
    ("headings", "headings"), ("alt_text", "image_alt_text"), ("lists", "lists"),
    ("basic_tables", "table"), ("document_language", "document_language"),
    ("inline_language", "inline_language"), ("decorative_images", "decorative_image"),
    ("hyperlinks", "hyperlinks"), ("document_metadata", "document_title"),
    ("complex_tables", "complex_table"), ("footnotes", "footnotes"),
    ("equations", "equation"), ("captions", "captions"),
]


def pdf(document: dict, **values) -> dict:
    return {"format": "pdf", "tagged": True, "document": document, **values}


def expected_from_intent(intent: str) -> str:
    return {"exact": "EQUIVALENT", "alternate": "EQUIVALENT", "altered": "DIFFERENT", "partial": "PARTIAL", "lost": "LOST", "ambiguous": "UNRESOLVED"}[intent]


def feature_controls(family: str, comparator_feature: str) -> list[dict]:
    controls: list[dict] = []
    for intent in ["exact", "alternate", "altered", "partial", "lost", "ambiguous"]:
        source = {"document": {"language": "en-US"}}
        destination = pdf({"language": "en-US"})
        if family == "headings":
            source["headings"] = [{"level": 1}, {"level": 2}]
            destination["headings"] = [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 2, "evidence": {"pdf_role": "H2"}}]
            if intent == "altered": destination["headings"][1]["level"] = 3
            if intent == "partial": destination["headings"] = destination["headings"][:1]
            if intent == "lost": destination["headings"] = []
            if intent == "ambiguous": destination["headings"][0]["evidence"] = {}
        elif family in {"alt_text", "decorative_images"}:
            source["figures"] = [{"alt": "Chart", "decorative": False}]
            destination["figures"] = [{"alt": "Chart", "decorative": False}]
            if family == "decorative_images" and intent == "alternate": source["figures"] = [{"alt": "", "decorative": True}]; destination["figures"] = [{"alt": "", "decorative": True}]
            if intent == "altered": destination["figures"][0]["alt"] = "Different chart"
            if intent == "partial": destination["figures"] = [{"alt": "", "decorative": True}]
            if intent == "lost": destination["figures"] = []
            if intent == "ambiguous": destination["figures"] = [{"alt": "", "decorative": False}]
        elif family == "lists":
            source["lists"] = [{"type": "unordered", "depth": 0, "text": "A"}, {"type": "unordered", "depth": 0, "text": "B"}]
            destination["lists"] = [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]
            if intent == "altered": destination["lists"][-1]["text"] = "C"
            if intent == "partial": destination["lists"] = [{"type": "L", "depth": 0}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]
            if intent == "lost": destination["lists"] = []
            if intent == "ambiguous": destination["lists"] = [{"type": "L", "depth": 0}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]
        elif family in {"basic_tables", "complex_tables"}:
            if family == "basic_tables":
                source["tables"] = [{"cells": [["A", "B"], ["1", "2"]], "headers": ["A", "B"], "dimensions": {"rows": 2, "columns": 2}}]
                destination["tables"] = [{"identifier": "table-1"}, {"role": "TH"}, {"role": "TH"}, {"role": "TD"}, {"role": "TD"}]
                destination["table_headers"] = [True]
                if intent in {"partial", "ambiguous"}: destination["tables"] = [{"identifier": "table-1"}, {"role": "TH"}, {"role": "TD"}]
            else:
                source["tables"] = [{"cells": [["Group", "Result"], ["A", "1"]], "header_rows": [0, 1], "grid_spans": [[2]]}]
                destination["tables"] = [{"identifier": "table-1"}, {"role": "TH", "scope": "Column", "col_span": "2"}, {"role": "TH", "scope": "Column"}, {"role": "TD"}, {"role": "TD"}]
                if intent in {"partial", "ambiguous"}: destination["tables"] = [{"identifier": "table-1"}, {"role": "TH"}, {"role": "TD"}]
            if intent == "altered": destination["tables"] = [{"identifier": "table-1"}, {"role": "TH"}, {"role": "TD"}]
            if intent == "lost": destination["tables"] = []
        elif family == "document_language":
            source["document"] = {"language": "fr-FR"}
            destination["document"] = {"language": "fr-FR" if intent in {"exact", "alternate"} else ("de-DE" if intent == "altered" else None)}
        elif family == "inline_language":
            source["document"] = {"language": "en-US"}; source["inline_languages"] = [{"text": "bonjour", "language": "fr-FR"}]
            destination["document"] = {"language": "en-US"}; destination["inline_languages"] = [{"text": "bonjour", "language": "fr-FR"}]
            if intent == "altered": destination["inline_languages"][0]["language"] = "es-ES"
            if intent in {"partial", "lost", "ambiguous"}: destination["inline_languages"] = []
        elif family == "hyperlinks":
            source["hyperlinks"] = [{"target": "https://example.org", "text": "Guidance"}]
            destination["hyperlinks"] = [{"target": "https://example.org"}]
            if intent == "altered": destination["hyperlinks"][0]["target"] = "https://other.example"
            if intent in {"partial", "lost", "ambiguous"}: destination["hyperlinks"] = []
        elif family == "document_metadata":
            source["document"] = {"metadata": {"title": "Report"}}
            destination["document"] = {"metadata": {"Title": "Report"}}
            if intent == "altered": destination["document"]["metadata"]["Title"] = "Changed"
            if intent in {"partial", "lost", "ambiguous"}: destination["document"] = {"metadata": {}}
        elif family == "footnotes":
            source["footnotes"] = [{"id": 1, "text": "Note"}]
            destination["footnotes"] = [{"id": 1, "text": "Note", "evidence": {"pdf_role": "Note"}}]
            if intent == "altered": destination["footnotes"][0]["text"] = "Changed"
            if intent == "partial": destination["footnotes"] = [{"id": 1, "text": "", "evidence": {"pdf_role": "Note"}}]
            if intent in {"lost", "ambiguous"}: destination["footnotes"] = []
        elif family == "equations":
            source["equations"] = [{"tokens": ["E", "=", "m", "c", "2"]}]
            destination["equations"] = [{"representation": "PDF /Formula", "expression": "E = mc^2"}]
            if intent == "altered": destination["equations"] = [{"representation": "PDF visible text fallback", "expression": "E = mc^2"}]
            if intent == "partial": destination["equations"] = [{"representation": "PDF visible text fallback", "expression": "E = mc^2"}]
            if intent in {"lost", "ambiguous"}: destination["equations"] = []
        elif family == "captions":
            source["captions"] = [{"text": "Figure 1. Overview."}]
            destination["captions"] = [{"text": "Figure 1. Overview.", "association": "PDF /Caption structure"}]
            if intent == "altered": destination["captions"][0]["text"] = "Figure 1. Changed."
            if intent == "partial": destination["captions"][0]["association"] = "ordered page-text adjacency"
            if intent in {"lost", "ambiguous"}: destination["captions"] = []
        controls.append({"control_id": f"{family}_{intent}", "feature_family": family, "comparator_feature": comparator_feature, "intent": intent, "expected": expected_from_intent(intent), "source": source, "destination": destination})
    return controls


def all_controls() -> list[dict]:
    controls = []
    for family, comparator_feature in FEATURES:
        controls.extend(feature_controls(family, comparator_feature))
    return controls


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    controls_path = BASE / "CALIBRATION_CONTROLS.json"
    if args.freeze or not controls_path.exists():
        controls_path.write_text(json.dumps({"protocol": "experiments/v4/V4_PROTOCOL.md", "control_count": len(all_controls()), "controls": all_controls()}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"frozen": True, "control_count": len(all_controls())}, indent=2))
        return
    frozen = json.loads(controls_path.read_text(encoding="utf-8"))
    rows = []
    for case in frozen["controls"]:
        result = compare_feature_v4(case["source"], case["destination"], case["comparator_feature"], explicit_ambiguity=case["intent"] == "ambiguous")
        raw = result["fidelity_classification"]
        observed = {"EXACT_PRESERVATION": "EQUIVALENT", "SEMANTICALLY_EQUIVALENT": "EQUIVALENT", "MUTATED": "DIFFERENT", "REGENERATED": "DIFFERENT", "PARTIAL_PRESERVATION": "PARTIAL", "LOST": "LOST", "NOT_REPRESENTABLE": "UNRESOLVED", "MEASUREMENT_ERROR": "MEASUREMENT_ERROR"}.get(raw, "UNRESOLVED")
        expected = case["expected"]
        confident = observed in {"EQUIVALENT", "DIFFERENT", "LOST"}
        correct = observed == expected
        rows.append({"control_id": case["control_id"], "feature_family": case["feature_family"], "intent": case["intent"], "expected": expected, "observed": observed, "raw_fidelity": raw, "correct": correct, "unsupported_confident": expected == "UNRESOLVED" and confident, "notes": result.get("notes", "")})
    counts = {key: sum(row[key] for row in rows) for key in ["correct", "unsupported_confident"]}
    report = {"status": "COMPLETE", "control_count": len(rows), "controls_sha256": digest(controls_path), "counts": {"correct": counts["correct"], "incorrect": len(rows) - counts["correct"], "unsupported_confident": counts["unsupported_confident"], "false_positives": sum(row["expected"] in {"DIFFERENT", "LOST"} and row["observed"] == "EQUIVALENT" for row in rows), "false_negatives": sum(row["expected"] == "EQUIVALENT" and row["observed"] in {"PARTIAL", "UNRESOLVED", "LOST"} for row in rows), "correct_unresolved": sum(row["expected"] == "UNRESOLVED" and row["observed"] == "UNRESOLVED" for row in rows)}, "rows": rows, "interpretation": "Controls are purposive diagnostics. They characterize this comparator and do not support population sensitivity/specificity."}
    (BASE / "COMPARATOR_CALIBRATION.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# V4 Comparator Calibration", "", f"- Controls: {report['control_count']}", f"- Correct classifications: {report['counts']['correct']}", f"- False positives: {report['counts']['false_positives']}", f"- False negatives: {report['counts']['false_negatives']}", f"- Correct unresolved: {report['counts']['correct_unresolved']}", f"- Unsupported confident classifications: {report['counts']['unsupported_confident']}", "", "The suite is feature-specific and diagnostic; it is not a validation sample for population sensitivity or specificity.", "", "| Feature | Controls | Correct | FP | FN |", "|---|---:|---:|---:|---:|"]
    for family, _ in FEATURES:
        group = [row for row in rows if row["feature_family"] == family]
        lines.append(f"| {family} | {len(group)} | {sum(r['correct'] for r in group)} | {sum(r['expected'] in {'DIFFERENT','LOST'} and r['observed'] == 'EQUIVALENT' for r in group)} | {sum(r['expected'] == 'EQUIVALENT' and r['observed'] in {'PARTIAL','UNRESOLVED','LOST'} for r in group)} |")
    (ROOT / "reports" / "V4_COMPARATOR_CALIBRATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], indent=2))


if __name__ == "__main__":
    main()
