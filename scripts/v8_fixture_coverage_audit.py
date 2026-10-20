"""Audit family/variant/branch coverage without changing frozen evidence."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "experiments" / "v8" / "V8_FIXTURE_COVERAGE.json"


def main() -> None:
    mutation = json.loads((ROOT / "experiments/v6/V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    family_rows = defaultdict(list)
    for row in mutation["rows"]:
        family_rows[row["feature_family"]].append(row)
    families = {}
    for family, rows in sorted(family_rows.items()):
        families[family] = {
            "variants": sorted(r["fixture_id"][-1] for r in rows),
            "fixture_count": len(rows),
            "mutation_attempts": len(rows),
            "applied": sum(bool(r["mutation_applied"]) for r in rows),
            "valid_applied": sum(bool(r["mutation_applied"] and r.get("valid_pdf")) for r in rows),
            "classification_detections": sum(bool(r.get("classification_changed")) for r in rows),
            "evidence_alerts": sum(bool(r.get("evidence_drift_alert")) for r in rows),
            "outcome_statuses": dict(Counter(r["outcome_status"] for r in rows)),
        }
    records = []
    for path in (ROOT / "experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json", ROOT / "experiments/v4/conversions/google/analysis/V4_GOOGLE_ANALYSIS.json"):
        records.extend(json.loads(path.read_text(encoding="utf-8"))["records"])
    primary_by_family_pipeline = Counter((r["feature_family"], r["converter"]) for r in records)
    report = {
        "protocol": "V8 fixture coverage audit",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "families": families,
        "family_count": len(families), "atomic_fixture_count": sum(x["fixture_count"] for x in families.values()),
        "primary_observations": len(records), "primary_family_pipeline_counts": {f"{k[0]}::{k[1]}": v for k, v in sorted(primary_by_family_pipeline.items())},
        "interpretation": "The five variants are correlated within each family and are not independent draws. This is a design-coverage audit, not a population-representativeness claim.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("family_count", "atomic_fixture_count", "primary_observations")}, indent=2))


if __name__ == "__main__":
    main()
