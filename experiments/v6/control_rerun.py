from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from common import V4, V6, control_disagreement, load_atomic_records, run_case, sha256, tool_versions


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    out_dir = V6 / "control_rerun_cases"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for record in load_atomic_records():
        case_error = None
        computed = None
        frozen_extracted_path = V4 / "conversions" / "libreoffice" / "extracted" / "atomic" / f"{record['fixture_id']}.json"
        try:
            reopened_parseable = False
            from pypdf import PdfReader
            reopened_parseable = len(PdfReader(str(record["pdf_path"])).pages) > 0
            result = run_case(record["source_path"], record["pdf_path"], record["family"])
            computed = result["classification"]
            frozen_extracted = json.loads(frozen_extracted_path.read_text(encoding="utf-8"))
            frozen_semantics = {
                "destination": frozen_extracted.get("destination", {}),
                "secondary": frozen_extracted.get("secondary", {}),
            }
            # This comparison deliberately excludes the frozen classification and
            # compares recomputed semantic evidence with the archived extraction.
            from common import extracted_semantic_evidence, normalized_hash
            recomputed_extracted_hash = result["extracted_evidence_sha256"]
            frozen_extracted_hash = normalized_hash(extracted_semantic_evidence(frozen_semantics["destination"], frozen_semantics["secondary"]))
            evidence_match = recomputed_extracted_hash == frozen_extracted_hash
            payload = {
                "protocol": "V6 independently rerun unmutated baseline control",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "fixture_id": record["fixture_id"],
                "feature_family": record["family"],
                "role": record["role"],
                "source_path": str(record["source_path"].relative_to(V6.parents[1])).replace("\\", "/"),
                "pdf_path": str(record["pdf_path"].relative_to(V6.parents[1])).replace("\\", "/"),
                "source_sha256": sha256(record["source_path"]),
                "expected_source_sha256": record["source_sha256"],
                "pdf_sha256": sha256(record["pdf_path"]),
                "expected_pdf_sha256": record["pdf_sha256"],
                "reopened_parseable": reopened_parseable,
                "tool_versions": tool_versions(),
                "frozen_classification": record["frozen_classification"],
                "control_classification": computed,
                "classification_disagreement": control_disagreement(computed, record["frozen_classification"]),
                "recomputed_semantic_evidence_sha256": recomputed_extracted_hash,
                "archived_semantic_evidence_sha256": frozen_extracted_hash,
                "semantic_evidence_match": evidence_match,
                "recomputed_trace": result,
                "archived_extraction_path": str(frozen_extracted_path.relative_to(V6.parents[1])).replace("\\", "/"),
            }
        except Exception as exc:  # preserve the failed trace rather than hiding it
            case_error = repr(exc)
            payload = {
                "protocol": "V6 independently rerun unmutated baseline control",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "fixture_id": record["fixture_id"],
                "feature_family": record["family"],
                "role": record["role"],
                "source_path": str(record["source_path"].relative_to(V6.parents[1])).replace("\\", "/"),
                "pdf_path": str(record["pdf_path"].relative_to(V6.parents[1])).replace("\\", "/"),
                "source_sha256": sha256(record["source_path"]),
                "expected_source_sha256": record["source_sha256"],
                "pdf_sha256": sha256(record["pdf_path"]),
                "expected_pdf_sha256": record["pdf_sha256"],
                "tool_versions": tool_versions(),
                "frozen_classification": record["frozen_classification"],
                "control_classification": "EXTRACTION_FAILURE",
                "classification_disagreement": True,
                "semantic_evidence_match": False,
                "error": case_error,
            }
        (out_dir / f"{record['fixture_id']}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append({
            "fixture_id": record["fixture_id"],
            "feature_family": record["family"],
            "frozen_classification": record["frozen_classification"],
            "control_classification": payload["control_classification"],
            "classification_disagreement": payload["classification_disagreement"],
            "semantic_evidence_match": payload.get("semantic_evidence_match", False),
            "extraction_failure": "error" in payload,
            "source_sha256": payload["source_sha256"],
            "pdf_sha256": payload["pdf_sha256"],
            "case_evidence": f"experiments/v6/control_rerun_cases/{record['fixture_id']}.json",
        })
    disagreements = sum(row["classification_disagreement"] for row in rows)
    failures = sum(row["extraction_failure"] for row in rows)
    evidence_differences = sum(not row["semantic_evidence_match"] for row in rows)
    report = {
        "protocol": "V6 Phase A control rerun",
        "status": "COMPLETE" if len(rows) == 65 else "INCOMPLETE",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "controls_evaluated": len(rows),
        "expected_controls": 65,
        "classification_disagreements": disagreements,
        "control_disagreement_rate": disagreements / len(rows) if rows else None,
        "false_positive_controls": disagreements,
        "extraction_failures": failures,
        "semantic_evidence_differences": evidence_differences,
        "interpretation": "A control disagreement is a measured mismatch between a fresh classification and the frozen V4 label; no expected label is copied into the fresh result.",
        "tool_versions": tool_versions(),
        "rows": rows,
    }
    (V6 / "V6_CONTROL_RERUN.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "controls_evaluated", "classification_disagreements", "control_disagreement_rate", "extraction_failures", "semantic_evidence_differences")}, indent=2))
    if report["status"] != "COMPLETE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
