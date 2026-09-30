from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    ("source_verification", ["scripts/verify_corpus_ooxml.py"]),
    ("phase4", ["scripts/phase4_tests.py"]),
    ("pilot1", ["scripts/test_pilot.py"]),
    ("pilot2", ["scripts/pilot2_tests.py"]),
    ("pilot3", ["scripts/pilot3_tests.py"]),
    ("full_experiment_regressions", ["scripts/full_experiment_tests.py"]),
]


def main() -> None:
    results = []
    for name, script in SUITES:
        command = [sys.executable, *script]
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        results.append({"suite": name, "command": command, "return_code": completed.returncode, "passed": completed.returncode == 0, "stdout_tail": completed.stdout[-3000:], "stderr_tail": completed.stderr[-3000:]})
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "passed": all(row["passed"] for row in results), "suites": results, "new_tests_added": ["scripts/validate_full_outputs.py", "scripts/run_full_experiment_analysis.py", "scripts/full_experiment_tests.py"]}
    out = ROOT / "results" / "full_experiment" / "reports" / "test_results.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "suites": len(results), "failed": [row["suite"] for row in results if not row["passed"]]}))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
