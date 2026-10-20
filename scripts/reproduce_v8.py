"""Run the additive A11yPreserve hardening checks without overwriting freezes."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> None:
    command = [sys.executable, str(ROOT / "scripts" / script)]
    completed = subprocess.run(command, cwd=ROOT, text=True)
    if completed.returncode:
        raise SystemExit(f"{script} failed with exit code {completed.returncode}")


def verify_results() -> None:
    mutation = json.loads((ROOT / "experiments/v8/V8_MUTATION_GROUND_TRUTH.json").read_text(encoding="utf-8"))
    benign = json.loads((ROOT / "experiments/v8/V8_BENIGN_TRANSFORMATIONS.json").read_text(encoding="utf-8"))
    cross = json.loads((ROOT / "experiments/v8/V8_CROSS_CONVERTER_MUTATIONS.json").read_text(encoding="utf-8"))
    coverage = json.loads((ROOT / "experiments/v8/V8_FIXTURE_COVERAGE.json").read_text(encoding="utf-8"))
    expected = {
        "mutation_attempted": 65, "mutation_applied": 59,
        "mutation_faults": 59, "mutation_detected": 46,
        "mutation_survivors": 13, "mutation_unsupported": 6,
        "benign_controls": 26, "benign_projection_alerts": 0,
        "benign_classification_regressions": 0, "cross_attempted": 39,
        "coverage_families": 13, "coverage_atomic_fixtures": 65,
    }
    actual = {
        "mutation_attempted": mutation["attempted"], "mutation_applied": mutation["application_success"],
        "mutation_faults": mutation["independently_established_semantic_faults"],
        "mutation_detected": mutation["scorable_faults_detected_by_frozen_comparator"],
        "mutation_survivors": mutation["genuine_surviving_faults"],
        "mutation_unsupported": mutation["reference_tier_counts"].get("B", 0),
        "benign_controls": benign["controls"], "benign_projection_alerts": benign["projection_alerts"],
        "benign_classification_regressions": benign["classification_regressions"],
        "cross_attempted": cross["attempted"], "coverage_families": coverage["family_count"],
        "coverage_atomic_fixtures": coverage["atomic_fixture_count"],
    }
    if actual != expected:
        raise SystemExit(json.dumps({"expected": expected, "actual": actual}, indent=2))
    print(json.dumps({"status": "PASS", "verified": actual}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true", help="check existing V8 JSON without regenerating it")
    args = parser.parse_args()
    if not args.verify_only:
        for script in ("v8_mutation_ground_truth_audit.py", "v8_benign_transformations.py", "v8_cross_converter_mutation.py", "v8_fixture_coverage_audit.py"):
            run(script)
    verify_results()


if __name__ == "__main__":
    main()
