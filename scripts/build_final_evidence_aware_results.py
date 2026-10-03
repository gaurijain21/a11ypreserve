from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "full_experiment" / "EVIDENCE_STATUS_FREEZE_V2.json"


def final_result(row: dict) -> str:
    outcome = row["outcome"]
    status = row["evidence_status"]
    if outcome == "PRESERVED" and status == "VERIFIED_EQUIVALENCE":
        return "VERIFIED_PRESERVED"
    if outcome == "PARTIALLY_PRESERVED" and status == "OBSERVED_PARTIAL":
        return "OBSERVED_PARTIAL"
    if outcome == "PARTIALLY_PRESERVED" and status == "UNRESOLVED_EQUIVALENCE":
        return "UNRESOLVED_EQUIVALENCE"
    if outcome == "ALTERED" and status == "OBSERVED_DIFFERENCE":
        return "ALTERED"
    if outcome == "LOST" and status == "INDEPENDENTLY_CONFIRMED_ABSENCE":
        return "CONFIRMED_LOST"
    if outcome == "MEASUREMENT_ERROR" and status == "MEASUREMENT_FAILURE":
        return "MEASUREMENT_ERROR"
    raise ValueError(f"Unsupported evidence-aware mapping: {outcome}/{status}")


def artifact_for(row: dict, final: str) -> str:
    fixture = row["fixture"]
    converter = row["converter"].lower().replace(" ", "_")
    if final == "UNRESOLVED_EQUIVALENCE" or final == "OBSERVED_PARTIAL":
        return "final_strengthening/PARTIAL_CASE_REAUDIT.md"
    if final == "CONFIRMED_LOST":
        short_fixture = "F06" if fixture.startswith("F06_") else "F11" if fixture.startswith("F11_") else fixture
        return f"final_strengthening/loss/{short_fixture}_GOOGLE_LOSS_CERTIFICATE.md"
    if final == "MEASUREMENT_ERROR":
        return "final_strengthening/PDF_PARSER_TRIANGULATION.md"
    if final == "VERIFIED_PRESERVED":
        return "final_strengthening/INDEPENDENT_SOURCE_ORACLE.md"
    return "final_strengthening/EVIDENCE_STATUS_FREEZE_V2.json"


def main() -> None:
    freeze = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = []
    for row in freeze["records"]:
        final = final_result(row)
        records.append({
            "fixture": row["fixture"],
            "pipeline": row["converter"],
            "historical_v1_outcome": row["outcome"],
            "final_evidence_aware_result": final,
            "evidence_status": row["evidence_status"],
            "supporting_artifact": artifact_for(row, final),
            "source_sha256": row["source_sha256"],
            "destination_sha256": row["destination_sha256"],
            "evidence_path": row["evidence_path"],
        })
    counts = Counter(row["final_evidence_aware_result"] for row in records)
    if len(records) != 26:
        raise SystemExit(f"Expected 26 records, found {len(records)}")
    result = {"result_model": "FINAL_EVIDENCE_AWARE_V2", "primary_v1_unchanged": True, "record_count": len(records), "counts": dict(sorted(counts.items())), "records": records}
    out_json = ROOT / "results" / "full_experiment" / "FINAL_EVIDENCE_AWARE_RESULTS.json"
    out_md = ROOT / "results" / "FINAL_EVIDENCE_AWARE_RESULTS.md"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Final evidence-aware results", "", "This V2 interpretation is derived programmatically from `results/full_experiment/EVIDENCE_STATUS_FREEZE_V2.json`. It does not modify the historical V1 freeze, fixtures, PDFs, manifests, hashes, or denominator.", "", f"- Cases: {len(records)}", "- Primary unit: one fixture–pipeline pair", "", "| Fixture | Pipeline | Historical V1 outcome | Final evidence-aware result | Evidence status | Supporting artifact |", "|---|---|---|---|---|---|"]
    for row in records:
        lines.append(f"| {row['fixture']} | {row['pipeline']} | {row['historical_v1_outcome']} | {row['final_evidence_aware_result']} | {row['evidence_status']} | `{row['supporting_artifact']}` |")
    lines.extend(["", "## Final distribution", "", "| Final result | Count |", "|---|---:|"])
    for key, value in sorted(counts.items()):
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "The V1 primary classifications remain archived for provenance. The V2 labels make uncertainty explicit: only directly supported differences are `OBSERVED_PARTIAL`; unresolved cross-format equivalence is reported separately."])
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(records), "counts": dict(sorted(counts.items()))}, indent=2))


if __name__ == "__main__":
    main()
