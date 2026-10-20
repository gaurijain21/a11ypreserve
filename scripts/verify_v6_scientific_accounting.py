"""Verify V6 scientific outputs and fail on stale or incomplete generated evidence."""
from __future__ import annotations

import ast
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"


def load(name: str):
    return json.loads((V6 / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recorded_time(path: Path, field: str) -> datetime:
    value = json.loads(path.read_text(encoding="utf-8"))[field]
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> None:
    control = load("V6_CONTROL_RERUN.json")
    mutation = load("V6_MUTATION_SENSITIVITY.json")
    ablation = load("V6_BASELINE_ABLATION.json")
    checks: dict[str, bool] = {}
    checks["control_complete"] = control["status"] == "COMPLETE" and control["controls_evaluated"] == 65
    checks["control_genuine"] = control["classification_disagreements"] >= 0 and control["extraction_failures"] >= 0
    checks["control_case_files"] = len(list((V6 / "control_rerun_cases").glob("*.json"))) == 65
    checks["mutation_complete"] = mutation["status"] == "COMPLETE" and mutation["attempted"] == 65
    checks["mutation_case_files"] = len(list((V6 / "mutation_cases").glob("*.json"))) == 65
    checks["mutation_counts_sum"] = sum(mutation["outcome_counts"].values()) == 65
    checks["ablation_complete"] = ablation["status"] == "COMPLETE" and ablation["primary_cases"] == 130
    checks["known_fault_denominator"] = ablation["mutation_fault_sensitivity"]["faults_evaluated"] == 59
    source_manifest = json.loads((ROOT / "experiments/v4/source_manifest.json").read_text(encoding="utf-8"))
    checks["frozen_denominators"] = (
        source_manifest["fixture_count"] == 65
        and source_manifest["feature_family_count"] == 13
        and source_manifest["variants_per_feature"] == 5
        and len(source_manifest["records"]) == 65
    )

    control_source = (ROOT / "experiments/v5/destination_mutation_testing.py").read_text(encoding="utf-8")
    tree = ast.parse(control_source)
    checks["no_tautological_assignment"] = all(
        "control_classification = baseline_classification" not in ast.unparse(node)
        and "false_positive = False" not in ast.unparse(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
    )
    for row in control["rows"]:
        checks[f"control_hash_{row['fixture_id']}"] = bool(row["source_sha256"] and row["pdf_sha256"])
    for row in mutation["rows"]:
        if row["mutated_pdf_sha256"]:
            checks[f"mutation_hash_{row['fixture_id']}"] = sha256(ROOT / row["mutated_pdf_path"]) == row["mutated_pdf_sha256"]

    generated_pairs = [
        (V6 / "V6_CONTROL_RERUN.json", V6 / "control_rerun_cases"),
        (V6 / "V6_MUTATION_SENSITIVITY.json", V6 / "mutation_cases"),
    ]
    for aggregate, directory in generated_pairs:
        case_paths = sorted(directory.glob("*.json"))
        aggregate_field = "completed_at_utc"
        case_times = [recorded_time(path, "timestamp_utc") for path in case_paths]
        # Filesystem mtimes are not provenance: Git restores and cloud-sync
        # tools can rewrite them while preserving the recorded experiment
        # chronology. Compare the serialized UTC timestamps instead.
        checks[f"fresh_{aggregate.name}"] = (
            bool(case_times)
            and aggregate_field in json.loads(aggregate.read_text(encoding="utf-8"))
            and recorded_time(aggregate, aggregate_field) >= max(case_times)
        )
    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    (ROOT / "reports" / "v6" / "V6_SCIENTIFIC_ACCOUNTING.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "failed": [name for name, value in checks.items() if not value]}, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
