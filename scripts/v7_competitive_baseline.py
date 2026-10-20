"""Evaluate a source-aware, independently implemented baseline on known faults."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from v7_independent_oracle_audit import destination_projection, source_projection

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
REPORT = ROOT / "experiments" / "v7" / "V7_COMPETITIVE_BASELINE.json"


def status(family: str, source: dict, dest: dict) -> str:
    roles = dest["role_counts"]
    if family == "headings":
        return "SUPPORTED" if roles.get("/H1", 0) + roles.get("/H2", 0) + roles.get("/H3", 0) else "UNSUPPORTED"
    if family == "alt_text":
        wanted = {item.get("alt") for item in source.get("figures", []) if item.get("alt")}
        return "SUPPORTED" if wanted and wanted.issubset(set(dest["alt_values"])) else "UNSUPPORTED"
    if family == "decorative_images":
        return "SUPPORTED" if roles.get("/Artifact", 0) else "UNSUPPORTED"
    if family == "hyperlinks":
        wanted = {item.get("target") for item in source.get("hyperlinks", []) if item.get("target")}
        return "SUPPORTED" if wanted and wanted.issubset(set(dest["annotation_uris"])) else "UNSUPPORTED"
    if family == "document_metadata":
        wanted = source.get("metadata", {}).get("title")
        return "SUPPORTED" if wanted and dest.get("metadata_title") == wanted else "UNSUPPORTED"
    required_roles = {
        "lists": "/L", "basic_tables": "/Table", "complex_tables": "/Table",
        "document_language": None, "inline_language": None, "footnotes": "/Note",
        "equations": "/Formula", "captions": "/Caption",
    }
    if family == "document_language":
        return "SUPPORTED" if dest.get("catalog_lang") or dest.get("lang_values") else "UNSUPPORTED"
    if family == "inline_language":
        return "SUPPORTED" if dest.get("lang_values") else "UNSUPPORTED"
    role = required_roles.get(family)
    return "SUPPORTED" if role and roles.get(role, 0) else "UNSUPPORTED"


def main() -> None:
    mutation = json.loads((V6 / "V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    rows = []
    for item in mutation["rows"]:
        if not (item.get("mutation_applied") and item.get("valid_pdf")):
            continue
        source = ROOT / item["source_path"]
        baseline_pdf = ROOT / item["baseline_pdf_path"]
        mutant_pdf = ROOT / item["mutated_pdf_path"]
        source_obs = source_projection(source, item["feature_family"])
        before = status(item["feature_family"], source_obs, destination_projection(baseline_pdf))
        after = status(item["feature_family"], source_obs, destination_projection(mutant_pdf))
        rows.append({
            "fixture_id": item["fixture_id"], "family": item["feature_family"],
            "operator": item["mutation_operator"], "baseline_status": before,
            "mutant_status": after, "fault_detected": before != after,
        })
    report = {
        "method": "source-aware structural baseline",
        "definition": "Fresh OOXML contract projection paired with raw PDF role, metadata, URI, and text evidence; no frozen comparator import.",
        "known_faults_evaluated": len(rows),
        "faults_detected": sum(row["fault_detected"] for row in rows),
        "family_detection": {},
        "decision_counts": dict(Counter(f"{row['baseline_status']}->{row['mutant_status']}" for row in rows)),
        "rows": rows,
        "interpretation": "This is a competent but deliberately bounded source-aware baseline. It is not independent ground truth and does not claim full semantic equivalence.",
    }
    for family in sorted({row["family"] for row in rows}):
        subset = [row for row in rows if row["family"] == family]
        report["family_detection"][family] = {"evaluated": len(subset), "detected": sum(row["fault_detected"] for row in subset)}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("known_faults_evaluated", "faults_detected")}, indent=2))


if __name__ == "__main__":
    main()
