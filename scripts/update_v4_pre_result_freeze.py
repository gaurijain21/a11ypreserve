from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    files = []
    for path in (ROOT / "experiments" / "v4").rglob("*"):
        if path.is_file() and "results" not in path.parts:
            files.append(path)
    files += [ROOT / "docs" / "V4_FAULT_MODEL.md", ROOT / "docs" / "V4_FEATURE_SELECTION_MATRIX.md", ROOT / "docs" / "V4_DESTINATION_EXTRACTION_PLAN.md", ROOT / "reports" / "V4_PRIOR_ART_AUDIT.md", ROOT / "reports" / "V4_CONVERTER_FEASIBILITY.md", ROOT / "reports" / "V4_READING_ORDER_DECISION.md", ROOT / "reports" / "V4_REPEATABILITY_REPORT.md", ROOT / "reports" / "V4_UNRESOLVED_CASE_ANALYSIS.md"]
    records = {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in sorted(set(files))}
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {"freeze_type": "V4 final pre-result methodology and corpus freeze", "initial_protocol_freeze_commit": "41a7d3f", "created_from_git_commit": commit, "converter_outputs_inspected_before_freeze": False, "files": records}
    (ROOT / "experiments" / "v4" / "PRE_RESULT_FREEZE.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"commit": commit, "files": len(records)}, indent=2))


if __name__ == "__main__":
    main()
