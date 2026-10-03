"""Small, synthetic comparator calibration set; does not rerun frozen outputs."""
from __future__ import annotations

import json
from pathlib import Path

from phase4_compare import compare_feature

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "final_strengthening" / "COMPARATOR_CALIBRATION.json"


def doc(**values):
    return {"format": "pdf", "document": {"language": "en-US"}, **values}


def controls():
    cases = []
    def add(feature, name, source, destination, truth, kind):
        cases.append({"feature": feature, "name": name, "source": source, "destination": destination, "truth": truth, "kind": kind})

    add("headings", "positive", {"headings": [{"level": 1}, {"level": 2}]}, {"headings": [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 2, "evidence": {"pdf_role": "H2"}}]}, "EQUIVALENT", "positive")
    add("headings", "negative", {"headings": [{"level": 1}, {"level": 2}]}, {"headings": [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 3, "evidence": {"pdf_role": "H3"}}]}, "DIFFERENT", "negative")
    add("headings", "alternate_sequence_uncertain", {"headings": [{"level": 1}, {"level": 2}]}, {"headings": [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 2, "evidence": {"pdf_role": "H2"}}]}, "EQUIVALENT", "alternate-equivalent")

    source_lists = {"lists": [{"type": "unordered", "depth": 0, "text": "A"}, {"type": "unordered", "depth": 0, "text": "B"}]}
    add("lists", "positive", source_lists, {"lists": [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]}, "EQUIVALENT", "positive")
    add("lists", "negative", source_lists, {"lists": [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "B"}, {"type": "LI", "depth": 1, "text": "A"}]}, "DIFFERENT", "negative")
    add("lists", "alternate_without_numbering", source_lists, {"lists": [{"type": "L", "depth": 0}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]}, "UNRESOLVED", "alternate-equivalent")

    informative = {"figures": [{"alt": "Chart", "decorative": False}]}
    add("decorative_image", "positive", informative, {"figures": [{"alt": "Chart", "decorative": False}]}, "EQUIVALENT", "positive")
    add("decorative_image", "negative", informative, {"figures": [{"alt": "", "decorative": True}]}, "DIFFERENT", "negative")
    decorative = {"figures": [{"alt": "Chart", "decorative": False}, {"alt": "", "decorative": True}]}
    add("decorative_image", "alternate_artifact_unavailable", decorative, {"figures": [{"alt": "Chart", "decorative": False}, {"alt": "", "decorative": True}]}, "UNRESOLVED", "alternate-equivalent")

    source_link = {"hyperlinks": [{"target": "https://example.org", "text": "Guidance"}]}
    add("hyperlinks", "positive_target", source_link, {"hyperlinks": [{"target": "https://example.org"}]}, "UNRESOLVED", "positive")
    add("hyperlinks", "negative_target", source_link, {"hyperlinks": [{"target": "https://other.example"}]}, "DIFFERENT", "negative")
    add("hyperlinks", "alternate_named_association", source_link, {"hyperlinks": [{"target": "https://example.org", "text": "Guidance", "association": "Link structure"}]}, "EQUIVALENT", "alternate-equivalent")

    source_table = {"tables": [{"cells": [["A", "B"], ["1", "2"]], "header_rows": [0], "grid_spans": [[1, 1], [1, 1]]}]}
    table_positive = {"tables": [{"role": "Table"}, {"role": "TH", "scope": "Column", "col_span": "1"}, {"role": "TH", "scope": "Column"}, {"role": "TD"}, {"role": "TD"}]}
    add("complex_table", "positive", source_table, table_positive, "EQUIVALENT", "positive")
    add("complex_table", "negative", source_table, {"tables": [{"role": "Table"}, {"role": "TH"}, {"role": "TH"}, {"role": "TD"}, {"role": "TD"}]}, "DIFFERENT", "negative")
    add("complex_table", "alternate_scope_uncertain", source_table, {"tables": [{"role": "Table"}, {"role": "TH", "col_span": "1"}, {"role": "TH"}, {"role": "TD"}, {"role": "TD"}]}, "UNRESOLVED", "alternate-equivalent")

    source_note = {"footnotes": [{"id": 1, "text": "note"}]}
    add("footnotes", "positive", source_note, {"footnotes": [{"id": 1, "text": "note", "evidence": {"pdf_role": "Note"}}]}, "EQUIVALENT", "positive")
    add("footnotes", "negative", source_note, {"footnotes": []}, "DIFFERENT", "negative")
    add("footnotes", "alternate_unmeasured_body", source_note, {"footnotes": [{"id": 1, "text": "", "evidence": {"pdf_role": "Note"}}]}, "UNRESOLVED", "alternate-equivalent")

    source_formula = {"equations": [{"tokens": ["E", "=", "m", "c", "2"]}]}
    add("equation", "positive", source_formula, {"equations": [{"representation": "PDF /Formula", "expression": "E = mc^2"}]}, "EQUIVALENT", "positive")
    add("equation", "negative_visible_only", source_formula, {"equations": [{"representation": "PDF visible text fallback"}]}, "DIFFERENT", "negative")
    add("equation", "alternate_tokens", source_formula, {"equations": [{"representation": "MathML-like", "tokens": ["E", "=", "m", "c", "2"]}]}, "EQUIVALENT", "alternate-equivalent")

    source_caption = {"captions": [{"text": "Figure 1. Overview."}]}
    add("captions", "positive", source_caption, {"captions": [{"text": "Figure 1. Overview.", "association": "PDF /Caption structure"}]}, "EQUIVALENT", "positive")
    add("captions", "negative", source_caption, {"captions": [{"text": "Figure 1. Different."}]}, "DIFFERENT", "negative")
    add("captions", "alternate_adjacency", source_caption, {"captions": [{"text": "Figure 1. Overview.", "association": "ordered page-text adjacency"}]}, "UNRESOLVED", "alternate-equivalent")

    source_language = {"document": {"language": "en-US"}, "inline_languages": [{"text": "Hola", "language": "es-MX"}]}
    add("inline_language", "positive", source_language, {"document": {"language": "en-US"}, "inline_languages": [{"text": "Hola", "language": "es-MX"}]}, "EQUIVALENT", "positive")
    add("inline_language", "negative", source_language, {"document": {"language": "en-US"}, "inline_languages": []}, "DIFFERENT", "negative")
    add("inline_language", "alternate_text_span", source_language, {"document": {"language": "en-US"}, "inline_languages": [{"text": "", "language": "es-MX"}], "pdf_text": "Hola"}, "EQUIVALENT", "alternate-equivalent")
    return cases


