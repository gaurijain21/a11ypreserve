from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
OUT = V4 / "conversions" / "google"
EXTRACTED = OUT / "extracted"
ANALYSIS = OUT / "analysis"
sys.path.insert(0, str(V4))
from run_frozen_analysis import FEATURES, compare_feature_v4, docx_extract, final_classification, pdf_extract, secondary, summarize  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def feature_row(source_path: Path, output_path: Path, fixture_id: str, family: str, role: str, corpus: str, expected_source_hash: str) -> dict[str, Any]:
    source = docx_extract(source_path)
    destination = pdf_extract(output_path)
    second = secondary(output_path)
    feature = FEATURES[family]
    raw = compare_feature_v4(source, destination, feature)
    classification, classification_basis = final_classification(raw, feature, destination, second)
    out_path = EXTRACTED / corpus
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / f"{fixture_id}.json").write_text(json.dumps({"source": source, "destination": destination, "secondary": second}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "corpus": corpus, "fixture_id": fixture_id, "feature_family": family, "comparator_feature": feature, "role": role,
        "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha256(source_path), "expected_source_sha256": expected_source_hash,
        "output_path": str(output_path.relative_to(ROOT)).replace("\\", "/"), "output_sha256": sha256(output_path),
        "converter": "Google Docs", "raw_fidelity": raw.get("fidelity_classification"), "destination_accessibility": raw.get("destination_accessibility"),
        "classification": classification, "classification_basis": classification_basis, "notes": raw.get("notes", ""),
        "evidence": {"primary": raw.get("evidence", []), "secondary": second},
    }


def main() -> None:
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    atomic_manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    rows = []
    for entry in atomic_manifest["records"]:
        fixture = entry["variant_id"]
        record = next(row for row in manifest["records"] if row["fixture_id"] == fixture and row["corpus"] == "atomic")
        source_path, output_path = ROOT / entry["fixture"], ROOT / record["output_path"]
        if sha256(source_path) != entry["source_sha256"]:
            raise ValueError(f"source hash changed: {fixture}")
        rows.append(feature_row(source_path, output_path, fixture, entry["feature_family"], entry["role"], "atomic", entry["source_sha256"]))

    realistic_rows = []
    realistic = json.loads((V4 / "realistic" / "REALISTIC_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
    for entry in realistic["records"]:
        doc_id = entry["document_id"]
        record = next(row for row in manifest["records"] if row["fixture_id"] == doc_id and row["corpus"] == "realistic")
        source_path, output_path = ROOT / entry["path"], ROOT / record["output_path"]
        source = docx_extract(source_path)
        destination = pdf_extract(output_path)
        second = secondary(output_path)
        for contract_index, contract in enumerate(entry["contracts"], start=1):
            family = contract["property"]
            if family not in FEATURES:
                continue
            raw = compare_feature_v4(source, destination, FEATURES[family])
            classification, basis = final_classification(raw, FEATURES[family], destination, second)
            realistic_rows.append({"corpus": "realistic", "document_id": doc_id, "contract_index": contract_index, "feature_family": family, "contract": contract, "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha256(source_path), "output_path": str(output_path.relative_to(ROOT)).replace("\\", "/"), "output_sha256": sha256(output_path), "raw_fidelity": raw.get("fidelity_classification"), "classification": classification, "classification_basis": basis, "notes": raw.get("notes", ""), "evidence": {"primary": raw.get("evidence", []), "secondary": second}})

    ANALYSIS.mkdir(parents=True, exist_ok=True)
    payload = {"analysis_version": "v4-frozen-analysis-runner-1", "protocol": "experiments/v4/V4_PROTOCOL.md", "converter": "Google Docs", "manifest": "experiments/v4/conversions/google/manifest.json", "method": "frozen source extractor + frozen V4 comparator boundary + independent PyMuPDF secondary evidence", "records": rows, "summary": summarize(rows), "holdout": summarize([row for row in rows if row["role"] == "holdout"]), "development": summarize([row for row in rows if row["role"] != "holdout"]), "realistic": {"records": realistic_rows, "summary": summarize(realistic_rows)}}
    (ANALYSIS / "V4_GOOGLE_ANALYSIS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"atomic": payload["summary"], "development": payload["development"], "holdout": payload["holdout"], "realistic": payload["realistic"]["summary"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
