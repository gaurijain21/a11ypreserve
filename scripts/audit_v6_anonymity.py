"""Check that the V6 release package contains no checkout/account-specific paths."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = [ROOT / "experiments" / "v6", ROOT / "reports" / "v6", ROOT / "submission" / "ICST2027_V6"]
PATTERNS = [
    re.compile(r"[A-Za-z]:[\\/]Users[\\/]", re.IGNORECASE),
    re.compile(r"OneDrive", re.IGNORECASE),
    re.compile(r"iamga", re.IGNORECASE),
    re.compile(r"gaurijain", re.IGNORECASE),
    re.compile(r"AUTHOR-REQUIRED", re.IGNORECASE),
]


def main() -> None:
    findings = []
    output = ROOT / "reports" / "v6" / "V6_ANONYMITY_CHECK.json"
    for root in SCAN_ROOTS:
        for path in root.rglob("*"):
            if path == output or path.name == "V6_UPLOAD_BUNDLE_CHECK.json":
                continue
            # The generated upload candidate is checked independently by
            # verify_v6_upload_bundle.py.  Exclude it here so the repository
            # scan does not report the detector source's intentional pattern
            # literals as leaked identity data.
            if "upload_v6" in path.parts:
                continue
            if not path.is_file() or path.suffix.lower() in {".pdf", ".png", ".docx", ".pyc", ".log", ".aux", ".bbl", ".blg", ".out"} or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                findings.append({"path": str(path.relative_to(ROOT)), "reason": f"read failure: {exc}"})
                continue
            for pattern in PATTERNS:
                if pattern.search(text):
                    findings.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "pattern": pattern.pattern})
    result = {"status": "PASS" if not findings else "FAIL", "scanned_roots": [str(p.relative_to(ROOT)).replace("\\", "/") for p in SCAN_ROOTS], "findings": findings}
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
