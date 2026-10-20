"""Create a hash/size manifest for static V6 release files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [
        ROOT / "requirements-v6.txt",
        ROOT / ".github" / "workflows" / "v6.yml",
        ROOT / "scripts" / "build_v6_reports.py",
        ROOT / "scripts" / "verify_v6_scientific_accounting.py",
        ROOT / "scripts" / "verify_v6_package_manifest.py",
        ROOT / "scripts" / "record_v6_build_provenance.py",
        ROOT / "scripts" / "audit_v6_manuscript_consistency.py",
        ROOT / "scripts" / "audit_v6_anonymity.py",
        ROOT / "scripts" / "build_v6_upload_bundle.py",
        ROOT / "scripts" / "reproduce_v6.py",
        ROOT / "scripts" / "verify_v6_upload_bundle.py",
        ROOT / "experiments" / "v6" / "common.py",
        ROOT / "experiments" / "v6" / "control_rerun.py",
        ROOT / "experiments" / "v6" / "mutation_sensitivity.py",
        ROOT / "experiments" / "v6" / "baseline_ablation.py",
        ROOT / "tests" / "test_v6_scientific_hardening.py",
        ROOT / "submission" / "ICST2027_V6" / "main.tex",
        ROOT / "submission" / "ICST2027_V6" / "v6_hardening.tex",
        ROOT / "submission" / "ICST2027_V6" / "references.bib",
        ROOT / "submission" / "ICST2027_V6" / "IEEEtran.cls",
        ROOT / "submission" / "ICST2027_V6" / "IEEEtran.bst",
        ROOT / "submission" / "ICST2027_V6" / "main.pdf",
    ]
    paths.extend(sorted((ROOT / "submission" / "ICST2027_V6" / "sections").glob("*.tex")))
    rows = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"missing static V6 file: {path}")
        rows.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "size_bytes": path.stat().st_size, "sha256": sha256(path)})
    result = {"manifest_version": "V6-static-files-1", "files": rows}
    output = ROOT / "experiments" / "v6" / "V6_PACKAGE_MANIFEST.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "files": len(rows), "manifest": str(output.relative_to(ROOT)).replace("\\", "/")}, indent=2))


if __name__ == "__main__":
    main()
