from __future__ import annotations

import json
from pathlib import Path

from phase4_compare import classify_observation, compare_feature


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit" / "phase6_comparator_tests.json"


def check(name: str, actual: str, expected: str, details: str = "") -> dict:
    return {"name": name, "actual": actual, "expected": expected, "passed": actual == expected, "details": details}


def main() -> None:
    cases = []
    cases.append(check("exact", classify_observation("x", "x", exact=True)["fidelity_classification"], "EXACT_PRESERVATION"))
    cases.append(check("semantic_equivalence", classify_observation("x", {"equivalent": True}, equivalent=True)["fidelity_classification"], "SEMANTICALLY_EQUIVALENT"))
    cases.append(check("partial", classify_observation("x", "part", partial=True)["fidelity_classification"], "PARTIAL_PRESERVATION"))
    cases.append(check("alteration", classify_observation("x", "changed", mutated=True)["fidelity_classification"], "MUTATED"))
    cases.append(check("regeneration", classify_observation("x", "generated", regenerated=True)["fidelity_classification"], "REGENERATED"))
    cases.append(check("loss", classify_observation("x", None)["fidelity_classification"], "LOST"))
    cases.append(check("not_representable", classify_observation("x", "unsupported", representable=False)["fidelity_classification"], "NOT_REPRESENTABLE"))
    cases.append(check("measurement_error", classify_observation("x", "ambiguous", measured=False)["fidelity_classification"], "MEASUREMENT_ERROR"))
    cases.append(check("invalid_conversion", classify_observation("x", {}, valid_conversion=False)["fidelity_classification"], "INVALID_CONVERSION"))

    source_headings = {"headings": [{"level": 1}, {"level": 2}]}
    same_headings = {"headings": [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 2, "evidence": {"pdf_role": "H2"}}]}
    extra_heading = {"headings": [{"level": 1, "evidence": {"pdf_role": "H1"}}, {"level": 2, "evidence": {"pdf_role": "H2"}}, {"level": 1, "evidence": {"pdf_role": "H1"}}]}
    cases.append(check("headings_exact_sequence", compare_feature(source_headings, same_headings, "headings")["fidelity_classification"], "SEMANTICALLY_EQUIVALENT"))
    cases.append(check("headings_extra_structure", compare_feature(source_headings, extra_heading, "headings")["fidelity_classification"], "PARTIAL_PRESERVATION"))

    source_lists = {"lists": [{"type": "unordered", "depth": 0, "text": "A"}, {"type": "unordered", "depth": 0, "text": "B"}]}
    same_lists = {"lists": [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "B"}]}
    reordered_lists = {"lists": [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "B"}, {"type": "LI", "depth": 1, "text": "A"}]}
    duplicated_lists = {"lists": [{"type": "L", "depth": 0, "list_type": "unordered"}, {"type": "LI", "depth": 1, "text": "A"}, {"type": "LI", "depth": 1, "text": "A"}]}
    cases.append(check("lists_same_order", compare_feature(source_lists, same_lists, "lists")["fidelity_classification"], "SEMANTICALLY_EQUIVALENT"))
    cases.append(check("lists_reordered", compare_feature(source_lists, reordered_lists, "lists")["fidelity_classification"], "PARTIAL_PRESERVATION"))
    cases.append(check("lists_duplicated", compare_feature(source_lists, duplicated_lists, "lists")["fidelity_classification"], "PARTIAL_PRESERVATION"))

    source_figures = {"figures": [{"alt": "A chart", "decorative": False}]}
    changed_figure = {"figures": [{"alt": "A graph", "decorative": False}]}
    cases.append(check("alt_text_mutation", compare_feature(source_figures, changed_figure, "image_alt_text")["fidelity_classification"], "MUTATED"))

    source_inline = {"document": {"language": "en-US"}, "inline_languages": [{"text": "Hola", "language": "es-MX"}]}
    missing_inline = {"document": {"language": "en-US"}, "inline_languages": []}
    cases.append(check("inline_language_missing", compare_feature(source_inline, missing_inline, "inline_language")["fidelity_classification"], "PARTIAL_PRESERVATION"))

    source_link = {"hyperlinks": [{"target": "https://example.org", "text": "Guidance"}]}
    missing_link = {"hyperlinks": []}
    cases.append(check("hyperlink_missing", compare_feature(source_link, missing_link, "hyperlinks")["fidelity_classification"], "LOST"))

    passed = all(case["passed"] for case in cases)
    report = {"passed": passed, "case_count": len(cases), "cases": cases, "scope": "Phase 6 hostile comparator regression cases; does not rewrite frozen primary results."}
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "case_count": len(cases), "failed": [case["name"] for case in cases if not case["passed"]]}))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
