"""Apply the V3 classification precedence to label-blinded evidence facts.

The facts table is deliberately separate from the frozen V2 result labels. It
is an audit runner, not a replacement for the V2 analysis implementation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "contracts" / "v3" / "classification_rules.json"
OUT = ROOT / "v3" / "core_reclassification"

CASES = [
    ("F01_HEADINGS", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F01_HEADINGS", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "contract_has_multiple_components": True, "required_component_present": True, "required_component_directly_differs_or_absent": True, "missing_component_is_measured": True}),
    ("F02_ALT_TEXT", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "concept_present": True, "author_relevant_value_differs": True}),
    ("F02_ALT_TEXT", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F03_LISTS", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F03_LISTS", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
    ("F04_TABLE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F04_TABLE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F05_DOCUMENT_LANGUAGE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F05_DOCUMENT_LANGUAGE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "concept_present": True, "author_relevant_value_differs": True}),
    ("F06_INLINE_LANGUAGE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F06_INLINE_LANGUAGE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "required_representation_absent": True, "independent_absence_corroborated": True}),
    ("F07_DECORATIVE_IMAGE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "contract_has_multiple_components": True, "required_component_present": True, "required_component_directly_differs_or_absent": True, "missing_component_is_measured": True}),
    ("F07_DECORATIVE_IMAGE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "contract_has_multiple_components": True, "required_component_present": True, "required_component_directly_differs_or_absent": True, "missing_component_is_measured": True}),
    ("F08_LINKS", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
    ("F08_LINKS", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
    ("F09_DOCUMENT_TITLE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F09_DOCUMENT_TITLE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "concept_present": True, "author_relevant_value_differs": True}),
    ("F10_COMPLEX_TABLE", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F10_COMPLEX_TABLE", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
    ("F11_FOOTNOTES", "LibreOffice", {"measurement_valid": False, "source_verified": True, "insufficient_evidence": True}),
    ("F11_FOOTNOTES", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "required_representation_absent": True, "independent_absence_corroborated": True}),
    ("F12_EQUATION", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F12_EQUATION", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
    ("F14_CAPTIONS", "LibreOffice", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "all_required_components_equivalent": True, "evidence_sufficient": True}),
    ("F14_CAPTIONS", "Google Docs", {"measurement_valid": True, "source_verified": True, "destination_representable": True, "evidence_sufficient": False}),
]

def classify(facts: dict) -> str:
    if facts.get("measurement_valid") is False and facts.get("insufficient_evidence") is True:
        return "MEASUREMENT_ERROR"
    if all(facts.get(k) is True for k in ("source_verified", "destination_representable", "required_representation_absent", "independent_absence_corroborated")):
        return "CONFIRMED_LOST"
    if all(facts.get(k) is True for k in ("contract_has_multiple_components", "required_component_present", "required_component_directly_differs_or_absent", "missing_component_is_measured")):
        return "OBSERVED_PARTIAL"
    if facts.get("concept_present") is True and facts.get("author_relevant_value_differs") is True:
        return "ALTERED"
    if facts.get("all_required_components_equivalent") is True and facts.get("evidence_sufficient") is True:
        return "VERIFIED_PRESERVED"
    if facts.get("measurement_valid") is True and facts.get("evidence_sufficient") is False:
        return "UNRESOLVED_EQUIVALENCE"
    raise ValueError(f"No rule applies: {facts}")

def main() -> None:
    RULES.parent.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [{"fixture": fixture, "pipeline": pipeline, "evidence_facts": facts, "v3_decision": classify(facts)} for fixture, pipeline, facts in CASES]
    payload = {"protocol": "V3 blind-at-label-level reclassification", "historical_labels_used_as_input": False, "rows": rows}
    (OUT / "BLINDED_EVIDENCE_RECLASSIFICATION.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    counts = {}
    for row in rows:
        counts[row["v3_decision"]] = counts.get(row["v3_decision"], 0) + 1
    (OUT / "V3_RECLASSIFICATION_SUMMARY.json").write_text(json.dumps({"counts": counts, "case_count": len(rows)}, indent=2), encoding="utf-8")
    print(json.dumps({"case_count": len(rows), "counts": counts}, indent=2))

if __name__ == "__main__":
    main()

