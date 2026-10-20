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
    parser.add_argument(
        "--refresh-artifacts",
        action="store_true",
        help="deprecated: V5 artifacts are frozen; use scripts/reproduce_v6.py for fresh reruns",
    )
    args = parser.parse_args()
    py = sys.executable
    if args.refresh_artifacts:
        raise SystemExit(
            "V5 historical artifacts are immutable. Run scripts/reproduce_v6.py "
            "for fresh control, mutation, and baseline computations."
        )
    run("repository safety and secret audit", [py, "scripts/audit_repository_safety.py"])
    run("holdout accounting", [py, "scripts/audit_v5_holdout_accounting.py"])
    run("calibration audit", [py, "scripts/audit_v5_calibration.py"])
    run("V5 consistency audit", [py, "scripts/audit_v5_final_consistency.py"])
    run("V5 regression tests", [py, "tests/test_v5_hardening.py"])
    run("bundle verification", [py, "scripts/verify_v5_bundle.py"])
    print("V5 reproduction/check: PASS")


if __name__ == "__main__":
    main()
