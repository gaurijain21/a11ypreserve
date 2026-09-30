from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = {
    "source_verification": [sys.executable, "scripts/verify_corpus_ooxml.py"],
    "phase4": [sys.executable, "scripts/phase4_tests.py"],
    "pilot1": [sys.executable, "scripts/test_pilot.py"],
    "pilot2": [sys.executable, "scripts/pilot2_tests.py"],
    "pilot3": [sys.executable, "scripts/pilot3_tests.py"],
}


def main() -> None:
    rows = []
    for name, command in COMMANDS.items():
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        rows.append({"suite": name, "command": command, "return_code": completed.returncode, "passed": completed.returncode == 0, "stdout_tail": completed.stdout[-4000:], "stderr_tail": completed.stderr[-4000:]})
    report = {"checked_at": datetime.now().astimezone().isoformat(), "passed": all(row["passed"] for row in rows), "suites": rows, "new_tests_added": ["scripts/verify_corpus_ooxml.py", "scripts/phase4_tests.py"]}
    target = ROOT / "results" / "test_results.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
