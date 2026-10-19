"""Run the one-command V5 repository checks."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> None:
    print(f"== {label} ==")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-artifacts", action="store_true", help="rerun destination mutations and rebuild the anonymous V5 bundle")
    args = parser.parse_args()
    py = sys.executable
    if args.refresh_artifacts:
        run("destination mutation testing", [py, "experiments/v5/destination_mutation_testing.py"])
    run("repository safety and secret audit", [py, "scripts/audit_repository_safety.py"])
    run("holdout accounting", [py, "scripts/audit_v5_holdout_accounting.py"])
    run("calibration audit", [py, "scripts/audit_v5_calibration.py"])
    run("V5 consistency audit", [py, "scripts/audit_v5_final_consistency.py"])
    run("V5 regression tests", [py, "tests/test_v5_hardening.py"])
    if args.refresh_artifacts:
        run("anonymous bundle build", [py, "build_v5_upload_bundle.py"])
    run("bundle verification", [py, "scripts/verify_v5_bundle.py"])
    print("V5 reproduction/check: PASS")


if __name__ == "__main__":
    main()
