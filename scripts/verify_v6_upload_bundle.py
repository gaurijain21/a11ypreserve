"""Verify the V6 anonymous upload bundle without trusting its manifest alone."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submission" / "ICST2027_V6"
BUNDLE = SUB / "ICST2027_V6_anonymous_upload.zip"
PACKAGE_ZIP = SUB / "upload_v6" / "replication_package.zip"
FORBIDDEN = [
    re.compile(r"[A-Za-z]:[\\/]Users[\\/]", re.IGNORECASE),
    re.compile(r"OneDrive", re.IGNORECASE),
    re.compile(r"iamga", re.IGNORECASE),
    re.compile(r"gaurijain", re.IGNORECASE),
]
DETECTOR_SOURCE = "replication_package/reproduction/audit_v6_anonymity.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures = []
    manifest_path = SUB / "upload_v6" / "BUNDLE_MANIFEST.json"
    if not BUNDLE.is_file() or not PACKAGE_ZIP.is_file() or not manifest_path.is_file():
        raise SystemExit("V6 upload bundle is incomplete")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if sha256(SUB / "upload_v6" / "paper.pdf") != manifest["paper"]["sha256"]:
        failures.append("paper hash mismatch")
    if sha256(PACKAGE_ZIP) != manifest["replication_package"]["sha256"]:
        failures.append("replication package hash mismatch")
    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        names = set(archive.namelist())
        required = {
            "replication_package/README.md",
            "replication_package/manuscript/main.tex",
            "replication_package/evidence/v6/experiments/V6_CONTROL_RERUN.json",
            "replication_package/evidence/v6/experiments/V6_MUTATION_SENSITIVITY.json",
            "replication_package/evidence/v6/experiments/V6_BASELINE_ABLATION.json",
            "replication_package/evidence/v6/reports/V6_SUBMISSION_READINESS.md",
            "replication_package/reproduction/reproduce_v6.py",
        }
        failures.extend(f"missing {name}" for name in sorted(required - names))
        forbidden_names = [name for name in names if name.endswith("CITATION.cff") or name.endswith("LICENSE")]
        failures.extend(f"identity/legal metadata unexpectedly included: {name}" for name in forbidden_names)
        for name in sorted(names):
            if not name.lower().endswith((".json", ".md", ".py", ".tex", ".bib", ".txt", ".yml", ".yaml")):
                continue
            text = archive.read(name).decode("utf-8", errors="replace")
            # The detector source intentionally contains the patterns it is
            # designed to find.  Keep this exemption exact and explicit; all
            # other packaged text remains subject to the private-path scan.
            if name == DETECTOR_SOURCE:
                continue
            for pattern in FORBIDDEN:
                if pattern.search(text):
                    failures.append(f"private-path pattern {pattern.pattern} in {name}")
    result = {"status": "PASS" if not failures else "FAIL", "bundle": str(BUNDLE.relative_to(ROOT)).replace("\\", "/"), "package_files": manifest["replication_package"]["files"], "failures": failures}
    output = ROOT / "reports" / "v6" / "V6_UPLOAD_BUNDLE_CHECK.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
