"""Build the anonymous ICST 2027 V5 upload bundle.

The bundle preserves the verified V4 replication package and adds the
completed V5 hardening inputs, analyses, reports, and self-contained manuscript
sources. Text copies are sanitized for local paths; repository source files
are not rewritten.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUB = ROOT / "submission" / "ICST2027_V5"
V4_PACKAGE = ROOT / "submission" / "ICST2027_V4" / "upload" / "replication_package"
UPLOAD = SUB / "upload_v5"
PACKAGE = UPLOAD / "replication_package"

TEXT_SUFFIXES = {
    ".json", ".md", ".py", ".ps1", ".tex", ".bib", ".txt", ".csv", ".toml", ".yaml", ".yml", ".vbs"
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sanitize(text: str) -> str:
    text = text.replace(str(ROOT), "<ARTIFACT_ROOT>")
    text = text.replace(str(ROOT).replace("\\", "/"), "<ARTIFACT_ROOT>")
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Users[\\/]+[^\\/\"']+", "<USER_HOME>", text)
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Users[\\/]+[^\"\r\n]+", "<USER_HOME>", text)
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Program Files(?: \(x86\))?[\\/]+[^\"']+", "<INSTALLED_APPLICATION>", text)
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Program Files(?: \(x86\))?[\\/]+[^\"\r\n]+", "<INSTALLED_APPLICATION>", text)
    text = text.replace("<CLOUD_PATH>/", "<CLOUD_PATH>/")
    text = text.replace(r"<LOCAL_WORD_WORKSPACE>", "<LOCAL_WORD_WORKSPACE>")
    text = text.replace("C:" + chr(92) * 2 + "A11yWordTest", "<LOCAL_WORD_WORKSPACE>")
    text = text.replace("C:" + "/A11yWordTest", "<LOCAL_WORD_WORKSPACE>")
    return text


def copy_file(source: Path, relative: str, *, sanitize_text: bool = True) -> None:
    destination = PACKAGE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if sanitize_text and source.suffix.lower() in TEXT_SUFFIXES:
        destination.write_text(sanitize(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    else:
        shutil.copy2(source, destination)


def copy_tree(source: Path, relative_root: str) -> int:
    count = 0
    for item in source.rglob("*"):
        if (
            not item.is_file()
            or "__pycache__" in item.parts
            or "cache" in {part.lower() for part in item.parts}
            or "profiles" in {part.lower() for part in item.parts}
            or item.suffix.lower() in {".bin", ".lock"}
        ):
            continue
        copy_file(item, str(Path(relative_root) / item.relative_to(source)))
        count += 1
    return count


def write_text(relative: str, content: str) -> None:
    destination = PACKAGE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def main() -> None:
    if not V4_PACKAGE.is_dir():
        raise RuntimeError(f"Missing verified V4 package: {V4_PACKAGE}")
    if UPLOAD.exists():
        if UPLOAD.resolve().parent != SUB.resolve():
            raise RuntimeError(f"Refusing to clear unexpected path: {UPLOAD}")
        shutil.rmtree(UPLOAD)
    UPLOAD.mkdir(parents=True)
    PACKAGE.mkdir(parents=True)

    shutil.copy2(SUB / "main.pdf", UPLOAD / "paper.pdf")
    copy_tree(V4_PACKAGE, "")

    for source in [SUB / "main.tex", SUB / "v5_hardening.tex", SUB / "IEEEtran.cls", SUB / "IEEEtran.bst", SUB / "references.bib", SUB / "build.ps1"]:
        copy_file(source, str(Path("manuscript") / source.name))
    copy_tree(SUB / "sections", "manuscript/sections")

    for source in [ROOT / "FINAL_V5_RESEARCH_READINESS.md", ROOT / "V5_BASELINE_AND_CHANGE_POLICY.md"]:
        copy_file(source, str(Path("evidence") / "v5" / source.name))
    for source in sorted((ROOT / "reports").glob("V5_*.md")):
        copy_file(source, str(Path("evidence") / "v5" / source.name))
    copy_tree(ROOT / "contracts" / "v5", "evidence/v5/contracts")
    copy_tree(ROOT / "experiments" / "v5", "evidence/v5/experiments")
    for source in [
        ROOT / "scripts" / "audit_v5_holdout_accounting.py",
        ROOT / "scripts" / "audit_v5_calibration.py",
        ROOT / "scripts" / "audit_v5_final_consistency.py",        ROOT / "scripts" / "audit_repository_safety.py",        ROOT / "scripts" / "verify_v5_bundle.py",        ROOT / "scripts" / "reproduce_v5.py",        ROOT / "requirements-v5.txt",
        ROOT / "tests" / "test_v5_hardening.py",
    ]:
        copy_file(source, str(Path("reproduction") / source.name))

    write_text(
        "README.md",
        """# Anonymous A11yPreserve V5 replication package

