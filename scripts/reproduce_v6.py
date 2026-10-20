"""Run the V6 scientific computations and integrity checks in order."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> None:
    print(f"== {label} ==")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    py = sys.executable
    run("V6 control rerun", [py, "experiments/v6/control_rerun.py"])
    run("V6 mutation sensitivity", [py, "experiments/v6/mutation_sensitivity.py"])
    run("V6 baseline and ablation", [py, "experiments/v6/baseline_ablation.py"])
    run("V6 human-readable reports", [py, "scripts/build_v6_reports.py"])
    run("V6 regression tests", [py, "tests/test_v6_scientific_hardening.py"])
    run("V6 scientific accounting", [py, "scripts/verify_v6_scientific_accounting.py"])
    run("V6 manuscript consistency", [py, "scripts/audit_v6_manuscript_consistency.py"])
    run("V6 anonymity audit", [py, "scripts/audit_v6_anonymity.py"])
    run("V6 PDF build provenance", [py, "scripts/record_v6_build_provenance.py"])
    run("V6 package manifest", [py, "scripts/build_v6_package_manifest.py"])
    run("V6 package manifest", [py, "scripts/verify_v6_package_manifest.py"])
    run("repository safety", [py, "scripts/audit_repository_safety.py"])
    print("V6 scientific reproduction/check: PASS")


if __name__ == "__main__":
    main()
