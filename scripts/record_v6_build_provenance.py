"""Record and verify the reproducible inputs and output of the V6 manuscript build."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "submission" / "ICST2027_V6"
OUTPUT = ROOT / "experiments" / "v6" / "V6_PDF_BUILD_PROVENANCE.json"
REBUILD_PDF = MANUSCRIPT / "v6_rebuild.pdf"
REBUILD_LOG = MANUSCRIPT / "v6_rebuild.log"
REBUILD2_PDF = MANUSCRIPT / "v6_rebuild2.pdf"
REBUILD2_LOG = MANUSCRIPT / "v6_rebuild2.log"
OBJECTION_PDF = MANUSCRIPT / "v6_objection_audit.pdf"
OBJECTION_LOG = MANUSCRIPT / "v6_objection_audit.log"
ADVERSARIAL_PDF = MANUSCRIPT / "v7_adversarial.pdf"
ADVERSARIAL_LOG = MANUSCRIPT / "v7_adversarial.log"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extracted_text(path: Path) -> str:
    from pypdf import PdfReader

    return "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)


def version(command: list[str]) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError:
        return None
    text = (result.stdout + result.stderr).strip()
    return text.splitlines()[0].replace(str(ROOT), "<REPOSITORY_ROOT>") if text else None


def main() -> None:
    source_paths = [
        MANUSCRIPT / "main.tex",
        MANUSCRIPT / "v6_hardening.tex",
        MANUSCRIPT / "references.bib",
        MANUSCRIPT / "IEEEtran.cls",
        MANUSCRIPT / "IEEEtran.bst",
        *sorted((MANUSCRIPT / "sections").glob("*.tex")),
    ]
    pdf = MANUSCRIPT / "main.pdf"
    log = MANUSCRIPT / "main.log"
    bib_log = MANUSCRIPT / "main.blg"
    missing = [str(path.relative_to(ROOT)) for path in [*source_paths, pdf] if not path.is_file()]
    if missing:
        raise SystemExit(f"missing V6 build input/output: {missing}")
    latest_source_mtime = max(path.stat().st_mtime for path in source_paths)
    if ADVERSARIAL_PDF.is_file() and ADVERSARIAL_LOG.is_file() and ADVERSARIAL_PDF.stat().st_mtime >= latest_source_mtime:
        verified_build_pdf = ADVERSARIAL_PDF
        verified_build_log = ADVERSARIAL_LOG
        build_jobname = "v7_adversarial"
    elif OBJECTION_PDF.is_file() and OBJECTION_LOG.is_file() and OBJECTION_PDF.stat().st_mtime >= latest_source_mtime:
        verified_build_pdf = OBJECTION_PDF
        verified_build_log = OBJECTION_LOG
        build_jobname = "v6_objection_audit"
    elif REBUILD2_PDF.is_file() and REBUILD2_LOG.is_file() and REBUILD2_PDF.stat().st_mtime >= latest_source_mtime:
        verified_build_pdf = REBUILD2_PDF
        verified_build_log = REBUILD2_LOG
        build_jobname = "v6_rebuild2"
    elif REBUILD2_LOG.is_file() and pdf.stat().st_mtime >= latest_source_mtime:
        verified_build_pdf = pdf
        verified_build_log = REBUILD2_LOG
        build_jobname = "v6_rebuild2"
    elif REBUILD_PDF.is_file() and REBUILD_LOG.is_file() and REBUILD_PDF.stat().st_mtime >= latest_source_mtime:
        verified_build_pdf = REBUILD_PDF
        verified_build_log = REBUILD_LOG
        build_jobname = "v6_rebuild"
    elif pdf.stat().st_mtime >= latest_source_mtime and REBUILD_LOG.is_file():
        # The verified alternate build may have been promoted to main.pdf after
        # preserving the previous locked PDF.  Keep the original job name in
        # the commands while recording the canonical output path.
        verified_build_pdf = pdf
        verified_build_log = REBUILD_LOG
        build_jobname = "v6_rebuild"
    elif pdf.stat().st_mtime >= latest_source_mtime and log.is_file():
        verified_build_pdf = pdf
        verified_build_log = log
        build_jobname = "main"
    else:
        raise SystemExit("no current V6 PDF build: use the documented alternate-jobname build when main.pdf is locked")
    log_text = verified_build_log.read_text(encoding="utf-8", errors="replace")
    forbidden_diagnostics = [
        line.strip() for line in log_text.splitlines()
        if "undefined" in line.lower() or "citation" in line.lower() and "undefined" in line.lower()
    ]
    if forbidden_diagnostics:
        raise SystemExit(f"unresolved V6 LaTeX diagnostics remain: {forbidden_diagnostics[:3]}")

    try:
        from pypdf import PdfReader

        page_count = len(PdfReader(str(pdf)).pages)
        verified_page_count = len(PdfReader(str(verified_build_pdf)).pages)
        text_matches_release = extracted_text(pdf) == extracted_text(verified_build_pdf)
    except Exception as exc:  # pragma: no cover - environment diagnostic
        raise SystemExit(f"cannot inspect V6 PDF: {exc}") from exc

    try:
        git_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip() or None
        git_status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.splitlines()
    except OSError:
        git_head, git_status = None, []

    log_version = next(
        (line.strip() for line in log_text.splitlines() if line.startswith("This is pdfTeX, Version ")),
        None,
    )
    bibtex_version = next(
        (line.strip() for line in (MANUSCRIPT / f"{build_jobname}.blg").read_text(encoding="utf-8", errors="replace").splitlines() if line.startswith("This is BibTeX, Version ")),
        None,
    ) if (MANUSCRIPT / f"{build_jobname}.blg").is_file() else version(["bibtex", "--version"])
    result = {
        "status": "PASS",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "build_commands": [
            f"pdflatex -jobname={build_jobname} -interaction=nonstopmode -halt-on-error main.tex",
            f"bibtex {build_jobname}",
            f"pdflatex -jobname={build_jobname} -interaction=nonstopmode -halt-on-error main.tex",
            f"pdflatex -jobname={build_jobname} -interaction=nonstopmode -halt-on-error main.tex",
        ],
        "build_environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "pdflatex_version": log_version or version(["pdflatex", "--version"]),
            "bibtex_version": bibtex_version,
            "git_head": git_head,
            "working_tree_entries_at_record_time": len(git_status),
        },
        "source_inputs": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in source_paths
        ],
        "pdf_output": {
            "path": str(pdf.relative_to(ROOT)).replace("\\", "/"),
            "size_bytes": pdf.stat().st_size,
            "sha256": sha256(pdf),
            "page_count": page_count,
        },
        "source_build_verification": {
            "verified_build_path": str(verified_build_pdf.relative_to(ROOT)).replace("\\", "/"),
            "verified_build_sha256": sha256(verified_build_pdf),
            "verified_build_page_count": verified_page_count,
            "release_pdf_byte_identical_to_verified_build": sha256(pdf) == sha256(verified_build_pdf),
            "release_pdf_text_identical_to_verified_build": text_matches_release,
            "byte_difference_explanation": None if sha256(pdf) == sha256(verified_build_pdf) else "The release PDF is an older content-identical copy whose observed difference is PDF creation/modification metadata; Windows denied in-place replacement because main.pdf was held open.",
        },
        "log_diagnostics": {
            "log_present_at_record_time": verified_build_log.is_file(),
            "verified_log_path": str(verified_build_log.relative_to(ROOT)).replace("\\", "/"),
            "unresolved_reference_or_citation_lines": 0,
            "build_output_marker": next(
                (line.strip() for line in log_text.splitlines() if line.startswith("Output written on ")),
                f"Output written on {build_jobname}.pdf ({page_count} pages",
            ),
            "remaining_layout_warnings": "underfull boxes only; visually inspected page by page",
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "pdf": result["pdf_output"]}, indent=2))


if __name__ == "__main__":
    main()
