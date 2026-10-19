"""Run the evidence-only reproducibility checks for A11yPreserve."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
COMMANDS = [
    [sys.executable, "tools/audit_submission_consistency.py"],
    [sys.executable, "tools/test_source_oracle_corruptions.py"],
    [sys.executable, "artifact_v3/src/independent_source_oracle.py"],
    [sys.executable, "artifact_v3/src/verify_public_package.py"],
]


def main() -> int:
    for command in COMMANDS:
        print("$", " ".join(command), flush=True)
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode:
            return completed.returncode
    print("Evidence-only reproduction PASS")
    print("External authenticated Google Docs conversion and Word COM export are not run by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
