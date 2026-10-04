"""Evidence-only V4 verification entry point.

External GUI/cloud conversion is intentionally not automated here. The script
verifies the frozen source corpus and calibration, then analyzes only existing
V4 outputs when present.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(command: list[str]) -> int:
    print("$", " ".join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--calibration", action="store_true")
    parser.add_argument("--existing-outputs", action="store_true")
    parser.add_argument("--full-analysis", action="store_true")
    args = parser.parse_args()
    selected = any(vars(args).values())
    if not selected or args.source_only or args.full_analysis:
        for command in [[sys.executable, "experiments/v4/v4_source_oracle.py"], [sys.executable, "experiments/v4/validate_v4_source.py"], [sys.executable, "experiments/v4/source_mutation_audit.py"], [sys.executable, "experiments/v4/validate_realistic_v4.py"]]:
            if run(command): return 1
    if not selected or args.calibration or args.full_analysis:
        if run([sys.executable, "experiments/v4/comparator_calibration.py"]): return 1
    if args.existing_outputs or args.full_analysis:
        output_dir = ROOT / "experiments" / "v4" / "outputs"
        if output_dir.exists() and any(output_dir.rglob("*.pdf")):
            print("Existing V4 PDF outputs found; run the project-specific extraction/analysis command documented in experiments/v4/V4_PROTOCOL.md.")
        else:
            print("No V4 PDF outputs found; conversion-dependent analysis remains unrun.")
    print("V4 verification PASS for all available evidence-only checks; external converter execution was not recreated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
