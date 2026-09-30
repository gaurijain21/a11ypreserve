"""Freeze provenance for the completed V3 Google output arms.

This script records hashes and structural validation facts for already-created
PDFs.  It does not convert documents or modify any V2 evidence.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CORE = [
    "F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE",
    "F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE",
    "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE", "F11_FOOTNOTES",
    "F12_EQUATION", "F14_CAPTIONS",
]
SOURCE_DIRS = {fixture: (ROOT / "pilot" / "fixtures" if fixture in CORE[:4] else ROOT / "corpus" / "fixtures") for fixture in CORE}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_facts(path: Path) -> dict:
    raw = path.read_bytes()
    reader = PdfReader(str(path))
    root = reader.trailer.get("/Root")
    root = root.get_object() if hasattr(root, "get_object") else root
    tagged = bool(root and root.get("/StructTreeRoot") is not None)
    metadata = reader.metadata or {}
    return {
        "sha256": sha256(path),
        "file_size": len(raw),
        "page_count": len(reader.pages),
        "parseable": True,
        "pdf_header": raw[:5].decode("ascii", errors="replace"),
        "tagged": tagged,
        "producer": str(metadata.get("/Producer")) if metadata.get("/Producer") is not None else None,
        "creator": str(metadata.get("/Creator")) if metadata.get("/Creator") is not None else None,
    }


def record(fixture: str, source: Path, output: Path, *, run: str, route: str) -> dict:
    facts = pdf_facts(output)
    return {
        "fixture_id": fixture,
        "source": str(source.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha256(source),
        "run": run,
        "pipeline": "Google Docs DOCX-to-PDF conversion pipeline",
        "workflow": "Google Docs Open file -> Upload -> Browse -> PDF export",
        "export_route": route,
        "browser_version": "not captured in the conversion log",
        "operating_system": "Windows (native file chooser interaction)",
        "google_backend_version": "not observable/pinnable",
        "recorded_at_utc": datetime.fromtimestamp(output.stat().st_mtime, tz=timezone.utc).isoformat(),
        "destination": str(output.relative_to(ROOT)).replace("\\", "/"),
        "output": facts,
    }


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    runs: list[dict] = []
    for run, directory_name in (("R2", "run2"), ("R3", "run3")):
        directory = ROOT / "v3" / "google_repeatability" / directory_name
        for fixture in CORE:
            source = SOURCE_DIRS[fixture] / f"{fixture}.docx"
            output = directory / f"{fixture}__GOOGLE_DOCS__{run}.pdf"
            if not source.exists() or not output.exists():
                raise SystemExit(f"missing required Core file: {source} or {output}")
            runs.append(record(fixture, source, output, run=run, route="visible Google Docs UI File -> Download -> PDF"))
    payload = {
        "manifest_version": "v3-google-run-manifest-1",
        "generated_at_utc": generated,
        "scope": "V3 Core repeatability; historical Run 1 remains frozen V2 evidence",
        "run_1_reference": "results/full_experiment/outputs/google_docs",
        "records": runs,
        "validation": {"expected_new_outputs": 26, "recorded_new_outputs": len(runs), "all_parseable": all(x["output"]["parseable"] for x in runs), "all_tagged": all(x["output"]["tagged"] for x in runs)},
        "notes": [
            "Runs 2 and 3 were independently uploaded through the authenticated Google Docs workflow.",
            "Google service backend version was not observable and is not claimed.",
            "This manifest does not alter any V2 output, manifest, or classification.",
        ],
    }
    target = ROOT / "v3" / "google_repeatability" / "RUN_MANIFEST.json"
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    records = []
    for index in range(1, 14):
        variant = f"B{index:02d}"
        source = ROOT / "corpus" / "v3_variant_set_b" / "fixtures" / f"{variant}.docx"
        output = ROOT / "v3" / "variant_set_b" / "google" / "outputs" / f"{variant}__GOOGLE_DOCS.pdf"
        if not source.exists() or not output.exists():
            raise SystemExit(f"missing required Variant B file: {source} or {output}")
        records.append(record(variant, source, output, run="single_variant_run", route="authenticated Google Docs export backend recovery after UI download did not register"))
    report = {
        "report_version": "v3-google-variant-conversion-report-1",
        "generated_at_utc": generated,
        "converter": "Google Docs DOCX-to-PDF conversion pipeline",
        "variant_count": len(records),
        "records": records,
        "validation": {"expected_outputs": 13, "recorded_outputs": len(records), "all_parseable": all(x["output"]["parseable"] for x in records), "all_tagged": all(x["output"]["tagged"] for x in records)},
        "route_disclosure": "For B01-B13, the authenticated Google Docs session accepted each exact DOCX upload. The visible File -> Download -> PDF action did not register a Chrome download for B01 despite retries, so the in-session Google Docs export backend was used for the saved PDF outputs. This is disclosed as a workflow deviation; no print-to-PDF, screenshot, or manual editing was used.",
        "notes": [
            "The Google backend version was not observable/pinnable.",
            "These outputs are V3 secondary evidence and do not rewrite V2 files.",
        ],
    }
    target = ROOT / "v3" / "variant_set_b" / "google" / "CONVERSION_REPORT.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_manifest": str(ROOT / "v3/google_repeatability/RUN_MANIFEST.json"), "run_records": len(runs), "variant_report": str(target), "variant_records": len(records)}, indent=2))


if __name__ == "__main__":
    main()
