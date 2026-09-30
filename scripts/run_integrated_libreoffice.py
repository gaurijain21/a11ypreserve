from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "integrated_study"
RUNTIME = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.com"
OUTPUT = OUT / "outputs" / "libreoffice"
PROFILES = OUT / "lo_profiles"
SETTINGS = "UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    root = reader.trailer.get("/Root")
    return {"pages": len(reader.pages), "tagged": bool(root and root.get("/StructTreeRoot")), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PROFILES.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((OUT / "INTEGRATED_CONTRACTS.json").read_text(encoding="utf-8"))
    version_run = subprocess.run([str(RUNTIME), "--version"], capture_output=True, text=True, timeout=30)
    version = (version_run.stdout or version_run.stderr).strip()
    records = []
    for document in manifest["documents"]:
        source = ROOT / document["source_docx"]
        destination = OUTPUT / f"{document['document_id']}__LIBREOFFICE.pdf"
        profile = PROFILES / document["document_id"]
        profile.mkdir(parents=True, exist_ok=True)
        profile_uri = "file:///" + str(profile).replace("\\", "/")
        command = [str(RUNTIME), f"-env:UserInstallation={profile_uri}", "--headless", "--invisible", "--nodefault", "--nologo", "--nolockcheck", "--norestore", "--nofirststartwizard", "--convert-to", f"pdf:writer_pdf_Export:{SETTINGS}", "--outdir", str(OUTPUT), str(source)]
        started = datetime.now().astimezone().isoformat()
        run = subprocess.run(command, cwd=RUNTIME.parent, capture_output=True, text=True, timeout=180)
        generated = OUTPUT / f"{source.stem}.pdf"
        if generated.exists() and generated != destination:
            if destination.exists():
                destination.unlink()
            generated.replace(destination)
        record = {"document_id": document["document_id"], "source": document["source_docx"], "source_sha256": sha256(source), "pipeline": "LibreOffice", "converter_version": version, "settings": SETTINGS, "started_at": started, "completed_at": datetime.now().astimezone().isoformat(), "command_returncode": run.returncode, "stdout": run.stdout[-1000:], "stderr": run.stderr[-1000:], "destination": str(destination.relative_to(ROOT))}
        if destination.exists():
            record.update({"result": "SUCCESS", **inspect_pdf(destination)})
        else:
            record["result"] = "FAILED"
        records.append(record)
    result = {"pipeline": "LibreOffice", "records": records, "successful": sum(r["result"] == "SUCCESS" for r in records), "total": len(records)}
    (OUT / "LIBREOFFICE_RESULTS.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"pipeline": result["pipeline"], "successful": result["successful"], "total": result["total"], "tagged": [r.get("tagged") for r in records]}, indent=2))
    if result["successful"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
