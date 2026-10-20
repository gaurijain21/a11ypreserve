"""Build a sanitized, anonymous ICST 2027 V6 upload bundle.

The bundle is additive: the already-sanitized V5 replication package is retained
as historical evidence, while the V6 manuscript, evidence, reports, and checks
are added separately. Identity-bearing root citation/license files are omitted
pending author decisions.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submission" / "ICST2027_V6"
V5_PACKAGE = ROOT / "submission" / "ICST2027_V5" / "upload_v5" / "replication_package"
V6_EVIDENCE = ROOT / "experiments" / "v6"
V6_REPORTS = ROOT / "reports" / "v6"
UPLOAD = SUB / "upload_v6"
PACKAGE = UPLOAD / "replication_package"
BUNDLE_ZIP = SUB / "ICST2027_V6_anonymous_upload.zip"
PAPER_SOURCE = SUB / "v6_rebuild.pdf" if (SUB / "v6_rebuild.pdf").is_file() else SUB / "main.pdf"

TEXT_SUFFIXES = {".json", ".md", ".py", ".ps1", ".tex", ".bib", ".txt", ".csv", ".toml", ".yaml", ".yml", ".cff"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sanitize(text: str) -> str:
    text = text.replace(str(ROOT), "<ARTIFACT_ROOT>")
    text = text.replace(str(ROOT).replace("\\", "/"), "<ARTIFACT_ROOT>")
    text = re.sub(r"(?i)[A-Za-z]:[\\/]Users[\\/][^\\/\"']+", "<USER_HOME>", text)
    text = re.sub(r"(?i)[A-Za-z]:[\\/]Program Files(?: \(x86\))?[\\/][^\"']+", "<INSTALLED_APPLICATION>", text)
    text = text.replace("github.com/gaurijain21", "<ANONYMOUS_REPOSITORY>")
    text = text.replace("iamga", "<ANONYMOUS_USER>")
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
        parts_lower = {part.lower() for part in item.parts}
        if (
            not item.is_file()
            or item.name == "V6_UPLOAD_BUNDLE_CHECK.json"
            or "__pycache__" in item.parts
            or ".pdf-qa" in item.parts
            or "cache" in parts_lower
            or "profiles" in parts_lower
            or item.suffix.lower() in {".bin", ".lock", ".pyc", ".log", ".aux", ".bbl", ".blg", ".out"}
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
    if not V5_PACKAGE.is_dir():
        raise SystemExit(f"missing sanitized historical V5 package: {V5_PACKAGE}")
    if not PAPER_SOURCE.is_file():
        raise SystemExit("missing compiled V6 PDF")
    if UPLOAD.exists():
        if UPLOAD.resolve().parent != SUB.resolve():
            raise SystemExit(f"refusing to clear unexpected path: {UPLOAD}")
        shutil.rmtree(UPLOAD)
    if BUNDLE_ZIP.exists():
        BUNDLE_ZIP.unlink()
    UPLOAD.mkdir(parents=True)
    PACKAGE.mkdir(parents=True)

    shutil.copy2(PAPER_SOURCE, UPLOAD / "paper.pdf")
    copy_tree(V5_PACKAGE, "evidence/v5")
    for name in ["main.tex", "v6_hardening.tex", "IEEEtran.cls", "IEEEtran.bst", "references.bib"]:
        copy_file(SUB / name, f"manuscript/{name}", sanitize_text=name not in {"IEEEtran.cls", "IEEEtran.bst"})
    copy_tree(SUB / "sections", "manuscript/sections")
    copy_tree(V6_EVIDENCE, "evidence/v6/experiments")
    copy_tree(V6_REPORTS, "evidence/v6/reports")
    final_release_reports = [
        "FINAL_SCIENTIFIC_AUDIT.md",
        "FINAL_REFERENCE_AUDIT.md",
        "ICST2027_COMPLIANCE_AUDIT.md",
        "FINAL_ANONYMITY_AUDIT.md",
        "AUTHOR_SIGNOFF_CHECKLIST.md",
        "FINAL_SUBMISSION_READINESS.md",
    ]
    for name in final_release_reports:
        copy_file(SUB / name, f"evidence/v6/release/{name}")

    for source in [
        ROOT / "scripts" / "reproduce_v6.py",
        ROOT / "scripts" / "build_v6_reports.py",
        ROOT / "scripts" / "build_v6_package_manifest.py",
        ROOT / "scripts" / "verify_v6_package_manifest.py",
        ROOT / "scripts" / "verify_v6_scientific_accounting.py",
        ROOT / "scripts" / "audit_v6_manuscript_consistency.py",
        ROOT / "scripts" / "audit_v6_anonymity.py",
        ROOT / "scripts" / "record_v6_build_provenance.py",
        ROOT / "tests" / "test_v6_scientific_hardening.py",
        ROOT / "requirements-v6.txt",
        ROOT / ".github" / "workflows" / "v6.yml",
    ]:
        copy_file(source, f"reproduction/{source.name}")

    write_text("README.md", """# Anonymous A11yPreserve V6 replication package

