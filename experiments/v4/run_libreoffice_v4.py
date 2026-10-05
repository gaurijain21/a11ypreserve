from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.com"
RUNTIME_EXE = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.exe"
SETTINGS = "UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"
V4_MANIFEST = ROOT / "experiments" / "v4" / "source_manifest.json"
REALISTIC_MANIFEST = ROOT / "experiments" / "v4" / "realistic" / "REALISTIC_CORPUS_MANIFEST.json"
BASE = ROOT / "experiments" / "v4" / "conversions" / "libreoffice"
OUTPUT = BASE / "outputs"
STAGING = BASE / "staging"
PROFILES = BASE / "profiles"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def pdf_facts(path: Path) -> dict:
    raw = path.read_bytes()
    facts = {"exists": path.exists(), "size_bytes": len(raw), "pdf_header": raw[:5].decode("ascii", errors="replace"), "sha256": sha256(path)}
    try:
        reader = PdfReader(str(path))
        root = reader.trailer.get("/Root")
        root = root.get_object() if hasattr(root, "get_object") else root
        metadata = reader.metadata or {}
        facts.update({
            "parseable": True,
            "page_count": len(reader.pages),
            "tagged": bool(root and root.get("/StructTreeRoot") is not None),
            "producer": str(metadata.get("/Producer")) if metadata.get("/Producer") is not None else None,
            "creator": str(metadata.get("/Creator")) if metadata.get("/Creator") is not None else None,
        })
    except Exception as exc:
        facts.update({"parseable": False, "page_count": None, "tagged": None, "producer": None, "creator": None, "parse_error": repr(exc)})
    return facts

def version() -> tuple[str, str]:
    for executable in (RUNTIME, RUNTIME_EXE):
        if executable.exists():
            try:
                run = subprocess.run([str(executable), "--version"], cwd=executable.parent, capture_output=True, text=True, timeout=30)
                text = (run.stdout or run.stderr).strip()
                if text:
                    return str(executable), text
            except Exception:
                continue
    return str(RUNTIME), "unavailable"

def source_records(include_realistic: bool) -> list[dict]:
    payload = json.loads(V4_MANIFEST.read_text(encoding="utf-8"))
    records = []
    for entry in payload["records"]:
        records.append({"corpus": "atomic", "fixture_id": entry["variant_id"], "source": ROOT / entry["fixture"], "expected_source_sha256": entry["source_sha256"]})
    if include_realistic:
        realistic = json.loads(REALISTIC_MANIFEST.read_text(encoding="utf-8"))
        for entry in realistic["records"]:
            records.append({"corpus": "realistic", "fixture_id": entry["document_id"], "source": ROOT / entry["path"], "expected_source_sha256": entry["source_sha256"]})
    return records

def convert(record: dict, executable: str, converter_version: str) -> dict:
    source = record["source"]
    fixture = record["fixture_id"]
    corpus = record["corpus"]
    destination = OUTPUT / corpus / f"{fixture}__LIBREOFFICE.pdf"
    staging = STAGING / corpus / source.name
    profile = PROFILES / corpus / fixture
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging.parent.mkdir(parents=True, exist_ok=True)
    profile.mkdir(parents=True, exist_ok=True)
    source_hash = sha256(source) if source.exists() else None
    expected_hash = record["expected_source_sha256"]
    start = datetime.now(timezone.utc)
    started_epoch = start.timestamp()
    result = "SUCCESS"
    error = None
    stdout = stderr = ""
    if not source.exists():
        result, error = "FAILED", "source does not exist"
    elif source_hash != expected_hash:
        result, error = "FAILED", f"source hash mismatch: expected {expected_hash}, observed {source_hash}"
    else:
        shutil.copy2(source, staging)
        profile_uri = "file:///" + str(profile).replace("\\", "/")
        command = [executable, f"-env:UserInstallation={profile_uri}", "--headless", "--invisible", "--nodefault", "--nologo", "--nolockcheck", "--norestore", "--nofirststartwizard", "--convert-to", f"pdf:writer_pdf_Export:{SETTINGS}", "--outdir", str(destination.parent), str(staging)]
        try:
            run = subprocess.run(command, cwd=Path(executable).parent, capture_output=True, text=True, timeout=180)
            stdout, stderr = run.stdout, run.stderr
            generated = destination.parent / f"{staging.stem}.pdf"
            if generated.exists() and generated != destination:
                if destination.exists():
                    destination.unlink()
                generated.replace(destination)
            if run.returncode != 0 or not destination.exists():
                result, error = "FAILED", f"returncode={run.returncode}; stdout={stdout[-1200:]}; stderr={stderr[-1200:]}"
        except Exception as exc:
            result, error = "FAILED", repr(exc)
    facts = pdf_facts(destination) if destination.exists() else {"exists": False, "size_bytes": None, "pdf_header": None, "sha256": None, "parseable": False, "page_count": None, "tagged": None, "producer": None, "creator": None}
    if result == "SUCCESS":
        if facts.get("size_bytes", 0) <= 0 or facts.get("pdf_header") != "%PDF-" or not facts.get("parseable") or facts.get("page_count", 0) <= 0:
            result, error = "FAILED", "output validation gate failed"
        elif destination.stat().st_mtime < started_epoch:
            result, error = "FAILED", "output timestamp predates conversion start"
    return {
        "corpus": corpus, "fixture_id": fixture, "source_path": str(source.relative_to(ROOT)).replace("\\", "/"), "source_sha256": source_hash, "expected_source_sha256": expected_hash,
        "converter": "LibreOffice", "converter_version": converter_version, "executable": executable, "settings": SETTINGS, "route": "V3-reconstructed headless soffice.com writer_pdf_Export with isolated profile",
        "started_at": start.isoformat(), "completed_at": datetime.now(timezone.utc).isoformat(), "output_path": str(destination.relative_to(ROOT)).replace("\\", "/"), "output": facts,
        "status": result, "error": error, "stdout_tail": stdout[-1200:], "stderr_tail": stderr[-1200:], "environment": platform.platform(),
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", type=int, default=None, help="convert only the first N atomic records")
    parser.add_argument("--include-realistic", action="store_true")
    args = parser.parse_args()
    if not RUNTIME.exists() and not RUNTIME_EXE.exists():
        raise SystemExit(f"LibreOffice runtime not found: {RUNTIME}")
    executable, converter_version = version()
    records = source_records(args.include_realistic)
    if args.pilot is not None:
        records = records[:args.pilot]
    rows = [convert(record, executable, converter_version) for record in records]
    payload = {"manifest_version": "v4-libreoffice-conversion-1", "generated_at_utc": datetime.now(timezone.utc).isoformat(), "converter": "LibreOffice", "converter_version": converter_version, "executable": executable, "settings": SETTINGS, "records": rows, "total": len(rows), "successful": sum(row["status"] == "SUCCESS" for row in rows), "failed": sum(row["status"] != "SUCCESS" for row in rows)}
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"total": payload["total"], "successful": payload["successful"], "failed": payload["failed"], "manifest": str(BASE / "manifest.json")}, indent=2))
    if payload["failed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
