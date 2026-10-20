"""Run conservative semantic-preservation controls on archived PDFs.

Only metadata rewrites and a pypdf round-trip are tested. The contract
projection deliberately excludes object numbering and producer metadata. No
unjustified claim is made that arbitrary visual or tagging rewrites are
semantically equivalent.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "v8" / "benign_transformation_cases"
REPORT = ROOT / "experiments" / "v8" / "V8_BENIGN_TRANSFORMATIONS.json"
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from v8_mutation_ground_truth_audit import pdf_structures, sha256  # noqa: E402
sys.path.insert(0, str(ROOT / "experiments" / "v6"))
from common import run_case  # noqa: E402


def projection(raw: dict) -> dict:
    return {"pages": raw["pages"], "role_counts": raw["role_counts"], "role_nodes": raw["role_nodes"], "figure_alts": raw["figure_alts"], "struct_langs": raw["struct_langs"], "catalog_lang": raw["catalog_lang"], "links": raw["links"]}


def selected_records() -> list[dict]:
    data = json.loads((ROOT / "experiments/v6/V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    chosen = {}
    for row in data["rows"]:
        chosen.setdefault(row["feature_family"], row)
    return list(chosen.values())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []
    for record in selected_records():
        baseline = ROOT / record["baseline_pdf_path"]
        source = ROOT / record["source_path"]
        before = pdf_structures(baseline)
        for kind in ("metadata_rewrite", "pypdf_roundtrip"):
            out = OUT / f"{record['feature_family']}_{kind}.pdf"
            reader = PdfReader(str(baseline), strict=False)
            writer = PdfWriter()
            writer.clone_document_from_reader(reader)
            if kind == "metadata_rewrite":
                info = writer._info.get_object() if writer._info is not None else None
                if info is not None:
                    info[NameObject("/Producer")] = TextStringObject("A11yPreserve benign-control rewrite")
                    info[NameObject("/Creator")] = TextStringObject("A11yPreserve benign-control rewrite")
            with out.open("wb") as handle:
                writer.write(handle)
            after = pdf_structures(out)
            equality = projection(before) == projection(after)
            try:
                base_result = run_case(source, baseline, record["feature_family"])
                out_result = run_case(source, out, record["feature_family"])
                classification_unchanged = base_result.get("classification") == out_result.get("classification")
            except Exception as exc:
                classification_unchanged = None
                error = repr(exc)
            else:
                error = None
            rows.append({
                "feature_family": record["feature_family"], "fixture_id": record["fixture_id"], "kind": kind,
                "baseline_sha256": sha256(baseline), "transformed_sha256": sha256(out),
                "contract_projection_equal": equality, "classification_unchanged": classification_unchanged,
                "error": error, "timestamp_utc": timestamp,
            })
    report = {
        "protocol": "V8 conservative benign semantic transformations",
        "controls": len(rows), "projection_alerts": sum(not r["contract_projection_equal"] for r in rows),
        "classification_regressions": sum(r["classification_unchanged"] is False for r in rows),
        "extraction_errors": sum(r["error"] is not None for r in rows), "rows": rows,
        "interpretation": "The tested transformations are metadata-only rewrites and parser serialization round-trips. Other candidate transformations were not promoted because semantic equivalence could not be defended from available evidence.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("controls", "projection_alerts", "classification_regressions", "extraction_errors")}, indent=2))


if __name__ == "__main__":
    main()