This package accompanies the anonymous ICST 2027 Research Papers submission.
It preserves the sanitized historical V5 evidence and adds the V6 scientific
hardening layer: genuine no-op control reruns, destination mutation traces,
executable baselines and ablations, manuscript provenance, package checks, and
anonymity checks.

The frozen primary denominator remains 130 fixture--pipeline cases: 65 atomic
DOCX fixtures across LibreOffice and Google Docs. Microsoft Word remains a
separate post-freeze supplementary arm with 65 observations. V6 does not claim
PDF/UA conformance, human usability, natural-document generalization, temporal
Google repeatability, or external expert adjudication.

The manuscript source is under `manuscript/`; the anonymous PDF is `../paper.pdf`.
Run the V6 checks from a repository checkout with the original project layout.
Google Docs reproduction requires an authorized interactive session. Credentials,
cookies, browser profiles, account identifiers, and private paths are not
distributed. Root author/citation/license metadata is intentionally omitted from
this anonymous package pending human release decisions.
""")
    write_text("REPRODUCTION_NOTES.md", """# V6 reproduction notes

Run `python reproduction/reproduce_v6.py` from the original repository layout.
The scientific script genuinely reruns controls, mutations, and baselines; it
does not trust pre-existing aggregate JSON as the experimental computation.

The included PDF was built from the listed manuscript inputs using MiKTeX
pdfTeX and BibTeX. Source/PDF hashes and page count are recorded in
`evidence/v6/experiments/V6_PDF_BUILD_PROVENANCE.json`.

External converter/cloud reruns require the named local or authenticated
environments. No credentials or private browser state are included.
""")
    write_text("ANONYMITY_NOTICE.md", """# Anonymous release notice

Identity-bearing root `CITATION.cff` and placeholder `LICENSE` files are not
included. Authors must decide whether and how to add them after review. Before
upload, inspect the complete archive and HotCRP metadata for author names,
institutions, repository URLs, private paths, and account identifiers.
""")

    manifest = {}
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file() and path.name != "PACKAGE_MANIFEST.json":
            manifest[str(path.relative_to(PACKAGE)).replace("\\", "/")] = {"sha256": sha256(path), "size_bytes": path.stat().st_size}
    (PACKAGE / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    package_zip = UPLOAD / "replication_package.zip"
    with zipfile.ZipFile(package_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, str(Path("replication_package") / path.relative_to(PACKAGE)))
    upload_readme = UPLOAD / "UPLOAD_README.md"
    upload_readme.write_text("""# Anonymous ICST 2027 V6 upload bundle

- `paper.pdf`: anonymous 9-page IEEE conference-format manuscript.
- `replication_package.zip`: sanitized V5 historical evidence plus V6 evidence,
  source, scripts, and reproduction instructions.

Human authors must complete HotCRP authorship/COI, originality, simultaneous-
submission, licensing, and artifact-access decisions before upload.
""", encoding="utf-8")
    generated_from = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    generated_prefixes = (
        "submission/ICST2027_V6/upload_v6",
        "submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip",
        "submission/ICST2027_V6/.pdf-qa",
    )
    raw_working_tree_status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    working_tree_status = "\n".join(
        line for line in raw_working_tree_status.splitlines()
        if not any(prefix in line for prefix in generated_prefixes)
    )
    bundle_manifest = {
        "paper": {"path": "paper.pdf", "source": str(PAPER_SOURCE.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(UPLOAD / "paper.pdf"), "size_bytes": (UPLOAD / "paper.pdf").stat().st_size, "pages": 9},
        "replication_package": {"path": "replication_package.zip", "sha256": sha256(package_zip), "size_bytes": package_zip.stat().st_size, "files": len(manifest)},
        "generated_from_commit": generated_from,
        "working_tree_dirty": bool(working_tree_status.strip()),
        "working_tree_note": "Bundle generated from the current checkout; generated upload outputs are excluded from this status." if working_tree_status.strip() else "Bundle generated from a clean checkout apart from generated upload outputs.",
        "scientific_results_modified": False,
        "historical_v5_package_reused": True,
        "identity_bearing_root_metadata_included": False,
    }
    (UPLOAD / "BUNDLE_MANIFEST.json").write_text(json.dumps(bundle_manifest, indent=2) + "\n", encoding="utf-8")
    with zipfile.ZipFile(BUNDLE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ["paper.pdf", "replication_package.zip", "UPLOAD_README.md", "BUNDLE_MANIFEST.json"]:
            archive.write(UPLOAD / name, name)
    print(json.dumps({"status": "PASS", "package_files": len(manifest), "package_zip": str(package_zip), "bundle": str(BUNDLE_ZIP)}, indent=2))


if __name__ == "__main__":
    main()
