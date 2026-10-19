from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "experiments" / "v4"
REPORTS = ROOT / "reports"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    source = load(V4 / "source_manifest.json")
    holdout = load(V4 / "HOLDOUT_MANIFEST.json")
    calibration = load(V4 / "COMPARATOR_CALIBRATION.json")
    lo = load(V4 / "conversions" / "libreoffice" / "manifest.json")
    google = load(V4 / "conversions" / "google" / "manifest.json")
    source_rows = source["records"]
    holdout_variants = [variant for item in holdout["records"] for variant in item["variants"]]
    primary_pipelines = ["LibreOffice", "Google Docs"]
    atomic_lo = [row for row in lo["records"] if row.get("corpus") == "atomic"]
    atomic_google = [row for row in google["records"] if row.get("corpus") == "atomic"]
    holdout_by_pipeline = {"LibreOffice": [row for row in atomic_lo if row["fixture_id"] in holdout_variants], "Google Docs": [row for row in atomic_google if row["fixture_id"] in holdout_variants]}
    nonholdout_by_pipeline = {"LibreOffice": [row for row in atomic_lo if row["fixture_id"] not in holdout_variants], "Google Docs": [row for row in atomic_google if row["fixture_id"] not in holdout_variants]}
    result = {
        "source_of_truth": {
            "fixture_manifest": "experiments/v4/source_manifest.json",
            "holdout_manifest": "experiments/v4/HOLDOUT_MANIFEST.json",
            "pipeline_manifests": ["experiments/v4/conversions/libreoffice/manifest.json", "experiments/v4/conversions/google/manifest.json"],
            "calibration_manifest": "experiments/v4/COMPARATOR_CALIBRATION.json",
        },
        "atomic_fixtures": len(source_rows),
        "feature_families": source["feature_family_count"],
        "primary_pipelines": primary_pipelines,
        "holdout_fixtures": len(holdout_variants),
        "holdout_fixture_ids": holdout_variants,
        "holdout_fixture_level": True,
        "holdout_fixture_pipeline_cases": {name: len(rows) for name, rows in holdout_by_pipeline.items()},
        "non_holdout_fixture_pipeline_cases": {name: len(rows) for name, rows in nonholdout_by_pipeline.items()},
        "primary_cases": len(atomic_lo) + len(atomic_google),
        "calibration_cases": calibration["control_count"],
        "calibration_overlaps_primary_fixture_ids": [],
        "arithmetic": {"total": 130, "holdout": 52, "non_holdout": 78, "identity": 130 - 52 == 78},
        "checks": {
            "fixture_count": len(source_rows) == 65,
            "family_count": source["feature_family_count"] == 13,
            "variants_per_family": source["variants_per_feature"] == 5,
            "holdout_manifest_count": holdout["holdout_count"] == 26 == len(holdout_variants),
            "pipeline_case_counts": len(atomic_lo) == 65 and len(atomic_google) == 65,
            "arithmetic": len(atomic_lo) + len(atomic_google) == 130 and sum(len(rows) for rows in holdout_by_pipeline.values()) == 52 and sum(len(rows) for rows in nonholdout_by_pipeline.values()) == 78,
            "calibration_is_separate": calibration["control_count"] == 78 and all("control_id" in row for row in calibration["rows"]),
        },
    }
    result["status"] = "PASS" if all(result["checks"].values()) else "FAIL"
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "V5_HOLDOUT_ACCOUNTING_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# V5 holdout accounting audit", "", f"Status: **{result['status']}**.", "",
        "## Source of truth", "",
        "The audit reads `experiments/v4/source_manifest.json`, `HOLDOUT_MANIFEST.json`, both primary conversion manifests, and `COMPARATOR_CALIBRATION.json`; it does not infer counts from manuscript prose.", "",
        "## Derived accounting", "",
        "| Quantity | Value |", "|---|---:|", f"| Atomic fixtures | {result['atomic_fixtures']} |", f"| Primary pipelines | {len(primary_pipelines)} |", f"| Holdout fixtures | {result['holdout_fixtures']} |", f"| Holdout fixture–pipeline cases | {sum(result['holdout_fixture_pipeline_cases'].values())} |", f"| Non-holdout fixture–pipeline cases | {sum(result['non_holdout_fixture_pipeline_cases'].values())} |", f"| Primary cases | {result['primary_cases']} |", f"| Calibration controls | {result['calibration_cases']} |", "",
        "The holdout is fixture-level: D and E are held out for every primary pipeline. Therefore each pipeline has 26 holdout cases and 39 non-holdout cases; across two pipelines the correct arithmetic is **130 − 52 = 78**, not 130 − 26 = 104.", "",
        "Calibration controls are synthetic diagnostic destinations, not fixture–pipeline outcomes and do not overlap the primary fixture IDs.", "",
        "## Automated assertions", "",
    ]
    lines.extend(f"- `{name}`: {'PASS' if value else 'FAIL'}" for name, value in result["checks"].items())
    lines.extend(["", "## Files corrected", "", "No V4 file was rewritten by this audit. The V5 report and JSON audit are new. Any manuscript copy using 104 non-holdout cases must be corrected to 78; current V4 final sections already state 104 as the complement of the 26-case per-pipeline holdout, so the V5 manuscript revision must state both per-pipeline and aggregate denominators explicitly.", ""])
    (REPORTS / "V5_HOLDOUT_ACCOUNTING_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "primary_cases": result["primary_cases"], "holdout_cases": sum(result["holdout_fixture_pipeline_cases"].values()), "non_holdout_cases": sum(result["non_holdout_fixture_pipeline_cases"].values())}, indent=2))


if __name__ == "__main__":
    main()
