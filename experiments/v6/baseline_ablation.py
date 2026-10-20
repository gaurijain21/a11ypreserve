from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import ROOT, V4, V6, load_atomic_records, run_case, tool_versions


def _flatten_text(value: Any, key: str = "") -> list[str]:
    if isinstance(value, dict):
        return [piece for child_key, child in value.items() for piece in _flatten_text(child, str(child_key))]
    if isinstance(value, list):
        return [piece for child in value for piece in _flatten_text(child, key)]
    if isinstance(value, str) and key.lower() in {"text", "title", "description", "alt", "visible_text", "expected_text", "expression", "uri"}:
        return [value]
    return []


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def visible_text_equal(result: dict[str, Any]) -> bool:
    # The source extractor's inline-language sequence is the closest available
    # machine-readable visible-text stream. It avoids metadata/evidence fields
    # that are not supposed to appear on the PDF page.
    source_chunks = [
        normalize_text(item.get("text", ""))
        for item in result["source"].get("inline_languages", [])
        if isinstance(item, dict) and item.get("text", "").strip()
    ]
    source_chunks = list(dict.fromkeys(chunk for chunk in source_chunks if chunk))
    destination_text = normalize_text(result["destination"].get("pdf_text", "") or result["secondary"].get("text_preview", ""))
    if not source_chunks:
        return False
    return all(chunk in destination_text for chunk in source_chunks)


def role_presence(family: str, result: dict[str, Any]) -> bool:
    destination = result["destination"]
    markers = result["secondary"].get("serialized_marker_counts", {})
    if family == "headings":
        return bool(destination.get("headings")) or any(markers.get(f"/H{i}", 0) for i in range(1, 7))
    if family == "alt_text":
        return bool(destination.get("figures")) and bool(markers.get("/Alt") or any(item.get("alt") for item in destination.get("figures", []) if isinstance(item, dict)))
    if family == "lists":
        return bool(destination.get("lists")) or bool(markers.get("/L") or markers.get("/LI"))
    if family in {"basic_tables", "complex_tables"}:
        return bool(destination.get("tables")) or bool(markers.get("/Table") or markers.get("/TH") or markers.get("/TD"))
    if family == "document_language":
        return bool(destination.get("language")) or bool(markers.get("/Lang"))
    if family == "inline_language":
        return len(destination.get("inline_languages", [])) > 1 or markers.get("/Lang", 0) > 1
    if family == "decorative_images":
        return bool(markers.get("/Artifact") or markers.get("/Figure") or destination.get("figures"))
    if family == "hyperlinks":
        return bool(destination.get("hyperlinks")) or bool(result["secondary"].get("links")) or bool(markers.get("/URI"))
    if family == "document_metadata":
        return bool(destination.get("title")) or bool(markers.get("/Title"))
    if family == "footnotes":
        return bool(destination.get("footnotes")) or bool(markers.get("/Note"))
    if family == "equations":
        return bool(destination.get("equations")) or bool(markers.get("/Formula"))
    if family == "captions":
        return bool(destination.get("captions")) or bool(markers.get("/Caption"))
    return False


def tag_presence(result: dict[str, Any]) -> bool:
    destination = result["destination"]
    markers = result["secondary"].get("serialized_marker_counts", {})
    return bool(destination.get("tagged") or destination.get("pdf", {}).get("struct_tree_root") or markers.get("/StructTreeRoot"))


def classify_without_secondary(result: dict[str, Any], family: str) -> str:
    import sys

    sys.path.insert(0, str(V4))
    sys.path.insert(0, str(ROOT / "artifact" / "src"))
    from run_frozen_analysis import final_classification  # type: ignore

    empty_secondary = {"serialized_marker_counts": {}, "links": [], "page_image_counts": [], "text_preview": "", "pages": result["secondary"].get("pages")}
    return final_classification(result["raw"], {"document_metadata": "document_title", "basic_tables": "table", "alt_text": "image_alt_text", "decorative_images": "decorative_image", "complex_tables": "complex_table"}.get(family, family), result["destination"], empty_secondary)[0]


def force_binary(result: dict[str, Any], family: str) -> str:
    """Pre-specified no-abstention policy: any observed destination evidence is PRESERVED."""
    return "PRESERVED" if role_presence(family, result) else "LOST"


def observation_bundle(result: dict[str, Any], family: str) -> dict[str, Any]:
    full = result["classification"]
    no_secondary = classify_without_secondary(result, family)
    return {
        "tag_presence": "TAGGED" if tag_presence(result) else "UNTAGGED",
        "visible_text_equality": "EQUAL" if visible_text_equal(result) else "DIFFERENT",
        "destination_only_evidence": "PRESENT" if role_presence(family, result) else "ABSENT",
        "without_secondary_evidence": no_secondary,
        "without_abstention": force_binary(result, family),
        "full_a11ypreserve": full,
        "full_abstention": full in {"UNRESOLVED_EQUIVALENCE", "MEASUREMENT_ERROR"},
    }


