from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_frozen_analysis import FEATURES, compare_feature_v4, docx_extract, final_classification, pdf_extract, secondary


ROOT = Path(__file__).resolve().parents[3]
V4 = ROOT / "experiments" / "v4"
OUT = V4 / "conversions" / "word" / "outputs" / "repeatability"
SELECTED = {
    "F04_D": "basic_tables",
    "F06_D": "complex_tables",
    "F08_D": "hyperlinks",
    "F11_D": "equations",
    "F12_D": "footnotes",
    "F13_D": "captions",
}


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def normalize_extraction(value: object, key: str | None = None) -> object:
    """Remove run-specific paths, object-debug strings, and export timestamps."""
    if key in {"object", "source", "CreationDate", "ModDate"}:
        return None
    if isinstance(value, dict):
        return {k: normalize_extraction(v, k) for k, v in value.items() if k not in {"object", "source", "CreationDate", "ModDate"}}
    if isinstance(value, list):
        return [normalize_extraction(v) for v in value]
    return value


rows = []
for fixture_id, family in SELECTED.items():
    source_path = ROOT / "experiments" / "v4" / "fixtures" / f"{fixture_id}.docx"
    source = docx_extract(source_path)
    run_rows = []
    for run in range(1, 4):
        pdf_path = OUT / f"{fixture_id}__WORD_DESKTOP__run{run}.pdf"
        destination = pdf_extract(pdf_path)
        evidence = secondary(pdf_path)
        comparator_feature = FEATURES[family]
        raw = compare_feature_v4(source, destination, comparator_feature)
        classification, basis = final_classification(raw, comparator_feature, destination, evidence)
        run_rows.append(
            {
                "run": run,
                "output_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
                "output_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                "destination_extraction_sha256": canonical_hash(normalize_extraction(destination)),
                "secondary_normalized_sha256": canonical_hash({k: v for k, v in evidence.items() if k != "pdf_sha256"}),
                "classification": classification,
                "classification_basis": basis,
            }
        )
    rows.append(
        {
            "fixture_id": fixture_id,
            "feature_family": family,
            "runs": run_rows,
            "byte_identity": len({x["output_sha256"] for x in run_rows}) == 1,
            "destination_extraction_identity": len({x["destination_extraction_sha256"] for x in run_rows}) == 1,
            "secondary_normalized_identity": len({x["secondary_normalized_sha256"] for x in run_rows}) == 1,
            "classification_identity": len({x["classification"] for x in run_rows}) == 1,
        }
    )

payload = {
    "analysis_version": "v4-word-repeatability-frozen-comparator-1",
    "method": "frozen destination extractor + frozen V4 comparator; secondary evidence normalized only by excluding output byte hash",
    "records": rows,
    "summary": {
        "fixtures": len(rows),
        "runs": sum(len(x["runs"]) for x in rows),
        "byte_identity_fixtures": sum(x["byte_identity"] for x in rows),
        "destination_extraction_identity_fixtures": sum(x["destination_extraction_identity"] for x in rows),
        "secondary_normalized_identity_fixtures": sum(x["secondary_normalized_identity"] for x in rows),
        "classification_identity_fixtures": sum(x["classification_identity"] for x in rows),
    },
}
path = V4 / "conversions" / "word" / "analysis" / "V4_WORD_REPEATABILITY_ANALYSIS.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(payload["summary"], indent=2))
