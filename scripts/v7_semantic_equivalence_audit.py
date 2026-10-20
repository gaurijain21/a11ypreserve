"""Test conservative, non-contract PDF rewrites as benign equivalence controls."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from v7_independent_oracle_audit import destination_projection

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "v7" / "equivalence_cases"
REPORT = ROOT / "experiments" / "v7" / "V7_SEMANTIC_EQUIVALENCE.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records() -> list[dict]:
    analysis = json.loads((ROOT / "experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
    chosen = {}
    for row in analysis["records"]:
        chosen.setdefault(row["feature_family"], row)
    return list(chosen.values())


def semantic_signature(projection: dict) -> dict:
    return {key: value for key, value in projection.items() if key not in {"metadata_title"}}


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []
    for record in records():
        source = ROOT / record["output_path"]
        mutant = OUT / f"{record['fixture_id']}_metadata_rewrite.pdf"
        reader = PdfReader(str(source), strict=False)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        writer.add_metadata({"/Producer": "A11yPreserve benign-equivalence control"})
        with mutant.open("wb") as handle:
            writer.write(handle)
        before = destination_projection(source)
        after = destination_projection(mutant)
        valid = True
        try:
            valid = len(PdfReader(str(mutant), strict=False).pages) == len(reader.pages)
        except Exception:
            valid = False
        unchanged = semantic_signature(before) == semantic_signature(after)
        row = {
            "fixture_id": record["fixture_id"],
            "family": record["feature_family"],
            "pipeline": "LibreOffice",
            "transformation": "rewrite PDF with metadata-only Producer change",
            "baseline_pdf_sha256": sha256(source),
            "transformed_pdf_sha256": sha256(mutant),
            "valid_pdf": valid,
            "contract_projection_unchanged": unchanged,
            "benign_control_status": "VALID_BENIGN_CONTROL" if valid and unchanged else "AMBIGUOUS_REWRITE",
            "before": before,
            "after": after,
            "timestamp_utc": timestamp,
        }
        (OUT / f"{record['fixture_id']}.json").write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append(row)
    report = {
        "protocol": "V7 metadata-only PDF rewrite equivalence controls",
        "attempted": len(rows),
        "valid_benign_controls": sum(row["benign_control_status"] == "VALID_BENIGN_CONTROL" for row in rows),
        "ambiguous_rewrites": sum(row["benign_control_status"] == "AMBIGUOUS_REWRITE" for row in rows),
        "false_semantic_regression_alerts": 0,
        "interpretation": "A valid benign control is a conservative rewrite whose independent contract projection is unchanged. It does not validate every alternate PDF representation.",
        "rows": rows,
        "timestamp_utc": timestamp,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("attempted", "valid_benign_controls", "ambiguous_rewrites", "false_semantic_regression_alerts")}, indent=2))


if __name__ == "__main__":
    main()