def primary_records() -> list[dict[str, Any]]:
    records = []
    for pipeline in ("libreoffice", "google"):
        analysis_path = V4 / "conversions" / pipeline / "analysis" / f"V4_{'LIBREOFFICE' if pipeline == 'libreoffice' else 'GOOGLE'}_ANALYSIS.json"
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        records.extend({"pipeline": pipeline, **row} for row in analysis["records"] if row.get("corpus") == "atomic")
    return records


def summarize_primary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for pipeline in sorted({row["pipeline"] for row in rows}):
        subset = [row for row in rows if row["pipeline"] == pipeline]
        methods = ["tag_presence", "visible_text_equality", "destination_only_evidence", "without_secondary_evidence", "without_abstention", "full_a11ypreserve"]
        summary[pipeline] = {
            "cases": len(subset),
            "classification_counts": dict(Counter(row["observations"]["full_a11ypreserve"] for row in subset)),
            "abstentions_full": sum(row["observations"]["full_abstention"] for row in subset),
            "methods": {
                method: {
                    "distinct_decisions": dict(Counter(row["observations"][method] for row in subset)),
                    "unsupported_or_abstention": sum(row["observations"][method] in {"UNRESOLVED_EQUIVALENCE", "MEASUREMENT_ERROR"} for row in subset),
                }
                for method in methods
            },
        }
    return summary


def mutation_evaluation() -> dict[str, Any]:
    lookup = {record["fixture_id"]: record for record in load_atomic_records()}
    rows = []
    mutation_dir = V6 / "mutation_cases"
    for case_path in sorted(mutation_dir.glob("*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        if not (case["mutation_applied"] and case["valid_pdf"]):
            continue
        record = lookup[case["fixture_id"]]
        before = run_case(record["source_path"], record["pdf_path"], record["family"])
        after = run_case(record["source_path"], ROOT / case["mutated_pdf_path"], record["family"])
        before_obs = observation_bundle(before, record["family"])
        after_obs = observation_bundle(after, record["family"])
        rows.append({
            "fixture_id": case["fixture_id"],
            "feature_family": record["family"],
            "known_applied_valid_fault": True,
            "baseline": before_obs,
            "mutated": after_obs,
            "detected_by": {method: before_obs[method] != after_obs[method] for method in before_obs if method != "full_abstention"},
        })
    methods = ["tag_presence", "visible_text_equality", "destination_only_evidence", "without_secondary_evidence", "without_abstention", "full_a11ypreserve"]
    summary = {
        method: {
            "faults_evaluated": len(rows),
            "detected_faults": sum(row["detected_by"][method] for row in rows),
            "detection_rate": sum(row["detected_by"][method] for row in rows) / len(rows) if rows else None,
        }
        for method in methods
    }
    return {"fault_reference": "operator-applied and parseable mutation; this is a known-fault oracle, not a human correctness label", "faults_evaluated": len(rows), "summary": summary, "rows": rows}


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    rows = []
    for record in primary_records():
        source_path = ROOT / record["source_path"]
        pdf_path = ROOT / record["output_path"]
        result = run_case(source_path, pdf_path, record["feature_family"])
        rows.append({
            "pipeline": record["pipeline"],
            "fixture_id": record["fixture_id"],
            "feature_family": record["feature_family"],
            "output_path": record["output_path"],
            "output_sha256": record["output_sha256"],
            "observations": observation_bundle(result, record["feature_family"]),
            "raw_fidelity": result["raw"].get("fidelity_classification"),
        })
    fault_eval = mutation_evaluation()
    report = {
        "protocol": "V6 executable baseline and ablation comparison",
        "status": "COMPLETE" if len(rows) == 130 else "INCOMPLETE",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "primary_cases": len(rows),
        "reference_label_protocol": {
            "primary": "No independent adjudicated labels were available. Primary agreement/error rates are therefore not claimed; rows retain observed outputs and abstentions.",
            "mutation_faults": "Applied-and-parseable destination mutations are known injected faults. Detection rates are supported fault-sensitivity measures for this operator set.",
            "no_abstention_policy": "PRESERVED when the destination-only role/evidence predicate is present, otherwise LOST; this forced binary policy is reported as a sensitivity analysis, not ground truth.",
        },
        "baseline_definitions": {
            "tag_presence": "destination tagged flag or StructTreeRoot marker; no source contract value",
            "visible_text_equality": "normalized source text is found in extracted destination text; no semantic structure or association check",
            "destination_only_evidence": "feature-specific destination role/marker presence without source expectation",
            "without_secondary_evidence": "frozen comparator with independent PyMuPDF/object-marker secondary evidence suppressed",
            "without_abstention": "forced binary role-presence policy with unresolved/measurement outcomes removed",
            "full_a11ypreserve": "source-grounded frozen comparator, multi-evidence classification, and explicit abstention",
        },
        "primary_summary": summarize_primary(rows),
        "mutation_fault_sensitivity": fault_eval,
        "rows": rows,
        "tool_versions": tool_versions(),
    }
    (V6 / "V6_BASELINE_ABLATION.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (V6 / "V6_MUTATION_BASELINE_EVALUATION.json").write_text(json.dumps(fault_eval, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "primary_cases": report["primary_cases"], "mutation_faults": fault_eval["faults_evaluated"], "fault_sensitivity": fault_eval["summary"]}, indent=2))
    if report["status"] != "COMPLETE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