This package accompanies the anonymous ICST 2027 Research Papers submission. It preserves the verified V4 evidence package and adds the completed V5 hardening layer: fixture-level holdout accounting, the LibreOffice export-profile comparison, source and destination mutation audits, an independent diagnostic cross-check, calibration ground-truth records, cross-format contracts, and the corresponding reports and reproduction scripts.

The primary denominator remains 130 fixture--pipeline cases across LibreOffice and Google Docs. Microsoft Word remains a separately reported supplementary arm with 65 atomic observations. The package does not pool supplementary or project-created realistic documents into the primary denominator.

The self-contained manuscript sources are under `manuscript/`; the anonymous paper is `../paper.pdf`. The V5 audit scripts can be run from a repository checkout with the original project layout. Google Docs reproduction requires an authorized session; credentials, cookies, browser profiles, account identifiers, and private cloud material are intentionally not distributed.

All local machine paths in text and JSON copies are replaced with placeholders. The included PDFs are the genuine outputs used for the recorded analyses, not relabeled outputs from another converter. The study claims selected machine-verifiable preservation contracts under recorded conditions; it is not a complete PDF accessibility validator, user study, prevalence estimate, or universal converter ranking.
""",
    )
    write_text(
        "REPRODUCTION_NOTES.md",
        """# V5 reproduction notes

The V4 evidence and V5 hardening records are frozen inputs to the anonymous package. Run the three `audit_v5_*.py` scripts and `test_v5_hardening.py` to check the machine-derived accounting and regression assertions. Re-running conversion requires the named converter environments; Google Docs requires an authorized account/session, and Word requires the recorded desktop GUI route.

The manuscript source is self-contained under `manuscript/`. The V5 build uses three `pdflatex` passes with `bibtex` after the first pass; the generated anonymous PDF is stored at the package root as `paper.pdf`.
""",
    )

    manifest = {}
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file() and path.name != "PACKAGE_MANIFEST.json":
            manifest[str(path.relative_to(PACKAGE)).replace("\\", "/")] = {
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
    (PACKAGE / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    package_zip = UPLOAD / "replication_package.zip"
    with zipfile.ZipFile(package_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, str(Path("replication_package") / path.relative_to(PACKAGE)))

    (UPLOAD / "UPLOAD_README.md").write_text(
        """# Anonymous ICST 2027 V5 upload bundle

- `paper.pdf`: anonymous 9-page IEEE conference-format Research Papers manuscript.
- `replication_package.zip`: sanitized V5 replication package containing the frozen V4 evidence and completed V5 hardening records.

Before portal submission, complete the HotCRP author/COI fields, final author-anonymity check, originality and simultaneous-submission declarations, and any portal-specific artifact license/access settings.
""",
        encoding="utf-8",
    )

    bundle_manifest = {
        "paper": {"path": "paper.pdf", "sha256": sha256(UPLOAD / "paper.pdf"), "size": (UPLOAD / "paper.pdf").stat().st_size, "pages": 9},
        "replication_package": {"path": "replication_package.zip", "sha256": sha256(package_zip), "size": package_zip.stat().st_size, "files": len(manifest)},
        "generated_from_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scientific_results_modified": False,
        "v5_hardening_included": True,
    }
    (UPLOAD / "BUNDLE_MANIFEST.json").write_text(json.dumps(bundle_manifest, indent=2) + "\n", encoding="utf-8")

    bundle_zip = SUB / "ICST2027_V5_anonymous_upload.zip"
    if bundle_zip.exists():
        bundle_zip.unlink()
    with zipfile.ZipFile(bundle_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ("paper.pdf", "replication_package.zip", "UPLOAD_README.md", "BUNDLE_MANIFEST.json"):
            archive.write(UPLOAD / name, name)

    print(json.dumps({
        "status": "PASS",
        "package_files": len(manifest),
        "paper": str(UPLOAD / "paper.pdf"),
        "replication_package": str(package_zip),
        "bundle": str(bundle_zip),
    }, indent=2))


if __name__ == "__main__":
    main()
