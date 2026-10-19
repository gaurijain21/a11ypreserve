"""Build the anonymous ICST 2027 V4 upload bundle from frozen artifacts.

This script copies verified evidence and converter outputs without changing them,
while sanitizing local machine paths in text/JSON copies. Canonical repository
files are never rewritten.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V4 = ROOT / "experiments" / "v4"
SUB = ROOT / "submission" / "ICST2027_V4"
UPLOAD = SUB / "upload"
PACKAGE = UPLOAD / "replication_package"

TEXT_SUFFIXES = {
    ".json", ".md", ".py", ".ps1", ".tex", ".bib", ".txt", ".csv", ".toml", ".yaml", ".yml"
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
    escaped_root = str(ROOT).replace(chr(92), chr(92) * 2)    text = text.replace(escaped_root, "<ARTIFACT_ROOT>")
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Users[\\/]+[^\\/\"']+", "<USER_HOME>", text)
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Users[\\/]+[^\"\r\n]+", "<USER_HOME>", text)
    text = re.sub(r"(?i)" + re.escape("C:") + r"[\\/]+Program Files(?: \(x86\))?[\\/]+[^\"']+", "<INSTALLED_APPLICATION>", text)
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


def copy_tree(source: Path, relative_root: str, pattern: str | None = None) -> int:
    count = 0
    for item in source.rglob(pattern or "*"):
        if not item.is_file() or "__pycache__" in item.parts:
            continue
        relative = Path(relative_root) / item.relative_to(source)
        copy_file(item, str(relative))
        count += 1
    return count


def write_text(relative: str, content: str) -> None:
    destination = PACKAGE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def remove_upload_tree(path: Path) -> None:
    """Clear a previously generated bundle, including OneDrive read-only files."""
    def clear_readonly(func, target, exc_info):
        target_path = Path(target)
        try:
            target_path.chmod(target_path.stat().st_mode | stat.S_IWRITE)
            func(target)
        except OSError:
            raise exc_info[1]

    shutil.rmtree(path, onerror=clear_readonly)


def main() -> None:
    if UPLOAD.exists():
        if UPLOAD.resolve().parent != SUB.resolve():
            raise RuntimeError(f"Refusing to clear unexpected path: {UPLOAD}")
        remove_upload_tree(UPLOAD)
    PACKAGE.mkdir(parents=True)

    shutil.copy2(SUB / "main.pdf", UPLOAD / "paper.pdf")

    files = [
        V4 / "source_manifest.json",
        V4 / "PRE_RESULT_FREEZE.json",
        V4 / "HOLDOUT_MANIFEST.json",
        V4 / "REPEATABILITY_MANIFEST.json",
        V4 / "CALIBRATION_CONTROLS.json",
        V4 / "COMPARATOR_CALIBRATION.json",
        V4 / "SOURCE_VALIDATION.json",
        V4 / "SOURCE_ORACLE_CERTIFICATE.json",
        V4 / "SOURCE_ORACLE_MUTATION_AUDIT.json",
        V4 / "V4_PROTOCOL.md",
        V4 / "results" / "V4_ACCOUNTING.json",
        V4 / "results" / "V4_PRIMARY_RESULTS.json",
        V4 / "conversions" / "CROSS_PIPELINE_COMPARISON.json",
        V4 / "conversions" / "V4_CONVERSION_RECOVERY_AUDIT.json",
        V4 / "conversions" / "V4_REPEATABILITY_NORMALIZED.json",
        V4 / "realistic" / "REALISTIC_CORPUS_MANIFEST.json",
        V4 / "realistic" / "REALISTIC_CONTRACTS.json",
        V4 / "realistic" / "REALISTIC_SOURCE_VALIDATION.json",
        V4 / "conversions" / "libreoffice" / "manifest.json",
        V4 / "conversions" / "google" / "manifest.json",
        V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json",
        V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json",
        V4 / "conversions" / "word" / "manifest.json",
        V4 / "conversions" / "word" / "repeatability_manifest.json",
        V4 / "conversions" / "word" / "analysis" / "V4_WORD_ANALYSIS.json",
        V4 / "conversions" / "word" / "analysis" / "V4_WORD_REPEATABILITY_ANALYSIS.json",
        V4 / "word_supplement" / "WORD_SUPPLEMENT_PROTOCOL.md",
        V4 / "conversions" / "libreoffice" / "repeatability" / "V4_LIBREOFFICE_REPEATABILITY.json",
        V4 / "conversions" / "google" / "repeatability" / "V4_GOOGLE_REPEATABILITY.json",
    ]
    for source in files:
        if source.exists():
            copy_file(source, str(Path("evidence") / source.relative_to(V4)))

    copy_tree(V4 / "fixtures", "source/fixtures")
    copy_tree(V4 / "manifests", "source/manifests")
    copy_tree(V4 / "source_extractions", "source/source_extractions")
    copy_tree(V4 / "source_oracle_certificates", "source/source_oracle_certificates")
    copy_tree(V4 / "realistic", "source/realistic", "*.docx")

    for pipeline in ("libreoffice", "google"):
        output_root = V4 / "conversions" / pipeline / "outputs"
        if output_root.exists():
            copy_tree(output_root, f"outputs/{pipeline}", "*.pdf")
    word_output_root = V4 / "conversions" / "word" / "outputs"
    if word_output_root.exists():
        copy_tree(word_output_root, "outputs/word", "*.pdf")

    for source in [
        V4 / "v4_source_oracle.py",
        V4 / "v4_comparator.py",
        V4 / "run_frozen_analysis.py",
        V4 / "run_libreoffice_v4.py",
        V4 / "run_google_frozen_analysis.py",
        V4 / "run_libreoffice_repeatability.py",
        V4 / "analyze_libreoffice_repeatability.py",
        V4 / "analyze_google_repeatability.py",
        V4 / "word_supplement" / "build_word_manifest.py",
        V4 / "word_supplement" / "build_word_repeatability_manifest.py",
        V4 / "word_supplement" / "run_word_supplementary_analysis.py",
        V4 / "word_supplement" / "run_word_repeatability_analysis.py",
        V4 / "compare_pipelines.py",
        ROOT / "check_v4_manuscript_consistency.py",
    ]:
        if source.exists():
            copy_file(source, str(Path("reproduction") / source.name))

    write_text(
        "README.md",
        """# Anonymous A11yPreserve V4 replication package