def observed_status(result: dict) -> str:
    label = result["fidelity_classification"]
    if label in {"EXACT_PRESERVATION", "SEMANTICALLY_EQUIVALENT"}:
        return "EQUIVALENT"
    if label in {"MUTATED", "REGENERATED", "LOST"}:
        return "DIFFERENT"
    return "UNRESOLVED"


def main() -> None:
    rows = []
    for case in controls():
        result = compare_feature(case["source"], case["destination"], case["feature"])
        observed = observed_status(result)
        expected = case["truth"]
        if expected == "UNRESOLVED":
            verdict = "CORRECT_UNRESOLVED" if observed == "UNRESOLVED" else "FALSE_POSITIVE"
        elif expected == observed:
            verdict = "CORRECT"
        elif expected == "EQUIVALENT" and observed == "UNRESOLVED":
            verdict = "FALSE_NEGATIVE"
        elif expected == "DIFFERENT" and observed == "EQUIVALENT":
            verdict = "FALSE_POSITIVE"
        else:
            verdict = "UNRESOLVED"
        rows.append({"feature": case["feature"], "name": case["name"], "kind": case["kind"], "expected": expected, "observed": observed, "raw_fidelity": result["fidelity_classification"], "verdict": verdict, "notes": result.get("notes", "")})
    counts = {key: sum(row["verdict"] == key for row in rows) for key in ["CORRECT", "CORRECT_UNRESOLVED", "FALSE_POSITIVE", "FALSE_NEGATIVE", "UNRESOLVED"]}
    report = {"status": "COMPLETE", "control_count": len(rows), "counts": counts, "scope": "synthetic comparator calibration only; no frozen fixture/output was changed or rerun", "rows": rows}
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"control_count": len(rows), "counts": counts}, indent=2))


if __name__ == "__main__":
    main()
