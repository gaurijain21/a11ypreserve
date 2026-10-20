"""Verify V6 static-file hashes and sizes; fail on missing or unexpected listed files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "experiments" / "v6" / "V6_PACKAGE_MANIFEST.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    for row in manifest["files"]:
        path = ROOT / row["path"]
        if not path.is_file():
            failures.append({"path": row["path"], "reason": "missing"})
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if path.stat().st_size != row["size_bytes"]:
            failures.append({"path": row["path"], "reason": "size mismatch"})
        if digest != row["sha256"]:
            failures.append({"path": row["path"], "reason": "sha256 mismatch"})
    result = {"status": "PASS" if not failures else "FAIL", "listed_files": len(manifest["files"]), "failures": failures}
    (ROOT / "reports" / "v6" / "V6_PACKAGE_MANIFEST_CHECK.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
