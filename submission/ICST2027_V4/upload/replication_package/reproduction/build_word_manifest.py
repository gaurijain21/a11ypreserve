"""Build the provenance manifest for the supplementary Word GUI arm.

This script only inventories byte-preserving copies of PDFs produced by Word's
native GUI export. It does not create or modify PDF content.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
LOCAL = Path(r"<LOCAL_WORD_WORKSPACE>\word_inputs")
OUT_ROOT = ROOT / "experiments" / "v4" / "conversions" / "word" / "outputs"
MANIFEST_PATH = ROOT / "experiments" / "v4" / "conversions" / "word" / "manifest.json"
WORD_VERSION = "Microsoft 365 O365ProPlusRetail x64 build 16.0.20430.20092"
WINDOWS_VERSION = "Microsoft Windows NT 10.0.26200.0"
ROUTE = "Word GUI File -> Export -> Create PDF/XPS Document -> Create PDF/XPS"
SETTINGS = (
    "PDF; Standard optimization; all pages; Document; bookmarks/properties; "
    "Document structure tags for accessibility=true; Open file after publishing=false"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_info(path: Path) -> dict:
    raw_header = path.read_bytes()[:5]
    info = {
        "exists": path.exists(),
        "size_bytes": path.stat().st_size,
        "pdf_header": raw_header.decode("latin-1", errors="replace"),
        "sha256": sha256(path),
        "parseable": False,
        "page_count": None,
        "tagged": False,
        "producer": None,
        "creator": None,
    }
    try:
        reader = PdfReader(str(path))
        info["parseable"] = True
        info["page_count"] = len(reader.pages)
        metadata = reader.metadata or {}
        info["producer"] = str(metadata.get("/Producer")) if metadata.get("/Producer") else None
        info["creator"] = str(metadata.get("/Creator")) if metadata.get("/Creator") else None
        root = reader.trailer.get("/Root")
        info["tagged"] = bool(root and root.get("/StructTreeRoot"))
    except Exception as exc:  # retain diagnostic detail in the manifest
        info["parse_error"] = f"{type(exc).__name__}: {exc}"
    return info


def source_record(source_manifest: dict, fixture_id: str) -> dict:
    record = next(item for item in source_manifest["records"] if item["variant_id"] == fixture_id)
    repo_path = ROOT / Path(record["fixture"])
    local_path = LOCAL / repo_path.name
    selected = local_path if local_path.exists() else repo_path
    observed = sha256(selected)
    if observed.lower() != record["source_sha256"].lower():
        raise RuntimeError(f"source hash mismatch for {fixture_id}: {selected}")
    return {
        "feature_family": record["feature_family"],
        "role": record["role"],
        "source_path": record["fixture"].replace("\\", "/"),
        "source_sha256": observed,
        "local_source_path": str(selected),
    }


def realistic_source_record(realistic_manifest: dict, document_id: str) -> dict:
    record = next(item for item in realistic_manifest["records"] if item["document_id"] == document_id)
    repo_path = ROOT / Path(record["path"])
    local_path = LOCAL / repo_path.name
    selected = local_path if local_path.exists() else repo_path
    observed = sha256(selected)
    if observed.lower() != record["source_sha256"].lower():
        raise RuntimeError(f"source hash mismatch for {document_id}: {selected}")
    return {
        "source_path": record["path"].replace("\\", "/"),
        "source_sha256": observed,
        "local_source_path": str(selected),
        "provenance": record["provenance"],
        "contract_count": len(record["contracts"]),
    }


def output_record(corpus: str, identifier: str, source: dict, pdf_path: Path) -> dict:
    output = pdf_info(pdf_path)
    return {
        "corpus": corpus,
        "fixture_id" if corpus == "atomic" else "document_id": identifier,
        **source,
        "converter": "Microsoft Word desktop",
        "converter_version": WORD_VERSION,
        "windows_version": WINDOWS_VERSION,
        "route": ROUTE,
        "settings": SETTINGS,
        "output_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
        "output": output,
        "status": "SUCCESS" if output["parseable"] and output["size_bytes"] > 0 else "FAILURE",
        "retries": None,
        "failure_detail": None,
    }


def main() -> None:
    source_manifest = json.loads((ROOT / "experiments/v4/source_manifest.json").read_text(encoding="utf-8"))
    realistic_manifest = json.loads(
        (ROOT / "experiments/v4/realistic/REALISTIC_CORPUS_MANIFEST.json").read_text(encoding="utf-8")
    )
    records = []
    for i in range(1, 14):
        for variant in "ABCDE":
            fixture_id = f"F{i:02d}_{variant}"
            pdf_path = OUT_ROOT / "atomic" / f"{fixture_id}__WORD_DESKTOP.pdf"
            if not pdf_path.exists():
                raise RuntimeError(f"missing atomic output: {pdf_path}")
            records.append(output_record("atomic", fixture_id, source_record(source_manifest, fixture_id), pdf_path))
    for i in range(1, 11):
        document_id = f"R{i:02d}"
        pdf_path = OUT_ROOT / "realistic" / f"{document_id}__WORD_DESKTOP.pdf"
        if not pdf_path.exists():
            raise RuntimeError(f"missing realistic output: {pdf_path}")
        records.append(
            output_record("realistic", document_id, realistic_source_record(realistic_manifest, document_id), pdf_path)
        )
    manifest = {
        "manifest_version": "v4-word-gui-supplement-1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "converter": "Microsoft Word desktop",
        "converter_version": WORD_VERSION,
        "windows_version": WINDOWS_VERSION,
        "executable": r"<INSTALLED_APPLICATION>",
        "route": ROUTE,
        "settings": SETTINGS,
        "protocol": "experiments/v4/word_supplement/WORD_SUPPLEMENT_PROTOCOL.md",
        "primary_denominator_note": "Supplementary third-pipeline arm; frozen primary denominator remains 130 LibreOffice + Google cases.",
        "atomic_count": sum(1 for record in records if record["corpus"] == "atomic"),
        "realistic_count": sum(1 for record in records if record["corpus"] == "realistic"),
        "records": records,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(MANIFEST_PATH), "records": len(records), "atomic": manifest["atomic_count"], "realistic": manifest["realistic_count"]}, indent=2))


if __name__ == "__main__":
    main()
