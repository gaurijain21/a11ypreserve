from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "integrated_study"
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import extract  # noqa: E402
from phase4_compare import compare_all  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def final_result(raw: dict, triangulated_status: str | None = None) -> tuple[str, str]:
    fidelity = raw.get("fidelity_classification")
    notes = raw.get("notes", "")
    if fidelity in {"PRESERVED", "EXACT_PRESERVATION", "SEMANTICALLY_EQUIVALENT"}:
        return "VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE"
    if fidelity in {"ALTERED", "MUTATED"}:
        return "ALTERED", "OBSERVED_DIFFERENCE"
    if fidelity == "MEASUREMENT_ERROR":
        return "MEASUREMENT_ERROR", "MEASUREMENT_FAILURE"
    if fidelity == "LOST":
        if triangulated_status == "INDEPENDENTLY_CONFIRMED_ABSENCE":
            return "CONFIRMED_LOST", triangulated_status
        return "UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE"
    if fidelity in {"PARTIALLY_PRESERVED", "PARTIAL_PRESERVATION"}:
        lowered = notes.lower()
        direct = any(token in lowered for token in ("level/order sequence differs", "item count or nesting differs", "override is absent", "figure count or decorative/alternative-text state differs"))
        if direct:
            return "OBSERVED_PARTIAL", "OBSERVED_PARTIAL"
        return "UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE"
    return "MEASUREMENT_ERROR", "MEASUREMENT_FAILURE"


def main() -> None:
    manifest = json.loads((OUT / "INTEGRATED_CONTRACTS.json").read_text(encoding="utf-8"))
    source_oracle = json.loads((OUT / "INTEGRATED_SOURCE_ORACLE.json").read_text(encoding="utf-8"))
    triangulation = json.loads((OUT / "PARSER_TRIANGULATION.json").read_text(encoding="utf-8"))
    oracle_by_instance = {row["instance"]: row for row in source_oracle["records"]}
    triangulation_by_key = {(row["document"], row["feature"]): row["status"] for row in triangulation["records"]}
    records = []
    for document in manifest["documents"]:
        source_path = ROOT / document["source_docx"]
        source = extract(source_path)
        for pipeline, directory in (("LibreOffice", "libreoffice"), ("Google Docs", "google_docs")):
            pdf_path = OUT / "outputs" / directory / f"{document['document_id']}__{pipeline.upper().replace(' ', '_')}.pdf"
            destination = extract(pdf_path)
            by_feature = {}
            for contract in document["contracts"]:
                if contract["feature"] not in by_feature:
                    comparison = compare_all(source, destination, contract["feature"])[0]
                    by_feature[contract["feature"]] = comparison
                raw = by_feature[contract["feature"]]
                triangulated_status = triangulation_by_key.get((document["document_id"], contract["feature"]))
                result, evidence_status = final_result(raw, triangulated_status)
                oracle_row = oracle_by_instance[contract["instance"]]
                records.append({
                    "document": document["document_id"],
                    "property_instance": contract["instance"],
                    "feature": contract["feature"],
                    "pipeline": pipeline,
                    "historical_comparator_result": raw.get("fidelity_classification"),
                    "result": result,
                    "evidence_status": evidence_status,
                    "source_oracle": "PASS" if oracle_row["passed"] else "FAIL",
                    "triangulation_status": triangulated_status,
                    "source_sha256": sha256(source_path),
                    "destination_sha256": sha256(pdf_path),
                    "destination_evidence": raw.get("evidence", []),
                    "observation": raw.get("notes", ""),
                    "source_path": str(source_path.relative_to(ROOT)),
                    "destination_path": str(pdf_path.relative_to(ROOT)),
                })
    result = {"study": "secondary_integrated_external_validity_sanity_check", "documents": 3, "primary_denominator_excluded": True, "property_instances": len({r["property_instance"] for r in records}), "records": records}
    (OUT / "INTEGRATED_RESULTS.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Integrated sanity-check results", "", "This is a secondary evaluation of three multi-feature documents. It uses only existing feature contracts and the same two named pipelines. Its property instances are not merged into the primary 13-fixture × 2-pipeline denominator.", "", f"- Documents: {result['documents']}", f"- Property instances: {result['property_instances']}", f"- Pipeline cases: {len(records)}", f"- Independent integrated source contracts: {source_oracle['passed']}/{source_oracle['contract_count']}", "", "| Document | Property instance | Pipeline | Result | Evidence status | Observation |", "|---|---|---|---|---|---|"]
    for row in records:
        lines.append(f"| {row['document']} | {row['property_instance']} | {row['pipeline']} | {row['result']} | {row['evidence_status']} | {row['observation']} |")
    lines.extend(["", "## Interpretation", "", "The protocol remained executable when multiple existing accessibility properties coexisted in realistic documents. The secondary check is a usability demonstration of the conformance procedure, not a prevalence estimate, converter ranking, or independent generalization study. Any unresolved rows retain that status rather than being promoted to loss."])
    (OUT / "INTEGRATED_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    counts = {}
    for row in records:
        counts[row["result"]] = counts.get(row["result"], 0) + 1
    print(json.dumps({"documents": 3, "property_instances": result["property_instances"], "pipeline_cases": len(records), "counts": dict(sorted(counts.items()))}, indent=2))


if __name__ == "__main__":
    main()
