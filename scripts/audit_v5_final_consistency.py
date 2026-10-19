from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "experiments" / "v4"
V5 = ROOT / "experiments" / "v5"
REPORTS = ROOT / "reports"
MANUSCRIPT_ROOT = ROOT / "submission" / "ICST2027_V5"


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))


def counts(path: Path): return load(path)["summary"]["counts"]


def manuscript_text() -> str:
    paths = [MANUSCRIPT_ROOT / "main.tex", MANUSCRIPT_ROOT / "v5_hardening.tex"]
    paths.extend(sorted((MANUSCRIPT_ROOT / "sections").glob("*.tex")))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())


def main() -> None:
    source = load(V4 / "source_manifest.json")
    holdout = load(REPORTS / "V5_HOLDOUT_ACCOUNTING_AUDIT.json")
    calibration = load(V5 / "calibration_ground_truth_audit.json")
    mutations = load(V5 / "destination_mutation_manifest.json")
    profile_path = V5 / "LIBREOFFICE_PROFILE_B_ANALYSIS.json"
    lo = load(V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json")
    google = load(V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json")
    word = load(V4 / "conversions" / "word" / "analysis" / "V4_WORD_ANALYSIS.json")
    checks = {
        "atomic_fixture_count": source["fixture_count"] == 65,
        "feature_family_count": source["feature_family_count"] == 13,
        "variants_per_family": source["variants_per_feature"] == 5,
        "primary_denominator": len(lo["records"]) == 65 and len(google["records"]) == 65,
        "supplementary_denominator": len(word["records"]) == 65,
        "holdout_denominator": holdout["status"] == "PASS" and holdout["primary_cases"] == 130 and sum(holdout["holdout_fixture_pipeline_cases"].values()) == 52 and sum(holdout["non_holdout_fixture_pipeline_cases"].values()) == 78,
        "calibration_denominator": calibration["control_count"] == 78 and calibration["counts"] == {"correct": 60, "false_positives": 0, "false_negatives": 5, "correct_abstentions": 13},
        "destination_mutations": mutations["valid_mutants"] == 12 and mutations["detected_mutants"] == 12 and mutations["surviving_mutants"] == 0,
        "libreoffice_profile_b": profile_path.exists() and load(profile_path)["status"] == "COMPLETE" and len(load(profile_path)["records"]) == 65 and not load(profile_path)["classification_changes"] and load(profile_path)["profile_summary"]["v5_tagged_count"] == 65,
        "realistic_documents": len(load(V4 / "realistic" / "REALISTIC_CORPUS_MANIFEST.json")["records"]) == 10,
        "primary_counts_libreoffice": counts(V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json") == {"VERIFIED_PRESERVED": 38, "OBSERVED_PARTIAL": 11, "ALTERED": 9, "CONFIRMED_LOST": 1, "UNRESOLVED_EQUIVALENCE": 1, "MEASUREMENT_ERROR": 5},
        "primary_counts_google": counts(V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json") == {"VERIFIED_PRESERVED": 11, "OBSERVED_PARTIAL": 32, "ALTERED": 11, "CONFIRMED_LOST": 6, "UNRESOLVED_EQUIVALENCE": 5},
        "supplementary_counts_word": counts(V4 / "conversions" / "word" / "analysis" / "V4_WORD_ANALYSIS.json") == {"VERIFIED_PRESERVED": 16, "OBSERVED_PARTIAL": 26, "ALTERED": 16, "CONFIRMED_LOST": 2, "MEASUREMENT_ERROR": 5},
        "manuscript_primary_numbers": all(token in manuscript_text() for token in ("65 atomic DOCX fixtures", "130", "52 fixture-level holdout", "78 non-holdout", "38 & 11 & 16", "11 & 32 & 26", "9 & 11 & 16", "1 & 6 & 2", "1 & 5 & 0", "5 & 0 & 5")),
        "v4_provenance_exists": (ROOT / "V4_BASELINE_FREEZE.md").exists() and (ROOT / ".git").exists(),
    }
    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "v4_primary_denominator": 130, "v4_supplementary_denominator": 65, "v4_archived_atomic_observations": 195, "v5_profile_analysis": str((V5 / "LIBREOFFICE_PROFILE_B_ANALYSIS.json").relative_to(ROOT)) if (V5 / "LIBREOFFICE_PROFILE_B_ANALYSIS.json").exists() else "PENDING"}
    (REPORTS / "V5_FINAL_CONSISTENCY_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = ["# V5 final consistency audit", "", f"Status: **{result['status']}**.", "", "The audit checks frozen corpus sizes, primary/supplementary denominators, holdout arithmetic, calibration, destination mutations, LibreOffice profile completion, realistic-document count, exact classification sums, manuscript tokens, and V4 provenance references.", ""]
    lines.extend(f"- `{name}`: {'PASS' if value else 'FAIL'}" for name, value in checks.items())
    lines.extend(["", "The aggregate V4 accounting is 130 primary + 65 supplementary Word = 195 archived atomic observations. Supplementary Word rows are not included in the primary denominator.", ""])
    (REPORTS / "V5_FINAL_CONSISTENCY_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS": raise SystemExit(1)


if __name__ == "__main__": main()
