from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
V5 = ROOT / "experiments" / "v5"
RUNTIME = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.com"
RUNTIME_EXE = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.exe"
SETTINGS = "UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=0"
OUT = V5 / "conversions" / "libreoffice_profile_b"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_facts(path: Path) -> dict:
    raw = path.read_bytes()
    facts = {
        "exists": path.exists(),
        "size_bytes": len(raw),
        "pdf_header": raw[:5].decode("ascii", errors="replace"),
        "sha256": sha256(path),
        "raw_pdfa_markers": {marker.decode("ascii"): raw.count(marker) for marker in (b"pdfaid:part", b"GTS_PDFA1", b"PDF/A")},
    }
    try:
        reader = PdfReader(str(path))
        root = reader.trailer.get("/Root")
        root = root.get_object() if hasattr(root, "get_object") else root
        metadata = reader.metadata or {}
        facts.update({
            "parseable": True,
            "page_count": len(reader.pages),
            "tagged": bool(root and root.get("/StructTreeRoot") is not None),
            "document_language": str(root.get("/Lang")) if root and root.get("/Lang") else None,
            "producer": str(metadata.get("/Producer")) if metadata.get("/Producer") is not None else None,
            "creator": str(metadata.get("/Creator")) if metadata.get("/Creator") is not None else None,
            "pdf_version": reader.pdf_header,
        })
    except Exception as exc:
        facts.update({"parseable": False, "page_count": None, "tagged": None, "document_language": None, "producer": None, "creator": None, "pdf_version": None, "parse_error": repr(exc)})
    return facts


def executable_and_version() -> tuple[str, str]:
    for executable in (RUNTIME, RUNTIME_EXE):
        if executable.exists():
            try:
                run = subprocess.run([str(executable), "--version"], cwd=executable.parent, capture_output=True, text=True, timeout=30)
                version = (run.stdout or run.stderr).strip()
                if version:
                    return str(executable), version
            except Exception:
                pass
    return str(RUNTIME), "unavailable"


def convert(entry: dict, executable: str, version: str, reuse_existing: bool = False) -> dict:
    fixture = entry["variant_id"]
    source = ROOT / entry["fixture"]
    destination = OUT / "outputs" / f"{fixture}__LIBREOFFICE_PROFILE_B.pdf"
    profile = OUT / "profiles" / fixture
    staging = OUT / "staging" / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    profile.mkdir(parents=True, exist_ok=True)
    staging.parent.mkdir(parents=True, exist_ok=True)
    result = "SUCCESS"
    error = None
    stdout = stderr = ""
    started = datetime.now(timezone.utc)
    source_hash = sha256(source)
    if source_hash != entry["source_sha256"]:
        result, error = "FAILED", f"source hash mismatch: {source_hash} != {entry['source_sha256']}"
    elif reuse_existing and destination.exists():
        stdout = "reused existing V5 profile-B output"
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
                result, error = "FAILED", f"returncode={run.returncode}; stdout={stdout[-1000:]}; stderr={stderr[-1000:]}"
        except Exception as exc:
            result, error = "FAILED", repr(exc)
    facts = pdf_facts(destination) if destination.exists() else {"exists": False, "sha256": None, "parseable": False}
    if result == "SUCCESS" and (not facts.get("parseable") or facts.get("page_count", 0) <= 0 or facts.get("pdf_header") != "%PDF-"):
        result, error = "FAILED", "output validation gate failed"
    return {
        "corpus": "atomic", "fixture_id": fixture, "feature_family": entry["feature_family"], "role": entry["role"],
        "source_path": entry["fixture"], "source_sha256": source_hash, "expected_source_sha256": entry["source_sha256"],
        "converter": "LibreOffice", "condition": "V5_PROFILE_B", "converter_version": version, "executable": "<LOCAL_LIBREOFFICE_RUNTIME>",
        "settings": SETTINGS, "route": "headless soffice writer_pdf_Export with isolated profile",
        "started_at": started.isoformat(), "completed_at": datetime.now(timezone.utc).isoformat(),
        "output_path": str(destination.relative_to(ROOT)).replace("\\", "/"), "output": facts,
        "status": result, "error": error, "stdout_tail": stdout[-1000:], "stderr_tail": stderr[-1000:], "environment": platform.platform(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--reuse-existing", action="store_true")
    args = parser.parse_args()
    executable, version = executable_and_version()
    if not Path(executable).exists():
        raise SystemExit(f"LibreOffice runtime not found: {executable}")
    manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    entries = manifest["records"][: args.limit] if args.limit else manifest["records"]
    rows = [convert(entry, executable, version, reuse_existing=args.reuse_existing) for entry in entries]
    payload = {
        "manifest_version": "v5-libreoffice-profile-b-1", "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "converter": "LibreOffice", "condition": "V5_PROFILE_B", "settings": SETTINGS,
        "converter_version": version, "executable": "<LOCAL_LIBREOFFICE_RUNTIME>", "records": rows,
        "total": len(rows), "successful": sum(row["status"] == "SUCCESS" for row in rows), "failed": sum(row["status"] != "SUCCESS" for row in rows),
        "pdf_profile_interpretation": "SelectPdfVersion=0 is the documented default PDF 1.7 selection, not PDF/A.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("total", "successful", "failed", "condition", "settings")}, indent=2))
    if payload["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