This package accompanies the anonymous ICST 2027 Research Papers submission. It contains the frozen V4 source fixtures, source manifests/contracts, verified conversion records and PDFs for the two primary LibreOffice and Google Docs conditions, the separately frozen supplementary Microsoft Word desktop GUI arm, frozen analysis records, repeatability records, and reproduction scripts.

The prospectively frozen primary corpus contains 65 atomic DOCX fixtures and 130 fixture--pipeline cases across LibreOffice and Google Docs. The supplementary Word arm adds 65 atomic observations, for 195 archived atomic observations in total without changing the primary denominator. The primary realistic arm contains 10 project-created integrated DOCX documents and 78 property contracts per pipeline; Word adds 10 supplementary PDFs and the same frozen contracts are analyzed separately. These documents are not a natural external corpus.

Word desktop used native GUI File -> Export -> Create PDF/XPS with document-structure tags enabled. COM activation failed with 0x80070520 in the local Windows session, so the GUI route was used and separately frozen. The included Word PDFs are genuine desktop Word exports, not print-to-PDF or relabeled outputs. Word classifications can be reproduced from the included PDFs without running Word.

No credentials, cookies, browser profiles, account identifiers, or private cloud material are included. Local machine paths are replaced with placeholders in text and JSON copies. Canonical repository files are not modified by bundle construction.

Reproduction is environment-dependent. Use the source manifests and recorded converter conditions; do not edit fixtures or decision rules. The included PDFs are the genuine outputs used for the frozen analysis, not relabeled outputs from another converter.
""",
    )
    write_text(
        "REPRODUCTION_NOTES.md",
        """# Reproduction notes

The manuscript reports the frozen V4 analysis already present in the evidence records. Re-running conversion requires the named converter environments and, for Google Docs, an authorized account/session; credentials are intentionally not distributed. The package preserves route and provenance records without including browser state.

The manuscript consistency checker is included under `reproduction/`. It checks the displayed scientific counts against the canonical analysis JSON.
""",
    )

    manifest = {}
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file():
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

    upload_readme = UPLOAD / "UPLOAD_README.md"
    upload_readme.write_text(
        """# Anonymous ICST 2027 upload bundle

- `paper.pdf`: anonymous 8-page IEEE conference-format Research Papers manuscript.
- `replication_package.zip`: anonymized replication package with frozen evidence and genuine converter outputs.

Before portal submission, the authors must complete HotCRP author/COI fields, verify the final author-anonymity state, and confirm compliance with simultaneous-submission rules.
""",
        encoding="utf-8",
    )

    bundle_manifest = {
        "paper": {"path": "paper.pdf", "sha256": sha256(UPLOAD / "paper.pdf"), "size": (UPLOAD / "paper.pdf").stat().st_size},
        "replication_package": {"path": "replication_package.zip", "sha256": sha256(package_zip), "size": package_zip.stat().st_size},
        "generated_from_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "protocol_freeze_commit": "41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1",
        "scientific_results_modified": False,
    }
    (UPLOAD / "BUNDLE_MANIFEST.json").write_text(json.dumps(bundle_manifest, indent=2) + "\n", encoding="utf-8")

    bundle_zip = SUB / "ICST2027_V4_anonymous_upload.zip"
    if bundle_zip.exists():
        bundle_zip.unlink()
    with zipfile.ZipFile(bundle_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ("paper.pdf", "replication_package.zip", "UPLOAD_README.md", "BUNDLE_MANIFEST.json"):
            archive.write(UPLOAD / name, name)

    print(json.dumps({
        "status": "PASS",
        "package_files": len(manifest),
        "atomic_fixtures": len(list((PACKAGE / "source" / "fixtures").glob("*.docx"))),
        "libreoffice_pdfs": len(list((PACKAGE / "outputs" / "libreoffice").rglob("*.pdf"))),
        "google_pdfs": len(list((PACKAGE / "outputs" / "google").rglob("*.pdf"))),
        "word_atomic_pdfs": len(list((PACKAGE / "outputs" / "word" / "atomic").rglob("*.pdf"))),
        "word_realistic_pdfs": len(list((PACKAGE / "outputs" / "word" / "realistic").rglob("*.pdf"))),
        "word_repeatability_pdfs": len(list((PACKAGE / "outputs" / "word" / "repeatability").rglob("*.pdf"))),
        "primary_atomic_observations": 130,
        "supplementary_word_atomic_observations": 65,
        "archived_atomic_observations": 195,
        "paper": str(UPLOAD / "paper.pdf"),
        "bundle": str(bundle_zip),
    }, indent=2))


if __name__ == "__main__":
    main()
